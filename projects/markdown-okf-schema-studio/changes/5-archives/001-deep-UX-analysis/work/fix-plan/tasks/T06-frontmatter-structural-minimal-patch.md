# T06 — Minimal patches for adding, renaming and removing frontmatter fields

| Field | Value |
| --- | --- |
| Fixes | [UX-16](../../03-frontmatter-editing/UX-16-field-edit-reserializes-frontmatter.md) (structural edits); prepares D-08 (insert after a row) |
| Depends on | T05 |
| Gate | `unit trusted` |
| Risk | Medium (P-E7) |
| Commit message | `fix(vscode): add, rename and remove frontmatter fields without reformatting` |

## Goal

Rename, remove and add touch only the lines of the field concerned. All T01
`todo: "UX-16 (T06)"` tests pass, and their markers are removed.

Add accepts an optional position (`afterField`). T24 uses it from the UI; this task only adds the
function option and its tests.

## Context to read first

- T05's `minimalPairPatch` and its region and style helpers. Reuse them; do not duplicate them.
- `createFrontmatterFieldRenamePatch`, `createFrontmatterFieldRemovePatch`, and the add path of
  `createFrontmatterFieldPatch` (`extraction.document.set(name, value)`).
- `extractFrontmatter`'s regex. The YAML text excludes the line break that precedes the closing
  `---`/`...`, so the last field line has no trailing line break inside `text`.

## Allowed files

- `src/frontmatter/okfFrontmatter.ts`
- `test/frontmatter/frontmatterPreservation.test.ts` (remove T06 markers; add tests)
- `test/frontmatter/okfFrontmatter.test.ts` (add tests only)
- `test/integration/realInput.test.ts` (add RI-T06)

## Design

Refactor T05's code just enough to share these helpers. Keep T05 behaviour identical; its tests
must still pass:

- `fieldRegion(text, pair) → { start, end }` (T05 step 2);
- `yamlStyle(text, document, pair?) → { indentSeq, flowCollectionPadding, lineWidth: 0 }` (T05 step 3);
- `renderPair(pair, style, lineEnding)` (T05 step 4, including the save, clear and restore of the
  comment fields);
- `verified(candidateText, expected) → boolean` (T05 step 6).

1. **Rename** (`createFrontmatterFieldRenamePatch`). Keep all existing guards (duplicate key, empty
   name, unchanged name, line breaks). Replace only the key text,
   `[pair.key.range[0], pair.key.range[1])`. The new key text is
   `stringify(newName, { lineWidth: 0 }).trimEnd()`, from `yaml`; it quotes when needed.
   - Verify: same keys in the same order with `currentName` replaced by `newName`, and the same
     values.
   - Fallback: today's whole-document path.
2. **Remove** (`createFrontmatterFieldRemovePatch`). Delete the field's whole lines: from the start
   of the key line to `fieldRegion.end`, **plus** the following line break. When the field is the
   last line of `text` (no following line break), remove the **preceding** line break instead.
   - Keep comment lines above the key; never delete user comments.
   - Verify: the expected object without the key.
   - Fallback: today's path.
3. **Add** (`createFrontmatterFieldPatch` when the pair is missing). New signature:

   ```ts
   createFrontmatterFieldPatch(source, name, value, options?: { afterField?: string })
   ```

   - Render the new pair with `yamlStyle` detected from the document; use a fresh `Pair` built by
     `document.createPair(name, value)`.
   - **Insertion point:**
     - when `options.afterField` names an existing top-level field, insert at that field's
       `fieldRegion.end`, with `lineEnding + rendered`;
     - otherwise at the end of `text`, with `lineEnding + rendered`;
     - when `text` is empty, at offset 0, with `rendered + lineEnding`.
   - Verify: the expected object has the new key, **and** the key order is right
     (`Object.keys(toJS())` has `name` right after `afterField`, or last).
   - Fallback: today's path (`document.set`), which appends at the end. In the fallback,
     `afterField` is ignored and the fallback is reported by returning
     `{ …patch, positioned: false }`.

     For that, extend `FrontmatterFieldPatch` with the optional `positioned?: boolean`, `true` when
     `afterField` was honoured. Callers that ignore the field keep working.

## Tests

Write first, and show the failures:

1. Remove every `todo: "UX-16 (T06)"` marker. All structural cases pass.
2. Add, in `frontmatterPreservation.test.ts`:
   - add `owner: Ana` with `afterField: "title"` on F2 → one line inserted directly after
     `title: Alpha  # trailing comment`;
   - add after the **last** field → the same result as without `afterField`;
   - add to an empty frontmatter (`---\n---\nBody`) → `---\nowner: Ana\n---\nBody`;
   - add a list value on F1 (compact style) → `owner:\n- a\n- b` (compact);
   - remove the last field of F2 (`status`) → the blank line before it stays, the closing fence
     stays, and there is no double line break artefact. Assert the full expected text;
   - rename to a key that needs quoting (`a: b`) → `"a: b": …` on that line only;
   - CRLF variants of add and remove.
3. Real-input E2E, scenario **RI-T06** (same bundle fixture style as RI-T05):
   - **Rename:** click the `summary` name cell, select all (`${MOD}+A`), type `abstract`, press
     `Enter`. Assert a one-line change from `summary:` to `abstract:` and identical continuation
     lines. If the schema forbids the key, use a schema-free document for this step.
   - **Remove:** click the `tags` value, click the "Remove frontmatter field" button with the
     mouse. Assert that exactly the `tags` lines are removed.

   Both must fail before the fix. Record the failures.

## Expected changes to existing tests

- `okfFrontmatter.test.ts` rename, remove and add tests whose expected text is the whole
  re-serialized frontmatter. List each one, old versus new.
- `previewEditing.test.ts` add, remove and rename expectations, likewise.

## Must not change

- The guards: duplicate names, required-field removal check in `handleFrontmatterSave`, key
  validation.
- Schema validation flow and error messages.
- T05 value-edit behaviour.

## Done when

- The `unit` and `trusted` gates pass.
- No T01 todo marker remains in `frontmatterPreservation.test.ts`.
- RI-T06 shows one-line or field-only diffs.
