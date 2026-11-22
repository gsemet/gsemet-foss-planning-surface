# Conflicts: rebase of CR-458 on origin/main (CR-460)

All three hunks in scenario/run_scenario.py, commit 6f919732; both sides kept.

1. UNITS `surface-board`: cases list = main's (with `several_boards`) plus `remote_cli`. Budget 735 (main 710 + 25), as the CR had it.
2. Definitions near line 2822: CR-460's `NoRedirect` + `several_boards` and this CR's `remote_cli` both kept, two blank lines between.
3. CASES dict: `several_boards` and `remote_cli` both registered.

Welcome op count: `len(protocol.OPS)` = 27 in the worktree (main 26 + cli.run); scenario check and README "27 ops" already agree. No change needed.

Fast gate: `just check` in the worktree. First run: 1 failed (Windows flake test_w2_a_shell_inside_the_folder_refuses_then_lets_go under load), passed alone; second full run: 2140 passed, 20 skipped, release-notes ok.
