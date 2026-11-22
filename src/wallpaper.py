"""Modèle et rendu HTML des fonds d'écran : deux zones, deux orientations, thèmes, langues.

Un fond d'écran (src/content/*.py) déclare un `Wallpaper` : une zone gauche/haute (`left`)
et une zone droite/basse (`right`), chacune avec son bandeau (`Brand`) et ses colonnes de
panneaux. Un panneau est un tuple (titre, étiquette, largeur colonne commande en px ou None, lignes)
et une ligne un tuple (commande, description).

Conventions dans les lignes :
  "§cmd"        commande essentielle (mise en avant)
  «x»           paramètre (couleur secondaire, traduit s'il fait 2 caractères ou plus)
  "⚠ desc"      commande destructive
  "desc [GNU]"  badge de compatibilité en fin de description

Traduction (voir i18n.py) : les titres de panneaux, descriptions, sous-titres des bandeaux
et paramètres sont traduits. Les étiquettes de panneaux et les titres des bandeaux sont du
code, gardés tels quels, sauf s'ils sont écrits T("…").
"""
import html
import re
from dataclasses import dataclass

ORIENTATIONS = {"landscape": (2560, 1440), "portrait": (1440, 2560)}
PORTRAIT_COLUMNS = 3


class T(str):
    """Texte à traduire là où on garde d'habitude le texte tel quel (étiquette, titre de bandeau)."""


@dataclass
class Brand:
    title: str                 # titre du bandeau (code, sauf T("…"))
    prompt: str = ""           # invite affichée avant le titre, ex. "PS>"
    cursor: str = ""           # "", "block" ou "under"
    svg: str = ""              # petit dessin après le titre
    note: str = ""             # sous-titre (traduit)
    legend: str = "default"    # zone gauche : "default", "vim" ou ""
    warn: str = "destructive"  # libellé du ⚠ dans la légende (traduit)


@dataclass
class Zone:
    brand: Brand
    columns: list              # colonnes de panneaux, telles qu'affichées en paysage
    tag_prefix: str = ""       # préfixe des étiquettes, ex. ":h " (une étiquette "=…" s'en passe)
    footer: tuple = None       # panneau pleine largeur en bas de zone : (titre, étiquette, lignes)


@dataclass
class Wallpaper:
    slug: str
    title: str
    accents: dict              # {thème: "--a:…; --b:…; --param:…;"}
    left: Zone
    right: Zone
    css: str = ""              # CSS propre à ce fond d'écran (ajustements de hauteur…)


# ---------------------------------------------------------------------------
# Thèmes : fond et texte communs ; chaque fond d'écran ajoute ses accents.
# ---------------------------------------------------------------------------
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

