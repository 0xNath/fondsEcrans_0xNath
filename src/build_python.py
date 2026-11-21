"""Fond d'écran aide-mémoire Python : langage + outils (venv, pip, uv, pytest, ruff, pdb).

Modifier le contenu ci-dessous, puis :
    make html        -> génère build/html/python-{aritim,dark,light,amoled}.html
    make             -> exporte aussi les PNG dans wallpapers/

Conventions (voir common.py) : "§cmd" essentiel, «x» paramètre, "⚠ desc" destructif,
"desc [badge]" badge de compatibilité.
Panneau : (titre, étiquette ou "", largeur colonne commande en px ou None, lignes)
"""
from common import build_two_zones

LANGAGE = [
    [  # colonne 1
        ("Types de base", "", 230, [
            ("§int  float  str  bool", "scalaires"),
            ("None", "absence de valeur"),
            ("§[1, 2]  list(«it»)", "liste (mutable)"),
            ("(1, 2)  (1,)", "tuple (immuable)"),
            ('§{"a": 1}  dict()', "dictionnaire"),
            ("{1, 2}  set()", "ensemble"),
            ('b"…"  bytes', "octets"),
            ("isinstance(«x», «T»)", "test de type"),
            ('int("42")  str(42)', "convertir"),
            ("§len(«x»)", "taille"),
        ]),
        ("Chaînes", "", 230, [
            ('§f"{«x»}"  f"{«x»=}"', "f-string (+ nom)"),
            ('f"{«n»:.2f}"', "2 décimales"),
            ('f"{«s»:>10}"', "aligner à droite"),
            ("§«s».split(«sep»)", "découper"),
            ("§«sep».join(«liste»)", "assembler"),
            ("«s».strip()", "espaces aux bords"),
            ("«s».replace(«a», «b»)", "remplacer"),
            ("«s».startswith(«p»)", "commence par"),
            ("«s».lower()  .upper()", "casse"),
            ('r"\\d+"', "chaîne brute (regex)"),
            ('"""…"""', "multiligne"),
        ]),
        ("Tranches & déballage", "", 230, [
            ("§«x»[0]  «x»[-1]", "premier / dernier"),
            ("«x»[1:3]", "indices 1 et 2"),
            ("«x»[:«n»]  «x»[-«n»:]", "n premiers / derniers"),
            ("«x»[::2]  «x»[::-1]", "un sur deux / inversé"),
            ("a, *reste = «x»", "déballer"),
            ("a, b = b, a", "échanger"),
            ("f(*«liste», **«dict»)", "passer en arguments"),
        ]),
        ("Dictionnaires & ensembles", "", 230, [
            ("§«d».get(«k», «déf»)", "sans KeyError"),
            ("«d».setdefault(«k», [])", "initialiser si absent"),
            ("«d» | «d2»", "fusionner"),
            ("«k» in «d»", "clé présente ?"),
            ("del «d»[«k»]  .pop(«k»)", "supprimer"),
            ("«a» & «b»  «a» | «b»", "intersection / union"),
            ("«a» - «b»", "différence"),
        ]),
    ],
    [  # colonne 2
        ("Contrôle", "", 250, [
            ("«a» if «c» else «b»", "ternaire"),
            ("§enumerate(«l»)", "indice + élément"),
            ("§«d».items()", "paires clé / valeur"),
            ("zip(«a», «b»)", "parcourir en parallèle"),
            ("range(«a», «b», «pas»)", "suite d'entiers"),
            ("break  continue", "sortir / suivant"),
            ("match «x»: case …:", "filtrage de motifs"),
            ("§with open(«f») as f:", "fermeture auto"),
            ("§try: … except «E» as e:", "gérer une erreur"),
            ('raise «E»("…") from e', "lever / chaîner"),
            ("finally:", "toujours exécuté"),
            ("assert «cond», «msg»", "vérification"),
        ]),
        ("Compréhensions", "", 250, [
            ("§[«f(x)» for x in «it»]", "liste"),
            ("[x for x in «it» if «c»]", "avec filtre"),
            ("{k: v for k, v in «it»}", "dictionnaire"),
            ("(x for x in «it»)", "générateur (paresseux)"),
            ("any(…)  all(…)", "au moins un / tous"),
            ("sum  min  max", "agrégats"),
            ("§sorted(«it», key=«f»)", "trier (copie)"),
            ("lambda x: «expr»", "fonction anonyme"),
        ]),
        ("Fonctions", "", 250, [
            ("def f(«a», «b»=1):", "valeur par défaut"),
            ("def f(*args, **kw):", "arguments variables"),
            ("def f(a, /, b, *, c):", "positionnel / nommé"),
            ("«x»: «T»  -> «T»", "annotations de type"),
            ("§return  yield", "renvoyer / générer"),
            ("@«décorateur»", "envelopper"),
            ("global  nonlocal", "portée"),
        ]),
        ("Fichiers & E/S", "", 250, [
            ('open(«f», "w")', "écrire (a : ajouter)"),
            ("for ligne in «f»:", "lire ligne à ligne"),
            ('encoding="utf-8"', "toujours le préciser"),
            ("file=sys.stderr", "print vers stderr"),
            ("input(«msg»)", "lire au clavier"),
            ("sys.argv  sys.exit(«n»)", "arguments / quitter"),
            ('__name__ == "__main__"', "point d'entrée"),
            ("os.environ[«VAR»]", "variable d'env."),
            ("csv.DictReader(«f»)", "lire un CSV"),
        ]),
    ],
    [  # colonne 3
        ("Classes", "", 250, [
            ("class «C»(«Base»):", "héritage"),
            ("§def __init__(self, …):", "constructeur"),
            ("super().__init__(…)", "parent"),
            ("§@dataclass", "classe de données"),
            ("@dataclass(frozen=True)", "immuable"),
            ("@property", "attribut calculé"),
            ("@classmethod", "constructeur alternatif"),
            ("@staticmethod", "sans self"),
            ("__repr__  __str__", "affichage"),
            ("__eq__  __lt__  __hash__", "comparaison"),
            ("__len__  __iter__", "protocoles"),
            ("__enter__  __exit__", "gestionnaire with"),
        ]),
        ("Bibliothèque standard", "", 250, [
            ("§from pathlib import Path", "chemins"),
            ("Path(«p»).read_text()", "lire un fichier"),
            ('«p».glob("**/*.py")', "chercher"),
            ("json.loads  json.dumps", "JSON"),
            ("§collections.Counter", "compter"),
            ("defaultdict(list)", "dict avec défaut"),
            ("itertools.groupby", "regrouper"),
            ("functools.cache", "mémoïser"),
            ("datetime.now()", "date courante"),
            ("re.findall(«rx», «s»)", "regex"),
            ("subprocess.run([…])", "lancer une commande"),
            ("logging.getLogger()", "journalisation"),
            ("argparse", "arguments CLI"),
        ]),
        ("Asynchrone", "asyncio", 250, [
            ("async def f():", "coroutine"),
            ("await «coro»", "attendre"),
            ("§asyncio.run(main())", "lancer"),
            ("asyncio.gather(…)", "en parallèle"),
            ("async with  async for", "variantes async"),
        ]),
        ("Typage", "", 250, [
            ("list[int]  set[str]", "génériques"),
            ("«T» | None", "optionnel"),
            ("type «Alias» = …", "alias de type"),
            ("def f[T](x: T) -> T:", "fonction générique"),
            ("Protocol  TypedDict", "structures"),
            ("Literal  Final", "valeurs fixes"),
        ]),
    ],
]

