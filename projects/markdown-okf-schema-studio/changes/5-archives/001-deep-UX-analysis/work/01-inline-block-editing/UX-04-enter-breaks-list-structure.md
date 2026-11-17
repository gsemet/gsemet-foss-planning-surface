# UX-04 — Adding a list item inline silently re-parents the following items

| Field | Value |
| --- | --- |
| Severity | High |
| Confidence | Reproduced |
| Area | Inline block editing (lists) |
| Evidence | [u16-list-add-item.jpg](../../evidence/u16-list-add-item.jpg), [u17-tab-in-block.jpg](../../evidence/u17-tab-in-block.jpg) |

## Use case

An author wants to add a sibling item to a nested list in the preview: click the item, press
Enter, type `- Frozen goods`.

## Steps to reproduce

1. Side preview on `fixtures-visual/04-code-and-tables.md`, edit mode on.
2. Click "Dry goods" in "Deeply nested lists". The textarea opens with the innermost sublist:
   `      - Dry goods\n      - Refrigerated goods`.
3. Press Enter, type `- Frozen goods`, then press Tab or click elsewhere.

## Expected

Enter keeps the current indentation (or continues the list with `      - `), as the VS Code text
editor does for Markdown. The new item becomes a sibling of "Refrigerated goods".

## Observed

The new line starts at column 0. After commit the source becomes:

```markdown
      - Dry goods
      - Refrigerated goods
- Frozen goods
  - Deduplication
```

"Frozen goods" is a new top-level item, and the unrelated "Deduplication" item, which was a child
of "Intake", is now a child of "Frozen goods". Nothing warns the user; the preview simply shows the
new structure.

## Impact

Structural corruption of the document outside the edited block, from the most natural list
gesture. The edited textarea shows only part of the list, so the user cannot see that indentation
matters.

## Where it comes from

- The inline editor is a plain `<textarea>` (`src/webview/scrollSync.ts` L1701-L1737) with no
  Markdown-aware Enter handling.
- The block range is the innermost list, so the indentation context lives outside the textarea.

## Suggested direction

Handle Enter in the textarea: carry over leading whitespace and list markers (`- `, `1. ` with
increment, `> `); exit the list on an empty item. Combine with Tab/Shift+Tab indentation
([UX-05](UX-05-tab-commits-instead-of-indenting.md)). Consider opening the whole top-level list so
the indentation context is visible.

## Test to add

E2E: click a nested list item, `keyboard.press("Enter")`, `keyboard.type("- X")`, blur; assert the
item is inserted with the sibling indentation and that the following items keep their parent.

## Done when

Inline list edits never change the parent of items the user did not touch.
