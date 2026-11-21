# CR-455 debugger: T2 "preview scrolls with the replace-like diff" red in CI 44914183706

Repro: `gh workflow run ci.yml --ref chantier/batch-07/cr-455-... -f heavy=true` (job `integration`, step
`diff-preview`). Not reproducible locally (Windows, no xvfb VS Code); diagnosis is from code plus the CI log,
which only holds the timeout line (no focus or event trace).

## Cause (test bug, candidate a, with a focus root cause)

`src/host-vscode/activation.ts` ~l.408: the side preview is made with
`createWebviewPanel(PANEL_VIEW_TYPE, "Studio", ViewColumn.Beside, {...})`, no `preserveFocus`, so the new
webview group takes the workbench focus. In T2 the preview is opened AFTER the diff, then the test runs
`cursorBottom` (diffPreview.test.ts l.100) with the focus in the webview group: it moves no text editor,
no visible-range event fires, `lastSourceScrollLine` stays undefined/0 -> timeout. The preceding
asserts (active editor is the virtual side, preview ready, no text tab added) all pass without proving the
focus is back in the diff. T1 passes because there the diff is opened after the preview, so the diff's
`vscode.diff` call leaves the focus in the diff and `cursorBottom` scrolls the real (modified) side.
So T1 green-in-CI also proves (c) is false: diff real side -> visible-range event -> `syncEditorToPreview`
-> preview scroll works in a real window (side by side).

Secondary, by design (not the failure): `syncEditorToPreview` (scrollSync.ts l.137-147) only follows an
editor whose `document.id === preview.documentUri` (the `file:` one), so a scroll of the virtual side never
moves the preview directly; it works only if VS Code mirrors the scroll to the real side and fires that
editor's `onDidChangeTextEditorVisibleRanges` (likely in side by side, UNPROVEN). (b) is not shown by any
evidence: activation.ts l.194 forwards every visible-range event, hostEvents l.476 does not filter.

## Fix (test only)

In T2, after `previewOf(b.md)` and the no-tab assert, put the focus back on the diff and on the REAL side, which
is the original (left) one, then scroll it:
`await vscode.commands.executeCommand("workbench.action.compareEditor.focusPrimarySide")` (as T3/T5 do), wait for
`activeTextEditor.document.uri.scheme === "file"`, then `cursorBottom`. Scrolling the real side removes the
dependence on VS Code mirroring the virtual side's scroll. Do not use `focusFirstEditorGroup` (windowFocus.ts
l.112 note). Same fix wanted wherever the test acts after a Studio command with the diff expected focused.

## Remaining tests (read, not run)

- T3: focus is set explicitly (focusPrimarySide, waits for the virtual side) before the command: should pass.
- T5: `openDiff` then focusPrimarySide, then waits for the switch; `followActiveDiff` takes the modified file
  side: should pass. Note T3's command leaves the focus in the webview (`panel.reveal()` without
  preserveFocus, activation.ts l.397), but `vscode.diff` then reopens in the text group.
- T6: PASSES VACUOUSLY at risk: the preview exists, so the command ends with `panel.reveal()` (focus in the
  webview); `cursorBottom` then scrolls nothing, so "no scroll follows" would be true for the wrong reason.
  Add the focus-back step (and, ideally, an assert that `activeTextEditor` is the diff's side) before
  `cursorBottom`.
- Inline layout (second loop iteration), likely failure of T2 inline: with `renderSideBySide=false` the real
  file is the ORIGINAL side, which is not rendered as a separate editor (it is view zones in the modified
  editor), so no visible-range event of the real file can come from scrolling; `focusPrimarySide` is also
  not meaningful there. Either keep T2 side-by-side only (inline: only assert the preview opens and the
  replace-like shape opens no tab) or accept that the spec's "scroll with the real file's side" cannot hold
  for a real file on the original side in inline mode (document it as a limitation). T1 inline (real file on
  the modified side) should pass, unproven.
- `withLayout`'s `finally` restores `before` (undefined when unset): fine.

## Untested here
Everything real-window: the mirror of virtual-side scroll to the real side, inline-layout event behavior, T3/T5/T6.
