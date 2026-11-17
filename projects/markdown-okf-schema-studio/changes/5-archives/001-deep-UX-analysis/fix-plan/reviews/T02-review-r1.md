# T02 review — round 1

Base: 52a79e0a642907ce83632e5fbdea328d99cc7f40 · Reviewed diff: 4 files, +462/-1
(`trusted-suite.ts` +7, `review-index.ts` +1/-1, new `realInput.test.ts` 210 lines, new
`realInput/harness.ts` 244 lines). No `src/` change; `checkboxToggle.test.ts` and
`previewEditing.test.ts` are untouched.

## Gates
- compile: PASS (`logs/T02-compile.log`, `logs/T02-review-compile.log`)
- unit: PASS. 355 tests, 321 pass, 0 fail, 34 todo, the same as T01 (`logs/T02-unit.log`, `logs/T02-review-unit.log`)
- trusted-build: PASS (`logs/T02-trusted-build.log`)
- trusted: PASS 33 s in three independent runs: implementer (`logs/T02-impl-trusted.log`),
  orchestrator (`logs/T02-trusted.log`) and reviewer (`logs/T02-review-trusted.log`). Each run logs
  the five `PASS real-input screenshot: 01…05` lines.
- Compared with the T00 baseline, the trusted level has no new failures. The T00 baseline records
  no trusted failures.

## Done-when
- [x] The trusted gate passes with the new suite, and its log shows the five scenario names. Evidence: the three logs above.
- [x] `.artifacts/REAL-INPUT-LATEST.md` says passed, and its `INDEX.md` lists five captures. Evidence: `real-input-5YG3uR/INDEX.md` and `real-input-SFUaas/INDEX.md` (reviewer run).
- [x] `rg -n "sendPreviewMessageForTests|\.fill\(" test/integration/realInput*` finds nothing. I also found no `dispatchEvent`, `postMessage`, `.focus()` or `.type()` on a locator.
- [x] The harness exports the whole API in the task, plus `findCurrentFrame` and `withCurrentFrame`, which the report justifies. `writeSchema` matches the `_schema/<type>.schema.yaml` layout in `previewEditing.test.ts`.
- [x] Registration follows the spec: one try/catch block right after the checkbox block, with the required `console.error` text. The review index gains item 6 only; a word diff shows no other change on that line.
- [~] The goal says the smoke scenarios "protect P-E2, P-E3, P-E4 and P-E5". **They do not protect blur commit, Enter in a table cell, or Cmd/Ctrl+Enter in the Open With editor** (finding 1). The step `${MOD}+End` **does nothing on macOS** (finding 2).

## Protected features checked
No product code changed, so a product regression is not possible. I checked whether the new tests
really cover each area the task names:
- P-E2 (a click opens the exact block): covered for a paragraph, a table and a table cell. S1–S5 wait for the right editor.
- P-E3 (autosave to the buffer, commit on blur and Cmd/Ctrl+Enter, re-render): only Cmd/Ctrl+Enter in the side preview is covered (S2: `waitForRender` only becomes true after the final save, then no editor is open). **Blur (S1) and Cmd/Ctrl+Enter in the Open With editor (S5) are not covered.** See finding 1.
- P-E4 (arrow navigation): covered by S3. Its wait cannot pass before ArrowDown, because the textarea first holds `Second paragraph.`.
- P-E5 (table cell editing): S4 covers that one cell changes and the row count stays the same. **Enter finalizing the cell is not covered** (finding 1).
- P-L1 (side preview) and P-L2 (Open With editor): both are exercised (S1–S4 and S5).
- P-R5 (checkbox): `checkboxToggle.test.ts` is unchanged and still passes before the new suite.
- P-S2 (messages): actions never inject messages.
- Effect on the other suites: the existing order is unchanged. One side effect remains:
  `closeAllEditors()` closes every editor that earlier suites left open and discards their dirty
  buffers. Screenshot 01 shows `feature-contract.md` (dirty, from `projectFeatures`), `preview.md`
  and `preview-other.md` still open. VS Code's extension-test mode answers "Don't Save", so no file
  changes on disk (`git status` is clean for the fixtures). The later suites pass in all three
  runs. Edit mode is per-webview state (`vscode.getState().editMode` in `scrollSync.ts`), not
  per-workspace state as the report claims, so it does not leak into `previewEditing`. I accept
  this side effect.

