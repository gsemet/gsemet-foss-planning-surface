# UX-23 — Diagnostics appear as bare codes ("[E10]") with the explanation hidden in a native tooltip

| Field | Value |
| --- | --- |
| Severity | Medium |
| Confidence | Observed |
| Area | Properties table diagnostics |
| Evidence | [r3-swrs.jpg](../evidence/r3-swrs.jpg) |

## Observed

- Invalid links render as red text with a suffix: `src/export.py [E10]`.
- The explanation exists only in the `title` attribute of the link span and of the row
  ("[E10] target 'src/export.py' does not resolve to a file at 'implemented_in_files[0]'"). It
  appears after the native tooltip delay, not on keyboard focus, and not in the custom tooltip
  used for valid links.
- The header counter "Frontmatter properties ✖ 2" is not clickable and does not list the issues.
- Errors are not reported in the Problems panel, so they are invisible when the preview is closed.

## Expected

Each issue shows a short human message next to the value ("File not found"), the details in the
custom tooltip (keyboard accessible), and the header counter jumps to the first issue or expands a
list. Ideally, schema and link issues are also published as VS Code diagnostics on the frontmatter
lines.

## Suggested direction

Reuse the link tooltip component for invalid links; replace `[E10]` by an icon + message; publish
a `DiagnosticCollection` keyed on frontmatter line ranges.

## Done when

A user can understand every red value without hovering for a second or reading an error code.
