## Summary

The real-window diff preview scroll test (step D1) timed out intermittently on `main` and in heavy runs ("Timed out waiting for the inline diff's editor to scroll"). The test scrolled a possibly stale editor object with a fire-and-forget reveal and left no diagnostics. This makes the step wait on the live diff editor and scroll it with an awaited command, so a failure explains itself.

## Deliverables

None (test-only change).

## Changes

- `test/integration/diffPreviewScroll.test.ts`: pick the live editor of the active diff tab (a new `a.md` editor, not one open before the diff), scroll it with the awaited `revealLine` command (D1 and the D2 loop); the scroll wait's timeout message reports editors, active editor, tabs, layout, preview scroll state and the highest first visible line seen.
- `test/shared/stressPlan.ts`, `test/integration/realInput/run.ts`, `test/build/stressPlan.test.ts`: `diff-preview-scroll` is an on-demand stress scenario (`-f stress_scenarios=diff-preview-scroll`).

## Impacts

No visual change; no change to the extension.

## Blast radius

Grade: 1. Test code only; a plain `git revert` restores the previous test.

## Test plan

- [ ] New or changed tests (the failure is an intermittent race: the proof is the repeated heavy runs and the stress scenario, not a local red then green)
- [ ] Requirements: No behaviour change
- [ ] Changelog: No user-facing change
- [ ] Local gates: `just check` pass, `just requirements-update` 0 changes
- [ ] Review
- [ ] CI green (heavy runs, stress on `diff-preview-scroll`)
