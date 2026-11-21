"""Fond d'écran aide-mémoire Podman + virsh (libvirt / QEMU-KVM).

Modifier le contenu ci-dessous, puis :
    make html        -> génère build/html/podman-virsh-{aritim,dark,light,amoled}.html
    make             -> exporte aussi les PNG dans wallpapers/

Conventions (voir common.py) : "§cmd" essentiel, «x» paramètre, "⚠ desc" destructif,
"desc [badge]" badge de compatibilité.
Panneau : (titre, étiquette ou "", largeur colonne commande en px ou None, lignes)
Les préfixes « podman » et « virsh » sont omis.
"""
from common import build_two_zones

PODMAN = [
    [  # colonne 1
        ("Conteneurs", "podman run · ps", 250, [
            ("§run -it --rm «img» sh", "interactif, jetable"),
            ("§run -d --name «n» «img»", "en arrière-plan"),
            ("§run -p 8080:80 «img»", "publier un port"),
            ("run -v «dir»:/data:Z", "volume (SELinux :Z)"),
            ("run -e «VAR»=«v»", "variable d'env."),
            ("run --env-file .env", "fichier de variables"),
            ("§ps  ps -a", "actifs / tous"),
            ("§start  stop «c»", "démarrer / arrêter"),
            ("restart «c»", "redémarrer"),
            ("pause  unpause «c»", "geler / reprendre"),
            ("attach «c»", "s'attacher (Ctrl-p q)"),
            ("wait «c»", "attendre la fin"),
            ("rename «a» «b»", "renommer"),
            ("commit «c» «img»", "conteneur → image"),
            ("rm -f «c»", "⚠ supprimer de force"),
        ]),
        ("Options de run", "", 250, [
            ("--restart=always", "relancer si arrêt"),
            ("--replace", "écraser l'existant"),
            ("-m 512m  --cpus 1.5", "limiter RAM / CPU"),
            ("-w «dir»", "dossier de travail"),
            ("-u «uid»", "utilisateur"),
            ("--entrypoint «cmd»", "remplacer l'entrypoint"),
            ("§--userns=keep-id", "garder mon UID"),
            ("--read-only", "racine en lecture seule"),
            ("--cap-add «CAP»", "ajouter une capacité"),
            ("--init", "init (signaux, zombies)"),
            ("--pull=newer", "màj l'image si besoin"),
            ("--device /dev/«x»", "périphérique hôte"),
        ]),
        ("Images", "podman image", 250, [
            ("§images", "images locales"),
            ("§pull «img»:«tag»", "télécharger"),
            ("§build -t «img» .", "construire l'image"),
            ("build -f «fichier» .", "autre Containerfile"),
            ("build --no-cache", "sans cache"),
            ("tag «img» «reg»/«img»", "étiqueter"),
            ("push «reg»/«img»", "publier"),
            ("history «img»", "couches"),
            ("save -o «f».tar «img»", "exporter (load -i)"),
            ("rmi «img»", "⚠ supprimer l'image"),
        ]),
    ],
    [  # colonne 2
        ("Inspecter & déboguer", "", 250, [
            ("§logs -f «c»", "logs en direct"),
            ("logs --since 10m «c»", "10 dernières minutes"),
            ("logs --tail 50 «c»", "50 dernières lignes"),
            ("§exec -it «c» sh", "shell dans le conteneur"),
            ("inspect «c»", "détails JSON"),
            ("inspect -f '{{.«Champ»}}'", "un seul champ"),
            ("top «c»", "processus"),
            ("§stats", "CPU / RAM en direct"),
            ("port «c»", "ports publiés"),
            ("diff «c»", "fichiers modifiés"),
            ("cp «c»:«src» «dst»", "copier vers l'hôte"),
            ("events", "flux d'événements"),
            ("healthcheck run «c»", "lancer le healthcheck"),
        ]),
        ("Containerfile", "", 250, [
            ("FROM «img»:«tag»", "image de base"),
            ("RUN «cmd»", "commande (1 couche)"),
            ("COPY «src» «dst»", "copier dans l'image"),
            ("WORKDIR «dir»", "dossier courant"),
            ("ENV «VAR»=«v»", "variable d'env."),
            ("ARG «nom»", "--build-arg nom=…"),
            ("EXPOSE «port»", "port documenté"),
            ("USER «uid»", "ne pas tourner en root"),
            ('§ENTRYPOINT ["«bin»"]', "programme lancé"),
            ('CMD ["«arg»"]', "arguments par défaut"),
        ]),
        ("Kubernetes & Compose", "", 250, [
            ("§kube generate «p» > p.yaml", "pod → YAML"),
            ("§kube play «f».yaml", "lancer depuis YAML"),
            ("kube down «f».yaml", "arrêter et supprimer"),
            ("compose up -d", "fichier compose"),
            ("compose down", "arrêter"),
            ("compose logs -f", "logs des services"),
        ]),
        ("Ménage & système", "", 250, [
            ("§system df", "espace utilisé"),
            ("system df -v", "détail par objet"),
            ("info", "config, rootless"),
            ("container prune", "⚠ suppr. les arrêtés"),
            ("image prune -a", "⚠ suppr. inutilisées"),
            ("system prune -a", "⚠ tout nettoyer"),
            ("system reset", "⚠ remise à zéro totale"),
        ]),
    ],
    [  # colonne 3
        ("Pods", "podman pod", 250, [
            ("§pod create -n «p» -p «port»", "créer (ports au pod)"),
            ("§run -d --pod «p» «img»", "ajouter un conteneur"),
            ("pod ps", "lister les pods"),
            ("pod start  stop «p»", "démarrer / arrêter"),
            ("pod logs -f «p»", "logs de tout le pod"),
            ("pod stats «p»", "ressources"),
            ("pod top «p»", "processus du pod"),
            ("pod inspect «p»", "détails"),
            ("pod rm -f «p»", "⚠ pod + conteneurs"),
        ]),
        ("Volumes, réseaux, secrets", "", 250, [
            ("volume ls", "volumes"),
            ("volume create «v»", "créer"),
            ("volume inspect «v»", "point de montage"),
            ("volume prune", "⚠ suppr. inutilisés"),
            ("network ls", "réseaux"),
            ("§network create «net»", "créer un réseau"),
            ("network inspect «net»", "sous-réseau, gw"),
            ("§run --network «net»", "rattacher (DNS)"),
            ("network connect «net» «c»", "brancher un conteneur"),
            ("secret create «s» «f»", "créer un secret"),
            ("secret ls", "lister les secrets"),
            ("run --secret «s»", "dans /run/secrets"),
            ("unshare «cmd»", "namespace rootless"),
        ]),
        ("Quadlet & systemd", "systemctl --user", 250, [
            ("«nom».container", "unité Quadlet"),
            (".pod  .volume  .network", "autres types"),
            ("…/containers/systemd/", "dossier (~/.config)"),
            ("Image=  PublishPort=", "clés de Container"),
            ("WantedBy=default.target", "démarrage auto"),
            ("§daemon-reload", "générer les services"),
            ("§start  status «nom»", "démarrer / état"),
            ("journalctl --user -u «n»", "logs du service"),
            ("loginctl enable-linger", "survivre à la déco."),
            ("podman auto-update", "MàJ des images"),
        ]),
        ("Registres", "", 250, [
            ("search «nom»", "chercher une image"),
            ("login  logout «reg»", "s'authentifier"),
            ("pull docker.io/«img»", "nom complet"),
            ("registries.conf", "registres de recherche"),
        ]),
    ],
]

