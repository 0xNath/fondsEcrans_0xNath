"""Traductions des fonds d'écran.

La langue source est l'anglais : c'est le texte écrit dans src/content/*.py. Chaque autre
langue est un catalogue locales/<code>.json de la forme {"texte anglais": "traduction"}.
Une traduction vide ou absente retombe sur l'anglais.

Les paramètres des commandes ont leurs guillemets dans la clé : "«file»": "«fichier»".
Les badges de compatibilité restent en fin de traduction : "in place [GNU]": "en place [GNU]".
Deux sens différents doivent avoir deux textes anglais différents (pas de contexte).

    python src/i18n.py check        clés manquantes, obsolètes ou vides, par langue
    python src/i18n.py update       ajoute les clés manquantes ("") et retire les obsolètes
    python src/i18n.py new <code>   crée locales/<code>.json avec toutes les clés à traduire
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCALES_DIR = ROOT / "locales"
SOURCE = "en"


def available():
    """Langues disponibles : l'anglais puis chaque catalogue de locales/."""
    return [SOURCE] + sorted(p.stem for p in LOCALES_DIR.glob("*.json"))


def load_catalog(lang):
    if lang == SOURCE:
        return {}
    path = LOCALES_DIR / f"{lang}.json"
    if not path.exists():
        raise SystemExit(f"Langue inconnue : {lang} (pas de {path.relative_to(ROOT)})")
    return json.loads(path.read_text(encoding="utf-8"))


def save_catalog(lang, catalog):
    path = LOCALES_DIR / f"{lang}.json"
    path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


class Translator:
    """t(texte) -> traduction ; garde la liste ordonnée des textes demandés."""

    def __init__(self, lang=SOURCE):
        self.lang = lang
        self.catalog = load_catalog(lang)
        self.used = {}

    def __call__(self, s):
        self.used.setdefault(s, None)
        return self.catalog.get(s) or s


def source_keys():
    """Tous les textes à traduire, dans l'ordre où les fonds d'écran les affichent."""
    from build import load_wallpapers
    from wallpaper import render
    t = Translator(SOURCE)
    for wp in load_wallpapers():
        render(wp, "dark", "landscape", t)  # tous les textes y figurent
    return list(t.used)


def check():
    keys = source_keys()
    ok = True
    for lang in available()[1:]:
        cat = load_catalog(lang)
        missing = [k for k in keys if k not in cat]
        obsolete = [k for k in cat if k not in set(keys)]
        empty = [k for k in keys if k in cat and not cat[k]]
        done = len(keys) - len(missing) - len(empty)
        print(f"{lang}: {done}/{len(keys)} traduits, {len(missing)} manquants, "
              f"{len(empty)} vides, {len(obsolete)} obsolètes")
        for k in missing[:20]:
            print(f"   manquant : {k}")
        for k in obsolete[:20]:
            print(f"   obsolète : {k}")
        ok &= not missing and not obsolete
    return ok


def update():
    keys = source_keys()
    for lang in available()[1:]:
        cat = load_catalog(lang)
        new = {k: cat.get(k, "") for k in keys}
        added = sum(k not in cat for k in keys)
        removed = sum(k not in new for k in cat)
        save_catalog(lang, new)
        print(f"{lang}: +{added} clés, -{removed} obsolètes")


def new(lang):
    if (LOCALES_DIR / f"{lang}.json").exists() or lang == SOURCE:
        raise SystemExit(f"{lang} existe déjà")
    path = save_catalog(lang, {k: "" for k in source_keys()})
    print(f"créé : {path.relative_to(ROOT)} — remplir les valeurs, puis `make LOCALES={lang}`")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "check":
        sys.exit(0 if check() else 1)
    elif cmd == "update":
        update()
    elif cmd == "new" and len(sys.argv) == 3:
        new(sys.argv[2])
    else:
        raise SystemExit(__doc__)
