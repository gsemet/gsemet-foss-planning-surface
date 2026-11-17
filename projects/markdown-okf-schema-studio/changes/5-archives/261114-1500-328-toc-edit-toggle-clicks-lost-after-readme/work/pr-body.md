## Summary

In the real-window integration run, the first click on the edit toggle was sometimes lost right after a preview opened: three real clicks in a row never reached the page, so the step failed with "Edit mode did not switch to on". It showed in the `toc` step after `readme-html` and once more in `myst-blocks` after `toc`. What the runs prove is the adjacency: these three steps reopen the side bar in their cleanup, so the next step starts with it open and focused, then closes it and maximizes the group after its preview has opened. With the side bar closed before each step the loop never failed (40 of 40 rounds). That the first click met a layout that was still moving is inferred from this control, not measured: the group box was not readable in the failing round (the probe's group lookup was wrong, fixed here).

The owner reviewed the failing round and decided it is an effect of the test host only (Xvfb without a window manager, a side bar layout still moving under the emulated viewport), not a user-visible bug. No page-side mitigation and no upstream report. The fix is test-only.

## Deliverables

The failing round, as the new diagnostics record it (adjacency loop, 40 rounds of `readme-html`, `toc`, `myst-blocks`; round 7 failed in `toc`):

| Where the click was counted | pointerdown / mousedown / click |
|---|---|
| Workbench document | 4, 5, 6, 7 (grows with each of the 3 clicks) |
| Webview host frame | 0 |
| Webview content frame | 0 |

At the same moment the hit test said the click point was on the webview iframe, the side bar was hidden and the window was focused. The clicks went to the workbench, not into the webview. The control loop (side bar closed before each step) ran 40 of 40 rounds green.

## Changes

- The three steps (`readme-html`, `toc`, `myst-blocks`) read the side bar state from the workbench, close it before their preview opens, and restore the state they found, never a blind toggle.
- Before the first click they wait for the webview box to equal its editor group box, then for the window to be ready for a click (`myst-blocks` and `readme-html` now do the latter as `toc` did).
- Failures of the edit-toggle click now carry where the click was counted (workbench, host frame, content frame), the iframe and group boxes, the side bar state and the focused part.
- The `toc-loop` repro job takes a list of steps (`toc_steps`) and a side bar control (`toc_control`); its launch deadline is computed from the rounds and steps. The CI guideline paragraph is updated.
- `readme-html` and `myst-blocks` join `toc` in the stress scenarios. `myst-blocks` puts the viewport back to 1400x900 when it ends: it left 1400x1000, and the scenario `incoming-changes` then failed in the stress run (a seven-scenario stress run reproduced it before and passed after).

## Impacts

Test and CI only; no change to the extension. The real-window steps no longer depend on the side bar state of the previous step.

## Blast radius

Grade: **1**. Tests, the repro job and a guideline paragraph; a plain revert restores the previous behaviour.

## Test plan

- [x] New or changed tests (they fail on the previous code): the adjacency loop reproduced the loss on the previous code (1 of 40); unit tests cover the new loop settings and the computed deadline
- [x] Requirements: No behaviour change
- [x] Changelog: No user-facing change
- [ ] Local gates: `just check`, workflow tests (74), `just requirements-update`; `just preflight` fails locally on macOS in visual, untrusted-suite and gallery stages (same as another change on its own head), CI passes them
- [ ] Review
- [x] CI green: on the final head the adjacency loop passed 40 of 40 rounds and `integration` passed. The default `stress` job (advisory) failed on `palette`, the known unrelated flake, on the run and on its one re-run; `incoming-changes` and the three steps of this change passed in it. The scoped stress of `readme-html`, `toc` and `myst-blocks` passed 60 rounds on the earlier head.

## Internal references

Chantier CR-328.
