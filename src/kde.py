"""Intégration KDE Plasma : paquets de fonds d'écran, script KWin (raccourcis) et commande `cheatsheet`.

    python src/kde.py install [--lang fr] [--dark konsole] [--light light]
    python src/kde.py uninstall

install :
  - un paquet Plasma par fond d'écran dans ~/.local/share/wallpapers/cheatsheet-<slug>/ :
    contents/images/<LxH>.png (thème clair) et contents/images_dark/<LxH>.png (thème sombre).
    Plasma choisit la bonne taille pour chaque écran (1920x1080 → format compact, écran pivoté
    → portrait…) et la variante claire ou sombre selon le jeu de couleurs ;
  - le script KWin « cheatsheet » : un raccourci par sujet, sujet suivant / précédent, et
    (facultatif) un sujet par bureau virtuel ; raccourcis modifiables dans Configuration du
    système › Raccourcis › KWin ;
  - la commande ~/.local/bin/cheatsheet (lien vers bin/cheatsheet).
"""
import argparse
import json
import shutil
import subprocess
from pathlib import Path

from build import load_wallpapers
from i18n import Translator
from wallpaper import FORMATS, ROOT

HOME = Path.home()
WALLPAPERS_DIR = HOME / ".local/share/wallpapers"
KWIN_SCRIPT_DIR = HOME / ".local/share/kwin/scripts/cheatsheet"
BIN_LINK = HOME / ".local/bin/cheatsheet"
PREFIX = "cheatsheet-"

# Raccourcis par sujet (Meta+Alt+…) ; les autres sujets restent accessibles via suivant / précédent.
SHORTCUTS = {"vim-regex": "V", "git-linux": "G", "windows-powershell": "W", "as400": "A",
             "podman-virsh": "O", "python": "Y", "rust": "R", "nodejs": "N"}
NEXT, PREV = "Meta+Alt+PgDown", "Meta+Alt+PgUp"

KWIN_METADATA = {
    "KPlugin": {"Id": "cheatsheet", "Name": "Cheat sheet wallpapers",
                "Name[fr]": "Fonds d'écran aide-mémoire",
                "Description": "Switch the cheat sheet wallpaper with shortcuts or per virtual desktop",
                "Description[fr]": "Change de fond d'écran aide-mémoire par raccourci ou par bureau virtuel",
                "Authors": [{"Name": "0xNath"}], "EnabledByDefault": False, "License": "MIT"},
    "X-Plasma-API": "javascript", "X-Plasma-MainScript": "code/main.js", "KPackageStructure": "KWin/Script",
}

KWIN_MAIN = r"""// Généré par src/kde.py — ne pas modifier ici.
const TOPICS = __TOPICS__;   // [{slug, name, path}]
let index = 0;

function plasmaScript(path) {
    return 'desktops().forEach(function (d) { if (d.screen < 0) return;' +
        ' d.wallpaperPlugin = "org.kde.image";' +
        ' d.currentConfigGroup = ["Wallpaper", "org.kde.image", "General"];' +
        ' d.writeConfig("Image", "' + path + '"); });';
}

function show(i) {
    index = (i + TOPICS.length) % TOPICS.length;
    callDBus("org.kde.plasmashell", "/PlasmaShell", "org.kde.PlasmaShell", "evaluateScript",
             plasmaScript(TOPICS[index].path));
}

function showSlug(slug) {
    const i = TOPICS.findIndex(t => t.slug === slug);
    if (i >= 0) show(i);
}

__SHORTCUTS__
registerShortcut("Cheatsheet: next", "Cheat sheet: next topic", "__NEXT__", () => show(index + 1));
registerShortcut("Cheatsheet: previous", "Cheat sheet: previous topic", "__PREV__", () => show(index - 1));

// Un sujet par bureau virtuel : kwinrc [Script-cheatsheet] desktopTopics=1=git-linux,2=python
const mapping = {};
String(readConfig("desktopTopics", "")).split(",").forEach(function (pair) {
    const kv = pair.split("=");
    if (kv.length === 2) mapping[kv[0].trim()] = kv[1].trim();
});
workspace.currentDesktopChanged.connect(function () {
    const n = String(workspace.desktops.indexOf(workspace.currentDesktop) + 1);
    if (mapping[n]) showSlug(mapping[n]);
});
"""


def wallpaper_png(lang, fmt, scale, slug, theme):
    w, h = FORMATS[fmt]["size"]
    return ROOT / "wallpapers" / lang / f"{round(w * scale)}x{round(h * scale)}" / f"{slug}-{theme}.png"


