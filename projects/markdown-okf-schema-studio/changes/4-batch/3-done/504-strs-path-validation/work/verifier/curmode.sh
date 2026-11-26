#!/bin/sh
# usage: curmode.sh <worktree> <scratch dir> <commit>...
# Same scratch extraction as newmode.sh with the committed coverage mode: okfreq validate, then the head's marker check.
W="$1"; S="$2"; shift 2
for c in "$@"; do
  D="$S/c"; rm -rf "$D"; mkdir -p "$D"; git init -q "$D"
  git -C "$W" archive "$c" requirements src sphinx skills scripts test package.json esbuild.mjs | tar -x -C "$D"
  echo "== $c $(grep '^strs_test_coverage_mode' "$D/requirements/config.yml")"
  uvx --python 3.12 --from okf-schema==0.18.1 okfreq validate "$D/requirements" --check-links --project-root "$D" --json > "$S/v-cur-$c.json"
  echo "validate exit $?"
  python -I -c "
import json,sys
r=json.load(open(sys.argv[1],encoding='utf-8'))
print({k:(len(v) if isinstance(v,list) else v) for k,v in r.items() if k!='requirements'})
" "$S/v-cur-$c.json"
  node "$W/scripts/check-marker-companions.mjs" --root "$D" > "$S/cm-$c.log" 2>&1 ; echo "check-markers (head script, --root copy) exit $?"
  tail -n 4 "$S/cm-$c.log" | cut -c1-220
  grep -c . "$S/cm-$c.log"
  rm -rf "$D"
done
