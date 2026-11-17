# T05 review — round 2

Base: 98f624722ef8616d02c4a045a7c32dd4ddc435a9 · Reviewed diff: 4 files, +395/-23

## Gates
- compile: PASS. I recompiled locally.
- unit: PASS (`logs/T05-r2-unit.log` and `logs/T05-impl-r2-unit.log`): 392 tests, 388 pass, 0 fail, 4 todo
  (T06 markers only). My local run of `okfFrontmatter.test.js` and `frontmatterPreservation.test.js`
  gave 64 tests: 60 pass, 0 fail, 4 todo.
- types: PASS (`logs/T05-r2-types.log`).
- trusted: PASS in the implementer's run on this tree (`logs/T05-impl-r2-trusted.log`, exit 0). That
  run includes `08-frontmatter-value-minimal-patch`. The orchestrator's three reruns
  (`T05-r2*-trusted.log`) fail only at the checkbox suite step "Timed out waiting for one undo to
  restore the original source", because the screen was locked. As instructed, I did not run trusted.
  It must be rerun after the fix below in any case.
- Compared with the T00 baseline: no new unit or type failures.

## Round-1 findings: verification
Each fix matches the round-1 instructions. I checked that each test guards its fix by mutating a
scratch copy of the compiled `out/` code and re-running the two frontmatter test files:

| R1 finding | Fix in `minimalPairPatch` | Guarding test(s) | Mutation result |
| --- | --- | --- | --- |
| 1 BLOCKER: trailing comment of a block seq or map duplicated | `originalIsBlockScalar`; `commentNode` covers Scalar/Seq/Map; suffix formula | "appending to a sequence keeps a trailing commented-out item once", "editing a nested map keeps its trailing comment once" | Limiting `commentNode` to Scalars makes both fail, and the finding-3 test too |
| 2 BLOCKER: block-scalar header comment lost | `commentNode` is undefined when the original is a block scalar | "editing a block scalar keeps its header comment" | Removing `&& !originalIsBlockScalar` from `commentNode` makes exactly this test fail |
| 3 MAJOR: comment doubled when a scalar becomes a list | same `commentNode` change | "replacing a commented scalar by a list keeps the comment once" | Fails under the finding-1 mutation |
| 4 MAJOR: `PLAIN` type copied | `&& originalValue.type !== "PLAIN"` | "a multi-line value on a plain field is written as a literal block" | Removing the condition makes exactly this test fail |
| 6 NIT: unused import | `currentPreviewFrame` removed | — | Verified with grep |
| 7 NIT: two blank lines | Reduced to one before `applyFieldPatch` | — | Verified |

The pre-fix evidence in `logs/T05-impl-r2-prefix-unit.log` (lines 98–103) shows the 5 new tests
failing and the guard test passing, as the report states. Round-1 MINOR 5 is unchanged, as allowed. It
still falls back safely and gives output identical to base.

The `!originalIsBlockScalar` gate in `suffix` is redundant: no test fails without it. For block scalars
the suffix is already empty (`valueEnd > regionEnd`, or an empty slice at the end of the text). It is
harmless.

## Sibling hunt (comment handling in `minimalPairPatch`)
I ran about 180 hand-written probes, each in LF and CRLF. They compare the minimal path with the base
whole-document patch (base bundled from 98f6247) and cover:
- comments before, after and inside the field: key line, header, first item, between items, after the
  last item at column 0, at item indentation and deeper, after a blank line, and inside nested maps
  and sequences of maps;
- block scalars with `|+`, `|-`, `|2`, `>2+ # h`, followed by comment lines, as the last field, and
  turned into a list, a number or `null`;
- flow sequences and maps: padded, multi-line, with inline comments, as the last field, turned into
  `[]` or `null`;
- empty values: `x:`, `x: ~`, `x: ""`, an empty value followed by a comment line, and an empty value
  as the last field;
- quoted, tagged and anchored values, quoted keys, the `...` end marker, trailing blank lines, tabs
  before comments, and non-BMP characters;
- the only field, and the last field before `---`.

I also ran a seeded fuzz of about 7,400 random value edits (append an item, change a scalar or map
value, no-op, `null`), with random comment groups, in LF and CRLF.

Results:
- **Data:** no input made the minimal path write data different from `expected`. Anchors, aliases,
  `!!str` changes, `x:  # why` and literal-content collisions all fall back or verify correctly.
- **LF:** no comment is lost, duplicated or moved compared with base. The only comment losses are
  comments attached to an item the edit removes, and base loses them identically.
- **CRLF:** one defect, finding 1. It affects 329 of 3,706 and 333 of 3,710 fuzz edits; base has none
  of them.

## Done-when
- [ ] `unit` and `trusted` gates pass. Unit and types pass. Trusted passed in the implementer's run and
  must be rerun after unlock and after the fix for finding 1.
- [x] T01 value-edit tests pass without markers: the 14 `value edit … changes only the named field`
  tests pass, and no `UX-16 (T05)` marker remains.
- [x] RI-T05 shows a one-line diff. `scenarioFrontmatterValueMinimalPatch` asserts `lineDelta`
  `status: draft` → `status: active`. Round 1 verified the pre-fix failure by reproduction.
- [ ] Reviewer finds no bad input. **Data: met. CRLF and comment formatting: not met** (finding 1).
  The task goal requires that CRLF stays identical and that comments are preserved.

## Protected features checked
- P-E7 (frontmatter editing, YAML comments preserved): LF is fully covered by the six new tests, the
  round-1 tests and the T01 corpus. **CRLF regresses** (finding 1). Add, remove, rename and
  `handleFrontmatterSave` validation are untouched.
