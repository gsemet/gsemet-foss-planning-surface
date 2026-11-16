# Conflicts, rebase onto origin/main (3fb9129)

Three files conflicted; all resolved keeping both intents.

- docs/agents-and-models.md (1 hunk): kept main's `ci` (`beside_gate`) sentence and added this CR's `long_gate` key to the list of other keys.
- skills/chantier/references/driver.md (1 hunk, long gate bullet): kept main's lead (first push and PR, `ci: beside the long gate` order) and this CR's body (only the rules' long gate, as many at once as `chantier.yaml` allows, short gates run directly, `--no-gate`).
- skills/chantier/scripts/cli/src/chantier/playbook/config.py (2 hunks): kept main's `keyed` dispatch (`prices`, `board`, `ci`) plus a separate `long_gate` branch calling `_long_gate` (it returns an int, so not in `keyed`); the unknown-key message now lists "roles", "prices", "board", "ci" and "long_gate".

Commit message unchanged. Rebase finished (`git rebase --continue`), new head 74fd88b. Not pushed.

Fast gate: `just check` after the resolution: format, ruff, mypy, uv lock, pytest (63 passed) and release-notes check all pass (exit 0). A first run failed ruff format on line endings of my edit; fixed before the final run.
