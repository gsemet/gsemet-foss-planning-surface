# T30 review — round 1

Base: e26e836 · Reviewed diff: 6 files, +395/-18 (src: extension.ts, propertiesTable.ts, scrollSync.ts;
tests: propertiesTable, scrollSync, realInput)

## Gates
- implementer: unit, types, contracts, scroll PASS; trusted PASS on rerun (run 1 failed in the unrelated
  `scenarioUndoStaysInEditor` block-editor wait, `logs/T30-impl-trusted-run1.log`; the standalone
  trusted run before it and the rerun passed — one clean rerun plus one earlier clean run).
- orchestrator: `logs/T30-unit.log` PASS (0 fail), `T30-types.log` PASS, `T30-contracts.log` PASS.
  `T30-full.log` was still in progress at review time (scroll E2E lines PASS so far, no FAIL); the
  visual log was not yet written. The orchestrator must confirm full + visual against the baseline
  before committing; this verdict assumes they show no new failure.

## Done-when
- [x] Both deferred passes use `patchPropertiesTable`; no html assignment on the in-place path —
  evidence: diff of `refreshFrontmatter`/`scheduleLinkEnrichment`; RI-T30 "10 html assignments,
  10 ready renders" and linked-file step with unchanged `htmlAssignments` and surviving window marker.
- [x] Runtime replace / insert / remove / defer / ignore other context / tabindex after replace —
  evidence: 5 new scrollSync tests, red log `T30-impl-red2-unit.log`.
- [x] Refactor output identical — `T30: replacing with precomputed markup is identical…`.
- [x] PlantUML path left as full assignment with comment.
- [x] T43 amendment: `preview.webview = { ...preview.webview, html }`, no `assignWebviewHtml` on the
  ready path.

## Protected features checked
- P-R7 (properties table content/attributes): markup is produced by the same `renderPropertiesTable`
  call with identical arguments; `replacePropertiesTableHtml` is the old body unchanged. Screenshot
  `30-properties-in-place.png` shows the table with types, link and updated excerpt, identifier
  cells on one line (machine check PASS), toolbar not covering text.
- Description-column state: `applyDescriptionVisibility()` after the swap; covered by the
  "tooltip closed, re-measured, description state kept" test.
- Link tooltips: `closeLinkTooltip()` before removing the section (no tooltip anchored to a
  detached node).
- Edit flows (P-E*): frontmatter editor open → markup deferred, so `activeFrontmatterEdit` never
  references removed nodes; applied on close (latest wins). Add-field resume: in-place patch keeps the
  same `context.requestId`, so `resumePendingFrontmatterEdit` behaviour is unchanged (it already waited
  for the next render's load before T30). Edit cells regain `tabindex` via `setFrontmatterEditCells`.
- P-E8 read-only: `editingEnabled = !preview.readOnly` passed as before; `setFrontmatterEditCells(editMode)`
  is inert without edit mode.
- P-S2/P-S4: handler gated by `sameContext`; `markup` must be a string; markup only host-generated
  (escaped in propertiesTable.ts), no other sink.
- Conventions §2: no backtick or `${` added in the runtime template; optional-chained DOM APIs.

## Stale-page analysis (VS Code-initiated reloads)
`panel.webview.html` keeps the pre-patch string while the record is newer.
- Hide/show tab: both the side panel (`createWebviewPanel`) and the custom editor
  (`registerCustomEditorProvider`) use `retainContextWhenHidden: true` → no reload.
- Window reload: `deserializePreviewPanel` assigns a status page and re-renders from the record /
  a fresh build → not stale.
- Refresh command / theme / edit-mode: refresh queues a build (full render with the record);
  theme change posts no html. Not stale.
- Panel moved between groups (if the VS Code version reloads the iframe): the old string loads, reports
  ready for the same requestId, and shows the table as of the last full render until the next render
  (next keystroke or save). Before T30 the same move would have shown the latest patched page. Very
  low likelihood, self-healing, cosmetic → MINOR 1.

## Findings
1. [MINOR] extension.ts:`patchPropertiesTable` — after a VS Code-initiated iframe reload (group move) the
   page shows the html from the last full assignment, and later patches with the same markup are no-ops
   because the record already matches. Follow-up option: in the `previewReady` handler, if
   `preview.panel.webview.html !== preview.webview.html` and the ready requestId equals the stage, post
   `previewPropertiesTable` with the markup extracted from the record (or call `assignWebviewHtml` with
   the record). Not required for T30.
2. [MINOR] scrollSync.ts:`previewPropertiesTable` deferral — an open frontmatter editor now keeps
   "Saved. Refreshing preview…" until the next full render (~1 s) instead of ~300 ms. Acceptable (the
   full render follows every save); log in followups so the UX-28 step 3 / T43 status work can check it.
3. [NIT] `renderedStages` test hook and `refreshInsertPoints()` call are small, justified additions in
   allowed files; the insert-point rebuild is guarded by `!activeBlockEdit` and only runs when the
   section appears/disappears. OK.
4. [NIT] RI-T30's first half does not discriminate (report says so); the linked-file half does
   (red log `T30-impl-red4-trusted.log`, 13 vs 10). Acceptable.

## Existing assertions changed
- scrollSync.test.ts fake DOM: `[data-okf-edit-cell]` selector now returns the current section's cells
  when the section was replaced, original cells otherwise — harness extension, no assertion weakened. OK.
- No other existing assertion modified or removed.

VERDICT: PASS
