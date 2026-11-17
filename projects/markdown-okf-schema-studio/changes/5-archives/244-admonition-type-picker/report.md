# Report: CR 244

Status: **done** (2026-11-03, branch `change-requests/244-admonition-type-picker`, PR [#298](https://github.com/gsemet/markdown-okf-schema-studio/pull/298), merged as ff7efe43 and ad62da9a, bottom of the final stack).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | With the caret on the type of a GFM alert or a MyST `:::{note}` / ```` ```{note} ```` admonition, a list of types with icons opens at the caret. GFM shows the five GFM types, MyST the admonition list. A pick replaces the type text only. Arrows move, Enter picks, Escape closes. The `@implements_req` markers for the picker sit in `editPalette.ts`, `editActions.ts` and `calloutIcons.ts`. | ff7efe43 |
| T1 round 3 | Four simulated `palette-slash` scenarios (GFM alert and MyST admonition pickers, light and dark) with screenshots in the PR body (owner decision). | ad62da9a |

Requirements: new SwRS PALETTE-269 (`proposed`; it was PALETTE-268 in the branch and was renumbered when it was stacked after CR 243), log entry, one CHANGELOG line.

## Proof of completion

- Five tests failed before the change because no list opened. `just check` passed, and the `palette-slash` visual group passed. Reviews: round 1 APPROVE with a missing-marker finding, round 2 APPROVE (markers added), round 3 APPROVE (3 of 3 rounds used). CI green. Real-window jobs not run.

## Open items

- The picker opens BELOW the caret, not above: the type sits on the head line, which is the first line under the edit bar, so there is no room above (the SwRS boundary row allows it). The log entry and the feature commit message still say "above the caret".
- The picker covers the body line, the hint row and part of the next paragraph.
- The MyST list is cut off at the bottom after Hint, though it stays inside the viewport.
- With the list open, ArrowLeft or ArrowRight inside the type word closes it and keeps it closed (probably unintended).
- Follow-up CR proposed: fix the MyST max-height and the arrow keys.
