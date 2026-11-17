# T02 review — round 2

Base: 52a79e0a642907ce83632e5fbdea328d99cc7f40 · Reviewed diff: 4 files, +582/-1
(`trusted-suite.ts` +7, `review-index.ts` +1/-1, new `realInput.test.ts` 245 lines, new
`realInput/harness.ts` 329 lines). No `src/` change. `checkboxToggle.test.ts` and
`previewEditing.test.ts` are untouched.

## Gates
- compile: PASS (`logs/T02-r2-compile.log`)
- unit: PASS. 355 tests, 321 pass, 0 fail, 34 todo, the same counts as T01 (`logs/T02-r2-unit.log`).
- trusted, on this harness revision:
  - implementer: 1 of 1 PASS (`logs/T02-impl-trusted.log`)
  - orchestrator: 4 of 5 PASS (`T02-r2`, `T02-r2c`, `T02-r2d`, `T02-r2e`). FAIL in `T02-r2b`, in `previewEditing`, not in the new suite.
  - reviewer: 2 of 2 PASS (`logs/T02-review-r2-trusted.log`, `logs/T02-review-r2b-trusted.log`). Each run logs the five `PASS real-input screenshot: 01…05` lines and 16 frontmatter captures. No fixture folders are left behind.
- T00 baseline: the trusted level had no known failures. `previewEditing` has now passed 10 of 11
  runs with the real-input suite before it (3 in round 1, 8 in round 2). The single failure is
  analysed below. It is a pre-existing race, and more than two clean reruns exist (checklist item 12).

## Answer to the round-2 question: the r2b failure is a pre-existing flake, not an order dependency

**What failed.** The failure is at `previewEditing.test.ts:449`, the first theme-toggle click of the
`white` iteration (compiled line 444). The call log reaches "done scrolling" and never reaches
"performing click action". So the frame was replaced before the click was sent; the click did not
replace it. The theme toggle cannot replace the frame, because it is client-side only: the host
branch `previewThemeModeChanged` only stores the mode (`extension.ts:1655-1659`). The click is a
retry-free action on a frame resolved once (`previewEditing.test.ts:447-450`), and
`previewFrame()` had just validated that frame against previewEditing's **own** preview: nonce,
document id, version and request id. Only an assignment of `panel.webview.html` on that new panel
replaces its inner frame.

**State the real-input suite leaves, and why none of it can assign that HTML:**

| Left behind | Effect on the next suite |
| --- | --- |
| Previews and webviews, including the Open With custom editor | All gone. `closeAllEditors()` calls `disposeActivePreviewForTests()`, which disposes every entry of `activePreviews` with its panel (`extension.ts:2496`). The deferred work (the link-enrichment timer and PlantUML) checks `preview.disposed` / `activePreviews.has` before writing HTML (`extension.ts:606-617, 714-740`). S5 awaits its final render before teardown. |
| A webview still reloading | No. S5 ends with `waitForRender` plus DOM waits, then the capture. |
| Open editors | None. The only real difference from pre-T02 is the editor-group layout. Before T02, group 2 still held `preview.md` and `preview-other.md` from earlier suites (screenshot `real-input-vxf4q4/01`), and previewEditing's preview opened as a tab in it. Now previewEditing creates group 2. A layout change repositions the overlay webview; it does not assign HTML. |
| FS events from deleting `realinput-s5-*` | `dependencyWatcher.onDidDelete` → `refreshReferencedPath` re-renders only for the active file or a `queue.dependsOn` path (`extension.ts:1869-1886`). `smoke.md` is neither for `finding.md`. |
| "Don't Save" revert of `smoke.md` | `refreshPreview` → the same `refreshReferencedPath` filter (`extension.ts:2269-2287`). No effect. |
| Active editor | None after `closeAllEditors`, so `followActiveEditor(undefined)` returns. |
| Edit mode | Per-webview `vscode.getState()` (`scrollSync.ts:83`), not host state. The new panel starts with edit mode off. |
| Theme, configuration, viewport, focus, keyboard | Theme and configuration: not touched. Viewport: previewEditing sets 2400×1100 itself. Focus: previewEditing calls `showTextDocument` first. Keyboard: the CDP session is closed by `browser.close()`, as in the checkbox suite, and `keyboard.press` releases every key. |

