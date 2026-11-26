# CR-510 verification, round 1

Head: 7d35be3430689c4979a58f471d4cd588ecb93fac

Verdict: **VERIFIED** (fourth description pass; see claim 11 and the verdict at the end). All
claims were judged at `7d35be3`; base `5a73b6e`. Claims 1 to 10 come from the first pass at this
same head and base (no move): they were not re-run since, except where claim 11 says so.
`<worktree>` is the CR's worktree, `<scratch>` the CR's `work/scratch`. The earlier passes'
throwaway files and detached worktree are removed; the third and fourth passes made none.
Evidence: `verifier/evidence/before-after.md`.

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

## 11. Posted description, fourth pass: VERIFIED (7d35be3)

State: `git rev-parse HEAD` `7d35be34...`, `git status --porcelain` empty, `git ls-remote origin`
head `7d35be34...` and base branch `5a73b6eb...`, both unchanged. `gh pr view 530 --json ...`:
open, draft, head and base as above. `diff --strip-trailing-cr <(gh pr view 530 --json body --jq
.body) work/pr-body.md`: only one trailing empty line differs.

Only two sentences changed since the third pass judged the whole body. The third pass wrote its
note at 03:56 UTC against the edit of 03:52:51Z; the one later edit is 03:56:49Z
(`gh api graphql ... userContentEdits`). `diff` of those two versions: lines 38 (Impacts) and 50
(Autonomous decisions, third bullet), nothing else. The rest of the body is carried from the third
pass (same head, same text), whose findings on it were all "passed".

Autonomous decisions, third bullet: true.

```text
- The fix ships as a pull request in the current stack, based on the branch of #522, not as a
separate one on the default branch: no pull request below it moves, and every pull request stacked
on it checks out the fixed script.
```

- "based on the branch of #522", not on the default branch: 530's `baseRefName` is #522's
  `headRefName` (`.../cr-501-clip-keyboard-navigation-in-nested-admon`), `baseRefOid` `5a73b6e` =
  #522's head (`gh pr list --state open`).
- "no pull request below it moves": heads 512 `8c6845a`, 513 `1d55649`, 514 `c3c3a57`, 515
  `cae819b`, 517 `d386ff6`, 518 `af4a4aa`, 519 `37ef61b`, 521 `b7518fb`, 522 `5a73b6e`, the same
  as at the third pass, each the base of the next, and 522's the base of 530: the fix needed no
  rebase below it.
- "every pull request stacked on it": a branch stacked on this one contains `7d35be3`, which
  carries the script (claim 1). No open pull request is based on this branch yet; #516 and #529
  are based on #522's branch, beside it, and the bullet claims nothing of them.
- "in the current stack": by its base branch. It is not yet in the forge's stack 528
  (`gh api .../stacks`: 512 to 522 and 516), as Known gaps says ("not linked into the stack yet").
- The decision is `02-answers.md` Q1, taken without the user.

Impacts: true as far as the forge's observed behaviour goes.

```text
For a stacked pull request that contains this fix, in a stack whose branches are rebased on one
another, the check no longer fails on the forge's own test merges (shown on the tests' chains and
on the replayed real chain; a live chain in CI is listed under Known gaps).
```

- "shown on the tests' chains and on the replayed real chain": claims 3, 6 and 7 (carried).
- Live chain listed under Known gaps: the UNVERIFIED bullet is there.
- The stack of the failing run reports the default branch as base: `gh run view 45741461955
  --log-failed`, both static jobs run the script with `"origin/main"`, on PR #516, whose own base
  is a lower branch. With that base the chain's root (the default branch tip the forge merged on)
  is an ancestor of the base, the condition of the walk.

Whole body: `gh api .../pulls/530` full body_html renders the sections and both new sentences
(`#522` links to the pull request). `grep -inE
"gaeta|semet|C:.Users|/home/|/Users/|!\[|<img|STALE|UNVERIFIED"` on the posted body: the one
match is the Known gaps UNVERIFIED bullet. `gh pr checks 530`: `checks`, `report`, `static`,
`static-windows`, `viewer-graph`, `visual` pass, the others skipping (run 45748406898). Review
box: `chantier log CR-510`, `r1 approved at 5a73b6e..., committed as 7d35be34...`. "Verified at"
unchecked as intended.

Observation, not a failure (read in `scripts/check-no-merge-commits.sh`, not probed): if a forge
ever checked out a chain while naming a lower branch as the base, and the default branch had moved
past what that lower branch contains, no first parent of the chain would be an ancestor of that
base, and the merges would be reported. The one observed stack run names the default branch; the
specification keeps the lower-base case as "should the forge report it". The first CI run after
the pull request is linked into the stack shows which base the forge gives.

**VERIFIED** (7d35be3).
