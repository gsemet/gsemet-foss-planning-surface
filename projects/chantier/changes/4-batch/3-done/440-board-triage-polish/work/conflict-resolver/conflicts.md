# Conflicts, CR-440 rebase onto CR-436 branch

- skills/chantier/scripts/cli/tests/test_board_design.py, one hunk (end of file): base side holds the
  batch-kanban tests (BATCH_KEYS, test_the_batch_kanban_as_shipped, batch folder chip test); this CR adds
  test_the_fold_and_the_writes_count_explanation_ship. Choice: keep both, base's first, then this CR's.
- Second commit (docs screenshots): no conflict.

Fast gate: `uv run --no-sync --project C:/Users/gaeta/Projets/chantier pytest tests/test_board_design.py -q` (in skills/chantier/scripts/cli): 37 passed. `just test` not run (caller's instruction).
Head: 9b22d87490cbedbbc31b797543989ca79cc396c3
