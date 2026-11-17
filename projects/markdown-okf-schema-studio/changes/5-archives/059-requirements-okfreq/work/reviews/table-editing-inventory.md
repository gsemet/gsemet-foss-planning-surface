Ids in this file predate the reduction; see `reduction/mapping.csv`.

# P10.1 critic review: table-editing

## Missing rows

Script: all 33 `table-editing` rows of `checklists/*.md` were grepped in the inventory; every id appears. 30 are cited in an F-TABLE line.
The other 3 are listed as moved and the target inventories do NOT cite them (checked by grep over
`inventory/*.md`; only `table-editing.md` mentions them):

- C-CL-058 (moved to gfm): `inventory/gfm.md` does not cite it.
- C-CL-097 (moved to rendering-core): `inventory/rendering-core.md` does not cite it.
- C-CL-100 (moved to layout-width or rendering-core): neither inventory cites it.

The inventory itself flags them as orphans, but until a target inventory cites them they are not handled.
Co-owned rows (C-AR-038, C-CL-063/064, C-CL-016, C-AR-047, C-AR-084, C-CL-090, C-CL-098) are cited in
the other scope too: fine. C-CL-061/085/086 are cited only here (block-editing claims the block halves
without ids): acceptable, they stay owned here.

## Missing behaviours

None of substance. Every function of `markdownTable.ts`, `tableEditActions.ts` and `tableCellEditor.ts`
is covered (only the two factory wrappers `createMarkdownTableTools` / `createTableEditActions` are not
named, they have no behaviour of their own). Error paths (F-TABLE-046, 052, 053), read-only (049), CRLF
(036, 040), undo (016, 028), IME (013, 019), stale/pointer-blur (020), flush (021) and 360 px (050) are all
present.

## Wrong/unverifiable evidence

Scripted check of 256 evidence tokens (`ALIAS:symbol`, `ALIAS:test title`, `src/...:symbol`) against the
refactored worktree: 0 missing. Manually read: visual ids v01..v05 and real-input ids r01..r08 exist in
`test/visual/scenarioIds.ts` and `test/shared/captureRegistry.ts`. The "four-action" stale wording claim
is confirmed in `scenarioIds.ts` (v02 to v05 descriptions). Coverage states checked: the 4 `untested`
rows (041, 050, 052, 053) have no test title in the evidence, consistent. Nothing false found.

## Count check

Table has 53 F-TABLE rows; tested 49 (24 unit + others) + untested 4 = 53; Undocumented counted by
script = 16, matching the list; Doc-only 0. Checklist "30 cited + 3 moved / 33" is arithmetically right,
but the 3 moved are not accepted by their targets (see Missing rows).

## Verdict

Real gap: 3 checklist rows (C-CL-058, C-CL-097, C-CL-100) are handled only on paper. Fixes:
1. gfm inventory: add C-CL-058 to F-GFM-001.
2. rendering-core inventory: cite C-CL-097 (RTL alignment).
3. layout-width (or rendering-core) inventory: cite C-CL-100 (overflow-wrap anywhere).
Alternative: keep these 3 as F-TABLE cell variants here (cite them in a row) and change the Counts to 33 / 33.

Verdict: REVISE

## Re-check

- Fixes: C-CL-097 cited in rendering-core F-CORE-034, C-CL-100 in layout-width F-LAYOUT-001 and rendering-core F-CORE-033/035; C-CL-058 (not cited by gfm) kept as F-TABLE-054 (cell variant), all verified by grep.
- Checklist: all 33 ids assigned to table-editing are cited in an `| F-TABLE` line or listed under Checklist corrections with a target citation.
- Evidence: 8 claims spot-checked in the worktree (isHandledEditorKey, installEditorKeyContainment, isTextSelectAll, cellSafeEdit, escapeCellPipes, insertTable, paletteShortcut, hideTableCellContent, autolinkBareUrls and its test title): all exist.
- Counts: 54 F-rows, 50 tested + 4 untested, 16 undocumented (listed ids match the grep), 31 cited + 2 moved / 33: all match.

Re-check verdict: APPROVE
