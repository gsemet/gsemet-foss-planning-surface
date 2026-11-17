## Summary

In edit mode, the text boxes of blocks and table cells ignored the usual editor shortcuts: undo did
nothing, so a mistake could not be cancelled. These shortcuts now follow VS Code: undo (Cmd/Ctrl+Z,
several steps), redo (Cmd+Shift+Z / Ctrl+Y), select all (Cmd/Ctrl+A, limited to the focused text
box) and delete line (Cmd/Ctrl+Shift+K).

## Deliverables

Each action is a VS Code command with a default key binding gated on the preview edit context, so
a user's own keybinding overrides apply. The page lets the key reach VS Code, which sends the
command back to the focused text box.

```text
key press -> page (native action cancelled) -> VS Code keybinding -> command -> focused text box
```

Before / after (delete line, cream and dark themes; undo shots sit beside them):

| Shortcut | Before | After |
| --- | --- | --- |
| Delete line, cream | ![](reports/shots/before-cream-delete-line.png) | ![](reports/shots/after-cream-delete-line.png) |
| Delete line, dark | ![](reports/shots/before-dark-delete-line.png) | ![](reports/shots/after-dark-delete-line.png) |
| Undo, cream | ![](reports/shots/before-cream-undo.png) | ![](reports/shots/after-cream-undo.png) |
| Undo, dark | ![](reports/shots/before-dark-undo.png) | ![](reports/shots/after-dark-undo.png) |

(Screenshots are to be pushed to the assets branch and linked by raw URL by the stack driver.)

Also: new requirement, user documentation (editing page), changelog entry, unit tests and a real
VS Code window scenario covering two undo steps, redo, select all, delete line and undo of the delete.

## Autonomous decisions

- Defaults are VS Code's: Cmd/Ctrl+Z, Cmd+Shift+Z / Ctrl+Y, Cmd/Ctrl+A, Cmd/Ctrl+Shift+K.
- The request asked for Cmd/Ctrl+K to delete a line; VS Code's delete-line is Cmd/Ctrl+Shift+K and
  Cmd/Ctrl+K is a chord prefix (and the link panel here), so VS Code's binding is followed.
- Select all selects the text box content only, not the page.
- Frontmatter fields keep their previous behaviour.

## Known limits

A key pressed in the instant between an editor opening and the host setting its context key has its
native action cancelled and does nothing.

## Internal references

- Change request 119, backlog item ctrl-z-now-working; requirement SwRS-MDOKFSTUDIO-BLOCK-002.
- Review nit: BLOCK-002 verification notes cite a nonexistent `realInput.test.ts`; the test is
  `test/integration/editKeys.test.ts`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
