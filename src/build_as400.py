"""Fond d'écran aide-mémoire AS/400 — IBM i 7.4 (V7R4) : CL / 5250 + Db2 for i.

Modifier le contenu ci-dessous, puis :
    make html        -> génère build/html/as400-{aritim,dark,light,amoled}.html
    make             -> exporte aussi les PNG dans wallpapers/

Conventions (voir common.py) : "§cmd" essentiel, «x» paramètre, "⚠ desc" destructif,
"desc [TR5]" badge de compatibilité.
Panneau : (titre, étiquette ou "", largeur colonne commande en px ou None, lignes)
Côté SQL, le schéma QSYS2 des services IBM i est omis.
"""
from common import build_two_zones

CL = [
    [  # colonne 1
        ("Navigation 5250", "clavier", 170, [
            ("§F1", "aide sur le champ"),
            ("§F3", "quitter"),
            ("§F4", "invite (paramètres)"),
            ("F5", "rafraîchir"),
            ("F9", "rappeler la commande"),
            ("F10", "paramètres supplémentaires"),
            ("F11", "autre vue"),
            ("§F12", "écran précédent"),
            ("F24", "autres touches"),
            ("Roll ↑ ↓", "page préc. / suiv."),
            ("Attn  SysReq", "interruption / système"),
            ("Reset", "débloquer le clavier (X II)"),
            ("Field Exit", "valider le champ"),
        ]),
        ("Lire une commande", "verbe + objet", 170, [
            ("§WRK…", "travailler avec (liste)"),
            ("DSP…  CHG…", "afficher / modifier"),
            ("CRT…  DLT…", "créer / supprimer"),
            ("STR…  END…", "démarrer / arrêter"),
            ("*LIBL  *CURLIB", "liste / bibl. courante"),
            ("*ALL  *SAME", "tout / inchangé"),
            ("«lib»/«obj»", "nom qualifié"),
            ("§2  4  5", "options : modif. / suppr. / voir"),
            ("GO MAIN", "menu principal"),
            ("SIGNOFF", "se déconnecter"),
        ]),
        ("Jobs", "", 250, [
            ("§WRKACTJOB", "jobs actifs"),
            ("WRKACTJOB SBS(«sbs»)", "… d'un sous-système"),
            ("§WRKUSRJOB", "mes jobs"),
            ("WRKSBMJOB", "jobs soumis"),
            ("§DSPJOBLOG", "historique du job"),
            ("SBMJOB CMD(«cmd»)", "soumettre en batch"),
            ("HLDJOB  RLSJOB", "suspendre / libérer"),
            ("CHGJOB", "modifier le job"),
            ("ENDJOB «j» OPTION(*IMMED)", "⚠ arrêt immédiat"),
            ("WRKJOBQ", "files d'attente"),
            ("WRKSBS", "sous-systèmes"),
            ("DSPJOB", "job courant"),
        ]),
    ],
    [  # colonne 2
        ("Objets & bibliothèques", "", 240, [
            ("§WRKLIB «lib»", "bibliothèques"),
            ("§WRKOBJ «lib»/«obj»", "objets"),
            ("§DSPLIBL", "liste de bibliothèques"),
            ("§ADDLIBLE «lib»", "ajouter à la *LIBL"),
            ("RMVLIBLE «lib»", "retirer de la *LIBL"),
            ("CHGCURLIB «lib»", "bibliothèque courante"),
            ("CRTLIB «lib»", "créer une bibliothèque"),
            ("CRTDUPOBJ", "dupliquer un objet"),
            ("MOVOBJ  RNMOBJ", "déplacer / renommer"),
            ("SAVLIB  RSTLIB", "sauver / restaurer bibl."),
            ("SAVOBJ  RSTOBJ", "sauver / restaurer objets"),
            ("DLTLIB «lib»", "⚠ supprimer une bibl."),
            ("DSPOBJD «l»/«o» *ALL", "description d'objet"),
            ("WRKOBJLCK «obj» «type»", "verrous sur un objet"),
        ]),
        ("Fichiers & membres", "", 240, [
            ("§DSPPFM «fichier»", "contenu d'un PF"),
            ("DSPFD «f»", "description du fichier"),
            ("§DSPFFD «f»", "zones du fichier"),
            ("DSPDBR «f»", "LF / vues dépendants"),
            ("§WRKMBRPDM «lib»/«f»", "membres source (PDM)"),
            ("STRPDM", "gestionnaire PDM"),
            ("CRTSRCPF «lib»/«f»", "créer un fichier source"),
            ("ADDPFM", "ajouter un membre"),
            ("CPYF «de» «vers»", "copier un fichier"),
            ("CLRPFM «f»", "⚠ vider un membre"),
            ("RGZPFM «f»", "réorganiser le membre"),
            ("RUNQRY *NONE «f»", "requête rapide"),
            ("CPYTOIMPF  CPYFRMIMPF", "export / import CSV"),
        ]),
        ("Messages", "", 240, [
            ("§WRKMSG", "messages (+ réponse)"),
            ("DSPMSG QSYSOPR", "messages opérateur"),
            ("SNDMSG … TOUSR(«u»)", "envoyer un message"),
            ("SNDBRKMSG", "message d'interruption"),
            ("WRKMSGQ", "files de messages"),
            ("DSPLOG", "historique (QHST)"),
            ("DSPMSGD «id»", "texte d'un message CPF"),
        ]),
    ],
    [  # colonne 3
        ("Spoules", "", 240, [
            ("§WRKSPLF", "mes spoules (5 = voir)"),
            ("WRKSPLF SELECT(«u»)", "d'un utilisateur"),
            ("WRKOUTQ «outq»", "file de sortie"),
            ("WRKWTR", "imprimantes (writers)"),
            ("STRPRTWTR «dev»", "démarrer un writer"),
            ("CPYSPLF", "spoule → fichier"),
            ("HLDSPLF  RLSSPLF", "suspendre / libérer"),
            ("CHGSPLFA", "attributs d'un spoule"),
        ]),
        ("Système & sécurité", "", 240, [
            ("§WRKSYSSTS", "état (CPU, ASP)"),
            ("WRKDSKSTS", "état des disques"),
            ("WRKCFGSTS *DEV", "état des unités"),
            ("GO SAVE", "menu sauvegarde"),
            ("WRKSYSVAL", "valeurs système"),
            ("DSPPTF", "PTF installées"),
            ("DSPSFWRSC", "logiciels installés"),
            ("§WRKUSRPRF «u»", "profils utilisateurs"),
            ("CHGPWD", "nouveau mot de passe"),
            ("EDTOBJAUT «obj»", "droits sur un objet"),
            ("WRKAUTL", "listes d'autorisations"),
            ("PWRDWNSYS", "⚠ arrêt / IPL système"),
        ]),
        ("IFS & réseau", "", 240, [
            ("§WRKLNK '/home/«u»'", "parcourir l'IFS"),
            ("§STRQSH", "shell Qshell"),
            ("CALL QP2TERM", "shell PASE (AIX)"),
            ("CPYTOSTMF  CPYFRMSTMF", "membre ↔ fichier IFS"),
            ("WRKAUT  CHGAUT", "droits IFS"),
            ("NETSTAT *CNN", "connexions TCP/IP"),
            ("CFGTCP", "configuration TCP/IP"),
            ("PING «hôte»", "tester la connexion"),
        ]),
        ("Développement", "", 240, [
            ("§CRTBNDRPG", "compiler un RPG ILE"),
            ("CRTSQLRPGI", "RPG avec SQL intégré"),
            ("CRTBNDCL", "compiler un CL"),
            ("STRDBG «pgm»", "déboguer"),
            ("DSPPGMREF «pgm»", "objets utilisés"),
        ]),
    ],
]

