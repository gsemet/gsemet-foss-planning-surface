# T41 review — round 1

Base: fabc1fa · Reviewed diff: 6 files, +449/-34
(`src/extension.ts`, `src/frontmatter/okfFrontmatter.ts`, `src/webview/scrollSync.ts`, three test files)

## Gates
- unit, types, contracts: PASS (orchestrator gate).
- full: PASS in 223 s (`logs/T41-full.log`).
- visual: PASS against the baseline, with 0 new failures.
- No new failure compared with the T00 baseline.

## Done-when
- [x] **D-21 a, position.** Covered by these tests:
  - unit: `T41: a schema field goes between its schema neighbours…`, `…skips absent schema
    neighbours…`, `…custom key goes after the last row…`, and `T41: beforeField inserts above the
    named field…` (start, middle, CRLF);
  - E2E: RI-T41 step 1 (one-line diff after `owner`, with the row right after `owner`), and RI-T24
    and RI-T25 updated.

  I also checked `frontmatterAddPlacement` by hand against `fieldsFromYaml`:
  - `(['b','x','a'],['a','b','c'],'c')` gives `after b`;
  - `(['b'],['a','b'],'a')` gives `before b`;
  - `(['x'],['a'],'a')` gives `before x`;
  - `(['x'],['a'],'y')` gives `after x`;
  - an empty frontmatter, and no schema, give `{}`.

  All of these match the table order. I also checked these cases:
  - CRLF, with a comment between keys: the key is inserted after the anchor's line and before the
    comment that belongs to the next key.
  - An empty frontmatter: correct.
  - Duplicate keys: `extractFrontmatter` rejects them, so the code never reaches this path.
  - `expected` uses the same `afterField` and insert index (0 for `leading`). `verified` compares
    the key order, so a position that did not match would be rejected. It would never be written
    silently.
- [x] **D-21 b, Enter and Shift+Enter for a new custom key.** Covered by the webview tests:
  - Enter saves, with `fieldValueStyle: "plain"`;
  - Shift+Enter does not save;
  - an existing field's save carries no style.

  RI-T41 step 2 shows the one-line diff `approver: Ann`, and RI-T25 shows `reviewer: Ana`.
- [ ] **D-21 b, "quoted only when YAML requires it."** Not fully met: some values are written plain
  but are not read back as strings by the project's own YAML consumer. See finding 1.
- [x] **D-21 c, Escape.**
  - The document listener checks three things: there is an `activeFrontmatterEdit`, it is not
    `saving` or `disabled`, and the target is inside `[data-okf-properties]`.
  - `edit.cancel()` sets the same closure `cancelled` flag that `saveValue` and the key-save path
    check, so the later blur or focusout writes nothing.
  - The control's own Escape closes the editor first, which leaves `activeFrontmatterEdit`
    undefined, so this listener does nothing on the bubble. No double handling.
  - The block and table-cell Escape listener is unchanged.
  - Evidence: the webview tests, RI-T41 step 3 (buffer unchanged), and the screenshot
    `t41-escape-on-picker.png` (`status: draft` unchanged).
- [x] **Plain style only for a just-created custom key.**
  - The webview sends the style only when all of these hold: `options.newField`, the value is `""`,
    the declared type is unknown, and the row has class `okf-unknown`.
  - The host also requires all of these: not an add, a remove or a rename; the current value is
    `""`; and the new value is a string.
  - `isPreviewSyncMessage` accepts only `"plain"`, only on `previewFrontmatterSave`, and only
    without `frontmatterAction` or `fieldValueFormat`. Any other message must leave it
    `undefined`.
  - A probe showed that an existing quoted value keeps its quotes without `plainScalar`
    (`title: '"Ann"'` style unchanged).
  - A trailing comment is kept: `title: ""  # note` became `title: Ann  # note`.

## Protected features checked
- **P-F (frontmatter writes):**
  - one-line diffs: RI-T41 `lineDelta` checks, and the unit test for CRLF and the middle position;
  - comments kept: probe, with the comment between keys kept and the trailing comment kept;
  - UX-16 and part-2 style preservation: `minimalPairPatch` is unchanged unless `plainScalar` is
    set, and the existing unit suite passes.
- **D-08 required fields:** RI-T24 still asserts that Remove is disabled for `scope`. The diff does
  not touch the remove path.
- **P-S2 / P-S4:** the new field is validated, and the version checks of the edit path are
  untouched. No new `innerHTML`.
