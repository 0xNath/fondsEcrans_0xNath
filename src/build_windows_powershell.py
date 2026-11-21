"""Fond d'écran aide-mémoire PowerShell + Windows.

Modifier le contenu ci-dessous, puis :
    make html        -> génère build/html/windows-powershell-{aritim,dark,light,amoled}.html
    make             -> exporte aussi les PNG dans wallpapers/

Conventions (voir common.py) : "§cmd" essentiel, «x» paramètre, "⚠ desc" destructif,
"desc [PS7]" badge de compatibilité.
Panneau : (titre, étiquette ou "", largeur colonne commande en px ou None, lignes)
"""
from common import build_two_zones

POWERSHELL = [
    [  # colonne 1
        ("Aide & découverte", "Get-Help", 250, [
            ("§Get-Help «cmd» -Examples", "exemples d'usage"),
            ("Get-Help «cmd» -Online", "doc en ligne"),
            ("§Get-Command *«mot»*", "trouver une commande"),
            ("Get-Command -Noun «nom»", "par nom (Noun)"),
            ("Get-Command «cmd» -Syntax", "syntaxe"),
            ("§«obj» | Get-Member", "propriétés / méthodes"),
            ("Get-Alias «alias»", "cmdlet derrière l'alias"),
            ("Get-Verb", "verbes approuvés"),
            ("Update-Help", "mettre à jour l'aide"),
            ("$PSVersionTable", "version de PowerShell"),
        ]),
        ("Fichiers", "FileSystem", 250, [
            ("§ls  gci -Force", "lister (+ cachés)"),
            ("gci -r -fi *.«ext»", "recherche récursive"),
            ("§cd «dir»", "changer de dossier"),
            ("pwd", "dossier courant"),
            ("cd -", "dossier préc. [PS7]"),
            ("ni «f»  mkdir «dir»", "créer fichier / dossier"),
            ("§cp «src» «dst» -r", "copier récursivement"),
            ("mv «a» «b»", "déplacer / renommer"),
            ("rm «dir» -r -Force", "⚠ suppr. sans retour"),
            ("§gc «f» -Tail 20 -Wait", "suivre (≈ tail -f)"),
            ("Test-Path «chemin»", "existe ?"),
            ("Resolve-Path «rel»", "chemin absolu"),
            ("ii .", "ouvrir l'Explorateur ici"),
        ]),
        ("Pipeline & objets", "", 250, [
            ("§? «Prop» -eq «v»", "filtrer (Where-Object)"),
            ("§select «P1»,«P2»", "garder des propriétés"),
            ("select -First «n»", "n premiers"),
            ("select «P» -Unique", "dédoublonner"),
            ("§sort «Prop» -Desc", "trier (décroissant)"),
            ("group «Prop»", "regrouper / compter"),
            ("measure «Prop» -Sum", "somme, moyenne…"),
            ("% { $_.«Prop» }", "pour chaque (ForEach)"),
            ("$_  $PSItem", "objet courant"),
            ("ft -AutoSize  fl *", "tableau / liste"),
            ("Out-GridView", "grille interactive"),
            ("§-WhatIf  -Confirm", "simuler / confirmer"),
        ]),
    ],
    [  # colonne 2
        ("Texte & recherche", "", 250, [
            ("§sls «motif» «f»", "grep (Select-String)"),
            ("gci -r | sls «motif»", "grep récursif"),
            ("sls «motif» -NotMatch", "lignes sans le motif"),
            ("sls «motif» -Context 2", "avec lignes autour"),
            ("§«s» -match «regex»", "tester → $Matches"),
            ("«s» -replace «a»,«b»", "remplacer (regex)"),
            ("«s» -split «sep»", "découper"),
            ("«s» -like «*x*»", "joker (* ?)"),
            ("«s».Trim()  .ToUpper()", "méthodes .NET"),
            ('"total : $(«expr»)"', "interpolation"),
            ("'{0:N2}' -f «n»", "formater un nombre"),
        ]),
        ("Import / export", "", 250, [
            ("§Import-Csv «f»", "CSV → objets"),
            ("Export-Csv «f» -NoType", "objets → CSV"),
            ("ConvertTo-Json -Depth 5", "objets → JSON"),
            ("ConvertFrom-Json", "JSON → objets"),
            ("gc «f» -Raw", "fichier en une chaîne"),
            ("Out-File «f» -Append", "écrire / ajouter"),
            ("§irm «url»", "API REST → objets"),
            ("iwr «url» -OutFile «f»", "télécharger"),
            ("Get-Clipboard  scb", "lire / écrire presse-pap."),
            ("Compress-Archive", "créer un zip"),
            ("Expand-Archive «f»", "extraire un zip"),
        ]),
        ("Variables & types", "", 240, [
            ("§$x = 1, 2, 3", "tableau"),
            ("$h = @{ a = 1 }", "table de hachage"),
            ("[pscustomobject]@{…}", "objet personnalisé"),
            ("$x.Count  $x[-1]", "taille / dernier"),
            ("[int]«s»  «x».GetType()", "convertir / type"),
            ("$null  $true  $false", "constantes"),
            ("§$env:PATH", "variable d'env."),
            ("$?  $LASTEXITCODE", "succès / code retour"),
            ("$PROFILE", "script de démarrage"),
            ("§$Error[0]", "dernière erreur"),
            ("Get-Date -f yyyy-MM-dd", "formater la date"),
            ("[datetime]::Now", "date et heure"),
        ]),
    ],
    [  # colonne 3
        ("Scripts & contrôle", "", 250, [
            ("if («a» -eq «b») {…}", "-ne -gt -lt -like"),
            ("foreach ($i in $x) {…}", "boucle"),
            ("while («cond») {…}", "boucle conditionnelle"),
            ("param([string]$Nom)", "paramètres du script"),
            ("1..10", "plage de nombres"),
            ("switch -Regex («s») {…}", "aiguillage"),
            ("function F($a) {…}", "définir une fonction"),
            ("§try {…} catch { $_ }", "gérer une erreur"),
            ("-ErrorAction Stop", "erreur bloquante"),
            ("§.\\script.ps1", "lancer un script"),
            (". .\\lib.ps1", "charger (dot-sourcing)"),
            ("Set-ExecutionPolicy «p»", "autoriser les scripts"),
        ]),
        ("Modules & paquets", "", 250, [
            ("Find-Module «nom»", "chercher (PSGallery)"),
            ("§Install-Module «nom»", "installer un module"),
            ("Get-Module -ListAvail", "modules installés"),
            ("Import-Module «nom»", "charger un module"),
            ("§winget search «app»", "chercher une appli"),
            ("§winget install «id»", "installer une appli"),
            ("winget upgrade --all", "tout mettre à jour"),
            ("winget list", "applis installées"),
        ]),
        ("Jobs & à distance", "", 250, [
            ("Start-Job { … }", "tâche de fond"),
            ("Get-Job  Receive-Job", "état / résultat"),
            ("Stop-Job  Remove-Job", "arrêter / supprimer"),
            ("«cmd» &", "arrière-plan [PS7]"),
            ("§Enter-PSSession «pc»", "session distante"),
            ("icm «pc» { … }", "exécuter à distance"),
            ("ssh «u»@«hôte»", "OpenSSH intégré"),
        ]),
        ("Console", "PSReadLine", 200, [
            ("§Tab  Ctrl-Espace", "compléter / menu"),
            ("§Ctrl-r", "chercher dans l'historique"),
            ("F7  h", "historique (Get-History)"),
            ("Ctrl-c", "interrompre"),
            ("Ctrl-← →", "mot préc. / suivant"),
            ("cls", "effacer l'écran"),
        ]),
    ],
]

