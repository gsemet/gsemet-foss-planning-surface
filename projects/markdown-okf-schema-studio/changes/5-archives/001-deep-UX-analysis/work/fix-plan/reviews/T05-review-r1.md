# T05 review — round 1

Base: 98f624722ef8616d02c4a045a7c32dd4ddc435a9 · Reviewed diff: 4 files, +334/-23

## Gates
- compile: PASS (`logs/T05-compile.log`). I also recompiled and re-ran
  `frontmatterPreservation.test.js` and `okfFrontmatter.test.js` locally: 58 tests, 54 pass, 0 fail, 4 todo (T06).
- unit: PASS (`logs/T05-unit.log`): 386 tests, 382 pass, 0 fail, 4 todo. T04 had 362 pass + 18 todo
  (380 tests). The difference is the 14 T05 markers removed plus 6 new tests. No `UX-16 (T05)` marker remains.
- types: PASS (`logs/T05-types.log`).
- trusted: PASS, exit 0 (`logs/T05-trusted.log`), including `PASS real-input screenshot: 08-frontmatter-value-minimal-patch`.
- No new failures compared with the T00 baseline. The task does not require contracts, full or visual.

## Done-when
- [x] `unit` and `trusted` gates pass. Evidence: logs above.
- [x] The T01 value-edit tests pass without markers. Evidence: the 14 `value edit … changes only the named field` tests pass.
- [x] RI-T05 passes and shows a one-line diff. Evidence: `scenarioFrontmatterValueMinimalPatch` asserts
  `lineDelta` = `status: draft` → `status: active`. I opened the screenshot
  `.artifacts/real-input-V0yEEt/08-frontmatter-value-minimal-patch.png`: the buffer and the properties table both show
  `active`, and the compact sequences and two-line summary are unchanged. The amended type-ahead step is accepted.
  - **Pre-fix failure:** the report does not record a pre-fix run. I established the failure by reproduction instead.
    I bundled the base `okfFrontmatter.ts` (98f6247) into scratch space and called
    `createFrontmatterFieldPatch(REQ_DOCUMENT, "status", "active")`, the same call `handleFrontmatterSave` makes. The base
    patch covers offsets 4–182 and rewrites 6 lines: `- alpha`/`- beta`/`- StRS-CORE-001` are re-indented to
    `  - …`, and `summary` is flattened to one line. The scenario's
    `waitFor(bufferText(document) === expected)` therefore cannot succeed before the fix. The patched build covers
    offsets 38–51 and changes only `status`. I consider this sufficient.
- [ ] "The reviewer can find no input that makes the minimal path write data different from `expected`." **Data: met.**
  I found no input where the minimal path writes wrong data (about 100 probes, below). **But the goal "every other
  byte stays identical: comments…" and P-E7 "YAML comments preserved" are not met.** The minimal path duplicates or
  deletes comments that the base whole-document patch kept (findings 1–3). `toJS` verification cannot catch this, because
  comments do not change the data.

### Specific points from the orchestrator
1. **Fallback and add path.** Each of these takes the whole-document patch, and its output is byte-identical to the
   base patch:
   - a top-level anchor (`a: &x 1`) or alias (`b: *x`);
   - a non-column-0 key (`{title: Alpha, b: 2}`, `? title`);
   - a candidate that does not verify (`exemption_reason:  # why`, `!!str` value set to a number).

   Two more cases fail safely:
   - Nested anchors or aliases inside the edited value either verify, or fail verification and fall back.
     An anchor used elsewhere whose item is removed returns `undefined`, as on base.
   - A nested map is patched minimally, with correct `toJS`.

   Parse errors still return `undefined` before any patching, as on base. The add path
   (`extraction.document.set`) and the rename and remove functions are untouched. The `if (pair)` restructuring is
   equivalent to the old two-branch code. `minimalPairPatch` restores every field it clears (`finally`), so the fallback
   stringifies the same document as base.
2. **Verification.** The region is the edited key line through the end of the line that holds `valueEnd`. All text
   outside it is byte-identical by construction. `isDeepStrictEqual(parseDocument(candidate).toJS({maxAliasCount:100}),
   expected)` compares the whole map. Both sides are parsed with the same default schema, as `extractFrontmatter` does.
   I confirmed that the check distinguishes:
   - `1` from `"1"`, and `true` from `"true"`;
   - `null` from `""`;
   - a `!!str` tag change.

   For example, `count: 1` → `"123"` writes `count: "123"`. `!!str 123` → `456` fails verification and falls back. Quote
   style of other fields cannot change, because they are outside the region. Key order is irrelevant to the data.
3. **CRLF and empty value.** Each of these is correct, with CRLF kept and no `\r\n` split:
   - CRLF: scalar with an inline comment, multi-line plain scalar, `>-` scalar as the last field, block sequence as
     the last field, comment between sequence items, `null` → list, new multi-line values;
   - empty value: `exemption_reason:` in the middle, as the last line, and on CRLF.

   `exemption_reason:  # why` falls back safely (see finding 5).
