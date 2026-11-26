#!/bin/sh
# usage: newmode.sh <worktree> <scratch dir> <commit>...
# Extracts each commit's sources and bundle into a scratch folder, switches the mode there only,
# runs okfreq 0.18.1 validate and trace, then removes the copy.
W="$1"; S="$2"; shift 2
for c in "$@"; do
  D="$S/c"; rm -rf "$D"; mkdir -p "$D"; git init -q "$D"
  git -C "$W" archive "$c" requirements src sphinx skills scripts test | tar -x -C "$D"
  sed -i 's/^strs_test_coverage_mode:.*/strs_test_coverage_mode: linked-swrs-and-acceptance-paths/' "$D/requirements/config.yml"
  echo "== $c $(grep '^strs_test_coverage_mode' "$D/requirements/config.yml")"
  uvx --python 3.12 --from okf-schema==0.18.1 okfreq validate "$D/requirements" --check-links --project-root "$D" --json > "$S/v-newmode-$c.json"
  echo "validate exit $?"
  uvx --python 3.12 --from okf-schema==0.18.1 okfreq trace "$D/requirements" --json > "$S/v-trace-$c.json"
  echo "trace exit $?"
  python -I -c "
import json,sys,collections
r=json.load(open(sys.argv[1],encoding='utf-8'))
t=json.load(open(sys.argv[2],encoding='utf-8'))
print({k:(len(v) if isinstance(v,list) else v) for k,v in r.items() if k!='requirements'})
print('warnings by code',dict(collections.Counter(str(w).split()[0] if isinstance(w,str) else w.get('code') for w in r.get('warnings',[]))))
for e in r.get('errors',[])[:10]: print('ERR',str(e)[:300])
print('scenario_markers',len(t.get('scenario_markers',[])))
" "$S/v-newmode-$c.json" "$S/v-trace-$c.json"
  rm -rf "$D"
done
