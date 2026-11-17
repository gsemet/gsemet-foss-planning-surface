# A grid inside a list item maps its cards one line too early

Type: fix. Filed 2026-11-12 by the coder of CR-308; grilled 2026-11-13 by the Chief of Staff.

## Owner's words

> grillons les tous de suite

## Problem

A `{grid}` opened on a list item line (`- ::::{grid} 2`), followed by a blank line and indented
cards, maps each card, its title and its body one source line too early: a click in edit mode opens
the block editor on the line above the clicked card. Same symptom as the quoted grid fixed by
CR-308 (PR #378).

## Cause (read at `main`)

`directiveBody` in `src/core/render/mystGridToctree.ts` cuts a directive's body from the source
lines only when the opener passes `FENCE_LINE` (`^[ \t]*(fence)`). The opener line carries the list
marker (`- `, `* `, `1. `), so the test fails and the body falls back to the parser's `node.value`,
which lost the blank first line, while `firstLine` still assumes the body starts right after the
opener.

## Scope

- `directiveBody` also recognises an opener behind a list-item marker (bullet or ordered, any
  indentation), and strips the item's content indentation from the body lines, so the nested
  `bodySource` sees plain lines as in the unquoted case.
- The quote case of CR-308 and the `node.value` fallback keep working.
- A render-level test, written first and failing on `main`, in
  `test/core/render/gridCardTitleSourceLine.test.ts`: card, title and body lines for a grid in a
  bullet item and in an ordered item, with and without the blank first line.
- SwRS-MDOKFSTUDIO-BLOCK-258 (already carries the quoted case) gains the list-item case.
- No visible change other than the edit target: rendering is the same.
