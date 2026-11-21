# Conflicts (rebase onto the rewritten cr-436 base)

- js/core/router.js (e317196e): header comment, resolve() (kept base's keptTab logic and added `topic`), apply() (kept base's `keep(place)`, added `topic`), href() (base's `t` line for the Batch view plus `viewPart(place)`). Both intents kept.
- js/main.js: both imports kept (`batchMode`, `topicIds`).
- tests/test_board_design.py: base's title-row tests and the CR's Help tests were both pure additions; kept both. The merged file passed 400 lines, so the Help tests moved to tests/test_board_help.py (staged, uncommitted).
- f3de619c applied with no conflict.

Fast gate: `just check` in the worktree: 1635 passed, 20 skipped, release-notes ok.
