# T05 review — round 3

Base: 98f624722ef8616d02c4a045a7c32dd4ddc435a9 · Reviewed diff: 4 files, +420/-23

Since round 2, only two files changed (checked by modification time against `T05-review-r2.md`):
- `src/frontmatter/okfFrontmatter.ts`: in `minimalPairPatch`, the `body` computation and a two-line
  comment;
- `test/frontmatter/okfFrontmatter.test.ts`: two tests appended.

`frontmatterPreservation.test.ts` and `realInput.test.ts` are unchanged since round 2.

## Gates
- compile: PASS (`logs/T05-r3-compile.log`). I recompiled locally.
- unit: PASS (`logs/T05-r3-unit.log`, `logs/T05-impl-r3-unit.log`): 394 tests, 390 pass, 0 fail,
  4 todo (T06 markers only). My local run of `okfFrontmatter.test.js` and
  `frontmatterPreservation.test.js` gave 66 tests: 62 pass, 0 fail, 4 todo.
- types: PASS (`logs/T05-r3-types.log`).
- trusted: PASS on the round-2 tree (`logs/T05-impl-r2-trusted.log`, exit 0, includes
  `PASS real-input screenshot: 08-frontmatter-value-minimal-patch`). **Not yet run on this round-3
  tree** because the screen is locked. As instructed, I did not run it.
  - Why the risk is low: the round-3 change only affects rendered text that contains `\r`. Only
    CRLF documents with multi-line comments produce such text. The RI-T05 fixture (`REQ_DOCUMENT`)
    is LF, so its output is unchanged.
  - Condition: this PASS holds only if the orchestrator's `gate.sh T05 trusted` run on this tree is
    green before the commit, with no new failure against the T00 baseline.
- Compared with the T00 baseline: no new unit or type failures.

## Round-2 BLOCKER: verification
**The fix matches the round-2 instruction exactly.** `minimalPairPatch` now builds `body` with the
same normalization as `createFrontmatterDocumentPatch`:

```ts
const body = rendered
  .replace(/\r\n|\r|\n/gu, lineEnding)
  .replace(/(?:\r\n|\r|\n)$/u, "");
```

**The tests match the specification.** Both tests are worded exactly as round 2 specified, including
the `assert.doesNotMatch(patch.text, /\r(?!\n)/u)` check and the full expected output strings:
- `a multi-line comment between CRLF sequence items keeps CRLF line endings`;
- `a multi-line comment inside a CRLF nested map keeps CRLF line endings`.

**The tests fail before the fix.** `logs/T05-impl-r3-prefix-unit.log` shows both tests failing on
the lone `\r` before the fix (`fail 2`):
- `'tags:\r\n  - one\r\n  # note line 1\r\r\n  # note line 2\r\n…'`;
- `'meta:\r\n  k: w\r\n  # a\r\r\n  # b\r\n  z: 1'`.

I confirmed this independently by mutation. In a scratch copy of the compiled `out/`, I restored the
round-2 `body` expression. Exactly these two tests then failed (60 pass, 2 fail). Both pass on the
current code.

## Earlier findings: still fixed
The code for the round-1 fixes is unchanged since round 2. I re-ran the round-2 mutation checks on a
scratch copy of the current `out/`:

| Fix | Mutation | Tests that fail |
| --- | --- | --- |
| R1-2 (block-scalar header comment) | drop `&& !originalIsBlockScalar` from `commentNode` | `editing a block scalar keeps its header comment` |
| R1-1/R1-3 (trailing comment duplicated; doubled when a scalar becomes a list) | limit `commentNode` to Scalars | `appending to a sequence keeps a trailing commented-out item once`, `editing a nested map keeps its trailing comment once`, `replacing a commented scalar by a list keeps the comment once` |
| R1-4 (no `PLAIN` type copy) | drop `&& originalValue.type !== "PLAIN"` | `a multi-line value on a plain field is written as a literal block` |

The round-1 NITs are still applied: the unused import is removed and there is one blank line.

## CRLF re-probe (scratch scripts outside the repository, against the compiled `out/`)
I compared the current `out/src/frontmatter/okfFrontmatter.js` with base 98f6247, compiled into
scratch space.

**Hand-written probes: 65 cases, each in LF and CRLF (130 runs).** They cover:
- block scalars with header comments (`>- # header`, `| # header`, `|+`, `|2 # h`, `>2+ # h`):
  - turned into a string, `null`, a list, a number or multi-line text;
  - followed by comment lines at column 0 or at content indentation;
  - with comments before the key;
  - as the last field;
- trailing comment lines:
  - commented-out items, with an append or a no-op edit;
  - two-line groups at item indentation, at column 0, deeper, and after a blank line;
  - inside nested maps and sequences of maps;
  - a block list turned into `[]` or `null`;
  - the last field, the only field, the `...` end marker, and trailing blank lines;
- multi-line comments:
  - between sequence items, with append, no-op, remove and reorder edits;
  - before the first item;
  - between nested keys, including a no-op edit;
  - `meta: # c` followed by `  # d`;
  - three commented-out items between real items;
  - three-line groups inside a sequence of maps;
  - inside unindented sequences and nested sequences;
