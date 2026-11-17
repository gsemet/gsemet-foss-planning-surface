# T08 — Escape closes the inline editor and keeps the text

| Field | Value |
| --- | --- |
| Fixes | [UX-01](../../01-inline-block-editing/UX-01-escape-discards-autosaved-text.md) |
| Decisions | D-01 |
| Depends on | T02 |
| Gate | `unit trusted` |
| Risk | Medium (P-E3 commit paths) |
| Commit message | `fix(vscode): keep typed text when leaving an inline editor with Escape` |

## Goal

No path silently removes text the user typed in a raw-Markdown or table-cell editor:

- **Escape** in the block textarea or the table cell textarea commits, exactly like blur.
- **Turning edit mode off** while a block editor is open commits instead of reverting.
- **Discarding** stays possible only through an explicit action: the Revert button added by T15,
  which reuses the existing cancel path. Keep that path intact.

Frontmatter editors keep Escape = cancel. They never autosave, so nothing reaches the document
before Save.

## Context to read first

- `src/webview/scrollSync.ts`:
  - `closeBlockEdit(cancel = false)`, whose cancel branch posts `previewEditCancel`;
  - `postBlockEditSave(final)`, `saveBlockEdit()`;
  - the keydown listener in `receiveBlockEditSource` (Escape → `closeBlockEdit(true)`);
  - the keydown listener in `renderTableCellEditor` (Escape → `closeBlockEdit(true)`);
  - `applyEditMode(enabled)`, which calls `closeBlockEdit(true)` when disabling.
- `src/extension.ts` → `handlePreviewEditCancel`. **Do not change it**: T15's Revert uses it.

## Allowed files

- `src/webview/scrollSync.ts`
- `test/webview/scrollSync.test.ts`
- `test/visual/capture.py` (only if a visual check expects the old Escape behaviour, see below)
- `test/integration/realInput.test.ts` (add RI-T08)
- `README.md` ("Edit mode" paragraph wording)

## Steps

1. Write the tests first and record the failures.
2. Block textarea keydown: on `Escape`, call `event.preventDefault?.()` and then `saveBlockEdit()`.
3. Table cell keydown: the same.
4. `applyEditMode(enabled)`, when `!enabled`:
   - keep `closeFrontmatterEditor()` as is;
   - replace `closeBlockEdit(true)` with:
     - when `activeBlockEdit` exists and `typeof activeBlockEdit.originalText === "string"`
       (the source has loaded), `postBlockEditSave(true)`. This closes immediately when nothing
       changed; otherwise the re-render closes it.
     - when the source has not loaded yet, `closeBlockEdit(false)`.
5. Do **not** delete the `cancel` branch of `closeBlockEdit`. Nothing calls it with `true` until
   T15; add a comment above the function saying so ("used by the explicit Revert action").
6. README, "Edit mode" paragraph: the current text says Cancel discards. Replace it with: "Escape,
   clicking elsewhere, or Cmd/Ctrl+Enter keeps your changes." T15 adds the Revert sentence. Keep the
   other sentences.

## Tests

**Unit** (`scrollSync.test.ts`):

1. Open a block, load its source, change `textarea.value`, dispatch keydown `Escape` → the last
   message is `previewEditSave` with `final: true` and the edited text; no `previewEditCancel` is
   posted.
2. Open a block, load its source, **no change**, Escape → no message is posted, and the editor
   element is removed.
3. Table cell: change a cell, Escape → `previewEditSave` final with the table text.
4. Edit mode toggled off with a changed textarea → `previewEditSave` final; with an unchanged
   textarea → no message.
5. Frontmatter Escape still cancels: the existing tests stay green.

**Real-input E2E**, scenario **RI-T08** (fixture: the T02 `smoke.md`):

- Open "Second paragraph.", press `End`, type ` KEEP ME PLEASE.`, press `Escape`.
- Wait for `phase === "ready"`. The buffer contains `Second paragraph. KEEP ME PLEASE.`, and no
  `[data-sphinx-preview-block-editor]` remains.
- Open the same block, type ` B`, then click the pencil toggle to turn edit mode off. The buffer
  contains ` B`.
- Table cell: click `two`, type `2`, press `Escape` → the buffer contains `| beta | two2 |`.

All three must fail before the fix (the first is the bug sheet's exact scenario).

## Expected changes to existing tests

- In `scrollSync.test.ts`, tests that send Escape to a **block or table** editor and expect
  `previewEditCancel` must now expect a final `previewEditSave`, or no message when nothing changed.
  List each one.
- In `capture.py`, a scenario that presses Escape on a block editor and asserts a cancel message
  from the mock host must be updated the same way. List each one.
- Frontmatter Escape tests do not change.

## Must not change

- Blur, Cmd/Ctrl+Enter, arrow-key navigation (P-E3, P-E4).
- `handlePreviewEditCancel` on the host.
- Frontmatter Escape = cancel.

## Done when

- The `unit` and `trusted` gates pass; RI-T08 passes.
- `rg -n "closeBlockEdit\(true\)" src` finds no Escape or edit-mode caller.
