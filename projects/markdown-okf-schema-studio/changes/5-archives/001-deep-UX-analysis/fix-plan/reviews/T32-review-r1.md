# T32 review — round 1

Base: 29a3df8 · Reviewed diff: 5 files, +265/-2

## Gates
- compile, unit, types, contracts: PASS (logs/T32-*.log).
- full: FAIL once (logs/T32-full.log): RI-T21 `scenarioListEditorClickAndKeys`, "Timed out waiting
  for StRS-A.md to become the active text editor". This failure is not in the T00 baseline.
- trusted rerun: PASS (logs/T32-rerun-trusted.log). That is one clean rerun. Checklist item 12 needs
  two, and finding 1 gives a plausible T32 cause, so this failure is not proven flaky.
- visual: PASS vs baseline (0 new).

## Done-when
- [x] unit gate passes, with two new unit tests.
- [ ] RI-T32 passes "with before/after drift in the report". There is no "before" drift. The list
  case may pass on base code too (see finding 3). In the table case, the table is about 1050 px
  above the viewport when the commit is measured (rerun log: `Tcommit=-1049.2`). The
  `33-save-keeps-table-in-place` screenshot shows the top of the document with no table visible.
- [ ] R7 holds across the re-render after a save. It holds only for the first render after the
  save. It does not hold when a second render follows (finding 1, finding 2).
- [~] trusted/scroll: the trusted rerun passed. The full gate had one new failure, which is still
  unexplained.

## Protected features checked
- P-N1 R6, the initial anchor with no save: unchanged. The pin branch runs only when
  `context.initialPin` is set, and `takePendingPin` returns undefined when there was no final save.
  Covered by the existing scrollSync unit tests, which still pass.
- P-N1 R4, source-led scrolling: untouched.
- Echo guard: the pin restore uses `programmaticScroll`, so no `previewScroll` is posted. OK.
- P-S2 edit version checks: the pin is stored before dispatch, but it is never applied as an edit.
  Version checks are unchanged. OK.
- P-E8 read-only: no new controls. A read-only `previewEditSave` that carries a pin still stores
  `pendingPin` before the read-only rejection. This is harmless: the next render just pins the same
  element. See NIT 6.
- Webview template rules (§2): no backticks, no `${`, no global `setTimeout` in the added runtime
  code. OK.
- Message validation: `validPin` accepts the fields only on `previewEditSave` with `final === true`,
  and on `previewFrontmatterSave`. It requires a safe integer ≥ 1 and |top| ≤ 100000. OK.

## Orchestrator notes, answered
1. **Does the pin survive the next full re-assignment?** Partly. The note is refuted for
   enrichment and frontmatter refresh, and confirmed for a second render.
   - Link enrichment (`scheduleLinkEnrichment`), the frontmatter refresh and PlantUML injection all
     call `setPanelHtml(preview.webview.html …)`. That html still embeds the same serialized context
     (`JSON.stringify(context)`, scrollSync.ts:41), including `initialPin`. These reloads re-pin to
     the same spot, so they do not jump back.
   - A second `updatePreview` gets no pin, because `takePendingPin` already cleared it. It restores
     from `initialAnchorLine(preview)`, which is the host's `preview.anchor`. The webview never
     reports the pinned anchor:
     - `previewReady` carries `sourceLine` and `scrollTop`, but no `anchorLine`;
     - the pin scroll is silent;
     - so `preview.anchor` keeps the pre-pin value from the save message's `anchorField()`, shifted
       by `shiftAnchorsForEdits`.

     This is MAJOR (finding 1).
   - A second render is common. Autosave fires after 400 ms and a render takes about 1.2 s. One
     example: an autosave render is in flight when Mod+Enter is pressed. That is also open point 2
     (finding 2).
   - RI-T21 does several Enter presses and saves on a frontmatter list, measures the link box, then
     clicks. A second render that restores the stale anchor would move the link between the
     measurement and the click. That is plausible but not proven.
2. **No red-first.**
   - Both unit tests would fail on base. The `pinLine` field is absent there, and `initialPin` is
     ignored, so `scrollY` would not be 380.
   - RI-T32 list case: probably **not** red on base. The reading-line anchor sits in a filler
     paragraph above the list. Nothing above the list changes, so the base anchor restore puts the
     list at the same top anyway (drift 0 is expected on base too).
   - This is not acceptable as evidence for an interaction bug. See finding 3.
3. **Table measured at Enter.**
   - Nothing in T32's diff runs while typing. Pin fields are added only when `final` is true, and
     `restoreState` runs only on load. T32 cannot cause or worsen the scroll jump while typing.
   - Measuring at Enter does match the Goal's wording ("where it was when the user committed").
   - In practice, though, the table is about 1050 px off-screen at commit. The test then proves
     only that an invisible element keeps an off-screen offset, so the table case is not evidence
     of the Goal. See finding 4.
4. **An in-flight autosave render consumes the pin.** The risk is real and likely: type, then
   commit within about 1.6 s. The fix belongs in this task, because the Goal is "in the new render"
   after the commit. See finding 2.

