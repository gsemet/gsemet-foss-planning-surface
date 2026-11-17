# T15 implementation — round 1

STATUS: DONE

## Summary
Edit mode now outlines (dashed `outline`, no layout shift) the element a click would edit, via
`mouseover`/`mouseout`/`focusin`/`focusout` listeners and `setEditHover`/`editHoverTarget` in the
runtime (list -> the `ul`/`ol` that `editingElementFor` returns, `pre` for code, the cell inside a
table). The raw-Markdown block editor has a frame and background, an editor monospace font with
`tab-size: 4` (frontmatter YAML textarea too, not `data-okf-text-value`), a hint line
(`Lines 50–52 · Enter: new line · Tab: indent · Esc or ⌘↩: done`, `Ctrl+Enter` off macOS) and Done/Revert
buttons. Revert is disabled until the text differs or an autosave reached the document; it calls
`closeBlockEdit(true)` only after an autosave, else `closeBlockEdit(false)`. Both buttons
`preventDefault` on `mousedown` so the textarea blur-commit does not fire first.

## Files changed
All under ``:
- src/webview/scrollSync.ts — hover helpers and listeners, `blockEditHint`, buttons, Revert logic, `closeBlockEdit` comment.
- src/preview/previewStyles.ts — hover outline, framed `.sphinx-preview-block-editor` (`::before` marker removed), editor font on block and YAML textareas.
- test/webview/scrollSync.test.ts — new tests, harness `closest` extended for `ul, ol` and `[data-sphinx-preview-block-editor]`.
- test/webview/previewStyles.test.ts — see "Existing assertions changed".
- test/integration/realInput.test.ts — RI-T15 (`scenarioEditAffordances`).
- test/visual/scenarios.ts — scenario `edit-affordances-hover-and-open` (+ `editAffordances` field).
- test/visual/capture.py — `check_edit_affordances` for the new scenario; one existing check updated.
- README.md — "Edit mode" paragraph rewrapped at 100 columns, hover/Done/Revert sentences added.

## Tests written first (failing before the fix)
- Unit run before any src change (`logs/T15-impl-pre-unit.log`): failing were the 4 new scrollSync tests
  (hover, hint + buttons, Revert, Done), the 3 new previewStyles tests, and the two changed existing ones.
  Excerpt: `✖ edit mode hover marks the whole list that a click would edit`, `✖ an opened block editor shows its line range, Done and a disabled Revert`.
- RI-T15 against the unmodified src/webview/scrollSync.ts and previewStyles.ts (HEAD copies swapped in for one run, then restored;
  `logs/T15-pre-trusted.log`): `Real-input integration failed: Error: Timed out waiting for the hovered list to carry the outline attribute.`

## Tests added or changed
- scrollSync: "edit mode hover marks the whole list that a click would edit" (edit mode on sets it on the `ul`, off sets nothing; mouseout/focusout/edit-off clear it).
- scrollSync: "an opened block editor shows its line range, Done and a disabled Revert" (`Lines 50–52`, platform key text, Revert disabled).
- scrollSync: "Revert enables on change and cancels only what reached the document" (autosave then Revert posts `previewEditCancel`; without autosave nothing is posted, timers are cleared, blur posts nothing).
- scrollSync: "Done posts a final save and both buttons keep the textarea focused on press".
- previewStyles: frame, hover outline, and editor-font tests (block textarea, YAML textarea, text field excluded).
- RI-T15: hover nested item -> exactly one `ul[data-sphinx-preview-edit-hover]`; type ` R`, wait 600 ms, click Revert -> buffer equals original, editor closed; type ` D`, click Done -> buffer contains ` D`.
- Visual `edit-affordances-hover-and-open` (`machineChecks: ["overlay-clipped"]`): asserts the hovered `UL` has a dashed outline, the editor frame (1px border, opaque background), monospace, tab-size 4, hint regex, Done and Revert visible, Revert disabled.

## Existing assertions changed
- scrollSync.test.ts:"edit mode loads raw Markdown and saves changes when the block loses focus" — old: no buttons labelled Save/Cancel (kept) → added: the Done and Revert buttons exist — required by: step 5.
- previewStyles.test.ts:"block editing grows without internal scrolling and uses a square theme-aware margin marker" — old: `::before` marker assertions (`inset-inline-start: -12px`, `width: 3px`, blue background…) → new (renamed "…and is framed"): no `::before` rule, and frame declarations (border 1px focusBorder, radius 4px, padding 6px 8px, editor background) — required by: step 2.
- previewStyles.test.ts:"frontmatter edits stay inline…" `.sphinx-preview-block-editor` rule — old: `padding: 0; border: 0; background: transparent;` → new: `border: 1px solid var(--vscode-focusBorder, Highlight); … padding: 6px 8px; … background: var(--vscode-editor-background, Canvas);` — required by: step 2.
- previewStyles.test.ts same test, block textarea rule — old: `…background: transparent; font: inherit;` → new: `…background: transparent;` followed by `font-family: var(--vscode-editor-font-family, ui-monospace, …)` — required by: step 3.
- capture.py `check_preview_edit_mode` (edit targets title/paragraph/admonition/list): old: `getComputedStyle(parent).borderWidth != "0px"` → failure "raw block editor still has a surrounding frame"; new: `borderTopWidth != "1px"` → failure "raw block editor has no visible surrounding frame". Listed in the task's "Expected changes to existing tests" (capture.py checks that assert no frame). Without it, edit-paragraph-dark, edit-admonition-dark, edit-list-narrow and edit-mode-dark (alias) fail. Flagging this because the orchestrator reminder says to STOP on such checks; I followed the task text, which names it.

## Verification
- `gate.sh T15-impl unit types trusted` → PASS (logs/T15-impl-{compile,unit,types,trusted-build,trusted}.log); RI-T15 ran inside `trusted` and passed.
- `gate.sh T15-impl visual` → PASS vs baseline, 0 new failure lines (logs/T15-impl-visual.log). Note: `logs/T15-impl-visual-new-failures.txt` is stale from an earlier run in this round (its lines come from before the capture.py frame-check update and the sticky-band style tag); the final run's verdict is the PASS line.
- Tracked `test/visual/screenshots` left clean by the gate.

## Evidence for reviewers
- Visual (kept by the gate): `logs/visual-T15-impl/edit-affordances-hover-and-open-hover.png` (nested list outlined),
  `logs/visual-T15-impl/edit-affordances-hover-and-open.png` (+ `.txt`) (paragraph editor: frame, hint, Done/Revert). Only the dark theme is captured for this scenario.
- Real-input: `.artifacts/real-input-*/21-edit-hover.png` and `22-editor-frame-and-buttons.png` (latest run directory).

## Feedback addressed (rounds 2–3)
None (round 1).

## Open points / STOP reason
- Hint for a single-line block reads `Line N` rather than `Lines N–N`.
- The visual scenario hides the sticky heading band with an injected style tag in `check_edit_affordances`: HEAD already fails
  "sticky heading overlaps the reserved toolbar row" on every scrolled page (baseline), and a new scenario that scrolled would otherwise show up as a new failed id.
- Hovered nested lists outline the innermost `ul`/`ol` (what `editingElementFor` opens), not the top-level list.
- Cosmetic: the status line sits about 1em above the buttons, because `#sphinx-myst-preview-content p` margin wins over the status rule. Not changed.
- Hover is not shown on links (clicks on links do not open the editor) and not inside the properties table or an open editor.
