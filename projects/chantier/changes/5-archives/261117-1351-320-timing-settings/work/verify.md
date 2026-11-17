# Verify CR-320

Head: 17b1c6b16d65785004aac790ccfbbef89f938893

All claims judged at 17b1c6b (full SHA above).

1. Tests: `just test` in the worktree: `410 passed in 19.14s`. CI at the head (`gh pr checks 276`): five jobs pass, `just scenario (ubuntu-latest)` 3m32s included. The scenario's timing checks are in `scenario/run_scenario.py` (external_surface, stack_batch).
2. Defaults, no timing in the file: `chantier playbook` on a scratch repo prints `timing: Claude Code subagent: cache TTL 5 min, CI re-runs 1` and `timing: Claude Code session: steering wake 30 min, cache TTL 60 min`, no warning.
3. Labels and resolution: scratch `chantier.yaml` with `session: steering_wake: 20m, cache_ttl: 1h` prints `session: steering wake 20 min [surface project], cache TTL 60 min [surface project]`. With general `cache_ttl: 10m` plus `session: steering_wake: 20m`: `session: ... cache TTL 10 min [surface project]` (general beats shipped `session: 1h`) and `timing: Claude Code session: steering wake 20 min is above the cache TTL 10 min: each wake starts cold`.
4. Refusals, each with file:line (`chantier.yaml:<n>`): `driver_wake` -> `unknown key "driver_wake": one of steering_wake, cache_ttl, ci_reruns, subagent, session`; `gpt` under claude -> unknown key; `steering_wake` under subagent -> `is not read by the subagent column: set it under session, or as the general value`; `ci_reruns` under session -> `not read by the session column`; `61m` -> `at most 60 minutes on Claude Code: found "61m"`; `30s` -> `a duration of 1 minute or more`; `30` -> same; `ci_reruns: -1` and `1.5` under subagent -> `a whole number, 0 or more`; Copilot `90s` -> `whole minutes on Copilot (<n>m or <n>h): found "90s"`; `ci_reruns: 0` accepted, printed `CI re-runs 0 [surface project]`. Commands: `chantier --project <scratch> playbook` after writing each file.
5. Board Timing tab: screenshot at 1680 px from a scratch demo board at the head, `work/verifier/evidence/timing-tab-1680.png`, beside `final-config-1680.png`; see before-after.md. Matches the specification (read-only, two cards, per-column pills, "not used" cells, legend on the tabs' line, URL fragment `#timing` kept).
6. Late mark: `semantics.js` `heartbeat()` run in node with `steering_wake_min` 30: 20 min not late, 35 not late, 36 late; with 4 (Copilot): 9 not late, 10 late. `state.py`'s `steering_wake_min` takes the session column on Claude Code, the longest on Copilot.
7. Cards grep: `grep -rn "1800 seconds|every 30 minutes|/every 4m|has run since the last wake|driver_wake|one re-run" skills docs README.md` leaves only `claude-code.md:66` ("30 minutes, 1800 seconds, by default"), `copilot.md:43` (the whole-minutes row's proved `/every 4m`), `driver.md:267` and `driver.md:1039` (the remote command's and the Release driver's re-runs, kept by the specification): all sanctioned.
8. Review box: `Review: approved at 17b1c6b` in the description; the Driver's note was not read with `$CHANTIER log` in this pass (not checked: carried to the Driver's own record).
9. PR description (posted on the forge): renders, sections and fold present, no images. FAILS consistency: its Changes bullet lists `playbook/layers.py` among the changed files (and `config.py` fine), but `git diff HEAD~1 HEAD --stat -- '*layers.py'` shows only `tests/test_playbook_layers.py` changed; the reading and resolution are in `timing.py` and `timing_check.py` (its Autonomous decisions says so). Also its Test plan says `[ ] Evidence: none yet` and `Known gaps` says no screenshot of the Timing tab, which this pass now supplies in `work/verifier/evidence/`: the Driver updates both.

Unproved until a real batch (stated in Known gaps): the Foreman's `ScheduleWakeup` at a configured value, `/every` at a configured value, the idle stop with a short wake.

NOT VERIFIED (claim 9: the description lists `playbook/layers.py` as changed; it is not).

## Second pass: posted description only
Head: 17b1c6b16d65785004aac790ccfbbef89f938893

Everything else carried from 17b1c6b (same head). Claim 9 re-judged at 17b1c6b: `gh pr view 276 --json body` now lists `playbook/timing.py`, `playbook/timing_check.py`, `playbook/config.py` (all in `git diff --stat HEAD~1 HEAD`), no `layers.py`; Changes match the 32-file diff (cards, docs, board files, scenario, tests); Known gaps holds only the real-batch unproved items, no screenshot gap; two images, the Timing tab shows made-up paths (shop-api, no username or home folder; opened `work/verifier/evidence/timing-tab-1680.png`, the same capture). Review box `approved at 17b1c6b`: `$CHANTIER log CR-320` has "move 9bb941f..17b1c6b (conflict) inspector approved at 17b1c6b16d65..." . Test plan SHAs 17b1c6b (check, CI: `gh pr checks 276` five jobs pass), b888fc6 carried (scenario local, before the rebase), 9bb941f before. No STALE mark. Internal references only name work files.

VERIFIED

## Restack pass
Head: 8ab311466d66090dd81e56ad7d6b6351328dc998

Move 17b1c6b..8ab3114 (restack onto CR-319 b89e096; foreman.md, hosts/claude-code.md, hosts/copilot.md conflicts resolved). Judged at 8ab3114:

1. Tests: `just test` -> `422 passed in 27.17s`. No conflict markers in skills or docs (grep empty).
2. Defaults, labels, warning, refusals: probes on a scratch repo with `chantier --project <scratch> playbook`: no file -> `timing: Claude Code session: steering wake 30 min, cache TTL 60 min` and the subagent line; general `cache_ttl: 10m` + `session.steering_wake: 20m` -> `session: steering wake 20 min [surface project], cache TTL 10 min [surface project]` and `steering wake 20 min is above the cache TTL 10 min: each wake starts cold`; `61m` -> `chantier.yaml:5: ... at most 60 minutes on Claude Code: found "61m"`; `steering_wake` under subagent -> `chantier.yaml:5: ... is not read by the subagent column`. Other refusals (units, ci_reruns, Copilot minutes): carried from 17b1c6b, covered by test_playbook_timing.py (passes at the head).
3. Resolved card files: read `git diff HEAD~1 HEAD` of foreman.md, claude-code.md, copilot.md: the heartbeat follows the `timing:` line, the idle stop is 30 minutes with no Driver whatever the wake, host-table rows for cache TTL, wake bound and `/every` whole minutes present; consistent with each other. Cards grep for stale phrases leaves only sanctioned hits (claude-code.md:66 default, copilot.md:43, driver.md:267, driver.md:1039).
4. Board Timing tab, late mark, state.py: carried from 17b1c6b: the move did not change those files (board web files differ from CR-319's base only by the CR's own patch; screenshot taken at 17b1c6b is not re-taken, not re-checked at the new base, the restyle of CR-319 is under the tab).
5. Review: `$CHANTIER log CR-320`: "move 17b1c6b..8ab3114 (restack) inspector approved at 8ab311466d66..." .
6. CI at the head: `gh pr checks 276`: check macos and ubuntu, eval-dry-run pass; `just check (windows-latest)` and `just scenario (ubuntu-latest)` pending. The long gate is not yet green at the head.
7. PR description (posted): FAILS. It still names 17b1c6b / 9bb941f as head in the screenshot caption, "just check at 17b1c6b (410 passed)", "Review: approved at 17b1c6b", "CI green at 17b1c6b ... all five jobs pass"; the head is 8ab3114 (422 passed), CI is pending there. Those proofs must name 8ab3114 (or be carried with a reason) once true.

NOT VERIFIED

## Third pass: posted description and CI at the restacked head
Head: 8ab311466d66090dd81e56ad7d6b6351328dc998

Everything else carried from the restack pass (same head).

1. CI at 8ab3114: `gh pr checks 276`: all five jobs pass (check macos, ubuntu, windows; eval-dry-run; `just scenario (ubuntu-latest)` 2m50s). Judged.
2. Screenshot: `git diff --stat 17b1c6b 8ab3114 -- '*board/web*'` prints nothing, so the capture of `timing-tab-1680.png` (taken at 17b1c6b) still holds; carried.
3. PR description (posted, `gh pr view 276 --json body`): renders; Summary, Deliverables, Changes match the diff (timing.py, timing_check.py, config.py, cards, docs, board files, tests); Review box, evidence and CI lines name 8ab3114; `$CHANTIER log` holds the inspector's approval at 8ab3114 (restack pass). FAILS one proof: the Test plan says "`just check` at 8ab3114 (410 passed)"; I ran `just test` at 8ab3114 and got `422 passed in 27.17s` (restack pass), so the count is wrong at the head (410 was the count at 17b1c6b). Also the screenshot caption says "after (at 8ab3114)" while the capture is from 17b1c6b (unchanged board files, by git above): should read "carried from 17b1c6b".

NOT VERIFIED

## Fourth pass: posted description
Head: 8ab311466d66090dd81e56ad7d6b6351328dc998

Everything else carried from the third pass (same head). Re-judged at 8ab3114: `gh pr view 276 --json body` now says `just check at 8ab3114 (422 passed)` (matches `422 passed` of the restack pass) and the screenshot caption reads "captured at 17b1c6b, carried: no board file changed by the restack" (matches the empty `git diff --stat 17b1c6b 8ab3114 -- '*board/web*'`). Headline `headRefOid` is 8ab3114; `gh pr checks 276`: five jobs pass.

VERIFIED
