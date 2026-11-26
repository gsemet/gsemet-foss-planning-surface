# Stack CI: the merge-commit check accepts the forge's chained test merge

## Goal

`just check-no-merge-commits` passes on a pull request above the bottom of a GitHub native stack,
whose checked-out `refs/pull/<n>/merge` is a chain of forge test merges, and still fails for every
merge commit that a branch of the stack really carries (Q2). Without this, any new CI run of such a
pull request is red (`static`, `static-windows`, then the required `checks`), and batch-09's stack
cannot be completed.

## Diagnosis (run 45741461955, PR #516 at 8ce169f)

- `ci-static` called the script with base `origin/main` (`_merge-check-base` read
  `GITHUB_BASE_REF=main`).
- HEAD `921754e3` is the top of a first-parent chain of ten two-parent merges:
  `M0 = Merge 8c6845a (#512 head) into 17b779d5 (main)`, then each `Mk = Merge <head k> into M(k-1)`,
  up to `921754e3 = Merge 8ce169f (#516 head) into 1f63061c`.
- The script only peels one test merge (`HEAD^1` must be an ancestor of the base). Here `HEAD^1`
  is `1f63061c`, another test merge, so it listed all ten merges and failed.
- Checked locally on the ten second parents: each is an ancestor of the next (the stack's
  branches are nested), `17b779d5` is an ancestor of the lowest, and none carries a merge commit
  against `origin/main`.

The base is not the cause: the fix does not touch `_merge-check-base` nor the `justfile` line.

## What changes

### `scripts/check-no-merge-commits.sh`

Replace the single-tip peel (the `head="HEAD^2"` block) with a chain peel:

1. Start at `c = HEAD`. While `c` has exactly two parents (`c^2` resolves, `c^3` does not), record
   `c^2` as a branch head; if `c^1` is an ancestor of the base, the chain is found, stop; else go
   on with `c = c^1`.
2. The chain is accepted only if it was found (the walk reached a first parent that is an ancestor
   of the base) and its recorded heads are nested: each lower head is an ancestor of the next upper
   one. A chain of two or more merges also needs each merge to carry the forge's test-merge
   subject `Merge <sha> into <sha>` (Q5); the Driver first reads the real subjects of the observed
   chain (the log shows `Merge 8ce169f0... into 1f63061c...`, full 40-character SHAs) and, if what
   GitHub writes differs, matches GitHub and says so in the pull request. Then `head` is the top recorded head (`HEAD^2`), whose range `base..head` holds the
   commits of every branch of the chain (the lower ones included).
3. In every other case (the walk meets a commit that is not a two-parent merge, the heads are
   not nested, or a merge of a chain of two or more lacks the subject), `head` stays `HEAD` and every merge in `base..HEAD` is reported, as today.

A single test merge keeps today's behaviour exactly (no subject required, GitLab's merged
results included). The
rest of the script (base and common-commit checks, the passed line with the count from `base..head`,
the failure listing and the rebase command) stays as is. Update the header comment to say the
check peels the forge's test merge, single or chained (native stack), under the two conditions
above. Bash and git only, as today (no network, no forge API); it runs on Linux and in Git for
Windows' bash (`static-windows`).

### `test/build/test_no_merge_commits.py`

Add a helper that builds the observed shape on the throwaway clone: nested stack branches
`s1`..`s3` (each from the one below, `s1` from `origin/main`), then a detached chain
`M1 = merge s1 into origin/main`, `M2 = merge s2 into M1`, `M3 = merge s3 into M2` (`--no-ff`,
subject like the forge's `Merge <sha> into <sha>`). New cases, beside the `test_test_merge_*` ones:

- `test_chained_test_merge_of_a_linear_stack_passes`: passes, and the count is the commits of
  `origin/main..s3`.
- `test_chained_test_merge_passes_against_the_lower_branch_base`: same chain, base `origin/s2`
  (with `s2` pushed): passes (base of the PR's own target, should the forge report it).
- `test_chained_test_merge_fails_when_the_top_branch_carries_a_merge`: `s3` merges `origin/main`
  into itself; fails listing that merge and no chain merge.
- `test_chained_test_merge_fails_when_a_lower_branch_carries_a_merge`: the merge is in `s1`
  (inherited by `s2`, `s3`); fails listing it.
- `test_chain_with_non_nested_heads_reports_every_merge`: the second parents are unrelated
  branches; fails and lists the chain merges (not a stack, no peel).
- `test_nested_chain_with_another_subject_reports_every_merge`: the nested linear chain, one
  merge with a subject other than `Merge <sha> into <sha>`; fails and lists the chain merges.
- `test_chain_not_rooted_on_the_base_reports_every_merge`: the lowest merge's first parent is a
  branch commit not on the base (a branch updated by merge, then merged twice); fails.

The existing tests stay and pass unchanged.

### Text

`.agents/guidelines/pull-request.guidelines.md`, "Updating a branch": one sentence that the check
ignores the forge's test merge, also the chained one of a native stack, and still reports every
merge a branch of the stack carries. No requirement changes: the check is build tooling, no SwRS
covers it and no `@implements_req` marker is involved. The CHANGELOG or release note only if the
project's rules ask for one for a CI script fix.

## Decisions carried from `02-answers.md`

- Q1: a new change in batch-09's stack, directly above CR-501 and below CR-500, CR-504, CR-505,
  CR-507 and CR-509; not a pull request on `main`.
- Q2: the check stays as strict; no skipped job, no `continue-on-error`, no stack exemption; tests
  prove both directions on the chain shape of run 45741461955.
- Q3: proof by the unit tests and by this pull request's own green CI run above the bottom of the
  native stack; holes go in Known gaps.
- Q4: directly above CR-501 (replaces heavy-ci-Q4's "as low as possible" for CR-509, above it);
  up to 10 rounds; context hand-back at 300,000 tokens (order O-131).
- Q5: a chain of two or more merges also requires GitHub's test-merge subject on each merge; a
  single test merge keeps today's behaviour; the Driver checks the real subjects first.

## Out of scope

Any other CI job, `_merge-check-base` and `ci.yml`, loosening or disabling the check, the stack's
other changes.

## CI environment

The `static` (ubuntu) and `static-windows` jobs of `.github/workflows/ci.yml`, full-history
checkout (`fetch-depth: 0`) of `refs/pull/<n>/merge`, `GITHUB_BASE_REF` as the forge sets it. What
the local machine lacks: a real forge chain of test merges (the tests synthesize it) and the value
of `GITHUB_BASE_REF` on a native stack PR (observed `main` once). Only this pull request's first CI
run above the stack's bottom proves the live case.

## Evidence

- `uv run pytest test/build/test_no_merge_commits.py` green, the new cases included (they run the
  shipped script through the shipped `justfile`, at the head under test).
- `just ci-static` locally on the worktree (Windows Git bash) and `just preflight`.
- The pull request's own `static`, `static-windows` and `checks` green above CR-501 in the native
  stack, the log line `check-no-merge-commits: passed (...)`; cite the run id.

## Known gaps

What git alone cannot tell: a branch whose own history is a first-parent chain of two or more
two-parent merges rooted on the base, with nested second parents and each subject written as
`Merge <sha> into <sha>`, checked out at its tip, is read as a forge chain and its merges are not
reported. A single merge keeps today's gap (no subject required). The merges carried inside the
second parents are still all reported.
