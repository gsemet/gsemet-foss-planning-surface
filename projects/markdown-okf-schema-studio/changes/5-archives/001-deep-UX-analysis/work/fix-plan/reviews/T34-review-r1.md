# T34 review — round 1

Base: 0f4605a · Reviewed diff: 10 tracked files changed, +932/-33, plus 2 new files
(`src/preview/contentPatch.ts`, `test/webview/contentPatch.test.ts`). The diff was read from the
working tree. The other dirty files under `.agents/skills/…` are not part of T34.

## Gates
- Implementer: unit PASS 650/650, types PASS, contracts PASS 2/2, trusted PASS (after the nonce
  fix), scroll PASS, reload PASS, full PASS twice (`logs/T34-impl-full-run1.log`, `-run2.log`, both
  `RI-T34 typing: 0 html assignments, 20 content patches`), visual PASS (0 new lines compared with
  the baseline, `logs/T34-impl-visual.log`).
- Orchestrator: `logs/T34-unit.log` PASS 651/651, `T34-types.log` PASS, `T34-contracts.log` PASS.
  `T34-full.log` was still running when I read it (scroll E2E lines PASS so far). `T34-b-full.log`
  and the visual log did not exist yet. **This verdict assumes that the orchestrator's `full` (both
  runs) and `visual` pass.** If either fails, treat the verdict as CHANGES REQUESTED.
- I ran no gate (read-only review).

## Done-when
- [x] `unit`, `contracts`, `full` and `visual` pass. Evidence: the implementer's logs, plus the
  orchestrator's unit and contracts logs. The orchestrator's full and visual runs are still pending.
- [x] RI-T34 passes. It checks: 0 assignments, the same `Frame`, request id and version equal to the
  host's, the typed text, the Mermaid image drawn again in the same frame, the slow render (overlay
  shown, result patched, overlay gone), and the setting turned off (the page is assigned again).
- [x] The report states the D-10 default (`true`) and why.

## Protected features checked
- **P-N1:** after a patch, `applyContentPatch` sets `initialAnchor`/`initialPin` from `next`, resets
  `pinApplied` and runs `initializeContent({ restore: true })`, so `restoreState` re-anchors as a
  fresh load would. Covered by the unit test "anchor and pin positioning equal to a freshly loaded
  page" and the scroll campaign (full).
- **P-E4:** `closeBlockEdit(false)` keeps `pendingBlockNavigation`; only the cancel branch clears
  it. The status region is rebuilt **before** `initializeContent`, so `hasRenderedPreview()` is
  true and `resumePendingBlockNavigation()` runs. Covered end to end only through the full campaign;
  there is no patch-path unit test (finding 2).
- **P-R3:** `contentReplaced()` dispatches `studio:content-replaced`, which `mermaidPreview.ts`
  listens to. RI-T34 checks the image in the same frame, and the screenshot confirms it.
- **P-R2:** math is rendered on the host (`mathRenderer.ts`), so no client typesetting is needed. A
  stylesheet change alters the shell key, which gives a full load. Unit test "different keys when
  math appears".
- **P-R5:** `initializeCheckboxes()` runs in `initializeContent`. `pendingCheckboxToggles` is
  cleared, as a reload would do. Checkbox scenarios pass in full.
- **P-S1:** `planContentPatch` refuses `<script` and `nonce=`. The content comes only from the
  host's sanitized render, and the status region uses `textContent`. The CSP is unchanged. For the
  nonce reuse, see finding 1.
- **P-S2:** `previewContentPatch` goes from host to webview. The runtime validates every field
  (`isValidContentPatch`, 21 malformed or stale variants tested) and needs `sameContext`. Webview
  messages still go through `isPreviewSyncMessage` and `matchesCurrentPreview`. The
  reloaded-document guard runs only on a validated `previewReady`.
- **P-E8:** the patch handler adds no interactive control. `applyEditMode(editMode)` re-applies the
  current mode.
- **Block and frontmatter editors:** closed without cancelling. `deferredPropertiesMarkup` is
  dropped before `closeFrontmatterEditor()`. The host's `refreshPreview` still skips renders while
  an applied block edit is in flight, so autosave keeps its editor, as before. Tested by "block
  editor closed without previewEditCancel/save" and "frontmatter editor closed and deferred markup
  dropped".
- **T30 properties patch:** `previewPropertiesTable` is addressed with the stage identifiers, and
  messages arrive in order after the patch. RI-T30 reports 0 assignments.
- **T43 overlay:** the host calls `clearPendingOverlay` on both patch paths, and the runtime calls
  `applyPendingOverlay({visible:false})`. RI-T34 covers the slow render.
- **Status region:** rebuilt with `createElement`/`textContent` and inserted as the first child of
  `body`. `hasRenderedPreview()` reads the new attribute (unit test).
