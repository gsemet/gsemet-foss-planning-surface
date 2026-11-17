# T19 implementation — round 1

STATUS: DONE

## Summary
Added `markWideTables()` to the webview runtime. It marks short (<= 24 chars, no whitespace) cells with `data-sphinx-short-cell` and sets `data-sphinx-table-overflow` when `scrollWidth > clientWidth + 1`. It skips `[data-okf-properties]` and writes attributes only on change. It runs before `measure()` in `stabilizeLayout` and before the initial `measure()`. Two CSS rules (nowrap for short cells, edge shadows) were added to `previewStyles.ts`. Short cells are only ever marked, never unmarked, so a cell with an open editor overlay cannot flip.

## Files changed
- src/webview/scrollSync.ts — `markWideTables` and two calls
- src/preview/previewStyles.ts — the two rules from the task, before the `th, td` rule
- test/webview/scrollSync.test.ts — fake DOM extensions (`scrollWidth`/`clientWidth`, `th, td` query, `contentTables` harness list, table selector in `document.querySelectorAll`) and 2 tests
- test/webview/previewStyles.test.ts — 1 test
- test/visual/scenarios.ts — new scenario `code-dark-table-narrow`

## Tests written first (failing before the fix)
- markWideTables marks short cells and the overflow of a wide table, never the properties table — failed (attributes null)
- markWideTables sets the overflow attribute only past a one pixel tolerance and is idempotent — failed
- overflowing content tables keep short cells whole and show scroll shadows — failed (rules missing)
(unit log fail 3 before the fix, 0 after; 510 pass)

## Tests added or changed
- the three above
- visual `code-dark-table-narrow` (fixture 04, 640 px, dark, full page) with `machineChecks: ["identifier-split"]`: PASS

## Existing assertions changed
None.

## Verification
- `gate.sh T19-impl unit types` → PASS (logs/T19-impl-unit.log, T19-impl-types.log)
- `gate.sh T19-impl trusted` → PASS (logs/T19-impl-trusted.log)
- `gate.sh T19-impl visual` → PASS vs baseline, 0 new failure lines (logs/T19-impl-visual.log)

## Evidence for reviewers
- logs/visual-T19-impl/code-dark-table-narrow.png (nw-02 and North on one line; right-edge shadow, table clipped at "Last…")
- logs/visual-T19-impl/code-dark-table.png (900 px, scrolled far right; left shadow visible)
- logs/visual-T19-impl/handbook-narrow-table.png (unchanged behaviour)

## Open points / STOP reason
- The repository had no narrow (<= 640) scenario on fixture 04. I added one. It uses scroll "top" and fullPage, because a scenario scrolled to `table` fails the baseline-known check "sticky heading overlaps the reserved toolbar row" (the same failure the existing code-dark-table and handbook-narrow-table have). That would have counted as a new failure line. No existing check was touched. The new scenario is not scrolled to the right, so the left shadow is shown in the 900 px scenario and the right shadow in the new one.
- Shadow alpha left at 0.28. It is visible but subtle on dark; the reviewer may want it stronger. The white theme was not inspected separately.
- Table toolbar (T18): it sits outside the table, so the table's background and overflow styles do not affect its placement. The trusted gate (table editing tests) passes.
