# Fonds d'écran aide-mémoire — voir README.md
VENV   ?= .venv
PYTHON ?= $(if $(wildcard $(VENV)/bin/python),$(VENV)/bin/python,python3)
JOBS   ?= 4

# Sélection facultative, valeurs séparées par des virgules :
#   make LOCALES=fr ORIENTATIONS=portrait ONLY=rust,python
SELECT = $(if $(LOCALES),--locale $(LOCALES)) $(if $(ORIENTATIONS),--orientation $(ORIENTATIONS)) $(if $(ONLY),--only $(ONLY))

.PHONY: all html png check setup clean i18n-check i18n-update i18n-new

all: png

html:                ## Génère les pages HTML dans build/html/
	$(PYTHON) src/build.py $(SELECT)

png: html            ## Exporte les PNG dans wallpapers/<langue>/<LxH>/
	$(PYTHON) src/render.py $(SELECT) -j $(JOBS)

check: html          ## Vérifie les débordements de texte, sans exporter
	$(PYTHON) src/render.py $(SELECT) -j $(JOBS) --check

i18n-check:          ## Traductions manquantes, vides ou obsolètes
	$(PYTHON) src/i18n.py check

i18n-update:         ## Ajoute les nouveaux textes aux catalogues, retire les obsolètes
	$(PYTHON) src/i18n.py update

i18n-new:            ## Nouvelle langue : make i18n-new LOCALE=de
	@test -n "$(LOCALE)" || (echo "usage : make i18n-new LOCALE=<code>" && exit 1)
	$(PYTHON) src/i18n.py new $(LOCALE)

setup:               ## Crée le venv et installe Playwright
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt

clean:               ## Supprime les fichiers générés (garde les PNG)
	rm -rf build src/__pycache__ src/content/__pycache__
