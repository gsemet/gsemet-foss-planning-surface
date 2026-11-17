# Report — ci-flaky-tests (F1, F2, F3)

Status: **done** (2026-10-22, branch `fix/ci-flaky-tests`, PR #13, merged as 11895ad..bb88aab).

## Delivered

| Task | Change | Commit (main) |
| --- | --- | --- |
| T1 F1 | Visual settle reads wait for fonts + two frames | `11895ad` |
| T1 F2/F3 | Saving a linked target refreshes its excerpt; unlock remembers TabGroups (no stale column focus) | `f8d315d` |
| T1 F1 | Leading properties table re-measured on its own resize, load/fonts.ready, trailing update after the burst limiter | `4eb52a6` |
| T1 F1 | Toolbar-overlap failure dumps the layout for CI diagnosis | `bb88aab` |

## Proof of completion

- F1 root cause from CI artifacts: read-state inset 0 instead of 84 (never re-measured). Product bug.
- Unit tests: groupFocus (3), firstClearance (+3), all failing on the old code; unit 1706+ green.
- Reviews: r1 FIX (F2 coverage, save scope), r2 APPROVE, r3 APPROVE (+ diagnostic requested).
- CI: run 39799596510 green on attempt 1 and attempt 3 (attempt 2 failed on setup-just infra only).

## Open items

- setup-just "no release for just matching version specifier" infra flake → pinned in PR #15.
- If F1 flakes again, the capture.py diagnostic dump names the moving input.
