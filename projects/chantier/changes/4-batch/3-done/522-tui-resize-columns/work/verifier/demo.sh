#!/usr/bin/env bash
# The Verifier's demo project: its own git repository in the scratch folder, made-up data only.
# usage: demo.sh <args of chantier>   (every call runs in it, with no --project and no CHANTIER_ROOT; the head's own code)
W="$(cygpath -m "$HOME")/Projets/chantier.worktrees/batch-32-CR-522"
S="$(cd "$(dirname "$0")/.." && pwd -W)/scratch"
cd "$S/demo-shop" || exit 9
exec env -u CLAUDE_CODE_SESSION_ID -u CHANTIER_ROOT -u CHANTIER_BATCH_DEMO -u COPILOT_CLI \
  CHANTIER_HOST=claude CLAUDE_CODE_ENTRYPOINT=claude-desktop CHANTIER_CONFIG_HOME="$S/config" \
  CHANTIER_SKILL_DIR="$W/skills/chantier" CHANTIER_PLUGIN_ROOT="$W" PYTHONUTF8=1 \
  uv run --no-sync --project "$W" chantier "$@"
