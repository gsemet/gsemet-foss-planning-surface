# T28 — Block insertion: preview affordance and empty documents

| Field | Value |
| --- | --- |
| Fixes | [UX-10](../../01-inline-block-editing/UX-10-no-way-to-insert-a-block.md) (webview half and "Done when") |
| Decisions | D-20 |
| Depends on | T27, T16 (no layout change in edit mode) |
| Gate | `unit trusted visual` |
| Risk | Medium (new elements in the content; layout must not move) |
| Commit message | `feat(vscode): insert new blocks and start empty documents from the preview` |

## Goal

In edit mode, the user can insert a new block between top-level blocks, after the last block, or
into an empty document (or a frontmatter-only one), from the preview alone. Turning edit mode on
still does not change the layout (T16 must keep passing).

## Design

- **Insertion points.** In edit mode, add one **zero-height** element after each top-level mapped
  block (`topLevelMappedBlocks()`), including the properties section:

  ```html
  <div class="sphinx-preview-insert-point" data-sphinx-insert-after-line="N">
    <button type="button" aria-label="Insert a block here">+</button>
  </div>
  ```

  - `N` is the block's `data-sphinx-source-end-line`, or its line. For the properties section
    (`[data-okf-properties]`), `N = 0` (the start of the body).
  - In reading mode, remove all insertion points.
  - Recreate them after each edit-mode toggle. A render creates a new document, so they are
    rebuilt at init when edit mode is on.
- **Empty body.** When `topLevelMappedBlocks()` is empty, or contains only the properties section,
  add a single insertion point with `N = 0` whose button reads `Start writing`. It stays visible in
  edit mode.
- **CSS.**
  - `.sphinx-preview-insert-point { position: relative; height: 0; }`. It has no margin, padding or
    border, so margins collapse through it and the layout does not move.
  - The button is absolutely positioned in the left gutter (`left: -1.6em; top: -0.8em`), 1.4em
    round, `opacity: 0`.
  - The button gets `opacity: 1` when its insertion point or the preceding block is hovered
    (`[data-sphinx-source-line]:hover + .sphinx-preview-insert-point button`), and on button
    `:hover` and `:focus-visible`.
  - The `Start writing` variant is a normal-flow button, always visible.
- **Opening.** Clicking a button calls
  `openBlockEditor(insertPoint, undefined, { line: max(1, N), endLine: max(1, N), insertAfterLine: N }, "end")`.
  Extend `openBlockEditor` and the `activeBlockEdit` object with `insertAfterLine`.
  - The rendered target is the insertion point. Hiding it with `data-sphinx-preview-editing` is
    harmless.
  - Include `insertAfterLine` in `previewEditOpen`, `previewEditSave` and `previewEditCancel`
    messages when it is set.
  - `receiveBlockEditSource` then shows an empty textarea, with the placeholder
    `Type Markdown, for example "## Heading" or "- item"`, the T15 hint, and Done/Revert.
- The insertion buttons must not open a block editor through the mapped-block click handler. They
  are not mapped, but add an explicit early return for `.sphinx-preview-insert-point` in the click
  and keydown handlers.

## Allowed files

- `src/webview/scrollSync.ts`
- `src/preview/previewStyles.ts`
- `test/webview/scrollSync.test.ts`, `test/webview/previewStyles.test.ts`
- `test/visual/scenarios.ts` (one scenario: an insertion point hovered in fixture
  `04-code-and-tables`)
- `test/integration/realInput.test.ts` (add RI-T28)
- `README.md` (Edit mode paragraph)

## Tests

**Unit:**

- Edit mode on → insertion points exist after each top-level block, with the right `N`; reading
  mode → none.
- An empty document → one `Start writing` point.
- Clicking a point posts `previewEditOpen` with `insertAfterLine`.
- A source reply with `""` → an empty textarea; typing then Done posts `previewEditSave` with
  `insertAfterLine` and `originalText: ""`.

**Real-input E2E**, scenario **RI-T28** (the bug sheet's "Done when"):

- Create an **empty** `scratch.md` and open it with `openStudioEditor`. Turn edit mode on.
- Click **Start writing**, type `# Incident review checklist`, press `Enter` twice, type
  `First paragraph.`, click **Done**.
- Assert that the buffer equals `# Incident review checklist\n\nFirst paragraph.\n`, or the exact
  output of T27's rules; assert the exact string.
- Hover the heading, click its `+`, type `- check logs` (Enter continues the list, T11), click
  **Done**. Assert that the list sits between the heading and the paragraph, separated by blank
  lines.
- Edit-mode layout check: re-run the T16 measurement on this document. Toggling edit mode changes
  `scrollHeight` by at most 2 px, ignoring the `Start writing` case, which only applies to empty
  bodies.

## Expected changes to existing tests

None expected. If a unit test counts children of the content or mapped elements and now sees the
insertion points, update **only** that count, and list it.

## Must not change

- T16's no-reflow guarantee; existing block editing; arrow navigation. Insertion points are not
  mapped blocks and must never appear in `topLevelMappedBlocks()` results.

## Done when

- The `unit`, `trusted` and `visual` gates pass; RI-T28 passes.
- README: "In edit mode, the + button between blocks inserts a new block; an empty document shows
  Start writing."
