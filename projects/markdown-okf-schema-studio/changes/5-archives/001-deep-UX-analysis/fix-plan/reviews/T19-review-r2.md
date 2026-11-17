# T19 review — round 2

Base: b2c5476 · Reviewed diff: 5 files (scrollSync.ts, previewStyles.ts, scrollSync.test.ts,
previewStyles.test.ts, scenarios.ts), all in Allowed files. Round-2 delta: shadow colour/size in
previewStyles.ts, tightened regex in previewStyles.test.ts, new `code-light-table-narrow` scenario.

## Gates
compile PASS; unit PASS; types PASS; trusted PASS; visual PASS vs T00 baseline (0 new failure lines).

## Done-when
- [x] unit/trusted/visual gates pass — orchestrator logs.
- [x] `identifier-split` required and PASS on `code-dark-table-narrow` and `code-light-table-narrow`
  (notes `logs/visual-T19/*.txt`). Screenshots show `nw-02` and `North` on one line.
- [ ] "a visible right-edge shadow" — met in light, NOT met in dark (finding 1).

## Round-1 finding 1 — judged on the screenshots
Crops of the table's right edge (2x capture, x 880–1280, y 2120–2680), body row pixel samples:
- **Light** (`code-light-table-narrow.png`): 255 → 207 → 177 approaching the edge. Clear grey
  shadow on the body rows. OK.
- **Dark** (`code-dark-table-narrow.png`): 31 → 25 → 22. A 9-level *darkening* on #1f1f1f, not the
  "lighter band" the report describes; not perceptible at normal viewing. Not met.
- **Root cause:** the visual harness themes (`test/visual/themes.ts`) define
  `--vscode-editor-foreground` but not `--vscode-foreground`, so the rule falls back to
  `CanvasText` (black in the page's colour scheme) and the dark cue is black-on-near-black — the
  same failure as round 1. Real VS Code defines `--vscode-foreground`, so production would probably
  look right, but the evidence the task requires does not show it, and the rule should not depend
  on a variable the harness lacks.

## Protected features checked
- P-N1: `markWideTables()` precedes `measure()` in `stabilizeLayout` and at init; scroll path
  untouched; unit + trusted scroll suites pass.
- P-R7: properties table skipped via `closest("[data-okf-properties]")`; unit test asserts it.
- P-E5: cell editing unaffected (marks only added, never removed); trusted table-editing tests pass;
  `check_horizontal_access` still passes on `code-dark-table`.
- Conventions §2: no backtick/`${` in runtime, `\\S` doubled. OK. Read-only/P-E8: purely visual,
  no new interactive surface.

## Findings
1. [MAJOR] `src/preview/previewStyles.ts`, rule
   `#sphinx-myst-preview-content table[data-sphinx-table-overflow="true"]`: in both
   `radial-gradient(...)` layers replace
   `var(--vscode-foreground, CanvasText)` with
   `var(--vscode-editor-foreground, var(--vscode-foreground, CanvasText))` (keep 35%, 1rem).
   Expected: dark capture shows a lighter band at the right edge of the body rows (peak about
   gray 90 on gray 31 with #cccccc), light capture stays a grey shadow.
   Test: in `test/webview/previewStyles.test.ts`, test "overflowing content tables keep short cells
   whole and show scroll shadows", change the end of the second regex to
   `radial-gradient\(farthest-side at 100% 50%, color-mix\(in srgb, var\(--vscode-editor-foreground, var\(--vscode-foreground`
   (write it first, see it fail). Re-run the visual gate and in the report give pixel samples
   (as above) from both narrow screenshots showing a difference of at least 40 levels between the
   cell background and the edge in each theme. Do not edit `test/visual/themes.ts`.
2. [MINOR, carried] `markWideTables` regex reads `textContent` that may include an editor overlay;
   harmless, follow-up only.

## Existing assertions changed
Only the T19-own regex added in round 1, tightened (not weakened). OK.

VERDICT: CHANGES REQUESTED
