# T18 implementation — round 1 (after orchestrator amendment)

STATUS: DONE

## Summary
All planned changes are implemented, including the orchestrator's "toolbar must be visible when it
appears" amendment. `unit`, `types`, `trusted` (with RI-T18) and `visual` pass; visual reports 0 new
failure lines and `scenarios.ts` scroll positions are unchanged. The earlier 4 new lines (narrow
`edit-table-wrapped-*-460`, bar at y=-28) are gone after the reveal scroll.

## Reveal rule (amendment)
`revealTableToolbar(menu, cell)` in `scrollSync.ts` runs once, when the toolbar is first created for
a table (not on cell switches), right after `applyAnchor()`. It calls `refreshReadingOffset()`,
measures the bar, and when `bar.top < readingOffsetValue` scrolls up by the shortfall (limited to
`window.scrollY`) through `programmaticScroll`, only if `cell.bottom + delta` stays within the
viewport. It then adds the delta to `editAnchor.viewportTop` so later anchor restores keep the page
where it is.

## Files changed (all under )
- src/webview/scrollSync.ts — toolbar inserted before the table (or its single-child DIV wrapper; body fallback), `applyAnchor()` after insertion, `positionMenu` and its listeners removed, label span per button, new status text.
- src/preview/previewStyles.ts — `.sphinx-preview-table-menu` static / wrap / `margin: 0 0 6px`, labelled button rules, selected-cell outline `2px solid` with `outline-offset: -2px`.
- test/webview/scrollSync.test.ts, test/webview/previewStyles.test.ts — new tests and listed changes, including the 3 reveal tests (exact delta, already visible, cell would leave the viewport).
- test/integration/realInput.test.ts — RI-T18.
- test/visual/scenarios.ts — `machineChecks: ["overlay-covers-text", "overlay-clipped"]` on both table-cell scenario definitions (single and wrapped matrix); description text updated.
- test/visual/capture.py — floating checks replaced (see below).

## Tests written first (failing before the fix)
- table toolbar sits in the flow above the table with text labels and a position status — `Expected "actual" to be reference-equal to "expected"` (menu parent was body).
- table toolbar sits in the document flow above the table with labelled buttons — `The input did not match the regular expression /\.sphinx-preview-table-menu\s*\{\s*position: static;...`
- RI-T18 against the unmodified runtime and CSS (HEAD versions of scrollSync.ts and previewStyles.ts swapped in temporarily, then restored; log `logs/T18-impl-old-trusted.log`): `Real-input integration failed: Error: Timed out waiting for the table toolbar to appear above the table.`

## Tests added or changed
- Unit: parent is the table's parent and the bar directly precedes the table, 4 labels, header and body status text, menu removed on close, no `data-placement` or `--sphinx-preview-table-menu-*` properties.
- previewStyles: new menu and outline rules.
- RI-T18: toolbar is the table's previous sibling, status `Row 1 of 2 · column 2 of 2`, labels, computed `position: static`, selected cell top moved <= 2 px, capture with both required checks (passes on the new code).
- capture.py now checks: bar visible, `position: static`, directly precedes its table, bar bottom <= table top + 1, no table cell intersected, inside the viewport, 4 operations, no Save/Cancel, SVG icons and titles, the four labels, selected cell outline `solid` / `2px`.

## Existing assertions changed
- scrollSync.test.ts:"table cell editing exposes row and column operations and saves the edited table" — old: parent `BODY`, `data-placement` above/below, `--sphinx-preview-table-menu-top/left` values after resize/scroll → new: no `data-placement`, empty top/left properties — required by: removal of floating placement.
- previewStyles.test.ts:"control tooltips retain their offset while sticky headings remain at the top" — old: loop over `["table","frontmatter"]` asserting `flex-wrap: nowrap;` → new: frontmatter keeps `nowrap`, table asserts `\.sphinx-preview-table-menu \{[^}]*flex-wrap: wrap;` — required by: step 3 (orchestrator amendment). Other assertions of that test unchanged.
- capture.py (floating-placement checks): "floating table action bar is missing or hidden" → "table action bar is missing or hidden"; `position != "fixed"` → `!= "static"`; `parentElement === document.body` → "directly precedes its table"; "not aligned with its active cell" (placement `controls`, barLeft 8, barBottom <= cellTop) → "not above the table or covers cells"; "outside the screenshot viewport" kept unchanged; "floating ... Save or Cancel" wording only; "selected table cell still has an outline" (outlineStyle none) → requires `solid` and `2px`.

## Verification
- `scripts/gate.sh T18-impl unit types trusted visual` (output `logs/T18-gate-r1c.out`):
  - compile PASS, unit PASS (506 pass, 0 fail; logs/T18-impl-unit.log), types PASS
  - trusted PASS 57 s (logs/T18-impl-trusted.log, includes RI-T18)
  - visual PASS vs baseline: 0 new failure lines, 4 baseline lines now passing, 0 moved (logs/T18-impl-visual.log)
- Baseline lines now passing: the 4 `table action bar is not aligned with its active cell` lines (08-okf-schema dark and light sticky-3, two scenarios each).

## Evidence for reviewers
- `PLAN/logs/visual-T18-impl/edit-table-wrapped-dark-460.png` and `-light-460.png` (previously failing): the bar is now in the viewport, below the sticky band. In the final frame the bar's first row sits very close to the band's lower edge and its top few pixels look tight; the `overlay-clipped` and viewport checks pass. Reviewer, please look at it.
- `edit-table-wrapped-dark-900.png`, `-light-900.png`.

## Open points
- Wrapper rule: the bar is placed before a single-child DIV parent without `data-sphinx-source-line`, otherwise before the table; the renderer emits no `.table-wrapper` today.
- The reveal assumes `readingOffsetValue` (65 px with three sticky lines) as the usable top, as the amendment specifies.
