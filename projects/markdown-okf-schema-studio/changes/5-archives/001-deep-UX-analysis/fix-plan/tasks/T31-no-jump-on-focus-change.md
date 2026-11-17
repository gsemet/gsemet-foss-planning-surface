# T31 — The preview does not jump when focus moves between panes

| Field | Value |
| --- | --- |
| Fixes | [UX-29](../../06-render-churn-and-scroll/UX-29-scroll-jump-on-owner-switch.md) |
| Depends on | T30 |
| Gate | `unit trusted scroll` |
| Risk | Medium (P-N1 anchoring rules R4–R6); investigation-first |
| Commit message | `fix(vscode): keep the preview still when focus moves between panes` |

## Goal

After the user scrolls the preview, then clicks into the source editor and types, or clicks a
table cell in the preview, the preview does not move by more than 4 px.

## Primary hypothesis (H1; verify it first)

`createPreview` registers:

```ts
panel.onDidChangeViewState(() => { if (panel.visible) restorePreviewState(preview); })
```

`onDidChangeViewState` fires on **active/inactive** changes too: clicking into the source editor
makes the panel inactive, and clicking back into the preview makes it active. `restorePreviewState`
then calls `syncEditorToPreview(editor)`. That makes the **editor** the owner, using its first
visible line. After a preview-led reveal, that line differs from the preview's fractional anchor:
`editorTopLine` floors it, and VS Code's sticky scroll can offset `revealRange(AtTop)` by a few
lines. The preview then jumps.

The comment on `restorePreviewState` says it is meant only for a panel that was **hidden** and
becomes visible.

## Context to read first

- `src/extension.ts`: `createPreview` (the `onDidChangeViewState` subscription),
  `restorePreviewState`, `syncEditorToPreview`, `revealEditorLine`, `EditorEchoGuard` usage, and
  `initialAnchorLine`.
- `docs/scroll-anchoring.md` (R4–R6).
- `test/integration/scroll-sync-suite.ts`: how the scroll campaign measures the preview's
  `scrollY`.

## Allowed files

- `src/extension.ts`
- `test/integration/realInput.test.ts` (add RI-T31)
- `test/integration/scroll-sync-suite.ts` (only if the new behaviour belongs better there; add a
  scenario, never weaken one)
- `docs/scroll-anchoring.md` (one sentence under R4 or R6)

## Steps

1. **Reproduce first (RI-T31).** Fixture: copy `test/visual/fixtures/05-long-chapter.md`. Side
   preview, anchoring on, `scrollEditorWithPreview` default.
   - Move the mouse over the preview frame and `page.mouse.wheel(0, 1200)`; wait 800 ms.
   - Record `frame.evaluate(() => scrollY)` as `Y0`.
   - **Case A:** click inside the source editor text (the `.monaco-editor .view-lines` bounding box
     of the editor in column One, at 30 % height). Wait 600 ms. Record `Y1`.
   - Type `x` (`page.keyboard.type`). Wait for the re-render to be ready, plus 500 ms. Record `Y2`.
   - Assert `|Y1 − Y0| <= 4` and `|Y2 − Y0| <= 4`.
   - **Case B:** wheel the preview again, record `Y3`, click a **table cell** in edit mode, then
     record `Y4` within 100 ms of the click. Assert `|Y4 − Y3| <= 4`.

   Run it before any change. Write the measured jumps in the report.
2. **Fix H1.** In `createPreview`, track the previous visibility:
   `let wasVisible = panel.visible;`. In `onDidChangeViewState`, call `restorePreviewState` only on
   a **hidden → visible** transition, then update `wasVisible`.
3. Rerun RI-T31 and the `scroll` gate.
4. **If RI-T31 still fails after H1, STOP.** Report the measurements and the sequence of
   `sourceScroll` / `previewScroll` messages that preceded the jump. To capture them, temporarily
   log them in a local build; **do not commit the logging**. Do not try other fixes. The
   orchestrator escalates to the user with your data.
5. `docs/scroll-anchoring.md`: add under R6, "A panel that only changes focus (active ↔ inactive)
   keeps its anchor; only a hidden panel that becomes visible catches up with the editor."

## Expected changes to existing tests

None. All scroll-suite scenarios must pass unchanged.

## Must not change

- A hidden panel that becomes visible still catches up with an editor that moved (P-N1).
- Anchoring rules R1–R9; the echo guard.

## Done when

- The `unit`, `trusted` and `scroll` gates pass, and RI-T31 passes, with the before/after
  measurements in the report.
- Or: STOP with data per step 4.

## Amendment after round 1 STOP (orchestrator)

Round 1 data: case A (wheel the preview, click into the editor, type) does **not** move the preview,
before or after H1 (Y0 = Y1 = Y2 = 1200). That is the bug sheet's "Done when", so UX-29 case 1 does
not reproduce on HEAD. Case B moved `scrollY` from 1600 to 1658 when a table cell was clicked, with
no host scroll message. That is T18's deliberate R7 anchor (D-18): the toolbar is inserted in flow
above the table, and the page scrolls by its height so the **selected cell stays fixed on screen**.
`scrollY` is the wrong measure for case B; the bug sheet's expectation is "the pane the user is
looking at does not move".

- **Case B, test mechanics only.** Measure the clicked cell's viewport top
  (`getBoundingClientRect().top` of the cell element, which stays in the DOM with
  `data-sphinx-preview-table-cell-selected`). Take it before the click, again about 100 ms after
  the click (the bug sheet's case 2 was a jump *before* the editor opened), and again once the cell
  editor is open. Assert that both deltas are at most 4 px.
  - Wheel so that the table's top is at least 150 px below the usable top. The D-18a reveal rule
    then does not apply: it legitimately scrolls when the bar would land above the usable top.
  - Do not assert on `scrollY` in case B.
  - Keep case A exactly as it is.
- **H1 stays in the tree** for review. The reviewer decides whether to keep it: it matches the
  documented intent of `restorePreviewState`, and P-N1 (hidden → visible catch-up) must still hold.
  The `docs/scroll-anchoring.md` sentence stays with H1.
- The report must state plainly that UX-29 case 1 did not reproduce before the change, with the
  numbers.
