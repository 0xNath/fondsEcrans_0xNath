"""Fond d'écran aide-mémoire Git + outils Linux.

Modifier le contenu ci-dessous, puis :
    make html        -> génère build/html/git-linux-{aritim,dark,light,amoled}.html
    make             -> exporte aussi les PNG dans wallpapers/

Syntaxe : «x» = paramètre (couleur secondaire) ; une description qui commence
par "⚠ " est marquée comme destructive.
Panneau : (titre, étiquette ou "", largeur colonne commande en px ou None, lignes)
Côté Git, le préfixe « git » est omis.
"""
from common import build_two_zones

GIT = [
    [  # colonne 1
        ("Configurer & démarrer", "git config", 268, [
            ("config --global user.name", "votre nom"),
            ("config --global user.email", "votre e-mail"),
            ("config --global -e", "éditer la config"),
            ("config --list", "afficher la config"),
            ("init", "créer un dépôt ici"),
            ("§clone «url»", "cloner un dépôt"),
            ("clone --depth 1 «url»", "clone superficiel"),
        ]),
        ("Indexer & valider", "git add · commit", 246, [
            ("§status -sb", "état court + branche"),
            ("§add «fichier»", "indexer un fichier"),
            ("§add -p", "indexer par morceaux"),
            ("add -A", "tout indexer"),
            ("restore «fichier»", "⚠ jeter les modifs"),
            ("§restore --staged «f»", "désindexer"),
            ("rm --cached «f»", "ne plus suivre"),
            ("mv «a» «b»", "renommer / déplacer"),
            ('§commit -m "«msg»"', "valider"),
            ('commit -am "«msg»"', "indexer + valider"),
            ("§commit --amend", "corriger le dernier"),
            ("commit --amend --no-edit", "… sans le message"),
        ]),
        ("Inspecter", "git log · diff", 232, [
            ("§log --oneline --graph", "historique (+ --all)"),
            ("log -p «fichier»", "historique d'un fichier"),
            ("log --author=«nom»", "commits d'un auteur"),
            ("log -S «texte»", "qui a ajouté/retiré texte"),
            ("§diff", "modifs non indexées"),
            ("§diff --staged", "modifs indexées"),
            ("diff «a»..«b»", "entre deux commits"),
            ("show «commit»", "détail d'un commit"),
            ("blame «fichier»", "auteur de chaque ligne"),
            ("shortlog -sn", "commits par auteur"),
            ("reflog", "journal de HEAD"),
        ]),
        (".gitignore", "", 160, [
            ("*.log", "tous les .log"),
            ("build/", "un dossier entier"),
            ("/todo.txt", "seulement à la racine"),
            ("**/tmp", "tmp à n'importe quel niveau"),
            ("!keep.log", "exception à une règle"),
        ]),
    ],
    [  # colonne 2
        ("Branches", "git switch · branch", 214, [
            ("branch", "branches locales"),
            ("branch -a", "… et distantes"),
            ("branch -vv", "avec branche amont"),
            ("§switch «b»", "changer de branche"),
            ("§switch -c «b»", "créer et basculer"),
            ("switch -", "branche précédente"),
            ("branch -m «nom»", "renommer la courante"),
            ("branch -d «b»", "supprimer (si fusionnée)"),
            ("branch -D «b»", "⚠ forcer la suppression"),
        ]),
        ("Fusionner & rebaser", "git merge · rebase", 214, [
            ("§merge «b»", "fusionner b ici"),
            ("merge --no-ff «b»", "avec commit de fusion"),
            ("merge --abort", "annuler la fusion"),
            ("rebase «b»", "rejouer mes commits sur b"),
            ("§rebase -i HEAD~«n»", "réécrire les n derniers"),
            ("rebase --continue", "après résolution du conflit"),
            ("rebase --abort", "annuler le rebase"),
            ("cherry-pick «commit»", "appliquer un commit ici"),
            ("mergetool", "outil de résolution"),
        ]),
        ("Dépôts distants", "git remote · push", 236, [
            ("remote -v", "lister les distants"),
            ("remote add «nom» «url»", "ajouter un distant"),
            ("fetch --prune", "récupérer et nettoyer"),
            ("pull", "fetch + merge"),
            ("§pull --rebase", "fetch + rebase"),
            ("§push", "envoyer"),
            ("§push -u origin «b»", "publier + suivre"),
            ("push --force-with-lease", "⚠ forcer (prudemment)"),
            ("push -d origin «b»", "suppr. branche distante"),
            ("push --tags", "envoyer les tags"),
        ]),
        ("Remiser", "git stash", 220, [
            ("§stash", "mettre de côté"),
            ("stash -u", "… y compris non suivis"),
            ('stash push -m "«msg»"', "avec un message"),
            ("stash list", "lister"),
            ("§stash pop", "réappliquer et retirer"),
            ("stash apply stash@{«n»}", "réappliquer, garder"),
            ("stash drop", "supprimer la dernière"),
        ]),
    ],
    [  # colonne 3
        ("Annuler", "", 226, [
            ("restore .", "⚠ jeter toutes les modifs"),
            ("§reset HEAD~1", "défaire le commit, garder"),
            ("reset --soft HEAD~1", "… garder indexé"),
            ("reset --hard «commit»", "⚠ revenir, tout jeter"),
            ("reset --hard HEAD@{1}", "annuler le dernier reset"),
            ("§revert «commit»", "commit inverse (sûr)"),
            ("restore -s «c» «f»", "fichier tel qu'en c"),
            ("commit --fixup «c»", "commit correctif pour c"),
            ("rebase -i --autosquash", "… l'intégrer à c"),
            ("clean -n", "simuler le nettoyage"),
            ("clean -fd", "⚠ suppr. les non suivis"),
        ]),
        ("Références", "gitrevisions", 172, [
            ("HEAD", "commit courant"),
            ("HEAD~«n»", "n-ième ancêtre"),
            ("HEAD^2", "2e parent (fusion)"),
            ("HEAD@{«n»}", "n-ième position de HEAD"),
            ("main@{yesterday}", "main telle qu'hier"),
            ("@{u}", "branche amont"),
            ("@{-1}", "branche précédente"),
            ("«a»..«b»", "commits de b absents de a"),
            ("«a»...«b»", "commits propres à a ou b"),
        ]),
        ("Tags & outils", "", 226, [
            ("tag", "lister les tags"),
            ('tag -a v1.0 -m "«msg»"', "tag annoté"),
            ("describe --tags", "version selon les tags"),
            ("bisect start", "trouver le commit fautif"),
            ("bisect good  bad", "marquer le commit testé"),
            ("bisect reset", "terminer la recherche"),
            ("worktree add «dir» «b»", "2e copie de travail"),
            ("grep «motif»", "chercher dans le dépôt"),
            ("archive -o a.zip HEAD", "exporter en archive"),
        ]),
        ("Workflow type", "", 236, [
            ("switch -c feat/«x»", "1. nouvelle branche"),
            ("add -p ; commit", "2. petits commits"),
            ("fetch origin", "3. récupérer"),
            ("rebase origin/main", "4. se mettre à jour"),
            ("push -u origin feat/«x»", "5. publier → PR"),
            ("switch main ; pull", "6. après la fusion"),
            ("branch -d feat/«x»", "7. faire le ménage"),
        ]),
    ],
]