OUTILS = [
    [
        ("Environnements", "venv · pip", 250, [
            ("§python -m venv .venv", "créer un venv"),
            ("§. .venv/bin/activate", "activer (bash/zsh)"),
            ("deactivate", "désactiver"),
            ("§pip install «pkg»", "installer"),
            ("pip install -e .", "projet éditable"),
            ("pip install -r «f».txt", "depuis un fichier"),
            ("pip freeze > «f».txt", "figer les versions"),
            ("pip list --outdated", "paquets à màj"),
            ("pip show «pkg»", "infos / dépendances"),
            ("pip uninstall «pkg»", "désinstaller"),
            ("pipx install «outil»", "CLI isolée"),
        ]),
        ("uv", "", 250, [
            ("§uv init", "nouveau projet"),
            ("§uv add «pkg»", "ajouter une dép."),
            ("uv add --dev pytest", "dépendance de dev"),
            ("uv remove «pkg»", "retirer"),
            ("§uv run «cmd»", "lancer dans le venv"),
            ("uv sync", "installer le lockfile"),
            ("uv lock --upgrade", "mettre à jour"),
            ("uv python install 3.14", "installer un Python"),
            ("uvx «outil»", "outil jetable"),
            ("uv pip install «pkg»", "pip, en rapide"),
        ]),
        ("pyproject.toml", "", 250, [
            ("[project]", "nom, version"),
            ("dependencies = […]", "dépendances"),
            ("requires-python", "version minimale"),
            ("[project.scripts]", "commandes CLI"),
            ("[tool.ruff]", "config des outils"),
            ("[build-system]", "backend de build"),
        ]),
        ("REPL & scripts", "", 250, [
            ("python", "REPL interactif"),
            ("_", "dernier résultat"),
            ("help(«obj»)", "aide"),
            ("dir(«obj»)", "attributs"),
            ("#!/usr/bin/env python3", "shebang"),
            ("python -m «module»", "lancer un module"),
            ("python -O", "sans les assert"),
            ("PYTHONPATH=«dir»", "chemins d'import"),
            ("python -W error", "warnings → erreurs"),
        ]),
    ],
    [
        ("Tests", "pytest", 250, [
            ("§pytest", "lancer les tests"),
            ("pytest -x", "arrêt au 1er échec"),
            ("§pytest -k «motif»", "filtrer par nom"),
            ("pytest «f»::«test»", "un seul test"),
            ("pytest -v  -q", "verbeux / silencieux"),
            ("§pytest --lf", "relancer les échecs"),
            ("pytest -s", "voir les print"),
            ("pytest --pdb", "pdb sur échec"),
            ("pytest --cov", "couverture (plugin)"),
            ("pytest -n auto", "parallèle (xdist)"),
            ("monkeypatch  tmp_path", "fixtures intégrées"),
            ("assert «a» == «b»", "vérifier"),
            ("pytest.raises(«E»)", "attendre une exception"),
            ("@pytest.fixture", "fixture"),
            ("@pytest.mark.parametrize", "cas multiples"),
        ]),
        ("Qualité", "", 250, [
            ("§ruff check .", "linter"),
            ("ruff check --fix", "corriger"),
            ("§ruff format", "formater"),
            ("mypy «src»", "typage statique"),
            ("mypy --strict", "typage strict"),
            ("pre-commit install", "hooks git"),
        ]),
        ("Déboguer & profiler", "pdb", 250, [
            ("§breakpoint()", "point d'arrêt"),
            ("n  s", "ligne suiv. / entrer"),
            ("c  q", "continuer / quitter"),
            ("p «x»  pp «x»", "afficher"),
            ("python -m pdb «f».py", "lancer sous pdb"),
            ("python -m cProfile «f»", "profiler"),
            ("python -X importtime", "temps d'import"),
            ("python -i «f».py", "interactif après"),
        ]),
        ("python -m utiles", "", 250, [
            ("python -m http.server", "serveur HTTP local"),
            ("python -m json.tool «f»", "formater du JSON"),
            ("python -m zipfile -l «f»", "lister un zip"),
            ('python -m timeit "…"', "chronométrer"),
            ('python -c "«code»"', "exécuter une ligne"),
        ]),
    ],
]

# Bleu et jaune Python, paramètres en vert
ACCENTS = {
    "aritim": "--a:#3daee9; --b:#fdbc4b; --param:#27ae60;",
    "dark":   "--a:#6cb2ff; --b:#f3d36a; --param:#7ee2a2;",
    "light":  "--a:#0b5cad; --b:#7a5a00; --param:#14713a;",
    "amoled": "--a:#5b9ae0; --b:#cdb35a; --param:#5cc485;",
}

BRAND_LANG = ('<h2><span class="prompt">&gt;&gt;&gt;</span>PYTHON<span class="cursor under"></span></h2>'
              '<small>3.12+ · <i>paramètres</i> · <span class="warn">⚠</span> destructif · '
              '<span class="ess-key"></span>essentiel</small>')
BRAND_TOOLS = ('<small>venv · pip · uv · pytest · ruff</small>'
               '<h2><span class="prompt">$</span>OUTILS</h2>')

if __name__ == "__main__":
    build_two_zones("python", "Python", ACCENTS, BRAND_LANG, BRAND_TOOLS, LANGAGE, OUTILS)
