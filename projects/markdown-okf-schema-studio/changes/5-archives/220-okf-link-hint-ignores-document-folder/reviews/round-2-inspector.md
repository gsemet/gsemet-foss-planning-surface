# CR 220 — Inspector review, round 2

Worktree: markdown-okf-schema-studio-wt-220 (uncommitted changes over 0b4ede78).

## Verdict: APPROVE

Round-1 findings 1–3 are fixed correctly. Nothing from round 1 regressed. No new findings.

## Round-2 changes checked

- **Finding 1: known set only when capped** (src/core/frontmatter/okfFrontmatter.ts:455-459).
  `linkKnownStems` is set only when `stems.known.length > stems.suggestions.length`. The comparison
  is exact. `known` is `index.stems()`, every key of `candidatesByStem`. `suggestions` is
  `nearestStems(dir, 500)`: one entry per Map key (deduplication comes from the Map key, with
  `Math.min` over the candidates), sliced to 500. So when nothing is capped, `suggestions` holds
  exactly the same set as `known` in a different order, and the two lengths differ only when capped.
  The editor (src/page/features/frontmatterListEditor.ts:68-71) falls back to `suggestions ∪ []`
  when the attribute is absent, which is then the full set. When capped, the attribute is emitted
  and the warning checks `suggestions ∪ known` = the full index, as in round 1.
- **Finding 2: non-finite limit** (src/core/frontmatter/stemIndex.ts:78). This is the same
  expression as `stems()` at :67: `+Infinity` returns every stem, `NaN` and `-Infinity` return none.
  The stemIndex.test.ts assertions cover `Infinity` for both methods and `NaN` for `nearestStems`.
- **Finding 3: invalid known JSON** (test/page/runtimeFrontmatterFields.test.ts:249-261). `stemsOf`
  catches the parse error and returns `undefined`. The new test checks that no exception is thrown,
  that a suggested stem stays valid, and that `zzz` warns.
- **Core assertion.** linkSuggestions.test.ts, second test: when nothing is capped,
  `linkKnownStems === undefined`. The first test (606 known, 500 suggestions) still asserts the full
  known set.
- **propertiesTable.ts:252-255** is unchanged. It emits the known attribute when the field carries
  `linkKnownStems`. The T220 table test still sets that field directly, and the comment there points
  to the analysis-level rule.
- **Visual scenarios** (test/visual/linkHintScenarios.ts). The fixture writes 600 fillers, a
  sibling and the document, so known (more than 600) exceeds the 500 suggestions and
  `data-okf-link-known` is still emitted. The assertions `known.length > 500 && includes(sibling)`
  and `suggestions.length === 500`, sibling before filler, still hold. I did not re-run the captures.
- **Requirement.** SwRS-MDOKFSTUDIO-FMEDIT-010 is `req_lifecycle: proposed`. The new boundary
  scenario now says "sent uncapped, and only when the dropdown was capped", and the verification
  note lists "no known list when nothing was capped". Both match the code. The only requirement
  files in the diff are FMEDIT-010 and requirements/tiers/log.md, so no approved requirement is
  modified.

## Gates

- `rtk proxy just check`: exit 0. Unit tests 3325/3325 (one more than round 1: the new page test),
  security tests 71/71. Coverage, projections and indexes are clean. The W2 broken cross-link
  warnings in PALETTE-264 were already there before this CR.
- `UV_NO_CONFIG=1 uv run --group requirements okfreq validate --check-links --project-root .`:
  exit 0, with only the same W2 warnings that were already there.
- T220 tests: all 5 pass inside `just check` (linkSuggestions ×2, propertiesTable ×1,
  runtimeFrontmatterFields ×2). The T22 stemIndex test passes. A direct `npx tsx --test` run of the
  page tests fails with `Cannot find module …/scripts/page-bundle.mjs`. That comes from the harness
  resolving the path for the compiled layout, so it is an environment issue and not this change.

## Findings

None. Round-1 finding 4 (raw index stems include broken or escaping symlinks) remains a note only,
as agreed.
