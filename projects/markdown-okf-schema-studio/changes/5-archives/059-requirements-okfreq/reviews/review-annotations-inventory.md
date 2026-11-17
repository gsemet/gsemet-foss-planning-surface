Ids in this file predate the reduction; see `reduction/mapping.csv`.

# Critic review: review-annotations inventory

## Missing rows

All 81 checklist rows of scope `review-annotations` (scripted: ids parsed from `checklists/*.md`
with scope column `review-annotations[?]`) appear in `inventory/review-annotations.md`. 72 are
cited by F lines; 9 are listed as moved in "Checklist corrections". Target inventories were checked:

- Handled (target inventory cites the id): C-CL-002, C-CL-080, C-AR-141 (toolbar-navigation),
  C-CL-015 (block-editing); C-CL-089 is `n/a: tooling`.
- NOT handled (target inventory does not cite the id):
  - C-CL-029 (target palette-slash): absent from `inventory/palette-slash.md`.
  - C-CL-030 (palette-slash): absent there; only cited in passing by F-REVIEW-070.
  - C-AR-033 (palette-slash): absent there; only cited in passing by F-REVIEW-070.
  - C-AR-016 (target code-blocks): absent from `inventory/code-blocks.md`.

## Missing behaviours

None of substance. Constants and guards in anchoring (negation words, candidate/rare-occurrence
caps, fuzzy text cap), author fallback, queue serialisation, HEAD cache cap (64), CRLF, undo,
stale, read-only/untrusted/standalone are all present. Minor: `headBaseline.ts` cache cap of 64
entries is not mentioned (optional note).

## Wrong/unverifiable evidence

Scripted check of all 237 `src|test` path references in the Evidence column: every file exists,
every symbol and test title found by grep (0 failures). Manually confirmed: the 3 "untested" rows
(F-REVIEW-006, 044, 065) have no test mentioning them (integration tests only cover the
untracked-file case for incoming changes); `INCOMING_CHANGES_DEBOUNCE_MS = 300`, `NEGATIONS`,
`MAX_CANDIDATES = 200`, `MAX_RARE_OCCURRENCES = 20`, `MAX_FUZZY_TEXT` match the text. No false evidence.

## Count check

Table has 70 F rows (ordered, unique): 67 tested, 3 untested, 19 undocumented; matches Counts.
75 distinct ids cited in F lines = 72 staying + 3 moved-but-cited (C-AR-033, C-AR-141, C-CL-030);
72 + 9 = 81 matches.

## Verdict

REVISE only because 4 moved rows are not picked up by their target scope. Fixes:
1. Add C-CL-029 and C-CL-030 and C-AR-033 to `inventory/palette-slash.md` (Link button/Cmd+K,
   edition palette bar), or keep them in this scope with an F line.
2. Add C-AR-016 (code Copy button) to `inventory/code-blocks.md` (F-CODE-017..019), or keep it here.

Verdict: REVISE

## Re-check

- Fixes: C-CL-029 now cited by F-PALETTE-031, C-CL-030 and C-AR-033 by F-PALETTE-002, C-AR-016 by F-CODE-019 (target `| F-` lines, scripted); C-CL-002/080/AR-141/CL-015 also cited in toolbar-navigation and block-editing F-lines.
- All 81 ids assigned to the scope are in an `| F-` line or in Checklist corrections (C-CL-089 n/a tooling); 175 `src|test` path:symbol evidence refs re-grepped in the worktree, 0 failures; Counts (70 F rows, 67 tested, 3 untested, 19 undocumented, 83 ids) match.
- Cosmetic only: Checklist corrections names F-PALETTE-010 for C-CL-030 and F-BLOCK-042 for C-CL-015, but the target cites are F-PALETTE-002 and F-BLOCK-039/040.

Re-check verdict: APPROVE
