Ids in this file predate the reduction; see `reduction/mapping.csv`.

# Critic review: block-editing inventory (P10.1)

## Missing rows

- Scope rows in checklists (column Scope = `block-editing` or `block-editing?`): 59. All 59 are cited in
  `inventory/block-editing.md` (script: awk on the Scope column, `comm` against the C- ids of the inventory): none uncited.
- Rows moved out in "Checklist corrections": C-AR-093 and C-AR-103 (to lifecycle-sync).
  - C-AR-093: cited 3 times in `inventory/lifecycle-sync.md`. Handled.
  - **C-AR-103: NOT cited in `inventory/lifecycle-sync.md`** (0 hits). F-LIFE-068 (`preview.markEditorSelection`) cites only
    C-PKG-015. The row is therefore handled by no scope. This is the only gap.
- Moved-in rows (10) are all cited in the block-editing table.

## Missing behaviours

None of substance. Checked against `blockEdits.ts`, `sourceEdits.ts` (session), `textControls.ts`, `blockMoves.ts`,
`blockSelectionView.ts`, `editorKeys.ts`, `selectAllKey.ts`: read-only/Restricted Mode refusals ("needs a trusted workspace"),
stale ("out of date", reportStaleEdit), open-editor refusal, paste race ("document changed while pasting"), flush refusal
warning (`flushRefusalMessage`, `FLUSH_WAIT_MS`), CRLF (F-BLOCK-071), undo steps (F-BLOCK-018), IME, Home/End, arrows,
Escape, Tab all appear.
Minor (not blocking): the paste-failure string "VS Code could not apply the paste." (`sourceEdits.ts:420`) and the
thrown-error refusal of paste/copy are not named (F-BLOCK-051 covers refusals generically).

## Wrong/unverifiable evidence

- Scripted: 174 distinct `path:symbol` references, 0 missing files, 0 missing symbols; every quoted test title
  (`test/...:title`) found in its file (0 missing).
- Manual spot checks of coverage states (F-BLOCK-010, 014, 055, 057, 064 "untested"): no test contains
  "already being edited", "could not apply the Markdown", "changed while this block", "Loading Markdown source"
  or "source block changed". States are right.
- No false evidence found.

## Count check

Table has 77 rows: 71 tested, 5 untested, 1 doc-only (sums to 77). Undocumented: 11 rows flagged, matches the 11 listed.
"67 / 67 (59 - 2 + 10)" is arithmetically right, but is only true if C-AR-103 is cited by lifecycle-sync (it is not).

## Verdict

Fixes:
1. Add C-AR-103 to the Checklist column of F-LIFE-068 (or a sibling row) in `inventory/lifecycle-sync.md`
   (UX-47 `markEditorSelection`); lifecycle-sync counts then need its row total updated.
2. Optional: name the paste-failure refusal strings in F-BLOCK-051.

Verdict: REVISE

## Re-check

- Fix 1 done: C-AR-103 now cited in `| F-LIFE-068` of `inventory/lifecycle-sync.md` (C-AR-093 also cited there); lifecycle counts say 86 rows, matching 86 F-LIFE rows.
  Fix 2 done: F-BLOCK-051 names "VS Code could not apply the paste." (also for a thrown error).
- Checklist ids with Scope block-editing(?): 59; the only uncited are C-AR-093 and C-AR-103, both listed in Checklist corrections and cited in the lifecycle-sync F-rows. All 17 moved-in rows are cited in F-BLOCK rows.
- Spot-check: 13 path:symbol refs in 4 rows and 8 random test-title refs all found. Counts: 77 rows = 71 tested + 5 untested + 1 doc-only; 11 undocumented, ids match the list.

Re-check verdict: APPROVE
