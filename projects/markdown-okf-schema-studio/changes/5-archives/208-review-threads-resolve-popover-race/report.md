# Report: CR 208

PR [#234](https://github.com/gsemet/markdown-okf-schema-studio/pull/234), merged commit 5ebd3b2f. Landed 2026-10-31 in stack #230 → #234 (gh stack 235, rebase merge by the user, main 5ebd3b2f). Top heavy run 41151371662 on tree abe65ccbb2525d9e48e5aacc2778aff79e7f270a: attempt 1 red only on the known alert-dropdown flake (stress round 7/20), `--failed` green. Final Opus Inspector on the whole stack: APPROVE (nits in P3 stack-230-234-followups).

- Hardening: `readSidecar` returns UNREADABLE for any error except not-found, so a failed read posts nothing instead of an empty thread list.
- The product race is NOT proven fixed (its likely cause, the rename gap, was already fixed by 5f0f3be0). The post-hash ordering part is covered by #202. Backlog item P2 review-threads-resolve-popover-race stays open.

## Backlog item (archived 2026-10-31)

The backlog item `review-threads-resolve-popover-race` is kept in [backlog-item/](backlog-item/). Hardening merged; likely fixed by 5f0f3be0; on watch in stress (owner, 2026-10-31). Earlier CR 174 on the same race is not archived again.
