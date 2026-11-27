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

# CR-507 rebase on the CR below in the stack

- Command that stopped: `git -C <worktree> rebase --onto a5550c32100a24e646efdf293db93cdac30e3cba b9a1abd074ab34ba49920448315c86452d80d832`
- Base: `a5550c32100a24e646efdf293db93cdac30e3cba` (7 commits above `b9a1abd0`)
- CR commit before: `fb5fb2fd9501f4fa618d8c3b6233edcdc62b1180`
- Rebased head: `bde4bd58938e334a6ccbd076c56901b7c5991c88`, one commit above the base, message unchanged
- Finished with `git -C <worktree> -c core.editor=true rebase --continue`; no merge, no skip, not pushed

## Conflicted hunks

One hunk, in `requirements/tiers/log.md`, under `## 2026-11-26`. Both sides added entries at the top
of the date section:

- base: "Enter and click in an admonition open the selected element" (CR-514), then the CR-513 and
  CR-511 entries
- CR-507: "How we test page"

Choice: all entries kept whole, under the one date heading. "How we test page" is first (newest first,
and where the CR's patch had put it), then the base's entries in their order. No word of any entry
changed; against the base the file has 4 added lines and no removed line. It still starts without a
byte-order mark.

No other file conflicted.

## Merged by Git alone

- `.agents/guidelines/ci.guidelines.md`: the CR's rule 16 stays after rule 15. The base added no rule
  (it reworded item 4 of "Recovering from a red heavy job on a release push"), so the numbers run 1 to
  16 with no duplicate. The page's two references to rule 14 still point to the release tag rule.
- `CONTRIBUTING.md`: the CR's one sentence opens "Checks"; the base's CR-515 text is kept below it
  and in the other sections.
- `git range-diff` of the old and the new commit differs only in the context lines of the `log.md`
  hunk. The commit still touches 17 files, 638 insertions and 23 deletions.

## Statements the base makes false (reported, nothing edited)

All come from CR-515 (`2fb89df9`): the visual stage now runs in the jobs `visual`
(`just ci-visual 1`, then the breakout tests) and `visual-2` (`just ci-visual 2`).

`docs/how-we-test.md`:

- Line 53, table row "Simulated bench": the CI jobs read `visual`, `viewer-graph`; `visual-2` is
  missing.
- Line 130: "CI job: `visual` and `viewer-graph`, on every pull request." `visual-2` is missing.
- Line 254: "on a pull request: `static`, `static-windows`, `visual` and `viewer-graph`" omits
  `visual-2`.
- Lines 261-262: "`visual` and `viewer-graph` run only the Chromium tests of the simulated bench."
  `visual-2` runs part of them too (true as far as it goes, incomplete).
- Lines 271-272: "`checks`: the required status, which sums `static`, `static-windows`, `visual`,
  `viewer-graph` and `report`". False: `checks` also needs `visual-2`.

`images/how-we-test/test-levels.svg` (the drift test does not read the job names of the picture):

- Line 3, `<desc>`: "the simulated bench in the jobs visual and viewer-graph" omits `visual-2`.
- Line 78, the "Simulated bench" box: "visual, viewer-graph" omits `visual-2`.

Still true: line 128 (`just ci-visual` with no part runs the visual scenarios and the breakout tests)
and lines 264-265 (the table width checks run in the `visual` job, on Linux).

Remark, not false: lines 114-115 list the "other repository checks" of the Python tests of
`test/build` without the new `test_visual_parts.py` (the list already left out others).

Other files of the CR's patch: no statement found false. The other commits of the base (CR-511,
CR-513, CR-514) add no CI job, test folder, e2e group, marker verb or lint command.

## Fast gate, at the rebased head

Dependencies were already installed in the worktree; `just dev` was not re-run. The base changes no
`package.json`, `package-lock.json` or `uv.lock`.

- `just --justfile C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-09-CR-507/justfile requirements-lint`:
  pass (exit 0). It prints W2 "Broken cross-link" warnings on requirement files.
- `just --justfile C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-09-CR-507/justfile check`:
  FAIL (exit 1), in recipe `unit`: 5443 tests, 5435 pass, 1 fail, 7 skipped. The clip kit tests
  before it passed (56/56). The one failure is the expected one.
- `check` stops at `unit`, so the targets after it were run on their own:
  `just --justfile C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-09-CR-507/justfile contracts security release-tests release-notes-check`:
  pass (exit 0). Contracts: 0 tests; security: 116/116; release tests: 296 passed; release notes ok.
  `requirements-lint`, the last target of `check`, is the first bullet.
- The worktree was clean after the gate.
- Not run: `just preflight`, `just sphinx-check`, `just audit`, the visual and real VS Code jobs.

The only failing assertion, verbatim:

```
test at out\test\site\howWeTest.test.js:130:25
✖ How we test names every CI job (60.1383ms)
  AssertionError [ERR_ASSERTION]: Expected values to be strictly deep-equal:
  + actual - expected
  
  + [
  +   'visual-2'
  + ]
  - []
  
      at TestContext.<anonymous> (C:\Users\gaeta\Projets\markdown-okf-schema-studio.worktrees\batch-09-CR-507\out\test\site\howWeTest.test.js:132:22)
      at Test.runInAsyncScope (node:async_hooks:227:14)
      at Test.run (node:internal/test_runner/test:1402:25)
      at Test.processPendingSubtests (node:internal/test_runner/test:974:18)
      at Test.postRun (node:internal/test_runner/test:1542:19)
      at Test.run (node:internal/test_runner/test:1467:12)
      at async Test.processPendingSubtests (node:internal/test_runner/test:974:7) {
    generatedMessage: true,
    code: 'ERR_ASSERTION',
    actual: [ 'visual-2' ],
    expected: [],
    operator: 'deepStrictEqual',
    diff: 'simple'
  }
```

Logs: `work/gates/rebase2-just-requirements-lint.log`, `work/gates/rebase2-just-check.log`,
`work/gates/rebase2-just-check-remaining.log`.
