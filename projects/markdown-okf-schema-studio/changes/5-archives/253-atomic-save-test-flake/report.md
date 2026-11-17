# Report: CR 253

Status: **closed, no change** (2026-11-03, branch `change-requests/253-atomic-save-test-flake`, no PR, no commit; head stayed at ac32bda4).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | None. The flake could not be reproduced, so per the owner decision ("if no flake cause is found after a focused repeat run, say so and stop: no change") nothing was changed. | — |

## Proof of completion

- Test: "a linked target replaced by a rename (atomic save) is reported, and dispose stops the events" in `test/node-services/linkedTargetWatch.test.ts`, covering `watchLinkedTargetDirectly` in `src/node-services/linkedTargetWatch.ts`.
- 200 runs (4 parallel loops of 50, with 12 busy-loop node processes adding CPU load on macOS): 0 failures.
- Code reading found no timing defect: the setup settle time can only cause a false pass, the rename wait allows 3 s, and the watcher is closed on dispose so no late event reaches the final assertion.
- No reviewer round (no diff) and no gates run (nothing to gate).

## Open items

- If the flake shows up again, capture the CI platform and the failing assertion message. The only candidate change then is a longer timeout in the test's `until` wait (an inotify event more than 3 s late on a heavily loaded Linux CI runner).
