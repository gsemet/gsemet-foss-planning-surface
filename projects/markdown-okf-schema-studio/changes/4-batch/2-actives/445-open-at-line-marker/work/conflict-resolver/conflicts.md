# Conflicts: rebase of CR-445 on the CR-444 branch (5 commits, finished)

Hunks and choices (no whole side taken; no text dropped):

1. `requirements/tiers/log.md`, "## 2026-11-21": kept both. CR-445 round-1 entry first (newest on top), then the CR-444 and CR-439 entries unchanged.
2. `test/site/e2eGroups.test.ts` (scenario count, commit 2): kept HEAD's long description, appended ", plus 9 line marker scenarios (CR 445)", total 487 + 9 = 496.
3. `test/visual/scenarioDefinitions1.ts` (imports, commit 2): kept both imports (DELETE_BLOCK_BAR, BLANK_LINES_BLOCK from HEAD, LINE_MARKER); the spreads merged cleanly.
4. `.agents/glossary/common.md` (commit 3): kept HEAD's "Block selection" (with "Delete or Backspace deletes it") and "Delete block button", added CR-445's "Feature introduction", "Jump", "Line marker"; dropped CR-445's older duplicate "Block selection" line (superseded by HEAD's longer one).
5. `test/site/e2eGroups.test.ts` (integration test count, commit 3): HEAD 34 + the open-at-line test (CR 445) = 35, description lists both.

No generated blocks conflicted, so `just requirements-update` was not needed. No BOM added. Nothing committed beyond the rebase, nothing pushed.

Fast gate: `just check` (run in the worktree), result: pass (exit 0). Log: `check.log` in this folder.
