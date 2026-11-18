# Before / after (CR-367)

Before: base 380eca4f (main checkout code, new tests from the head's worktree):
`uv run --no-sync --project <main checkout> python -m pytest <the 5 test files> -q` -> 4 failed, 65 passed
(test_batch_end: merged-release-PR[link], stack-line; test_board_prs_release[True]; test_external_archive delivery).
After: head 4833e30c, same command with `--project .` in the worktree -> 69 passed.
Board: board-rows.json (state the board serves, from `project_state`) and board-lists.log (node on semantics.js).
No screenshot of the pane from a real session (none available): a known gap.
