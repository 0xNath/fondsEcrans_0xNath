"""Git (préfixe « git » omis) + outils Linux.

Textes en anglais (langue source) ; traductions dans locales/<langue>.json.
Conventions : voir src/wallpaper.py.
"""

from wallpaper import Brand, T, Wallpaper, Zone

GIT = [
    [  # colonne 1
        ("Configure & start", "git config", 268, [
            ("config --global user.name", "your name"),
            ("config --global user.email", "your e-mail"),
            ("config --global -e", "edit the config"),
            ("config --list", "show the config"),
            ("init", "create a repo here"),
            ("§clone «url»", "clone a repo"),
            ("clone --depth 1 «url»", "shallow clone"),
        ]),
        ("Stage & commit", "git add · commit", 246, [
            ("§status -sb", "short status + branch"),
            ("§add «file»", "stage a file"),
            ("§add -p", "stage in hunks"),
            ("add -A", "stage everything"),
            ("restore «file»", "⚠ discard changes"),
            ("§restore --staged «f»", "unstage"),
            ("rm --cached «f»", "stop tracking"),
            ("mv «a» «b»", "rename / move"),
            ('§commit -m "«msg»"', "commit"),
            ('commit -am "«msg»"', "stage + commit"),
            ("§commit --amend", "amend the last one"),
            ("commit --amend --no-edit", "… keep the message"),
        ]),
        ("Inspect", "git log · diff", 232, [
            ("§log --oneline --graph", "history (+ --all)"),
            ("log -p «file»", "history of a file"),
            ("log --author=«name»", "commits by an author"),
            ("log -S «text»", "who added/removed text"),
            ("§diff", "unstaged changes"),
            ("§diff --staged", "staged changes"),
            ("diff «a»..«b»", "between two commits"),
            ("show «commit»", "details of a commit"),
            ("blame «file»", "author of each line"),
            ("shortlog -sn", "commits per author"),
            ("reflog", "HEAD log"),
        ]),
        (".gitignore", "", 160, [
            ("*.log", "all .log files"),
            ("build/", "a whole directory"),
            ("/todo.txt", "root only"),
            ("**/tmp", "tmp at any depth"),
            ("!keep.log", "exception to a rule"),
        ]),
    ],
    [  # colonne 2
        ("Branches", "git switch · branch", 214, [
            ("branch", "local branches"),
            ("branch -a", "… and remote ones"),
            ("branch -vv", "with upstream branch"),
            ("§switch «b»", "switch branch"),
            ("§switch -c «b»", "create and switch"),
            ("switch -", "previous branch"),
            ("branch -m «name»", "rename current one"),
            ("branch -d «b»", "delete (if merged)"),
            ("branch -D «b»", "⚠ force delete"),
        ]),
        ("Merge & rebase", "git merge · rebase", 214, [
            ("§merge «b»", "merge b into here"),
            ("merge --no-ff «b»", "with a merge commit"),
            ("merge --abort", "abort the merge"),
            ("rebase «b»", "replay my commits on b"),
            ("§rebase -i HEAD~«n»", "rewrite the last n"),
            ("rebase --continue", "after resolving conflicts"),
            ("rebase --abort", "abort the rebase"),
            ("cherry-pick «commit»", "apply a commit here"),
            ("mergetool", "resolution tool"),
        ]),
        ("Remotes", "git remote · push", 236, [
            ("remote -v", "list remotes"),
            ("remote add «name» «url»", "add a remote"),
            ("fetch --prune", "fetch and prune"),
            ("pull", "fetch + merge"),
            ("§pull --rebase", "fetch + rebase"),
            ("§push", "push"),
            ("§push -u origin «b»", "publish + track"),
            ("push --force-with-lease", "⚠ force (safely)"),
            ("push -d origin «b»", "delete remote branch"),
            ("push --tags", "push tags"),
        ]),
        ("Stash", "git stash", 220, [
            ("§stash", "set aside"),
            ("stash -u", "… including untracked"),
            ('stash push -m "«msg»"', "with a message"),
            ("stash list", "list stashes"),
            ("§stash pop", "reapply and drop"),
            ("stash apply stash@{«n»}", "reapply, keep"),
            ("stash drop", "drop the latest"),
        ]),
    ],
    [  # colonne 3
        ("Undo", "", 226, [
            ("restore .", "⚠ discard all changes"),
            ("§reset HEAD~1", "uncommit, keep changes"),
            ("reset --soft HEAD~1", "… keep them staged"),
            ("reset --hard «commit»", "⚠ go back, discard all"),
            ("reset --hard HEAD@{1}", "undo the last reset"),
            ("§revert «commit»", "reverse commit (safe)"),
            ("restore -s «c» «f»", "file as it was in c"),
            ("commit --fixup «c»", "fixup commit for c"),
            ("rebase -i --autosquash", "… squash it into c"),
            ("clean -n", "dry-run the clean"),
            ("clean -fd", "⚠ delete untracked"),
        ]),
        ("References", "gitrevisions", 172, [
            ("HEAD", "current commit"),
            ("HEAD~«n»", "n-th ancestor"),
            ("HEAD^2", "2nd parent (merge)"),
            ("HEAD@{«n»}", "n-th position of HEAD"),
            ("main@{yesterday}", "main as of yesterday"),
            ("@{u}", "upstream branch"),
            ("@{-1}", "previous branch"),
            ("«a»..«b»", "commits in b not in a"),
            ("«a»...«b»", "commits only in a or b"),
        ]),
        ("Tags & tools", "", 226, [
            ("tag", "list tags"),
            ('tag -a v1.0 -m "«msg»"', "annotated tag"),
            ("describe --tags", "version from tags"),
            ("bisect start", "find the bad commit"),
            ("bisect good  bad", "mark the tested commit"),
            ("bisect reset", "end the search"),
            ("worktree add «dir» «b»", "2nd working copy"),
            ("grep «pattern»", "search the repo"),
            ("archive -o a.zip HEAD", "export as an archive"),
        ]),
        ("Typical workflow", "", 236, [
            ("switch -c feat/«x»", "1. new branch"),
            ("add -p ; commit", "2. small commits"),
            ("fetch origin", "3. fetch"),
            ("rebase origin/main", "4. catch up"),
            ("push -u origin feat/«x»", "5. publish → PR"),
            ("switch main ; pull", "6. after the merge"),
            ("branch -d feat/«x»", "7. clean up"),
        ]),
    ],
]

