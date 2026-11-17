# T34 implementation — round 1

STATUS: DONE

## Summary
A ready render whose page shell is unchanged is now sent to the open webview as `previewContentPatch`
(new inner HTML of `#sphinx-myst-preview-content`, status, diagnostics, next identifiers, anchor/pin)
instead of a new `webview.html`. The runtime closes open editors without cancelling, replaces the
content, moves its identifiers, rebuilds the status region with `textContent`, runs
`initializeContent({ restore: true })`, rescans links, calls `contentReplaced()` and posts
`previewReady`. Anything unusual falls back to the full assignment (different shell, page not ready,
setting off, resource roots or startup settings changed, no acknowledgement within 2 s). PlantUML
diagram injection also patches in place. The kill switch is `markdownOkfSchemaStudio.preview.incrementalUpdates`.

## Default of `markdownOkfSchemaStudio.preview.incrementalUpdates` (D-10)
`true` (package.json and `DEFAULT_PREVIEW_CONFIGURATION`). Reason: every gate required by the task
passed with it on: `unit`, `types`, `contracts`, `trusted`, `scroll`, `reload`, `full` (two runs) and
`visual` (0 new failure lines vs baseline). The orchestrator may flip it to `false` after the review.

## Files changed
- `src/preview/contentPatch.ts` (new) — parse5-based `extractMainContent`, `shellKey`, `canPatch`, `planContentPatch`; plus small pure helpers the host uses: `runtimeContextKey`, `diagnosticsFitPatch`, `reportsReloadedDocument`, `reuseNonce`.
- `src/extension.ts` — setting read; patch path in `updatePreview`; `postContentPatch`; 2 s acknowledgement fallback; PlantUML patch in `scheduleDeferredPreviewWork`; `loadedContext`, `assignedRequestId`, `contentPatches` fields; test hooks `contentPatches`, `incrementalUpdates`.
- `src/configuration/previewConfiguration.ts` — `incrementalUpdates` (default true).
- `src/webview/scrollSync.ts` — `previewContentPatch` handler (`isValidContentPatch`, `applyStatusRegion`, `applyContentPatch`), `postPreviewReady()` extracted from the startup tail (same message).
- `src/preview/webview.ts` — exports `formatStatusDiagnostic` (the small export the amendment allows); `statusMarkup` uses it, output unchanged.
- `package.json` — one configuration property. `README.md` — one paragraph.
- Tests: `test/webview/contentPatch.test.ts` (new), `test/webview/scrollSync.test.ts`, `test/configuration/previewConfiguration.test.ts`, `test/security/package-contract.test.ts`, `test/integration/realInput.test.ts`.

## Tests written first (failing before the fix)
- Runtime unit tests (log `logs/T34-red-unit.log`, 11 of the 14 new runtime tests fail before the handler exists, e.g. `T34: a content patch replaces the content, moves the identifiers and posts previewReady` — `'' !== '<p>fresh</p>'`). The other 3 are guards that pass vacuously before and are caught by mutation (see below).
- RI-T34 against the old behaviour (patch path disabled by a temporary mutation of `updatePreview`, since restored; log `logs/T34-red-trusted.log`): `RI-T34 typing: 20 html assignments, 0 content patches` then `AssertionError: typing does not assign the webview document`.
- `contentPatch.test.ts` tests a new module, so they cannot fail "before" in a meaningful way.
- Mutation check of the runtime tests (9 mutations of `applyContentPatch`, each caught by at least one test): no `closeBlockEdit`, deferred markup kept, `pinApplied` not reset, no `rescan`, pending toggles kept, no status region, overlay not hidden, no `contentReplaced`, no `initialState` carry-over.