4. **Step 2b.** Present. The four F2 outputs (tags, links, quoted, summary) are appended to
   "structural F2 edits keep both comments unless their own line is removed".

## Protected features checked
- P-E7 (frontmatter editing, comments preserved): **regressed** (findings 1–3). The other P-E7 parts are unchanged:
  `handleFrontmatterSave` validation, type-aware controls, add, remove, rename, and the error state.
  The covering tests are `okfFrontmatter.test.ts`, `frontmatterPreservation.test.ts` and the trusted suite.
- P-R7 / UX-24 (properties table value display): `propertiesTable.ts` is not touched. The display derives from data,
  which is verified.
- P-E6 (stale version and request checks): `handleFrontmatterSave` is unchanged and still applies one patch through the
  version-checked path.
- P-S2 and P-S4: no message protocol or webview change.
- P-E8 (read-only mode): no change to the edit entry points.
- UX-22 and UX-34 (frozen): not touched.

## Findings

1. **[BLOCKER] `src/frontmatter/okfFrontmatter.ts`: `minimalPairPatch` duplicates the trailing comment of a block
   sequence or map value on every edit, including a no-op edit.**

   **Cause.** In a block collection, `value.range[1]` stops before trailing comment lines at the collection's
   indentation, but the parser stores those lines in `value.comment`. The region ends at `range[1]`, so the comment
   line stays in the source. The renderer then emits `pair.value.comment` a second time.

   **Reproduction.** Commented-out list items are a common pattern.

   - Source: `"---\nderives_from:\n  - StRS-CORE-001\n  # - StRS-CORE-002\nstatus: draft\n---\n"`.
   - Call: `createFrontmatterFieldPatch(source, "derives_from", ["StRS-CORE-001", "StRS-CORE-003"])`.
   - Result: `  # - StRS-CORE-002` appears twice. With the unchanged value `["StRS-CORE-001"]`, it is also duplicated.
     Each further edit adds another copy.
   - Base keeps one copy.

   **Other inputs with the same defect:**
   - a nested map value (`meta:\n  owner: old\n  # trailing in meta\nother: keep`);
   - a sequence of maps;
   - a block list replaced by `[]`;
   - an indented comment after a blank line;
   - the last field of the frontmatter.

   **Fix.** Combined with findings 2 and 3; the same change fixes all three. I validated it in a scratch copy: all 58
   frontmatter unit tests still pass, and every probe keeps each comment exactly once with correct data.

   1. Right after `valueRange`/`valueEnd`/`regionEnd` are computed, add:
      ```ts
      const originalIsBlockScalar = isScalar(originalValue)
        && (originalValue.type === "BLOCK_FOLDED" || originalValue.type === "BLOCK_LITERAL");
      ```
   2. Replace the `suffix` computation with:
      ```ts
      const suffix = !originalIsBlockScalar && valueEnd <= regionEnd ? text.slice(valueEnd, regionEnd) : "";
      ```
   3. Next to `newScalar`, add:
      ```ts
      const commentNode = newValue && (isScalar(newValue) || isSeq(newValue) || isMap(newValue)) && !originalIsBlockScalar
        ? newValue : undefined;
      ```
   4. Save `commentNode?.comment` instead of `newScalar?.comment`. Clear it with
      `if (commentNode) commentNode.comment = undefined;` before rendering. Restore it in `finally` with
      `if (commentNode) commentNode.comment = savedValueComment;`.
   5. Keep restoring `newScalar.type` separately.

   **Why this works.** When the original value is not a block scalar, its own comment is in one of two places:
   - on the region's last line after `valueEnd`, where the suffix keeps it byte for byte (scalars and flow collections);
   - on lines after the region (block collections), where the source keeps it.

   So the renderer must not emit it. When the original value is a block scalar, the comment is in the `>-`/`|` header
   inside the region, and only the renderer can emit it.

   **Tests.** Add to `test/frontmatter/okfFrontmatter.test.ts`; assert the whole output string:
   - `"appending to a sequence keeps a trailing commented-out item once"`.
     - Source: as in the reproduction above.
     - With `["StRS-CORE-001", "StRS-CORE-003"]`, expect
       `"---\nderives_from:\n  - StRS-CORE-001\n  - StRS-CORE-003\n  # - StRS-CORE-002\nstatus: draft\n---\n"`.
     - With `["StRS-CORE-001"]`, expect output `=== source`.
   - `"editing a nested map keeps its trailing comment once"`.
     - Source: `"---\nmeta:\n  owner: old\n  # trailing in meta\nother: keep\n---\n"`.
     - Value: `{ owner: "new" }`.
     - Expect `"---\nmeta:\n  owner: new\n  # trailing in meta\nother: keep\n---\n"`.

