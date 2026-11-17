# T02 review — round 3

Base: 52a79e0a642907ce83632e5fbdea328d99cc7f40 · Reviewed diff: 4 files, +583/-1
(`trusted-suite.ts` +7, `review-index.ts` +1/-1, new `realInput.test.ts` 245 lines, new
`realInput/harness.ts` 330 lines). No `src/` change. `checkboxToggle.test.ts` and
`previewEditing.test.ts` are untouched.

Round-3 delta: only `realInput/harness.ts` changed, by +1 line (329 to 330), in `setEditMode`.
Modification times confirm the rest. `harness.ts` changed at 17:14:19, after the round-2 review
(17:13:42). `realInput.test.ts` (16:21), `trusted-suite.ts` (15:57) and `review-index.ts` (15:57)
have not changed since round 2.

## Gates
All runs below used this revision; every log is newer than the 17:14:19 harness edit.
- compile: PASS (`logs/T02-r3-compile.log`, `logs/T02-review-r3-compile.log`).
- unit: PASS. 355 tests: 321 pass, 0 fail, 34 todo. These are the same counts as T01 and round 2
  (`logs/T02-r3-unit.log`, `logs/T02-impl-unit.log`, `logs/T02-review-r3-unit.log`).
- trusted-build: PASS (`logs/T02-r3-trusted-build.log`, `logs/T02-r3b-trusted-build.log`,
  `logs/T02-review-r3-trusted-build.log`).
- trusted: PASS 5 of 5. Each run exits 0 and logs the four checkbox captures, the five
  `PASS real-input screenshot: 01…05` lines and the 16 frontmatter captures. No run logs
  `integration failed` or a detach error.
  - implementer: `logs/T02-r3a-trusted.log`, `logs/T02-impl-trusted.log`
  - orchestrator: `logs/T02-r3-trusted.log` (39 s), `logs/T02-r3b-trusted.log` (40 s)
  - reviewer: `logs/T02-review-r3-trusted.log` (40 s), one run only, as instructed
- T00 baseline: the trusted level has no known failures, and there is no new failure. The
  `previewEditing` flake from round 2 (F1) did not recur in these five runs.

## Round-2 finding
| # | Status | Evidence |
| --- | --- | --- |
| 1 MAJOR, `setEditMode` first read not detach-tolerant | **Fixed as specified** | `harness.ts:211-213`: `const mode = await withCurrentFrame(page, (frame) => frame.locator("html").getAttribute("data-sphinx-preview-edit-mode")); if (mode === wanted) return currentPreviewFrame(page);`. The rest of the function is unchanged: up to 3 clicks through `withCurrentFrame`, then a 1.5 s `waitFor` that reads through `findCurrentFrame`. The read is idempotent, so a retry inside `withCurrentFrame` is safe. Proof (a): I reran the `rg` myself and got the same 18 hits as the report. Each hit is in an allowed context: `findCurrentFrame` (116-118, inside its own try/catch), `focusedCaret` (154; its only caller is the `waitFor` predicate at `realInput.test.ts:51`), `setEditMode` (212 `withCurrentFrame`, 215 `withCurrentFrame`, 220 `waitFor`), `capture` (270/275/283; its only caller is `captureAfter`, which wraps it in `withCurrentFrame`), the test clicks (95, 99, 126, 150, 174, 203, all inside `withCurrentFrame`) and the test reads (112, 161, both `waitFor` predicates). Proof (b): two gate runs passed (above). Proof (c): the report's sentence about `setEditMode` now describes the code. |

