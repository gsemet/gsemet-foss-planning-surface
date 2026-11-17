# T38 implementation — round 1

STATUS: STOP

## Update after the third amendment (STOP 4: screen locked)
STATUS: STOP (environment). The three STOP-3 changes are applied in `test/integration/scroll-sync-suite.ts`:
- `capture()` "checkpoint sync control": expected `String(!scenario.includes("independent"))` ->
  `String(!scenario.includes("independent") && vscode.window.visibleTextEditors.length > 0)`; message text and the
  `sync:` field unchanged.
- `runBlockNavigation`: `if (await anchorButton.getAttribute("aria-pressed") !== "true") await anchorButton.click();`
  -> `assert.equal(await anchorButton.isDisabled(), true);`.
- keyboard-navigation callback: anchor `aria-pressed` expected `"true"` -> `"false"`, plus
  `assert.equal(await keyboardFrame.locator("[data-sphinx-preview-anchor]").isDisabled(), true);`.

`gate.sh T38-impl3 full` (log `logs/T38-impl3-full.log`): the whole scroll suite now PASSES (all solo-* and
paired-* scenarios and "PASS block keyboard navigation E2E"). The following `trusted` run then failed in
`checkboxToggle.test.js:171` ("Timed out waiting for one undo to restore the original source"). `ioreg` reports
`"CGSSessionScreenIsLocked"=Yes` right after the run: the screen is locked again, which is the documented cause of
exactly this failure (conventions §6). Per the conventions I did not chase it. `trusted` (including RI-T38 and its
screenshots) and `reload` therefore did not run. Please unlock the screen and rerun `gate.sh T38-impl4 full`
(no source change needed). `unit`, `types`, `contracts`, `visual` results are from the earlier gate (unchanged).

Note for the reviewer: `checkboxToggle.test.ts` presses the edit toggle to turn edit mode on (line ~152) and then
asserts `on`. If a persisted edit mode were on at its start, that click would turn it off. Each VS Code test host
starts with an in-memory workspace state, and checkboxToggle runs before `realInput`, so I expect no leak, but
the rerun will confirm.

## Update after the second amendment (STOP 3)
STATUS stays STOP. I applied exactly the amended scroll-suite change (solo half: no anchor click, assert disabled,
title, `aria-pressed=false`). `gate.sh T38-impl2 full` then passed `solo-reading-*` and `solo-editing-anchored/independent`
and failed in `solo-block-anchored` at the next anchor-dependent assertion, in code the amendment does not cover:

```
AssertionError [ERR_ASSERTION]: checkpoint sync control
'false' !== 'true'
  at capture (out/test/integration/scroll-sync-suite.js:257:16)  (log: logs/T38-impl2-full.log)
```

Cause: the `capture()` helper in `test/integration/scroll-sync-suite.ts` asserts
`state.anchored === String(!scenario.includes("independent"))` (`"checkpoint sync control"`). In the solo
half the anchor button is now disabled with `aria-pressed="false"`, so `solo-*-anchored` checkpoints fail. Same
class, not yet reached (suite stops at the first failure), in the same file:
- `runBlockNavigation` (keyboard-navigation fixture, opened with Open With, no text editor):
  `if (await anchorButton.getAttribute("aria-pressed") !== "true") await anchorButton.click();` clicks a
  disabled button (30 s timeout);
- the keyboard-navigation callback asserts `[data-sphinx-preview-anchor]` `aria-pressed === "true"`.

Needed amendment (orchestrator): in `capture()`, expect `"false"` when the preview has no paired text editor
(solo half, and the keyboard-navigation fixture); drop the anchor click in `runBlockNavigation` and expect
`isDisabled()` there instead of `aria-pressed === "true"`. Not run: `trusted` RI-T38 screenshots, `reload`
(the full gate stopped in the scroll suite; no persisted-edit-mode failure was seen).

Also applied in this attempt (existing assertion changed, per amendment 2), `test/integration/scroll-sync-suite.ts`:
- old `if (anchored) await anchorButton.click();` -> new `if (anchored && withSource) await anchorButton.click();`
- old `assert.equal(await anchorButton.getAttribute("aria-pressed"), String(anchored));` -> kept as is when
  `withSource`; otherwise `isDisabled() === true`, title `"No text editor shows this file"`, `aria-pressed === "false"`.
- Verification: `gate.sh T38-impl2 full` -> FAIL (`logs/T38-impl2-full.log`), see above.

## Summary
The feature is implemented: anchor pairing (disabled button plus tooltip, `previewPairing` message), edit mode
remembered per workspace (`previewEditModeChanged` to `workspaceState`, `initialEditMode` in the context, saved
webview state wins, read-only never starts in edit mode), chain-link icon, README, unit tests, RI-T38, and the
edit-mode teardown in `realInput.test.ts`. The amended assertion was applied.
`unit`, `types`, `contracts` and `visual` pass. `full` fails in the scroll suite, a file outside the Allowed
files, because the scroll suite clicks the anchor button in a preview that has no text editor. This is the
intended D-16 behaviour, not an edit-mode leak. I stopped as required (conventions §9.1/§9.2).

## STOP reason
`full` log: `logs/T38-impl-full.log`, thrown from `out/test/integration/scroll-sync-suite.js:425`
(`test/integration/scroll-sync-suite.ts`, loop `for (const withSource of [false, true])`):

```
locator.click: Timeout 30000ms exceeded.
  - locator resolved to <button disabled ... aria-pressed="false" data-anchor-mode="on" data-sphinx-preview-anchor=""
      title="No text editor shows this file" ...>
  - 57 x waiting for element to be visible, enabled and stable: element is not enabled
```