VIRSH = [
    [
        ("Machines virtuelles", "virsh", 230, [
            ("§list --all", "toutes les VM"),
            ("§start «vm»", "démarrer"),
            ("§shutdown «vm»", "arrêt propre (ACPI)"),
            ("reboot «vm»", "redémarrer"),
            ("destroy «vm»", "⚠ couper le courant"),
            ("suspend  resume «vm»", "pause / reprise"),
            ("autostart «vm»", "démarrer avec l'hôte"),
            ("autostart --disable «vm»", "… ne plus démarrer"),
            ("§console «vm»", "console série (Ctrl-])"),
            ("managedsave «vm»", "suspendre sur disque"),
            ("domrename «a» «b»", "renommer"),
            ("undefine «vm»", "⚠ supprimer la définition"),
        ]),
        ("Inspecter", "", 230, [
            ("§dominfo «vm»", "état, CPU, mémoire"),
            ("§domifaddr «vm»", "adresse IP"),
            ("domstate «vm»", "état"),
            ("domblklist «vm»", "disques"),
            ("domiflist «vm»", "interfaces réseau"),
            ("vncdisplay «vm»", "port VNC"),
            ("domdisplay «vm»", "URI VNC / Spice"),
            ("dommemstat «vm»", "mémoire de l'invité"),
            ("domstats «vm»", "statistiques"),
            ("dumpxml «vm»", "définition XML"),
        ]),
        ("Configuration", "", 230, [
            ("§edit «vm»", "modifier le XML"),
            ("define «f».xml", "créer / màj depuis XML"),
            ("create «f».xml", "lancer sans définir"),
            ("setvcpus «vm» «n»", "vCPU (+ --config)"),
            ("setmem «vm» «2G»", "mémoire (≤ max)"),
            ("setmaxmem «vm» «4G»", "mémoire max"),
            ("attach-disk «vm» «f» vdb", "ajouter un disque"),
            ("detach-disk «vm» vdb", "retirer un disque"),
            ("change-media «vm» «dev»", "changer d'ISO"),
        ]),
        ("Instantanés", "", 280, [
            ("§snapshot-create-as «vm» «s»", "créer"),
            ("snapshot-list «vm»", "lister"),
            ("§snapshot-revert «vm» «s»", "revenir à s"),
            ("snapshot-current «vm»", "instantané courant"),
            ("snapshot-delete «vm» «s»", "⚠ supprimer"),
        ]),
    ],
    [
        ("Stockage", "", 260, [
            ("§pool-list --all", "pools de stockage"),
            ("§vol-list «pool»", "volumes du pool"),
            ("vol-path «v» --pool «p»", "chemin du fichier"),
            ("vol-create-as «p» «v» 20G", "créer un volume"),
            ("vol-resize «v» 30G --pool «p»", "agrandir"),
            ("vol-delete «v» --pool «p»", "⚠ supprimer"),
            ("pool-refresh «pool»", "rescanner"),
            ("pool-start «pool»", "démarrer un pool"),
            ("qemu-img info «f».qcow2", "infos disque"),
            ("qemu-img resize «f» +10G", "agrandir un fichier"),
        ]),
        ("Réseau", "", 260, [
            ("§net-list --all", "réseaux virtuels"),
            ("net-start default", "démarrer le NAT"),
            ("net-autostart default", "… au démarrage"),
            ("net-info «net»", "état, pont"),
            ("§net-dhcp-leases default", "IP des VM (DHCP)"),
            ("net-edit «net»", "modifier le XML"),
            ("net-destroy «net»", "arrêter le réseau"),
        ]),
        ("Connexion & migration", "", 260, [
            ("-c qemu:///system", "VM système"),
            ("-c qemu:///session", "VM de l'utilisateur"),
            ("-c qemu+ssh://«h»/system", "hôte distant"),
            ("§uri", "connexion courante"),
            ("migrate --live «vm» «uri»", "migration à chaud"),
        ]),
        ("Hôte", "", 260, [
            ("version", "libvirt / QEMU"),
            ("hostname", "nom de l'hôte"),
            ("§nodeinfo", "CPU / RAM de l'hôte"),
            ("nodememstats", "mémoire détaillée"),
            ("capabilities", "capacités (XML)"),
        ]),
        ("Outils virt-*", "", 260, [
            ("§virt-install …", "créer une VM"),
            ("osinfo-query os", "valeurs de --osinfo"),
            ("virt-clone -o «vm» …", "cloner une VM"),
            ("virt-viewer «vm»", "afficher l'écran"),
            ("virt-manager", "interface graphique"),
        ]),
    ],
]

