# T27 — Block insertion: host protocol

| Field | Value |
| --- | --- |
| Fixes | [UX-10](../../01-inline-block-editing/UX-10-no-way-to-insert-a-block.md) (host half) |
| Decisions | D-20 |
| Depends on | T09 (minimal edits), T15 (editor UI reused by T28) |
| Gate | `unit trusted` |
| Risk | Medium (new edit path; P-E6 safety must hold) |
| Commit message | `feat(vscode): accept new Markdown blocks inserted from the preview` |

## Goal

The host accepts an inline editing session that **inserts** a new block after a given source line,
reusing the existing `previewEditOpen` / `previewEditSave` / `previewEditCancel` messages with one
new optional field, `insertAfterLine`.

- `0` means "at the start of the body": after the frontmatter if there is one, otherwise at offset
  0.
- `N >= 1` means "after source line N".

The inserted text is separated from its neighbours by blank lines. Saving empty text inserts
nothing. Revert removes the inserted block. Autosave, minimal edits and undo grouping behave as for
ordinary blocks.

T28 builds the webview side. This task is testable on its own through
`sendPreviewMessageForTests` in `previewEditing.test.ts`; this is not a real-input test, but it
verifies the protocol.

## Context to read first

- `src/extension.ts`: `PreviewSyncMessage`, `isPreviewSyncMessage` (edit requests require
  `line`/`endLine`), `ActiveBlockEdit`, `handlePreviewEditOpen`, `handlePreviewEditSave`,
  `handlePreviewEditCancel`, `drainActiveBlockEdit`, `activeBlockEditSource`,
  `completeActiveBlockEdit`.
- `src/mapping/textDiff.ts` (T09).
- `src/frontmatter/okfFrontmatter.ts` → `extractFrontmatter` (to find the end of the frontmatter).

## Allowed files

- `src/mapping/insertion.ts` (new, pure)
- `src/extension.ts`
- `test/mapping/insertion.test.ts` (new)
- `test/integration/previewEditing.test.ts` (add one protocol test)

## Design

### Pure module `src/mapping/insertion.ts`

```ts
export interface InsertionPlan { offset: number; prefix: string; suffix: string; lineEnding: string }
/** Where and how to insert a new block after `afterLine` (0 = start of body). */
export function planInsertion(text: string, afterLine: number): InsertionPlan | undefined
export function insertionText(plan: InsertionPlan, raw: string): string
```

`planInsertion`:

- `lineEnding` is `"\r\n"` if `text` contains `\r\n`, else `"\n"`.
- If `afterLine === 0`:
  - **frontmatter present** (`/^---\r?\n[\s\S]*?\r?\n(?:---|\.\.\.)[ \t]*(?:\r?\n|$)/`): the
    anchor line is the closing fence line; treat it as `afterLine = fence line number`;
  - **no frontmatter**: `offset = 0`, `prefix = ""`; `suffix` is one `lineEnding` if `text` is
    empty, otherwise **two** line endings when the first line is not blank, else one.
- If `afterLine >= 1`: return `undefined` when it exceeds the line count. Otherwise:
  - `offset` = the end of line `afterLine`, before its line break, or the end of `text`;
  - `prefix = lineEnding + lineEnding`;
  - `suffix` = `lineEnding` when the following line exists and is **not** blank, else `""`.

`insertionText`: an empty string when `raw.trim() === ""`. Otherwise
`plan.prefix + raw.replace(/\r?\n/g, plan.lineEnding).replace(/(\r?\n)+$/u, "") + plan.suffix`.

### Host

1. `PreviewSyncMessage.insertAfterLine?: number`. Validation: allowed only on `previewEditOpen`,
   `previewEditSave` and `previewEditCancel`; it must be a safe integer `>= 0`. These requests still
   carry `line`/`endLine` (the webview sends `max(1, insertAfterLine)` for both), so the existing
   validation holds.
2. `ActiveBlockEdit.insertion?: InsertionPlan`.
3. `handlePreviewEditOpen`: when `insertAfterLine` is set, check that the document is current
   (`currentPreviewDocument`) and that `planInsertion` returns a plan. Then reply with
   `previewEditSource` with `originalText: ""` and `insertAfterLine` echoed. Errors use the
   existing error messages.
4. `handlePreviewEditSave`, when there is **no** active edit and `insertAfterLine` is set:
   - plan again with the current document text (it must be the same version);
   - create the `ActiveBlockEdit` with `sourceStartOffset = plan.offset`, `originalText = ""`,
     `lastSavedText = ""` and `insertion = plan`;
   - set `pendingText = insertionText(plan, message.editedText)`.

   For later saves of the same edit, `pendingText = insertionText(edit.insertion, message.editedText)`.
   The comparison `message.originalText !== edit.originalText` still works: both are `""`.
5. `handlePreviewEditCancel`: unchanged. `pendingText = originalText`, which is `""`, removes the
   inserted text.
6. Insertion and ordinary edits share `drainActiveBlockEdit`. The safety check on
   `lastSavedText` at `sourceStartOffset` must keep working: it does, because the inserted text
   starts exactly at the offset.

## Tests

1. `insertion.test.ts`:
   - after line 1 of `"A\n\nB\n"` → `"A\n\nNEW\n\nB\n"`;
   - after the last line (`"A\n"`, after 1) → `"A\n\nNEW\n"`;
   - after a line followed directly by a non-blank line (`"- a\n- b\n"`, after 1) →
     `"- a\n\nNEW\n\n- b\n"`. The next item now starts a new list; this is acceptable and
     documented;
   - start of an empty document → `"NEW\n"`;
   - start with frontmatter `"---\na: 1\n---\nBody\n"` → `"---\na: 1\n---\n\nNEW\n\nBody\n"`,
     which re-parses with the same frontmatter;
   - "following line exists" means `offset + lineEnding.length < text.length`. A final line
     break does not count as a following line.
   - CRLF documents;
   - whitespace-only raw text → nothing inserted;
   - out of range → `undefined`.

   Apply each case as `text.slice(0, offset) + insertionText(…) + text.slice(offset)`.
2. `previewEditing.test.ts`, a new protocol test:
   - send `previewEditOpen { insertAfterLine: 1 }`;
   - send `previewEditSave { insertAfterLine: 1, originalText: "", editedText: "New block", final: false }`
     and wait for the buffer;
   - send a second save `"New block more"`, `final: true` → the buffer has the block once, with
     separators;
   - then a second session, with a cancel after a save, removes its inserted text.

## Expected changes to existing tests

None.

## Must not change

- Ordinary block edits, stale-source protection, checkbox refusal during edits, and frontmatter
  saves.

## Done when

- The `unit` and `trusted` gates pass.
