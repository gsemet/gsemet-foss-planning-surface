Ids in this file predate the reduction; see `reduction/mapping.csv`.

# Critic review: frontmatter-schema inventory (P10.1)

Scripted against `checklists/*.md` (scope column `frontmatter-schema`, 52 rows incl. the `?`
rows) and `inventory/*.md`.

## Missing rows

- C-AR-114 (023 T1 F1: leading properties table re-measured on resize / fonts.ready / burst
  limiter): scope frontmatter-schema, cited in no inventory and not in "Checklist corrections".
- C-CL-105 (leading properties table keeps its Description toggle clear of the floating toolbar):
  not cited here or in "Checklist corrections"; `toolbar-navigation.md` l.102 says it belongs to
  layout-width but `layout-width.md` does not cite it.
- C-AR-145 (051 T1 postMessage morph incl. properties table): not listed as moved here, but it is
  cited by `lifecycle-sync.md` l.139 (F-LIFE-026/043/044/049/073). Acceptable; add a "moved to
  lifecycle-sync" line for traceability.
- Moved rows whose target inventory does not cite them: C-AR-017 (block-editing) and C-CL-004
  (layout-width) appear in no other inventory. The other moved rows (C-AR-020, 074, 075, 086, 100,
  105, C-CL-012, 013, C-CTL-022/023/025/027/028) are cited by their targets.

## Missing behaviours

None of substance. Minor: `filenameStemSuggestions` (stem completion, limit 500) in
`fileLinks.ts` and `postEditError` flush-refusal warning in `session/features/frontmatter.ts` are
editing behaviours (FMEDIT scope); `setSchemaFileReaderForTests` is test-only. Restricted Mode and
standalone (F-028), CRLF (F-001), refusals/errors (F-004/005/009/011), symlink containment (F-040)
and stale/live updates (F-027/031/048) are covered.

## Wrong/unverifiable evidence

Checked all `file:symbol` references of the 49 rows (every file and symbol exists in the 059
worktree) and 86 quoted test names (84 found by grep in `test/` and `sphinx/tests`; the two others,
"Frontmatter is not a mapping." and "applied live, good", are UI messages, not tests). Coverage states
agree with the evidence (untested F-005, 009, 027, 048 have no test names cited). No false evidence
found.

## Count check

Behaviours 49, tested 45 (44 + F-034 partial), untested 4, undocumented 18: all match the table.
"Checklist rows: 54 / 54" does not match the checklists: the scope has 52 rows, of which 3 are in
no inventory (C-AR-114, C-CL-105, and C-AR-145 only via lifecycle-sync); the 54 includes the five
C-CTL rows and C-CL-065, which are frontmatter-editing rows. "19 non-visual + 22 visual" is not
re-derivable from the text; recount after fixes.

## Fixes

1. Add C-AR-114 and C-CL-105 to a behaviour row (F-021/F-030 area) or to "Checklist corrections"
   with a target scope that cites them (layout-width for C-CL-105).
2. Make `block-editing.md` cite C-AR-017 and `layout-width.md` cite C-CL-004 (or keep them here).
3. Add C-AR-145 as moved to lifecycle-sync; fix the Counts "54 / 54" line.

Verdict: REVISE

## Re-check

All 3 fixes done: C-AR-114 cited in F-024, C-CL-105 and C-AR-145 listed in Checklist corrections and cited by layout-width / lifecycle-sync; C-AR-017 and C-CL-004 now cited by block-editing / layout-width; Counts line rewritten (52 / 52).
Scripted: all 52 scoped C- ids are cited in an `| F-` line or listed in corrections, and every moved row is cited in its target's `| F-` line (17/17).
Spot-checked 10 evidence claims (symbols, test names, 640 px, 300 ms debounce, dead `formatValue`): all found. Counts match the F-rows: 49 behaviours, 45 tested, 4 untested, 18 undocumented.

Re-check verdict: APPROVE
