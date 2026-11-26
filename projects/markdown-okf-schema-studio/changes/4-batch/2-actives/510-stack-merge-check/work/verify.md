# CR-510 verification, round 1

Head: 7d35be3430689c4979a58f471d4cd588ecb93fac

Verdict: **NOT VERIFIED**. One failure, in the posted description (claim 11, second description
pass). Every claim about the code, tests, gates and CI is VERIFIED. All claims were judged at
`7d35be3`; base `5a73b6e`. Claims 1 to 10 come from the first pass at this same head and base
(no move): they were not re-run in the second pass, except where claim 11 says so.
`<worktree>` is the CR's worktree, `<scratch>` the CR's `work/scratch`. My throwaway files and my
detached worktree are removed. Evidence: `verifier/evidence/before-after.md`.

## 1. Head, diff and scope: VERIFIED (7d35be3)

`git rev-parse HEAD`, `git status --porcelain`, `git ls-remote origin ...`:
head `7d35be34...`, tree clean, remote branch at the head, remote base branch at `5a73b6eb...`.
`git diff --stat 5a73b6e HEAD`:

```text
 .agents/guidelines/pull-request.guidelines.md |   3 +-
 scripts/check-no-merge-commits.sh             |  37 ++++++++--
 test/build/test_no_merge_commits.py           | 100 ++++++++++++++++++++++++++
 3 files changed, 132 insertions(+), 8 deletions(-)
```

`git diff --quiet 5a73b6e HEAD -- justfile .github pyproject.toml uv.lock` exit 0
(`_merge-check-base` and `ci.yml` unchanged, as the specification asks).
Commit: one `ci:` commit, subject without scope, `Assisted-by:` trailer, no merge.

## 2. Script and guideline as specified: VERIFIED (7d35be3)

`git diff 5a73b6e HEAD`: walk over exactly-two-parent merges down the first parents; peel to
`HEAD^2` only when a first parent is an ancestor of the base, the second parents are nested, and
(two merges or more) each subject matches `^Merge [0-9a-f]{40} into [0-9a-f]{40}$`; else `HEAD`.
Header comment updated. Rest of the script unchanged. Git and bash only. Guideline "Updating a
branch" gains the one sentence; no `src/` change, so no requirement or marker.

## 3. Tests at the head: VERIFIED (7d35be3)

`uv run pytest test/build/test_no_merge_commits.py -v -p no:cacheprovider`:
`19 passed in 75.88s`, the seven specified cases by name included
(`verifier/evidence/tests-after.txt`).

## 4. New cases against the previous script: VERIFIED (7d35be3 tests, 5a73b6e script)

Detached worktree of `5a73b6e` under `<scratch>`, head's test file over it:
`4 failed, 15 passed`. Failed: `..._of_a_linear_stack_passes`,
`..._against_the_lower_branch_base`, `..._top_branch_carries_a_merge`,
`..._a_lower_branch_carries_a_merge` (the last two on `assert not [<chain merges>]`, after the
carried merge was found: the old script lists both). The 12 earlier cases and 3 guard cases pass.

## 5. The 3 guard cases catch a looser check: VERIFIED (7d35be3)

Head script copied to `<scratch>`, one condition dropped at a time, `pytest -k chain`:

```text
=== mutation: no nested-heads condition (changed lines: 1)
FAILED test_chain_with_non_nested_heads_reports_every_merge
1 failed, 6 passed
=== mutation: no forge-subject condition (changed lines: 1)
FAILED test_nested_chain_with_another_subject_reports_every_merge
1 failed, 6 passed
=== mutation: no rooted-on-base condition (changed lines: 1)
FAILED test_chain_with_non_nested_heads_reports_every_merge
FAILED test_nested_chain_with_another_subject_reports_every_merge
FAILED test_chain_not_rooted_on_the_base_reports_every_merge
3 failed, 4 passed
```

## 6. The real forge chain of run 45741461955: VERIFIED (7d35be3)

Throwaway clone under `<scratch>`, `git fetch <repository URL> refs/pull/516/merge`:
`921754e3`, a first-parent chain of ten two-parent merges down to `17b779d5` (main), every
subject `Merge <40-hex second parent> into <40-hex first parent>`. Previous script: lists the
ten merges, exit 1. Head script: `passed (24 commits since origin/main, no merge commit)`,
exit 0; `git rev-list --merges --count origin/main..HEAD^2` = 0
(`verifier/evidence/real-chain.txt`). This reproduces the Driver's replay with the real objects.

## 7. This head linked above 5a73b6e, both directions: VERIFIED (7d35be3, local only)

Same clone: `git merge-tree --write-tree` + `git commit-tree` of `7d35be3` onto the forge's
`1f63061c` with the forge's subject; the script taken from the merged tree has the head's blob
(`f20b48b6` both).

```text
chain merges from top down to main: 10
--- base origin/main: passed (21 commits since origin/main, no merge commit)  exit 0
--- base origin/cr501: passed (1 commits since origin/cr501, no merge commit)  exit 0
== a branch above 5a73b6e carries a merge of a moved main (same chain)
91bbbc36 Merge branch main into the probe branch
check-no-merge-commits: FAILED  exit 1        (only that merge listed, no chain merge)
```

A merge carried by a lower branch of a chain: `..._a_lower_branch_carries_a_merge` (claim 3).

## 8. Local gate: VERIFIED (7d35be3, Driver's log judged, not re-run)

