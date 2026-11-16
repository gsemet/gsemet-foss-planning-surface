# Batch-17 retro: card fixes

Filed 2026-11-14 by the Chief of Staff, on the user's word (ID-Q1, A): the batch-17 retro's
card-only points, drafts 1, 2, 8, 9, 11, 12, 13, 14 and 15 of
`.agents/changes/batch-17-issue-drafts.md` (read it for each point's evidence and fix). Card and
doc text only; no CLI code.

1. Drivers and conflict resolvers run every git command as `git -C <worktree>`; the main checkout
   is read-only except the post-merge fast-forward.
2. The stack-driver plans one restack pass right after each native stack merge, siblings pushed
   at once.
8. Tests and smoke runs of the board's write paths use a scratch planning folder, never the live
   record.
9. `.git/info/exclude` is out of bounds for a Driver.
11. The Inspector reviews the round's last commit.
12. The Foreman's Driver brief always carries the Foreman's address.
13. The spec critic flags a spec that bundles a refactor with a lint or type cleanup, or several
    views, and the grill splits it.
14. The `stack-ready-to-merge` line carries each CR's open gaps; the Chief of Staff applies the
    gap and pane-screenshot rule to it before it offers the stack for merge.
15. The Chief of Staff runs `asks --read A-<k>` in the turn it relays an ask or orders on it.
