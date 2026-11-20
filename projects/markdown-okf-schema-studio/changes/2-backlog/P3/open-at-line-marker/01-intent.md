# Open Studio at a searched line and mark it with an arrow

## The request

The owner (2026-11-20): when a VS Code search result (or any "open at line" action) opens a
Markdown file, Studio opens at the top of the document instead of at that line. Studio should
scroll to the requested line and show a marker on it, ideally an arrow in the left margin. A new
feature, to be designed and tested well.

## What happens today (exploration at release 1.10.0, origin/main dd89211d)

- The owner's VS Code makes Studio the default editor of `*.md`
  (`workbench.editorAssociations`: `"*.md": "markdown-okf-schema-studio.editor"`). The manifest
  declares the editor with priority `option`; the association is the user's own setting.
- A search result, Go to Line in Quick Open (`file.md:12`), a problem, a terminal link or a
  Ctrl+click opens the file through VS Code's editor service with a selection. With the
  association, VS Code opens the Open-With editor and calls
  `resolveCustomTextEditor(document, webviewPanel, token)` (`src/host-vscode/activation.ts`,
  `resolvePreviewEditor`). That call carries no selection and no options: the API gives the
  extension no way to learn the requested line (documented by the API typings,
  `CustomTextEditorProvider.resolveCustomTextEditor` in `@types/vscode`; the VS Code custom-editor
  guide leaves selection to the extension). The line is lost before Studio sees it.
- Without the association, the same actions open a text editor at the line; a side preview that
  follows the active editor (`scrollPreviewWithEditor`, on by default) scrolls to it through the
  scroll sync (`src/session/features/scrollSync.ts`, `sourceScroll` message), and the optional
  setting `markEditorSelection` (off by default) outlines the block that holds the cursor line
  (SwRS-MDOKFSTUDIO-TOOLBAR-128, `markSourceLine` in `src/page/features/scrollCore.ts`).
- The page already knows how to go to a source line: the `data-line` source map
  (`parseMappings`, `scrollAtLine`) and, inside a multi-line block, the top of each line
  (`measureLineTops`, used for code blocks).

## The way that is open

Since VS Code gives the line only to a text editor, Studio must catch the opening in a text
editor and then show itself at that line: Studio decides itself to open `.md` files (its own
setting instead of the VS Code association), lets the text editor open, reads its selection, and
replaces it by the Studio tab scrolled to the line, with the marker. Whether this works without a
visible flash, with an already open Studio tab, and with "Reopen Editor With > Text Editor" is
unproved: the trials are part of the specification.

## Open points for the grill

Entry points covered; the switch from the VS Code association to Studio's own choice; the marker
(shape, place, when it goes away); edit mode and view mode; a line inside a block (paragraph,
code block, table, folded section); the side preview; accessibility; the tests (unit, visual
captures, real VS Code integration).
