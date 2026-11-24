# Verify CR-484

Head: f98043379922b2d4d3776f38880fb20a60b092d8

All claims judged at f980433.

1. Bind, double start, stray stop, watcher confirmation and relink, status line: `uv run --no-sync --project . pytest tests/test_board_claim.py tests/test_watch_confirm.py tests/test_serve_webui.py tests/test_watch_board.py -q` run in the worktree: `71 passed in 6.28s`. The tests exist (test_board_claim.py: join on lost claim, refusal at the bound, claim held for life, stray stops and leaves the entry alone; test_watch_confirm.py: foreign link ends naming both PIDs, restart relinks from cursor, start line, status line; test_serve_webui.py: real-socket held-on-any-address, parametrized 0.0.0.0/127.0.0.1 both ways).
   VERIFIED
2. Scenario step `one_board` (one process serves, hub not idle, merge journalled and told, same watcher told next merge once after `serve --restart`): gate log `work/gates/20261125-001836.log`, first line names CR-484 and head f980433..., last line `result: pass at f98043379922b2d4d3776f38880fb20a60b092d8`; `one_board` is registered in scenario/run_scenario.py (line 2988, 11997).
   VERIFIED
3. CI: `gh pr view 462 --json headRefOid,statusCheckRollup` gives head f980433... and conclusions `["SUCCESS"]`.
   VERIFIED
4. Status line: `hub/lines.py` `unsubscribed()` prints one line when the watcher runs and the hub is idle, absent or not the recorded PID (read in the diff; covered by item 1).
   VERIFIED
5. AGENTS.md: the surface-server, hub and watcher sentences say the one-process rule, any-address hold, stray stop and watcher confirmation; no new lock file (reuses `hub.lock`, named). Note: the inserted clause sits before the old "and prints it (remote-cli-Q17)", so "prints it" now reads as attached to the stray's stop; the meaning is recoverable but the sentence is awkward (not a failure).
   VERIFIED
6. PR description: Summary, Deliverables and Changes match the diff (24 files; binding, claim, command, start_lines, watcher files, lines, AGENTS.md, chief-of-staff card, scenario). Known gaps names the macOS bind proof and status not probing for two servers. Test plan still holds `<to fill>` placeholders, which the Driver fills at handoff. Live evidence quoted from the specification. No images.
   VERIFIED
7. Not run by me: the bind test on macOS and Windows (CI's `just check` matrix is green, item 3); the "fails on today's code" proof was not re-run on the base.

VERIFIED
