# UX-21 — Adding and removing fields: required fields offered for removal, new fields appended at the end

| Field | Value |
| --- | --- |
| Severity | Low |
| Confidence | Reproduced |
| Area | Frontmatter add/remove/rename |
| Evidence | [r3-fm-remove-required.jpg](../../evidence/r3-fm-remove-required.jpg), [r3-fm-add-open.jpg](../../evidence/r3-fm-add-open.jpg) |

## Observed

- **Remove** (⊟) is enabled on required fields. Clicking it on `scope` shows a clear error
  ("Cannot remove required frontmatter field "scope".") in a large red box that stays visible
  while the user starts another action.
- **Add** (⊞) offers only schema properties not yet present (here only `depends_on`). There is no
  free-form key, even when the schema allows additional properties or when no schema matches.
- The new field is appended at the end of the frontmatter (`depends_on: []` after
  `tested_in_files`), not next to the row where the user clicked ⊞, and it is added as an empty
  value without opening its editor.
- The confirm button is disabled until a field is chosen, but nothing explains that a second click
  is needed after choosing.

## Suggested direction

Disable ⊟ with a tooltip on required fields; allow "Custom key…" in the add picker when
`additionalProperties` is not `false`; insert after the current row (or in schema order); open the
new field's editor immediately; auto-confirm on selection.

## Done when

Adding a field is one choice followed by typing its value, and removal is impossible (not just
refused) for required fields.
