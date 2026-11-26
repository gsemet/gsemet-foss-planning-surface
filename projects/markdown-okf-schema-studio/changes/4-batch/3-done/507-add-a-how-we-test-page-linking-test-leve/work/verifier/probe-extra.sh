#!/usr/bin/env bash
# Usage: probe-extra.sh <worktree> <verifier folder>
# Extra drift probes for the PR body's "adds or renames ... now fails" sentence. Each one is a
# temporary change, then the compiled drift test alone, then a restore by copy (never git).
set -uo pipefail
tree="$1"
notes="$2"
cd "$tree" || exit 2
log="$notes/probe-extra.log"
: >"$log"

run_drift() {
    node scripts/node-test.mjs unit out/test/site/howWeTest.test.js 2>&1 |
        grep -E "^ℹ (tests|pass|fail|skipped)|^✖ How we test|^✖ every|missing|^  \+   '|^  \+ '|actual:|check_new_probe|zzz|line [0-9]+:" |
        sort -u
}

probe() { # <name> <file> <node edit expression on t>
    local name="$1" file="$2" edit="$3" backup="$notes/probe-extra.backup" before after
    cp -p "$file" "$backup"
    before="$(sha256sum "$file" | cut -d' ' -f1)"
    node -e 'const fs=require("node:fs");const [f,e]=process.argv.slice(1);const t=fs.readFileSync(f,"utf8");const o=new Function("t","return "+e)(t);if(o===t){console.error("edit changed nothing");process.exit(3)}fs.writeFileSync(f,o)' "$file" "$edit" || { cp -p "$backup" "$file"; rm -f "$backup"; echo "$name: edit failed" | tee -a "$log"; return; }
    {
        echo "== $name at $(git rev-parse HEAD)"
        git diff -U0 -- "$file" | grep -E "^[+-]" | cut -c1-160
        run_drift
    } >>"$log"
    cp -p "$backup" "$file"
    rm -f "$backup"
    after="$(sha256sum "$file" | cut -d' ' -f1)"
    echo "restored $file: sha256 $before = $after" >>"$log"
}

probe "new requirements-lint script" justfile 't.replace(/(\n    \{\{ npm \}\} run check:diagrams)/, "\n    uv run --no-sync python scripts/check_new_probe.py$1")'
probe "new CI job" .github/workflows/ci.yml 't.replace(/\njobs:(\r?\n)/, "\njobs:$1  zzz-probe:$1    runs-on: ubuntu-latest$1    steps: []$1")'
probe "e2e group no longer named" docs/how-we-test.md 't.split("`gfm`").join("")'
probe "broken relative link" docs/how-we-test.md 't + "\n[probe](../test/zzz-missing.ts)\n"'

folder=test/zzz-probe
if [ ! -e "$folder" ]; then
    mkdir "$folder"
    {
        echo "== new test folder $folder at $(git rev-parse HEAD)"
        run_drift
    } >>"$log"
    rmdir "$folder"
fi
echo "== status after the extra probes" >>"$log"
git status --porcelain >>"$log"
echo "== end" >>"$log"
cat "$log"
