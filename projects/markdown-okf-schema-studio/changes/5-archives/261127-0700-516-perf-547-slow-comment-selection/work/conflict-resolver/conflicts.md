# CR-516: conflict in meaning after the rebase onto origin/main (1953eaa)

Head: 96331f0ffc538dea3cb5b887cc5e1e8df6fbfe58 (rebase already done, textually clean; no rebase run
here, no textual hunk).

## Hunk 1: `docs/how-we-test.md`, "Repro tools and probes"

- Base intent: the page names every CI job (CI guidelines rule 16, `test/site/howWeTest.test.ts`).
- Branch intent: `ci.yml` gains the on-demand job `perf-547`.
- Choice: one addition to the section, beside `toc-loop`: job, `just ci-perf-547`, what it measures,
  no limit, manual dispatch with `perf_547=true`, never gates a merge. "Neither has a marker" became
  "None of these jobs and probes has a marker", since the paragraph now names two jobs.
- Not added to the table or the diagram: both list the test levels only; `perf-547` sets no limit and
  proves no requirement, and `toc-loop` is in neither. Not added to "These jobs run no test level",
  which likewise leaves `toc-loop` to this section.

## Other base changes read against the branch's lines (no edit)

- `.agents/guidelines/ci.guidelines.md`: base adds rule 16; consistent with the branch's `perf-547`
  lines in rule 13 (on demand, not in `checks`), and satisfied by hunk 1.
- `CONTRIBUTING.md`: base adds the link to How we test under "Checks"; consistent with the branch's
  `ci-perf-547` section and the 13-minute step line.

## State: staged, NOT committed

The brief asked for a commit; the role card says "Never: commit, push, create a worktree or run
`git stash`". The card was followed. Staged: `docs/how-we-test.md` only; staged tree
`fcb2ae2c0c24ee58b3e136d66914df9cad924d6c`. Commit message prepared in `commit-message.txt`
(this folder), project format.

## Fast gate

`fnm exec -- just check`, in the worktree, on HEAD 96331f0 plus the staged change (not on a committed
head): exit 0. Log: `../gates/conflict-resolver-check.log` (TypeScript tests 5515, pass 5508, fail 0,
skipped 7, with the How we test drift tests passing; release tests 298 passed). After the run, the
worktree held the staged change only. `just dev` not run: the base changes touch no lock file.
