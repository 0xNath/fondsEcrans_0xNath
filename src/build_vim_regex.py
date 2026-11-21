"""Fond d'écran aide-mémoire Vim + Regex.

Modifier le contenu ci-dessous, puis :
    make html        -> génère build/html/vim-regex-{aritim,dark,light,amoled}.html
    make             -> exporte aussi les PNG dans wallpapers/ (Chromium + Playwright)

Syntaxe : «x» = paramètre (affiché dans la couleur secondaire).
Chaque panneau : (titre, étiquette :help ou "", largeur colonne commande en px ou None, lignes)
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "build" / "html"

VIM = [
    [  # colonne 1
        ("Modes", "vim-modes", None, [
            ("§Esc  Ctrl-[", "retour au mode normal"),
            ("§i  a", "insérer avant / après"),
            ("§v", "visuel (caractères)"),
            ("V", "visuel (lignes)"),
            ("Ctrl-v", "visuel (bloc)"),
            ("R", "mode remplacement"),
            ("§:", "ligne de commande"),
        ]),
        ("Déplacements", "motion.txt", None, [
            ("§h j k l", "← ↓ ↑ →"),
            ("§w  b  e  ge", "mot suiv. / préc. / fin / fin préc."),
            ("W  B  E", "idem, MOTS (sép. par espace)"),
            ("gj  gk", "ligne affichée (texte replié)"),
            ("§0  ^  $", "début / 1er car. / fin de ligne"),
            ("§gg  G  «n»G", "début / fin / ligne n"),
            ("H  M  L", "haut / milieu / bas de l'écran"),
            ("{  }", "paragraphe préc. / suivant"),
            ("%", "parenthèse correspondante"),
            ("f«c»  t«c»", "sur / juste avant le car. c"),
            ("F«c»  T«c»", "idem, vers l'arrière"),
            (";  ,", "répéter f/t (avant / arrière)"),
            ("Ctrl-d  Ctrl-u", "½ page bas / haut"),
            ("Ctrl-f  Ctrl-b", "page entière bas / haut"),
            ("Ctrl-e  Ctrl-y", "défiler d'une ligne"),
            ("zz  zt  zb", "ligne au centre / haut / bas"),
        ]),
        ("Édition", "change.txt", None, [
            ("I  A", "insérer en début / fin de ligne"),
            ("o  O", "ligne en dessous / au-dessus"),
            ("§d«m» c«m» y«m»", "couper / changer / copier"),
            ("§dd  cc  yy", "… sur la ligne entière"),
            ("D  C", "couper / changer → fin de ligne"),
            ("§p  P", "coller après / avant"),
            ("x  r«c»", "suppr. / remplacer un car."),
            ("s  S", "remplacer le car. / la ligne"),
            ("xp  ddp", "échanger 2 car. / 2 lignes"),
            ("J", "joindre avec la ligne suivante"),
            ("§u  Ctrl-r", "annuler / rétablir"),
            ("§.", "répéter la dernière modification"),
            (">>  <<", "indenter / désindenter"),
            ("=«m»  ==", "réindenter (mouvement / ligne)"),
            ("~  gu«m»  gU«m»", "inverser / min. / MAJ."),
            ("Ctrl-a  Ctrl-x", "incrémenter / décrémenter"),
        ]),
    ],
    [  # colonne 2
        ("Objets textuels", "text-objects", None, [
            ("iw  aw", "mot (seul / avec espace)"),
            ('i"  a"', "entre guillemets"),
            ("i(  a(", "entre parenthèses"),
            ("i{  a{", "entre accolades"),
            ("i[  a[", "entre crochets"),
            ("i<  a<", "entre chevrons"),
            ("it  at", "balise HTML / XML"),
            ("ip  ap", "paragraphe"),
            ("§ciw  da(  yi\"", "exemples : opérateur + objet"),
        ]),
        ("Mode visuel", "visual-operators", None, [
            ("o", "aller à l'autre extrémité"),
            ("gv", "resélectionner"),
            ("iw  ip  i(", "étendre avec un objet"),
            (">  <  =", "indenter / réindenter"),
            ("u  U", "minuscules / majuscules"),
            ("I  A", "(bloc) insérer sur chaque ligne"),
            (":", ":'<,'> agir sur la sélection"),
            ("r«c»", "remplacer la sélection par c"),
            ("J", "joindre les lignes"),
        ]),
        ("Rechercher & remplacer", "pattern", None, [
            ("§/«motif»  ?«motif»", "chercher avant / arrière"),
            ("§n  N", "occurrence suiv. / préc."),
            ("*  #", "mot sous le curseur ↓ / ↑"),
            (":s/«a»/«b»/", "1re occurrence de la ligne"),
            (":s/«a»/«b»/g", "toute la ligne"),
            ("§:%s/«a»/«b»/g", "tout le fichier"),
            (":%s/«a»/«b»/gc", "… avec confirmation"),
            (":%s//«b»/g", "réutiliser la dernière recherche"),
            ("cgn  .", "changer les occurrences 1 à 1"),
            (":noh", "effacer le surlignage"),
        ]),
        ("Macros & registres", "registers", None, [
            ("q«a» … q", "enregistrer la macro a"),
            ("q«A»", "compléter la macro a"),
            ("@«a»  @@", "jouer a / rejouer la dernière"),
            ("10@«a»", "jouer la macro 10 fois"),
            (":%norm @«a»", "jouer a sur chaque ligne"),
            ('"«a»yy  "«a»p', "copier / coller via le reg. a"),
            ('"0p', "coller la dernière copie"),
            ('"+y  "+p', "presse-papiers système"),
            (":reg", "lister les registres"),
        ]),
    ],
    [  # colonne 3
        ("Marques, sauts & plis", "mark-motions", None, [
            ("m«a»", "poser la marque a"),
            ("'«a»  `«a»", "aller à la ligne / position de a"),
            ("''", "revenir avant le dernier saut"),
            ("Ctrl-o  Ctrl-i", "position préc. / suivante"),
            ("gi", "reprendre la dernière insertion"),
            ("`.", "dernière modification"),
            ("gd  gf", "définition / fichier sous curseur"),
            ("za  zo  zc", "basculer / ouvrir / fermer un pli"),
            ("zR  zM", "tout déplier / tout plier"),
        ]),
        ("Fichiers, buffers & onglets", "windows", None, [
            ("§:w  :q  :wq", "enreg. / quitter / les deux"),
            (":q!", "quitter sans enregistrer"),
            (":wa  :qa", "tout enregistrer / tout quitter"),
            (":e «fichier»", "ouvrir un fichier"),
            (":sav «fichier»", "enregistrer sous"),
            (":ls  :b«n»", "lister / aller au buffer n"),
            (":bn  :bp  :bd", "buffer suiv. / préc. / fermer"),
            (":sp  :vsp", "diviser horiz. / vert."),
            ("Ctrl-w h/j/k/l", "changer de fenêtre"),
            ("Ctrl-w =", "égaliser les fenêtres"),
            ("Ctrl-w o", "ne garder que cette fenêtre"),
            (":tabe «fichier»", "ouvrir dans un onglet"),
            ("gt  gT", "onglet suivant / précédent"),
        ]),
        ("Commandes Ex", "ex-cmd-index", None, [
            (":g/«motif»/d", "suppr. les lignes trouvées"),
            (":v/«motif»/d", "suppr. les autres lignes"),
            (":«n»,«m»d", "supprimer les lignes n à m"),
            (":sort u", "trier, sans doublons"),
            (":earlier 5m", "revenir 5 minutes en arrière"),
            (":%norm A;", "ajouter ; à chaque ligne"),
            (":!«cmd»", "exécuter une commande shell"),
            (":r !«cmd»", "insérer la sortie de cmd"),
            (":%!«filtre»", "filtrer le fichier (ex. jq .)"),
        ]),
        ("Mode insertion", "ins-special-keys", None, [
            ("Ctrl-n  Ctrl-p", "compléter un mot (suiv. / préc.)"),
            ("Ctrl-x Ctrl-f", "compléter un chemin de fichier"),
            ("Ctrl-r «a»", "insérer le registre a"),
            ("Ctrl-w  Ctrl-u", "effacer le mot / la ligne"),
            ("Ctrl-o «cmd»", "une commande normale"),
            ("Ctrl-t  Ctrl-d", "indenter / désindenter"),
        ]),
    ],
]

REGEX = [
    [
        ("Classes", "", None, [
            ("§.", "n'importe quel caractère"),
            ("§\\d  \\D", "chiffre / non-chiffre"),
            ("§\\w  \\W", "[A-Za-z0-9_] / l'inverse"),
            ("§\\s  \\S", "espace blanc / l'inverse"),
            ("§[abc]  [^abc]", "a, b ou c / tout sauf"),
            ("[a-z]  [0-9]", "plages de caractères"),
            ("[\\s\\S]", "tout, saut de ligne compris"),
            ("\\.  \\(  \\\\", "caractère littéral (échappé)"),
        ]),
        ("POSIX & échappements", "=grep · sed · PCRE", 214, [
            ("[[:alpha:]]", "lettres"),
            ("[[:digit:]]", "chiffres"),
            ("[[:alnum:]]", "lettres et chiffres"),
            ("[[:space:]]", "espaces blancs"),
            ("[[:upper:]]", "majuscules ([:lower:])"),
            ("[[:punct:]]", "ponctuation"),
            ("\\t  \\n  \\r", "tab / saut / retour chariot"),
            ("\\x41  \\u00e9", "caractère par code"),
        ]),
        ("Quantificateurs", "", None, [
            ("§*  +  ?", "0 ou + / 1 ou + / 0 ou 1"),
            ("{«n»}", "exactement n"),
            ("{«n»,}", "n ou plus"),
            ("§{«n»,«m»}", "de n à m"),
            ("*?  +?  ??", "non gourmands (au plus court)"),
            ("*+  ++", "possessifs [PCRE]"),
        ]),
        ("Ancres", "", None, [
            ("§^  $", "début / fin (de ligne avec m)"),
            ("\\b  \\B", "limite de mot / pas une limite"),
            ("\\A  \\Z", "début / fin de la chaîne"),
        ]),
    ],
    [
        ("Groupes & alternatives", "", None, [
            ("§(…)", "groupe capturant"),
            ("(?:…)", "groupe non capturant"),
            ("(?>…)", "groupe atomique (PCRE)"),
            ("(?<«nom»>…)", "groupe nommé (PCRE, JS)"),
            ("(?P<«nom»>…)", "groupe nommé (Python)"),
            ("§«a»|«b»", "a ou b"),
            ("\\1  \\k<«nom»>", "réutiliser un groupe"),
        ]),
        ("Assertions", "", None, [
            ("(?=…)  (?!…)", "suivi / non suivi de …"),
            ("(?<=…)  (?<!…)", "précédé / non précédé de …"),
        ]),
        ("Drapeaux", "", None, [
            ("i", "insensible à la casse"),
            ("m", "^ et $ à chaque ligne"),
            ("s", ". inclut le saut de ligne"),
            ("x", "mode étendu (espaces ignorés)"),
            ("g", "toutes les occurr. (JS, sed)"),
            ("(?i)", "drapeau dans le motif"),
        ]),
        ("Spécificités Vim", "magic", None, [
            ("§\\v", "very magic : syntaxe ≈ PCRE"),
            ("\\+ \\? \\| \\( \\)", "à échapper sans \\v"),
            ("\\< \\>", "début / fin de mot (≈ \\b)"),
            ("\\{-}", "* non gourmand"),
            ("\\zs  \\ze", "début / fin du résultat"),
            ("\\@= \\@! \\@<=", "assertions (après le groupe)"),
            ("\\c  \\C", "ignorer / respecter la casse"),
            ("\\_s  \\_.", "… y compris saut de ligne"),
            ("\\%V", "dans la sélection visuelle"),
            ("&  \\1  \\r", "tout / groupe 1 / saut (rempl.)"),
        ]),
    ],
]

EXAMPLES = [
    ("[\\w.+-]+@[\\w-]+\\.[\\w.]+", "adresse e-mail (simplifiée)"),
    ("\\d{4}-\\d{2}-\\d{2}", "date AAAA-MM-JJ"),
    ("\\b(\\w+)\\s+\\1\\b", "mot répété (« le le »)"),
    ("#[0-9a-fA-F]{6}\\b", "couleur hexadécimale"),
    (":%s/\\s\\+$//e", "Vim : espaces en fin de ligne"),
    (":g/^\\s*$/d", "Vim : supprimer les lignes vides"),
    (":%s/\\v(\\d{4})-(\\d{2})-(\\d{2})/\\3\\/\\2\\/\\1/g", "Vim : AAAA-MM-JJ → JJ/MM/AAAA"),
    ("grep -rnE '\\bTODO\\b' .", "shell : les TODO, avec n° de ligne"),
    ("sed -E 's/(\\w+) (\\w+)/\\2 \\1/'", "shell : inverser deux mots"),
]

THEMES = {
    # Aritim Dark (palette Plasma de Mrcuve0/Aritim-Dark)
    "aritim": """
  --bg:#10151a; --bg2:#141a21; --grid:rgba(146,152,165,.04);
  --panel:rgba(20,26,33,.96); --border:#2f343f;
  --text:#d3dae3; --text2:#bcc3ce; --muted:#9298a5; --hl:rgba(43,82,120,.45); --warn:#da4453;
  --vim:#27ae60; --rx:#f67400; --param:#5d88ca; --on-accent:#10151a;""",
    "dark": """
  --bg:#0c1220; --bg2:#111a2d; --grid:rgba(140,170,220,.05);
  --panel:rgba(19,28,46,.94); --border:rgba(130,160,210,.16);
  --text:#cdd5e3; --text2:#b3bccb; --muted:#8792a8; --hl:rgba(255,255,255,.075); --warn:#ff6ad5;
  --vim:#7ee2a2; --rx:#f3bb6a; --param:#82b8ff; --on-accent:#0c1220;""",
    "light": """
  --bg:#f2eee5; --bg2:#e9e4d8; --grid:rgba(60,70,90,.06);
  --panel:rgba(252,250,245,.96); --border:rgba(60,70,90,.16);
  --text:#1c2230; --text2:#3a4152; --muted:#5a6273; --hl:rgba(30,40,60,.07); --warn:#b0128a;
  --vim:#14713a; --rx:#8a5500; --param:#1f5fbf; --on-accent:#ffffff;""",
    # AMOLED : noir pur, aucun dégradé ni grille (pixels éteints), texte un peu adouci
    "amoled": """
  --bg:#000000; --bg2:#000000; --grid:transparent;
  --panel:#000000; --border:#232a33;
  --text:#aab2be; --text2:#929aa7; --muted:#6f7886; --hl:#14171c; --warn:#d85cb8;
  --vim:#5cc485; --rx:#d99f4f; --param:#6c9be0; --on-accent:#000000;""",
}


