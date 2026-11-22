# Verify CR-456

Head: d42b8b3cc4f38e111befac469ed1915fc1746769

Move judged: the worktree and PR #430 head are now d42b8b3c, the prompt's f7afc81d rebased onto main a09a58bd.
`git rev-parse d42b8b3c^{tree} f7afc81d^{tree}` -> both `20de45c2c4626b4bbc964c23d8b90ebb700cf57b`; `git range-diff` shows the 3 commits equal. Code claims 1-3 judged at d42b8b3c (same tree as f7afc81d).

## Claims

1. Renamed lines, serve_argv, find_pid, command names, ports, cookies, webui (in-process), at d42b8b3c.
   `uv run --no-sync --project . pytest tests/test_serve_webui.py tests/test_command_names.py tests/test_board_running.py tests/test_writer_lines.py tests/test_watch_board.py tests/test_board_exposure.py -q` -> `94 passed in 39.14s`. PASS.
2. `chantier board` is argparse's invalid choice, at d42b8b3c: `chantier board` -> `chantier: error: argument cmd: invalid choice: 'board', maybe you meant 'order'? (choose from ... 'serve', 'webui', 'live' ...)`. PASS.
3. session-start.md step 4 names `PID <n> serve <project> (started by webui)`; AGENTS.md names `webui` (lines 131-132, 172): grep output matched at d42b8b3c. PASS.
4. Scenario `serve_and_webui` (surface-board unit): pipeline run https://github.com/gsemet/chantier/actions/runs/45031293669 at d42b8b3c, job `just scenario (ubuntu-latest)`: `FAIL  surface-board (github): 315/316 checks`, `FAIL surface-board (github): serve_and_webui ran to the end`, `error: recipe scenario failed on line 33`. The other units pass; check (3 OS) and eval-dry-run pass. No artifact or transcript is uploaded, so the failing line of the step is not visible in the log. FAIL. (Locally port 8765 is held by real boards, so the unit cannot prove it here.)
5. PR description: the Test plan says `Local gates at f7afc81: just check, just eval-dry-run`; the Driver's log says eval-dry-run was not re-run at f7afc81 ("not owed beyond r4"), and the head is now d42b8b3c with no carry line. The Review box's approval note is at 399c87e2, `committed as f7afc81` (accepted by the card). The Known gaps names the local scenario limit but not that the pipeline's surface-board is red. Minor; fails with claim 4.

## Verdict

NOT VERIFIED: the long gate `just scenario (ubuntu-latest)` is red at d42b8b3c on the CR's own step `serve_and_webui` (claim 4); the description's gates line overclaims (claim 5).