- sequences:
  - inline item comments;
  - padded, unpadded and multi-line flow sequences, a flow map, and a flow sequence turned into `[]`;
- scalars: inline comments, a scalar turned into a list or map, quoted values, empty values,
  `x:  # why`, an anchor, non-BMP characters, and a tab before a comment.

Every CRLF run meets all of these checks:
- the output has no lone `\r` and no lone `\n`;
- the patch never splits a `\r\n` pair;
- the bytes outside the patch are unchanged;
- the output with `\r\n` → `\n` equals the LF output;
- the comment multiset equals base.

The data is correct in every case, except one artifact of my probe's expectation: in
`a: &x 1` / `b: *x`, `b` follows the alias. That case takes the whole-document fallback, and its
output is byte-identical to base.

**Seeded fuzz: 3 seeds × 4,000 documents, LF and CRLF (23,312 edits).** The documents mix random
fields with random one- to three-line comment groups: plain, quoted, folded and literal scalars with
header comments; indented and unindented sequences; sequences of maps; flow collections; nested maps;
and empty values. The edits are append, remove, reverse, `[]`, scalar, `null`, map changes, type
changes and no-ops. Results:
- 0 data errors;
- 0 comment-multiset differences from base;
- 0 CRLF impurities;
- 0 differences between the CRLF output and the LF output;
- 0 changes outside the patch region.

On the round-2 code (mutated scratch copy), the same fuzz flags 286 CRLF cases and the probes flag
15, so the harness does detect the round-2 defect.

**Extra CRLF edges.** In each of these cases, verification keeps the data correct and the output
matches base:
- a value containing `\r` or `\r\n` on a literal, plain or quoted field, and inside a list item;
- a `|+` field set to `"x\n\n"`.

## Done-when
- [x] `unit` gate passes: `logs/T05-r3-unit.log`.
- [ ] `trusted` gate passes: PASS on the round-2 tree. **Pending on this tree** (orchestrator, after
  unlock, before commit). See Gates.
- [x] T01 value-edit tests pass without markers: the 14 `value edit … changes only the named field`
  tests pass. No `UX-16 (T05)` marker remains.
- [x] RI-T05 shows a one-line diff: `scenarioFrontmatterValueMinimalPatch` asserts `lineDelta`
  `status: draft` → `status: active`. It passed in the round-2 trusted run, and its code is
  unchanged.
- [x] The reviewer finds no bad input. **Data: met.** About 23,400 LF and CRLF edits and probes
  found no input where the minimal path writes data different from `expected`. **Comments and CRLF:
  met.** The round-2 CRLF defect is gone, and no comment is lost, duplicated or moved compared with
  base. The fallback is exercised by `value patch for an anchored value still writes correct data`.

## Protected features checked
- **P-E7** (frontmatter editing, YAML comments preserved): LF and CRLF are covered by the round-1 and
  round-2 tests, the two new CRLF tests and the T01 corpus. My probes and fuzz confirm the coverage.
  Add, rename and remove (T06), `handleFrontmatterSave` validation and `parseYamlValue` are
  untouched.
- **P-R7 / UX-24** (properties table value display): `propertiesTable.ts` is untouched, and the data
  is verified.
- **P-E6** (stale version and request checks): `handleFrontmatterSave` is unchanged and applies one
  version-checked patch.
- **P-S2, P-S4, P-E8**: no change to the message protocol, the webview, or the edit entry points.
- **UX-22, UX-34** (frozen): not touched.
- **Conventions §5** (CRLF must not get worse): now met. In CRLF output, every line break is `\r\n`.

## Findings
None new. The round-3 change is limited to the specified fix and its two tests.

### Follow-ups (carried over, not blocking; same as base or cosmetic, data correct)
- **MINOR**: when a `|+` keep-chomped block scalar is the **last** field, a blank line is left before
  the closing `---`.
- **MINOR**: inside the edited field, the renderer moves or reformats some comments, as base does:
  - `tags:  # c` and `key: # c` become comments on their own line;
  - a nested map's or a deeper item's trailing comment is re-indented;
  - inline comment spacing is normalized (`- a  # ca` → `- a # ca`).

  A header suffix, like the scalar suffix, could keep these lines byte-identical.
- **MINOR** (round 1, finding 5): `x:  # why` falls back to the whole-document patch. The data is
  correct, and the output is identical to base.
- **NIT**: the `!originalIsBlockScalar` term in `suffix` is redundant (noted in round 2). It is
  harmless.

## Existing assertions changed
- Round 3: none. `okfFrontmatter.test.ts` only gains two tests, and its diff against base is
  `+151/-0`.
- The round-1 and round-2 changes remain OK:
  - 14 T05 `todo` markers removed, and the T06 markers kept;
  - 4 F2 outputs appended (step 2b);
  - the optional `schemaYaml` parameter added to `withDocument`;
  - RI-T05 added;
  - the unused import removed.

VERDICT: PASS
