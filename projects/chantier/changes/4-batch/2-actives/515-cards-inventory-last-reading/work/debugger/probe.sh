#!/usr/bin/env bash
# Run the failing test on exported trees, with and without NO_COLOR. Usage: bash probe.sh
# Exports go under work/scratch/dbg/<name> and are removed at the end. The worktree is only read.
CR="C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/chantier/changes/4-batch/2-actives/515-cards-inventory-last-reading"
WT="C:/Users/gaeta/Projets/chantier.worktrees/batch-32-CR-515"
PY="$WT/.venv/Scripts/python.exe"
T="skills/chantier/scripts/cli/tests/test_live_ready.py"
K="test_the_interactive_screen_links_the_pr_and_colours_the_state_words"
D="$CR/work/scratch/dbg"
git -C "$WT" diff --quiet 4d12a5be 22ccbe0 -- uv.lock && echo "uv.lock: same at 4d12a5be and 22ccbe0"
echo "test file changes 4d12a5be..22ccbe0: $(git -C "$WT" diff --name-only 4d12a5be 22ccbe0 -- $T | wc -l)"
for rev in 22ccbe0 fbdb53d2 4d12a5be; do
  mkdir -p "$D/$rev"
  git -C "$WT" archive "$rev" pyproject.toml skills | tar -x -C "$D/$rev"
  src="$D/$rev/skills/chantier/scripts/cli/src"
  echo "== $rev: imports $(cd "$D/$rev" && PYTHONPATH="$src" "$PY" -c 'import chantier; print(chantier.__file__)')"
  for nc in unset 1; do
    if [ $nc = unset ]; then pre=(env -u NO_COLOR); else pre=(env NO_COLOR=1); fi
    out=$(cd "$D/$rev" && PYTHONPATH="$src" "${pre[@]}" "$PY" -m pytest -q -p no:cacheprovider "$T" -k "$K" 2>&1)
    echo "   NO_COLOR=$nc: $(echo "$out" | tail -1)"
    echo "$out" | grep -E '^tests?.*Error|test_live_ready\.py:[0-9]+' | sort | uniq -c
  done
done
rm -rf "$D"
echo "== head 22ccbe0 in the worktree, 20 runs each, alone"
for nc in unset 1; do
  if [ $nc = unset ]; then pre=(env -u NO_COLOR); else pre=(env NO_COLOR=1); fi
  for i in $(seq 20); do
    (cd "$WT" && "${pre[@]}" "$PY" -m pytest -q -p no:cacheprovider "$T" -k "$K" 2>&1 | tail -1 | sed -E 's/ in [0-9.]+s.*//')
  done | sort | uniq -c | sed "s/^/   NO_COLOR=$nc: /"
done