## Findings

1. [MAJOR] `test/integration/realInput.test.ts`: `scenarioParagraphBlurCommit`,
   `scenarioTableCellEnter`, `scenarioOpenWithEditor`. These scenarios do not check the commit
   action they are named for.
   - Why: every keystroke already autosaves. Both `textarea` and the cell `input` have an `input`
     handler that calls `autosaveBlockEdit()`, which sends `previewEditSave` with `final: false`.
     The host's `drainActiveBlockEdit` applies that save to the buffer, so the buffer reaches the
     expected text before the heading click, before Enter and before Cmd/Ctrl+Enter.
   - Result: S1 would pass with the textarea `blur` handler removed. S4 would pass if Enter did
     nothing. S5 would pass if Cmd/Ctrl+Enter did nothing. T08, T09 and T10 rework exactly these
     paths, and these smoke tests would not catch a regression there.
   - Why `waitForRender` is the evidence: a non-final autosave applies without re-rendering, because
     `refreshPreview` skips while `activeBlockEdit.applying`. So `waitForRender(document)` only
     succeeds after the final save (`completeActiveBlockEdit` → `refreshPreviewDocument`). S2
     already relies on this.

   Fix: right after the existing buffer `waitFor` in each of the three scenarios, add
   `await waitForRender(document);` and then a `waitFor` on the current frame (use `findCurrentFrame`):
   - S1: `p` with `hasText: "Second paragraph. Added."` has count 1, and no
     `[data-sphinx-preview-block-editor] textarea` value contains `"Second paragraph"`. Read the
     values with `locator.evaluateAll((areas) => areas.map((a) => (a as HTMLTextAreaElement).value))`;
     this is a read, so it is allowed.
   - S4: `[data-sphinx-preview-table-cell-editor]` has count 0, and
     `td` filtered with `hasText: /^one1$/u` has count 1.
   - S5: `[data-sphinx-preview-block-editor]` has count 0, and `p` with `hasText: "Second paragraph. Z"` has count 1.

   Prove each new check works:
   1. Comment out the commit action locally: the heading click in S1, `press(page, "Enter")` in
      S4, and `press(page, \`${MOD}+Enter\`)` in S5.
   2. Run `scripts/gate.sh T02-impl trusted` and confirm that each scenario now times out at the
      new wait. Copy the three timeout lines into the report.
   3. Restore the actions.

2. [MAJOR] `test/integration/realInput.test.ts`: `scenarioCtrlEnterCommit` (line 108) and
   `scenarioArrowNavigation` (line 134) press `${MOD}+End`, which does nothing on macOS, the
   platform the gates run on.
   - Evidence: I ran a probe with playwright-core 1.63.0 on darwin (Chromium, a textarea with three
     lines, caret at 0). `End` moves the caret to the end of the line. `Meta+End` and `Control+End`
     leave it at 0. `Meta+ArrowDown` moves it to the end of the document.
   - Playwright only maps `Meta+ArrowDown` to `moveToEndOfDocument` on Mac (see `crInput`
     `_commandsForCode`).
   - The scenarios pass today only because D-21 puts the caret at the end of the block. Once T14
     ("caret lands where the user clicked") lands, S2 can type ` X` after `line one` and fail for
     a reason unrelated to the product. Later tasks will also copy this pattern.

   Fix:
   - (a) In `realInput/harness.ts`, add and export
     `async function caretToEnd(page: Page): Promise<void>`. It presses `"Meta+ArrowDown"` when
     `process.platform === "darwin"` and `"Control+End"` otherwise, and its JSDoc says why.
   - (b) Add and export `async function focusedCaret(frame: Frame): Promise<{ start: number; end: number; length: number } | undefined>`.
     It reads `document.activeElement` through `frame.evaluate`. It returns `undefined` when the
     active element is not a `textarea` or `input`; otherwise it returns `selectionStart`,
     `selectionEnd` and `value.length`.
   - (c) In S2 and S3, replace `press(page, \`${MOD}+End\`)` with `await caretToEnd(page);`
     followed by `await waitFor("the caret at the end of the editor", ...)`. The predicate
     resolves `findCurrentFrame(page)` and requires `start === length && end === length`.
   - (d) Run the trusted gate. The new wait proves on macOS that the key worked.

   Neither key reaches block navigation, because `boundaryNavigation` ignores events that have
   `metaKey` or `ctrlKey`.

