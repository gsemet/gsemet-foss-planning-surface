# UX-43 — In a narrow preview, the properties table breaks words and clips values

| Field | Value |
| --- | --- |
| Severity | Medium |
| Confidence | Observed at 360 px (sash dragged in a 1440 px window) |
| Area | Responsive layout |
| Evidence | [p2-narrow.jpg](../evidence/p2-narrow.jpg) |

## Use case

A laptop user keeps the preview narrow next to the source editor (a common split with the
Explorer open).

## Observed

- Field names break in the middle of words: `annotation_exem` / `ption`, `implemented_in_` /
  `files`, with the type label on a third line.
- Values overflow the right edge and are clipped: `tests/test_expor…` is cut with no ellipsis.
- The floating toolbar sits on top of the "Frontmatter properties ✖ 2" header, hiding the error
  count.
- About 50 px of horizontal padding on each side remains, while the table needs the width.

## Suggested direction

Below about 480 px, switch the properties table to a stacked layout (name and type above the
value), allow `overflow-wrap: anywhere` only for values, and reduce the content padding. Reserve
space for the toolbar, or collapse it into a single menu button at narrow widths.

## Done when

The visual scenario "properties table at 360 px" shows complete names and values.