SQL = [
    [
        ("Lancer du SQL", "", 240, [
            ("§STRSQL", "SQL interactif (5250)"),
            ("RUNSQL SQL('«…»')", "une requête depuis CL"),
            ("RUNSQLSTM", "exécuter un script SQL"),
            ("§ACS › Run SQL Scripts", "client graphique"),
            ("SET SCHEMA «lib»", "schéma par défaut"),
            ("SET PATH «lib»", "chemin des fonctions"),
        ]),
        ("Requêtes Db2 for i", "", 250, [
            ("§SELECT * FROM «lib».«t»", "schéma = bibliothèque"),
            ("«lib»/«t»", "nommage *SYS"),
            ("§FETCH FIRST «n» ROWS ONLY", "n premières lignes"),
            ("LIMIT «n» OFFSET «m»", "pagination"),
            ("… WITH NC", "sans contrôle de valid."),
            ("VALUES CURRENT DATE", "évaluer une expression"),
            ("SYSIBM.SYSDUMMY1", "table « dual »"),
            ("RRN(«t»)", "n° relatif d'enreg."),
            ("CREATE OR REPLACE TABLE", "créer / remplacer"),
            ("MERGE INTO … USING", "insérer ou mettre à jour"),
            ("WITH «cte» AS (…)", "requête nommée (CTE)"),
        ]),
        ("Catalogue", "QSYS2", 230, [
            ("§SYSTABLES", "tables, vues, PF / LF"),
            ("SYSCOLUMNS", "colonnes"),
            ("SYSINDEXES", "index"),
            ("SYSVIEWS", "vues"),
            ("SYSREFCST", "clés étrangères"),
            ("SYSROUTINES", "procédures / fonctions"),
            ("SYSPARTITIONSTAT", "lignes, taille / membre"),
            ("TABLE_SCHEMA = '«LIB»'", "filtrer (en MAJUSCULES)"),
        ]),
        ("Fonctions utiles", "", 250, [
            ("VARCHAR_FORMAT(«d», «fmt»)", "date → texte"),
            ("TO_DATE(«s», «fmt»)", "texte → date"),
            ("DIGITS(«n»)", "nombre → texte (zéros)"),
            ("COALESCE(«a», «b»)", "1re valeur non nulle"),
            ("TRIM  RTRIM", "retirer les espaces"),
            ("LISTAGG(«c», ',')", "concaténer un groupe"),
            ("REGEXP_LIKE(«c», «rx»)", "tester une regex"),
            ("JSON_TABLE(…)", "lire du JSON"),
        ]),
    ],
    [
        ("Services : jobs", "QSYS2", 240, [
            ("§ACTIVE_JOB_INFO()", "≈ WRKACTJOB"),
            ("JOB_INFO()", "jobs, filtrables"),
            ("§JOBLOG_INFO('*')", "≈ DSPJOBLOG"),
            ("JOB_QUEUE_INFO", "≈ WRKJOBQ"),
            ("SUBSYSTEM_INFO", "≈ WRKSBS"),
            ("OUTPUT_QUEUE_ENTRIES", "≈ WRKOUTQ"),
            ("MESSAGE_QUEUE_INFO", "≈ DSPMSG"),
            ("HISTORY_LOG_INFO()", "≈ DSPLOG"),
            ("SCHEDULED_JOB_INFO", "≈ WRKJOBSCDE"),
            ("SPOOLED_FILE_INFO()", "≈ WRKSPLF"),
        ]),
        ("Services : système", "QSYS2", 240, [
            ("§SYSTEM_STATUS_INFO", "≈ WRKSYSSTS"),
            ("SYSDISKSTAT", "≈ WRKDSKSTS"),
            ("SYSTEM_VALUE_INFO", "≈ WRKSYSVAL"),
            ("PTF_INFO", "≈ DSPPTF"),
            ("GROUP_PTF_INFO", "≈ WRKPTFGRP"),
            ("ASP_INFO", "pools de disques (ASP)"),
            ("USER_STORAGE", "stockage par profil"),
            ("SOFTWARE_PRODUCT_INFO", "≈ DSPSFWRSC"),
            ("LICENSE_INFO", "licences"),
            ("§USER_INFO", "≈ WRKUSRPRF"),
            ("OBJECT_PRIVILEGES", "≈ DSPOBJAUT"),
            ("NETSTAT_INFO", "≈ NETSTAT *CNN"),
        ]),
        ("Services : objets & IFS", "QSYS2", 250, [
            ("§OBJECT_STATISTICS(«l»,«t»)", "≈ WRKOBJ"),
            ("LIBRARY_INFO(«lib»)", "taille d'une bibl."),
            ("LIBRARY_LIST_INFO", "≈ DSPLIBL"),
            ("RECORD_LOCK_INFO", "verrous d'enreg."),
            ("OBJECT_LOCK_INFO", "≈ WRKOBJLCK"),
            ("IFS_OBJECT_STATISTICS()", "parcourir l'IFS"),
            ("IFS_READ(«chemin»)", "lire un fichier IFS"),
        ]),
        ("CL depuis SQL", "", 250, [
            ("§CALL QCMDEXC('«cmd»')", "exécuter du CL"),
            ("TABLE(«fn»(…)) «x»", "fonction table"),
        ]),
    ],
]

# Couleurs d'un terminal 5250 : vert, turquoise, jaune
ACCENTS = {
    "aritim": "--a:#27ae60; --b:#3daee9; --param:#fdbc4b;",
    "dark":   "--a:#7ee2a2; --b:#6fd3e6; --param:#f3d36a;",
    "light":  "--a:#14713a; --b:#0a6678; --param:#8a5500;",
    "amoled": "--a:#5cc485; --b:#58b5c7; --param:#d6b35a;",
}

BRAND_CL = ('<h2><span class="prompt">===&gt;</span>AS/400<span class="cursor under"></span></h2>'
            '<small>IBM i 7.4 · CL · <i>paramètres</i> · <span class="warn">⚠</span> destructif · '
            '<span class="ess-key"></span>essentiel</small>')
BRAND_SQL = '<small>SQL · services « QSYS2. » omis</small><h2>DB2 for i</h2>'

if __name__ == "__main__":
    build_two_zones("as400", "AS/400 · IBM i 7.4", ACCENTS, BRAND_CL, BRAND_SQL, CL, SQL)
