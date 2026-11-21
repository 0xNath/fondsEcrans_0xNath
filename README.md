# Fonds d'écran aide-mémoire

Fonds d'écran « cheat sheet » générés en code (HTML → PNG via Playwright) :

- **Vim + Regex** : modes, déplacements, édition, objets textuels, macros… et regex PCRE/POSIX avec les spécificités Vim.
- **Git + Linux** : commandes Git courantes (préfixe `git` omis) et outils shell (grep, find, sed, awk, jq, systemctl…).

Chacun existe en 4 thèmes : `aritim` (palette Aritim Dark de Konsole), `dark`, `light`, `amoled` (noir pur, texte atténué contre le marquage).

![Aperçu Vim + Regex (Aritim)](wallpapers/1440p/vim-regex-aritim.png)

## Arborescence

```
.
├── src/
│   ├── build_vim_regex.py           # Vim + Regex (mise en page dédiée)
│   ├── build_git_linux.py           # Git + Linux
│   ├── common.py                    # rendu partagé, gabarit « deux zones », thèmes de base
│   └── render.py                    # HTML → PNG 1440p et 4K, détection des débordements
├── wallpapers/
│   ├── 1440p/                       # 2560×1440
│   └── 4k/                          # 3840×2160
├── build/html/                      # pages HTML intermédiaires (généré, ignoré par git)
├── Makefile
└── requirements.txt
```

## Utilisation

```sh
make setup   # une fois : crée .venv et installe Playwright
make         # génère le HTML puis tous les PNG
make html    # HTML seulement (aperçu rapide dans un navigateur à 2560×1440)
make clean   # supprime build/
```

Le rendu utilise le Chrome/Chromium du système (ou `CHROME_PATH=/chemin/vers/chrome make`).
À défaut : `.venv/bin/python -m playwright install chromium`.

`render.py` échoue si un texte déborde de son bloc ou entre dans la marge de sécurité du bas :
après une modification du contenu, raccourcir la ligne ou retirer une entrée.

## Modifier le contenu

Les listes de commandes sont en tête de chaque `src/build_*.py`.
Chaque panneau : `(titre, étiquette, largeur colonne commande en px ou None, lignes)`.

Conventions dans les lignes (voir `src/common.py`) :

| Syntaxe              | Effet                                       |
|----------------------|---------------------------------------------|
| `"§cmd"`             | commande essentielle (surlignée, en gras)   |
| `«x»`                | paramètre (couleur secondaire)              |
| `"⚠ desc"`           | commande destructive                        |
| `"desc [GNU]"`       | badge de compatibilité en fin de ligne      |

Thèmes : les couleurs de fond et de texte sont dans `BASE_THEMES` (`src/common.py`) ; chaque
script n'ajoute que ses accents dans `ACCENTS` (`--a` zone gauche, `--b` zone droite, `--param`).
Vim/Regex garde son propre dictionnaire `THEMES`.

Nouveau fond d'écran : copier un script à gabarit « deux zones » (par ex. `src/build_git_linux.py`),
changer le contenu, les accents et le slug,
puis l'ajouter à la cible `html` du `Makefile`.

## Polices

- Commandes : **MesloLGS Nerd Font** (repli : DejaVu Sans Mono).
- Titres et descriptions : Inter (repli : sans-serif du système).
