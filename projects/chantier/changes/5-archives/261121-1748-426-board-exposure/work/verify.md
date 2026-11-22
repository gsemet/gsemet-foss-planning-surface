# Verify CR-426

Head: 7c1d8905be1a1ca0a0f85e15710d2bc4670661ee

All claims judged at 7c1d890 (code run from the worktree, `uv run --no-sync --project <worktree> chantier ...`, in a scratch git project under work/scratch, removed after). Note: `board` blocks, so each start ran inside a `timeout`-bounded subshell with a short wait (a background of the run, bounded by timeout); no process was killed by name.

1. Default, no host, no chantier.yaml, `board --port 0`:
   `board on http://127.0.0.1:55195/?k=<key> over <scratch>/.agents/changes` (one line only); server.json `"host": "127.0.0.1"`. PASS.
   Before (base): `git show origin/main:.../board/address.py` line 21 `DEFAULT_HOST, DEFAULT_PORT = "0.0.0.0", 8765`; after line 21 `"127.0.0.1"`.
2. `board.host: network`, `board --port 0` (this machine has a network): server.json `"host": "0.0.0.0"`; lines:
   `board on http://192.168.5.45:64961/?k=<key> over ...`, `on this machine: http://127.0.0.1:64961/?k=<key>`, `board: listens on the local network (0.0.0.0); the link holds its key: give it to the user only, plain HTTP`. PASS. The no-network outcome is proved by the tests (claim 5), not run here.
3. `board.host: 127.0.0.1` in chantier.yaml: `playbook` exit 2 and `board --port 0` exit 2, messages:
   `chantier.yaml:2: board: "host" is network (this machine's local network address, found at each start); a fixed address goes in --host, for one start`. PASS.
4. `--new-key` while a board runs: second command printed `board already running at http://127.0.0.1:50516/?k=EzXE...Pzk`, key different from the first (`C5eD...Syg`); curl old link: `HTTP/1.1 401 Unauthorized`; new link: `HTTP/1.1 303 See Other`, `set-cookie: chantier_board=...; Max-Age=2592000; Path=/; HttpOnly; SameSite=Strict`. PASS.
5. `pytest test_board_exposure.py test_playbook_layers.py test_board_running.py -q`: `41 passed in 12.81s`. PASS.
6. CI at 7c1d890 (`gh pr checks 397`): 3x just check, eval-dry-run, scenario (ubuntu) all pass; Driver's log note records the same. The scenario's new checks (board steps 10, 11, revocation) are in the diff (`scenario/run_scenario.py`, `scenario/README.md`) and ran in that green job.
7. PR description vs diff (16 files: CLI address/command/key/declare/board_check/config, 4 cards, README, docs/web-board.md, docs/boards.md, scenario, tests): Summary, Deliverables, Changes and the autonomous decision (board_check.py split) match the diff; renders cleanly; no images. PASS.
   Notes for the Driver, not failures: the Known gap "UNVERIFIED: the pipeline's scenario run ... has not run at this head yet" is now stale (scenario ubuntu is green at 7c1d890); the Test plan keeps its `<sha7>` placeholders and unticked boxes, to fill at ship (no Review note at this head yet in `log`).

VERIFIED

## Description pass at 7c1d8905be1a1ca0a0f85e15710d2bc4670661ee

Command: `gh pr view 397 --repo gsemet/chantier --json body,headRefOid` (headRefOid 7c1d8905...), compared with `git diff --stat origin/main...HEAD` (16 files).
- Renders: sections, table and fold are well formed; no image attached.
- Consistent: every Changes bullet matches a file in the diff (address.py, board_check.py, config.py, key.py, command.py, declare/board.py, cards and docs, tests, scenario); no delivered change unmentioned.
- Known gaps: the before side (source line only) and the Windows scenario gap are named; no UNVERIFIED or STALE mark remains.
- Review box: `log` holds "r1 approved at 18f2ac2..., committed as 7c1d890", which matches the box's 7c1d890.
- Role names: only "CR-426" in Internal references; none elsewhere.
Description: VERIFIED
