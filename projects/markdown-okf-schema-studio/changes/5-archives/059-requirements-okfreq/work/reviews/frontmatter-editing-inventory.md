Ids in this file predate the reduction; see `reduction/mapping.csv`.

# Critic review: frontmatter-editing inventory (P10.1)

Reviewer: Sonnet critic, 2026-10-24. Checked `inventory/frontmatter-editing.md` against the 27
checklist rows with scope `frontmatter-editing`, `scope-map.json` and the code of
`markdown-okf-schema-studio-wt-059`.

## Missing rows

All 27 rows of the scope appear in the inventory (script: scope column of `checklists/*.md`, grep
of each C- id). Two are moved out and the move is not honoured by the target:

- C-AR-018 is moved to `layout-width`; `inventory/layout-width.md` does not cite it.
- C-CL-018 is moved to `gfm`; `inventory/gfm.md` does not cite it.

Until the target inventories cite them (or the checklist scope column is changed), both rows are
unhandled. Fix: add both to the target inventories, or re-scope the rows in the checklists.

## Missing behaviours

1. Flush of an open field or key editor before a navigation (no inventory mentions
   `flushFrontmatterEditor` or `flushingEditors`; `grep flush` finds nothing in this inventory):
   `src/page/features/frontmatterEditor.ts` (`flushFrontmatterEditor`, `state.flushingEditors`,
   key trimmed, empty key keeps the old one), `frontmatterValueEditor.ts` (typed number text kept
   as is), `src/core/edits/frontmatterEdit.ts:planFrontmatterSave` (`flush: true` skips the type
   check, accepts invalid YAML as typed, `needsSchemaCheck` false),
   `FrontmatterController.postEditError` (a refused flush shows a host warning via
   `flushRefusalMessage`). Tests exist (`test/core/edits/frontmatterEdit.test.ts`: "invalid YAML is
   refused unless the save is a flush"). Substantive: it is a data-loss guard.
2. `plainSavePending` (a refused plain save, Enter or blur, is saved again as a flush when a
   navigation waits for it, `frontmatterEditor.ts` l.242 and 337, `frontmatterValueEditor.ts`
   l.200).
3. Session-side refusals of `FrontmatterController.handleSave`: stale document or revision
   (`currentPreviewDocument` gives `FRONTMATTER_STALE`), and the schema check of the candidate
   (`checkFrontmatterCandidate`: "Schema validation failed: ...", "The renamed frontmatter field
   could not be validated.", "Cannot remove required frontmatter field") are partly present in the
   table text but the flush exception (`needsSchemaCheck: schemaFound && !flushed`) and
   `VS Code could not apply the frontmatter edit.` / rejected-edit message path are only
   mentioned in passing. Minor, can go in the F-FMEDIT-016/026 notes.

Only item 1 (with 2) is a real gap of substance; items under 3 are minor. Restricted Mode and
read-only (F-FMSCHEMA-028, no edit cells), CRLF (F-021), undo (F-027/028), stale (F-016/017) are
covered.

## Wrong/unverifiable evidence

Spot-checked 40+ claims; all verified by grep in the refactored tree:

- Symbols exist: `setFrontmatterEditCells`, `openFrontmatterKeyEditor`, `receiveFrontmatterResult`,
  `openFrontmatterValueEditor`, `createFrontmatterMenu`, `planFrontmatterSave`,
  `frontmatterValueMatchesField`, `checkFrontmatterCandidate`, `guardedPatch`,
  `frontmatterAddPlacement`, `isPlainSafeScalar`, `handleSave`, `postEditError`, `postEditSaved`,
  `applyEditMode`, `schemaAllowsNull`, `linkSuggestions`, `parseYamlValue`, `appendItem`,
  `moveItem`, `focusNeighbour`, `minimalPairPatch`, `isSameData`.
- Tests exist with the quoted names (runtimeFrontmatterEditor, runtimeFrontmatterFields,
  frontmatterEdit, frontmatterPreservation, okfFrontmatter: 20 names checked, including T21, T22,
  T25, T41 prefixes).
- Visual ids `frontmatter-editing/v02`, `v05`, `v06` are in `test/visual/scenarioIds.ts`;
  `scenarioBooleanOneClick`, `scenarioListEditorClickAndKeys` are in
  `test/integration/realInput.test.ts`; `26-`, `27-`, `28-` captures in
  `test/shared/captureRegistry.ts`.
- Coverage state looks right: F-005 untested (no test for "Enter a valid number."), F-029 doc-only.

Nit: the header cites `minimal*Patch`; the real functions are `minimalPairPatch`,
`minimalRenamePatch`, `minimalRemovePatch`, `minimalAddPatch` (fine as a glob).

## Count check

- Behaviours 33 matches the table. Tested 28 / untested 4 / doc-only 1 matches the table (untested
  F-005, 024, 027, 028; doc-only F-029).
- Checklist line is wrong: it says "16 / 16" rows of the scope, but the checklists give 27 rows
  now (CTL-022 to 033 and others were re-scoped here). Real figure: 25 in scope and cited, 2 moved
  out. The text "9 rows moved in from frontmatter-schema" lists 10 ids (C-AR-074, 075, 086, 100,
  105, C-CTL-022, 023, 025, 027, 028), of which C-CTL-022/023/025/027/028 are already scoped here
  in the checklists, and C-AR-074/075/086/100/105 are still scoped `frontmatter-schema?`. Fix the
  counts and the moved-in list (also CTL-026, 029, 030 to 033 are in scope and cited but not in
  that sentence).

## Verdict

Fixes: (1) add a behaviour row for the editor flush before navigation (items 1 and 2 above, with
tests); (2) get C-AR-018 and C-CL-018 cited by `layout-width` and `gfm` or re-scope them;
(3) correct the checklist counts (27 in scope: 25 cited, 2 moved) and the "moved in" list.

Verdict: REVISE

## Re-check

Scripted: (1) flush row F-FMEDIT-034 and plainSavePending row F-035 added with correct evidence; layout-width cites C-AR-018 and gfm cites C-CL-018 in `| F-` rows; counts text now says 27 = 25 cited + 2 moved. (2) All 27 checklist rows scoped frontmatter-editing(?) are cited in `| F-` lines or listed in Checklist corrections with the target citing them. (3) 8 symbols and 5 test names grep-verified in the wt-059 tree (flushFrontmatterEditor, flushingEditors, needsSchemaCheck, flushRefusalMessage, plainSavePending, afterResult, setFrontmatterEditCells; CR 025 and T21 test titles). (4) 35 F-rows: tested 30, untested 4, doc-only 1; 10 undocumented; all match the Counts table.

Re-check verdict: APPROVE