- P-R7 / UX-24 (properties table value display): `propertiesTable.ts` is untouched, and the data is
  verified.
- P-E6 (stale version and request checks): `handleFrontmatterSave` is unchanged and applies one patch.
- P-S2, P-S4, P-E8: no message protocol, webview or edit-entry changes.
- UX-22, UX-34 (frozen): not touched.

## Findings
1. **[BLOCKER] `src/frontmatter/okfFrontmatter.ts`: in `minimalPairPatch`, CRLF documents get a lone
   `\r` inside the edited field. In VS Code, that becomes a blank line splitting a comment group.**

   **Cause.** On CRLF input, the `yaml` parser keeps `\r\n` inside multi-line comment strings. For
   example, an item's `commentBefore` is `" note line 1\r\n note line 2"`, and a map's header
   `commentBefore` is `" c\r\n d"`. The renderer emits `# note line 1\r` followed by `\n`. The
   current conversion `(rendered.endsWith("\n") ? rendered.slice(0, -1) : rendered).replace(/\n/gu,
   lineEnding)` then produces `\r\r\n`. Base (`createFrontmatterDocumentPatch`) normalizes with
   `/\r\n|\r|\n/gu` and was correct.

   **Reproduction.**
   - Source:
     `"---\r\ntags:\r\n  - one\r\n  # note line 1\r\n  # note line 2\r\n  - two\r\nstatus: draft\r\n---\r\n"`.
   - Call: `createFrontmatterFieldPatch(source, "tags", ["one", "two", "three"])`.
   - Patch text: `"tags:\r\n  - one\r\n  # note line 1\r\r\n  # note line 2\r\n  - two\r\n  - three"`.
   - Base output has clean CRLF.

   **Effect.** VS Code converts the inserted text's line breaks to the document EOL and treats the lone
   `\r` as a line break. A blank line therefore appears between `# note line 1` and `# note line 2`.
   Data verification cannot catch this, because YAML reads the extra break as a blank line.

   **Affected inputs.** Every CRLF document with two or more consecutive comment lines inside the
   edited sequence or map. This includes:
   - lines between items, or before the first item;
   - lines between nested keys;
   - `meta: # c` followed by `  # d`;
   - commented-out list items between real items;
   - no-op edits.

   **Fix.** Replace the `body` computation in `minimalPairPatch` with the same normalization
   `createFrontmatterDocumentPatch` uses:
   ```ts
   const body = rendered
     .replace(/\r\n|\r|\n/gu, lineEnding)
     .replace(/(?:\r\n|\r|\n)$/u, "");
   ```
   I validated this in a scratch build:
   - all 64 frontmatter unit tests pass;
   - every LF and CRLF probe is clean;
   - the fuzz reports 0 bad cases (data, comment multiset and line endings).

   **Tests.** Add to `test/frontmatter/okfFrontmatter.test.ts`. I checked both: they fail on the
   current code and pass with the fix.
   - `"a multi-line comment between CRLF sequence items keeps CRLF line endings"`:
     - source:
       `"---\r\ntags:\r\n  - one\r\n  # note line 1\r\n  # note line 2\r\n  - two\r\nstatus: draft\r\n---\r\n"`;
     - value: `["one", "two", "three"]`;
     - assert `assert.doesNotMatch(patch.text, /\r(?!\n)/u)`;
     - assert `applyFieldPatch` equals
       `"---\r\ntags:\r\n  - one\r\n  # note line 1\r\n  # note line 2\r\n  - two\r\n  - three\r\nstatus: draft\r\n---\r\n"`.
   - `"a multi-line comment inside a CRLF nested map keeps CRLF line endings"`:
     - source: `"---\r\nmeta:\r\n  k: v\r\n  # a\r\n  # b\r\n  z: 1\r\nother: x\r\n---\r\n"`;
     - value: `{ k: "w", z: 1 }`;
     - assert `assert.doesNotMatch(patch.text, /\r(?!\n)/u)`;
     - assert the output equals `"---\r\nmeta:\r\n  k: w\r\n  # a\r\n  # b\r\n  z: 1\r\nother: x\r\n---\r\n"`.

   Record both failures before applying the fix. Then rerun `unit types trusted`.

### Follow-ups (not blocking; same as base or cosmetic)
- MINOR: a `|+` keep-chomped block scalar as the **last** field leaves its former trailing content line
  as a blank line before the closing `---` (`s: |+\n  a\n\n---` → `s: |-\n  x\n\n---`). The data is
  correct.
- MINOR: inside the edited field, the renderer moves some comments to their own line, exactly as base
  does:
  - a header comment on a block collection, `tags:  # c` → `tags:\n  # c`;
  - `key: # c` before a scalar on the next line.

  It also re-indents a nested map's trailing comment, and normalizes inline comment spacing in
  collections (`- a  # ca` → `- a # ca`). A header suffix, similar to the scalar suffix, could keep
  these lines byte-identical.
- Round-1 MINOR 5 (`x:  # why` falls back to the whole-document patch) is still open.

## Existing assertions changed
- Round 2: none. `frontmatterPreservation.test.ts` is unchanged since round 1. `okfFrontmatter.test.ts`
  only gains tests, plus the blank-line NIT. `realInput.test.ts` only loses an unused import.
- The round-1 changes remain OK: 14 T05 `todo` markers removed, 4 F2 outputs appended (step 2b), the
  optional `schemaYaml` parameter added, and RI-T05 added.

VERDICT: CHANGES REQUESTED
