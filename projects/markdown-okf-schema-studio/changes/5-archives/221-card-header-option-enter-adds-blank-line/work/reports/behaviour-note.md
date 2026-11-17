# Behaviour note: Enter in a card one-line editor

## Today

In edit mode, the `:header:` and `:footer:` options of a `{card}` and the card title (its directive line,
`:::{card} Title` / `:::{grid-item-card} Title`) open the multi-line block editor. Plain Enter inserts a
newline; Done or Cmd/Ctrl+Enter saves it. The result is an empty line after the option (or after the
directive line), and an empty line ends the MyST option block. Status hint: `Line 18 · Enter: new line ·
Tab: indent · Esc: cancel · ⌘↩: done`.

Reproduced: the page test `test/page/runtimeCardOptionEnter.test.ts` fails on the unchanged code for the
header, the footer and the title (3/3). A browser probe confirms all three, so "like the title editor" in
the QA sheet is wrong: the title has the same defect.

## After (proposal)

For a card's one-line editors (the `:header:` and `:footer:` option lines and the card title line), plain
Enter saves and closes the editor, as Done does. The diff is -1 +1. Other editors do not change.

## Requirements touched

- SwRS-MDOKFSTUDIO-BLOCK-258 (proposed): add the Enter rule and a scenario.
- SwRS-MDOKFSTUDIO-BLOCK-033 (proposed): the status hint reads "Enter: done" for one-line editors.
- No approved requirement changes.

## Open choices, with proposals

1. Include the card title (directive line): proposal yes, because it has the same defect.
2. Shift+Enter: proposal ignored (no newline, editor stays open). The alternative is to insert a space.
3. Hint for one-line editors: proposal `Line 18 · Enter: done · Esc: cancel · ⌘↩: done`, with
   "Tab: indent" dropped. Alternative: keep Tab and only swap "Enter: new line" for "Enter: done".
4. Pasted text with newlines in these editors: proposal out of scope; it stays as today.
5. Detection: a marker set by the renderer on the card option and title elements
   (`data-single-line`). It does not use "line == endLine", because one-line paragraphs and headings
   must keep Enter as a new line.
