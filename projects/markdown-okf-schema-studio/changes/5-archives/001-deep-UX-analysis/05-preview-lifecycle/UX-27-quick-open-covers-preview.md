# UX-27 — Opening a file while the preview has focus buries the preview

| Field | Value |
| --- | --- |
| Severity | Low |
| Confidence | Reproduced (VS Code default behaviour, amplified by the edit workflow) |
| Area | Side preview layout |

## Use case

An author edits inline in the side preview (focus is in the preview), then presses Cmd+P to open
another chapter.

## Observed

VS Code opens the file in the active group, which is the preview's group. The new text editor
covers the preview; the preview follows it and now shows the same file it is hidden behind. The
user ends up with two text editors and no visible preview until they move tabs around. Edit mode
makes this frequent, because inline editing keeps focus in the preview group.

## Expected

The preview group behaves as a side panel: files opened from it land in the source group.

## Suggested direction

Options to evaluate: when a text editor for a Markdown file opens in the preview's group, move it
to the source group (`workbench.action.moveEditorToPreviousGroup`) and re-reveal the preview; or
lock the preview group (`workbench.action.lockEditorGroup`) when the side preview is created.

## Done when

Cmd+P from the preview never hides the preview.