- **P-E8:** the Escape listener needs an open frontmatter editor, so it stays inert in read-only
  mode.
- **Webview template (`conventions.md` §2):** the new runtime code has no backtick and no `${`. The
  `\\b` in the regex is doubled correctly, and there is no global `setTimeout`.
- **Frozen behaviour (UX-22, UX-24, UX-34):** not touched.

## Findings
1. [MAJOR] `src/frontmatter/okfFrontmatter.ts`:`isPlainSafeScalar`.
   - **Problem.** The check uses the `yaml` library's YAML 1.2 core schema, plus a short list of
     1.1 booleans. The book's frontmatter is read by PyYAML (MyST front matter, `safe_load`, YAML
     1.1). I ran a probe against the built `out/` code, then read the results with PyYAML:

     | Value written plain | PyYAML result |
     | --- | --- |
     | `2026-10-13` | `datetime.date` |
     | `1_000` | `1000` |
     | `0b101` | `5` |
     | `12:30` | `750` |
     | `1:20:30` | `4830` |
     | `=` | `ConstructorError`: the whole frontmatter fails to load |
     | `<<` | `ConstructorError` |
     | `a<TAB>b` | `ScannerError` |

     The last three corrupt the file for the Sphinx build. The first five silently change the type.
   - **Fix.** After the existing checks, also require
     `stringify(text, { version: "1.1", lineWidth: 0 }) === text + "\n"`. I verified that this
     quotes `2026-10-13`, `1_000`, `0b101`, `12:30` and `1:20:30`, and keeps `Ann` and `two words`
     plain. Also return `false` for `/\t/u.test(text)` and for `/^(?:=|<<)$/u.test(text)`.
   - **Test.** In `test/frontmatter/okfFrontmatter.test.ts`, extend `T41: plain scalar safety`:
     - assert `false` for `2026-10-13`, `1_000`, `0b101`, `12:30`, `1:20:30`, `=`, `<<`,
       `"a\tb"`, `1e3`, `0x1F`, `.inf`, `- x`, `[a]`, `{a}`, `*a`, `&a`, `!t`, `%x`, `@x`, `` `x``,
       `'quote`, `"q`, `a #b` and `key: v`;
     - keep `true` for `Ann`, `two words` and `?x`.

     Add one `plainScalar` patch case asserting that `2026-10-13` is written as
     `approver: "2026-10-13"`.
2. [MINOR] `src/frontmatter/okfFrontmatter.ts`:`minimalAddPatch`, the `leading` branch.
   - **Problem.** The key goes at text offset 0, above a leading comment block. For
     `# header\ntitle: x`, the result is `a: ""\n# header\ntitle: x`. This is valid and
     `verified`, but it moves the key above file-header comments, for example a
     `# yaml-language-server: $schema=…` modeline.
   - **Safer behaviour.** Insert at the start of the line that holds the first key, after any
     leading comment lines: `offset = text.lastIndexOf("\n", root.items[0].key.range[0] - 1) + 1`,
     with the CRLF case handled by the same `\n` search.
   - **Test.** A unit test where `beforeField` is the first key and a `# header` comment line comes
     first. Expect `# header\na: ""\ntitle: x`, as a one-line diff.
   - **Trade-off.** A comment that documents the first key then sits above the new key. Header
     comments matter more, so this is still the better option. Severity is MINOR, so this does not
     block on its own.
3. [NIT] `frontmatterAddPlacement`.
   - **Behaviour.** JS `Object.keys` puts integer-like keys first (for example `2024:`), and a YAML
     key that parses as a number never matches the string anchor. In that case the add falls back
     to an append, with `positioned: false`.
   - **Assessment.** This is safe, because the order is verified and nothing is corrupted. No
     action is needed.

## Existing assertions changed
- RI-T24 `scenarioRequiredAndPositionedAdd`: `depends_on: []` now follows `owner` instead of
  `scope`. Required by D-21 a. The exact-buffer and `lines()` equality checks are kept. **OK.**
- RI-T25 `scenarioCustomKeyAndOpenNewField`: `reviewer: ""` now follows `owner` instead of `scope`,
  and the value is saved with Enter as `reviewer: Ana`, not with Cmd+Enter as `"Ana"`. Required by
  D-21 a and b. Exact-buffer equality is still asserted, and nothing else changed. **OK.**
- No other existing assertion was modified or removed. Every other test change is an addition.

VERDICT: CHANGES REQUESTED
