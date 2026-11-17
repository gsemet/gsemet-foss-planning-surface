<!-- Proof B — "Compact": no pictures, a summary table, one dense list per theme. Reads well in
     the GitHub release page and in the VS Code Marketplace changelog tab. -->

# 1.0.0 — The editable preview

Markdown OKF Schema Studio 1.0 turns the VS Code preview into a page you can **read, review and
edit**: MyST rendered like Sphinx, diagrams and charts built in, comments and change bars in place.

| | Since 0.3.1 |
| :-- | --: |
| New features | 70 |
| Fixes | 102 |
| Performance | 13 |

> [!IMPORTANT]
> Removed: `markdownOkfSchemaStudio.preview.doubleClickToSwitchToEditor` (no effect).
> Contributors: Python 3.11+ for the build and documentation tools.

## Editing

- **Block editor in the preview** with an edition palette in three modes (Strict, GitHub, MyST):
  bold, italic, link (<kbd>Cmd</kbd>+<kbd>K</kbd>), image, figure, table grid, colour, emoji,
  admonition, reference, and a <kbd>/</kbd> slash menu.
- **Tables**: insert and move rows and columns by drag handles, cell editor, padding kept.
- **Paste**: screenshots saved next to the document, rich text as Markdown, URLs as links.
- **Keyboard**: select, move (<kbd>Alt</kbd>+<kbd>↑</kbd>/<kbd>↓</kbd>), copy blocks; walk into
  tables, cards and tabs; VS Code undo, redo and delete-line keys.

## Rendering

- **MyST**: cards, grids, tabs, list tables, figures (`:width:`, `:align:`), version notes,
  `{toctree}`, `{include}`, `{code-block}`.
- **Diagrams and charts**: PlantUML without Java (`{uml} file.puml` too), Vega-Lite and Vega,
  clearer Mermaid errors.
- **GitHub flavour**: README HTML (`<div align>`, `<picture>`, `<details>`), `[TOC]`, `~~strike~~`,
  red `[!CAUTION]`, right-to-left paragraphs.
- Code highlighted by the VS Code TextMate grammars, with a copy button.

## Reviewing

- Comment threads anchored to the text, inline `<!-- THREAD -->` comments, TODO chips.
- Green change bars since the last commit, front matter rows included.

## Navigating

- Floating toolbar in five rows: refresh, edit, fold; side panel link, Back / Next; theme, zoom;
  width, table of contents; collapse all, diff, comment.
- Find and replace, section folding, sticky headings.

## Speed, safety

- Render off the extension host thread; stale renders stopped; faster long documents.
- Restricted Mode renders everything and runs nothing; PlantUML Java with the `ALLOWLIST` profile.

**Full list:** [CHANGELOG.md](https://github.com/gsemet/markdown-okf-schema-studio/blob/main/CHANGELOG.md) ·
**Install:** [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=GaetanSemet.markdown-okf-schema-studio)
