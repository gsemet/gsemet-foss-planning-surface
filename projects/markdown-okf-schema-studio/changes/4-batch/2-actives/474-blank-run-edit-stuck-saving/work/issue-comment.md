Thanks for the report: accepted.

What will change:

- In edit mode, each extra blank line shows as its own small block, instead of one block for the
  whole run. The one blank line that separates two blocks in Markdown stays hidden.
- Typing text in one of those blocks turns that line into a paragraph; the editor saves and goes
  back to the rendered view.
- Delete, Backspace or the Delete block button on one of them removes that one blank line.
- No edit can stay on "Saving Markdown…" for good: a save always ends in success or in an error
  shown to you, and Cancel always closes the editor.
- Tests cover runs of blank lines, typing in a blank-line block, and every save ending.

Left out: blank lines inside lists and other containers.

No date yet; the pull request will be linked here.
