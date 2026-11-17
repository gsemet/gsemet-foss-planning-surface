# T19 review — round 1

Base: b2c5476 · Reviewed diff: 5 files (scrollSync.ts, previewStyles.ts, scrollSync.test.ts,
previewStyles.test.ts, scenarios.ts), all in Allowed files.

## Gates
compile PASS; unit PASS; types PASS; trusted PASS; visual PASS vs T00 baseline (0 new failure lines).

## Done-when
- [x] unit/trusted/visual gates pass — orchestrator logs.
- [x] `identifier-split` required and passing on a narrow wide-table scenario — new
  `code-dark-table-narrow` (fixture 04, 640 px, `machineChecks: ["identifier-split"]`), notes show PASS.
  The screenshot shows `nw-02` and `North` on one line.
- [ ] "a visible right-edge shadow" — not met in the dark theme (see finding 1). The white theme
  was not checked at all (report admits it).

## Judged explicitly
- **`markWideTables` cost.** It is not on the scroll path: `scroll` calls `scheduleScroll` only;
  `stabilizeLayout` runs on resize, visualViewport resize, ResizeObserver and image loads. Reading
  `scrollWidth` forces layout, but `measure()` right after already reads layout, so no extra
  forced layout per frame. Attribute writes happen only on value change (idempotence unit test
  counts `setAttribute`/`removeAttribute`), and since they happen before `measure()`, measured line
  tops reflect the final layout. A nowrap change resizes the content, which re-fires the
  ResizeObserver once; the second pass writes nothing, so no loop. Per-resize cost is one
  `querySelectorAll("th, td")` walk per table plus a `getAttribute` per cell: acceptable. OK.
- **Shadow visibility.** Dark: invisible. `rgba(0,0,0,0.28)` on `#1e1e1e` has no perceptible
  contrast; in `code-dark-table-narrow.png` the right edge at "Last…" shows only clipping, no cue.
  White: not evidenced.
- **New narrow scenario.** Registered correctly in `SCENARIOS`, fixture/width match the task, keeps
  `machineChecks: ["identifier-split"]`. The choice of `scroll: top` + fullPage to avoid the
  baseline-known sticky overlap check is reasonable.

## Protected features checked
- P-N1: `measure()` still follows `markWideTables` in `stabilizeLayout` and at init; scroll
  listener untouched; scrollSync anchor tests pass (unit gate) and scroll suite (trusted).
- P-R7: properties table skipped via `closest("[data-okf-properties]")`; unit test asserts no
  frontmatter cell is marked.
- P-E5: cell editor unaffected — short-cell marks are never removed during an edit; trusted
  table-editing tests pass. `check_horizontal_access` still passes (code-dark-table).
- Conventions §2: no backtick or `${` in runtime, regex backslash doubled (`\\S`). OK.

## Findings
1. [MAJOR] `src/preview/previewStyles.ts`: rule
   `#sphinx-myst-preview-content table[data-sphinx-table-overflow="true"]` — the two
   `radial-gradient` shadows use black at 0.28, which is invisible on dark themes, so the task's
   "visible right-edge shadow" is not met. Fix: replace the shadow colour with a theme-aware one,
   e.g. `color-mix(in srgb, var(--vscode-foreground, CanvasText) 35%, transparent)` in both
   radial gradients (keeps black-ish on white, light-ish on dark), and widen the shadow size from
   `0.75rem` to `1rem`. Update the regex in `previewStyles.test.ts` test "overflowing content
   tables keep short cells whole and show scroll shadows" to also assert
   `radial-gradient\(farthest-side at 100% 50%, color-mix\(in srgb, var\(--vscode-foreground`.
   Then add a white/light counterpart scenario `code-light-table-narrow` (same as
   `code-dark-table-narrow` but `theme: "light"`, `fullPage: false`, scroll to `table` is not
   required; a top capture at height ≥ 1400 so the table is in the viewport, with
   `machineChecks: ["identifier-split"]`), and report both screenshots with a crop/zoom note
   confirming the right-edge cue is visible in each theme.
2. [MINOR] `src/webview/scrollSync.ts:markWideTables` — the regex runs on `textContent`; while a
   cell editor overlay is inside a cell, its contents can count. Harmless because marks are only
   added once before editing; note for follow-ups only.

## Existing assertions changed
None (test diff only adds harness fields, a selector branch and new tests). OK.

VERDICT: CHANGES REQUESTED