- **Link navigation:** hints are copied to the new links, then `rescan()` runs. Discovery of new
  links has a unit test.
- **Scroll sync:** the context identifiers move, so `sameContext` matches the host's next messages,
  and `previewReady` re-arms `readyRequestId`. Covered by the scroll campaign.
- **Custom editor (Open With) and reload/deserialize:** they use the same `updatePreview`.
  `retainContextWhenHidden` is true on both. The recreated-webview guard (`reportsReloadedDocument`)
  is pure and unit-tested. It is sound, and a false positive only costs one extra reload.
- **2 s fallback timer:** re-armed on each patch, and cleared in `assignWebviewHtml`, so it is also
  cleared on a document switch, which goes through the full path. Also cleared in `disposePreview`.
  When it fires, it checks the stage and `readyRequestId`.

## Decisions on the implementer's open points
- **RI-T43 with the setting off: accepted.** Its assertions are unchanged. It now covers the
  kill-switch path, and RI-T34 covers the overlay on the patch path (fast and slow). This is not a
  weakening.
- **Nonce:** see finding 1. It is a real but small loss of defence in depth, not a regression that
  can be exploited. MINOR.
- **Extra patch conditions:** accepted. Each one fails safe, because it falls back to a full load:
  same document identity and path, the same runtime startup settings (the page's own anchor toggle
  updates `loadedContext`), and diagnostics within the runtime limits so that the runtime does not
  silently ignore a patch.
- **Stale link-target hints until the next full load:** MINOR. Only the hint styling or title of a
  link whose target was created while typing is affected. Navigation itself resolves on click, so
  UX-22 is unaffected. Follow-up candidate: `discovered.clear()` in `linkNavigation.ts rescan()`.
- **Carrying open disclosures in `initialState`:** accepted. It is better than the task text and
  matches reload behaviour. It is unit-tested.

## Findings
1. [MINOR] `src/extension.ts` `armContentPatchFallback`, the reloaded-document branch of
   `handlePreviewSyncMessage`, and `setPanelHtml` (PlantUML fallback): each of these loads a **new**
   document from `preview.webview.html`. After a patch, that html carries the nonce of the earlier
   document (`reuseNonce`), so a nonce already exposed to an earlier document is used again. The
   patch path itself cannot inject a script (`<script` and `nonce=` are refused), so this is not
   exploitable. It still departs from P-S1's "per-render nonce".

   Fix: add `function freshNonceRecord(preview)`. It generates a new nonce with the same generator
   `buildPreviewWebviewHtml` uses, computes
   `html = reuseNonce(preview.webview.html, preview.webview.nonce, fresh)`, and sets
   `preview.webview = { ...preview.webview, html, nonce: fresh }`. Call it right before every
   `assignWebviewHtml(preview, preview.webview.html)` in those two places.

   Test: a unit test in `contentPatch.test.ts` checks that `reuseNonce` swaps every occurrence. An
   assertion in RI-T34 (or a small trusted test) forces the fallback, then checks that the frame's
   `script[nonce]` equals the record's nonce **and** differs from the nonce before the fallback.
   `previewEditing.test.ts` keeps reading the nonce from the current record. Log this as a
   follow-up if it is not fixed now.
2. [MINOR] `test/webview/scrollSync.test.ts`: there is no patch-path test for P-E4. Fix: add
   "T34: pending block navigation resumes after a content patch". In edit mode, open a block, press
   ArrowDown at the end (so `pendingBlockNavigation` is set), apply a `previewContentPatch` with
   success status, and assert that the next block's editor is open with the caret at the start.
3. [MINOR] `src/extension.ts` `scheduleDeferredPreviewWork`: the PlantUML patch arms no fallback
   timer. If that message is lost, the diagrams appear only on the next render. Fix (optional):
   arm a timer that calls `setPanelHtml` with the current record when no `previewReady` for
   `result.stage.requestId` arrives after the patch. Track this with a counter of acknowledged
   patches, because `readyRequestId` is already equal to the stage.
4. [NIT] `postContentPatch` sends the field `documentId: previous.activeDocumentIdentity`, while
   the runtime matches it against `context.documentId`. This is correct only because the patch
   needs the same identity. A comment would help.

## Existing assertions changed
- `previewConfiguration.test.ts` adds the new key to the expected object: OK (listed).
- `package-contract.test.ts` adds the key: OK (listed).
- `realInput.test.ts`: RI-T43 is now wrapped in `withIncrementalUpdates(false, …)`, and none of its
  assertions changed: OK (justified, see above).
- `scrollSync.test.ts`: only the test harness changed (the status query, an optional `details`
  list). No assertion was removed: OK.

## D-10 default
`true` is justified, provided the orchestrator's pending full and visual runs pass. Every required
gate passed for the implementer. No protected feature regressed in this review. The kill switch is
documented in the README, and every unusual case falls back to the old full-load path.

VERDICT: PASS