from common import CSS as COMMON_CSS, rows_html, columns



TEMPLATE = """<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8"><title>Vim · Regex — fond d'écran (__THEME__)</title>
<style>
:root { __VARS__ }
* { box-sizing:border-box; margin:0; padding:0; }
html,body { width:2560px; height:1440px; overflow:hidden; }
body {
  font-family:"Inter",sans-serif; color:var(--text);
  background:
    linear-gradient(var(--grid) 1px, transparent 1px) 0 0/40px 40px,
    linear-gradient(90deg, var(--grid) 1px, transparent 1px) 0 0/40px 40px,
    linear-gradient(160deg, var(--bg), var(--bg2));
  padding:56px 60px; display:flex; gap:44px;
}
.k, .tag, .brand small { font-family:"MesloLGS Nerd Font","MesloLGS NF","MesloLGS Nerd Font Mono","DejaVu Sans Mono",monospace; }

.zone { display:flex; flex-direction:column; gap:20px; min-width:0; }
.zone.vim { flex:3 1 0; }
.zone.rx { flex:2 1 0; }
.brand { display:flex; align-items:center; gap:18px; height:54px; padding:0 4px; }
.brand h2 { font-family:"Inter Display","Inter",sans-serif; font-weight:800; font-size:50px; letter-spacing:.04em; line-height:1; }
.vim .brand h2 { color:var(--vim); }
.rx .brand h2 { color:var(--rx); }
.cursor { display:inline-block; width:22px; height:44px; background:var(--vim); border-radius:2px; margin-left:6px; vertical-align:-4px; }
.brand small { font-size:17px; color:var(--muted); margin-top:12px; }
.brand small i { font-style:normal; color:var(--param); font-weight:bold; }
.rx .brand { justify-content:flex-end; }

.cols { display:grid; gap:18px; flex:1; min-height:0; }
.vim .cols { grid-template-columns:repeat(3,minmax(0,1fr)); }
.rx .cols { grid-template-columns:repeat(2,minmax(0,1fr)); }
.col { display:flex; flex-direction:column; justify-content:space-between; gap:12px; min-height:0; }

.panel { background:var(--panel); border:1px solid var(--border); border-radius:12px; padding:12px 18px 11px; position:relative; }
.panel::before { content:""; position:absolute; left:0; top:13px; bottom:13px; width:3px; border-radius:0 3px 3px 0; }
.panel.vim::before { background:var(--vim); }
.panel.rx::before { background:var(--rx); }
.panel header { display:flex; justify-content:space-between; align-items:baseline; margin-bottom:6px; gap:10px; }
.panel h3 { font-size:20px; font-weight:700; white-space:nowrap; }
.panel.vim h3 { color:var(--vim); }
.panel.rx h3 { color:var(--rx); }
.tag { font-size:16px; color:var(--muted); white-space:nowrap; }

.rows { display:grid; grid-template-columns:var(--kw,178px) 1fr; column-gap:14px; align-items:baseline; }
.k { font-size:17px; white-space:pre; line-height:26px; overflow:hidden; }
.vim .k { color:var(--vim); }
.rx .k { color:var(--rx); }
.k i { font-style:normal; color:var(--param); }
.d { font-size:16px; line-height:26px; white-space:nowrap; overflow:hidden; }

.examples .rows { grid-template-columns:1fr auto; }
.examples .d { color:var(--muted); text-align:right; }
__COMMON_CSS__
</style></head>
<body>
  <div class="zone vim">
    <div class="brand"><h2>VIM<span class="cursor"></span></h2>
      <small>:help — paramètres : <i>m</i> mouvement · <i>c</i> caractère · <i>n</i> nombre · <i>a</i> registre · <span class="ess-key"></span>essentiel</small></div>
    <div class="cols">__VIMCOLS__</div>
  </div>
  <div class="zone rx">
    <div class="brand"><small>syntaxe PCRE · Python · JS · grep -P</small><h2>/REGEX/</h2></div>
    <div class="cols">__RXCOLS__</div>
    <section class="panel rx examples"><header><h3>Exemples</h3><span class="tag">copier · coller · adapter</span></header>
      <div class="rows">__EXAMPLES__</div></section>
  </div>
</body></html>
"""

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, vars_ in THEMES.items():
        doc = (TEMPLATE.replace("__COMMON_CSS__", COMMON_CSS).replace("__THEME__", name).replace("__VARS__", vars_)
               .replace("__VIMCOLS__", columns(VIM, "vim", ":h "))
               .replace("__RXCOLS__", columns(REGEX, "rx", ":h "))
               .replace("__EXAMPLES__", rows_html(EXAMPLES)))
        (OUT / f"vim-regex-{name}.html").write_text(doc, encoding="utf-8")
    print("ok")