**Pre-existing trigger.** previewEditing writes `finding.md` and its whole fixture just before
opening the preview. The preview's `dependencyWatcher` (`**/*` under the workspace root, created in
`createPreview`, `extension.ts:2032-2050`) receives the create/change event for `finding.md`
whenever it arrives. `refreshReferencedPath` matches the active path and calls
`refreshPreviewDocument`. The queue then calls `setStatus("pending")` → `setPanelHtml`
(`extension.ts:772-777, 469-478`), which creates a new inner frame. If that event lands between
`previewFrame()` and the click, the run fails exactly like r2b. This is the UX-28 render churn.

**Corroboration:**
- The same race, the first interaction right after the first render of a freshly written fixture, hit the real-input suite four times during proofing. It hit in S1 (`T02-proof-s5-trusted.log`), whose predecessor is the unchanged checkbox suite, in S2 (`T02-diag`, `T02-proof-s4`) and in S5 (`T02-proof-s5b`). That is why the harness retries.
- In r2b, a `CodeWindow: failed to load (code -3)` line, an aborted webview load, appears inside S5. That happens in no other run during the real-input suite. It fits slower FS-event delivery in that run. The harness absorbed it; previewEditing could not.
- **Timing is unchanged.** previewEditing reaches its first capture 0.66–0.74 s after its start, both in pre-T02 runs (`frontmatter-e2e-RA2rNS`, `-KKFV5l`) and in T02 runs. The r2b run failed inside that same window (`frontmatter-e2e-iLfmYx`: started 14:24:01.200, completed 14:24:01.889).

**Conclusion:** I request no teardown change. The race belongs to previewEditing and the product
(see follow-up F1).

## Round-1 findings
| # | Status | Evidence |
| --- | --- | --- |
| 1 MAJOR, commit checks | Fixed | S1, S4 and S5 call `waitForRender` after the commit, then check the DOM (`realInput.test.ts:106-114, 183-189, 214-220`). The proof logs time out at the post-commit `waitForRender` with the commit action removed: `T02-proof-s1:302` (compiled line 106 in S1), `T02-proof-s4b:323` (S4), and `T02-debug3:762` (S5, where the preview stays at version 1 while the buffer is at version 3). The proofs ran on an earlier harness revision, but the commit waits are the same. |
| 2 MAJOR, macOS caret | Fixed | `caretToEnd` and `focusedCaret` are exported. S2 and S3 use `caretToEnd` plus `waitForCaretAtEnd`, and `${MOD}+End` is gone. The check passes trivially until T14, because D-21 already puts the caret at the end. That is accepted. |
| 3 MINOR, frame identity | Fixed | Returns `undefined` without a preview; the document-id check is at `harness.ts:116`. |
| 4 MINOR, detach in `waitFor` | Fixed | `harness.ts:47-56`; the pattern also covers "cannot find context". `waitForEditor` moved to the harness. **One call site added this round is still unprotected; see finding 1.** |
| 5–7 MINOR/NIT, JSDoc | Fixed | `closeAllEditors`, `capture`, `withCurrentFrame`. |
| 8 NIT | Note for T38 | Not a change here. |
| 9 NIT, gitignore | Open | Outside the allowed files. Carry it to `followups.md`. |

## Done-when
- [x] The trusted gate passes with the new suite, and the log shows the five scenario names. Evidence: the seven passing r2 runs above.
- [x] `.artifacts/REAL-INPUT-LATEST.md` says passed, and `real-input-vxf4q4/INDEX.md` lists five captures. Screenshots 01 and 05 show the committed text, with no open editor.
- [x] `rg -n "sendPreviewMessageForTests|\.fill\(" test/integration/realInput*` finds nothing. There is also no `dispatchEvent`, `postMessage`, `.focus(` or `locator.type`.
- [x] Registration and the review-index item are as specified (unchanged since round 1).

