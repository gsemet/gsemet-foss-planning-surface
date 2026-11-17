# T01 review — round 1

Base: aeb9c03c03db6f6de202969742345e3f43cfdc73 · Reviewed diff: 3 files (all new, untracked),
+448/-0 (`test/shared/lineDelta.ts` 23, `test/webview/markdownTablePreservation.test.ts` 146,
`test/frontmatter/frontmatterPreservation.test.ts` 279). `git diff aeb9c03 -- src/markdown-okf-schema-studio AGENTS.md`
is empty: no tracked file changed, nothing under `src/` changed.

## Gates

- compile: PASS (`logs/T01-review-compile.log`, rerun by the reviewer)
- unit: PASS (`logs/T01-review-unit.log`): 355 tests, 321 pass, 0 fail, 34 todo. T00 baseline:
  315 tests, 315 pass, 0 todo. 321 = 315 old + 6 new passing tests, so every baseline test still
  passes.
- types (extra, not required by the task): PASS (`logs/T01-review-types.log`).
- Matches the orchestrator's gate summary and `logs/T01-unit.log`.

## Todo markers: verified against a marker-free run

I copied the two compiled test files to the scratchpad, pointed their `require`s at the real `out/`
modules, replaced every `{ todo: … }` options object with `{}`, and ran them with `node --test`:

- 40 tests, **6 pass, 34 fail**. The 34 failing tests are exactly the 34 tests that carry a marker;
  the 6 passing ones (3 `lineDelta`, `alignment` round trip, `alignment` one-cell edit, the F2
  comments guard) carry none. No marker sits on a passing test; no failing test is unmarked.
- Every failure is on the intended property, never on test plumbing (no `patch must be produced`,
  no `fixture must contain this block once`, no exception):
  - tables: round trip differs on the rewritten delimiter / collapsed padding / added outer pipes /
    dropped indentation; one-cell edit fails `removed.length` with 2 or 3 changed lines;
  - frontmatter value and structural edits: the full-text diff shows only the whole-block
    reserialization artefacts (plain multi-line `description` joined, `- x` re-indented to `  - x`,
    `# trailing comment` spacing collapsed, `[a.md, b.md]` → `[ a.md, b.md ]`, folded `summary`
    joined or turned into a plain scalar). The "expected" side of every diff is the task's
    contract.
- The implementer's pre-marker log `logs/T01-tap.txt` shows the same 34 failures (6 pass, 34 fail).

## Expected values: verified

