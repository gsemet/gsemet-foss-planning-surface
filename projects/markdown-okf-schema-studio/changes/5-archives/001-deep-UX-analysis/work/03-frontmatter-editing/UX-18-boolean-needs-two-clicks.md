# UX-18 — A boolean checkbox needs two clicks to toggle

| Field | Value |
| --- | --- |
| Severity | Medium |
| Confidence | Reproduced |
| Area | Frontmatter properties table editing (booleans) |
| Evidence | [r3-fm-bool-click1.jpg](../../evidence/r3-fm-bool-click1.jpg) |

## Observed

In edit mode the `annotation_exemption` value is rendered as a checkbox next to "false". The first
click on the checkbox only opens the cell editor (a new checkbox gets focus, state unchanged). A
second click toggles it and commits. Users who click once see nothing happen and may click twice
quickly, or give up.

## Expected

In edit mode, one click on a boolean toggles and commits it (with the usual validation), like
Obsidian properties.

## Suggested direction

Render the read-mode checkbox as the actual control in edit mode, or forward the opening click to
the editor's checkbox.

## Done when

One click toggles a boolean field.
