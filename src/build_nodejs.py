"""Fond d'écran aide-mémoire Node.js : JavaScript + API Node, et npm / CLI node.

Modifier le contenu ci-dessous, puis :
    make html        -> génère build/html/nodejs-{aritim,dark,light,amoled}.html
    make             -> exporte aussi les PNG dans wallpapers/

Conventions (voir common.py) : "§cmd" essentiel, «x» paramètre, "⚠ desc" destructif,
"desc [badge]" badge de compatibilité.
Panneau : (titre, étiquette ou "", largeur colonne commande en px ou None, lignes)
"""
from common import build_two_zones

JAVASCRIPT = [
    [  # colonne 1
        ("Variables & types", "", 230, [
            ("§const  let", "constante / variable"),
            ("number  bigint (10n)", "numériques"),
            ("string  boolean", "texte / booléen"),
            ("null  undefined", "vide / non défini"),
            ("typeof «x»", "type"),
            ("Array.isArray(«x»)", "tableau ?"),
            ("§«a» ?? «b»", "défaut si null/undef."),
            ("§«o»?.«p»?.«q»", "chaînage optionnel"),
            ("§«a» === «b»", "égalité stricte"),
            ("Number(«s»)  String(«n»)", "convertir"),
            ("parseInt(«s», 10)", "texte → entier"),
        ]),
        ("Chaînes", "", 230, [
            ("§`${«x»} …`", "gabarit (template)"),
            ("«s».split(«sep»)", "découper"),
            ("«a».join(«sep»)", "assembler"),
            ("«s».trim()", "espaces aux bords"),
            ("«s».includes(«x»)", "contient"),
            ("«s».replaceAll(«a», «b»)", "remplacer tout"),
            ('«s».padStart(«n», "0")', "compléter à gauche"),
            ("«s».slice(«a», «b»)", "sous-chaîne"),
            ("«s».match(/«rx»/g)", "regex"),
        ]),
        ("Objets", "", 230, [
            ("§const { «a», «b» } = «o»", "déstructurer"),
            ("§{ ...«o», «k»: «v» }", "copier + modifier"),
            ("Object.keys(«o»)", "clés"),
            ("Object.entries(«o»)", "paires clé / valeur"),
            ("structuredClone(«o»)", "copie profonde"),
            ("JSON.parse  .stringify", "JSON ↔ objet"),
        ]),
        ("Map, Set & divers", "", 230, [
            ("new Map()  new Set()", "dictionnaire / ensemble"),
            ("«m».set(«k», «v»)", "ajouter"),
            ("«m».get(«k»)  .has(«k»)", "lire / tester"),
            ("[...new Set(«a»)]", "dédoublonner"),
            ("new Date().toJSON()", "date ISO"),
            ("Math.round  .floor", "arrondis"),
            ("«n».toFixed(2)", "2 décimales"),
            ("crypto.randomUUID()", "UUID"),
            ("Intl.NumberFormat", "formats localisés"),
        ]),
    ],
    [  # colonne 2
        ("Tableaux", "", 250, [
            ("§«a».map(x => …)", "transformer"),
            ("§«a».filter(x => …)", "filtrer"),
            ("«a».reduce((s, x) => …, 0)", "accumuler"),
            ("«a».find(x => …)", "premier trouvé"),
            ("«a».some(…)  «a».every(…)", "un / tous"),
            ("«a».includes(«x»)", "contient"),
            ("«a».flat()  .flatMap()", "aplatir"),
            ("«a».toSorted(«cmp»)", "trier (copie)"),
            ("«a».at(-1)", "dernier"),
            ("«a».push(«x»)  .pop()", "ajouter / retirer (fin)"),
            ("«a».indexOf(«x»)", "position"),
            ("«a».toSpliced(«i», 1)", "retirer (copie)"),
            ("[...«a», «x»]", "copier + ajouter"),
            ("Array.from(«it»)", "itérable → tableau"),
            ("Object.groupBy(«a», «f»)", "regrouper"),
        ]),
        ("Fonctions & classes", "", 250, [
            ("§const f = (x) => …", "fonction fléchée"),
            ("function f(«a» = 1)", "valeur par défaut"),
            ("(...args) => …", "paramètres restants"),
            ("class «C» extends «B»", "héritage"),
            ("#privé  static", "privé / statique"),
            ("get «p»()  set «p»(v)", "accesseurs"),
            ("function* gen()", "générateur"),
            ("«f».bind(«obj»)", "fixer this"),
            ("«x» instanceof «C»", "test de classe"),
        ]),
        ("Asynchrone", "", 250, [
            ("§async function f()", "fonction async"),
            ("§await «promesse»", "attendre"),
            ("try { await … } catch", "gérer l'erreur"),
            ("Promise.all([…])", "en parallèle"),
            ("Promise.allSettled([…])", "tous, même en échec"),
            ("Promise.race([…])", "le premier"),
            ("new Promise(…)", "créer une promesse"),
            (".then(…).catch(…)", "chaîner"),
            ("setInterval(«f», «ms»)", "répéter"),
            ("setTimeout(«f», «ms»)", "différer"),
            ("for await (… of «it»)", "itération async"),
            ("AbortController", "annuler (fetch…)"),
        ]),
    ],
    [  # colonne 3
        ("Modules", "", 250, [
            ('§import «x» from "«m»"', "import ESM"),
            ('import { «a» } from "«m»"', "import nommé"),
            ("export default  export", "exporter"),
            ('await import("«m»")', "import dynamique"),
            ('require("«m»")', "CommonJS"),
            ('"type": "module"', "ESM (package.json)"),
            ("import.meta.dirname", "dossier du fichier"),
        ]),
        ("Fichiers & chemins", "node:fs/promises", 250, [
            ('§readFile(«f», "utf8")', "lire un fichier"),
            ("writeFile(«f», «data»)", "écrire"),
            ("readdir(«dir»)", "lister"),
            ("rm  mkdir  stat", "suppr. / créer / infos"),
            ("§path.join(«a», «b»)", "joindre (node:path)"),
            ("path.resolve(«p»)", "chemin absolu"),
            ("path.extname(«f»)", "extension"),
            ("createReadStream(«f»)", "lire en flux"),
            ("existsSync(«f»)", "existe ? (node:fs)"),
        ]),
        ("Process & réseau", "", 250, [
            ("process.argv", "arguments"),
            ("§process.env.«VAR»", "variable d'env."),
            ("process.exit(«code»)", "quitter"),
            ("process.cwd()", "dossier courant"),
            ("§await fetch(«url»)", "requête HTTP"),
            ("await «res».json()", "lire le JSON"),
            ("http.createServer(…)", "serveur HTTP"),
            ("execFile(«cmd», [«args»])", "lancer une commande"),
            ("«ee».on(«evt», «f»)", "écouter un événement"),
            ('process.on("SIGINT", …)', "intercepter Ctrl-C"),
            ("os.cpus()  os.homedir()", "infos (node:os)"),
        ]),
        ("Console & débogage", "", 250, [
            ("console.table(«a»)", "afficher en tableau"),
            ('console.time("t")', "chronométrer"),
            ("console.error(…)", "vers stderr"),
            ("debugger", "point d'arrêt"),
            ("util.inspect(«o»)", "objet détaillé"),
            ("console.trace()", "pile d'appels"),
        ]),
    ],
]

