## Bug Fixes

- Cmd/Ctrl+F in a block editor, a table cell editor or a front matter field opens the find bar at once, so the first characters you type go into the find query instead of the Markdown.
- A table cell editor that opens after you pressed Cmd/Ctrl+F no longer takes the focus from the find field.
- Two causes of a comment thread losing its highlight or badge are fixed: a new thread no longer stays hidden until a reload, and threads are placed again after a reload from disk, a revert, an undo to the saved text, or an edit while the comments file is saved.
- Mermaid flowchart labels are no longer cut off in the VS Code preview: labels are measured and drawn with the same system font and size, and they stay HTML labels.
- The editor no longer edits the wrong text when the preview and the document disagree about a block's lines: it asks you to refresh and changes nothing.
- A GitHub alert (`> [!NOTE]`) inside a `:::{card}`, a `:::{tab-item}` or another colon container no longer ends that container early.

## Enhancements

- A click in the body of a GitHub alert in edit mode opens the whole alert, not only the clicked paragraph.

## Documentation

- The Marketplace listing is now filed under Programming Languages and Formatters, with the keywords markdown, OKF and MyST. The README announces 1.0, and the requirements page links its `tiers/` folder.
