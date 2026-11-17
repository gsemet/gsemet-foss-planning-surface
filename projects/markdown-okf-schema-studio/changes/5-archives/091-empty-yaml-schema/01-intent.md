# An empty YAML schema file makes the frontmatter analysis throw

User decision (2026-10-24): P3. Messages are defined in okf-schema, not here:
https://github.com/gsemet/okf-schema/issues/41

Current behaviour (SwRS-MDOKFSTUDIO-FMSCHEMA-023 (was SwRS-MDOKFSTUDIO-FMSCHEMA-025), Known issue): `parseSchemaFile`
(`src/core/frontmatter/okfFrontmatter.ts`) reads an empty or comment-only `.schema.yaml` as
`null` without error; `effectiveProperties` then reads `properties` on `null` outside the `try`
that shows "Schema could not be parsed", and the analysis throws. An empty `.schema.json` gives
the warning row instead. Real case: a schema file just created with "New File", not yet written.

## Expected

- Never analyse against an empty schema: a schema file that is empty right after creation is not
  filled yet, so the analysis waits for content (the same outcome as okf-schema, where the type
  has no schema) and never throws.
- The message, if any, follows what okf-schema issue #41 decides; do not invent our own wording.
- Unit test with an empty and a comment-only YAML schema; update FMSCHEMA-025 in the same change.

Requirement ids older than the baseline merge map to their current tile in `.agents/changes/archives/059-requirements-okfreq/reduction/mapping.csv`.
