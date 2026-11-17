# T21 — List fields: a click edits; Enter and Backspace manage items

| Field | Value |
| --- | --- |
| Fixes | [UX-19](../../03-frontmatter-editing/UX-19-list-editor-keyboard-and-completion.md) (points 1 and 2) |
| Decisions | D-07 |
| Depends on | T05, T20 |
| Gate | `unit trusted` |
| Risk | Medium (P-N6 link navigation must keep working) |
| Commit message | `fix(vscode): edit frontmatter list links on click and manage items from the keyboard` |

## Goal

1. **Click on a link value in edit mode.** A plain click on a link inside the properties table
   (`a[data-sphinx-preview-navigation^="okf-link:"]`) opens that field's editor. Cmd (macOS) or
   Ctrl+click still navigates. Reading mode is unchanged: a click navigates.
2. **In a list editor item:**
   - **Enter** inserts a new empty item **after** the current one and focuses it.
   - **Enter on an empty last item** removes it and saves the list.
   - **Backspace in an empty item** removes it and focuses the previous item, or the next one, or
     the "+ Add item" button.
   - **Cmd/Ctrl+Enter** saves the list.

## Context to read first

- `src/webview/linkNavigation.ts` → `installLinkNavigation`. It registers a bubble `click`
  listener on `document` that navigates every `a[data-sphinx-preview-navigation]`.
- `src/webview/scrollSync.ts`:
  - the frontmatter click listener (it returns early for okf links today);
  - `openFrontmatterEditor` → the list editor (`appendItem`, `itemRows`, `refreshItemLabels`,
    `addButton`, `focusListEditor`, `saveValue`, `readListValue`, the editor `focusout` save);
  - the `control` keydown (Escape cancels).

## Allowed files

- `src/webview/scrollSync.ts`
- `test/webview/scrollSync.test.ts`
- `test/integration/realInput.test.ts` (add RI-T21)
- `README.md` (one sentence)

## Steps

1. Write the tests first and record the failures.
2. **Capture-phase click.** In the runtime, register
   `document.addEventListener("click", handler, true)`. In the handler:
   - return unless `editMode`, the target is inside an okf link inside `tr[data-okf-field]` and
     `[data-okf-edit-cell]`, and neither `event.metaKey` nor `event.ctrlKey` is set;
   - then call `event.preventDefault()` and `event.stopImmediatePropagation()`;
   - then call `openFrontmatterEditor(row)`. It is a no-op when another editor is open.

   Register it **before** the other listeners, but it is a capture listener anyway. Do not modify
   `linkNavigation.ts`.
3. **Item keydown.** In `appendItem`, add a `keydown` listener on `input`:
   - `Enter` without Shift/Alt/Meta/Ctrl, not composing:
     - `preventDefault`;
     - if `input.value.trim() === ""` and the row is the last one: remove it, call
       `refreshItemLabels()`, then `saveValue()`;
     - otherwise create a row with `appendItem("")`, move it right after the current row
       (`itemList.insertBefore(newRow, row.nextSibling)`), call `refreshItemLabels()`, and focus
       its input.
   - `Enter` with Meta or Ctrl: `preventDefault`, then `saveValue()`.
   - `Backspace` when `input.value === ""` and `selectionStart === 0`: `preventDefault`, remove the
     row, then focus the previous row's input (caret at the end), else the next row's input, else
     `addButton`.

   Make sure the editor's `focusout` save does not fire while focus moves **between items**. It
   already ignores `relatedTarget` inside the editor; keep it that way. Removing the focused row
   must not trigger a save: focus the next target **before** removing the row, as the existing
   remove button does.
4. README, "Edit mode" paragraph: "In edit mode, click a link value to edit it; Cmd/Ctrl+click
   follows the link. In list fields, Enter adds an item and Backspace on an empty item removes it."

## Tests

**Unit:**

- Edit mode: a click on an okf link inside a row opens the editor and does not post `previewLink`.
- The same with `metaKey: true` → posts `previewLink` and opens no editor.
- Reading mode → posts `previewLink`.
- Enter in the item list → a new row after the current one, focused, and no save.
- Enter in an empty last item → a save with that item removed.
- Backspace in an empty middle item → the row is removed and the previous input is focused.

To post `previewLink`, the harness must run `installLinkNavigation`. It already does, because the
runtime inlines it. Extend the fake DOM's `closest` support for the okf-link selector if needed.

**Real-input E2E**, scenario **RI-T21**:

- Bundle fixture with `derives_from` (array, `x-okf-link: { resolution: filename-stem, syntax: plain }`)
  and two target documents `StRS-A.md` and `StRS-B.md`. The value is `[StRS-A]`, in compact style.
- Edit mode; a plain click on the `StRS-A` link text → the list editor is open, and the preview
  still shows the same document (`documentUri` unchanged).
- Focus the last item input (click it), press `End`, press `Enter`, type `StRS-B`, press `Enter`,
  then `Enter` again (on the empty item) → saved.
- Assert that the buffer list is `- StRS-A`, `- StRS-B`, and that only those lines changed.
- `${MOD}+click` on `StRS-A` → the active text editor becomes `StRS-A.md`.

## Expected changes to existing tests

None expected. If a test asserts that a plain click on an okf link navigates **in edit mode**,
STOP: it encodes the old behaviour, so report it and let the orchestrator amend this task.

## Must not change

- Reading-mode link navigation, marker-line selection (P-N6), drag-and-drop and keyboard reorder
  in the list editor, the null button, and Escape cancel.

## Done when

- The `unit` and `trusted` gates pass; RI-T21 passes.