NPM = [
    [
        ("CLI node", "", 250, [
            ("§node «f».js", "exécuter"),
            ("§node --watch «f».js", "relancer si modifié"),
            ("node --env-file=.env «f»", "charger .env"),
            ("node --test", "lanceur de tests"),
            ("node --inspect «f».js", "déboguer (DevTools)"),
            ('node -e "«code»"', "exécuter une ligne"),
            ('node -p "«expr»"', "afficher le résultat"),
            ("node --run «script»", "script npm, rapide"),
            ("node --check «f».js", "vérifier la syntaxe"),
            ("NODE_OPTIONS=«…»", "options par l'env."),
        ]),
        ("npm", "", 250, [
            ("§npm init -y", "nouveau package.json"),
            ("§npm install", "installer (lockfile)"),
            ("npm ci", "install. propre (CI)"),
            ("§npm i «pkg»", "ajouter une dép."),
            ("npm i -D «pkg»", "dépendance de dev"),
            ("npm i -g «pkg»", "installation globale"),
            ("npm uninstall «pkg»", "retirer"),
            ("npm update", "mettre à jour"),
            ("npm outdated", "versions dépassées"),
            ("npm ls «pkg»", "qui dépend de pkg"),
            ("npm view «pkg» versions", "versions publiées"),
            ("npm i «pkg»@«ver»", "version précise"),
            ("npm cache clean --force", "vider le cache"),
            ("npm audit fix", "corriger les failles"),
        ]),
        ("Scripts & npx", "", 250, [
            ("§npm run «script»", "lancer un script"),
            ("npm test  npm start", "raccourcis"),
            ("§npx «outil»", "sans installer"),
            ("npm run «s» -- «args»", "passer des arguments"),
            ("npm pkg set «k»=«v»", "éditer package.json"),
            ('"pre«script»"  "post…"', "hooks de script"),
        ]),
        ("TypeScript", "", 250, [
            ("npm i -D typescript", "installer"),
            ("npx tsc --init", "créer tsconfig.json"),
            ("§npx tsc --noEmit", "vérifier les types"),
            ("npx tsx «f».ts", "exécuter du TS"),
        ]),
    ],
    [
        ("package.json", "", 250, [
            ('"scripts": { … }', "commandes"),
            ('"dependencies"', "dépendances"),
            ('"devDependencies"', "outils de dev"),
            ('"^1.2.3"  "~1.2.3"', "mineure / patch"),
            ('"engines": { "node" }', "version de Node"),
            ('"main"  "exports"', "point d'entrée"),
            ('"bin"', "commandes CLI"),
            ('"private": true', "jamais publié"),
            ('"overrides"', "forcer une sous-dép."),
        ]),
        ("Tests intégrés", "node:test", 250, [
            ('§test("…", () => { … })', "un test"),
            ("describe  it", "regrouper"),
            ("§assert.equal(«a», «b»)", "égalité (strict)"),
            ("assert.deepEqual(«a», «b»)", "objets"),
            ("assert.throws(«f»)", "exception attendue"),
            ("node --test --watch", "en continu"),
            ("t.mock.fn()", "espion / mock"),
            ("test.only  test.skip", "seul / ignoré"),
        ]),
        ("Versions de Node", "", 250, [
            ("nvm install --lts", "dernière LTS"),
            ("nvm use «v»", "changer de version"),
            (".nvmrc", "version du projet"),
            ("corepack enable", "pnpm / yarn"),
        ]),
        ("Outils courants", "npx", 250, [
            ("npx eslint .", "linter"),
            ("npx prettier -w .", "formater"),
            ("npx vitest", "tests (Vitest)"),
            ("npm create vite@latest", "nouveau projet front"),
            ("npx serve .", "serveur statique"),
            ("npx npm-check-updates", "màj majeures (ncu)"),
        ]),
        ("Publier", "", 250, [
            ("npm login", "s'authentifier"),
            ("npm version patch", "incrémenter + tag"),
            ("npm pack --dry-run", "contenu publié"),
            ("npm publish", "publier"),
            ("npm unpublish «pkg»@«v»", "⚠ dépublier"),
        ]),
    ],
]

# Vert Node, violet pour npm, paramètres en jaune
ACCENTS = {
    "aritim": "--a:#27ae60; --b:#b27cd6; --param:#fdbc4b;",
    "dark":   "--a:#7ee2a2; --b:#c49bff; --param:#f3d36a;",
    "light":  "--a:#14713a; --b:#6a3fb5; --param:#8a5500;",
    "amoled": "--a:#5cc485; --b:#a98fe6; --param:#d6b35a;",
}

BRAND_LANG = ('<h2><span class="prompt">&gt;</span>NODE.JS<span class="cursor under"></span></h2>'
              '<small>Node 22 · ESM · <i>paramètres</i> · <span class="warn">⚠</span> destructif · '
              '<span class="ess-key"></span>essentiel</small>')
BRAND_NPM = ('<small>npm · npx · node --test</small>'
             '<h2><span class="prompt">$</span>NPM</h2>')

if __name__ == "__main__":
    build_two_zones("nodejs", "Node.js", ACCENTS, BRAND_LANG, BRAND_NPM, JAVASCRIPT, NPM)
