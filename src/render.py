"""Exporte build/html/** en PNG et signale tout débordement de texte.

    wallpapers/<langue>/<L>x<H>/<slug>-<thème>.png

Chaque page est rendue à la taille de son format (2560x1440, 1440x2560, 1920x1080) et, pour le
paysage et le portrait, aussi à x1,5 (3840x2160, 2160x3840) : même mise en page, texte net en 4K.

    python src/render.py [--locale …] [--format …] [--theme …] [--only …] [-j 4] [--check]

Navigateur : variable CHROME_PATH si définie, sinon le premier Chrome/Chromium trouvé dans
le PATH, sinon le Chromium fourni par Playwright (`python -m playwright install chromium`).
"""
import argparse
import os
import shutil
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from build import OUT as HTML, ROOT, options, selection
from wallpaper import FORMATS

WALLPAPERS = ROOT / "wallpapers"
SAFE_BOTTOM = 56  # marge de sécurité en bas (barre des tâches, dock)

CHECK = """(safe) => {
  const r = [];
  document.querySelectorAll('.k, .d, .panel header, .brand').forEach(e => {
    if (e.scrollWidth > e.clientWidth + 1) r.push(['DEBORDE', e.textContent.trim().slice(0, 60), e.scrollWidth - e.clientWidth]);
  });
  const limit = window.innerHeight - safe + 1;
  document.querySelectorAll('.panel').forEach(e => {
    const b = e.getBoundingClientRect();
    if (b.bottom > limit) r.push(['DEBORDE bas', e.querySelector('h3').textContent, Math.round(b.bottom - limit + 1)]);
  });
  return r; }"""


def find_browser():
    if os.environ.get("CHROME_PATH"):
        return os.environ["CHROME_PATH"]
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        if path := shutil.which(name):
            return path
    return None  # Chromium embarqué de Playwright


def out_path(lang, fmt, scale, name):
    w, h = FORMATS[fmt]["size"]
    return WALLPAPERS / lang / f"{round(w * scale)}x{round(h * scale)}" / f"{name}.png"


def render_batch(jobs, check_only=False):
    """jobs : [(lang, format, page)] — un navigateur par processus."""
    from playwright.sync_api import sync_playwright
    problems = []
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=find_browser())
        pages = {}
        for lang, fmt, page in jobs:
            w, h = FORMATS[fmt]["size"]
            for scale in (1,) if check_only else FORMATS[fmt]["scales"]:
                key = (fmt, scale)
                if key not in pages:
                    pages[key] = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=scale)
                pg = pages[key]
                pg.goto(page.as_uri())
                pg.wait_for_timeout(200)
                if scale == 1:
                    problems += [(f"{lang}/{fmt}/{page.stem}", *x) for x in pg.evaluate(CHECK, SAFE_BOTTOM)]
                if check_only:
                    continue
                dest = out_path(lang, fmt, scale, page.stem)
                dest.parent.mkdir(parents=True, exist_ok=True)
                pg.screenshot(path=str(dest))
        browser.close()
    return len(jobs), sum(len(FORMATS[f]['scales']) for _, f, _ in jobs), problems


def main():
    parser = options(argparse.ArgumentParser(description=__doc__))
    parser.add_argument("-j", "--jobs", type=int, default=4, help="processus en parallèle")
    parser.add_argument("--check", action="store_true", help="vérifier les débordements sans exporter")
    args = parser.parse_args()
    locales, formats, themes, wps = selection(args)
    jobs = []
    for lang in locales:
        for fmt in formats:
            for wp in wps:
                for theme in themes:
                    page = HTML / lang / fmt / f"{wp.slug}-{theme}.html"
                    if not page.exists():
                        raise SystemExit(f"{page.relative_to(ROOT)} absent : lancer `make html` d'abord.")
                    jobs.append((lang, fmt, page))
    n = max(1, min(args.jobs, len(jobs)))
    batches = [jobs[i::n] for i in range(n)]
    problems, done, pngs = [], 0, 0
    with ProcessPoolExecutor(n) as ex:
        for count, files, probs in ex.map(render_batch, batches, [args.check] * n):
            done += count
            pngs += files
            problems += probs
    for x in sorted(problems):
        print(*x)
    print(f"{done} pages vérifiées" if args.check else
          f"{done} pages → {pngs} PNG dans {WALLPAPERS.relative_to(ROOT)}/")
    if problems:
        raise SystemExit(f"{len(problems)} débordement(s) détecté(s).")


if __name__ == "__main__":
    main()