def install_packages(lang, dark, light):
    t = Translator(lang)
    topics = []
    for wp in load_wallpapers():
        pkg = WALLPAPERS_DIR / f"{PREFIX}{wp.slug}"
        if pkg.exists():
            shutil.rmtree(pkg)
        for sub, theme in (("images", light), ("images_dark", dark)):
            d = pkg / "contents" / sub
            d.mkdir(parents=True)
            for fmt, spec in FORMATS.items():
                for scale in spec["scales"]:
                    src = wallpaper_png(lang, fmt, scale, wp.slug, theme)
                    if not src.exists():
                        raise SystemExit(f"{src.relative_to(ROOT)} absent : lancer `make png LOCALES={lang}` d'abord.")
                    shutil.copy2(src, d / f"{src.parent.name}.png")
        name = f"{wp.title} — {t('cheat sheet')}"
        meta = {"KPlugin": {"Id": f"{PREFIX}{wp.slug}", "Name": name, "Authors": [{"Name": "0xNath"}],
                            "License": "MIT"}}
        (pkg / "metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        shutil.copy2(wallpaper_png(lang, "landscape", 1, wp.slug, dark), pkg / "contents" / "screenshot.png")
        topics.append({"slug": wp.slug, "name": wp.title, "path": f"file://{pkg}/"})
        print(f"paquet : {pkg}")
    return topics


def install_kwin_script(topics):
    if KWIN_SCRIPT_DIR.exists():
        shutil.rmtree(KWIN_SCRIPT_DIR)
    (KWIN_SCRIPT_DIR / "contents/code").mkdir(parents=True)
    (KWIN_SCRIPT_DIR / "metadata.json").write_text(json.dumps(KWIN_METADATA, ensure_ascii=False, indent=2) + "\n")
    shortcuts = "\n".join(
        f'registerShortcut("Cheatsheet: {t["slug"]}", "Cheat sheet: {t["name"]}", "Meta+Alt+{SHORTCUTS[t["slug"]]}", '
        f'() => showSlug("{t["slug"]}"));' for t in topics if t["slug"] in SHORTCUTS)
    code = (KWIN_MAIN.replace("__TOPICS__", json.dumps(topics, ensure_ascii=False))
            .replace("__SHORTCUTS__", shortcuts).replace("__NEXT__", NEXT).replace("__PREV__", PREV))
    (KWIN_SCRIPT_DIR / "contents/code/main.js").write_text(code, encoding="utf-8")
    # activer le script et le (re)charger
    subprocess.run(["kwriteconfig6", "--file", "kwinrc", "--group", "Plugins", "--key", "cheatsheetEnabled", "false"], check=True)
    subprocess.run(["qdbus6", "org.kde.KWin", "/KWin", "reconfigure"], check=False)
    subprocess.run(["kwriteconfig6", "--file", "kwinrc", "--group", "Plugins", "--key", "cheatsheetEnabled", "true"], check=True)
    subprocess.run(["qdbus6", "org.kde.KWin", "/KWin", "reconfigure"], check=False)
    print(f"script KWin : {KWIN_SCRIPT_DIR} (activé)")


def install_bin():
    BIN_LINK.parent.mkdir(parents=True, exist_ok=True)
    if BIN_LINK.is_symlink() or BIN_LINK.exists():
        BIN_LINK.unlink()
    BIN_LINK.symlink_to(ROOT / "bin" / "cheatsheet")
    print(f"commande : {BIN_LINK} → bin/cheatsheet")


def uninstall():
    for pkg in WALLPAPERS_DIR.glob(f"{PREFIX}*"):
        shutil.rmtree(pkg)
        print(f"supprimé : {pkg}")
    if KWIN_SCRIPT_DIR.exists():
        subprocess.run(["kwriteconfig6", "--file", "kwinrc", "--group", "Plugins", "--key", "cheatsheetEnabled", "--delete"], check=True)
        subprocess.run(["qdbus6", "org.kde.KWin", "/KWin", "reconfigure"], check=False)
        shutil.rmtree(KWIN_SCRIPT_DIR)
        print(f"supprimé : {KWIN_SCRIPT_DIR}")
    if BIN_LINK.is_symlink():
        BIN_LINK.unlink()
        print(f"supprimé : {BIN_LINK}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("action", choices=["install", "uninstall"])
    ap.add_argument("--lang", default="fr")
    ap.add_argument("--dark", default="konsole", help="thème des images sombres")
    ap.add_argument("--light", default="light", help="thème des images claires")
    args = ap.parse_args()
    if args.action == "install":
        topics = install_packages(args.lang, args.dark, args.light)
        install_kwin_script(topics)
        install_bin()
    else:
        uninstall()
