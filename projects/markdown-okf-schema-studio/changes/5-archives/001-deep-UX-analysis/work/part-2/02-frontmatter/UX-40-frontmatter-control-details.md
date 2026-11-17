# UX-40 — Frontmatter controls ignore schema hints (bounds, required enums, labels)

| Field | Value |
| --- | --- |
| Severity | Low |
| Confidence | Observed |
| Area | Frontmatter properties table controls |

## Observed

- Number fields use `<input type="number">` without the schema's `minimum`/`maximum`, so the
  spinner and the browser accept 9 for a field limited to 1-5; only the save-time validation
  catches it ("Schema validation failed: must be <= 5", which is clear enough).
- The enum dropdown for the **required** `status` field includes an empty option.
- The table header reads "Name / Value" when a schema matches and "Names / Values" when none does.
- Positive: date fields use a native date input, enum fields a dropdown, comments in the YAML are
  preserved, and `preview_shows_fields` shows the linked note's status next to the link.

## Suggested direction

Propagate `minimum`, `maximum`, `multipleOf`, `minLength`, `maxLength`, and `pattern` to the native
controls; omit the empty option for required enums; use one header wording.

## Done when

Controls prevent the values the schema rejects before the user saves.
