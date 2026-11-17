# Review round 1 — 219 schema-less number editor cannot commit

Verdict: **APPROVE**

Reviewed: uncommitted diff in `markdown-okf-schema-studio-wt-219` (4 files), against `rules.md`,
`backlog-item/01-intent.md`, `reports/behaviour-note.md` and `.agents/constitution.md`.

## Checks done

- Focused tests: `npm run compile` then `runtimeFrontmatterEditor.test.js`: 36 passed, 0 failed.
  `runtimeEditorFlush.test.js` (flush path, FMEDIT-067): 26 passed, 0 failed.
- Fail-before, proved by running the tests: I copied `out/`, `src/` and `scripts/` to the scratchpad
  and put back `git show HEAD:src/page/features/frontmatterValueEditor.ts`, without touching the
  worktree. The two new commit tests (`metaKey+Enter`, `ctrlKey+Enter`) fail; the other 34 pass.
  The refusal test passes before the fix too. That is expected: it pins the refusal that stays.
- No existing assertion changed. The src diff is 5 lines, all in the number check of `saveValue`.
- `git diff --check` clean; the c6-3 scenario JSON parses.
- Requirement: only `SwRS-MDOKFSTUDIO-FMEDIT-003` (`req_lifecycle: proposed`) is edited. No approved
  requirement changed.

## Edge cases (reasoned from the code and checked with `yaml.parseDocument` vs `Number(trim)`)

- Whitespace-only text: trims to `""`, so it is refused (as before).
- `"  3.5  "`, `"3.5\n"`, `.5`, `0x10`, `0o17`, `1e3`, `+3.5`, `3.`: both sides read the same number.
- `Infinity`, `.inf`, `1e400`: `Number.isFinite` is false, so they are refused (YAML would give a
  string or Infinity). This is correct.
- Flush: an invalid text still goes through the `flushingEditors` branch (`fieldValue = control.value`).
  A valid text skips that branch, and `fieldValue` was already the raw YAML text, so the message is
  the same as before. FMEDIT-067 is unchanged.
- Set to null (`forcedValue === null`) and other forced values: `yamlNumberText` is undefined, so
  `numberText` and `numberValue` fall back to the old operands. Unchanged.
- Blur: same `saveValue` path, so a valid number commits on blur.
- Unchanged value: the number check now passes, so `control.value === initialYaml` closes the
  editor without a post. Before, it showed "Enter a valid number.". This is an improvement and
  matches the "Value left unchanged" row.
- Schema number inputs: `useYamlEditor` is false, so `yamlNumberText` is undefined and the old
  expression applies.
- Host: `planFrontmatterSave` parses the YAML text with `parseYamlValue`. With no schema,
  `frontmatterValueMatchesField` returns true, so `"3.5\n"` becomes `3.5`.

## Findings

1. **nit** — `src/page/features/frontmatterValueEditor.ts:184-187`: two texts disagree between the
   page check and the host YAML parse. `0b101` passes the page check (`Number` gives 5), but YAML 1.2
   core keeps it as the string `"0b101"`, so the field flips to text. `3.5 # comment` is refused,
   though YAML reads 3.5. Both are rare and harmless: nothing is lost, the box shows what was typed,
   and no schema constrains the field. **No change requested.**
2. **nit** — `requirements/tiers/swrs/frontmatter-editing/SwRS-MDOKFSTUDIO-FMEDIT-003.md:80`: the new
   row says "the host writes rating: 3.5", but no `rating` field is introduced. The SHALL statement of
   FMEDIT-003 also speaks of "schema … fields", while the new rows are about a field without a schema.
   That is acceptable, since the behaviour note maps the superseded FMEDIT-007 into 003. Optional
   wording: "Number field without a schema, value 4.5, YAML box holding 3.5 and a line break, Cmd or
   Ctrl+Enter pressed | The YAML text is posted and the host writes the number 3.5".
3. **nit** — host-side test: `test/core/edits/frontmatterEdit.test.ts:41-53` (FMEDIT-016) already
   proves that a YAML-format save of `"4"` on a number field parses to `4`. No test uses a trailing
   newline or checks the written text `rating: 3.5`. I checked that `parseDocument("3.5\n")` gives
   `3.5`. The c6-3 replay covers the full write end to end. **No new host test needed.**
4. **nit** — marker consistency: `saveValue` carries `@implements_req` FMEDIT-019 and FMEDIT-067. The
   FMEDIT-003 marker sits at line 87 in the same function (`openFrontmatterValueEditor`), as it did
   for the existing invalid-number refusal. The new tests carry `@tests_req SwRS-MDOKFSTUDIO-FMEDIT-003`.
   The markers are consistent, and no move is needed. Adding a marker inside `saveValue` would only
   add churn in a file the stacked change also touches.

## Requested changes

None blocking. Finding 2 is an optional wording polish.
