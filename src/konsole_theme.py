"""Crée un thème de fond d'écran à partir d'un jeu de couleurs Konsole (.colorscheme).

    python src/konsole_theme.py "~/.local/share/konsole/Aritim Dark.colorscheme" [nom]

Écrit themes/<nom>.json (nom par défaut : konsole). Le fond, le texte et la sélection
reprennent ceux du terminal ; les accents de chaque fond d'écran sont pris dans la palette
du terminal (couleur de teinte la plus proche), éclaircis si besoin pour rester lisibles.
"""
import configparser
import json
import sys
from pathlib import Path

from wallpaper import ROOT, _hex, mix, readable


def color(cfg, section):
    r, g, b = (int(x) for x in cfg[section]["Color"].split(",")[:3])
    return _hex((r / 255, g / 255, b / 255))


def theme_from_colorscheme(path):
    cfg = configparser.ConfigParser(interpolation=None, strict=False)
    cfg.optionxform = str
    cfg.read(path, encoding="utf-8")
    bg, fg = color(cfg, "Background"), color(cfg, "Foreground")
    c = {i: color(cfg, f"Color{i}") for i in range(8)}
    ci = {i: color(cfg, f"Color{i}Intense") for i in range(8) if f"Color{i}Intense" in cfg}
    r, g, b = (int(x) for x in cfg["Color2"]["Color"].split(",")[:3])
    fr, fg_, fb = (int(x) for x in cfg["Foreground"]["Color"].split(",")[:3])
    return {
        "source": Path(path).name,
        "vars": {
            "--bg": bg, "--bg2": bg,
            "--grid": f"rgba({fr},{fg_},{fb},.035)",
            "--panel": mix(bg, fg, 0.035), "--border": mix(bg, c[0], 0.45),
            "--text": fg, "--text2": readable(mix(fg, bg, 0.15), bg, 7),
            "--muted": readable(c[0], bg), "--hl": f"rgba({r},{g},{b},.45)",
            "--warn": readable(c[1], bg),
        },
        # couleurs vives disponibles pour les accents (rouge exclu : réservé au ⚠)
        "palette": [c[i] for i in (2, 3, 4, 5, 6)] + [ci[i] for i in (2, 3, 4, 5, 6) if i in ci],
    }


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        raise SystemExit(__doc__)
    src = Path(sys.argv[1]).expanduser()
    name = sys.argv[2] if len(sys.argv) == 3 else "konsole"
    out = ROOT / "themes" / f"{name}.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(theme_from_colorscheme(src), indent=2) + "\n", encoding="utf-8")
    print(f"thème « {name} » écrit dans {out.relative_to(ROOT)}")