- **Tables.** All 9 corpus entries match the task table byte for byte (sources, `rows[r][c]`, new
  value, expected line; the delimiter row is index 1 in `parse`'s model, as the task states). I
  applied the documented padding rule by hand to each entry and it yields exactly the expected
  line: e.g. `" Ana "` → `" Ana Lee "` (too long, one trailing space), `" second   "` →
  `" second X "` (width 10 kept), `"d"` → `"dee"` (no whitespace stays without), `" d"` → `" dd"`
  (no-outer-pipes, leading kept, no trailing), CRLF → `"| Ship | Bob |\r"`.
- **Frontmatter.** Fixtures F1–F4 match the task (F3 = F1 with every `\n` → `\r\n`, F4 = F2 with
  `...`). All 14 value rows and 4 structural rows use the task's old/new blocks and compare the
  full resulting document (the robust variant the task asks for). I parsed every expected document
  with `extractFrontmatter`: each one has no YAML error, the same key order, and deep-equals the
  original data with only the named field changed (`derived_by: [X-1]` → `["X-1"]`,
  `quoted: "still: quoted"`, `summary: >-\n  New summary` → `"New summary"`,
  `exemption_reason: n/a`, `annotation_exemption: true` → boolean). Rename yields key `heading`
  in first position, removes yield the right key sets, add puts `owner: Ana` last.
- The expectations are consistent with the designs of T04 (padding rule), T05 (`minimalPairPatch`:
  scalar type copy gives `summary: >-`, `indentSeq` detection gives compact F1 / indented F2
  sequences, `flowCollectionPadding: false`, inline-comment suffix kept) and T06 (add at the end of
  `text` with `lineEnding + rendered` gives `- tests/test_export.py\nowner: Ana\n---`).

## Done-when

- [x] The `unit` gate passes — evidence: `logs/T01-review-unit.log` (0 fail, 34 todo).
- [x] The report lists every `todo` test with its failure reason — evidence: report section
  "Tests written first", 34 entries; the per-test counts (`actual: 2`/`3`) match
  `logs/T01-tap.txt` and my marker-free run.
- [x] Compact, padded, no-outer-pipes and CRLF table edits, and F1 `title`, F1 `derives_from`,
  F2 `title` frontmatter edits are present and fail without the marker — evidence: marker-free
  run, tests `one-cell edit changes exactly one line: compact-book|padded|no-outer-pipes|crlf`,
  `value edit F1 title|F1 derives_from|F2 title changes only the named field`.
- [x] `lineDelta` splits on `\n` only, trims prefix then suffix without overlap (suffix loop bounded
  by `limit - prefix`), and has the 3 required tests (identical, one changed, one inserted).
- [x] Padding rule documented as a comment at the top of `markdownTablePreservation.test.ts`.

## Protected features checked

Tests only; no runtime, host or webview code changed, so checks D-14 to D-17 and E do not apply.

- P-E5 (table cell editor): `parse`/`serialize` unchanged; `test/webview/markdownTable.test.ts`
  and the `scrollSync.test.ts` table tests still pass (part of the 315 baseline tests).
- P-E7 (frontmatter editing, comments preserved): `okfFrontmatter.ts` unchanged; existing
  comment tests in `okfFrontmatter.test.ts` ("frontmatter field patches preserve comments…",
  "array edits keep comments…", "key renames preserve comments…", "field removal preserves
  comments…") still pass, plus the new non-todo F2 comments guard.
- Packaging: `.vscodeignore` excludes `test/**` and `out/test/**`, so the new `test/shared/`
  folder does not reach the VSIX. `test:unit` globs do not include `out/test/shared/`, so the
  helper is not run as a test file.

## Findings

1. [MINOR] `test/frontmatter/frontmatterPreservation.test.ts`: test "structural F2 edits keep both
   comments unless their own line is removed" — the task asks for the comment check "in every F2
   case", but `outputs` covers only 5 of the 9 F2 operations (rename title, remove links, remove
   tags, value title, value status). Missing: the F2 value edits `tags` ← `["one","two","three"]`,
   `links` ← `["a.md","c.md"]`, `quoted` ← `"still: quoted"`, `summary` ← `"New summary"`
   (and optionally the F4 `status` edit with `F4` as source). Impact is low: those cases are
   already covered byte-for-byte by the todo full-text tests once T05/T06 remove the markers, and
   comment preservation is covered today by `okfFrontmatter.test.ts`. Fix (can be done by T05 or
   as a follow-up): append to the `outputs` array
   `applyPatch(F2, createFrontmatterFieldPatch(F2, "tags", ["one", "two", "three"])!)`,
   `applyPatch(F2, createFrontmatterFieldPatch(F2, "links", ["a.md", "c.md"])!)`,
   `applyPatch(F2, createFrontmatterFieldPatch(F2, "quoted", "still: quoted")!)`,
   `applyPatch(F2, createFrontmatterFieldPatch(F2, "summary", "New summary")!)`; they pass today
   (the marker-free diffs show both comment lines present in those outputs), so no marker.
2. [NIT] `reports/T01-implementation-r1.md` calls F1's `description` a "folded scalar"; it is a
   plain multi-line scalar (F2's `summary` is the folded one). Wording only.
3. [NIT] For T04 (not a T01 defect, the corpus follows the task): the padding rule's "keep the
   original width" branch is only exercised with a value that grows within the width
   (`" second   "` → `" second X "`). T04 could add a shrinking case, e.g. padded `rows[2][1]` =
   `s` → `| first    | s        |`.

## Existing assertions changed

None. `git diff aeb9c03 -- src/markdown-okf-schema-studio` is empty; only the three new files
exist. The 34 `todo` markers are the ones T01 is required to create, and each sits on a test that
fails today for the intended reason.

VERDICT: PASS
