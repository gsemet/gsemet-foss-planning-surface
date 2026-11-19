# Verify CR-384

Head: 7a87cfc25b6ac41a99ed50b7872bf7651c77816e

All claims judged at 7a87cfc (first verifier). Scratch project under work/scratch (own git repo, removed at the end); board routes called in-process with the scratch repo as working folder.

1. Board backlog writes append `board` lines to the project's forge journal, refusal none, label wakes=false (7a87cfc).
   Command: `uv run ... python work/verifier/probe.py` in scratch repo, then `cat .agents/changes/forge-journal.jsonl`.
   Output: new 200, move 200, unknown-item move 409, label 200; journal has seq 1 new wakes:true, seq 2 move wakes:true, seq 3 label wakes:false; no line for the 409.
2. Pull path (7a87cfc): `chantier watch --once --after 0` printed the three `board wrote (...)` lines and `watch: cursor 3; next, at the user's next message: ... watch --once --after 3`.
3. Watcher runs with no batch, ends with the `(no batch) still running` line (7a87cfc): `CHANTIER_HUB_TEST_TIMES=1:4 CLAUDE_CODE_SESSION_ID=sessA chantier watch --after 1` printed the two later board lines then `watch: p (no batch) still running: ... watch --after 3`. Before (9c3fb6d, base sources): `error: watch: no running batch in p: nothing to watch`.
4. `seat take` prints `watch: not running` with the `after the user's no ... watch --once` clause (7a87cfc): output captured in evidence/before-after.md section 4.
5. Tests at 7a87cfc: `pytest tests/test_watch_events.py tests/test_board_journal.py tests/test_board_config.py tests/test_watcher_autostart.py tests/test_forge_hub.py tests/test_limits.py` -> `109 passed in 25.01s`; the verbose run of the first three -> `34 passed`, covering the 20 s end rule (9 cases), seat end by another session (6), `--once` takes no lock, other project gets no line, config line per changed key (agent, model, slots, parallel), dry run none, board-version tail (test_forge_hub.py:262 "restart it").
6. CI at 7a87cfc (`gh pr view 351 statusCheckRollup`): check x3, scenario ubuntu, eval-dry-run all SUCCESS.
7. Review box: `log` shows "r3 inspector approved at 5bf8754d" and "r3 approved at 5bf8754, committed as 7a87cfc2"; the description's Review line is an unfilled `<sha7>` placeholder in the Test plan, to be filled by the Driver with the SHA of those notes.
8. PR description (as posted, read with `gh pr view 351`): identical to work/pr-body.md apart from a trailing blank line; Summary, Deliverables (mermaid, tables) and Changes match the diff stat (hub/journal.py, write_api.py, config_api.py, watch.py, seat/status, cards, docs, tests, scenario); no image attached; the Known gaps names the two unproved items; the spec-deviation on identical saves is the spec's own "a key left at its effective value writes none" and is in Autonomous decisions. Test plan boxes carry `<sha7>` placeholders (unfilled, unticked: pending, not asserted).
9. Not capturable (stay in Known gaps): real main session wake, orphaned watcher end, Copilot wake; a live Configuration PUT by hand (needs a planning surface; proved by item 5) and a live seat-take ending a running watcher (needs two processes; proved by item 5). See work/verifier/evidence/before-after.md.

VERIFIED

## Description pass at 7a87cfc25b6ac41a99ed50b7872bf7651c77816e
Command: `gh pr view 351`, `gh pr checks 351`, compared with verifier/evidence/before-after.md.
- Before/after in Deliverables names 9c3fb6d and 7a87cfc and matches before-after.md. Role names are product terms (cards changed). CR-384/375/383 only in Internal references. UNVERIFIED claim has its Known gaps bullet. CI 5 jobs pass. Test plan boxes match. Description verdict: VERIFIED.

## Description pass 2 at 7a87cfc25b6ac41a99ed50b7872bf7651c77816e
Command: `gh pr view 351 --json body,headRefOid` (headRefOid 7a87cfc2...), `$CHANTIER log CR-384`, `git log --stat -3`.
- Only change since the last pass: Test plan "Local gates" line says `just eval-dry-run` pass (17 of 17), run before the last test-only commit, at the rebased head with the same patch. True: log note 06:46:42Z "just eval-dry-run: pass (17 of 17, run at the patch-identical rebased head 876197d9)"; the later commit 7a87cfc2 touches only tests/conftest.py and tests/test_cli_runs.py (2 insertions), and `just check` passed after it (note 06:52:10Z). No SHA named that is outside history. Rest of the description carried from the pass above (unchanged). Description verdict: VERIFIED.

VERIFIED
