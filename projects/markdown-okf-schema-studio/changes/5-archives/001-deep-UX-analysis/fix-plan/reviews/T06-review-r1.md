# T06 review — round 1

Base: b3ee36dc8e4e0c608feabd9060a7cfd86a372ba1 · Reviewed diff: 4 files, +471/-64

All four files are in **Allowed files**:
- `src/frontmatter/okfFrontmatter.ts`;
- `test/frontmatter/frontmatterPreservation.test.ts`;
- `test/frontmatter/okfFrontmatter.test.ts`;
- `test/integration/realInput.test.ts`.

There is no unrelated churn. The frozen areas (UX-22, UX-24, UX-34) are not touched.

## Gates
- compile: PASS (`logs/T06-compile.log`; my rerun `logs/T06-review-compile.log`).
- unit: PASS, 406 tests, 406 pass, 0 fail, 0 todo (`logs/T06-unit.log`; my rerun `logs/T06-review-unit.log`).
  The frontmatter files alone give 78 pass, 0 fail. T05 had 394 tests (390 pass, 4 todo). T06 removes the 4
  markers and adds 12 tests.
- types: PASS (`logs/T06-types.log`, `logs/T06-review-types.log`).
- trusted: PASS, exit 0 (`logs/T06-trusted.log`, the orchestrator's run on this tree). It includes
  `PASS real-input screenshot: 09-frontmatter-rename-minimal-patch` and `10-frontmatter-remove-minimal-patch`. The
  `git fetch` and `CodeWindow: failed to load` lines are known test-host noise.
- Compared with the T00 baseline: no new failure.

## Done-when
- [x] The `unit` and `trusted` gates pass. Evidence: the logs above.
- [x] No T01 todo marker remains in `frontmatterPreservation.test.ts`. `grep "UX-16 (T06)"` finds nothing, and the
  only deleted test lines are the 4 `{ todo: "UX-16 (T06)" }` headers.
- [x] RI-T06 shows one-line or field-only diffs. `scenarioFrontmatterStructuralMinimalPatch` asserts the full
  buffer and the `lineDelta`:
  - `summary:` → `abstract:`, one line changed;
  - the three lines `tags:`, `- alpha`, `- beta` removed.

  I opened `.artifacts/real-input-nKpAUs/09-…png` and `10-…png` (the orchestrator's run). Both the buffer and
  the table are correct, and the compact sequences and the two-line `abstract` are unchanged.

  **Pre-fix failure:**
  - `logs/T06-impl-prefix2-trusted.log` shows `Timed out waiting for the key rename to reach the source buffer`.
  - I reproduced both steps with the base bundle (b3ee36d). Base rename and base remove both re-indent
    `- alpha`/`- StRS-CORE-001` and flatten `summary` to one line, so neither `waitFor` can succeed before the
    fix.
- [ ] Goal: "rename, remove and add touch only the lines of the field concerned", with P-E7 "YAML comments
  preserved". **Not met** in two cases:
  - add with `afterField` moves the anchor field's comments (finding 1);
  - removing the only field changes the frontmatter value from `{}` to `null` (finding 2).

## Specific points from the orchestrator

1. **T05 behaviour is unchanged. Verified.**
   - **Refactor equivalence.** I compared `fieldRegion`, `yamlStyle(text, original, originalPair)`, `renderPair`
     and `verified` line by line with the base `minimalPairPatch`. Ranges, `indentSeq`, `flowCollectionPadding`,
     comment save/clear/restore, the `PLAIN` type rule and the CRLF normalization are identical. `verified` adds
     two things:
     - a key-order comparison, which cannot change a value edit (the spread keeps the key in place);
     - `?? {}`, see finding 2.
   - **Differential re-probe** (scratch scripts outside the repo; current `out/` against base b3ee36d bundled with
     esbuild):
     - the T05 review cases from r1, r2 and r3, 30 sources × LF/CRLF: 60 of 60 patches are byte-identical;
     - a seeded fuzz with 4 seeds × 1,500 documents × LF/CRLF, about 68,000 value edits per seed: 0 patches differ
       from base.

     The documents mix plain, quoted, multi-line, folded and literal (`|+`, `|-`, `>`, header comments) scalars;
     indented and compact sequences with comments between items, commented-out items and deep trailing
     comments; flow collections; nested maps; empty values; quoted keys; leading, trailing and blank lines; and
     the `...` fence.
   - All T05 unit tests pass.
2. **Rename, remove and add.** I used the same fuzz, plus hand-written cases for CRLF, the first field, the last
   field before `---` and before `...`, empty frontmatter, block scalars with header comments, sequences with
   comment lines, and duplicate-looking keys. The duplicate-looking keys were `title`/`Title`/`title2`, a nested
   `meta.title` beside a top-level `title`, and int `1` beside string `"1"`.
   - **Rename** (about 36,000 per seed, 27,000 of them minimal): 0 problems. Exactly one line changes, no comment
     changes, comment attachment is unchanged, CRLF stays clean, and the duplicate guard still refuses. Quoted,
     explicit (`? key`), tagged and `key :` forms are handled. Names that need quoting (`a: b`, `123`, `true`,
     `#x`, `~`, `"`) are quoted correctly.
   - **Remove** (about 9,000 per seed, 8,300 minimal): data is correct, and no comment line outside
     `[key line, value end]` is ever deleted (position check). CRLF stays clean. First field, last field before
     `---`/`...`, and duplicate-looking keys are correct. **One regression:** removing the only field
     (finding 2). The `|+`-before-orphan-comment fallback case is byte-identical to base, so it is pre-existing.
   - **Add** (about 90,000 per seed): data and key order are correct, CRLF stays clean, and no comment byte
     changes. **But** about 5 % of the `afterField` adds insert the new field between the anchor field and the
     comment lines yaml attaches to it (finding 1).
3. **Open points of the report.**
   - **300 ms pause after select-all in RI-T06: accepted.** The cause is VS Code's webview host, not the
     extension. In `…/webview/browser/pre/index.html`, Cmd+A is not prevented: the keydown is posted to the
     workbench (`did-keydown`), and the workbench answers with an asynchronous `execCommand('selectAll')`. A
     character typed before that echo is selected again and then replaced (`bstract`).

     The failure also happens on pre-fix code, so the pause hides no T06 defect. The user-level steps stay
     real select-all, typing and Enter. See NIT 6.
   - **Blank line before the fence on add: MINOR** (finding 3). This is the task's literal "end of `text`" rule.
     The data is correct and no comment moves.
   - **Deleting comment lines inside a removed field: intended.** The task defines the removed range as "from the
     start of the key line to `fieldRegion.end`". Comments between the field's items lie inside it, and base
     deleted them too. "Keep comment lines above the key; never delete user comments" protects comments outside
     the field. The asymmetry with the field's own trailing comments, which stay, is finding 4 (MINOR).
4. **`afterField` and `positioned` do not change existing callers. Verified.**
   - `handleFrontmatterSave` calls `createFrontmatterFieldPatch(sourceText, name, value)` with no options. In
     about 15,000 adds without `afterField`, `positioned` was never set.
   - The add fallback without `afterField` is byte-identical to base.
   - Value edits ignore `options`.
   - The new `emptyFrontmatter` relaxation only opens the add path for `---\n---`, which the UI cannot reach
     today.

## Protected features checked
- **P-E7** (frontmatter editing, YAML comments preserved): rename is covered by the T01 corpus and the new quoting
  test. Remove is covered by the F2 tests and the comment-above-key test, and add by the `afterField`, empty,
  compact-list and CRLF tests. **Regressed** for add with `afterField` (finding 1) and for removing the last field
  (finding 2).
- **P-E6** (stale versions; required-field removal guard): `handleFrontmatterSave` is unchanged. The guard is still
  exercised by `integration-required-status-remove` in `previewEditing.test.ts` (trusted PASS). The guard's
  outcome for removing the only field is the same as on base: without `type` there is no schema.
- **P-R7 / UX-24** (properties-table display): `propertiesTable.ts` is untouched, and the data is verified.
- **P-S2, P-S4, P-E8**: no message-protocol, webview or edit-entry change.
- **UX-22, UX-34** (frozen): not touched.
- **Conventions §5** (CRLF must not get worse): met. Every CRLF output in the fuzz has only `\r\n` breaks.

## Findings

1. **[BLOCKER] `src/frontmatter/okfFrontmatter.ts`, `minimalAddPatch`: with `afterField`, the new field is inserted
   between the anchor field and the comment lines that belong to it.**

   **Cause.** `offset = region.end` uses `fieldRegion`, which ends at the value's `range[1]`. For a block
   collection or a scalar, `range[1]` stops before the indented comment lines that follow. yaml attaches those
   lines to the value: they lie inside the node end, `range[2]`. T05 review r1 established the same fact.

   **Reproductions** (current code, `positioned: true`):
   - `"---\ntags:\n  - a\n  # - b\nstatus: x\n---\n"` with `afterField: "tags"` gives
     `"---\ntags:\n  - a\nowner: Ana\n  # - b\nstatus: x\n---\n"`. The commented-out item of `tags` now sits under
     `owner`.
   - `"---\nmeta:\n  k: v\n  # trailing in meta\nstatus: x\n---\n"` with `afterField: "meta"`: the comment moves under
     `owner`.
   - `"---\ntitle: A\n  # indented note\nstatus: x\n---\n"` with `afterField: "title"`: same.
   - With a multi-line value (`"multi\nline"`) on the first source, the moved comment becomes block-scalar content.
     Verification then fails, and the add silently falls back to "append at the end" with `positioned: false`. T24
     would then place the field in the wrong row.

   The fuzz flags about 4,700 such adds per seed. T24 will call this path from the UI (D-08). Commented-out list
   items are a common OKF pattern.

   **Fix.** Add this helper next to `fieldRegion`:
   ```ts
   /**
    * End of a field including the comment lines that yaml attaches to its value (they lie before the value
    * node's end, `range[2]`). Excludes the final line break.
    */
   function fieldEndWithTrailingComments(text: string, pair: Pair, regionEnd: number): number {
     const nodeEnd = nodeRange(pair.value)?.[2] ?? 0;
     let end = regionEnd;
     let cursor = regionEnd;
     while (cursor < text.length) {
       const lineStart = text.indexOf("\n", cursor) + 1;
       if (lineStart === 0 || lineStart >= nodeEnd) break;
       let lineEnd = text.indexOf("\n", lineStart);
       if (lineEnd < 0) lineEnd = text.length;
       const contentEnd = lineEnd > lineStart && text[lineEnd - 1] === "\r" ? lineEnd - 1 : lineEnd;
       if (/^[ \t]*#/u.test(text.slice(lineStart, contentEnd))) end = contentEnd;
       cursor = lineEnd;
     }
     return end;
   }
   ```
   In `minimalAddPatch`, replace `offset = region.end;` with
   `offset = fieldEndWithTrailingComments(text, anchor, region.end);`. Do not use the helper in
   `minimalPairPatch` or `minimalRemovePatch`.

   **Validation.** I applied this change to a scratch copy of the compiled `out/` and checked:
   - all 78 frontmatter tests pass;
   - the 60 T05 cases stay byte-identical to base;
   - 4 fuzz seeds report no moved comment bytes.

     The only remaining attachment differences are yaml re-attributing a trailing column-0 comment after an
     empty last value. The bytes stay in place, so this is benign.

   Column-0 comments, such as `# about status` after a compact list, belong to the next key in yaml's model and stay
   above it. That is the expected behaviour.

   **Tests.** Add them to `test/frontmatter/frontmatterPreservation.test.ts`, assert the full output, and record the
   failures before the fix. Each call is `createFrontmatterFieldPatch(source, "owner", value, { afterField })`.
   - `"add after a list keeps its commented-out item above the new field"`:
     - source `"---\ntags:\n  - a\n  # - b\nstatus: x\n---\n"`, `afterField: "tags"`, value `"Ana"`;
     - expect `"---\ntags:\n  - a\n  # - b\nowner: Ana\nstatus: x\n---\n"` and `positioned === true`;
     - a CRLF variant of the same source (`\n` → `\r\n`) expects the same text with `\r\n`.
   - `"add after a nested map keeps its trailing comment above the new field"`:
     - source `"---\nmeta:\n  k: v\n  # trailing in meta\nstatus: x\n---\n"`, `afterField: "meta"`;
     - expect `"---\nmeta:\n  k: v\n  # trailing in meta\nowner: Ana\nstatus: x\n---\n"`.
   - `"add of a multi-line value after a commented list is still positioned"`:
     - source as in the first test, value `"multi\nline"`;
     - expect `"---\ntags:\n  - a\n  # - b\nowner: |-\n  multi\n  line\nstatus: x\n---\n"` and
       `positioned === true`.
   - `"add after a list keeps a column-0 comment with the next field"` (guards against over-extending):
     - source `"---\ntags:\n- a\n# about status\nstatus: x\n---\n"`, `afterField: "tags"`;
     - expect `"---\ntags:\n- a\nowner: Ana\n# about status\nstatus: x\n---\n"`.

2. **[BLOCKER] `src/frontmatter/okfFrontmatter.ts`, `verified` / `minimalRemovePatch`: removing the only field leaves
   an empty frontmatter block that the extension itself rejects.**

   **Reproduction.**
   - `createFrontmatterFieldRemovePatch("---\ntitle: x\n---\nBody\n", "title")` gives `"---\n\n---\nBody\n"`.
   - `extractFrontmatter` reports `"Frontmatter is not a mapping."`, and `analyzeFrontmatter` puts
     `✖ Invalid frontmatter YAML: Frontmatter is not a mapping.` in the properties table.
   - Base wrote `"---\n{}\n---\nBody\n"`, a valid empty mapping with no error.
   - With a comment, `"---\n# about\ntitle: x\n---\n"` gives `"---\n# about\n---\n"`, which has the same error.
   - The fuzz hits this case about 640 times per seed, which is every single-field document.

   **Effect.** This is reachable from the UI: open the only field, then press Remove. The frontmatter value
   changes from `{}` to `null`. The cause is `?? {}` in `verified`: it maps the `null` of an empty candidate
   to `{}`, so verification passes.

   **Fix.** In `verified`, reject any candidate whose root is not a mapping:
   `if (check.errors.length > 0 || !isMap(check.contents)) return false;`. Then drop the now-useless `?? {}`.
   Removing the only field then falls back to the whole-document patch and writes `{}`, as base did.

   **Validation.** I applied this to the scratch copy:
   - all 78 tests pass;
   - the T05 cases and the fuzz value edits stay identical to base;
   - single-field removes now give `{}`.

   **Test.** Add `"removing the only field leaves a valid empty mapping"`:
   - source `"---\ntitle: x\n---\nBody\n"` expects `"---\n{}\n---\nBody\n"`;
   - assert `extractFrontmatter(updated).error === undefined` and `frontmatter` deep-equals `{}`;
   - a CRLF variant `"---\r\ntitle: x\r\n---\r\nBody\r\n"` expects `"---\r\n{}\r\n---\r\nBody\r\n"`.

3. **[MINOR] (follow-up) `minimalAddPatch` without `afterField`, when the YAML text ends with blank lines.** The new
   field goes after them:
   - `"---\na: 1\n\n---\n"` gives `"a: 1\n\nowner: Ana"`;
   - with `afterField: "a"` the result is `"a: 1\nowner: Ana\n\n"`, so the claim "after the last field = without
     `afterField`" only holds without trailing blank lines or comments.

   The data is correct and no comment moves. T24 will always pass `afterField` (D-08), so this only affects the
   current UI. A possible follow-up is to place a plain add after the last top-level field
   (`fieldEndWithTrailingComments` of the last pair) instead of at the end of `text`.

4. **[MINOR] (follow-up) `minimalRemovePatch` keeps the removed field's own indented trailing comments.** Comment
   lines between the field's items are deleted, as designed. But the indented comments that yaml attaches to
   the field's value stay, and they then attach to the previous field. Example:
   - source `"links:\n  - a\ntags:\n  - x\n  # - y\nstatus: draft"`;
   - removing `tags` leaves `  # - y` under `links`.

   Nothing is lost and the data is correct, which matches the task's "never delete user comments". The orchestrator
   should decide whether remove should extend to `fieldEndWithTrailingComments` for consistency with base and with
   the deletion of inner comments.

5. **[MINOR] Tests: two of the new CRLF tests cannot tell the minimal path from the fallback.**
   - `structural CRLF remove of the last field drops the preceding break` and
     `structural CRLF add at the end appends one CRLF line before the fence` use fixtures whose whole-document
     fallback writes the same bytes.
   - A mutant that removes only `\n` of the preceding `\r\n` (`start -= 1`) survives: verification fails and the
     fallback produces the expected text.

   **Fix** (please do it in this round, since you add tests anyway). Add a compact-sequence assertion to each test:
   - remove `status` from `"---\r\ntags:\r\n- a\r\nstatus: draft\r\n---\r\n"`, expect `"---\r\ntags:\r\n- a\r\n---\r\n"`;
   - add `owner: Ana` to `"---\r\ntags:\r\n- a\r\n---\r\nBody\r\n"`, expect
     `"---\r\ntags:\r\n- a\r\nowner: Ana\r\n---\r\nBody\r\n"`.

   Base re-indents `  - a` in both, so a broken minimal path fails these tests.

6. **[NIT] `test/integration/realInput.test.ts`, RI-T06.** Keep the 300 ms pause, but make its comment state the
   cause: VS Code forwards Cmd/Ctrl+A to the workbench, which echoes `selectAll` into the webview asynchronously.
   A key typed before the echo is selected again.

7. **[NIT] Report.** The report says 13 new tests and 11 in `frontmatterPreservation.test.ts`. The actual numbers
   are 12 and 10 (406 = 394 + 12). The 13 is the pre-fix failure count.

## Existing assertions changed
- `frontmatterPreservation.test.ts`: OK. Only the 4 `{ todo: "UX-16 (T06)" }` options are removed, as the task
  requires. Their assertions are verbatim.
- `okfFrontmatter.test.ts`: OK. 2 tests added; no existing assertion changed. The existing rename and remove tests
  use regexes and pass unchanged.
- `realInput.test.ts`: OK. RI-T06 is added, plus one call in `run()`.
- `previewEditing.test.ts`: unchanged, and it passes in the trusted run.

VERDICT: CHANGES REQUESTED
