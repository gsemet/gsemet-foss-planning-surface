# CR-344 conflicts: rebase onto CR-343 (batch-06, order O-11)

Rebase: `git rebase --onto origin/chantier/batch-06/cr-343-change-specification-garden-the-requirem ee592ea3`,
7 commits. It was stopped at 5/7 when this resolver started. It is now complete: 7 commits, none dropped,
none aborted. The first four commits stay separate: d3b0e78d, 7c6cd6bb, 2d40dacc, 223c08b3 (the approved
StRS REVIEW-001/003/012/015). Then 11dd2d3b (garden), 08789888 (trace tests), 8580aeee (r4). Nothing is pushed.

Rule used throughout: each CR prunes the `derives_from` entries that point at its own scopes. CR-343 owns
block-editing and table-editing. CR-344 owns review-annotations, frontmatter-editing and frontmatter-schema.
A link that either side removed stays removed. A link either side added (`depends_on`, `relates_to`, a new
marker, a new test) is kept. Superseded IDs are renamed to their survivor.

## Commit 5/7: 30e4297e -> 11dd2d3b "docs: garden the review-annotations and frontmatter requirements"

- **SwRS BLOCK-041 `derives_from` and its Links.**
  - CR-343 (HEAD) dropped BLOCK-014/025/016/006 and kept FMEDIT-001.
  - CR-344 dropped FMEDIT-001 (and FMEDIT-008 and REVIEW-008) and kept the block StRS.
  - Result: BLOCK-003, GFM-003, MYST-009.
- **SwRS BLOCK-058 `derives_from` and its Links.**
  - CR-343 dropped BLOCK-016 and kept FMEDIT-008.
  - CR-344 dropped FMEDIT-008 (and FMEDIT-001 and REVIEW-015, which auto-merged).
  - Result: BLOCK-025, BLOCK-006, BLOCK-014, GFM-003, in CR-343's order.
- **SwRS BLOCK-109 `derives_from` and its Links.**
  - CR-343 dropped BLOCK-025 and kept FMEDIT-008.
  - CR-344 moved FMEDIT-008 to `relates_to`.
  - Result: derives from BLOCK-014 only, and `relates_to` FMEDIT-008 is kept. CR-343's supersedes of
    BLOCK-129 and its new scenarios auto-merged.
- **StRS FMEDIT-001 `derived_by` and its Links.** BLOCK-041 is removed, which follows the BLOCK-041
  resolution.
- **StRS FMEDIT-008 `derived_by`, `depends_on` and their Links.**
  - BLOCK-058, BLOCK-109, TRUST-005 and TRUST-065 are removed (CR-344).
  - CR-343's `depends_on: SwRS BLOCK-041` and its "Depends on" link are kept.
- **StRS REVIEW-008 Links "Derived by".** The REVIEW-094 and REVIEW-100 lines take CR-344's new titles. CR-343's
  `depends_on` BLOCK-041 had auto-merged.
- **test/core/protocol/pageStateMessages.test.ts marker block.**
  - CR-343 replaced BLOCK-236..239 with BLOCK-259.
  - CR-344 renamed FMEDIT-054 to FMEDIT-016.
  - Result: BLOCK-259 and FMEDIT-016.
- `just requirements-lint` was run on the resolved state before `--continue`: it passed (0 errors).

## Commit 6/7: 927f540 -> 08789888 "test: trace the review and frontmatter requirements to focused tests"

- **requirements/tiers/log.md.** Both sections are kept under 2026-11-17: CR-343's "Garden block-editing and
  table-editing" first, then CR-344's "Gardening of review-annotations, ...".
- **test/core/protocol/pageStateMessages.test.ts.**
  - CR-344 moved FMEDIT-016 to a focused test.
  - CR-343 had BLOCK-259.
  - Result: BLOCK-259 only.
- **test/core/protocol/pageToHost.test.ts.**
  - CR-344's new test "previewFrontmatterSave is refused ..." is kept. Its marker BLOCK-245 is renamed to
    BLOCK-259, because CR-343 merged BLOCK-236..245 into BLOCK-259. FMEDIT-016 is kept.
  - CR-343's `// @tests_req SwRS-MDOKFSTUDIO-BLOCK-259` stays on the "CR 025: previewEditFlushed" test.
- **test/integration/realInput/blockKeys.ts.** CR-344's new `scenarioTodoToggle` (REVIEW-012 and REVIEW-160) is
  kept. CR-343's `// @tests_req SwRS-MDOKFSTUDIO-BLOCK-047` stays on `scenarioCtrlEnterCommit`.
- **test/page/modules/editActions.test.ts file-level block.**
  - CR-343 removed the TABLE-073..117 lines and placed markers on their tests.
  - CR-344 removed REVIEW-160 and placed it on the TODO tests.
  - Result: both lines are removed, and every per-test marker from both sides is kept.
- **test/integration/previewEditing.test.ts** (2 hunks: CR-344 split `run()` into step functions and moved
  helpers to previewEditingHelpers.ts).
  - CR-343 changed only markers in this file. It moved StRS BLOCK-003 and SwRS BLOCK-014, 053, 058, 094, 191
    and 216 off the file-level block onto their steps.
  - Method: I took CR-344's restructured file, then re-applied CR-343's placements.
  - CR-344's step markers already cover BLOCK-003, 014 and 216 (stepBodyEdits), BLOCK-094 and 053
    (stepTableAndInsert), BLOCK-058 (stepFrontmatterSaves) and BLOCK-191 (stepEditLock).
  - I added the two code points that CR-343 marked and the step markers did not cover:
    `// @tests_req SwRS-MDOKFSTUDIO-BLOCK-058` before `autosaveContext`, and
    `// @tests_req SwRS-MDOKFSTUDIO-BLOCK-191` before `latest` (the mismatched block save), both in
    stepBodyEdits.
