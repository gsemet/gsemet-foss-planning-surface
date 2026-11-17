# QA-01 — Round-trip tests use fixtures already written in the serializer's own style

| Field | Value |
| --- | --- |
| Severity | High (test gap that let UX-12 and UX-16 ship) |
| Confidence | Code review of the tests |
| Area | Unit tests: `test/webview/markdownTable.test.ts`, `test/frontmatter/okfFrontmatter.test.ts` |

## Observed

- `markdownTable.test.ts` asserts `serialize(parse(source)) === source`, but every source table is
  already in canonical form: `| A | B |` cells with one space and `| --- |` delimiters. Compact
  delimiters (`|---|`, used throughout `book/chapters/`) and padded/aligned tables are never
  tested, so the whole-table rewrite of
  [UX-12](../02-table-editing/UX-12-cell-edit-rewrites-whole-table.md) passes.
- `okfFrontmatter.test.ts` checks that comments survive, but the array fixture is written with
  indented sequences (`  - alpha.md`), which is exactly what `document.toString()` produces. No
  test edits field A and asserts that field B's lines are byte-identical, so the re-serialization of
  [UX-16](../03-frontmatter-editing/UX-16-field-edit-reserializes-frontmatter.md) passes.

These asserts are not wrong, but they are aimed at the wrong property: they prove that canonical
input stays canonical, not that user formatting is preserved.

## Suggested change

Add property-style tests over a corpus of real formatting variants (compact and padded tables,
alignment rows, CRLF; compact and indented YAML sequences, folded and literal scalars, flow
collections, comments): edit one cell/field and assert that only the expected lines differ
(`diffLines` count == 1). Seed the corpus from `book/chapters/` and `okf-schema/examples/`.

## Done when

The suites fail on the current serializers and pass after UX-12/UX-16 are fixed.
