## A writer inserts GitHub Flavored Markdown constructs

### Normative behavior

When a writer works in the GitHub Flavored Markdown or a larger palette mode, the Studio SHALL offer palette buttons and slash commands that write alerts, task list boxes, collapsible sections, footnotes, keyboard keys and choice lists into the block text at the selection, each in one undoable step, or leave the text unchanged and say why when the action cannot apply.

### Preserved stakeholder intent

Writers of GitHub-style documents expect to insert a construct from a button without remembering its syntax.

As a writer of GitHub-style documents, I insert an alert, a task list, a collapsible section or a footnote from a button without remembering the syntax, and take the insertion back with a single undo.

### Rationale and constraints

- These buttons are offered from the GitHub Flavored Markdown mode up: the MyST and Full modes list them too, because the modes add up.
- A construct is written into the text of the block; the preview renders it afterwards.
- An action that cannot apply, such as an alert command inside an alert, produces no edit.
- Each insertion is one undoable edit, saved with the other text of that editor.

### Use case diagram

```mermaid
sequenceDiagram
    actor Writer
    participant Palette as Palette or slash menu
    participant Action as GFM action
    participant Box as Text box
    Writer->>Palette: press Alert or type /alert
    Palette->>Action: run on the touched lines
    alt the caret is outside an alert
        Action->>Box: quote the lines under a note head, one edit
        Palette-->>Writer: list of alert types at the caret
        Writer->>Palette: choose a type
        Palette->>Box: the type word of the head is replaced
    else the caret is already in an alert
        Action-->>Writer: the text is unchanged
    end
```

An alert is one undoable edit followed by a choice of its type.

### Main paths

#### Path 1: Insert an alert

1. The palette is shown above the text box in the GFM mode
   - SwRS-MDOKFSTUDIO-PALETTE-115: the writer presses Alert and the touched lines are quoted under a note head, with a list of the five types at the caret
2. An alert is written and its type list is open
   - SwRS-MDOKFSTUDIO-PALETTE-039: the writer undoes and the edit is taken back in one step
3. The text is as it was before the button
