#!/usr/bin/env bash
# The Verifier's demo project: its own git repository in the scratch folder, made-up data only.
# usage: demo.sh <args of chantier>   (every call runs in it, with no --project and no CHANTIER_ROOT; the head's own code)
W="C:/Users/gaeta/Projets/chantier.worktrees/batch-32-CR-522"
S="C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/chantier/changes/4-batch/2-actives/522-tui-resize-columns/work/scratch"
cd "$S/demo-shop" || exit 9
exec env -u CLAUDE_CODE_SESSION_ID -u CHANTIER_ROOT -u CHANTIER_BATCH_DEMO -u COPILOT_CLI \
  CHANTIER_HOST=claude CLAUDE_CODE_ENTRYPOINT=claude-desktop CHANTIER_CONFIG_HOME="$S/config" \
  CHANTIER_SKILL_DIR="$W/skills/chantier" CHANTIER_PLUGIN_ROOT="$W" PYTHONUTF8=1 \
  uv run --no-sync --project "$W" chantier "$@"
