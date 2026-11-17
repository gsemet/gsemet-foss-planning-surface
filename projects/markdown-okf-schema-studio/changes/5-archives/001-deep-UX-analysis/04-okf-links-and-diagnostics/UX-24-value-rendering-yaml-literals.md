# UX-24 — Property values are displayed with YAML syntax (`- item`, `[]`, `null`)

| Field | Value |
| --- | --- |
| Severity | Low |
| Confidence | Observed |
| Area | Properties table rendering |
| Evidence | [r3-projectroot.jpg](../evidence/r3-projectroot.jpg) |

## Observed

- List values are prefixed with a YAML dash: `- StRS-CORE-001`.
- Empty lists render as `[]`, null values as `null`, and a field missing from the schema shows the
  type label "(unknown)".
- The type label "(boolean)" wraps under the field name in a 200 px column.

## Expected

A properties panel shows data, not YAML: list items as chips or bullet-less lines, empty values as
a muted "Empty", null as "—". Type labels can be icons with tooltips (the icon is already there).

## Done when

No raw YAML tokens appear in read mode.
