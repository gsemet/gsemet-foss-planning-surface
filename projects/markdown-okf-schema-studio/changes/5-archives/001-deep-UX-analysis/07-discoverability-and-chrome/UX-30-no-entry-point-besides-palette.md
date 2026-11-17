# UX-30 — The preview can only be opened from the Command Palette

| Field | Value |
| --- | --- |
| Severity | Medium |
| Confidence | Observed (manifest checked) |
| Area | Discoverability |
| Evidence | [u01-open-preview.jpg](../evidence/u01-open-preview.jpg) (no Studio icon in the editor title bar) |

## Observed

`package.json` contributes two commands and a palette entry, but no `menus.editor/title` button,
no `editor/title/context` or `explorer/context` entry, and no keybinding. A user who installs the
VSIX sees nothing new in the UI; the built-in Markdown preview's "Open Preview to the Side" icon is
the only visible preview button.

## Suggested direction

Contribute an editor-title icon for `resourceLangId == markdown` (next to the built-in one, with a
distinct icon), explorer and tab context-menu entries ("Open with Markdown OKF-Schema Studio"), and
a keybinding (for example Cmd+K Shift+V, avoiding the built-in Cmd+K V).

## Done when

A first-time user finds the preview from the editor title bar of any Markdown file.