3. [MINOR, fix in this round] `realInput/harness.ts`: `findCurrentFrame` matches only document
   version and request id.
   - The `requestId` comes from a per-preview counter (`BuildQueue.requestCounter` starts at 0), so
     two fresh Studio webviews both carry version 1 and request id 1.
   - With a side preview and an Open With editor visible at the same time, the lookup can return
     the wrong frame. Later lifecycle and entry-point tasks will show both.

   Fix: inside the loop, add
   `if (await root.getAttribute("data-sphinx-preview-document-id") !== preview?.documentUri) continue;`.
   The runtime sets this attribute to `context.documentId`, which is `preview.documentUri`. Also
   return `undefined` immediately when `preview` is `undefined`.

4. [MINOR, fix in this round] `realInput/harness.ts`: `waitFor` lets a frame-detach error escape.
   - Predicates such as `waitForEditor`, the S2 and S3 waits, and the wait inside `setEditMode`
     call `findCurrentFrame` and then a locator method on that frame.
   - A render that replaces the frame between those two calls throws
     `Frame was detached` / `Execution context was destroyed` and fails the scenario instead of
     polling again. The implementer already hit this error once on a click.

   Fix: in `waitFor`, wrap `await predicate()` in try/catch. On an error matching
   `/frame.*detach|execution context was destroyed/iu`, treat the result as `false` and keep polling;
   rethrow any other error. Also move `waitForEditor` from the suite into the harness and export it,
   because every later task needs it.

5. [MINOR] `realInput/harness.ts`: `closeAllEditors`.
   - The spec says "revertAndCloseActiveEditor for the fixture". The code reverts whatever
     `vscode.window.activeTextEditor` is. That is usually `undefined` after a click in the webview,
     so nothing is reverted explicitly.
   - Cleanup works only because VS Code's extension-test mode answers "Don't Save" when
     `workbench.action.closeAllEditors` meets dirty editors.
   - It also closes and discards editors that earlier suites left open, as described above.

   Acceptable now, but document both facts in the function's JSDoc. Optional: revert dirty documents
   under `liveFixtureDirectories` explicitly before closing: `showTextDocument(document)`, then
   `workbench.action.revertAndCloseActiveEditor`.

6. [MINOR] `realInput/harness.ts`: `createEvidence().capture` changes state. It calls
   `window.scrollTo(0, 0)`, moves the mouse to the bottom-left corner of the frame, and blurs the
   toolbar buttons.
   - This is harmless after the final action, which is where this task calls it. Called in the
     middle of a scenario, it would disturb the scroll anchor, hover states (T15) and anything
     located below the first screen.
   - Fix: add a JSDoc to `capture` saying it must be called only after the scenario's last action
     and what it changes. Optional: add an `options?: { keepView?: boolean }` that skips the
     scroll and the mouse move.

7. [NIT] `withCurrentFrame` retries an action after a detach error. If the frame detached after
   the input was dispatched, the action runs twice. Today that would fail loudly (the edit toggle
   would flip back, and `setEditMode` would time out). Add one JSDoc line: only wrap actions that
   are safe or loud to repeat.

8. [NIT] The report's open point says edit mode "persists per workspace, and the checkbox suite
   leaves it on". That is inaccurate: today it is per-webview `vscode.getState()`. Followup for
   T38, which makes edit mode persist per workspace: the real-input suite must then turn edit mode
   off in `finally`, or `previewEditing` will start with edit mode on.

9. [NIT] `test/integration/fixtures/realinput-*` is not gitignored, the same as `checkbox-e2e-*`. A
   killed run would leave untracked fixture folders.

## Existing assertions changed
None. `trusted-suite.ts` only gains lines (OK). The single `review-index.ts` line is the whole
review template literal; the only change in it is the added item 6 (OK, the task allows it).

VERDICT: CHANGES REQUESTED
