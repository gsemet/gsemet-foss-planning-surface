# T19 review — round 3

Base: b2c5476 · Reviewed diff: 5 files (scrollSync.ts, previewStyles.ts, scrollSync.test.ts,
previewStyles.test.ts, scenarios.ts), all in Allowed files. Round-3 delta: the radial shadow layers
use `var(--vscode-editor-foreground, var(--vscode-foreground, CanvasText))`; T19 regex tightened.

## Gates
compile PASS; unit PASS; types PASS; trusted PASS (57s); visual PASS vs T00 baseline (0 new failure
lines). Logs in `logs/`.

## Done-when
- [x] unit/trusted/visual gates pass — orchestrator logs.
- [x] `identifier-split` required and PASS on `code-dark-table-narrow` and `code-light-table-narrow`
  (`logs/visual-T19/*.txt`: "PASS identifier-split").
- [x] Visible right-edge shadow — round-2 finding 1 fixed. Crops of this run's screenshots
  (`logs/visual-T19/code-{dark,light}-table-narrow.png`, x 880–1280, y 2120–2680): dark shows a clear
  light band at the table's clipped right edge on every body row; light shows a clear grey shadow.
  Consistent with the report's pixel samples (dark 31→82, light 255→196 at y=2360).
- [x] Short cells (`nw-02`, `North`) on one line — screenshots + machine check.

## Protected features checked
- P-N1: `markWideTables()` runs before `measure()` in `stabilizeLayout` and at init; writes only on
  change (idempotence unit test counts zero writes) so ResizeObserver cannot loop.
- P-R7: properties table skipped via `closest("[data-okf-properties]")`; unit test asserts it.
- P-E5: table cell editing unaffected (attributes only); trusted table-editing tests pass;
  `check_horizontal_access` still passes on `code-dark-table`.
- Conventions §2: no backtick/`${` in runtime, `\\S` doubled. P-E8: purely visual, no new interactive surface.

## Findings
1. [MINOR, carried] `scrollSync.ts:markWideTables` — short-cell regex reads `textContent`, which may
   include an open editor overlay's text; marks are add-only so harmless. Follow-up only.
2. [NIT] Dark-theme cue is a lighter band (foreground-coloured) rather than a dark shadow; it reads
   clearly as an edge cue, acceptable.

## Existing assertions changed
Only the T19-own regex (added round 1), tightened again. OK.

VERDICT: PASS