## Findings
1. [MAJOR] src/webview/scrollSync.ts: the `previewReady` post (end of the runtime, after
   `restoreState()`). The host never learns the pinned anchor. A later `updatePreview` restores the
   pre-pin `preview.anchor`, which undoes R7.
   - **Fix.** When `restoreState` used the pin, add `...anchorField()` to the `previewReady`
     message, so it carries `anchorLine`. The host already stores `value.anchorLine` for any
     validated message, before the type dispatch (`handlePreviewSyncMessage`), so the host needs no
     change. Before you rely on that, check that `validAnchorLine` accepts `previewReady`.
   - Scope it to pin restores only. Have `restoreState` set a local flag `pinApplied`, and add
     `anchorLine` only when that flag is set. Loads without a pin then stay byte-identical (R6
     unchanged).
   - **Unit test.** Build the harness with `initialPin: { line: 50, viewportTop: 120 }`. Assert that
     the `previewReady` message has `anchorLine === lineAtScroll(380)` (the value the runtime set),
     and that a harness without `initialPin` sends no `anchorLine` on `previewReady`.
   - **E2E.** In RI-T32 (list case), after the current T1 check, trigger a second render with no
     pin and re-measure. For example, run `vscode.commands.executeCommand` for the refresh command,
     or apply a no-op-position edit far below through `WorkspaceEdit`, then `waitForRender`. Assert
     |T2 − T0| ≤ 3.
2. [MAJOR] src/extension.ts: `takePendingPin` / `updatePreview`. An earlier, in-flight render (an
   autosave build) consumes the pin, and the render of the final save then gets none.
   - **Fix, part 1.** When storing `pendingPin` in `handlePreviewSyncMessage`, add `minVersion`, set
     after the final edit is applied. The simplest form is
     `minVersion: (preview.document?.version ?? 0) + 1` when the final save changes text.
   - **Fix, part 2.** Better: set `preview.pendingPin.minVersion = document.version` right after
     the save's `applyEdit` resolves in the edit-save handler. If the final text equals the last
     autosave and no edit is applied, set `minVersion` to the current version.
   - **Fix, part 3.** In `takePendingPin`, return the pin **without clearing it** when
     `result.stage.activeDocumentVersion < pin.minVersion`. Clear it only when it is used on a
     render with version ≥ `minVersion`, or when it expires. Keep the 5 s expiry.
   - **Unit test.** If the extension host has a unit seam for `takePendingPin`, export it for tests
     and cover three cases:
     - a stage version below `minVersion` returns the pin and keeps it;
     - a stage version ≥ `minVersion` returns the pin and clears it;
     - an expired pin returns undefined.

     Otherwise cover it in RI-T32 with a new list sub-case: type `Frozen goods`, wait 700 ms (the
     autosave fires and a render starts), then press Mod+Enter at once, and assert the final T1
     within 3 px of T0.
3. [MAJOR] test/integration/realInput.test.ts: `scenarioSaveKeepsBlockInPlace`. Nothing shows that
   the list case fails on base. With the anchor in unchanged filler above the list, it most likely
   passes on 29a3df8.
   - **Fix.** Make the case one where base code drifts. Put the reading line **inside** the edited
     block, as in UX-11's observed 95 px drift: scroll so the list top is about 40 px below the
     viewport top, not in the middle. Or use a block whose growth moves content that crosses the
     reading line.
   - The orchestrator measures the base drift by running RI-T32 in a separate worktree checked out
     at 29a3df8 with only the test file copied in. This is not source swapping in the tree. Record
     that "before" drift (expected > 3 px) and the "after" drift in the report.
4. [MAJOR] test/integration/realInput.test.ts: the table sub-case. The commit happens with the
   table about 1050 px off-screen (`Tcommit=-1049`), and the screenshot shows no table. That does
   not demonstrate R7 for a visible table.
   - **Fix.** Keep the table close enough to the document top that typing does not trigger the
     unrelated jump. For example, use 8 filler paragraphs above instead of 40, with the table
     visible. Assert `0 <= Tcommit <= viewportHeight` before the drift check, so an off-screen
     commit fails loudly.
   - Measure the drift against T0 when Tcommit is within 3 px of T0. Otherwise keep the Tcommit
     reference and log both values.
   - Make sure the `33-…` screenshot shows the table.
5. [MINOR] RI-T21 new failure. After findings 1 and 2, run `PLAN/scripts/gate.sh T32-r2 full`
   twice. If RI-T21 still fails, add a short settle step in `scenarioListEditorClickAndKeys` before
   measuring the link box: wait for the link-enrichment reload, re-measure, and click only when two
   boxes taken 300 ms apart are equal. Report both runs.
6. [NIT] src/extension.ts: `handlePreviewSyncMessage`. `pendingPin` is stored before the read-only
   and type dispatch. Moving the store into the accepted `previewEditSave` (final) and
   `previewFrontmatterSave` paths would make the intent clearer. It is harmless as is.

## Existing assertions changed
None. `git diff 29a3df8 -- test/` shows only additions. OK.

VERDICT: CHANGES REQUESTED
