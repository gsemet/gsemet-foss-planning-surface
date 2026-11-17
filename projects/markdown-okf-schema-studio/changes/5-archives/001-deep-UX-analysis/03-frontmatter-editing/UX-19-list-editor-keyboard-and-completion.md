# UX-19 — List fields: Enter does nothing, no link completion, link text navigates

| Field | Value |
| --- | --- |
| Severity | Medium |
| Confidence | Reproduced |
| Area | Frontmatter list editor (`derives_from`, `implemented_in_files`, …) |
| Evidence | [r3-fm-list-add.jpg](../evidence/r3-fm-list-add.jpg) |

## Use case

An author adds an upstream requirement to `derives_from` on `SwRS-CORE-001.md`.

## Observed

1. **Opening the editor:** clicking the item text (`StRS-CORE-001`) follows the link and switches
   the preview to the target document, even in edit mode. The user must click the empty part of the
   cell to edit the list.
2. **Adding an item:** "+ Add item" adds an empty input. Typing `StRS-CORE-999` and pressing Enter
   does nothing: no commit and no new row. The list is saved only on blur.
3. **No completion:** the field has `x-okf-link: {resolution: filename-stem}`, and the extension
   already indexes every Markdown stem, but the input offers no suggestions. The author must know
   the identifiers by heart.
4. **Invalid values are accepted silently:** `StRS-CORE-999` (no such file) is written, then shown
   in red as `StRS-CORE-999 [E10]`. Link errors are deliberately excluded from save-time
   validation, but no warning is shown before writing.

## Expected

- Clicking a value in edit mode edits it; navigation stays available via Cmd/Ctrl+click or a
  dedicated icon.
- Enter in an item commits it and opens the next empty item; Backspace on an empty item removes it.
- Inputs for `x-okf-link` items offer a datalist or quick pick of resolvable targets (stems, or
  paths under the bundle/project root).
- An unresolvable target shows an inline warning before commit ("No file named StRS-CORE-999.md in
  the bundle — save anyway?").

## Where it comes from

`src/webview/scrollSync.ts` list editor (around L1038-L1200) and frontmatter keydown
(L1324-L1331, `!useListEditorValue && Enter`).

## Done when

A link list can be extended from the keyboard with suggestions, and edit mode never navigates on a
plain click.
