# CR-328 Change Specification: the edit toggle loses its clicks right after a preview opens (toc, myst-blocks)

✅ merged · batch-04 · [PR](https://github.com/gsemet/markdown-okf-schema-studio/pull/402)

**Now:** Merged: https://github.com/gsemet/markdown-okf-schema-studio/pull/402.
**Next:** Nothing.

## Progress

- [x] Round 1: Phase A: diagnostics and loop knobs (spec commits 1 and 2), no fix yet
- [x] Note: Phase A pushed (611f6b74). Adjacency loop run 43595436167: 39/40 clean, round 7 toc failed, 3 clicks reached the workbench document (workbench counters 4..7) and none the host frame or content frame while hit test said the webview iframe; side bar hidden. Control loop (side bar closed first) run 43595438463: 40/40 green. Side-bar lead confirmed; proceeding to fix.
- [x] Round 2: Phase B: the fix (spec Decision 3) and stress list (Decision 5)
- [x] Long gate fail: 0a154127
- [x] Shipped: https://github.com/gsemet/markdown-okf-schema-studio/pull/402
- [x] Blocked: question: owner decision on user impact before ready: in the failing round (run 43595436167, round 7, toc) 3 real clicks reached the workbench document (counters 4..7), none the webview host or content frame, while VS Code reported the window focused and hit test said webview. Likely test-host effect (CDP viewport emulation, no window manager) but not proved. PR 402 draft, fix proven green
- [x] Shipped: https://github.com/gsemet/markdown-okf-schema-studio/pull/402
- [x] Handed back
- [x] Shipped: https://github.com/gsemet/markdown-okf-schema-studio/pull/402
- [x] Merged: https://github.com/gsemet/markdown-okf-schema-studio/pull/402

## Documents

- [intent](01-intent.md)
- [answers](02-answers.md)
- [specification](03-change-spec.md)
- [pr-body](work/pr-body.md)
- [long gate log](work/gates/20261114-135416.log)
- [.agents/guidelines/ci.guidelines.md](../../../guidelines/ci.guidelines.md)
- [.agents/guidelines/git-commit-allowed-scopes.md](../../../guidelines/git-commit-allowed-scopes.md)

## Where

- Branch: `chantier/batch-04/cr-328-change-specification-the-edit-toggle-los`
- Worktree: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio.worktrees/batch-04-CR-328`
- Driver: `-`

## Decisions and open questions

- Phase A pushed (611f6b74). Adjacency loop run 43595436167: 39/40 clean, round 7 toc failed, 3 clicks reached the workbench document (workbench counters 4..7) and none the host frame or content frame while hit test said the webview iframe; side bar hidden. Control loop (side bar closed first) run 43595438463: 40/40 green. Side-bar lead confirmed; proceeding to fix.
- Owner, verbatim: « Test env only ». The lost clicks in the failing round are treated as a test-host effect (Xvfb with no window manager, side bar layout still moving), not a user-visible bug: rebase on main, mark PR #402 ready, the owner merges by rebase. No page-side mitigation, no upstream report. Also file an inbox ticket for the one-off incoming-changes stress flake (frame.waitForFunction 30 s, round 2).
- back to a Driver: Owner: « Test env only ». Treat lost clicks as test-host effect, no page-side mitigation, no upstream report. Rebase PR 402 on main (force-with-lease on its own branch), wait for CI green on the exact head (branch heavy run), mark PR ready (not draft, never auto-merge), then hand back. Do not touch the incoming-changes flake (CoS files the ticket).

## Cost

$5.01.