## Earlier findings: still fixed
| Round / # | Status | Evidence in the current code |
| --- | --- | --- |
| r1-1 MAJOR, commit checks | Still fixed | S1 `realInput.test.ts:106-114`, S4 `:183-189` and S5 `:214-220` call `waitForRender` after the commit, then check the DOM. Unchanged since round 2. |
| r1-2 MAJOR, macOS caret | Still fixed | `caretToEnd` (`harness.ts:143-145`) and `focusedCaret` (`:151-165`). S2 and S3 call `caretToEnd` then `waitForCaretAtEnd` (`:128-129`, `:152-153`). `rg 'MOD\}\+End'` finds nothing. |
| r1-3 MINOR, frame identity | Still fixed | `harness.ts:108` (`undefined` when there is no preview) and `:116` (document-id check). |
| r1-4 MINOR, detach in `waitFor` | Still fixed | `harness.ts:47-56`. `waitForEditor` is in the harness (`:128-135`). |
| r1-5/6/7 JSDoc | Still fixed | `closeAllEditors` `:318-323`, `capture` `:263-268`, `withCurrentFrame` `:178-183`. |
| r1-8 NIT, T38 note | Carried as follow-up F3 below | — |
| r1-9 / r2-F2 NIT, gitignore | In `followups.md` | — |
| r2-F1 MINOR, previewEditing flake | In `followups.md` | — |

## Done-when
- [x] The `trusted` gate passes with the new suite included, and its log shows the five scenario names. Evidence: the five round-3 runs listed above.
- [x] `.artifacts/REAL-INPUT-LATEST.md` says passed, and `INDEX.md` lists five captures. Evidence: after the orchestrator's last run, `REAL-INPUT-LATEST.md` linked `real-input-QhjI3g/INDEX.md`, and after my run it links `real-input-MdiSa7/INDEX.md`. Both index files list 01–05. In screenshot `real-input-MdiSa7/05-open-with-editor.png`, the Open With editor shows `Second paragraph. Z`, edit mode is on and no block editor is open.
- [x] `rg -n "sendPreviewMessageForTests|\.fill\(" test/integration/realInput*` finds nothing. There is also no `dispatchEvent`, `postMessage`, `.focus(` or `locator.type`. The only `.type(` hit is `page.keyboard.type` in `typeText`, which the specification requires.
- [x] The harness API, the scenario steps, the registration (`trusted-suite.ts:86-91`, after the checkbox block, with the required `console.error` text) and review-index item 6 all match the task. None of them changed this round.

## Protected features checked
No product code changed, so a product regression is not possible. The new suite still covers these
protected features:
- P-E2 (a click opens the exact block): S1–S5 (paragraph, table, table cell, Open With).
- P-E3 (commit on blur and on Cmd/Ctrl+Enter, then re-render): blur in S1, Cmd/Ctrl+Enter in the side preview in S2, Cmd/Ctrl+Enter in Open With in S5. Each commit is checked with `waitForRender` and the DOM.
- P-E4 (arrow navigation): S3.
- P-E5 (table cell, Enter finalizes): S4.
- P-L1 (side preview) and P-L2 (Open With editor): both are exercised.
- P-R5 (checkbox): the checkbox suite is unchanged and passes its 4 captures in every run.
- P-S2 (messages): no injected messages.
- The later suites (`previewEditing` and the rest of `trusted`) pass in all 5 runs.
- After my run, no `realinput-*` fixture folder was left behind, and `git status` lists only the four T02 files.

## Findings
None blocking. I found no new BLOCKER or MAJOR in code unchanged since round 2.

Note on the report: the transient `realInput/frontmatter-e2e-yNnrMy/` entry it mentions does not
come from the harness. The harness writes only to `.artifacts/real-input-*` and
`test/integration/fixtures/realinput-*`. `frontmatter-e2e-*` folders are created by
`previewEditing.test.ts:210` under `.artifacts`, which is ignored. My run left no such folder. It was
most likely a misread of condensed `git status` output. No action.

## Follow-ups for `followups.md` (not blocking)
- **F3 (NIT, for T38).** Round-1 NIT 8 is not yet in `followups.md`. Today edit mode lives in each
  webview's `vscode.getState()`, so it does not leak between suites. T38 makes edit mode persist
  per workspace. When it does, `realInput.test.ts` must turn edit mode off before teardown, for
  example with `setEditMode(page, false)` inside each scenario's `finally` before
  `closeAllEditors()`, or `previewEditing` will start with edit mode on. Add this line to T38's
  task file or to `followups.md`.

## Existing assertions changed
None. `trusted-suite.ts` only gains lines (OK). The `review-index.ts` change only adds item 6 (OK,
the task allows it).

VERDICT: PASS