CSS = """
* { box-sizing:border-box; margin:0; padding:0; }
body {
  font-family:"Inter",sans-serif; color:var(--text); overflow:hidden;
  background:
    linear-gradient(var(--grid) 1px, transparent 1px) 0 0/40px 40px,
    linear-gradient(90deg, var(--grid) 1px, transparent 1px) 0 0/40px 40px,
    linear-gradient(160deg, var(--bg), var(--bg2));
  padding:56px 60px; display:flex; gap:44px;
}
.k, .tag, .brand small, .prompt, .badge { font-family:__MONO__; }
.zone { display:flex; flex-direction:column; gap:20px; min-width:0; }
.zone.a { flex:3 1 0; }
.zone.b { flex:2 1 0; }
.brand { display:flex; align-items:center; gap:18px; height:54px; padding:0 4px; }
.brand h2 { font-family:"Inter Display","Inter",sans-serif; font-weight:800; font-size:50px; letter-spacing:.04em; line-height:1; white-space:nowrap; }
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
.rows { display:grid; grid-template-columns:calc(var(--kw,178px) + 14px) 1fr; align-items:baseline; }
.k { font-size:17px; white-space:pre; line-height:26px; overflow:hidden; padding-right:14px; }
.a .k { color:var(--a); }
.b .k { color:var(--b); }
.k i { font-style:normal; color:var(--param); }
.d { font-size:16px; line-height:26px; white-space:nowrap; overflow:hidden; color:var(--text2); }
.k.ess, .d.ess { background:var(--hl); }
.k.ess { font-weight:bold; border-radius:5px 0 0 5px; margin-left:-6px; padding-left:6px; }
.d.ess { color:var(--text); border-radius:0 5px 5px 0; margin-right:-6px; padding-right:6px; }
.warn { color:var(--warn); font-weight:bold; }
.badge { font-size:16px; color:var(--muted); border:1px solid var(--border); border-radius:4px; padding:0 4px; margin-left:6px; }
.ess-key { display:inline-block; width:34px; height:20px; background:var(--hl); border-radius:4px; vertical-align:-3px; margin-right:6px; }
.footer .rows { grid-template-columns:1fr auto; }
.footer .d { color:var(--muted); text-align:right; }

/* Portrait : zones empilées, 3 colonnes chacune, texte des commandes à 16 px */
body.portrait { flex-direction:column; padding:56px 40px; gap:32px; }
.portrait .zone.a { flex:none; }
.portrait .zone.b { flex:1 1 0; min-height:0; }
.portrait .cols { gap:16px; }
.portrait .a .cols, .portrait .b .cols { grid-template-columns:repeat(3,minmax(0,1fr)); }
.portrait .panel { padding-left:12px; padding-right:12px; }
.portrait .rows { grid-template-columns:calc(var(--kw,178px) * 16 / 17 + 8px) 1fr; }
.portrait .k { font-size:16px; padding-right:8px; }
.portrait .footer .rows { grid-template-columns:1fr auto; }
"""

TEMPLATE = """<!DOCTYPE html>
<html lang="__LANG__"><head><meta charset="utf-8"><title>__TITLE__</title>
<style>
:root { __VARS__ }
html, body { width:__W__px; height:__H__px; }
__CSS__
</style></head>
<body class="__ORIENTATION__">
  <div class="zone a">
    <div class="brand">__BRAND_A__</div>
    <div class="cols">__ACOLS__</div>__AFOOT__
  </div>
  <div class="zone b">
    <div class="brand">__BRAND_B__</div>
    <div class="cols">__BCOLS__</div>__BFOOT__
  </div>
</body></html>
"""

esc = lambda s: html.escape(s, quote=False)


def _identity(s):
    return s


def fmt_cmd(s, t):
    """Échappe une commande et met en forme (et traduit) ses «paramètres»."""
    def param(m):
        p = m.group(1)
        if len(p) >= 2:
            p = t(f"«{p}»")[1:-1]
        return f"<i>{esc(p)}</i>"
    return re.sub(r"«(.*?)»", param, esc(s))


def fmt_desc(s, t):
    s = t(s)
    badge = ""
    m = re.search(r"\s\[([^\]]+)\]$", s)
    if m:
        badge = f'<span class="badge">{esc(m.group(1))}</span>'
        s = s[: m.start()]
    if s.startswith("⚠ "):
        return f'<span class="warn">⚠</span> {esc(s[2:])}{badge}'
    return esc(s) + badge


def rows_html(rows, t):
    out = []
    for k, d in rows:
        ess = k.startswith("§")
        k = k[1:] if ess else k
        c = " ess" if ess else ""
        out.append(f'<div class="k{c}">{fmt_cmd(k, t)}</div><div class="d{c}">{fmt_desc(d, t)}</div>')
    return "".join(out)


def tag_text(tag, prefix, t):
    if isinstance(tag, T):
        return t(tag)
    if tag.startswith("="):
        return tag[1:]
    return prefix + tag if tag else ""


def panel_html(p, side, prefix, t, extra=""):
    title, tag, kw, rows = p
    tag = tag_text(tag, prefix, t)
    tag_html = f'<span class="tag">{esc(tag)}</span>' if tag else ""
    style = f' style="--kw:{kw}px"' if kw else ""
    return (f'<section class="panel {side}{extra}"{style}><header><h3>{esc(t(title))}</h3>{tag_html}</header>'
            f'<div class="rows">{rows_html(rows, t)}</div></section>')


