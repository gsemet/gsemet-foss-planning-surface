Ids in this file predate the reduction; see `reduction/mapping.csv`.

# Review: toolbar-navigation inventory (P10.1 critic)

Scope `toolbar-navigation` (TOOLBAR). Inventory: `inventory/toolbar-navigation.md` (54 behaviours).
Code read at worktree `c166165`.

## Missing rows

Scripted: rows whose scope column starts with `toolbar-navigation` (exact 52 + guessed `?` 10 = 62,
matches the "/62" of the Counts table). Every row is cited in the inventory, except none uncited
directly. The 6 rows listed under "Checklist corrections" as moved were checked in the target scope:

- C-PKG-006, C-PKG-007, C-CL-107: cited in `inventory/lifecycle-sync.md`. OK.
- C-AR-115: n/a (test tooling), no target needed. OK.
- C-AR-050 (moved to block-editing, F-BLOCK-039/040): `inventory/block-editing.md` does NOT cite
  C-AR-050 (F-BLOCK-039/040 exist but their Checklist column lacks it). NOT handled.
- C-AR-052 (moved to palette-slash, F-PALETTE-093/095/096): `inventory/palette-slash.md` does NOT
  cite C-AR-052. NOT handled.

## Missing behaviours

None of substance. Checked `navigationHistory.ts`, `history.ts`, `viewState.ts`, `workspaceChoices.ts`,
`anchorMode.ts`, `toolbarCollapse.ts`: the history cap/dedupe/depart, host Back/Next failure paths,
read-only acceptance, stale ids, anchor pairing, persistence are all present. Minor, not counted:
`setViewPreference` logs "Failed to persist the Markdown preview view preferences." when the storage
write fails (no row; F-TOOLBAR-009 says untested host side). Other `viewState` messages (previewRefresh,
previewState, banner, theme/edit/palette mode) are in lifecycle-sync, myst, theme-zoom, palette-slash
inventories (grep confirmed).

## Wrong/unverifiable evidence

Spot-checked 30 claims, all found by grep: symbols `renderPreviewToolbar`, `installToolbarCollapse`,
`installTocColumn`, `installHistoryControls`, `installLinkNavigation`, `normalizeViewPreferences`,
`applyViewPreference`, `setViewPreference`, `postHistoryState`, `recordNavigation`,
`markdownFragmentRange`, `installStickyHeadings`, `refreshReadingOffset`, `measureHeadings`,
`normalizeStickyHeadingDepth`, `stickyHeadingDepthOf`, `markEditorSelectionInPreview`,
`EDIT_REQUEST_TYPES`, `injectPreviewThemeControl`, `applyPairing`, `keepVisible`, `applyCollapse`,
`headingLabel`, `applyTargets`; tests "preview toolbar has three rows", "P8: the collapse button hides
rows 2-3", "a fresh workspace starts with the toolbar collapsed", "caps sticky heading convergence at
three passes", "T11: a previewHistoryState of another document version is ignored",
"previewHistoryGo accepts only back or forward", "the sticky band label leaves out comment chips",
"a click right after a content patch scrolls to the live heading", "the TOC scrolls itself, not the
page", "T34: links of the new conten(t)", "sticky heading depth is rounded and clamped"; Python checks
`check_preview_toolbar_rows`, `check_toolbar_collapse`, `check_toc_column`, `check_toc_shot`,
`check_sticky_headings`, `stress_sticky_heading_scroll`, `toolbar_probe`; `previewHistory.test.ts`.
Coverage states looked right (the 6 untested rows have no test). No false evidence found.

## Count check

- Behaviours 54: matches the table (F-TOOLBAR-001..054). Tested 48 + untested 6 = 54: OK.
- Checklist 56 cited + 6 moved / 62: arithmetic OK (but see C-AR-050/052 above).
- Undocumented: the Counts table says 14 and lists 14 ids, but the table's notes also flag
  F-TOOLBAR-041 as undocumented ("Undocumented g..."). Real count is 15; add 041 to the list or
  fix the 041 note.

## Verdict

Fixes:
1. Add C-AR-050 to the Checklist column of F-BLOCK-039/040 in `inventory/block-editing.md`
   (or cite it in the toolbar inventory instead and drop it from "Checklist corrections").
2. Same for C-AR-052 in `inventory/palette-slash.md` (F-PALETTE-093/095/096).
3. Fix the Undocumented count/list for F-TOOLBAR-041 (14 vs 15).
4. Optional: add a note on the "Failed to persist" console error of `setViewPreference`.

Verdict: REVISE

## Re-check

- Fixes: C-AR-050 now cited in F-BLOCK-039/040 and C-AR-052 in F-PALETTE-093/095/096 (grep OK); Undocumented list now has 15 ids incl. 041 (matches the F-rows); "Failed to persist" note added to F-TOOLBAR-009 (code in `workspaceChoices.ts:129`, OK).
- Checklist: all 62 C- ids of toolbar-navigation are cited in `| F-TOOLBAR` rows (56) or in Checklist corrections (6: PKG-006/007, CL-107 cited in lifecycle-sync rows; AR-050/052 cited in targets; AR-115 n/a). None missing.
- Spot-checked 8 evidence symbols/files by grep (flushOpenEditorsThen, previewHistoryState, markEditorSelectionInPreview, installStickyHeadings, check_toc_column, stress_sticky_heading_scroll, normalizeStickyHeadingDepth, EDIT_REQUEST_TYPES): all found. Counts: 54 rows = 48 tested + 6 untested, 0 doc-only, 15 undocumented: matches the table.

Re-check verdict: APPROVE