2. **[BLOCKER] `minimalPairPatch` deletes the header comment of a block scalar.**

   **Cause.** Step 4 clears `pair.value.comment` for every Scalar. For a block scalar, `range[1]` is on the next line,
   so `valueEnd > regionEnd` and the suffix is empty. The comment text is in neither the render nor the suffix.

   **Reproduction.**
   - Source: `"---\nsummary: >- # header\n  Folded text\n  spans.\nstatus: draft\n---\n"`.
   - Edit `summary` to `"New"`.
   - Current: `summary: >-\n  New`, with `# header` lost.
   - Base: `summary: New # header`.
   - Setting the value to `null` also loses it.

   **Fix.** The fix in finding 1 (`originalIsBlockScalar` keeps the node comment, so the renderer emits it in the
   header).

   **Test.** Add `"editing a block scalar keeps its header comment"`.
   - Source: as above.
   - Value: `"New"`.
   - Expect `"---\nsummary: >- # header\n  New\nstatus: draft\n---\n"`.

3. **[MAJOR] `minimalPairPatch` writes the inline comment twice when a scalar becomes a collection.**

   **Cause.** `preserveYamlNodeMetadata` copies the scalar's comment onto the new seq/map. That comment is not cleared,
   because only Scalars are cleared, and the suffix `  # c` is appended as well.

   **Reproduction.**
   - Source: `"---\ntags: one  # c\nstatus: draft\n---\n"`.
   - Value: `["one", "two"]`.
   - Result: the line `  # c  # c`. Base writes `  # c` once.

   **Fix.** The fix in finding 1. Output becomes `tags:\n  - one\n  - two  # c`.

   **Test.** Add `"replacing a commented scalar by a list keeps the comment once"`.
   - Source: as above.
   - Assert that `(updated.match(/# c/gu) ?? []).length === 1`.
   - Assert that `extractFrontmatter(updated).frontmatter` deep-equals `{ tags: ["one", "two"], status: "draft" }`.

4. **[MAJOR] `minimalPairPatch` also copies the `PLAIN` type, and the design does not ask for it.** Design step 4 lists
   only `QUOTE_DOUBLE`, `QUOTE_SINGLE`, `BLOCK_FOLDED` and `BLOCK_LITERAL`.

   **Effect.** Multi-line text on a plain field (reachable through the text area, see D-06) is written as a folded
   plain scalar with blank lines, instead of base's `|-` block.

   **Reproduction.**
   - Source: `"---\ndescription: When export is requested\n  output.\nb: 2\n---\n"`.
   - Value: `"a\nb"`.
   - Current: `description: a\n\n  b`.
   - Base and spec: `description: |-\n  a\n  b`.

   For single-line values, copying `PLAIN` changes nothing, because the default is already plain when possible.

   **Fix.** Change the condition to
   `if (isScalar(originalValue) && newScalar && typeof newScalar.value === "string" && originalValue.type !== "PLAIN")`.

   **Test.** Add `"a multi-line value on a plain field is written as a literal block"`.
   - Source: as above.
   - Expect `"---\ndescription: |-\n  a\n  b\nb: 2\n---\n"`.

5. **[MINOR] (follow-up, safe today) Empty value with an inline comment falls back to the whole-document patch.**
   - Input: `exemption_reason:  # why`.
   - Cause: the empty node's `range` is at `#`, so the suffix is `# why` and the candidate `n/a# why` fails
     verification.
   - Effect: the whole frontmatter is re-serialized, as on base.
   - Possible fix: when `isScalar(originalValue) && originalValue.value === null && valueRange[0] === valueRange[1]`, use
     `valueEnd = keyRange[1] + 1`.
   - Not required for this round.

6. **[NIT] `test/integration/realInput.test.ts`.** `currentPreviewFrame` is imported but unused. Remove it from the
   import list.

7. **[NIT] `test/frontmatter/okfFrontmatter.test.ts`.** There are two blank lines before `applyFieldPatch`; one is
   enough.

Note for the orchestrator: findings 1–3 come from design steps 4–5 as written, which clear and suffix comments only for
Scalars. The implementer followed the design. The fix above amends those two steps. Consider noting this in the task
file, as was done for the RI-T05 key step.

## Existing assertions changed
- `frontmatterPreservation.test.ts`: OK. The 14 `todo: "UX-16 (T05)"` entries, the `todo?` field and the `{ todo }`
  option are removed, as the task requires. The T06 markers are kept.
- `frontmatterPreservation.test.ts`, F2 comment test: OK. 4 outputs were added (step 2b); nothing was removed.
- `okfFrontmatter.test.ts`: OK. Tests were only added; no existing expectation changed.
- `realInput.test.ts`: OK. `withDocument` gains an optional `schemaYaml` parameter, and existing callers are unchanged.
  RI-T05 is added.

VERDICT: CHANGES REQUESTED
