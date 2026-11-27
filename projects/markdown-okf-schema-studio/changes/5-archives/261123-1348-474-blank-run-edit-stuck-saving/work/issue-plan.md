# Plan: blank lines in edit mode, and saves that always end

## What changes for you

- **One block per blank line.** Between two blocks, Markdown needs one blank line to separate them;
  that one stays hidden. Every blank line beyond it shows as its own small block in edit mode. At
  the end of the document, and at its top when there is no frontmatter, every blank line shows. Six
  blank lines after your last paragraph give six blocks.
- **Typing in a blank-line block** turns that one line into text. A blank line is added before or
  after only when Markdown needs it to keep your text a block of its own.
- **Deleting** a blank-line block (Delete, Backspace or its Delete block button) removes that one
  line. The separating line always stays, so two blocks are never glued together.
- **Saving always ends.** Every edit, of any block, ends in a saved result or in an error you can
  read; an edit stuck on "Saving Markdown…" is a bug, and tests check every kind of save for it.
  Cancel always closes the editor, and the save goes on.

## Limits

- Blank lines inside lists, quotes and other containers follow the same rule, and keep their indent.
- Nothing inside the frontmatter changes.
- Line endings of the file are kept as they are.

## What is tested

- How N blank lines are split into blocks, between blocks, at the end and at the top of a file.
- Typing text in a blank-line block, then Done and Cancel.
- The save state always leaving "Saving Markdown…", on success and on error.
