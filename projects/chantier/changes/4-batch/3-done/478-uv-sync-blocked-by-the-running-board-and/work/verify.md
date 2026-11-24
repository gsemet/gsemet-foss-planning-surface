Head: 29162b76e022b8fbd762841a58ff5bcc4243eaa3

Verdict: VERIFIED (description re-judged at 29162b76: the posted body now lists address.py, watch_reads.py, orders_apply.py, CONTRIBUTING.md, scenario/README.md; `gh pr view 456` body matches pr-body.md)

Claims, each judged at 29162b76:

1. Long gate pass at the head: work/gates/20261124-173926.log first line `gate CR-478 ... head 29162b76e022b8fbd762841a58ff5bcc4243eaa3`, last line `result: pass at 29162b76e022b8fbd762841a58ff5bcc4243eaa3`. Holds.
2. Tests: `pytest test_board_restart.py test_launch_modes.py test_server_api_calls.py test_server_protocol.py test_start_reading.py -q` -> `49 passed in 56.09s`. They cover server.stop (public key, running command, private key), restart refusals, guard, watcher under guard, seat build in dev/plugin mode, cards. Holds.
3. Cards and hosts: `grep "never stop or restart the board" skills AGENTS.md` -> only the test's negative assertion; both hosts' "Run the board" rows name `serve --restart --seat <id>`. Holds.
4. New op/flag absent at base, present at head: protocol.json `server.stop` count 0 (origin/main c155c897) vs 1; serve.py `restart` 0 vs 2. Holds.
5. Review box: log `r2 approved at 34a3034, committed as 29162b7` matches the head. Holds.
6. PR description, consistency with the diff: fixed, holds at 29162b76 (earlier failure: omitted files, now listed). Changes lists no entry for `board/address.py` (new `call_op`, timeout parameter), `hub/watch_reads.py` (new `checked`, moved from watch.py), `commands/orders_apply.py` (unused import removed), `CONTRIBUTING.md` and `scenario/README.md`, all in the diff `origin/main...HEAD`. "No delivered change unmentioned" is not met.
7. Description: Known gaps names the unrun whole scenario unit; no image; mermaid renders as plain block. Otherwise clean.

Not run by me: a live `serve --restart` (the auto-mode classifier refused a hand run; the long gate's scenario unit 16d at this head covers it).

Fix: list the unmentioned files in Changes, then a new pass.
