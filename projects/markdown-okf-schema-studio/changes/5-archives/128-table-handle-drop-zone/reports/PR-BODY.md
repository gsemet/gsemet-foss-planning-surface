## Summary

Dragging a table row or column handle now works over the whole table and over the handle strips,
not only when the pointer sits exactly between two columns or rows. The drop marker follows the
pointer to the nearest gap (left or right half of a column, upper or lower half of a row),
releasing moves the column or row there, and releasing outside the table cancels the drag.
Works for pipe tables and `{list-table}`.

## Deliverables

- Drop zone covers every column/row and the handle strips; marker follows the pointer continuously
  and disappears when the pointer leaves the zone.
- Unit tests (fail on the old code) and real-window end-to-end scenarios for strip, mid-column,
  mid-row, outside the table and release-outside-cancels, for both table kinds.
- Requirements TABLE-002 and TABLE-007 updated; changelog entry.

Before (no marker over the column) and after (marker on the nearest gap), cream and dark themes:

| Before | After |
|---|---|
| ![before](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/212d1f5d8ebb0ccb77d4f96fa42ba61d4c9efc7e/before-pipe-cream-column-strip.png) | ![after](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/212d1f5d8ebb0ccb77d4f96fa42ba61d4c9efc7e/after-pipe-cream-column-strip.png) |
| ![before](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/212d1f5d8ebb0ccb77d4f96fa42ba61d4c9efc7e/before-pipe-dark-row-middle.png) | ![after](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/212d1f5d8ebb0ccb77d4f96fa42ba61d4c9efc7e/after-pipe-dark-row-middle.png) |


## Changes

- Table drag-and-drop drop-zone computation for row and column handles (pipe tables and `{list-table}`); unit tests, real-window scenarios, two requirements and the changelog.

## Impacts

Only drags of a row or column handle are affected.

## Blast radius

1 of 3: confined to table handle dragging.

## Autonomous decisions

- Follow the reported expected behaviour: nearest gap by half of the column or row, marker follows
  the pointer, release outside cancels.
- Extended the real-window table-moves test with drops over the handle strip and mid-column/row.

## Test plan

Unit tests and the real-window table-moves scenarios (see Deliverables). Notes:


- `just requirements-lint` could not run locally (installed okfreq too old for `--check-links`);
  `okfreq validate requirements` reports 0 errors. CI is the proof.

## Internal references

- CR 128: [00-request.md](../00-request.md), [review](../reviews/T1-r1.md)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
