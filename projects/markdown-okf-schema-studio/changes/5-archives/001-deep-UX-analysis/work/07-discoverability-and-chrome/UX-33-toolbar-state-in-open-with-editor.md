# UX-33 — The Open With editor shows an active anchor toggle and forgets edit mode

| Field | Value |
| --- | --- |
| Severity | Low |
| Confidence | Observed |
| Area | Floating toolbar |
| Evidence | [r2-custom-editor.jpg](../../evidence/r2-custom-editor.jpg) |

## Observed

- In the Open With editor there is no paired text editor, yet the anchor ("lock") button is shown
  in its active blue state. Clicking it has no visible effect.
- Edit mode is stored per webview: it was on in the side preview and off in the Open With editor
  opened a minute later. Users who mostly edit must re-enable it in every new view and after every
  reload.
- The toolbar icons (refresh, lock, pencil, monitor) have tooltips but no text; "lock" for "sync
  scrolling with the editor" and "monitor" for "theme" are not self-explanatory.

## Suggested direction

Hide (or disable with a tooltip) the anchor button when no text editor shows the same document;
persist edit mode per workspace (`workspaceState`) or offer a setting
`markdownOkfSchemaStudio.preview.startInEditMode`; consider a "sync scroll" icon instead of a lock.

## Done when

Every toolbar control does something in the view where it is shown, and edit mode survives
reopening.
