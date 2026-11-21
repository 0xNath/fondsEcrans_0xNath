"""Fond d'écran aide-mémoire Rust : langage + Cargo / rustup.

Modifier le contenu ci-dessous, puis :
    make html        -> génère build/html/rust-{aritim,dark,light,amoled}.html
    make             -> exporte aussi les PNG dans wallpapers/

Conventions (voir common.py) : "§cmd" essentiel, «x» paramètre, "⚠ desc" destructif,
"desc [badge]" badge de compatibilité.
Panneau : (titre, étiquette ou "", largeur colonne commande en px ou None, lignes)
"""
from common import build_two_zones

LANGAGE = [
    [  # colonne 1
        ("Variables & types", "", 230, [
            ("§let x = 5;", "immuable"),
            ("§let mut x = 5;", "mutable"),
            ("let x = x + 1;", "masquage (shadowing)"),
            ("const MAX: u32 = 10;", "constante"),
            ("i32  u64  f64  usize", "numériques"),
            ("u8::MAX  i32::MIN", "bornes"),
            ("bool  char  &str", "primitifs"),
            ("§String  Vec<T>", "possédés (sur le tas)"),
            ("[i32; 3]  (a, b)", "tableau / tuple"),
            ("§Option<T>", "Some(x) / None"),
            ("§Result<T, E>", "Ok(x) / Err(e)"),
            ("«x» as u64", "conversion simple"),
            ("«x».into()  T::from(«x»)", "conversion (From)"),
            ("«s».parse::<i32>()", "texte → nombre"),
        ]),
        ("Propriété & emprunts", "", 230, [
            ("§&«x»", "emprunt partagé"),
            ("§&mut «x»", "emprunt exclusif"),
            ("«x».clone()", "copie profonde"),
            ("Copy  Clone", "copie impl. / expl."),
            ("drop(«x»)", "libérer maintenant"),
            ("&«v»[..]", "tranche d'un Vec"),
            ("move || …", "closure propriétaire"),
            ("fn f<'a>(«x»: &'a T)", "durée de vie"),
            ("Box<T>", "valeur sur le tas"),
            ("Rc<T>  Arc<T>", "partage (Arc : threads)"),
            ("RefCell<T>", "mutabilité intérieure"),
            ("Mutex<T>", "verrou"),
            ("Cow<'a, str>", "emprunté ou possédé"),
        ]),
        ("Chaînes", "", 230, [
            ('§format!("{x}")', "formater"),
            ('println!("{x:?}")', "affichage Debug"),
            ('"{x:#?}"', "Debug indenté"),
            ('"{:>8.2}"', "largeur, précision"),
            ("«s».to_string()", "&str → String"),
            ("&«s»[1..3]", "tranche (octets)"),
            ("«s».chars()", "caractères"),
            ("«s».split(«c»)", "découper"),
            ("«s».trim()", "espaces aux bords"),
            ("«s».len()  .is_empty()", "taille (octets)"),
            ("«s».lines()", "lignes"),
        ]),
    ],
    [  # colonne 2
        ("Fonctions & contrôle", "", 250, [
            ("fn f(«x»: i32) -> i32", "fonction"),
            ("§match «x» { … }", "filtrage exhaustif"),
            ("Some(v) => …", "motif + liaison"),
            ("1..=5 | 7 => …", "plage, alternative"),
            ("v if v > 0 => …", "garde"),
            ("§if let Some(v) = «x»", "un seul motif"),
            ("let … else { return }", "let-else"),
            ("while let Some(v) = …", "boucle sur motif"),
            ("loop { break «v»; }", "boucle → valeur"),
            ("for i in 0..«n»", "plage exclusive"),
            ("break 'ext;", "sortir de la boucle 'ext"),
            ("|x| x + 1", "closure"),
        ]),
        ("Gestion d'erreurs", "", 250, [
            ("§«expr»?", "propager l'erreur"),
            ('.unwrap()  .expect("…")', "⚠ panique si erreur"),
            (".unwrap_or(«d»)", "valeur par défaut"),
            (".ok_or(«e»)?", "Option → Result"),
            (".map_err(|e| …)?", "convertir l'erreur"),
            (".and_then(|v| …)", "enchaîner"),
            ("if let Err(e) = «r»", "traiter l'erreur"),
            ("std::process::exit(1)", "quitter"),
            ("Box<dyn Error>", "toute erreur"),
            ("anyhow::Result<T>", "applications"),
            ("thiserror", "erreurs de biblio."),
            ('panic!("…")', "arrêter le programme"),
        ]),
        ("Modules", "", 250, [
            ("mod «m»;", "déclarer un module"),
            ("pub  pub(crate)", "visibilité"),
            ("§use crate::«m»::«T»;", "importer"),
            ("use super::*;", "module parent"),
            ("pub use «m»::«T»;", "ré-exporter"),
            ("self  Self", "instance / type"),
        ]),
        ("Concurrence", "", 250, [
            ("thread::spawn(move || …)", "lancer un thread"),
            ("«h».join()", "attendre la fin"),
            ("mpsc::channel()", "canal"),
            ("async fn  «f».await", "asynchrone"),
            ("#[tokio::main]", "runtime (tokio)"),
        ]),
    ],
    [  # colonne 3
        ("Itérateurs", "", 250, [
            ("§.iter()  .iter_mut()", "emprunter"),
            (".into_iter()", "consommer"),
            ("§.map(|x| …)", "transformer"),
            (".filter(|x| …)", "filtrer"),
            (".enumerate()", "avec l'indice"),
            (".zip(«it»)", "apparier"),
            (".fold(0, |a, x| …)", "accumuler"),
            (".flat_map(|x| …)", "aplatir"),
            (".max_by_key(|x| …)", "maximum par clé"),
            (".chain(«it»)", "concaténer"),
            (".peekable()", "regarder sans avancer"),
            (".windows(2)  .chunks(«n»)", "fenêtres / paquets"),
            (".sum()  .count()", "agréger"),
            ("§.collect::<Vec<_>>()", "matérialiser"),
            (".any()  .all()  .find()", "tests"),
            (".skip(«n»)  .take(«n»)", "sauter / prendre"),
        ]),
        ("Collections", "", 260, [
            ("§vec![1, 2, 3]", "Vec littéral"),
            ("«v».push(«x»)  .pop()", "ajouter / retirer"),
            ("«v».sort()  .dedup()", "trier / dédoublonner"),
            ("«v».sort_by_key(|x| …)", "trier par clé"),
            ("§HashMap::new()", "dictionnaire"),
            ("«m».insert(«k», «v»)", "insérer"),
            ("«m».get(&«k»)", "Option<&V>"),
            (".entry(«k»).or_insert(0)", "insérer si absent"),
            ("HashSet  BTreeMap", "ensemble / trié"),
            ("VecDeque", "file double"),
            ("«v».retain(|x| …)", "filtrer en place"),
        ]),
        ("Traits & génériques", "", 250, [
            ("trait «T» { … }", "définir un trait"),
            ("§impl «T» for «S» { … }", "implémenter"),
            ("fn f<T: «Trait»>(x: T)", "contrainte"),
            ("where T: Clone + Debug", "clause where"),
            ("impl «Trait»", "type opaque"),
            ("dyn «Trait»", "dispatch dynamique"),
            ("§#[derive(Debug, Clone)]", "dérivation auto"),
            ("Display  From  Default", "traits courants"),
            ("PartialEq  Eq  Hash", "comparer, hacher"),
            ("impl Iterator for «S»", "itérateur perso"),
            ("type Item = «T»;", "type associé"),
        ]),
    ],
]

