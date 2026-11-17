# T16 — Edit mode keeps the reading layout

| Field | Value |
| --- | --- |
| Fixes | [UX-09](../../01-inline-block-editing/UX-09-edit-mode-reflows-whole-document.md) |
| Depends on | T15 |
| Gate | `unit trusted scroll visual` |
| Risk | Low–medium (layout feeds the anchor map, P-N1) |
| Commit message | `fix(vscode): keep paragraph flow when edit mode is on` |

## Goal

Turning edit mode on does not change the layout of blocks that are not being edited. Paragraphs
keep their normal flow; source line breaks are not shown. Only the open editor shows raw source.

## Context to read first

- `src/preview/previewStyles.ts`. These two rules exist only to show soft line breaks in edit mode;
  the second one undoes the first inside tables:

  ```css
  html[data-sphinx-preview-edit-mode="on"] #sphinx-myst-preview-content p[data-sphinx-source-line] { overflow-wrap: anywhere; white-space: pre-wrap; }
  html[data-sphinx-preview-edit-mode="on"] #sphinx-myst-preview-content table p[data-sphinx-source-line] { overflow-x: visible; overflow-wrap: normal; white-space: normal; }
  ```

- `src/webview/scrollSync.ts` → `measureLineTops`. It measures the first visible character after
  each `\n` in the **DOM text**, which does not depend on `white-space`. Line-level anchoring keeps
  working with normal wrapping. Verify this by running the scroll gate; do not change the function.

## Allowed files

- `src/preview/previewStyles.ts`
- `test/webview/previewStyles.test.ts`
- `test/visual/capture.py` (only checks that assert pre-wrap paragraphs in edit mode)
- `test/integration/realInput.test.ts` (add RI-T16)

## Steps

1. Write RI-T16 first and record the failure.
   - Fixture: three paragraphs hard-wrapped at about 60 characters (four source lines each), plus
     a table.
   - In reading mode, record `scrollHeight` and the `getBoundingClientRect().top` of the third
     paragraph.
   - Turn edit mode on by clicking the pencil.
   - Assert that `scrollHeight` changed by at most 2 px, and the third paragraph's top by at most
     2 px.
2. Delete both rules above.
3. Run the `scroll` gate: its edit-mode scenarios must still pass.

## Expected changes to existing tests

- `previewStyles.test.ts`: the assertion matching the edit-mode `p[data-sphinx-source-line]`
  pre-wrap rule becomes
  `assert.doesNotMatch(PREVIEW_THEME_CSS, /html\[data-sphinx-preview-edit-mode="on"\][^{]*p\[data-sphinx-source-line\]\s*\{[^}]*white-space: pre-wrap/u)`.
  Same for the table exception rule, if it is asserted.
- `capture.py`: any check asserting pre-wrap paragraphs in edit mode. List them. If a check
  asserts **line-level scroll mapping in edit mode**, it must still pass unchanged. If it fails,
  STOP.

## Must not change

- Line-level anchoring (R3), the editor's own `white-space: pre-wrap` (textarea), sticky headings.

## Done when

- The `unit`, `trusted`, `scroll` and `visual` gates pass; RI-T16 passes.
