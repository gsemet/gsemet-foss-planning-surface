## A writer inserts MyST constructs

### Normative behavior

When a writer works in the MyST or the Full palette mode, the Studio SHALL offer palette buttons and slash commands that write admonitions, definition lists, math, roles, labels, references, citations, figures, tabs and, in the Full mode, charts and diagrams into the block text at the selection, each in one undoable step, or leave the text unchanged and say why when the action cannot apply.

### Preserved stakeholder intent

Writers of Sphinx and MyST documents expect to insert a directive or a role from a button without remembering its syntax.

As a writer of Sphinx and MyST documents, I insert an admonition, a definition list, a formula, a role, a figure or a tab set from a button or the slash menu without remembering the syntax, and take the insertion back with a single undo.

### Rationale and constraints

- These buttons are offered from the MyST mode up; the GitHub buttons are listed there too, because the modes add up, and the Full mode adds the chart and diagram commands.
- Both the GitHub key button (HTML kbd element) and the MyST key button (kbd role) are offered in the MyST mode, and nothing in the Studio tells which of the two to prefer.
- A construct is written into the text of the block; the preview renders it afterwards.
- A selection that a role cannot hold, such as one with a backtick, produces no edit.
- Each insertion is one undoable edit, saved with the other text of that editor.

### Use case diagram

```mermaid
sequenceDiagram
    actor Writer
    participant Palette as Palette or slash menu
    participant Action as MyST action
    participant Box as Text box
    Writer->>Palette: press Admonition or type /admonition
    Palette-->>Writer: list of admonition types
    Writer->>Palette: choose a type
    Palette->>Action: run on the touched lines
    alt the type is known
        Action->>Box: wrap the lines in a colon fence, one edit
        Writer->>Box: undo
        Box-->>Writer: the text is as it was
    else the type is missing or unknown
        Action-->>Writer: the text is unchanged
    end
```

An admonition is one undoable edit around the touched lines.

### Main paths

#### Path 1: Wrap lines in an admonition

1. The palette is shown above the text box in the MyST mode
   - SwRS-MDOKFSTUDIO-PALETTE-127: the writer presses Admonition and chooses a type, and the touched lines are wrapped in a colon fence of that type
   - Option SwRS-MDOKFSTUDIO-PALETTE-127 (refusal): a missing or unknown type produces no edit
2. The lines are wrapped in a fence
   - SwRS-MDOKFSTUDIO-PALETTE-039: the writer undoes and the edit is taken back in one step
3. The text is as it was before the button