- **scripts/marker-baseline.json.** The union of both sides' removals is kept (commentStyles.ts and
  previewEditing.test.ts are gone), with the lower value of each conflicting entry. Then
  `node scripts/check-marker-companions.mjs --update` lowered the entries to the actual counts:
  pageStateMessages 5, realInput/markers.ts 19 (blocks and unnamedCompanionLines), editActions 35. No entry
  was raised or added. `node scripts/check-marker-companions.mjs` passes.
- `just requirements-lint` was run on the resolved state before `--continue`: it passed.

## Commit 7/7: b84864ec -> 8580aeee

There was no conflict.

## Checks

- Byte-order mark: none of the 13 resolved files had one before, and none has one after (first bytes checked).
- No ID superseded by CR-343 (BLOCK-236..245, 029, 002, 129, 258; TABLE-070, 073, 074, 076, 080, 003..005, 102,
  035, 118) or by CR-344 (REVIEW-069 and the others, FMEDIT-054, FMSCHEMA-060) is left in an `@tests_req` or
  `@implements_req` marker in src/, test/ or scripts/ (grep).
- `just requirements-update`: exit 0, "0 files updated, 0 indexes updated, 0 requirement OKF projections
  updated". It changed nothing, so no generated navigation or coverage commit is needed.

## Fast gate (run on the rebased tip 8580aeee)

- `just requirements-lint`: **pass** (exit 0): "1136 requirements, 0 errors, 27 warnings" (pre-existing W2 cross-link
  warnings), 0 indexes / 0 projections / 0 coverage files would change, "main paths: 79 StRS checked, 538
  SwRS citations, all valid". Log: work/gates/conflict-requirements-lint.log.
- `just check` (first run): **fail** (exit 1). check-limits reported
  "test/page/modules/editActions.test.ts: 1501 lines, over the 1500-line limit of test/; split it". CR-343's
  per-test TABLE markers and CR-344's per-test REVIEW-160 markers together push the file one line over.
  - Fix, **left uncommitted in the worktree** because a resolver does not commit: the TODO-cases loop body
    `test("editActions todo " + ..., () => { assert.equal(...); });` becomes one line,
    `test("editActions todo " + JSON.stringify(input), () => assert.equal(run("todo", input), expected));`.
    The file is now 1499 lines and the behaviour is the same.
  - It belongs to commit 08789888 ("test: trace the review and frontmatter requirements to focused tests"):
    the Driver or Coder should fold it there, for example with a fixup commit and an autosquash rebase.
- `just check` (rerun with that fix): **pass** (exit 0). compile, min-vscode, boundaries, limits ("1104 files"),
  exports, markers and settings passed. Unit tests: 3997 tests, 3982 pass, 0 fail, 15 skipped. Security: 94 tests,
  92 pass, 2 skipped. Python: 175 passed. requirements-lint passed. Log: work/gates/conflict-just-check.log.
- Not run: the real-window suites (`just e2e`), which are not part of the fast gate.

## Rebase onto d99d2ef9 (CR-343 after its rebase on main c698ac97)

Seven commits kept with their messages; new head 3c19edc9. REVIEW-015 stays alone in its commit (cfe2a0d0), approved_at 2026-11-17T22:55:00+01:00 untouched.

### 223c08b3 (now cfe2a0d0): StRS-MDOKFSTUDIO-REVIEW-015.md
- Links block, "Derived by" tail: kept 192 with CR-344's new title, dropped TRUST-065 (the commit removes it from derived_by in the frontmatter), kept the "Depends on" BLOCK-058 section that CR-343 generates. Frontmatter merged cleanly.

### 11dd2d3b (now ad4a7bb9)
- SwRS BLOCK-041, derives_from and links: took CR-343's side (no GFM-003, MYST-009; CR-343 moved them to depends_on); CR-344's FMEDIT-001 removal already applied.
- SwRS BLOCK-058, derives_from and links: took CR-343's side (no BLOCK-006, BLOCK-014, GFM-003); CR-344's FMEDIT-008 and REVIEW-015 removals already applied.
- SwRS TRUST-001, derives_from and links: dropped both lines: REVIEW-001 (CR-344 removes it) and TOOLBAR-001 (main's toolbar gardening removed it).

### 73acf33b (now 0c8549eb)
- scripts/marker-baseline.json: commentWrite 9 (CR-344's 10 to 9), markers.ts 15 in both maps (HEAD 24 minus 9 FM markers), editActions 35; findInPreview and package-contract entries stay removed (main's gardening).
- test/integration/realInput/markers.ts: removed the FMEDIT/FMSCHEMA markers (CR-344) and did not restore LIFE-151, LIFE-001 (removed by main); 15 markers.
- test/session/diagReq.links.requirements.test.ts: kept TOOLBAR-077 (main renamed 113) plus FMSCHEMA-073 (CR-344).
- editActions.test.ts is 1499 lines (limit 1500).

### Fast gate (at head 3c19edc9)
- `just requirements-lint`: pass (exit 0; only existing W2 broken-cross-link warnings), log work/gates/rebase3-requirements-lint.log
- `just check`: pass (exit 0), log work/gates/rebase3-check.log
