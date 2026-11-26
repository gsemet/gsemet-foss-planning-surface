# Verify CR-472

Head: b9ec1d6c2b3f6e78cbe0d156f18666e61d057876

All claims judged at b9ec1d6 (full SHA above).

- Walk, held default (user's board on 127.0.0.1:8765, PID 18292), scratch project, real `chantier serve --host 127.0.0.1` at b9ec1d6:
  `board: port 8765 is held by another chantier board (another project's key): this one takes port 8766` then `board on http://127.0.0.1:8766/?k=<key>`. PASS.
- Walk past a plain socket: a plain socket on 8766 plus the user's board on 8765: `serve` bound 8767 (netstat: 127.0.0.1:8767 LISTENING by my chantier serve, which I then stopped by PID). PASS. The takes-port text for `another program` is asserted exactly by the walk test below.
- Named `--port 8765` held: `error: board not started: port 8765 on 127.0.0.1 is held by another chantier board (another project's key; ...): pass --port <n> (0: any free port)`, exit 4. PASS.
- Tests, `pytest tests/test_serve_webui.py tests/test_board.py tests/test_board_exposure.py -q`: 56 passed. They hold the walk test (another key, another folder, plain, two ports in a row, named port refused), the end-of-walk `no free port` line, WSAEACCES and WSAEADDRINUSE as held, and other errors refusing. PASS.
- Texts of part 5 (AGENTS.md, serve --port help, docs/web-board.md both places, evals/README.md step 2, scenario/README.md bullet): read in `git diff origin/main...HEAD`, match the spec. PASS.
- Size: `wc -l` binding.py 80, command.py 379, both under 400. PASS.
- Scenario step: no `--port DEFAULT_PORT` or skip left (grep of run_scenario.py: DEFAULT_PORT only in the new checks). Transcript scenario/results/20261124-074004-25532/surface-board-github.md: 353/353, with the first-server walk check, the second-surface check and `webui` printing `board already running at http://127.0.0.1:8766/...` with the user's board on 8765. PASS.
- Long gate: gates/20261124-075626.log first line names CR-472 and head b9ec1d6c...; gate result=pass in `log`; surface-board 353/353 ok. PASS.
- CI at b9ec1d6 (gh pr view 448): all 5 checks SUCCESS. PASS.
- Review: `log` notes "r1 approved at 55fed1ef..., committed as b9ec1d6c..." (rebased). The Review box is still a placeholder to be filled by the Driver.
- PR description (posted body = work/pr-body.md): renders, matches the diff, Known gaps carries the UNVERIFIED cause (part 0 did not reproduce) and the WSAEACCES/macOS gap, no image. PASS.
- Part 0: the cause is marked UNVERIFIED in the PR, as the brief states; not proved by me.

Scratch files removed. No before/after images (CLI change): the before is the spec's gate log.

VERIFIED
