## Summary

In edit mode, clicking a card of a grid written in a list item whose marker is followed by a tab (`-<TAB>::::{grid} 2`, `1.<TAB>::::{grid} 2`), or whose cards are indented with a tab, opened the editor on the line above the card. The list-item prefix was only recognised when the marker was followed by spaces, so the blank line inside the grid was lost and every line was mapped one too early. The same fix covers a standalone card or a tab set behind such a marker, a nested item, and an item inside a quote.

## Deliverables

None beyond the fix; before and after, for a grid opened by `-<TAB>::::{grid} 2` then a blank line and cards indented by 4 spaces (opener on line 3):

| Case | Card line before | Card line after |
| --- | --- | --- |
| `-<TAB>` marker, blank line, cards indented 4 spaces or a tab | 4 | 5 |
| nested `  -<TAB>` item | 5 | 6 |
| `- ` marker with a tab-indented body | no card | 5 |

## Changes

- `src/core/render/mystGridToctree.ts`: a list level is a marker followed by spaces or tabs; its content column is measured in absolute columns (tab stops of 4, quote prefix included); following lines lose their leading whitespace up to that column, a tab crossing it becoming the spaces left.
- `test/core/render/gridCardTitleSourceLine.test.ts`: new rows (failing before the fix) and regression guards.
- Requirement `SwRS-MDOKFSTUDIO-BLOCK-258` boundary scenario and verification note amended; log and changelog updated.

## Impacts

No visual change: the editor opens on the clicked card line instead of the line above. Verified: the 12 new rows fail on the previous code and pass now (50/50 in the file, 531 render tests); the branch heavy CI run (integration, stress, visual, static) is green.

## Blast radius

Grade: 1. Local to the container-prefix stripping of grids in list items; a plain `git revert` restores the previous behaviour.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Requirements: SwRS updated or added, markers in code and tests, `just requirements-update`
- [x] Changelog: one user-facing line under `## Unreleased` in `CHANGELOG.md`
- [x] Local gates: `just ci-static` and `just ci-visual` pass locally (local ci-integration blocked by the screen lock; the heavy branch run is the proof)
- [x] Review
- [x] CI green

## Internal references

CR-321; follows CR-319 (list items with a space marker).
