# Conflicts: CR-412 rebase onto origin/main

One conflicted hunk, in skills/chantier/scripts/cli/tests/test_board_journal.py (end of file):
main added `test_a_board_event_its_model_refuses_leaves_the_write_and_names_the_skipped_line`
(typed-journal change); the CR added `test_the_new_route_files_a_title_above_the_text_and_refuses_a_paragraph_without_one`.
Choice: kept both tests, one after the other, two blank lines between; no markers left, no BOM.
Rebase continued; the CR's commit is cdec7de8, tree clean.

Fast gate: `just check` in the worktree: passed (1094 passed, 14 skipped; biome clean; release-notes ok).
