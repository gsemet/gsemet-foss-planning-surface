Head: 589c77c8bc5ac4639af1ac1a38c16d5fd62eca45

1. isIsoDate refuses non-existent days, accepts real ones (589c77c8). `git diff origin/main -- src` shows isRealCalendarDay (leap rule, month table, day 1..max) added to isIsoDate.
2. Test passes at head (589c77c8): `npx tsx --test test/core/comments/commentModel.holes.test.ts` -> pass 7, fail 0. Good set includes 2024-02-29, 2000-02-29; bad set includes 2026-02-30, 2026-02-29, 1900-02-29, 2026-04-31, month 00, day 00.
3. Same test fails on the base (detached worktree at 7aa1e9b4, new test file copied in): `ℹ pass 6 / ℹ fail 1`, `AssertionError: 2026-02-30T10:00:00Z`. Base worktree removed.
4. Gate pass at head: gate log 20261121-203721.log first line `gate CR-459 ... head 589c77c8bc5ac4639af1ac1a38c16d5fd62eca45`, last line `result: pass at 589c77c8...` (ci-static passed).
5. PR description (pr-body.md, equal in start to the posted body of PR 469, head 589c77c8 per gh): matches the diff (src, test, SwRS-REVIEW-004, tiers/log.md); no unproven claim; Review box: log note "r1 approved at 7aa1e9b, committed as 589c77c8" covers it. "CI green" is unchecked, honest. Known gaps: none needed (no UNVERIFIED claim). No UI, no images.

VERIFIED
