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


# ---------------------------------------------------------------------------
# Gabarit « deux zones » (zone a sur 3 colonnes, zone b sur 2 colonnes),
# partagé par git-linux, windows-powershell et as400.
# ---------------------------------------------------------------------------
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "build" / "html"

# Couleurs de fond et de texte communes ; chaque fond d'écran ajoute ses
# accents --a (zone gauche), --b (zone droite) et --param.
BASE_THEMES = {
    # Aritim Dark (palette Plasma de Mrcuve0/Aritim-Dark)
    "aritim": """
  --bg:#10151a; --bg2:#141a21; --grid:rgba(146,152,165,.04);
  --panel:rgba(20,26,33,.96); --border:#2f343f;
  --text:#d3dae3; --text2:#bcc3ce; --muted:#9298a5; --hl:rgba(43,82,120,.45); --warn:#da4453;""",
    "dark": """
  --bg:#0c1220; --bg2:#111a2d; --grid:rgba(140,170,220,.05);
  --panel:rgba(19,28,46,.94); --border:rgba(130,160,210,.16);
  --text:#cdd5e3; --text2:#b3bccb; --muted:#8792a8; --hl:rgba(255,255,255,.075); --warn:#ff6ad5;""",
    "light": """
  --bg:#f2eee5; --bg2:#e9e4d8; --grid:rgba(60,70,90,.06);
  --panel:rgba(252,250,245,.96); --border:rgba(60,70,90,.16);
  --text:#1c2230; --text2:#3a4152; --muted:#5a6273; --hl:rgba(30,40,60,.07); --warn:#b0128a;""",
    # AMOLED : noir pur, aucun dégradé ni grille (pixels éteints), texte adouci
    "amoled": """
  --bg:#000000; --bg2:#000000; --grid:transparent;
  --panel:#000000; --border:#232a33;
  --text:#aab2be; --text2:#929aa7; --muted:#6f7886; --hl:#14171c; --warn:#d85cb8;""",
}

MONO = '"MesloLGS Nerd Font","MesloLGS NF","MesloLGS Nerd Font Mono","DejaVu Sans Mono",monospace'

TWO_ZONE_TEMPLATE = """<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8"><title>__TITLE__ — fond d'écran (__THEME__)</title>
<style>
:root { __VARS__ }
* { box-sizing:border-box; margin:0; padding:0; }
html,body { width:2560px; height:1440px; overflow:hidden; }
body {
  font-family:"Inter",sans-serif; color:var(--text);
  background:
    linear-gradient(var(--grid) 1px, transparent 1px) 0 0/40px 40px,
    linear-gradient(90deg, var(--grid) 1px, transparent 1px) 0 0/40px 40px,
    linear-gradient(160deg, var(--bg), var(--bg2));
  padding:56px 60px; display:flex; gap:44px;
}
.k, .tag, .brand small, .prompt { font-family:__MONO__; }
.zone { display:flex; flex-direction:column; gap:20px; min-width:0; }
.zone.a { flex:3 1 0; }
.zone.b { flex:2 1 0; }
.brand { display:flex; align-items:center; gap:18px; height:54px; padding:0 4px; }
.brand h2 { font-family:"Inter Display","Inter",sans-serif; font-weight:800; font-size:50px; letter-spacing:.04em; line-height:1; }
.a .brand h2 { color:var(--a); }
.b .brand h2 { color:var(--b); }
.graph { width:120px; height:48px; }
.prompt { color:var(--muted); font-weight:normal; letter-spacing:0; margin-right:16px; }
.cursor { display:inline-block; width:22px; height:44px; background:currentColor; border-radius:2px; margin-left:8px; vertical-align:-4px; }
.cursor.under { height:7px; vertical-align:0; }
.brand small { font-size:17px; color:var(--muted); margin-top:12px; }
.brand small i { font-style:normal; color:var(--param); font-weight:bold; }
.b .brand { justify-content:flex-end; }
.cols { display:grid; gap:18px; flex:1; min-height:0; }
.a .cols { grid-template-columns:repeat(3,minmax(0,1fr)); }
.b .cols { grid-template-columns:repeat(2,minmax(0,1fr)); }
.col { display:flex; flex-direction:column; justify-content:space-between; gap:14px; min-height:0; }
.panel { background:var(--panel); border:1px solid var(--border); border-radius:12px; padding:12px 18px 13px; position:relative; }
.panel::before { content:""; position:absolute; left:0; top:13px; bottom:13px; width:3px; border-radius:0 3px 3px 0; }
.panel.a::before { background:var(--a); }
.panel.b::before { background:var(--b); }
.panel header { display:flex; justify-content:space-between; align-items:baseline; margin-bottom:6px; gap:10px; }
.panel h3 { font-size:20px; font-weight:700; white-space:nowrap; }
.panel.a h3 { color:var(--a); }
.panel.b h3 { color:var(--b); }
.tag { font-size:16px; color:var(--muted); white-space:nowrap; }
.rows { display:grid; grid-template-columns:var(--kw,178px) 1fr; column-gap:14px; align-items:baseline; }
.k { font-size:17px; white-space:pre; line-height:26px; overflow:hidden; }
.a .k { color:var(--a); }
.b .k { color:var(--b); }
.k i { font-style:normal; color:var(--param); }
.d { font-size:16px; line-height:26px; white-space:nowrap; overflow:hidden; }
.warn { color:var(--warn); font-weight:normal; }
__COMMON_CSS__
</style></head>
<body>
  <div class="zone a">
    <div class="brand">__BRAND_A__</div>
    <div class="cols">__ACOLS__</div>
  </div>
  <div class="zone b">
    <div class="brand">__BRAND_B__</div>
    <div class="cols">__BCOLS__</div>
  </div>
</body></html>
"""


def build_two_zones(slug, title, accents, brand_a, brand_b, cols_a, cols_b, tag_prefix_a="", tag_prefix_b=""):
    """Écrit build/html/<slug>-<thème>.html pour chaque thème de BASE_THEMES.

    accents : {thème: "--a:…; --b:…; --param:…;"}
    """
    OUT.mkdir(parents=True, exist_ok=True)
    for theme, base in BASE_THEMES.items():
        doc = (TWO_ZONE_TEMPLATE
               .replace("__COMMON_CSS__", CSS).replace("__MONO__", MONO)
               .replace("__TITLE__", html.escape(title)).replace("__THEME__", theme)
               .replace("__VARS__", base + "\n  " + accents[theme].strip())
               .replace("__BRAND_A__", brand_a).replace("__BRAND_B__", brand_b)
               .replace("__ACOLS__", columns(cols_a, "a", tag_prefix_a))
               .replace("__BCOLS__", columns(cols_b, "b", tag_prefix_b)))
        (OUT / f"{slug}-{theme}.html").write_text(doc, encoding="utf-8")
    print(f"ok  {slug}")