CARGO = [
    [
        ("Projet", "cargo", 230, [
            ("§cargo new «nom»", "binaire (--lib)"),
            ("cargo init", "dans le dossier courant"),
            ("§cargo build", "compiler (debug)"),
            ("cargo build --release", "optimisé"),
            ("§cargo run -- «args»", "compiler + lancer"),
            ("cargo check", "vérifier sans binaire"),
            ("§cargo test", "tests"),
            ("cargo test «nom»", "filtrer"),
            ("… -- --nocapture", "voir les println"),
            ("cargo bench", "benchmarks"),
            ("cargo doc --open", "documentation"),
            ("cargo clean", "supprimer target/"),
        ]),
        ("Dépendances", "", 230, [
            ("§cargo add «crate»", "ajouter"),
            ("cargo add «c» -F «feat»", "avec une feature"),
            ("cargo add --dev «crate»", "dépendance de test"),
            ("cargo remove «crate»", "retirer"),
            ("cargo update", "mettre à jour le lock"),
            ("cargo tree", "arbre des dépendances"),
            ("cargo install «crate»", "installer un binaire"),
            ("cargo search «nom»", "chercher (crates.io)"),
        ]),
        ("Cargo.toml", "", 230, [
            ("[package]", "nom, version, édition"),
            ('edition = "2024"', "édition du langage"),
            ("[dependencies]", "dépendances"),
            ('«crate» = "1.0"', "version (^1.0)"),
            ("[dev-dependencies]", "pour les tests"),
            ("[profile.release]", "optimisations"),
            ("[workspace]", "plusieurs crates"),
        ]),
        ("Crates incontournables", "", 230, [
            ("§serde  serde_json", "(dé)sérialisation, JSON"),
            ("clap", "arguments CLI"),
            ("tokio", "runtime async"),
            ("reqwest", "client HTTP"),
            ("anyhow  thiserror", "erreurs"),
            ("tracing", "logs structurés"),
            ("rayon", "parallélisme"),
            ("regex", "expressions régulières"),
            ("chrono", "dates et heures"),
        ]),
    ],
    [
        ("Qualité", "", 230, [
            ("§cargo fmt", "formater"),
            ("§cargo clippy", "linter"),
            ("cargo clippy --fix", "corriger"),
            ("cargo fix --edition", "migrer d'édition"),
            ("cargo audit", "failles (cargo-audit)"),
        ]),
        ("rustup", "", 250, [
            ("§rustup update", "mettre à jour Rust"),
            ("rustup default stable", "toolchain par défaut"),
            ("rustup install nightly", "installer nightly"),
            ("cargo +nightly «cmd»", "une fois en nightly"),
            ("rustup target add «t»", "cible (cross-compil.)"),
            ("rustup component add «c»", "clippy, rust-src…"),
            ("rustup doc --std", "doc hors ligne"),
        ]),
        ("Tests", "", 230, [
            ("§#[test]", "fonction de test"),
            ("#[cfg(test)] mod tests", "module de test"),
            ("§assert_eq!(«a», «b»)", "égalité"),
            ("assert!(«cond»)", "condition"),
            ("#[should_panic]", "doit paniquer"),
            ("#[ignore]", "ignoré par défaut"),
            ("/// ```", "exemple testé (doc-test)"),
        ]),
        ("Débogage & attributs", "", 230, [
            ("§dbg!(«expr»)", "afficher et renvoyer"),
            ("todo!()", "à compléter (panique)"),
            ("#[allow(dead_code)]", "taire un avertissement"),
            ("#[cfg(unix)]", "compilation conditionnelle"),
            ("#[inline]", "suggérer l'inlining"),
            ("RUST_BACKTRACE=1", "pile en cas de panique"),
            ("RUST_LOG=debug", "niveau de log"),
        ]),
        ("Entrées / sorties", "std", 250, [
            ("§fs::read_to_string(«p»)?", "lire un fichier"),
            ("fs::write(«p», «s»)?", "écrire"),
            ("BufReader … .lines()", "ligne à ligne"),
            ("env::args()", "arguments"),
            ('env::var("«VAR»")', "variable d'env."),
            ("Command::new(«cmd»)", "lancer une commande"),
            ("Path::new(«p»).join(«x»)", "chemins"),
        ]),
    ],
]

# Rouille, ambre « carton » de Cargo, paramètres en bleu
ACCENTS = {
    "aritim": "--a:#f67400; --b:#fdbc4b; --param:#3daee9;",
    "dark":   "--a:#ff8f6b; --b:#f3d36a; --param:#82b8ff;",
    "light":  "--a:#b23a17; --b:#7a5a00; --param:#1f5fbf;",
    "amoled": "--a:#e57a59; --b:#cdb35a; --param:#6c9be0;",
}

BRAND_LANG = ('<h2><span class="prompt">fn</span>RUST<span class="cursor under"></span></h2>'
              '<small>édition 2024 · <i>paramètres</i> · <span class="warn">⚠</span> panique · '
              '<span class="ess-key"></span>essentiel</small>')
BRAND_CARGO = ('<small>rustup · clippy · rustfmt</small>'
               '<h2><span class="prompt">$</span>CARGO</h2>')

if __name__ == "__main__":
    build_two_zones("rust", "Rust", ACCENTS, BRAND_LANG, BRAND_CARGO, LANGAGE, CARGO)