LINUX = [
    [
        ("Fichiers", "", 214, [
            ("§ls -lah", "détails, cachés, tailles"),
            ("§cd -", "dossier précédent"),
            ("§cp -r «src» «dst»", "copier récursivement"),
            ("mv «a» «b»", "déplacer / renommer"),
            ("rm -rf «dir»", "⚠ supprimer sans retour"),
            ("§mkdir -p «a/b/c»", "créer l'arborescence"),
            ("ln -s «cible» «lien»", "lien symbolique"),
            ("tree -L 2", "arborescence (2 niveaux)"),
            ("du -sh *", "taille de chaque élément"),
            ("df -h", "espace disque libre"),
        ]),
        ("Lire & chercher", "", 226, [
            ("§less «f»", "paginer (/ = chercher)"),
            ("head  tail -n «n»", "début / fin du fichier"),
            ("§tail -f «log»", "suivre en direct"),
            ("§grep -rn «motif» .", "chercher récursivement"),
            ("grep -i  -v", "casse / inverser"),
            ("grep -c  -l", "compter / fichiers"),
            ('§find . -name "*.py"', "trouver par nom"),
            ("find -type f -mtime -1", "modifiés < 24 h [GNU]"),
            ("rg «motif»", "ripgrep, rapide"),
            ("fd «motif»", "find moderne"),
        ]),
        ("Traiter du texte", "", 214, [
            ("wc -l", "compter les lignes"),
            ("§sort | uniq -c", "compter les doublons"),
            ("sort -nr -k2", "num., inversé, col. 2"),
            ("cut -d, -f1,3", "colonnes 1 et 3 (CSV)"),
            ("awk '{print $2}'", "2e colonne"),
            ("sed -i 's/«a»/«b»/g'", "en place [GNU]"),
            ("tr a-z A-Z", "transformer des car."),
            ("xargs -I{} «cmd» {}", "une cmd par ligne"),
            ("jq '.«clé»'", "extraire du JSON"),
            ("diff -u «a» «b»", "comparer deux fichiers"),
        ]),
        ("Archives", "", 250, [
            ("§tar -czf «a».tar.gz «dir»", "créer"),
            ("§tar -xzf «a».tar.gz", "extraire (-C dossier)"),
            ("tar -tf «a».tar.gz", "lister le contenu"),
            ("zip -r «a».zip «dir»", "créer un zip (unzip)"),
        ]),
    ],
    [
        ("Processus & services", "", 228, [
            ("§ps aux | grep «nom»", "trouver un processus"),
            ("htop", "moniteur interactif"),
            ("§kill  kill -9 «pid»", "arrêter / forcer"),
            ("pkill «nom»", "arrêter par nom"),
            ("«cmd» &", "lancer en arrière-plan"),
            ("Ctrl-z  bg  fg", "suspendre / reprendre"),
            ("nohup «cmd» &", "survit à la déconnexion"),
            ("watch -n 2 «cmd»", "relancer toutes les 2 s"),
            ("free -h", "mémoire utilisée"),
            ("systemctl status «svc»", "état d'un service"),
            ("journalctl -u «svc» -f", "logs du service, en direct"),
        ]),
        ("Permissions", "", 214, [
            ("§chmod +x «f»", "rendre exécutable"),
            ("chmod 644 «f»", "rw-r--r--"),
            ("chmod 755 «dir»", "rwxr-xr-x"),
            ("chown «u»:«g» «f»", "changer le propriétaire"),
            ("sudo «cmd»", "exécuter en root"),
            ("§sudo !!", "relancer la dernière en root"),
            ("whoami  id", "utilisateur / groupes"),
        ]),
        ("Réseau", "", 228, [
            ("ip a", "interfaces et adresses"),
            ("ss -tulpn", "ports en écoute"),
            ("ping «hôte»", "tester la connexion"),
            ("dig «domaine»", "résolution DNS"),
            ("curl -I «url»", "en-têtes HTTP"),
            ("curl -LO «url»", "télécharger un fichier"),
            ("§ssh «u»@«hôte»", "connexion distante"),
            ("scp «f» «hôte»:«dir»", "copier vers un serveur"),
            ("§rsync -avz «src» «dst»", "synchroniser"),
        ]),
        ("Shell & redirections", "bash", 180, [
            (">  >>", "écrire / ajouter"),
            ("§2>&1  &>", "stderr / tout vers …"),
            ("|", "enchaîner (pipe)"),
            ("&&  ||", "si succès / si échec"),
            ("$(«cmd»)", "insérer la sortie"),
            ("!!  !$", "dernière cmd / dernier arg."),
            ("§Ctrl-r", "chercher dans l'historique"),
            ("Ctrl-a  Ctrl-e", "début / fin de ligne"),
            ("Ctrl-w  Ctrl-u", "effacer mot / début ligne"),
        ]),
    ],
]

