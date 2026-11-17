# CR-326 Change Specification: fix the flaky real-window integration steps of the v1.9.0 release

✅ merged · batch-04 · [PR](https://github.com/gsemet/markdown-okf-schema-studio/pull/398)

**Now:** Merged: https://github.com/gsemet/markdown-okf-schema-studio/pull/398.
**Next:** Nothing.

## Progress

- [x] Shipped: https://github.com/gsemet/markdown-okf-schema-studio/pull/398
- [x] Handed back
- [x] Merged: https://github.com/gsemet/markdown-okf-schema-studio/pull/398

## Documents

- [request](intake/request.md)
- [intent](01-intent.md)
- [answers](02-answers.md)
- [specification](03-change-spec.md)
- [.agents/guidelines/ci.guidelines.md](../../../guidelines/ci.guidelines.md)
- [.agents/guidelines/git-commit-allowed-scopes.md](../../../guidelines/git-commit-allowed-scopes.md)

## Where

- Branch: `chantier/batch-04/cr-326-change-specification-fix-the-flaky-real-`
- Worktree: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio.worktrees/batch-04-CR-326`
- Driver: `-`

## Decisions and open questions

- Chief of Staff on A-10 (no proven user impact, routine round): option 2 first, one more round: replace the xdotool focus path by page.bringToFront() over CDP, re-run heavy and stress. If alert-dropdown is still red: option 1, file the focus bounce as a separate bug in the inbox with run 43576429177 and the timings, ship CR-326 with alert-dropdown kept out of the stress list (no test removed from integration), and send an ask: the owner decides whether the bug goes before v1.9.1.
- Chief of Staff on A-11: go for the Driver's round: toc's own failure diagnostics (workbench focus over CDP, window state, tab list), scenarioToc waits on a state check before its first click (no retry, no timeout raised), heavy run plus a reproducing loop of toc right after readme-html. Then ship. If toc is still red: file it as a separate inbox bug with the runs and diagnostics, ship CR-326 with toc unchanged in integration, and send an ask. No bug filing, no stress-list removal for alert-dropdown.

## Cost

$5.17.
