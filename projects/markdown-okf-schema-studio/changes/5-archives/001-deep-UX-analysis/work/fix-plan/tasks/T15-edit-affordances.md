# T15 — Visible edit affordances, editor font, Done and Revert

| Field | Value |
| --- | --- |
| Fixes | [UX-07](../../01-inline-block-editing/UX-07-edit-affordances-invisible.md), [UX-08](../../01-inline-block-editing/UX-08-proportional-font-for-raw-source.md) |
| Decisions | D-01 (Revert is the explicit discard), D-22 |
| Depends on | T14 |
| Gate | `unit trusted visual` |
| Risk | Medium (layout of every editor; R7 anchoring) |
| Commit message | `feat(vscode): show what edit mode edits and how to finish` |

## Goal

A first-time user can tell **what a click will edit** and **how to finish** without reading the
README.

1. **Hover outline.** In edit mode, hovering (or keyboard-focusing) a mapped block outlines exactly
   the element whose source a click opens: the whole list for a list item, the `pre` for code, the
   directive for an admonition title.
2. **Framed editor.** The open block editor has a visible frame and background.
3. **Editor font (UX-08).** The raw-Markdown textarea uses the editor font: monospace,
   `tab-size: 4`. So does the frontmatter **YAML** textarea, but not the one-line text field
   (`data-okf-text-value`), which keeps the preview font.
4. **Status hint** under the textarea while editing:

   ```text
   Lines 12–14 · Enter: new line · Tab: indent · Esc or ⌘↩: done
   ```

   On non-macOS platforms, write `Ctrl+Enter` instead of `⌘↩`. Detect the platform with
   `navigator.platform` / `userAgentData`, guarded.
5. **Done and Revert buttons** under the textarea:
   - **Done** commits, like Escape.
   - **Revert** restores the block's original text: it calls the existing cancel path,
     `closeBlockEdit(true)` → `previewEditCancel` → host `handlePreviewEditCancel`. Revert is
     disabled while nothing has changed.

## Context to read first

- `src/preview/previewStyles.ts`:
  - the edit-mode rules (`html[data-sphinx-preview-edit-mode="on"] …`);
  - `.sphinx-preview-block-editor` and its `::before`, `textarea`, `[data-sphinx-preview-edit-status]`;
  - the unused `.sphinx-preview-block-editor-actions` rules;
  - `[data-okf-frontmatter-editor] > textarea`.
- `src/webview/scrollSync.ts`: `receiveBlockEditSource`, `closeBlockEdit`, `postBlockEditSave`,
  the T14 helper that decides the editing element.
- `test/webview/previewStyles.test.ts`: in-order regex assertions on these rules.
- `test/webview/scrollSync.test.ts`, test "edit mode loads raw Markdown and saves changes when the
  block loses focus". It asserts that **no** buttons labelled "Save Markdown block" or "Cancel
  Markdown edit" exist.

## Allowed files

- `src/webview/scrollSync.ts`
- `src/preview/previewStyles.ts`
- `test/webview/scrollSync.test.ts`
- `test/webview/previewStyles.test.ts`
- `test/visual/scenarios.ts` (one new scenario)
- `test/visual/capture.py` (only if the new scenario needs a step, reusing `editTarget` and hover
  helpers)
- `test/integration/realInput.test.ts` (add RI-T15)
- `README.md`

## Steps

1. **Hover.** Add `document` listeners for `mouseover` and `focusin`. When `editMode` is on and the
   event target is inside a mapped block (not inside `[data-okf-properties]`, an open editor, or the
   toolbar), set `data-sphinx-preview-edit-hover="true"` on the **editing element** and remove it
   from the previous one. Clear it on `mouseout` to outside, on `focusout`, when an editor opens,
   and when edit mode turns off. CSS:

   ```css
   html[data-sphinx-preview-edit-mode="on"] [data-sphinx-preview-edit-hover="true"] {
     outline: 1px dashed var(--vscode-focusBorder, Highlight);
     outline-offset: 3px;
   }
   ```

   Use an outline, not a border, so the layout does not move.
2. **Frame.** Replace the `::before` blue rule with a frame on `.sphinx-preview-block-editor`:

   ```css
   border: 1px solid var(--vscode-focusBorder, Highlight);
   border-radius: 4px;
   padding: 6px 8px;
   background: var(--vscode-editor-background, Canvas);
   ```

   Keep `position: relative` and the `z-index`.
