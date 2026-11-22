"""Modèle et rendu HTML des fonds d'écran : deux zones, trois formats, thèmes, langues.

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
import colorsys
import json
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Formats : taille de la page (px CSS) et facteurs d'export (1,5 = 4K net).
#   landscape : mise en page complète, 5 colonnes
#   portrait  : zones empilées, 3 colonnes chacune
#   compact   : 1920x1080, 2 + 2 colonnes, lignes non essentielles retirées pour tenir
FORMATS = {
    "landscape": {"size": (2560, 1440), "scales": (1, 1.5)},
    "portrait": {"size": (1440, 2560), "scales": (1, 1.5)},
    "compact": {"size": (1920, 1080), "scales": (1,)},
}
PORTRAIT_COLUMNS = 3
COMPACT_COLUMNS = 2
COMPACT_FOOTER_ROWS = 4


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
.rows { display:grid; grid-template-columns:calc(var(--kw,178px) + 10px) 1fr; align-items:baseline; }
.k { font-size:17px; white-space:pre; line-height:26px; overflow:hidden; padding-right:10px; }
.a .k { color:var(--a); }
.b .k { color:var(--b); }
.k i { font-style:normal; color:var(--param); }
/* Inter à 16 px : approche recommandée par ses « dynamic metrics » */
.d { font-size:16px; line-height:26px; white-space:nowrap; overflow:hidden; color:var(--text2); letter-spacing:-0.011em; }
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

/* Compact (1920x1080) : 2 + 2 colonnes, texte à 16 px, interlignes resserrés */
body.compact { padding:40px 40px 56px; gap:32px; }
.compact .zone { gap:14px; }
.compact .zone.a, .compact .zone.b { flex:1 1 0; }
.compact .brand { height:44px; gap:14px; }
.compact .brand h2 { font-size:40px; }
.compact .cursor { width:18px; height:36px; }
.compact .cursor.under { height:6px; }
.compact .graph { width:100px; height:40px; }
.compact .brand small { font-size:16px; margin-top:8px; line-height:1.2; white-space:normal; }
.compact .cols { gap:16px; }
.compact .a .cols, .compact .b .cols { grid-template-columns:repeat(2,minmax(0,1fr)); }
.compact .col { gap:12px; }
.compact .panel { padding:10px 12px 11px; }
.compact .panel::before { top:11px; bottom:11px; }
.compact .panel header { margin-bottom:4px; }
.compact .panel h3 { font-size:18px; }
.compact .rows { grid-template-columns:calc(var(--kw,178px) * 16 / 17 + 8px) 1fr; }
.compact .k { font-size:16px; padding-right:8px; line-height:24px; }
.compact .d { line-height:24px; }
.compact .footer .rows { grid-template-columns:1fr auto; }
"""

# Métriques pour estimer la hauteur d'un panneau : (base, hauteur de ligne, écart entre panneaux)
METRICS = {"landscape": (57, 26, 14), "portrait": (57, 26, 14), "compact": (50, 25, 12)}
COMPACT_COLS_HEIGHT = 1080 - 40 - 56 - 44 - 14  # page - marges - bandeau - écart


# ---------------------------------------------------------------------------
# Thèmes supplémentaires (themes/*.json, ex. généré depuis un thème Konsole) :
# les accents de chaque fond d'écran y sont dérivés de ses accents « dark ».
# ---------------------------------------------------------------------------
def _rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def _hex(rgb):
    return "#" + "".join(f"{round(max(0, min(1, c)) * 255):02x}" for c in rgb)