ACCENTS = {
    "aritim": "--a:#f67400; --b:#27ae60; --param:#5d88ca;",
    "dark":   "--a:#ff8f6b; --b:#6fd3e6; --param:#c6a8ff;",
    "light":  "--a:#b23a17; --b:#0a6678; --param:#6a3fb5;",
    "amoled": "--a:#e57a59; --b:#58b5c7; --param:#a98fe6;",
}

BRANCH_SVG = """<svg class="graph" viewBox="0 0 120 48" aria-hidden="true">
  <path d="M8 34 H112" stroke="var(--a)" stroke-width="3" fill="none"/>
  <path d="M34 34 C46 34 46 12 58 12 H78 C90 12 90 34 102 34" stroke="var(--param)" stroke-width="3" fill="none"/>
  <circle cx="14" cy="34" r="6" fill="var(--a)"/><circle cx="34" cy="34" r="6" fill="var(--a)"/>
  <circle cx="64" cy="12" r="6" fill="var(--param)"/><circle cx="72" cy="34" r="6" fill="var(--a)"/>
  <circle cx="102" cy="34" r="7" fill="var(--bg)" stroke="var(--a)" stroke-width="3"/>
</svg>"""

BRAND_GIT = ("<h2>GIT</h2>" + BRANCH_SVG +
             '<small>préfixe « git » omis · <i>paramètres</i> · <span class="warn">⚠</span> destructif · '
             '<span class="ess-key"></span>essentiel</small>')
BRAND_LINUX = ('<small>bash · coreutils · réseau · système</small>'
               '<h2><span class="prompt">~$</span>LINUX<span class="cursor"></span></h2>')

if __name__ == "__main__":
    build_two_zones("git-linux", "Git · Linux", ACCENTS, BRAND_GIT, BRAND_LINUX, GIT, LINUX)
