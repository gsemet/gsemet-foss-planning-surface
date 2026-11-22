# Verify CR-461

Head: aa8ca7f3bfde1b1a821008b89ba9d7265366457d

CI: all green at this head (cited from the caller's brief; Linux and macOS are CI's). Local runs on Windows below.

1. New live test fails before, passes after (aa8ca7f3).
   Before: detached worktree of be1794e7 (base) with the two test files from aa8ca7f3 checked out.
   `uv run --locked --group dev pytest -q -p no:xdist tests/test_live_model.py -k once_refuses_an_unserved`
   -> `1 failed, 47 deselected` (screen printed, no `--only` refusal).
   After (head): same command -> `1 passed, 47 deselected`.
2. 20 serial runs at head of `-k "only or w2 or once_refuses"` over test_live_link, test_live_model, test_triage_moves: 20 x `5 passed, 69 deselected`.
3. 30 more serial runs at head of the PR's exact command `-k "(test_the_refusals_of_several_boards and only) or w2"` (test_live_link, test_triage_moves): 30 x `3 passed, 23 deselected` (with the 20 above, 50 runs, none failing).
4. Folder-lock test under load, 8 parallel loops x 7 runs of `-k w2`:
   before (base be1794e7, old test): 55 passed, 1 failed (reproduces the flake);
   after (head): 56 x `1 passed, 8 deselected`.
5. PR description (`gh pr view 437`): posted body is identical to work/pr-body.md (diff: one trailing newline). Summary, Deliverables, Changes match the diff (live.py check, two test files); Known gaps present and true; no image; no role name outside Internal references. Gate log first line: `gate CR-461 branch chantier/batch-30/cr-461-... head aa8ca7f3bfde1b1a821008b89ba9d7265366457d` (scenario gate).
   Note: the Test plan boxes are unchecked placeholders, owned by the Driver at ship.

VERIFIED
