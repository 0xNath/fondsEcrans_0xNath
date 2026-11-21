"""Rendu commun aux deux fonds d'écran.

Conventions dans les listes de commandes :
  "§cmd"      -> commande essentielle (mise en avant)
  «x»         -> paramètre (couleur secondaire)
  "⚠ desc"    -> commande destructive
  "desc [GNU]" -> badge de compatibilité en fin de description
"""
import html
import re

CSS = """
.rows { display:grid; grid-template-columns:calc(var(--kw,178px) + 14px) 1fr; column-gap:0; align-items:baseline; }
.k { padding-right:14px; }
.k.ess, .d.ess { background:var(--hl); }
.k.ess { font-weight:bold; border-radius:5px 0 0 5px; margin-left:-6px; padding-left:6px; }
.d.ess { color:var(--text); border-radius:0 5px 5px 0; margin-right:-6px; padding-right:6px; }
.d { color:var(--text2); }
.warn { color:var(--warn); font-weight:bold; }
.badge { font-family:"MesloLGS Nerd Font","MesloLGS NF","MesloLGS Nerd Font Mono","DejaVu Sans Mono",monospace; font-size:16px; color:var(--muted); border:1px solid var(--border); border-radius:4px; padding:0 4px; margin-left:6px; }
.ess-key { display:inline-block; width:34px; height:20px; background:var(--hl); border-radius:4px; vertical-align:-3px; margin-right:6px; }
"""


def fmt_cmd(s):
    return re.sub(r"«(.*?)»", r"<i>\1</i>", html.escape(s, quote=False))


def fmt_desc(s):
    badge = ""
    m = re.search(r"\s\[([^\]]+)\]$", s)
    if m:
        badge = f'<span class="badge">{html.escape(m.group(1))}</span>'
        s = s[: m.start()]
    if s.startswith("⚠ "):
        return f'<span class="warn">⚠</span> {html.escape(s[2:])}{badge}'
    return html.escape(s) + badge


def rows_html(rows):
    out = []
    for k, d in rows:
        ess = k.startswith("§")
        k = k[1:] if ess else k
        c = " ess" if ess else ""
        out.append(f'<div class="k{c}">{fmt_cmd(k)}</div><div class="d{c}">{fmt_desc(d)}</div>')
    return "".join(out)


def panel(title, tag, kw, rows, side, tag_prefix=""):
    if tag.startswith("="):
        tag, tag_prefix = tag[1:], ""
    tag_html = f'<span class="tag">{html.escape(tag_prefix + tag)}</span>' if tag else ""
    style = f' style="--kw:{kw}px"' if kw else ""
    return (f'<section class="panel {side}"{style}><header><h3>{html.escape(title)}</h3>{tag_html}</header>'
            f'<div class="rows">{rows_html(rows)}</div></section>')


def columns(cols, side, tag_prefix=""):
    return "".join('<div class="col">' + "".join(panel(*p, side, tag_prefix=tag_prefix) for p in c) + "</div>"
                   for c in cols)
