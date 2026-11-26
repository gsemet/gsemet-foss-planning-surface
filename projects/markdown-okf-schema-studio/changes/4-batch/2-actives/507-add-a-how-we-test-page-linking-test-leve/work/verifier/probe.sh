#!/usr/bin/env bash
# Usage: probe.sh <worktree> <verifier folder> <1|2|3>
# One drift probe of the spec's evidence item 4: back the file up, edit it, run `just unit`,
# restore it by copy (never by a git command) and prove the hash is back.
set -uo pipefail
tree="$1"
notes="$2"
probe="$3"
cd "$tree" || exit 2
case "$probe" in
    1) file=docs/how-we-test.md ;;
    2) file=requirements/config.yml ;;
    3) file=.github/workflows/ci.yml ;;
    *) exit 2 ;;
esac
backup="$notes/probe-$probe.backup"
log="$notes/probe-$probe-unit.log"
cp -p "$file" "$backup"
before="$(sha256sum "$file" | cut -d' ' -f1)"
node -e '
const fs = require("node:fs");
const [probe, file] = process.argv.slice(1);
const text = fs.readFileSync(file, "utf8");
const edit = {
  "1": (t) => t.split("`stress`").join(""),
  "2": (t) => t.replace(/^(strs_test_coverage_mode:\s*)linked-swrs-and-validation-test/m, "$1linked-swrs-and-acceptance-paths"),
  "3": (t) => t.replace("group: [trust-security]", "group: [trust-security, gfm]"),
}[probe];
const out = edit(text);
if (out === text) { console.error("probe edit changed nothing"); process.exit(3); }
fs.writeFileSync(file, out);
' "$probe" "$file" || { cp -p "$backup" "$file"; exit 3; }
{
    echo "probe $probe at $(git rev-parse HEAD), edited $file:"
    git diff --stat -- "$file"
    git diff -U0 -- "$file"
    echo "---- just unit"
} >"$log" 2>&1
just unit >>"$log" 2>&1
code=$?
cp -p "$backup" "$file"
rm -f "$backup"
after="$(sha256sum "$file" | cut -d' ' -f1)"
echo "just unit exit $code" | tee -a "$log"
echo "sha256 before $before"
echo "sha256 after  $after"
echo "status after restore:"
git status --porcelain
