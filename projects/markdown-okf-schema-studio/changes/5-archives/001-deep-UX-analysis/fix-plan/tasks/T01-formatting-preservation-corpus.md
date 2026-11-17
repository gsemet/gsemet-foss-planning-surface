# T01 — Formatting-preservation corpus for tables and frontmatter

| Field | Value |
| --- | --- |
| Fixes | [QA-01](../../08-test-campaign-gaps/QA-01-roundtrip-fixtures-match-serializer-style.md) |
| Depends on | T00 |
| Gate | `unit` |
| Risk | None (tests only) |
| Commit message | `test(vscode): add formatting-preservation corpus for tables and frontmatter` |

## Goal

The current round-trip tests only feed the serializers input that is already in their own style.
Add tests that edit **one** cell or field of real-world formatting variants and require that every
other byte stays identical.

These tests encode the contract that T04 (tables) and T05/T06 (frontmatter) must satisfy. They fail
today. Mark every test that fails today with `{ todo: "<finding> (<task>)" }` so the suite stays
green. The fixing tasks remove the markers.

## Allowed files

- `test/webview/markdownTablePreservation.test.ts` (new)
- `test/frontmatter/frontmatterPreservation.test.ts` (new)
- `test/shared/lineDelta.ts` (new helper)

## Helper `test/shared/lineDelta.ts`

```ts
/** Lines removed from `before` and added in `after`, after trimming common leading and trailing lines. */
export function lineDelta(before: string, after: string): { removed: string[]; added: string[] }
```

- Split on `\n` only, so `\r` stays at the end of CRLF lines and line-ending changes are detected.
- Trim the common prefix of lines, then the common suffix, without overlapping.
- Return what remains.

Add 3 small tests of the helper inside `markdownTablePreservation.test.ts`: identical input, one
changed line, one inserted line.

## Table corpus (`markdownTablePreservation.test.ts`)

Use `createMarkdownTableTools()` from `src/webview/markdownTable.ts`. The public flow the runtime
uses, which T04 must keep, is:

```ts
const tools = createMarkdownTableTools();
const model = tools.parse(source)!;
model.rows[rowIndex][columnIndex] = "new value";   // rowIndex counts the delimiter row as index 1
const output = tools.serialize(model);
```

Corpus. Each entry is a name, the source, the cell to edit, the new value, and the exact expected
new line.

| Name | Source (`\n`-joined unless stated) | Edit | Expected changed line |
| --- | --- | --- | --- |
| compact-book | `\| Step \| Owner \|`, `\|---\|---\|`, `\| Plan \| Ana \|`, `\| Ship \| Bo \|` | `rows[2][1]` = `Ana Lee` | `\| Plan \| Ana Lee \|` |
| padded | `\| Column A \| Column B \|`, `\|----------\|----------\|`, `\| first    \| second   \|` | `rows[2][1]` = `second X` | `\| first    \| second X \|` |
| no-spaces | `\|a\|b\|`, `\|---\|---\|`, `\|c\|d\|` | `rows[2][1]` = `dee` | `\|c\|dee\|` |
| alignment | `\| L \| R \| C \|`, `\| :--- \| ---: \| :---: \|`, `\| 1 \| 2 \| 3 \|` | `rows[2][2]` = `30` | `\| 1 \| 2 \| 30 \|` |
| no-outer-pipes | `a \| b`, `--- \| ---`, `c \| d` | `rows[2][1]` = `dd` | `c \| dd` |
| escaped-and-code | see the code block below | `rows[3][1]` = `w` | `\| k \| w \| z \|` |
| indented | `  \| a \| b \|`, `  \|---\|---\|`, `  \| c \| d \|` | `rows[2][0]` = `cc` | `  \| cc \| d \|` |
| crlf | the compact-book table joined with `\r\n`, plus a trailing `\r\n` | `rows[3][1]` = `Bob` | `\| Ship \| Bob \|\r` (as returned by `lineDelta`) |
| wider-than-padding | the padded table | `rows[2][0]` = `a much longer value` | `\| a much longer value \| second   \|` |

The pipes in the Source column are shown escaped (`\|`) because of the Markdown table. Write real
`|` characters in the test. The `escaped-and-code` source is exactly these four lines (row 2 holds
an escaped pipe and a code span containing a pipe; it must round-trip untouched):

```text
| Key | Value | Code |
|---|---|---|
| a \| b | x | `y|z` |
| k | v | z |
```

Tests:

1. **Round trip.** For every corpus source, `serialize(parse(source)) === source`.
2. **One-cell edit.** For every corpus entry, `lineDelta(source, output)` is `removed.length === 1`,
   `added.length === 1`, and `added[0] === expected`.
3. **Padding rule.** This is the T04 contract, documented in the test as a comment:
   - Keep the edited cell's leading whitespace.
   - If the cell had trailing whitespace, pad with spaces so the segment between the pipes keeps
     its original width.
   - When the new text is too long, use exactly one trailing space.
   - A cell without surrounding whitespace stays without.

