# UX-39 — Object fields: "unknown" type, de-indented YAML, and raw parser errors

| Field | Value |
| --- | --- |
| Severity | Medium |
| Confidence | Reproduced |
| Area | Frontmatter properties table (objects, YAML errors) |
| Evidence | [p2-fm-object-after.jpg](../evidence/p2-fm-object-after.jpg), [p2-broken.jpg](../evidence/p2-broken.jpg) |

## Observed

- `owner` is declared `type: object` in `edge.schema.yaml`, yet the table labels it "(unknown)".
- Its editor shows the mapping **de-indented** (`name: Ada` instead of `  name: Ada` as in the
  source). Adding a key the way it looks in the file (`  role: lead`) produces a YAML error.
- The error is the raw `yaml` library message, about ten lines with `^` caret markers that do not
  align in a proportional font, positions relative to the textarea ("line 2, column 7"), and two
  messages joined by `;`. It is partly hidden by the row menu and the floating toolbar.
- For invalid YAML frontmatter (`synth/broken.md`), the banner reports "line 2, column 16" while
  the bad line is line 3 of the file (frontmatter-relative numbering).
- Literal block scalars (`notes: |`) are displayed on one line in read mode; their line breaks are
  lost.

## Suggested direction

Map `type: object` to an "object" label and icon; edit nested mappings as sub-rows (key/value
pairs) instead of raw YAML, or keep the source indentation in the textarea; translate parser errors
into one sentence with a file line number ("Line 20: indentation does not match the other keys");
render literal blocks with `white-space: pre-line`.

## Done when

Adding a key to an object field works on the first try, and every YAML error names a file line.
