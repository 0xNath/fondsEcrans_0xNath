# Fonds d'écran aide-mémoire — Vim/Regex et Git/Linux
VENV   ?= .venv
PYTHON ?= $(if $(wildcard $(VENV)/bin/python),$(VENV)/bin/python,python3)

.PHONY: all html png setup clean

all: png

html:                ## Génère les pages HTML dans build/html/
	$(PYTHON) src/build_vim_regex.py
	$(PYTHON) src/build_git_linux.py
	$(PYTHON) src/build_windows_powershell.py
	$(PYTHON) src/build_as400.py
	$(PYTHON) src/build_podman_virsh.py
	$(PYTHON) src/build_python.py
	$(PYTHON) src/build_rust.py
	$(PYTHON) src/build_nodejs.py

png: html            ## Exporte les PNG 1440p et 4K dans wallpapers/
	$(PYTHON) src/render.py

setup:               ## Crée le venv et installe Playwright
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt

clean:               ## Supprime les fichiers générés (garde les PNG)
	rm -rf build src/__pycache__