LINUX = [
    [  # colonne 1
        ("Files", "", 214, [
            ("§ls -lah", "details, hidden, sizes"),
            ("§cd -", "previous directory"),
            ("§cp -r «src» «dst»", "copy recursively"),
            ("mv «a» «b»", "move / rename"),
            ("rm -rf «dir»", "⚠ delete for good"),
            ("§mkdir -p «a/b/c»", "create the whole tree"),
            ("ln -s «target» «link»", "symbolic link"),
            ("tree -L 2", "tree (2 levels)"),
            ("du -sh *", "size of each item"),
            ("df -h", "free disk space"),
        ]),
        ("Read & search", "", 226, [
            ("§less «f»", "pager (/ = search)"),
            ("head  tail -n «n»", "start / end of file"),
            ("§tail -f «log»", "follow live"),
            ("§grep -rn «pattern» .", "search recursively"),
            ("grep -i  -v", "case / invert"),
            ("grep -c  -l", "count / files"),
            ('§find . -name "*.py"', "find by name"),
            ("find -type f -mtime -1", "modified < 24 h [GNU]"),
            ("rg «pattern»", "ripgrep, fast"),
            ("fd «pattern»", "modern find"),
        ]),
        ("Process text", "", 214, [
            ("wc -l", "count lines"),
            ("§sort | uniq -c", "count duplicates"),
            ("sort -nr -k2", "num., reversed, col. 2"),
            ("cut -d, -f1,3", "columns 1 and 3 (CSV)"),
            ("awk '{print $2}'", "2nd column"),
            ("sed -i 's/«a»/«b»/g'", "in place [GNU]"),
            ("tr a-z A-Z", "translate chars"),
            ("xargs -I{} «cmd» {}", "one cmd per line"),
            ("jq '.«key»'", "extract from JSON"),
            ("diff -u «a» «b»", "compare two files"),
        ]),
        ("Archives", "", 250, [
            ("§tar -czf «a».tar.gz «dir»", "create"),
            ("§tar -xzf «a».tar.gz", "extract (-C dir)"),
            ("tar -tf «a».tar.gz", "list contents"),
            ("zip -r «a».zip «dir»", "create a zip (unzip)"),
        ]),
    ],
    [  # colonne 2
        ("Processes & services", "", 228, [
            ("§ps aux | grep «name»", "find a process"),
            ("htop", "interactive monitor"),
            ("§kill  kill -9 «pid»", "stop / force"),
            ("pkill «name»", "stop by name"),
            ("«cmd» &", "run in background"),
            ("Ctrl-z  bg  fg", "suspend / resume"),
            ("nohup «cmd» &", "survives logout"),
            ("watch -n 2 «cmd»", "rerun every 2 s"),
            ("free -h", "memory used"),
            ("systemctl status «svc»", "status of a service"),
            ("journalctl -u «svc» -f", "service logs, live"),
        ]),
        ("Permissions", "", 214, [
            ("§chmod +x «f»", "make executable"),
            ("chmod 644 «f»", "rw-r--r--"),
            ("chmod 755 «dir»", "rwxr-xr-x"),
            ("chown «u»:«g» «f»", "change owner"),
            ("sudo «cmd»", "run as root"),
            ("§sudo !!", "rerun the last as root"),
            ("whoami  id", "user / groups"),
        ]),
        ("Network", "", 228, [
            ("ip a", "interfaces and addresses"),
            ("ss -tulpn", "listening ports"),
            ("ping «host»", "test the connection"),
            ("dig «domain»", "DNS lookup"),
            ("curl -I «url»", "HTTP headers"),
            ("curl -LO «url»", "download a file"),
            ("§ssh «u»@«host»", "remote login"),
            ("scp «f» «host»:«dir»", "copy to a server"),
            ("§rsync -avz «src» «dst»", "synchronise"),
        ]),
        ("Shell & redirections", "bash", 180, [
            (">  >>", "write / append"),
            ("§2>&1  &>", "stderr / all to …"),
            ("|", "chain (pipe)"),
            ("&&  ||", "if success / if failure"),
            ("$(«cmd»)", "insert the output"),
            ("!!  !$", "last cmd / last arg."),
            ("§Ctrl-r", "search history"),
            ("Ctrl-a  Ctrl-e", "start / end of line"),
            ("Ctrl-w  Ctrl-u", "delete word / to line start"),
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

WALLPAPER = Wallpaper(
    slug="git-linux",
    title="Git · Linux",
    accents=ACCENTS,
    left=Zone(Brand("GIT", svg=BRANCH_SVG, note='"git" prefix omitted'), GIT),
    right=Zone(Brand("LINUX", prompt="~$", cursor="block", note="bash · coreutils · network · system"), LINUX),
)
