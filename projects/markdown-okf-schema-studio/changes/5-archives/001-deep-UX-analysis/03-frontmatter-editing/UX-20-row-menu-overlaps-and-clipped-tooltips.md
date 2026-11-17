# UX-20 — Frontmatter row menu hides values, and its tooltips are clipped

| Field | Value |
| --- | --- |
| Severity | Low |
| Confidence | Observed in three states |
| Area | Frontmatter properties table editing |
| Evidence | [r3-fm-remove-required.jpg](../evidence/r3-fm-remove-required.jpg), [r3-fm-add-open.jpg](../evidence/r3-fm-add-open.jpg), [r3-fm-list-add.jpg](../evidence/r3-fm-list-add.jpg) |

## Observed

- The ⊞/⊟ menu of the open field floats over the **previous row's value**: `uuid` (partially
  hidden), `origin: native` (hidden), `project: OKFREQXMP` (shows "MP").
- The menu's tooltips ("Add frontmatter field", "Remove frontmatter field") are positioned to the
  left of the buttons and clipped by the webview edge ("ntmatter field").
- The add-field `<select>` and its confirm button sit over the next rows and the preview's right
  edge.
- Single-word scalars (`scope: Core`) open a tall multi-line textarea; with an error message the
  row grows to about 170 px.

## Suggested direction

Attach the row actions inside the row (an actions column, or a kebab button at the row end),
position tooltips with viewport clamping (as the link tooltip already does), and size text
controls from their content.

## Done when

No editing control covers another row's value, and every tooltip is fully visible at 540 px
preview width.