# Podman en violet, libvirt en cyan, paramètres en jaune
ACCENTS = {
    "aritim": "--a:#b27cd6; --b:#3daee9; --param:#fdbc4b;",
    "dark":   "--a:#c49bff; --b:#6fd3e6; --param:#f3d36a;",
    "light":  "--a:#6a3fb5; --b:#0a6678; --param:#8a5500;",
    "amoled": "--a:#a98fe6; --b:#58b5c7; --param:#d6b35a;",
}

# Un pod : trois conteneurs dans une enveloppe commune
POD_SVG = """<svg class="graph" viewBox="0 0 120 48" aria-hidden="true">
  <rect x="4" y="4" width="112" height="40" rx="12" fill="none" stroke="var(--a)" stroke-width="3" stroke-dasharray="7 5"/>
  <rect x="16" y="14" width="22" height="20" rx="4" fill="var(--a)"/>
  <rect x="49" y="14" width="22" height="20" rx="4" fill="var(--a)"/>
  <rect x="82" y="14" width="22" height="20" rx="4" fill="var(--param)"/>
</svg>"""

BRAND_PODMAN = ("<h2>PODMAN</h2>" + POD_SVG +
                '<small>préfixe « podman » omis · <i>paramètres</i> · <span class="warn">⚠</span> destructif · '
                '<span class="ess-key"></span>essentiel</small>')
BRAND_VIRSH = ('<small>« virsh » omis · QEMU/KVM</small>'
               '<h2><span class="prompt">virsh #</span>LIBVIRT</h2>')

if __name__ == "__main__":
    build_two_zones("podman-virsh", "Podman · virsh", ACCENTS, BRAND_PODMAN, BRAND_VIRSH, PODMAN, VIRSH)