def _lum(rgb):
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(a, b):
    la, lb = sorted((_lum(_rgb(a)), _lum(_rgb(b))), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def mix(a, b, t):
    """Mélange a vers b (t = 0 → a, 1 → b)."""
    return _hex(tuple(x + (y - x) * t for x, y in zip(_rgb(a), _rgb(b))))


def readable(color, bg, ratio=4.5):
    """Éclaircit (fond sombre) ou fonce (fond clair) color jusqu'au contraste demandé (WCAG)."""
    target = "#ffffff" if _lum(_rgb(bg)) < 0.5 else "#000000"
    t = 0.0
    while contrast(color if t == 0 else mix(color, target, t), bg) < ratio and t < 1:
        t += 0.02
    return color if t == 0 else mix(color, target, t)


def _hue_dist(a, b):
    ha = colorsys.rgb_to_hsv(*_rgb(a))[0]
    hb = colorsys.rgb_to_hsv(*_rgb(b))[0]
    d = abs(ha - hb)
    return min(d, 1 - d)


def derive_accents(dark_accents, palette, bg):
    """Accents d'un thème externe : chaque accent « dark » → couleur de palette de teinte la plus proche."""
    wanted = dict(re.findall(r"(--[\w-]+):\s*(#[0-9a-fA-F]{6})", dark_accents))
    colorful = [c for c in palette if colorsys.rgb_to_hsv(*_rgb(c))[1] >= 0.25] or palette
    used, out = [], []
    for var in ("--a", "--b", "--param"):
        # teintes nettement différentes des accents déjà choisis (sinon : simplement non utilisées)
        choices = ([c for c in colorful if all(_hue_dist(c, u) > 0.07 for u in used)]
                   or [c for c in colorful if c not in used] or colorful)
        best = min(choices, key=lambda c: _hue_dist(c, wanted[var]))
        used.append(best)
        out.append(f"{var}:{readable(best, bg)};")
    return " ".join(out)


def _load_extra_themes():
    themes = {}
    for f in sorted((ROOT / "themes").glob("*.json")):
        data = json.loads(f.read_text(encoding="utf-8"))
        themes[f.stem] = data
    return themes


EXTRA_THEMES = _load_extra_themes()
THEMES = list(BASE_THEMES) + [t for t in EXTRA_THEMES if t not in BASE_THEMES]


def theme_vars(wp, theme):
    if theme in BASE_THEMES:
        return BASE_THEMES[theme] + "\n  " + wp.accents[theme].strip()
    data = EXTRA_THEMES[theme]
    base = " ".join(f"{k}:{v};" for k, v in data["vars"].items())
    accents = wp.accents.get(theme) or derive_accents(wp.accents["dark"], data["palette"], data["vars"]["--bg"])
    return base + "\n  " + accents

TEMPLATE = """<!DOCTYPE html>
<html lang="__LANG__"><head><meta charset="utf-8"><title>__TITLE__</title>
<style>
:root { __VARS__ }
html, body { width:__W__px; height:__H__px; }
__CSS__
</style></head>
<body class="__FORMAT__">
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


def estimated_height(p, fmt="landscape"):
    """Hauteur approximative d'un panneau (px), pour répartir les colonnes."""
    base, line, _ = METRICS[fmt]
    return base + line * len(p[3])


def column_height(panels, fmt):
    return sum(estimated_height(p, fmt) for p in panels) + METRICS[fmt][2] * (len(panels) - 1)


def repack(columns, n, fmt="landscape"):
    """Répartit les panneaux (dans l'ordre) en n colonnes de hauteurs aussi égales que possible."""
    panels = [p for col in columns for p in col]
    best, best_h = None, float("inf")

    def splits(start, k):
        if k == 1:
            yield [panels[start:]]
            return
        for i in range(start + 1, len(panels) - k + 2):
            for rest in splits(i, k - 1):
                yield [panels[start:i]] + rest

    for groups in splits(0, min(n, len(panels))):
        h = max(column_height(g, fmt) for g in groups)
        if h < best_h:
            best, best_h = groups, h
    return best


def trim_to_fit(columns, n, capacity, fmt="compact"):
    """Retire les lignes non essentielles (en partant de la fin des plus gros panneaux) jusqu'à ce que
    les panneaux tiennent dans n colonnes de `capacity` px. Les lignes « § » sont gardées."""
    panels = [(title, tag, kw, list(rows)) for col in columns for title, tag, kw, rows in col]
    while True:
        groups = repack([panels], n, fmt)
        if max(column_height(g, fmt) for g in groups) <= capacity:
            return groups
        removable = [p for p in panels if any(not k.startswith("§") for k, _ in p[3])]
        if not removable:  # que des essentielles : on retire le dernier panneau
            panels.pop()
            continue
        rows = max(removable, key=lambda p: len(p[3]))[3]
        del rows[max(i for i, (k, _) in enumerate(rows) if not k.startswith("§"))]
        panels = [p for p in panels if p[3]]


def zone_columns(zone, side, fmt, t):
    cols, footer = zone.columns, zone.footer
    if fmt == "compact":
        if footer:
            footer = (footer[0], footer[1], footer[2][:COMPACT_FOOTER_ROWS])
        capacity = COMPACT_COLS_HEIGHT
        if footer:
            capacity -= estimated_height((None, None, None, footer[2]), fmt) + 14
        cols = trim_to_fit(cols, COMPACT_COLUMNS, capacity)
    elif fmt == "portrait" and len(cols) != PORTRAIT_COLUMNS:
        cols = repack(cols, PORTRAIT_COLUMNS, fmt)
    body = "".join('<div class="col">' + "".join(panel_html(p, side, zone.tag_prefix, t) for p in c) + "</div>"
                   for c in cols)
    foot = ""
    if footer:
        title, tag, rows = footer
        foot = "\n    " + panel_html((title, tag, None, rows), side, zone.tag_prefix, t, " footer")
    return body, foot


def render(wp, theme, fmt="landscape", t=_identity, lang="en"):
    """HTML complet d'un fond d'écran pour un thème, un format et une langue."""
    w, h = FORMATS[fmt]["size"]
    acols, afoot = zone_columns(wp.left, "a", fmt, t)
    bcols, bfoot = zone_columns(wp.right, "b", fmt, t)
    return (TEMPLATE
            .replace("__CSS__", CSS.replace("__MONO__", MONO) + wp.css)
            .replace("__LANG__", lang).replace("__W__", str(w)).replace("__H__", str(h))
            .replace("__FORMAT__", fmt)
            .replace("__TITLE__", esc(f"{wp.title} — {t('cheat sheet')} ({theme})"))
            .replace("__VARS__", theme_vars(wp, theme))
            .replace("__BRAND_A__", brand_html(wp.left.brand, "a", t))
            .replace("__BRAND_B__", brand_html(wp.right.brand, "b", t))
            .replace("__ACOLS__", acols).replace("__AFOOT__", afoot)
            .replace("__BCOLS__", bcols).replace("__BFOOT__", bfoot))
