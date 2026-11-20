## A writer formats text with buttons and shortcuts

### Normative behavior

When a writer edits a block in edit mode, the Studio SHALL offer palette buttons, slash commands and keyboard shortcuts that format the text at the selection or the caret, each in one undoable step saved with the other text of that editor, or leave the text unchanged and say why when the action cannot apply.

### Preserved stakeholder intent

Writers expect formatting buttons to act on the selection like in any editor, and to be told why when one cannot apply.

As a writer, I format text from buttons, slash commands or keyboard shortcuts without typing the syntax, take any such edit back with a single undo, and am never left with half-written markup.

### Rationale and constraints

- The buttons act on the selection or at the caret of the block text box; they only change the text, the preview renders it afterwards.
- The same actions are reachable from the slash menu and, for a few of them, from keyboard shortcuts; the tooltip of a button shows its shortcut.
- An action that cannot apply, such as a selection that cuts into a marker, produces no edit and the writer is told why.
- A button, a slash command or a keyboard shortcut changes the text in one step that the undo key combination of the text box reverts; the edit is saved with the autosave of the editor like typing.
- The command key is Cmd on macOS and Ctrl elsewhere; the typed letter wins over the physical key, so other keyboard layouts keep their cut, copy and paste.
- Every button of the edit bar shows a tooltip with its title and shortcut.

### Use case diagram

```mermaid
sequenceDiagram
    actor Writer
    participant Palette as Palette, slash menu or shortcut
    participant Action as Formatting action
    participant Box as Text box
    Writer->>Palette: press a button, pick a command or type a shortcut
    Palette->>Action: run on the selection or the caret
    alt the action returns an edit
        Action->>Box: one native edit, saved by the autosave
        Writer->>Box: undo
        Box-->>Writer: the text is as it was
    else the action returns nothing
        Action-->>Writer: the text is unchanged and the status line gives the reason
    end
```

A formatting action is one undoable edit, or no edit with a reason.

### Main paths

#### Path 1: Bold a word, then take it back

1. A block text box is open in edit mode
   - SwRS-MDOKFSTUDIO-PALETTE-001: the palette opens above the text box with the Palette buttons select and the buttons of the mode in registry order
2. The palette is shown above the text box
   - SwRS-MDOKFSTUDIO-PALETTE-276: the writer presses Bold and the selection is wrapped in two asterisks
   - Option SwRS-MDOKFSTUDIO-PALETTE-039 (refusal): an action that makes no edit leaves the text unchanged
3. The selection is wrapped in markers
   - SwRS-MDOKFSTUDIO-PALETTE-039: the writer undoes and the edit is taken back in one step
4. The text is as it was before the button