In the "solo" half (`withSource === false`: Open With editor only, `visibleTextEditors.length === 0`, asserted by
the suite itself), scenario `solo-*-anchored` runs `if (anchored) await anchorButton.click();` and then asserts
`aria-pressed === "true"`. With T38 the anchor button is disabled whenever no text editor shows the file, so the
click can never succeed. The suite needs an adaptation, outside this task's Allowed files. Possible options for
the orchestrator:
1. Amend T38 to allow `test/integration/scroll-sync-suite.ts`: in the solo half, skip the anchor click and assert
   the button is disabled (the "anchored" solo scenarios then check scrolling without pairing); or
2. change the design so a disabled button keeps its `aria-pressed` state (no help for the click itself).

Not caused by a persisted edit mode: the failing step is the anchor click. Because `full` stops at the first
failing suite, the later suites of `full` (including `reload`, and possibly `trusted`) did not run in this gate.
Their result with T38 is unknown. No leaked edit mode was observed in `visual`.

## Files changed
- `src/extension.ts` — `previewEditModeChanged` message type and `editMode` field,
  validated in `isPreviewSyncMessage` (boolean, this type only); host stores it in
  `workspaceState["markdownOkfSchemaStudio.editMode"]` (ignored when read-only); `scrollContext` takes
  `{pairedTextEditor, initialEditMode}` (`initialEditMode` only when `!preview.readOnly`); `notifyPairing` plus an
  `onDidChangeVisibleTextEditors` subscription posts `previewPairing`; storage cleared in `deactivate`.
- `src/webview/scrollSync.ts` — context fields; `applyPairing` (disabled, title,
  data-tooltip and aria-label, `aria-pressed=false` while unpaired so the pressed colour is not shown, restores
  through `applyAnchorMode`); edit mode init (saved state wins, then `initialEditMode`, off without a toggle);
  the toggle posts `previewEditModeChanged` synchronously, just before `applyEditMode`, so a block save posted by
  leaving edit mode stays the last message; handles `previewPairing`.
- `src/preview/previewToolbar.ts` — chain-link icon (two links, 24x24, same stroke).
- `README.md` — two sentences.
- `test/webview/scrollSync.test.ts` — harness config type, 5 T38 tests, amended assertion.
- `test/integration/realInput.test.ts` — RI-T38 (`scenarioToolbarState`, registered last);
  `leaveEditModeOff()` before each of the 4 `closeAllEditors()` teardown sites (uses a module-level page set in
  `run()`, because `withDocument` has no page parameter; 250 ms wait so the host receives the message first).

## Tests written first (failing before the fix)
No red-first run was recorded (I implemented before running them, and swapping sources is forbidden). Reasoning
against base `0d0ada9` (`git show 0d0ada9:src/webview/scrollSync.ts`
contains none of `previewPairing`, `initialEditMode`, `previewEditModeChanged`; its `editMode` initialiser is
`savedState?.editMode === true`; `applyAnchorMode` is the only anchor state writer):
- "an unpaired preview disables the anchor button..." — fails on base: `pairedTextEditor` is ignored, button is
  not disabled, no `previewPairing` handler.
- "a paired preview keeps ... foreign previewPairing is ignored" — passes on base (guards the new handler);
  regression guard only.
- "edit mode starts from the workspace choice..." — fails on base: `initialEditMode: true` is ignored, mode is off.
  (The saved-state and default sub-cases pass on base.)
- "a read-only preview never starts in edit mode" — passes on base (guard).
- "toggling edit mode posts previewEditModeChanged" — fails on base: no such message.
- Amended assertion in "turning edit mode off saves a changed block editor..." — fails on base (no
  `previewEditModeChanged` is posted, the slice is empty).
- RI-T38 — would fail on base: the anchor button is never disabled and a reopened preview starts with edit mode off.

## Tests added or changed
See the list above. RI-T38 has not run to completion: the `full` run stopped in the scroll suite. Whether
`trusted` (which holds `realInput`) ran before the scroll suite is not shown in the log; check
`logs/T38-impl-full.log` for the RI-T38 line before relying on it.

## Existing assertions changed
- `test/webview/scrollSync.test.ts`: "turning edit mode off saves a changed block editor and ignores an unchanged one"
  — old: `assert.equal(unchanged.messages.length, messageCount);` — new:
  `assert.deepEqual(unchanged.messages.slice(messageCount).map((message) => message.type), ["previewEditModeChanged"]);`
  — required by: every edit-toggle click now posts `previewEditModeChanged` (task amendment).
- No assertion on the padlock markup existed.

## Verification
- `scripts/gate.sh T38-impl unit types contracts full visual`:
  - unit PASS (log `logs/T38-impl-unit.log`), types PASS, contracts PASS
  - full FAIL (`logs/T38-impl-full.log`): scroll suite, anchor click on a disabled button (see STOP reason)
  - visual: PASS vs baseline (0 new failure lines, 0 baseline lines now passing, 0 moved coordinates)

## Evidence for reviewers
- Persisted edit mode: no new visual or scroll failure caused by it. The `full` failure is the disabled anchor.
- RI-T38 screenshots `38-anchor-disabled`, `38-anchor-enabled`, `38-edit-mode-remembered` are only produced if
  the trusted suite reached RI-T38 (check the real-input evidence folder).

## Open points
- Decide how the scroll suite should handle the disabled anchor (option 1 above), then rerun `full` including
  `reload`.