## Tests added or changed
- `contentPatch.test.ts` (12): extraction on a real `buildPreviewWebviewHtml` page (fake `vscode` module only supplies `Uri`); equal shell keys for different text, nonces, identifiers and statuses; different keys when Mermaid or math appears or disappears or the toolbar changes; PlantUML injection keeps the key; `canPatch` refuses `<script`/`nonce=`; status pages have no key; runtime-context key; status-line limits; reloaded-document detection; nonce reuse keeps shell and policy.
- `scrollSync.test.ts` (14 `T34:` tests): content/identifiers/attributes/`previewReady`; new identifiers only (and chained patches); 21 stale or malformed variants ignored; block editor closed without `previewEditCancel`/save; frontmatter editor closed and deferred markup dropped; overlay and link tooltip removed; status region built from plain text (no `innerHTML`, 0 or 1 optional children, first child of body when absent); open disclosures carried over; anchor and pin positioning equal to a freshly loaded page and the pin is for one render; scroll kept without anchor; pending checkbox toggles cleared; link target hints kept for known requests and new links discovered through `previewLinkDiscover`/`previewLinkTargets`; insertion points rebuilt in edit mode. Harness extensions (opt-in or neutral, startup trace test untouched and passing): `details`, `contentLinks`, `observedLinks`/`intersect`/`flushMicrotasks`, `dispatchedEvents`, `statusRegion`, `intersectionObserver` option, `initialAnchor` option, status query sees a rebuilt region.
- `previewConfiguration.test.ts`: new default test.
- RI-T34 (`realInput.test.ts`): Mermaid fixture, caret at the end; 20 characters at 60 ms; asserts `htmlAssignments === A0`, `contentPatches` grew, the same `Frame` is attached with a page marker intact, typed text shown, `data-sphinx-preview-request-id`/version equal to the host, one success status region, the diagram drawn again in the same frame (`img.myst-mermaid-image`), screenshot `34-content-patched`; then a 5 s render delay: overlay appears, the result lands as a patch, overlay gone, still 0 assignments; then the setting turned off through workspace configuration: typing assigns again, nothing is patched; the setting is restored.

## Existing assertions changed
- `test/configuration/previewConfiguration.test.ts`:"reads independent studio preview settings…" — old: `deepEqual(configuration, {…, stickyHeadingDepth: 2})` and the section set without the new key → new: both include `incrementalUpdates` (true) — required by: new setting (listed in the task).
- `test/security/package-contract.test.ts`:"contributes only opt-in … commands" — old: key list without the setting → new: list contains `markdownOkfSchemaStudio.preview.incrementalUpdates` — required by: new setting (listed).
- **Not listed in the task, decision needed:** `test/integration/realInput.test.ts` RI-T43 asserts one `htmlAssignments` per edit (fast and slow). With the default on that count is 0 (a patch is not an assignment). I did not change any RI-T43 assertion; `run()` now calls it as `withIncrementalUpdates(false, () => scenarioPendingOverlayWithoutReload(page, evidence))`, so it exercises the kill-switch (document assignment) path, and RI-T34 covers the slow render/overlay on the patch path. The reviewer may prefer another form.
- No assertion was deleted, skipped or weakened.