def brand_html(b, side, t):
    title = t(b.title) if isinstance(b.title, T) else b.title
    prompt = f'<span class="prompt">{esc(b.prompt)}</span>' if b.prompt else ""
    cursor = {"": "", "block": '<span class="cursor"></span>', "under": '<span class="cursor under"></span>'}[b.cursor]
    h2 = f"<h2>{prompt}{esc(title)}{cursor}</h2>"
    parts = [esc(t(b.note))] if b.note else []
    if side == "a" and b.legend == "default":
        parts += [f"<i>{esc(t('parameters'))}</i>", f'<span class="warn">⚠</span> {esc(t(b.warn))}',
                  f'<span class="ess-key"></span>{esc(t("essential"))}']
    elif side == "a" and b.legend == "vim":
        legend = esc(t("parameters: {m} motion · {c} character · {n} number · {a} register"))
        legend = re.sub(r"\{(\w)\}", r"<i>\1</i>", legend)
        parts += [f":help — {legend}", f'<span class="ess-key"></span>{esc(t("essential"))}']
    small = f"<small>{' · '.join(parts)}</small>" if parts else ""
    return h2 + b.svg + small if side == "a" else small + h2


def estimated_height(p):
    """Hauteur approximative d'un panneau (px), pour répartir les colonnes en portrait."""
    return 57 + 26 * len(p[3])


def repack(columns, n):
    """Répartit les panneaux (dans l'ordre) en n colonnes de hauteurs aussi égales que possible."""
    panels = [p for col in columns for p in col]
    best, best_h = None, float("inf")

    def height(group):
        return sum(estimated_height(p) for p in group) + 14 * (len(group) - 1)

    def splits(start, k):
        if k == 1:
            yield [panels[start:]]
            return
        for i in range(start + 1, len(panels) - k + 2):
            for rest in splits(i, k - 1):
                yield [panels[start:i]] + rest

    for groups in splits(0, min(n, len(panels))):
        h = max(height(g) for g in groups)
        if h < best_h:
            best, best_h = groups, h
    return best


def zone_columns(zone, side, orientation, t):
    cols = zone.columns
    if orientation == "portrait" and len(cols) != PORTRAIT_COLUMNS:
        cols = repack(cols, PORTRAIT_COLUMNS)
    body = "".join('<div class="col">' + "".join(panel_html(p, side, zone.tag_prefix, t) for p in c) + "</div>"
                   for c in cols)
    foot = ""
    if zone.footer:
        title, tag, rows = zone.footer
        foot = "\n    " + panel_html((title, tag, None, rows), side, zone.tag_prefix, t, " footer")
    return body, foot


def render(wp, theme, orientation="landscape", t=_identity, lang="en"):
    """HTML complet d'un fond d'écran pour un thème, une orientation et une langue."""
    w, h = ORIENTATIONS[orientation]
    acols, afoot = zone_columns(wp.left, "a", orientation, t)
    bcols, bfoot = zone_columns(wp.right, "b", orientation, t)
    return (TEMPLATE
            .replace("__CSS__", CSS.replace("__MONO__", MONO) + wp.css)
            .replace("__LANG__", lang).replace("__W__", str(w)).replace("__H__", str(h))
            .replace("__ORIENTATION__", orientation)
            .replace("__TITLE__", esc(f"{wp.title} — {t('wallpaper')} ({theme})"))
            .replace("__VARS__", BASE_THEMES[theme] + "\n  " + wp.accents[theme].strip())
            .replace("__BRAND_A__", brand_html(wp.left.brand, "a", t))
            .replace("__BRAND_B__", brand_html(wp.right.brand, "b", t))
            .replace("__ACOLS__", acols).replace("__AFOOT__", afoot)
            .replace("__BCOLS__", bcols).replace("__BFOOT__", bfoot))
