# T05 — Editing one frontmatter value changes only that field's lines

| Field | Value |
| --- | --- |
| Fixes | [UX-16](../../03-frontmatter-editing/UX-16-field-edit-reserializes-frontmatter.md) (value edits) |
| Depends on | T01 |
| Gate | `unit trusted` |
| Risk | Medium (P-E7 frontmatter editing, comment preservation) |
| Commit message | `fix(vscode): patch only the edited frontmatter field` |

## Goal

`createFrontmatterFieldPatch(source, name, value)` for an **existing** field returns a patch that
covers only that field's lines. Every other byte of the frontmatter stays identical: comments,
folded scalars, sequence indentation, blank lines, quoting, and CRLF.

When the minimal patch cannot be built or does not verify, fall back to today's whole-document
patch. Never write wrong data.

All T01 `todo: "UX-16 (T05)"` tests pass and lose their marker.

## Context to read first

- `src/frontmatter/okfFrontmatter.ts`: `extractFrontmatter` (parses with `keepSourceTokens: true`),
  `createFrontmatterFieldPatch`, `updateYamlSequence`, `preserveYamlNodeMetadata`,
  `createFrontmatterDocumentPatch`.
- The caller `handleFrontmatterSave` in `src/extension.ts`. It applies `{start, end, text}` as one
  `WorkspaceEdit` and validates the candidate. It does not need to change.
- `test/frontmatter/frontmatterPreservation.test.ts` (T01).

Verified facts about the installed `yaml` 2.9.1 (from a probe), for `parseDocument(text, { keepSourceTokens: true })`:

| Source line | `pair.key.range` | `pair.value` | `pair.value.range` | notes |
| --- | --- | --- | --- | --- |
| `title: Alpha  # c` (offset 0) | `[0,5,5]` | Scalar PLAIN | `[7,12,18]` | `value.comment === " c"`; value text ends at `range[1]` = 12 |
| `exemption_reason:` (offset 18) | `[18,34,34]` | Scalar PLAIN, value null | `[35,35,35]` | empty value: `range[0] === range[1]` |
| `derived_by: []` | … | YAMLSeq (flow) | `[48,50,51]` | |
| `links: [a.md, b.md]` | … | YAMLSeq (flow) | `[58,70,71]` | |
| `list:` / `- a` / `- b` | … | YAMLSeq (block) | `[77,85,85]` | ends after the last item |
| `q: "x: y"` | … | Scalar QUOTE_DOUBLE | `[88,94,95]` | |

To render a single pair, put it in a fresh map:

```ts
const map = new YAMLMap(); map.items.push(pair);
const single = new Document(); single.contents = map;
single.toString(options);
```

Results: `links: [a.md, b.md]\n` with `{ lineWidth: 0, flowCollectionPadding: false }`;
`list:\n- a\n- b\n` with `{ lineWidth: 0, indentSeq: false }`; `title: Alpha # c\n` (the yaml
library normalizes the comment spacing to one space; see step 4).

## Allowed files

- `src/frontmatter/okfFrontmatter.ts`
- `test/frontmatter/frontmatterPreservation.test.ts` (remove T05 markers; add tests)
- `test/frontmatter/okfFrontmatter.test.ts` (add tests only)
- `test/integration/realInput.test.ts` (add RI-T05)

## Design (follow it exactly)

Add an internal function, used by `createFrontmatterFieldPatch` **only when the pair already
exists**:

```ts
function minimalPairPatch(source: string, extraction: FrontmatterExtraction, pair: Pair, expected: Record<string, unknown>): FrontmatterFieldPatch | undefined
```

1. **Offsets.** `yamlStart` = the offset of the YAML text in `source`: the length of the opening
   fence match (`---\n` or `---\r\n`), as in `createFrontmatterDocumentPatch`. The node ranges are
   relative to `extraction.text`.
2. **Region.**
   - `keyStart = pair.key.range[0]`; the region starts at the beginning of that line (search
     backwards for `\n`).
   - `valueEnd`: `pair.value.range[1]` when the value exists, otherwise `pair.key.range[1] + 1`
     (just after the colon).
   - The region ends at the end of the line containing `valueEnd - 1`, **excluding** the line
     break, and excluding a `\r` before `\n`. Exactly:

     ```ts
     let regionEnd = text.indexOf("\n", valueEnd - 1);
     if (regionEnd < 0) regionEnd = text.length;
     if (regionEnd > 0 && text[regionEnd - 1] === "\r") regionEnd -= 1;
     ```

     Block values often end **after** their last line break (`range[1]` points to the next line). The
     formula handles this: the region ends at that line break.
   - Bail out (return `undefined`) if:
     - the key line does not start at column 0 (the pair is not top-level), or
     - the key or value carries an anchor (`&`) or alias (`*`).
3. **Style options.** Detect them from the original text:
   - `indentSeq`: when the original value is a **block** sequence, `true` if its first item line is
     indented more than the key line, else `false`. Otherwise use the first block sequence found in
     the frontmatter. With no block sequence anywhere, use `true` (the library default).
   - `flowCollectionPadding`: `true` only if the original value is a flow collection whose source
     text starts with `[ ` or `{ `. Otherwise `false`.
   - `lineWidth: 0`.
