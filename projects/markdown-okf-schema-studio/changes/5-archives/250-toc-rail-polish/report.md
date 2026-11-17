# Report: CR 250

Status: **done** (2026-11-03, branch `change-requests/250-toc-rail-polish`, PR [#294](https://github.com/gsemet/markdown-okf-schema-studio/pull/294), merged as 4560c504, bottom of stack #296).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | The narrow-pane TOC rail is polished: the content is padded for the 16 px rail, the overlay starts 40 px lower to clear the toolbar tooltip at 460 px, and Escape closes the overlay only when the key was not already consumed and comes from the overlay, the rail or the body. Scenarios v28 and v29 are renamed `v28-toc-rail-light-460` and `v29-toc-rail-dark-460`; the TOC checks moved out of `capture_layout_checks.py` into `capture_toc_checks.py` (1499 to about 1247 lines, no check dropped). | 4560c504 |

Requirements: new SwRS TOOLBAR-133 (`proposed`); TOOLBAR-037, 033, 040, 045 and StRS-006 updated; log entry and CHANGELOG line.

## Proof of completion

- Round 1: FIX-REQUIRED (the v28/v29 lock texts still said the content is not narrowed; the Escape test lacked its `@tests_req` for TOOLBAR-133). Round 2: both fixed, APPROVE (2 of 3 rounds).
- `just check` exit 0 in both rounds; simulated `toolbar-navigation` 40 scenarios passed (one flaky v31 passed on rerun). CI green on the rebased head. Real-window jobs not run (manual).
- No screenshots: the scenario run produced none; the PR body listed this as a follow-up.

## Open items

- The 40 px offset is sized for one-line tooltips; a long wrapped tooltip could still reach the overlay.
- Escape typed in the text no longer closes a pointer-opened overlay (by design: scoped to the overlay).
