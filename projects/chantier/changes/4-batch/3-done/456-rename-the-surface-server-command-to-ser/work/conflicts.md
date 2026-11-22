# CR-456 rebase onto origin/main

`git rebase origin/main` (worktree batch-30-CR-456): 1 commit replayed, no textual conflict. New head: see below.

Semantic follow-ups (main's new text that named the old command), staged, NOT committed (resolver never commits):
- CONTRIBUTING.md line 101: named tool `board` -> `serve`.
- docs/web-board.md lines 254, 259: `... chantier ... board` invocation -> `serve`.
Checked: commands/live.py (CR-446) already says `chantier serve (or chantier webui)`; scenario/run_scenario.py, cards, AGENTS.md need no change.

Gates (worktree, one at a time):
- `just check`: first run 1 failure, test_triage_moves.py::test_w2_a_shell_inside_the_folder_refuses_then_lets_go (Windows held-folder flake; file untouched by this CR; passes alone, 9 passed). Second full run: exit 0, 1909 passed, 20 skipped, release-notes ok.
- `just eval-dry-run`: exit 0, 19 of 19 cases as expected.
Logs: work/gates/check.log, check2.log, dry.log