4. **Render.** The pair object has already been modified by the existing code
   (`updateYamlSequence`, or `preserveYamlNodeMetadata` + `createNode`). Before rendering:
   - when the original and the new value are both Scalars and the new value is a string, copy the
     original scalar `type` (`QUOTE_DOUBLE`, `QUOTE_SINGLE`, `BLOCK_FOLDED`, `BLOCK_LITERAL`) onto
     the new node;
   - save, then clear, `pair.key.commentBefore`, `pair.key.spaceBefore` and `pair.spaceBefore`:
     those lines lie outside the region and must not be emitted twice;
   - if the value is a Scalar, save, then clear, `pair.value.comment`. The original inline comment
     text is kept from the source in step 5.

   Render the single-pair document, then **restore** every saved field. Strip the final line
   break, then convert the line breaks to the document's line ending (`\r\n` when the opening fence
   is `---\r\n`).
5. **Suffix.** When the **original** value was a Scalar (including an empty value) and
   `valueEnd <= regionEnd`, keep `text.slice(valueEnd, regionEnd)`, for example
   `  # trailing comment`, and append it after the rendered text. Otherwise use no suffix: block
   scalars and collections carry their own comments in the nodes.
6. **Verify.** Build the candidate frontmatter text: the original YAML text with the region
   replaced. `parseDocument(candidate)` must have no errors, and `toJS({ maxAliasCount: 100 })` must
   deep-equal `expected`.
   - `expected` is the original `extraction.frontmatter` with the field replaced by `value`, as a
     deep copy built **before** the document was modified.
   - Use `node:util` `isDeepStrictEqual`.
   - If verification fails, return `undefined`.
7. **Patch.** Return `{ start: yamlStart + regionStart, end: yamlStart + regionEnd, text: rendered + suffix }`.

In `createFrontmatterFieldPatch`, compute `expected` first. When `pair` exists, try
`minimalPairPatch`; if it returns `undefined`, use the existing whole-document path unchanged. The
add path (pair missing) stays unchanged in this task (T06).

## Tests

Write first, and show the failures:

1. Remove every `todo: "UX-16 (T05)"` marker in `frontmatterPreservation.test.ts`. All value-edit
   cases pass.
2. Add, in `okfFrontmatter.test.ts`:
   - an anchored value (`a: &x 1`) → the patch still produces correct data, through the fallback;
   - a nested map value edited as an object → correct data; minimal or fallback both accepted,
     assert on `toJS`;
   - a comment line between two sequence items (`tags:\n  - one\n  # note\n  - two`) is still present
     after appending an item;
   - the patch for an unchanged value produces the same text (no-op);
   - the `exemption_reason:` empty-value case on CRLF.
2b. **Added after the T01 review (MINOR finding).** In `frontmatterPreservation.test.ts`, test
   "structural F2 edits keep both comments unless their own line is removed": append these four
   outputs to its `outputs` array, so the comment check covers every F2 value edit:
   - `applyPatch(F2, createFrontmatterFieldPatch(F2, "tags", ["one", "two", "three"])!)`;
   - `applyPatch(F2, createFrontmatterFieldPatch(F2, "links", ["a.md", "c.md"])!)`;
   - `applyPatch(F2, createFrontmatterFieldPatch(F2, "quoted", "still: quoted")!)`;
   - `applyPatch(F2, createFrontmatterFieldPatch(F2, "summary", "New summary")!)`.

   They pass on the old whole-document patch too; they must still pass after the change.
3. Real-input E2E, scenario **RI-T05** in `realInput.test.ts`:
   - Fixture: a `_schema` bundle (use `writeSchema`) with type `req`. The schema properties are:
     - `title` (string), `status` (enum `draft`/`active`), `tags` (array of strings);
     - `summary` (string), `derives_from` (array of strings).
   - The document's frontmatter uses F1 style (compact sequences and a two-line plain `summary`).
   - In edit mode, click the `status` value, choose `active` with the keyboard (`select` focused:
     press `ArrowDown` until `active`, then `Enter`), then wait for the buffer.
     **Amended after round 1 (orchestrator, test mechanics only):** in the VS Code test host on
     macOS, `ArrowDown` on a focused `select` does not change its value (it targets the native
     popup). Use type-ahead instead: press `a` (selects `active`), then `Enter`.
   - Assert that `lineDelta` shows exactly the `status:` line changed.

   This test must fail before the fix. Record the failure.

## Expected changes to existing tests

- `okfFrontmatter.test.ts` tests whose expected patch text is the **whole re-serialized
  frontmatter** must be updated to the minimal output. List each one in the report with old and new
  expected text. Comment-preservation assertions must remain, unchanged or strengthened.
- `previewEditing.test.ts`: any expectation of the whole frontmatter after a field edit may change
  the same way. List them.

## Must not change

- The add path (`pair` missing), rename and remove (T06).
- Validation in `handleFrontmatterSave`, schema handling, and `parseYamlValue`.
- The YAML display in the properties table (UX-24 frozen).

## Done when

- The `unit` and `trusted` gates pass.
- T01 value-edit tests pass without markers. RI-T05 passes and shows a one-line diff.
- The reviewer can find no input that makes the minimal path write data different from `expected`.
  Verification guards this; the tests exercise the fallback at least once.
