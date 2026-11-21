"""Exporte build/html/*.html en PNG et signale tout débordement de texte.

    wallpapers/1440p/<nom>.png     2560x1440
    wallpapers/4k/<nom>-4k.png     3840x2160 (même mise en page, rendu x1,5)

Navigateur : variable CHROME_PATH si définie, sinon le premier Chrome/Chromium
trouvé dans le PATH, sinon le Chromium fourni par Playwright
(`python -m playwright install chromium`).
"""
import os
import shutil
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "build" / "html"
OUT_1440 = ROOT / "wallpapers" / "1440p"
OUT_4K = ROOT / "wallpapers" / "4k"

CHECK = """() => {
  const r = [];
  document.querySelectorAll('.k, .d, .panel header').forEach(e => {
    if (e.scrollWidth > e.clientWidth + 1) r.push(['DEBORDE', e.textContent, e.scrollWidth - e.clientWidth]);
  });
  document.querySelectorAll('.panel').forEach(e => {
    const b = e.getBoundingClientRect();
    if (b.bottom > 1440 - 56 + 1) r.push(['DEBORDE bas', e.querySelector('h3').textContent, Math.round(b.bottom)]);
  });
  return r; }"""


def find_browser():
    if os.environ.get("CHROME_PATH"):
        return os.environ["CHROME_PATH"]
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        if path := shutil.which(name):
            return path
    return None  # Chromium embarqué de Playwright


def main():
    pages = sorted(HTML.glob("*.html"))
    if not pages:
        raise SystemExit(f"Aucun HTML dans {HTML} : lancer `make html` d'abord.")
    OUT_1440.mkdir(parents=True, exist_ok=True)
    OUT_4K.mkdir(parents=True, exist_ok=True)
    problems = 0
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=find_browser())
        pg = b.new_page(viewport={"width": 2560, "height": 1440})
        pg4k = b.new_page(viewport={"width": 2560, "height": 1440}, device_scale_factor=1.5)
        for f in pages:
            pg.goto(f.as_uri())
            pg.wait_for_timeout(300)
            for x in pg.evaluate(CHECK):
                problems += 1
                print(f.stem, x)
            pg.screenshot(path=str(OUT_1440 / f"{f.stem}.png"))
            pg4k.goto(f.as_uri())
            pg4k.wait_for_timeout(300)
            pg4k.screenshot(path=str(OUT_4K / f"{f.stem}-4k.png"))
            print(f"ok  {f.stem}")
        b.close()
    if problems:
        raise SystemExit(f"{problems} débordement(s) détecté(s).")


if __name__ == "__main__":
    main()
