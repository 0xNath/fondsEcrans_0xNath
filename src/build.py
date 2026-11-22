"""Génère les pages HTML : build/html/<langue>/<format>/<slug>-<thème>.html

    python src/build.py [--locale fr,en] [--format landscape,portrait,compact] [--theme konsole]
                        [--only rust,vim-regex]

Sans option : toutes les langues, formats, thèmes et fonds d'écran.
Un fond d'écran = un module de src/content/ qui définit WALLPAPER.
"""
import argparse
import importlib
import pkgutil
import shutil
from pathlib import Path

import content
from i18n import Translator, available
from wallpaper import FORMATS, THEMES, render

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "build" / "html"


def load_wallpapers():
    mods = [importlib.import_module(f"content.{m.name}") for m in pkgutil.iter_modules(content.__path__)]
    return [m.WALLPAPER for m in mods]


def csv(value, allowed, what):
    if not value:
        return list(allowed)
    items = [v.strip() for v in value.split(",") if v.strip()]
    unknown = [v for v in items if v not in allowed]
    if unknown:
        raise SystemExit(f"{what} inconnu(s) : {', '.join(unknown)} (possibles : {', '.join(allowed)})")
    return items


def selection(args):
    wps = {wp.slug: wp for wp in load_wallpapers()}
    return (csv(args.locale, available(), "langue"), csv(args.format, FORMATS, "format"),
            csv(args.theme, THEMES, "thème"), [wps[s] for s in csv(args.only, wps, "fond d'écran")])


def options(parser):
    parser.add_argument("--locale", help="langues, séparées par des virgules")
    parser.add_argument("--format", help=", ".join(FORMATS))
    parser.add_argument("--theme", help=", ".join(THEMES))
    parser.add_argument("--only", help="slugs des fonds d'écran")
    return parser


def main():
    args = options(argparse.ArgumentParser(description=__doc__)).parse_args()
    locales, formats, themes, wps = selection(args)
    if not (args.locale or args.format or args.theme or args.only) and OUT.exists():
        shutil.rmtree(OUT)  # build complet : repartir de zéro (retire les pages obsolètes)
    n = 0
    for lang in locales:
        t = Translator(lang)
        for fmt in formats:
            d = OUT / lang / fmt
            d.mkdir(parents=True, exist_ok=True)
            for wp in wps:
                for theme in themes:
                    (d / f"{wp.slug}-{theme}.html").write_text(render(wp, theme, fmt, t, lang), "utf-8")
                    n += 1
        missing = [k for k in t.used if not t.catalog.get(k)] if lang != "en" else []
        if missing:
            print(f"{lang}: {len(missing)} texte(s) sans traduction (anglais utilisé) — voir `make i18n-check`")
    print(f"{n} pages dans {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
