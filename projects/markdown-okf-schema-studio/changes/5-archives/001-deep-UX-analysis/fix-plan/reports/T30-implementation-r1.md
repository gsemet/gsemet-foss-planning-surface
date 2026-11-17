# T30 implementation — round 1

STATUS: DONE

## Summary
The two deferred passes (`refreshFrontmatter`, `scheduleLinkEnrichment`) now call one host helper,
`patchPropertiesTable(preview, result, sourceMapping)`. It renders the markup once, updates the
host's record of the page (`preview.webview`), does nothing when the html is unchanged, and posts
`previewPropertiesTable` to a page that is ready for the current stage. A page that is not ready
falls back to `setPanelHtml` as before. The runtime replaces, inserts or removes
`[data-okf-properties]` in place, defers the markup while a frontmatter editor is open, and applies
it when the editor closes. The in-place path never assigns `panel.webview.html` (T43 amendment).

## Files changed
- `src/frontmatter/propertiesTable.ts` — new export
  `replacePropertiesTableHtml(html, markup)`; `replacePropertiesTableMarkup` renders and delegates
  (output identical).
- `src/extension.ts` — `patchPropertiesTable` helper replaces both
  `setPanelHtml(…replacePropertiesTableMarkup…)` call sites; comment on the PlantUML path; test hook
  `renderedStages` (counter incremented in `updatePreview`, exposed by `getActivePreviewForTests`);
  imports.
- `src/webview/scrollSync.ts` — `previewPropertiesTable` message
  handler, `applyPropertiesMarkup`, `deferredPropertiesMarkup`, deferred apply in
  `closeFrontmatterEditor`.
- `test/frontmatter/propertiesTable.test.ts` — one new test.
- `test/webview/scrollSync.test.ts` — fake DOM extended
  (`insertAdjacentHTML`, `onRemove`, a replaceable properties section in the harness) and 5 new tests.
- `test/integration/realInput.test.ts` — scenario RI-T30, registered
  after RI-T43.

## Tests written first (failing before the fix)
- `T30: replacing with precomputed markup is identical…` (propertiesTable) — compile failure before
  the refactor: `has no exported member named 'replacePropertiesTableHtml'`
  (`logs/T30-impl-red-compile.log`).
- Runtime tests (handler disabled temporarily; `logs/T30-impl-red2-unit.log`, 5 failures):
  - `previewPropertiesTable replaces the properties section in place` — `a new section replaced the old one`
  - `…inserts the section when it is absent and removes it on empty markup` — `an empty markup removes the section`
  - `…deferred while a frontmatter editor is open, then applied on close` — `the latest deferred markup was applied`
  - `a replaced section gets edit-cell tabindex in edit mode…` — `Expected values to be strictly equal`
  - `a replacement closes the link tooltip, re-measures…` — `the tooltip closed`
- RI-T30 (host fallback forced on temporarily, `logs/T30-impl-red4-trusted.log`) —
  `html assignments (13) must not exceed ready renders (10)`.

## Tests added or changed
- propertiesTable: `replacePropertiesTableHtml` output equals `replacePropertiesTableMarkup` for
  changed, removed and disabled tables; unchanged markup returns the identical string (the host's
  "nothing changed" check).
- scrollSync (5): replace in place; insert when absent and remove on empty markup; ignored for
  another requestId, documentVersion, documentId or a non-string markup; deferred while a
  frontmatter editor is open and applied (latest wins) on Escape; edit-cell `tabindex` after a
  replacement (on in edit mode, off outside it); tooltip closed, layout re-measured, description
  state kept.
- RI-T30: real typing of 10 characters (60 ms delay) in the body of a document with an
  x-okf-link; `htmlAssignments - A0 <= renders`; then the linked file's description changes on disk
  and the excerpt updates in the same frame (marker on `window` survives, `htmlAssignments`
  unchanged, frame not detached). Screenshot `30-properties-in-place`.

## Existing assertions changed
- None.

## Verification
- `gate.sh T30-impl unit types contracts` → PASS (`logs/T30-impl-unit.log`, `-types.log`,
  `-contracts.log`)
- `gate.sh T30-impl trusted` → run 1 FAIL in `scenarioUndoStaysInEditor` ("Timed out waiting for the
  editor matching [data-sphinx-preview-block-editor] textarea", an unrelated earlier scenario,
  `logs/T30-impl-trusted-run1.log`); rerun → PASS (`logs/T30-impl-trusted.log`, RI-T30 line:
  `10 html assignments, 10 ready renders`). The standalone trusted run just before it (same code) also passed.
- `gate.sh T30-impl scroll` → PASS (`logs/T30-impl-scroll.log`)
- No gate, VS Code test instance or other process of mine is left running.

## Evidence for reviewers
- RI-T30 screenshot written by the real-input harness (`30-properties-in-place`).
- Red/green logs in `PLAN/logs/T30-impl-red*-*.log`.

## Feedback addressed (rounds 2–3)
- n/a (round 1)

## Open points / STOP reason
- **Deviation 1 (test hook).** The task asks to count renders by polling `getActivePreviewForTests()`
  for `phase === "ready"`. That undercounts: a ready state is often followed at once by the next
  build (first attempt: 10 assignments vs 8 sampled renders, with and without the fix). I added the
  counter `renderedStages` (same kind as `restoreCalls` / `pendingOverlayShown`) and RI-T30 compares
  against it. The allowed file `src/extension.ts` was touched, no other file.
- **Deviation 2 (RI-T30 first half cannot discriminate).** Body typing already produced no table
  change, so the first assertion (`assignments <= renders`) also holds before the fix when counted
  exactly (10 vs 10 in red and green). The discriminating part is the linked-file step (no
  assignment, same page); with the fallback forced it fails as shown above (13 vs 10 in the first
  half too, after the caret fix).
- **Test flake note.** RI-T30 sets and waits for the caret at the end of the source and waits 300 ms
  before typing; without that, the first character landed at offset 0 of the document.
- **Behaviour to be aware of.** An open frontmatter editor now stays open ("Saved. Refreshing
  preview…") until the next full render reloads the page (about 1 s), because the 300 ms table patch
  is deferred while the editor is open. Before, the 300 ms reload closed it earlier. No test depends
  on this.
- A page that is still loading (not yet `previewReady`) when the 150 ms enrichment fires still takes
  the `setPanelHtml` fallback, as the task specifies.
- On the in-place path `panel.webview.html` stays at the older string while the host record is
  newer (as the amendment prescribes); a later full assignment always uses the record, so it is
  consistent.
- The runtime also calls `refreshInsertPoints()` when the section appears or disappears and no block
  editor is open (small addition; the "Start writing" and "+" points are anchored to the section).