WINDOWS = [
    [
        ("Système", "cmd", 240, [
            ("§winver  systeminfo", "version / infos"),
            ("msinfo32", "infos détaillées"),
            ("hostname  whoami", "machine / utilisateur"),
            ("§tasklist | findstr «n»", "trouver un processus"),
            ("taskkill /F /IM «x».exe", "⚠ tuer un processus"),
            ("§sfc /scannow", "réparer les fich. système"),
            ("dism … /RestoreHealth", "réparer l'image Windows"),
            ("chkdsk C: /f", "vérifier le disque"),
            ("shutdown /r /t 0", "redémarrer maintenant"),
            ("shutdown /s /t 0", "éteindre"),
            ("gpupdate /force", "appliquer les GPO"),
            ("powercfg /batteryreport", "rapport de batterie"),
        ]),
        ("Fichiers", "cmd", 240, [
            ("dir /a /s", "tout, récursivement"),
            ("§cd /d «D:\\dir»", "lecteur + dossier"),
            ("copy  move  ren", "copier / dépl. / renommer"),
            ("del /f /q «f»", "⚠ supprimer un fichier"),
            ("rd /s /q «dir»", "⚠ supprimer un dossier"),
            ("§robocopy «src» «dst» /E", "copie récursive robuste"),
            ("robocopy … /MIR", "⚠ miroir (supprime)"),
            ("§where «cmd»", "trouver un exécutable"),
            ("type «f»", "afficher un fichier"),
            ("tree /f", "arborescence"),
            ("findstr /sin «m» *.txt", "grep (findstr)"),
            ("attrib -h «f»", "attributs (caché…)"),
            ("mklink /d «lien» «cible»", "lien symbolique"),
        ]),
        ("Réseau", "", 240, [
            ("§ipconfig /all", "configuration IP"),
            ("ipconfig /flushdns", "vider le cache DNS"),
            ("ping  tracert «hôte»", "tester / chemin"),
            ("nslookup «domaine»", "résolution DNS"),
            ("§netstat -ano", "ports + PID"),
            ("arp -a  route print", "tables ARP / routage"),
            ("tnc «hôte» -Port «p»", "tester un port (PS)"),
            ("curl.exe -I «url»", "curl intégré"),
            ("net use Z: «\\\\srv\\part»", "monter un partage"),
        ]),
    ],
    [
        ("Outils", "Win+R", 200, [
            ("§taskmgr", "gestionnaire des tâches"),
            ("services.msc", "services"),
            ("§eventvwr.msc", "observateur d'événements"),
            ("devmgmt.msc", "périphériques"),
            ("diskmgmt.msc", "gestion des disques"),
            ("compmgmt.msc", "gestion de l'ordinateur"),
            ("regedit", "registre"),
            ("control", "panneau de configuration"),
            ("perfmon", "analyseur de perfs"),
            ("gpedit.msc", "stratégies locales"),
            ("appwiz.cpl", "programmes installés"),
            ("ncpa.cpl", "cartes réseau"),
            ("resmon", "moniteur de ressources"),
            ("%appdata%  %temp%", "dossiers utiles"),
        ]),
        ("Raccourcis", "clavier", 200, [
            ("§Win+E", "Explorateur"),
            ("Win+I", "Paramètres"),
            ("§Win+X", "menu avancé (Terminal)"),
            ("Win+V", "historique presse-papiers"),
            ("§Win+Shift+S", "capture d'écran"),
            ("Win+.", "émojis et symboles"),
            ("Win+← →", "ancrer la fenêtre"),
            ("Win+Ctrl+D", "nouveau bureau virtuel"),
            ("Win+Ctrl+← →", "changer de bureau"),
            ("Alt+Tab  Win+Tab", "fenêtres / vue tâches"),
            ("Ctrl+Shift+Échap", "gestionnaire des tâches"),
            ("Win+L", "verrouiller"),
        ]),
        ("Services & WSL", "", 240, [
            ("sc query «svc»", "état d'un service"),
            ("net start «svc»", "démarrer (stop : arrêter)"),
            ("§Get-Service «nom»", "état (PS)"),
            ("Restart-Service «nom»", "redémarrer (PS)"),
            ("schtasks /query", "tâches planifiées"),
            ("§wsl", "ouvrir Linux (WSL)"),
            ("wsl -l -v", "distributions WSL"),
            ("wsl --shutdown", "arrêter toutes les VM"),
        ]),
    ],
]

ACCENTS = {
    "aritim": "--a:#3daee9; --b:#fdbc4b; --param:#b28ce0;",
    "dark":   "--a:#6cb2ff; --b:#f3d36a; --param:#c6a8ff;",
    "light":  "--a:#0b5cad; --b:#7a5a00; --param:#6a3fb5;",
    "amoled": "--a:#5b9ae0; --b:#cdb35a; --param:#a98fe6;",
}

BRAND_PS = ('<h2><span class="prompt">PS&gt;</span>POWERSHELL<span class="cursor under"></span></h2>'
            '<small>alias courts · <i>paramètres</i> · <span class="warn">⚠</span> destructif · '
            '<span class="ess-key"></span>essentiel</small>')
BRAND_WIN = ('<small>cmd · outils · raccourcis</small>'
             '<h2><span class="prompt">C:\\&gt;</span>WINDOWS</h2>')

if __name__ == "__main__":
    build_two_zones("windows-powershell", "PowerShell · Windows", ACCENTS, BRAND_PS, BRAND_WIN,
                    POWERSHELL, WINDOWS)
