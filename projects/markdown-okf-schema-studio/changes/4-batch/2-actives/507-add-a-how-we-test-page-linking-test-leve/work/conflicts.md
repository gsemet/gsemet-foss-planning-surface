# CR-507 rebase on origin/main

- Command that stopped: `git -C <worktree> rebase --onto origin/main 9d7e788a479dec70fd882d295bf0d5e78f4f6b98`
- Base: origin/main `b9a1abd074ab34ba49920448315c86452d80d832`
- CR commit before: `fefaa0a4ecb4df791b304d354b3754e6e92bdf88`
- Rebased head: `fb5fb2fd9501f4fa618d8c3b6233edcdc62b1180`, one commit above origin/main, message unchanged
- Finished with `git -C <worktree> -c core.editor=true rebase --continue`; no merge, no skip, not pushed

## Conflicted hunks

One hunk, in `requirements/tiers/log.md`, under `## 2026-11-26`. Both sides added a new entry at the
top of the date section:

- origin/main: "Grid paste from a header cell: the missed editor reopen did not reproduce (CR-512)"
- CR-507: "How we test page"

Choice: both entries kept whole, under the one date heading. "How we test page" is first (newest
first, and where the CR's patch had put it), then the CR-512 entry, then the CR-505 entries as they
were. No word of either entry changed. The file still starts without a byte-order mark.

No other file conflicted.

## Did the CR's patch change?

Only the log entry's surroundings. `git range-diff` of the old and the new commit differs in the
context lines of the `log.md` hunk alone: the entry now sits above the CR-512 entry instead of above
the CR-505 one. Its added lines are the same, and the commit still touches 17 files, 638 insertions
and 23 deletions.

## Main's new content and docs/how-we-test.md

The tree of the old base `9d7e788a` equals the tree of `b9a1abd0~1`, so the only new content is
`b9a1abd0` (CR-512): the clip paste-spreadsheet-cells and its guideline, one log entry,
SwRS-MDOKFSTUDIO-TABLE-120 verification notes, `test/integration/realInput/{run,tableGridPaste}.ts`
and `test/shared/stressPlan.ts`.

Finding: it makes no statement of `docs/how-we-test.md` false. It adds no CI job, test folder, e2e
group or marker verb, and changes neither the coverage mode nor when a level runs.

Remark, not caused by the rebase: the Stress section says the scenarios of `stressPlan.ts` run again
and again. CR-512 adds `table-grid-paste-header` to `STRESS_ON_DEMAND_SCENARIOS`, which runs only
when named. That list already held two scenarios at the old base, so the sentence is no more and no
less exact than before. The page was not edited.

## Fast gate, at the rebased head

Dependencies were already installed in the worktree (`node_modules`, `.venv`); `just dev` was not
re-run. CR-512 changes no lock file.

- `just --justfile C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-09-CR-507/justfile requirements-lint`:
  pass (exit 0). 0 indexes, 0 projections and 0 coverage files would change; main paths and use case
  diagrams valid. It prints W2 "Broken cross-link" warnings on requirement files.
- `just --justfile C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-09-CR-507/justfile check`:
  pass (exit 0). Node test summaries: 56/56; 5371 pass, 0 fail, 7 skipped of 5378; 116/116. Python
  release tests: 254 passed. The `howWeTest.test.ts` tests passed.
- The worktree was clean after the gate.
- Not run: `just preflight`, `just sphinx-check`, the visual and real VS Code jobs.

Logs: `work/gates/rebase-just-requirements-lint.log`, `work/gates/rebase-just-check.log`.
