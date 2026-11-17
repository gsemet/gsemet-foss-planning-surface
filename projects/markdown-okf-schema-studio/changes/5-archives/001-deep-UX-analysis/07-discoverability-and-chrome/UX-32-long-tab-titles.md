# UX-32 — Tab titles are long and repeat the product name

| Field | Value |
| --- | --- |
| Severity | Low |
| Confidence | Observed |
| Area | Workbench chrome |
| Evidence | [r2-custom-editor.jpg](../evidence/r2-custom-editor.jpg), [u01-open-preview.jpg](../evidence/u01-open-preview.jpg) |

## Observed

Both the side preview and the Open With editor are titled
"Markdown OKF-Schema Studio: 01-handbook-overview.md". In the Open With case the tab is an editor
for the file, so the prefix pushes the filename out of view as soon as a few tabs are open; the
window title becomes equally long.

## Suggested direction

Side preview: "Studio · 01-handbook-overview.md" (or "Preview 01-handbook-overview.md", like the
built-in preview). Open With editor: the filename alone; VS Code already shows the editor type in
the breadcrumb switcher.

## Done when

The filename is visible in a 160 px tab.
