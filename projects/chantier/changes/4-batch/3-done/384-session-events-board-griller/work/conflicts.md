# Conflicts: CR-384 rebased onto CR-383 (9c3fb6d)

Only `scenario/run_scenario.py` conflicted, two hunks (near lines 8549 and 8569), in the board-config scenario's two `watch` end checks.

- Hunk 1 (`a running chantier watch ends with the config changed on the board line`): base (CR-383) asserts `got == [told, cursor(1)]` with the new `cursor()` helper; CR-384 asserted the same "still running ... watch --after 2" line inline. Same intent, so I kept the base's `cursor(1)` form. The helper is already defined above and carries the CR-384 text.
- Hunk 2 (`the watcher ends with the specifying.parallel 4 -> 1 line`): same, kept `cursor(2)`.

Checks: no byte-order mark added (file starts `#!/`). Rebase continued with the original message, no leading `#`. New head 876197d9.

Fast gate: `just check` in the worktree, passed (ruff, mypy "no issues in 240 source files", uv lock check, biome, pytest 759 passed, release-notes ok).