`work/gates/preflight-7d35be3.log`, first line
`CR-510 just preflight at 7d35be3430689c4979a58f471d4cd588ecb93fac branch ...`; node tests
`fail 0`; line 5713 `test_no_merge_commits.py ...................`; `212 passed`; Sphinx
`4 passed`; `ci-static: passed`; Windows skips the other stages; last line
`preflight exit=0 head=7d35be34...`. No doubt raised. No `chantier gate` pass is recorded:
`handoff` says `none in chantier.yaml`.

## 9. CI at the head: VERIFIED (7d35be3)

`gh pr checks 530`: `checks`, `report`, `static`, `static-windows`, `viewer-graph`, `visual`
pass; `gallery`, `integration`, `pages`, `release`, `release-check`, `stress`, `tag-release`,
`toc-loop` skipping. `gh run view 45748406898`: head `7d35be34...`, `pull_request`, attempt 1,
success. `work/ci-45748406898.log`: `HEAD is now at 9d814b5f Merge 7d35be34... into
5a73b6eb...` (single test merge) and, in both static jobs, `check-no-merge-commits: passed
(1 commits since origin/chantier/batch-09/cr-501-..., no merge commit)`.
`gh api .../stacks`: open stack 528 holds 512..522 and 516, not 530. The live chain proof in CI
(specification, Evidence) is therefore not captured; the description says so (Known gaps,
UNVERIFIED).

## 10. Known gaps and other body statements: VERIFIED (7d35be3)

Probe in a scratch repository, previous / head script:

```text
octopus at the tip, first parent on the base:      previous exit 0 / head exit 1 (listed)
own nested two-merge chain, forge-form subjects
  with identifiers that are not the parents:       previous exit 1 / head exit 0
single merge at the tip, any subject:              previous exit 0 / head exit 0
lower branch moved, upper not rebased:             previous exit 1 / head exit 1
```

- No test builds an octopus: the test file only merges one branch at a time.
- Lower pull requests keep the old script (the file changes only in `7d35be3`, above them), and
  the old script fails any chain of two or more (claims 4, 6).
- Deliverables table (as posted at the first pass, 4 rows): rows 1 to 4 match claims 3, 4, 6. Diagram matches the code and renders
  (headless Mermaid render looked at). Changes matches the three files; seven cases, six on
  stack branches, one on unrelated branches.
- Subjects of the failing run: claim 6. "212 build tests, 4 Sphinx": claim 8. CI box: claim 9.
- `Review: approved at 7d35be3`: `chantier log CR-510`, `r1 approved at 5a73b6e..., committed as
  7d35be3430689c4979a58f471d4cd588ecb93fac`.
- Changelog and requirements boxes: `ci` change, no `src/` change (claim 1).
- The wording of the UNVERIFIED bullet changed since this claim was judged: see claim 11.

## 11. Posted description, second pass: NOT VERIFIED (7d35be3)

State: `git rev-parse HEAD` `7d35be34...`, `git status --porcelain` empty, `git ls-remote` head and
base unchanged. `diff --strip-trailing-cr <(gh pr view 530 --json body --jq .body) work/pr-body.md`:
only one trailing empty line differs. `gh api .../pulls/530 --jq .body_html`: sections, table,
task list and Mermaid block render. `grep -inE "gaeta|C:.Users|/home/|/Users/|!\[|<img"` on the
posted body: exit 1 (no image, no username or home path). `gh pr checks 530`: same results as
claim 9; `gh run list --commit 7d35be3...`: the one run 45748406898, success. `gh api .../stacks`:
stack 528 still without 530.

Passed:

- The failure of the first pass is fixed: the first Test plan proof reads `19 passed at 7d35be3`
  and `on the previous script (5a73b6e)` (`tests-after.txt`, `tests-before.txt`).
- Real-chain row and caption: SHAs named; ten merges listed and exit 1 before, `passed (24
  commits since origin/main, no merge commit)` after (`real-chain.txt`).
- New Evidence item: SHAs named; first sentence matches `real-chain.txt` and `before-after.md`,
  second matches claim 7 (`1f63061c` is the chain's merge of `5a73b6e`; both bases pass; a merge
  carried by a branch above is still listed).
- "Verified at" unchecked, as intended before the verdict. Review and CI boxes: claim 10, claim 9.

Failure: one sentence added to the Known gaps UNVERIFIED bullet is contradicted by the CI log.

```text
- **UNVERIFIED:** the check passing on a real chain in CI, [...] It was run locally only, on the
  tests' chains and on the failing run's real chain. [...]
```

`grep -nE "test_no_merge_commits|passed in" work/ci-45748406898.log` (run at `7d35be3`):

```text
6064: static-windows  uv run ... pytest ... test/build/test_no_merge_commits.py ...
6079: static-windows  test\build\test_no_merge_commits.py ...................   [ 94%]
6082: static-windows  212 passed in 55.15s
13377: static         uv run ... pytest ... test/build/test_no_merge_commits.py ...
13392: static         test/build/test_no_merge_commits.py ...................   [ 94%]
13395: static         212 passed in 12.49s
```

The check ran on the tests' chains in CI too, on Linux and Windows; only the real-chain replays
were local only. The gap itself (no real forge chain in CI) is correct and stays.
Fix, in `pr-body.md` and on the pull request, for that sentence: "Its tests run it on the chains
they build, locally and in the CI run at `7d35be3`; the failing run's real chain was replayed
locally only." Then a description-only pass. No code change needed.