## Protected features checked
No product code changed.
- P-E2 (a click opens the exact block): covered by S1–S5 (paragraph, table cell, Open With).
- P-E3 (commit on blur and Cmd/Ctrl+Enter, re-render): now really covered. Blur by S1, Cmd/Ctrl+Enter in the side preview by S2, Cmd/Ctrl+Enter in Open With by S5. The proof logs show each check fails without its action.
- P-E4 (arrow navigation): covered by S3.
- P-E5 (table cell): Enter finalizes the cell (S4). The editor closes and `td` shows `one1`.
- P-L1 (side preview) and P-L2 (Open With): both exercised.
- P-R5 (checkbox): the checkbox suite is unchanged and passes.
- P-S2 (messages): no injected messages.
- Other suites: `previewEditing` now starts with an empty editor area (see the table above). The later suites pass in every run.

## Findings
1. [MAJOR] `test/integration/realInput/harness.ts`: `setEditMode`, lines 211-212. The first mode read
   is not detach-tolerant: `const frame = await currentPreviewFrame(page); if (await frame.locator("html").getAttribute(...) === wanted) return frame;`.
   - Every scenario, and every later task (T07–T28), calls `setEditMode` right after `waitForRender` on a freshly written fixture. That is exactly when a late FS event re-renders and replaces the frame.
   - This line already failed with `locator.getAttribute: Frame was detached` (`logs/T02-proof-s5-trusted.log:307`, S1).
   - The round-2 report says `setEditMode` "reads the mode through `withCurrentFrame`" and lists this flake as fixed. The code does not do that.

   Fix: in `setEditMode`, replace the two lines at the top of the loop with:
   ```ts
   const mode = await withCurrentFrame(page, (frame) =>
     frame.locator("html").getAttribute("data-sphinx-preview-edit-mode"));
   if (mode === wanted) return currentPreviewFrame(page);
   ```
   Change nothing else in the function. Proof:
   - (a) `rg -n "getAttribute|\.click\(|inputValue|evaluate" test/integration/realInput/harness.ts test/integration/realInput.test.ts`. Every hit must be inside a `waitFor` predicate, a `withCurrentFrame` action, `findCurrentFrame`, `focusedCaret` (called only from `waitFor`), or `capture` (called only through `withCurrentFrame`). List the hits in the report.
   - (b) Run `scripts/gate.sh T02-impl unit trusted` twice. Both runs must pass and show the five `PASS real-input screenshot` lines.
   - (c) In the report, correct the `setEditMode` sentence so that it describes the code.

## Follow-ups for `followups.md` (not blocking)
- **F1 (MINOR, pre-existing, needs user approval).** `previewEditing.test.ts` theme loops (lines
  447-450, 471-474, 502-505, 528-531) resolve the frame once and click without a detach retry. A
  late FS event for the freshly written `finding.md` can re-render the preview between
  `previewFrame()` and the click (r2b, 1 run in 11). The file is protected, so hardening it, for
  example by re-resolving `previewFrame(page)` inside the loop and retrying on
  `/frame.*detach|execution context was destroyed/`, needs the user's approval. The product root
  cause has two parts:
  - an FS create/change event on the active file re-renders even when the disk text equals the buffer;
  - every render reloads the webview (UX-28). T29 removes the pending-status reload and T34 the ready-render reload. Re-check this flake after T34.
- **F2 (NIT).** `test/integration/fixtures/realinput-*` is not gitignored (round-1 NIT 9).

## Existing assertions changed
None. `trusted-suite.ts` only gains lines (OK). The `review-index.ts` change only adds item 6 (OK).

VERDICT: CHANGES REQUESTED
