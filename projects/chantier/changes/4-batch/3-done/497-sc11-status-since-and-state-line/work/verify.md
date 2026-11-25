# Verify CR-497 (SC11 + SC12 + SC13)

Head: 6bbfcc78b90c3ba149a7256748703fd2ae50c443

All claims judged at 6bbfcc78 unless noted. Code run from the worktree's own `.venv` (`uv run --no-sync --project <worktree>`), not the main checkout.

1. Tests of the three parts at head (6bbfcc78): `pytest tests/test_status_since.py tests/test_watch_state_line.py tests/test_next_advice.py tests/test_msg_steering.py tests/test_watch_foreman.py tests/test_scenario_coverage.py tests/test_event_types.py tests/test_event_audience.py` -> `171 passed in 48.87s`.
2. `status --since` (6bbfcc78), read-only probe on the live batch-31 record: `status --since 0 --batch batch-31` first line `state: batch-31 running e1 | working 1, queued 9, merged 33, cancelled 9 | slots 1/4 | due 1`; `merged: 33 (33 since 0)`; `cancelled: 9 (9 since 0)`; last line `since 0, now 2221: next time `status --since 2221``. `--since -1` -> `error: status --since -1: a sequence is 0 or more; ...`; `--since 99999` -> `error: status --since 99999: batch-31's events stop at 2221; ...`.
3. `next` read-only (6bbfcc78): `next --epoch 1` printed `due: CR-497: lease not confirmed ... take CR-497 --reclaim ...`; `next CR-500` printed `next: A Driver starts it.`; `next --epoch 1 --lease 1` exit 2 `next: --lease is a Driver's, --epoch the steering session's; give one`; plain `next` printed asks/ready/watch lines. sha1sum of batch.json and events.jsonl identical before and after all runs (ddb53f37..., 1e6a523e...).
4. `msg`: `msg steering bogus x ...` -> argparse `invalid choice: 'bogus' (choose from 'anomaly', 'blocked', 'note')`. Delivery, wake, no-subscriber, refusals and `inbox` read marks: covered by test_msg_steering.py in claim 1 (not sent against the live journal).
5. CI at 6bbfcc78 (gh pr view 482): just check x3 OS, just scenario (ubuntu), just eval-dry-run all SUCCESS; head matches. Round 4 delta 5d969826..6bbfcc78 is scenario/run_scenario.py only (git diff --stat), so the code claims carry from 5d96982 (src and tests unchanged).
6. Review box `approved at 5d96982`: `chantier log CR-497` has "body re-inspection approved at 5d9698265e..." and part notes at e8278a9, 7f5f944. Matches.
7. PR description (fetched with gh pr view 482): renders, sections present, Summary/Deliverables/Changes match the diff stat (43 files; commands, schemas, watcher, docs, scenario, AGENTS.md). Known gaps lists the --since sequence-only choice, SC13 scenario steps proven by ubuntu job only, and no Windows run. FAILS: the Test plan states proofs at `5d96982` ("Local gates at `5d96982`: just check passed (2825 passed...)", "Verified at `5d96982`", "CI green at `5d96982`") and none is the head (6bbfcc78) nor carried with a reason after round 4's commit.

Not run: screenshots (none owed; no board pane change); Windows long gate (not owed, CR is not the stack's top).

NOT VERIFIED (description only: stale SHAs in the Test plan; the code behaves as the spec says at this head).

## Pass 2 (description re-read, 6bbfcc78)

Head: 6bbfcc78b90c3ba149a7256748703fd2ae50c443

- Test plan proofs now name 6bbfcc7 with round 4 noted: fixed.
- FAILS: the Review box says `Review: approved at 6bbfcc7 ... round 4 (scenario fix) at 6bbfcc7`. `chantier log CR-497 --batch batch-31` holds no Driver note of an approved pass at 6bbfcc7 (latest approval note: "body re-inspection approved at 5d9698265e..."; the only later entry is the NOT VERIFIED verdict). No note, so the box is unproved.

NOT VERIFIED (description: Review box has no matching note). Record the round 4 review note (or cite 5d96982 as the box's SHA) and ask again.

## Pass 3 (6bbfcc78)

Head: 6bbfcc78b90c3ba149a7256748703fd2ae50c443

- Review box `approved at 6bbfcc7`: `chantier log CR-497 --batch batch-31` holds "2026-11-25T10:59:08Z driver note r4 inspector approved at the uncommitted tree, committed as 6bbfcc78 (scenario/run_scenario.py only)". Matches.
- Test plan SHAs read 6bbfcc7 with round 4 noted (gh pr view 482). Code claims 1 to 5 above carry (head unchanged: `git rev-parse HEAD` = 6bbfcc78).

VERIFIED