Mark the round-trip tests for sources that are not already in the canonical `| a | b |` +
`| --- |` style, and the one-cell-edit tests that fail today, with
`{ todo: "UX-12 (T04)" }`. **Run the suite first**, then mark exactly the tests that fail. Do not
mark passing tests.

## Frontmatter corpus (`frontmatterPreservation.test.ts`)

Use `createFrontmatterFieldPatch`, `createFrontmatterFieldRenamePatch` and
`createFrontmatterFieldRemovePatch` from `src/frontmatter/okfFrontmatter.ts`. Apply a patch with
`source.slice(0, patch.start) + patch.text + source.slice(patch.end)`.

### F1 — real OKF requirement (compact sequences, plain multi-line scalar)

```yaml
---
type: SwRS
id: SwRS-CORE-001
uuid: 00000000-0000-4000-8000-000000000002
title: Write CSV output
description: When export is requested, the service SHALL write the report as CSV
  output.
project: OKFREQXMP
scope: Core
lifecycle: draft
origin: native
tier: SwRS
derives_from:
- StRS-CORE-001
annotation_exemption: false
exemption_reason:
derived_by: []
implemented_in_files:
- src/export.py
tested_in_files:
- tests/test_export.py
---

## EARS Expression
```

### F2 — indented sequences, comments, folded and quoted scalars, flow sequence

```yaml
---
# leading comment
title: Alpha  # trailing comment
tags:
  - one
  - two
summary: >-
  Folded text that
  spans lines.
links: [a.md, b.md]
quoted: "keep: me"

status: draft
---
Body
```

### F3 — F1 with CRLF line endings everywhere

### F4 — F2 closed with `...` instead of the second `---`

Value edits (contract for T05). Each row requires: `removed` equals the field's old lines, `added`
equals exactly the expected lines, and nothing else differs.

| Fixture | Field ← value | Expected added lines |
| --- | --- | --- |
| F1 | `title` ← `Write CSV output v2` | `title: Write CSV output v2` |
| F1 | `lifecycle` ← `approved` | `lifecycle: approved` |
| F1 | `annotation_exemption` ← `true` | `annotation_exemption: true` |
| F1 | `exemption_reason` ← `n/a` | `exemption_reason: n/a` |
| F1 | `derives_from` ← `["StRS-CORE-001","StRS-CORE-002"]` | `derives_from:`, `- StRS-CORE-001`, `- StRS-CORE-002` |
| F1 | `derived_by` ← `["X-1"]` | `derived_by: [X-1]` |
| F2 | `title` ← `Beta` | `title: Beta  # trailing comment` |
| F2 | `tags` ← `["one","two","three"]` | `tags:`, `  - one`, `  - two`, `  - three` |
| F2 | `links` ← `["a.md","c.md"]` | `links: [a.md, c.md]` |
| F2 | `quoted` ← `still: quoted` | `quoted: "still: quoted"` |
| F2 | `summary` ← `New summary` | `summary: >-`, `  New summary` |
| F2 | `status` ← `active` | `status: active` (the blank line before it is kept) |
| F3 | `title` ← `Write CSV output v2` | `title: Write CSV output v2\r` |
| F4 | `status` ← `active` | `status: active` and the `...` line unchanged |

For the multi-line rows, `removed` is the exact old block. For example, F1 `derives_from` removes
`derives_from:` and `- StRS-CORE-001`. If the minimal patch keeps a common line such as
`derives_from:` untouched, `lineDelta` trims it. In that case, assert on the **resulting full
text** instead: build the expected document by hand and compare with `assert.equal(output, expected)`.
That variant is the more robust one; use it for every row.

Structural edits (contract for T06):

| Fixture | Operation | Expected |
| --- | --- | --- |
| F2 | rename `title` → `heading` | only `title:` → `heading:` on that line, comment kept |
| F2 | remove `links` | exactly the line `links: [a.md, b.md]` disappears |
| F2 | remove `tags` | exactly `tags:`, `  - one`, `  - two` disappear |
| F1 | add `owner` = `Ana` | exactly one line `owner: Ana` added before the closing `---` |
| F2 | comments | in every F2 case, `# leading comment` and `# trailing comment` survive unless their own line is removed |

Mark failing value-edit tests `{ todo: "UX-16 (T05)" }` and failing structural tests
`{ todo: "UX-16 (T06)" }`. Again, run first and mark only what fails.

## Steps

1. Write `lineDelta` and its tests.
2. Write both corpus files.
3. Run `PLAN/scripts/gate.sh T01-impl unit`. Then list the todo-marked tests in the report: name
   and the first line of the failure message, obtained by temporarily running without the marker.

## Expected changes to existing tests

None.

## Must not change

- Any file under `src/`.
- Existing test files.

## Done when

- The `unit` gate passes.
- The report lists every `todo` test with its failure reason, so T04–T06 know their targets.
- At least the compact, padded, no-outer-pipes and CRLF table edits, and the F1 `title`, F1
  `derives_from` and F2 `title` frontmatter edits, are present and fail without the marker. If any
  of these passes today, report it; the corpus would then be wrong.