3. **Font.** On `.sphinx-preview-block-editor textarea`, replace `font: inherit` with:

   ```css
   font-family: var(--vscode-editor-font-family, ui-monospace, SFMono-Regular, Menlo, monospace);
   font-size: var(--vscode-editor-font-size, 0.95em);
   tab-size: 4;
   ```

   Keep `white-space: pre-wrap` and `overflow-wrap: anywhere` in the same order. Apply the same
   font to `[data-okf-frontmatter-editor] > textarea:not([data-okf-text-value])`.
4. **Hint.** In `receiveBlockEditSource`, after creating the textarea, set `edit.status.textContent`
   to the hint, with `edit.line`/`edit.endLine`. Restore the hint after a save error clears.
   "Saving Markdown…" still replaces it while saving.
5. **Buttons.** Append a `div.sphinx-preview-block-editor-actions` containing:
   - `button` "Done", `aria-label="Done editing"` → `saveBlockEdit()`;
   - `button` "Revert", `aria-label="Revert block to its original text"`. It is disabled until the
     first `input` event that makes `textarea.value` differ from the displayed original, or until
     `edit.hasAutosavedChange`. On click:
     - if `edit.hasAutosavedChange` (something reached the document), call `closeBlockEdit(true)`;
     - otherwise call `closeBlockEdit(false)`.

   Add `mousedown` → `preventDefault` on both buttons so that the textarea's blur-commit does not
   fire before the click. Make Done the first child; the existing CSS styles `:first-child` as
   primary. Update the comment above `closeBlockEdit` (T08 added it) to name the Revert button.
6. README, "Edit mode" paragraph: "Hover shows what a click will edit. Done, Escape, or clicking
   elsewhere keeps your changes; Revert restores the block's original text."
   **Added by the orchestrator (T07/T08 follow-up):** T07 and T08 left lines longer than 100
   columns in this paragraph. While editing it, rewrap the whole "Edit mode" paragraph at 100
   columns, at clause boundaries. Do not change any other wording.

## Tests

**Unit**:

- Hovering a list item in edit mode sets the attribute on the list element; reading mode sets
  nothing.
- After opening a block: the status contains `Lines 50–52` (the fixture's line and endLine); the
  Done and Revert buttons exist; Revert is disabled.
- Changing the value enables Revert. Clicking Revert after an autosave (`flushTimers`) posts
  `previewEditCancel`; without an autosave it posts nothing and closes.
- Done posts a final save.

**`previewStyles.test.ts`:** assertions for the hover outline, the frame, and the monospace font
(block and YAML textarea, not the text field).

**Visual:** add the scenario `edit-affordances-hover-and-open`, based on fixture
`04-code-and-tables`, edit mode on. Capture with the list hovered (outline visible) and with a
paragraph editor open (frame, hint, buttons visible). Set `machineChecks: ["overlay-clipped"]`.

**Real-input E2E**, scenario **RI-T15**:

- hover a nested list item → the outline attribute is on the `ul`;
- open a paragraph, type ` R`, wait 600 ms, click **Revert** → the buffer equals the original and
  the editor is closed;
- open again, type ` D`, click **Done** → the buffer contains ` D`.

Write the RI and unit tests first; record the failures.

## Expected changes to existing tests

- `scrollSync.test.ts` → "edit mode loads raw Markdown and saves changes when the block loses
  focus": the assertion that no Save/Cancel buttons exist becomes an assertion that the **Done**
  and **Revert** buttons exist (labels above).
- `previewStyles.test.ts`: assertions on `.sphinx-preview-block-editor::before`, or on
  `font: inherit` in the block textarea rule, change to the new declarations. List each one.
- `capture.py` checks that assert the editor has no visible frame or border, if any. List them.

## Must not change

- Which source range a click opens.
- Table cell editor visuals (T18 handles the toolbar).
- Escape / blur / Cmd+Enter semantics from T08.
- The YAML **display** in the properties table (UX-24).

## Done when

- The `unit`, `trusted` and `visual` gates pass; RI-T15 passes.
- The reviewer has looked at the two new screenshots in all captured themes: the outline and the
  frame are visible, the hint is readable, nothing is clipped.