## Deviations from the task text (all small, each needed to keep a protected behaviour)
1. **`initialState` is not simply deleted.** The runtime sets `context.initialState = { openDisclosures }` (only when some `<details>` was open, else deletes it), so open sections survive the patch as they did through a reload. `sourceLine`/`scrollTop`/`focusedBlockId` are deliberately not carried (the live anchor is kept; restoring focus risks stealing focus from the text editor).
2. **The host record keeps the loaded page's nonce.** A patch cannot change the nonce of the loaded document, and `previewEditing.test.ts` (`previewFrame`) matches the frame's `script[nonce]` against the first `nonce="…"` of `getActivePreviewForTests().html`; with a fresh nonce per render that existing test timed out ("Timed out waiting for the rendered Studio webview", first trusted run). `preview.webview.html`/`nonce` therefore carry the nonce of the loaded page (`reuseNonce`); everything else in `html` is what a reload would show. Consequence for P-S1 "per-render nonce": the nonce is per loaded document, and a fallback reload from the record reuses it. No script can enter via the patch (`canPatch` refuses `<script` and `nonce=`; content is the host's sanitized render; status uses `textContent`). Please confirm this trade-off.
3. **Extra patch conditions** beyond the task: same document identity and source path as the previous stage; the startup settings of the runtime (`documentId`, `activeSourceFile`, the four scroll flags, `stickyHeadingDepth`) are unchanged (`runtimeContextKey`; a settings change refreshes the page through the full path, so P-L6 still holds; the page's own anchor toggle updates the loaded key); diagnostics fit the runtime limits.
4. **Link hints.** Before replacing the content the runtime collects `data-sphinx-preview-link-state`/`title` of the old links per request and re-applies them to the new links, then calls `linkNavigation.rescan()` (which `initializeContent({restore:true})` does not do). New requests are discovered through the existing observer path (unit-tested). Not solved: `rescan()` keeps its `discovered` set, so a known link is not asked again; its hint can stay stale until the next full load (for example a target created while typing). A one-line `discovered.clear()` in `linkNavigation.ts` `rescan()` would give reload parity at the price of a `findFiles` round trip per visible link per render; that file is outside the allowed list, so I left it (follow-up candidate).
5. **Recreated webview guard.** VS Code keeps the html of the last assignment; if it recreates the webview (for example when the editor moves to another window) it would load a page older than the patches. `previewReady` carrying the identifiers of the last assignment while the stage moved on makes the host assign the current html (`reportsReloadedDocument`; pure and unit-tested, not exercised end to end).
6. The status message sent is `status`, `label`, optional `message` (runtime supports it, the host never needs it today) and `diagnostics` as `{ severity, text }[]` per the amendment.

## Verification
- `gate.sh T34-impl unit types contracts` → PASS (unit 650/650, contracts 2/2): `logs/T34-impl-unit.log`, `-types.log`, `-contracts.log`
- `gate.sh T34-impl trusted` → first run FAIL (previewEditing nonce check, see deviation 2); after the fix PASS (`logs/T34-impl-trusted.log`)
- `gate.sh T34-impl scroll` → PASS (`logs/T34-impl-scroll.log`); `reload` → PASS (`logs/T34-impl-reload.log`)
- `gate.sh T34-impl full` → PASS twice: `logs/T34-impl-full-run1.log`, `logs/T34-impl-full-run2.log` (both show `RI-T34 typing: 0 html assignments, 20 content patches`)
- `gate.sh T34-impl visual` → PASS vs baseline, 0 new failure lines (`logs/T34-impl-visual.log`, screenshots `logs/visual-T34-impl`, tracked folder restored)
- Final state after restoring the red experiment: `gate.sh T34-final unit types contracts trusted` → all PASS (`logs/T34-final-*.log`)
- No known flake appeared. The screen was unlocked before every long gate. No gate or VS Code test process of mine is left running.

## Evidence for reviewers
- Screenshot: `.artifacts/real-input-*/34-content-patched.png` (newest directory, derived folder).
- Measured: RI-T30 now reports `0 html assignments, 10 ready renders`; RI-T43 (setting off) still reports `fast edit html assignments: 1`.
- Read the runtime handler in `scrollSync.ts` (`applyContentPatch`) and the patch decision in `updatePreview`; the order in the handler matters (editors closed, content replaced, context mutated, status rebuilt, `initializeContent`, `rescan`, `contentReplaced`, `previewReady`).

## Open points / STOP reason
- Decisions for the orchestrator/reviewer: the nonce trade-off (deviation 2), RI-T43 run with the setting off (existing-assertion note above), the stale link hint limit (deviation 4).
- Not covered end to end: the recreated-webview guard; patches of very large (near 20 MB) content; a hidden panel receiving a patch (covered indirectly by the existing hidden-preview scenario, which passed).
- `followups.md` was not touched (outside my allowed paths); the follow-ups above are in this report.
