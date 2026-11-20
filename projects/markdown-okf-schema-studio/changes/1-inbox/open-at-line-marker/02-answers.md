# Answers

Short name: `open-at-line`

## Series 1, 2026-11-20

1. open-at-line-Q1: **How Studio gets the line.** A, Studio decides itself to open `.md` files: a Studio setting ("open Markdown files in Studio") replaces the VS Code `workbench.editorAssociations` entry; the text editor opens for a moment at the line, then Studio takes its place at that line, with the marker. (Context given: with the association, `resolveCustomTextEditor` receives no line; only a text editor gets it.)
2. open-at-line-Q2: **Entry points.** A, all of them, no closed list: whatever opens the text editor at a line (search, Quick Open `file.md:42`, Problems panel, terminal links, Ctrl+click, Outline...).
3. open-at-line-Q3: **File already open in Studio.** A, the same Studio tab scrolls to the new line and the marker moves; no new tab.
4. open-at-line-Q4: **Raw text asked on purpose.** A, Studio never replaces a text editor the user asked for on purpose ("Reopen Editor With > Text Editor", a Studio "open source" action): the text editor stays.
