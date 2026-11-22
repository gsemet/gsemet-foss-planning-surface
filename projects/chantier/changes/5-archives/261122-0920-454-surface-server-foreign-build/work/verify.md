Head: 7dd2e94e030b231fbff28a2978abcc6a8e70cd3b

Claims judged at 7dd2e94 (worktree head, `git rev-parse HEAD`):

1. source in server/hub entries, other_build, clause in one place (hub/lines.py), three callers
   (board_lines, Watch.start_line only when version clause absent, board --seat gated on
   `projects.chosen` and the dev-mode test): read in `git diff main...HEAD`; matches spec 1-3.
2. Tests: `python -m pytest tests/test_board_running.py tests/test_forge_hub.py
   tests/test_launch_modes.py tests/test_watcher_autostart.py -q` -> `78 passed in 21.50s`.
   They cover the matrix rows, start line, board --seat (single / no-project-chosen, exit 0, seat
   registered), the record fields, and the cards' sentences.
3. Cards (chief-of-staff.md, session-start.md) and the Q12 sentence in AGENTS.md, CONTRIBUTING.md,
   session-start.md: present in the diff; no stale `surface-server-foreign-build` reference
   (grep empty). The old "with no notice while the version is equal" clause is kept before the
   added "; but ..." (spec asked a replacement; the sense is right, noted, not failing).
4. Review: driver note "move 280c01d..7dd2e94 (conflict) inspector approved at 7dd2e94e03..." in
   `chantier log CR-454`.
5. PR body (work/pr-body.md): consistent with the diff; Known gaps name the UNVERIFIED real-session
   check and the forced multi-project case; the status line without `board:` prefix is declared
   under Autonomous decisions. `<sha7>` placeholders in the Test plan are for the Driver to fill.
6. CI green at this head per the brief (not re-run by me); no visual change, no evidence pairs.

VERIFIED


Description pass at 7dd2e94e030b231fbff28a2978abcc6a8e70cd3b (posted body of PR 427, gh pr view 427 --json body): sections and fold match pr-template; SHAs are 7dd2e94; Review box matches the log note "inspector approved at 7dd2e94e03..."; CI checks all pass (gh pr checks 427); Changes/Deliverables match the 13-file diff; Known gaps name the UNVERIFIED real-session check; Chief of Staff is a product term of a card change; no images.

VERIFIED
