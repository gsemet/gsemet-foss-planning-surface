# Verify CR-456, at head 11975a1f91b402edd6b5a10ae4f0d14081212e93

Head: 11975a1f91b402edd6b5a10ae4f0d14081212e93

Move judged: conflict restack of cf29f3c (resolved files hosts/claude-code.md, hosts/copilot.md). Behaviour claims re-run at this head.

## Claims

1. Renamed lines, serve_argv, find_pid, no stale command name, cookies, ports, webui (in-process), at 11975a1.
   `uv run --locked python -m pytest tests/test_serve_webui.py tests/test_command_names.py tests/test_board_running.py tests/test_writer_lines.py tests/test_watch_board.py -q` (in skills/chantier/scripts/cli) -> `79 passed in 4.70s`. PASS.
2. `chantier board` is argparse's invalid choice, at 11975a1.
   `chantier board` -> `chantier: error: argument cmd: invalid choice: 'board', maybe you meant 'order'? (choose from ... 'serve', 'webui', 'live' ...)`. PASS.
3. `webui` real exercise, at 11975a1, scratch repo under work/scratch (removed after): with no server, `chantier webui` -> `board on http://127.0.0.1:59016/?k=... over <folder>` and `board: stops by itself after 30 min with no client (webui started it)`, exit 0; the process list showed `... chantier --skill .../skills/chantier serve --stop-idle` with no `--seat`; a second `chantier webui` -> `board already running at http://127.0.0.1:59016/?k=...`, `board: watches the planning files`, idle-stop line. Server stopped by PID. PASS.
4. Cards/docs: `grep -rn '$CHANTIER board\|chantier board ' AGENTS.md skills/chantier/references README.md CONTRIBUTING.md docs` (release-notes excluded) -> only `AGENTS.md:59` (the prose "another chantier board", not the command). hosts/claude-code.md rows 39, 49, 55, 729 name `serve`. PASS.
5. Scenario step `serve_and_webui` (scenario/run_scenario.py:2686), `just scenario --unit surface-board --forge github` at 11975a1 (log: work/gates/scenario-surface-board.log): unit 105/125 FAIL on this machine. Its serve_and_webui steps failed because port 8765 is held on this machine by another program (the user's live board: `netstat` shows 127.0.0.1:8765 and 0.0.0.0:8765 LISTENING), so the second-surface step was skipped, and the unit's `webui` (cold `uvx --from <worktree>` start) exited 4 "did not start within 20 s"; the unit's earlier steps (remote_board, forge_hub, watcher steps, untouched by this CR's tests) fail on the same machine too. Not proved here; claim 3 is the nearest real exercise. The pipeline's ubuntu `just scenario` is the proof. NOT PROVED (not a code defect shown).
6. PR #430 description (gh pr view 430, head 11975a1): FAILS. The Test plan says `Local gates at cf29f3c` and `Review: approved at cf29f3c`, but the head is 11975a1 after the restack (the Driver's log: restack approved at 7c3de97, amended to 11975a1; gates at 11975a1 are in the log). Known gaps still says the step "has been compiled but not run locally" without the local run's failure on this machine. NOT VERIFIED until the box and gates line name the head (or a carried-from with reason) and Known gaps is updated.

## Verdict

NOT VERIFIED: the description is stale at the head (claim 6); the code claims 1-4 hold at 11975a1; the scenario step (5) is unproved locally and awaits the pipeline's gate.
