# Forbid merge commits in pull request branches

Short name: `no-merge-commits`. Origin: verbal (owner, batch-08 retro, 2026-11-22). No issue.

A branch under review gets updated only by rebase, never by merge. The pull-request guideline says
so in forge-neutral words, and a git-only static check fails any branch whose commits include a
merge commit. It works the same for a GitHub pull request, a GitLab merge request and a local run.

## Goal

The repository merges by rebase only, and history is linear (constitution, section 4). In
batch-07, GitHub's plain "Update branch" button put a merge commit into a pull request branch
twice (#458, #462), and each one cost a rebase round. After this change:

- the pull-request guideline forbids updating a branch by merge, whichever forge hosts it;
- `ci-static` fails as soon as a branch carries a merge commit, before any review time is spent,
  and its message names the merge commits and the command that removes them.

Owner's standing word (02-answers.md): every rule, word and check is forge-neutral. "Pull request
or merge request", GitHub or GitLab. A GitHub button is named only as an example.

## What changes

### 1. The pull-request guideline (`.agents/guidelines/pull-request.guidelines.md`)

Add a section `## Updating a branch`, after "Draft until mergeable" and before "GitHub issues".
Its content, in the guideline's style (the Driver writes the final wording):

- A pull request or merge request branch is updated only by rebase, never by merge: history is
  linear (constitution, section 4).
- Two ways are allowed: the forge's rebase action (for example GitHub's "Update with rebase", or
  GitLab's "Rebase" on a merge request), or a local rebase on the base branch followed by
  `git push --force-with-lease`.
- Any action that merges the base into the branch is forbidden. For example, GitHub's plain
  "Update branch" button or a local `git merge origin/main`.
- If you cannot rebase the branch yourself, ask whoever owns it to rebase it.
- `ci-static` enforces this rule with `just check-no-merge-commits` (section 2). A red check is fixed
  by the rebase the check prints.

Words to follow: constitution section 8 says a project guideline names no process role. So the
request's "asking the Driver to rebase" becomes "ask whoever owns the branch". The guideline does
not link the chantier CR (section "Out of scope").

### 2. The check: `scripts/check-no-merge-commits.sh` and `just check-no-merge-commits`

A new bash script, `scripts/check-no-merge-commits.sh`. It uses only git: no Node, no Python, no
network, no forge API. A new justfile recipe runs it:

```just
# Fail when the commits of the branch (BASE..HEAD) include a merge commit; the branch is updated by rebase only.
check-no-merge-commits BASE="origin/main":
    bash scripts/check-no-merge-commits.sh "{{ BASE }}"
```

The script's behaviour:

1. It takes one argument, the base ref (`origin/main` by default, from the recipe). It also works
   when the base is the branch below in a stack, for example `origin/change-requests/123-foo`.
2. It fails with a clear message (exit 1) when the base ref does not resolve
   (`git rev-parse --verify --quiet "<base>^{commit}"`) or when `git merge-base <base> HEAD`
   finds no common commit. The message names the cause and the fix: fetch the base and the full
   history (locally `git fetch origin`; in CI, a full-history checkout: `fetch-depth: 0` in
   GitHub's `actions/checkout`, `GIT_DEPTH: 0` on GitLab).
3. The forge's test merge. On a pull request event, GitHub's `actions/checkout` checks out
   `refs/pull/<n>/merge` by default. That is a synthetic merge commit of the branch into the base.
   A GitLab "merged results" pipeline does the same. That commit is not part of the branch and must
   not fail the check. Rule: when `HEAD` is a merge commit and its first parent is an ancestor of
   the base (`git merge-base --is-ancestor HEAD^1 <base>`), the script checks `HEAD^2` (the
   branch's real head) in place of `HEAD`. This rule applies only to the tip, never to a commit
   below it. A merge made by "Update branch" or a local `git merge origin/main` has the branch's
   own head as its first parent, so the rule never hides it. The "is an ancestor" test, rather than
   "equals the base tip", keeps the rule correct when the base moved between the forge's merge and
   the fetch.
4. It lists the merges with `git rev-list --merges <base>..<head>`. When there are none, it prints
   `check-no-merge-commits: passed (<n> commits since <base>, no merge commit)` and exits 0.
5. Otherwise it exits 1 and prints, on stderr:
   - one line per merge commit: `git log --merges --format='%h %s' <base>..<head>`;
   - the reason: the repository merges by rebase only, so a branch is updated by rebase, never by
     merge;
   - the command that removes the merges. For a base `origin/<branch>`:
     `git fetch origin && git rebase origin/<branch> && git push --force-with-lease`. A plain
     `git rebase` without `--rebase-merges` linearizes the merges away. For a base without an
     `origin/` prefix, the same command with the base as given and no fetch.
   - the last line: `check-no-merge-commits: FAILED`.

### 3. `ci-static` runs the check with the target branch from the CI

`ci-static` in the `justfile` runs `just check-no-merge-commits "$base"` as the first step of its
chain, before `just check`. A history problem then fails fast and cheaply. `$base` is computed
in the recipe, forge-neutrally:

```bash
target="${GITHUB_BASE_REF:-${CI_MERGE_REQUEST_TARGET_BRANCH_NAME:-}}"
base="origin/${target:-main}"
```

- On a GitHub pull request, `GITHUB_BASE_REF` holds the target branch name, the branch below for a
  stacked PR.
- On a GitLab merge request pipeline, `CI_MERGE_REQUEST_TARGET_BRANCH_NAME` holds it.
- Otherwise (a GitHub push to `main`, where `GITHUB_BASE_REF` is set but empty, a
  `workflow_dispatch`, or a local run), the base is `origin/main`.

The check is not added to `just check`, as 02-answers.md says ("in ci-static"). `just preflight`
runs it through `ci-static`, on Windows too, against `origin/main`.

Update the comment above `ci-static` so it names the merge-commit check. Update the list of
checks in AGENTS.md, under "Main targets", with
`just check-no-merge-commits [BASE]` (merge commits in the branch, base `origin/main` by default).
Update the line of CONTRIBUTING.md (line 275) that lists what `ci-static` runs in the same way.

### 4. The CI workflow (`.github/workflows/ci.yml`)

In the `static` and `static-windows` jobs, the `actions/checkout` step gets `fetch-depth: 0`, next
to `lfs: true`. Without it, the checkout is a depth-1 clone of the test merge. That clone has no
`origin/<base>` ref, no parents of `HEAD` and no merge base, so the check would fail on step 2.
This is a checkout setting, allowed by rule 3 of `ci.guidelines.md`. The workflow keeps its two
targets per job (rule 1): no new step and no inline script.

The other jobs (visual, viewer-graph, integration, report, gallery) do not change.

GitLab: the repository has no `.gitlab-ci.yml`, and this CR adds none. The script, the recipe and
the base computation already read GitLab's variable. A future GitLab pipeline sets `GIT_DEPTH: 0`
on its static job. The failure message of step 2 says so.

### 5. Tests (`test/build/test_no_merge_commits.py`, new)

A new pytest file. `test_workflows.py` is already 1 074 lines, so the new tests do not go there.
Add it to the pytest list of the `release-tests` recipe, so `just check` runs it. Each test builds
a throwaway git repository in `tmp_path`: a bare `origin` and a clone, with commits made by
`git commit --allow-empty` or small files, and a fixed `user.name`/`user.email` given with `-c`.
It then runs the shipped recipe from the repository's own justfile at the head under test:
`just --justfile <ROOT>/justfile --working-directory <tmp clone> check-no-merge-commits <base>`
(the same pattern as `_just_run` in `test_workflows.py`). The script is read from
`<ROOT>/scripts/`, never copied. Use the same Windows `bash` lookup as `_bash()` when a test calls
bash directly.

Cases:

1. Linear branch (two commits on `origin/main`): exit 0, output contains `passed`.
2. Branch updated by merge (a commit on the branch, a commit on main, then
   `git merge --no-ff origin/main` on the branch, which is what "Update branch" produces): exit 1.
   Stderr names the merge commit's short hash and subject, contains
   `git rebase origin/main` and `--force-with-lease`, and ends with `FAILED`.
3. The default base: the same repository as case 2, the recipe run with no argument: exit 1 (the
   default is `origin/main`).
4. The forge's test merge of a linear branch (`HEAD` is `git merge --no-ff <branch>` made on top
   of `origin/main`, detached): exit 0.
5. The forge's test merge when main moved after it (`origin/main` has one more commit than the
   test merge's first parent): exit 0.
6. The forge's test merge of a branch that carries a merge (case 2's branch, merged on top of
   main): exit 1, naming the inner merge commit.
7. A stacked base: the branch is based on `origin/lower`, which carries its own commits. Run with
   `origin/lower`: exit 0, and the count counts only the branch's own commits.
8. A base that does not resolve (`origin/nope`): exit 1, the message names the base and the fetch
   to run.
9. Wiring, read from the shipped files: `ci-static` in the repository's `justfile` runs
   `check-no-merge-commits` before `just check`, and computes the base from `GITHUB_BASE_REF`, then
   `CI_MERGE_REQUEST_TARGET_BRANCH_NAME`, then `main`. Prove it by running the shipped
   `ci-static` base computation: either factor it into a private recipe
   (`_merge-check-base`, which prints the base) and run it with each environment (GitHub
   `GITHUB_BASE_REF=lower`, GitHub push `GITHUB_BASE_REF=`, GitLab
   `CI_MERGE_REQUEST_TARGET_BRANCH_NAME=lower`, nothing set), or check the recipe text. Running it
   is preferred.
10. Workflow, read from the shipped `.github/workflows/ci.yml` with the existing `_jobs` split:
    the checkout step of `static` and of `static-windows` carries `fetch-depth: 0`.
11. Guideline, read from the shipped `.agents/guidelines/pull-request.guidelines.md`: it has the
    `## Updating a branch` section, mentions `--force-with-lease` and `check-no-merge-commits`, and
    names no process role (no "Driver").

## Decisions of 02-answers.md, carried

- Q1, where the rule lives: in the project, forge-neutral, in the pull-request guideline (rebase
  only: the forge's rebase action, or a local rebase and `--force-with-lease`, never a merge;
  GitHub's plain "Update branch" as an example). See section 1. The chantier side is a separate CR
  (section "Out of scope").
- Q2, the check: a git-only script run by the justfile, `just check-no-merge-commits <base>`, based
  on `git rev-list --merges <base>..HEAD`, run in `ci-static`. It fails naming the merge commits
  and the rebase command. The CI passes the target branch (`GITHUB_BASE_REF`,
  `CI_MERGE_REQUEST_TARGET_BRANCH_NAME`), and locally the base defaults to `origin/main`. See
  sections 2 and 3.
- Q3: specified for the running batch (batch-09). No spec critic (small, low risk).

Added by this specification as needed for the Q2 decision to work, not as new behaviour:
`fetch-depth: 0` (section 4) and the test-merge rule (section 2, step 3). Without them,
`<base>..HEAD` cannot run on a GitHub pull request checkout. See the open questions.

## Out of scope

- The chantier side, so that Drivers and conflict-resolvers never merge the base into a branch: a
  separate CR in the chantier project.
- A `.gitlab-ci.yml` or any GitLab pipeline.
- Branch protection or forge settings (for example turning off GitHub's "Update branch" button or
  requiring linear history). They are repository settings, not files of this repository.
- Pushes to `main`: they are not filtered beyond the check's normal run (empty range, passes).
- No SwRS or requirements change: the check guards the delivery process, not a behaviour of the
  extension in `src/`. No line in `requirements/tiers/log.md`.
- No `CHANGELOG.md` line: `## Unreleased` lists what extension users notice, and this change is
  for contributors only.
- Commit type: `ci` (no scope), per `git-commit-allowed-scopes.md`.

## Host and default matrix

The base and the checked head depend on the host and on whether the base is the default or comes
from the CI. One line per cell, each covered by the test named:

- GitHub pull request to `main` (`GITHUB_BASE_REF=main`, `HEAD` = test merge): base
  `origin/main`, head `HEAD^2`. Tests 4, 5, 9.
- GitHub stacked pull request (`GITHUB_BASE_REF=<lower branch>`, `HEAD` = test merge): base
  `origin/<lower>`, head `HEAD^2`. Tests 7, 9.
- GitHub push to `main` (`GITHUB_BASE_REF` empty): base `origin/main` (default), empty range,
  passes. Test 9 (base); test 1 covers the passing path.
- GitHub `workflow_dispatch` on a branch: base `origin/main` (default), head `HEAD`. Test 9, test 3.
- GitLab merge request pipeline (`CI_MERGE_REQUEST_TARGET_BRANCH_NAME=<target>`, `HEAD` = branch
  head): base `origin/<target>`, head `HEAD`. Test 9 (base), tests 1, 2.
- GitLab merged-results pipeline (`HEAD` = test merge): base `origin/<target>`, head `HEAD^2`.
  Tests 4, 6.
- Local run, `just check-no-merge-commits` without argument, or `just preflight`, on Linux,
  macOS or Windows (Git for Windows' bash): base `origin/main` (default). Test 3; the `just
  preflight` run on Windows below.
- Local run with an explicit base: that base. Tests 2, 7, 8.

## CI environment

The `static` job runs on `ubuntu-latest` and `static-windows` on `windows-latest`. Both run Git for
Windows' bash for the just recipes on Windows. Compared with a local worktree, the CI checkout
lacks these things:

- **Full history and the base ref.** Today the checkout has depth 1 and no `origin/<base>`. After
  this change it has `fetch-depth: 0`: every branch of the repository under `refs/remotes/origin/`
  and the whole history (about 730 commits on `main` today, none of them a merge, plus LFS objects
  pulled as before).
- **What `HEAD` is.** In CI, `HEAD` is GitHub's synthetic `refs/pull/<n>/merge` commit. Locally it
  is the branch head.
- **Environment variables.** CI has `GITHUB_BASE_REF`. A local run has none of the CI variables.
- No credentials or network are needed by the check. It runs offline once the checkout is done.

Evidence before the push (each on the Driver's worktree):

- `just check-no-merge-commits` passes on the change's own branch (a linear branch on
  `origin/main`).
- `just release-tests` (or `just check`) runs `test/build/test_no_merge_commits.py` green. It covers
  the test-merge cases, the stacked base and the base computation for each CI environment, all
  simulated with local git repositories and environment variables.
- `just preflight` passes (on Windows, the static stage, which now includes the check).

Only the first CI run can prove these:

- That `actions/checkout` with `fetch-depth: 0` on a `pull_request` event gives `origin/main` and
  a test merge whose first parent is an ancestor of it. The check passes on the CR's own pull
  request in both `static` and `static-windows`, with a `passed` line in the log naming
  `origin/main`.
- The extra checkout time of the full history in both static jobs. The job budgets (15 and 20
  minutes) are expected to hold.
- For a stacked PR, `origin/<lower branch>` is present. This is proved by the first stacked PR that
  runs after the merge, not by this CR's own run unless it sits in a stack.
- The GitLab rows are proved only by local simulation (tests 4, 6, 9), as there is no GitLab
  pipeline.

## Scenario steps (Verifier)

1. On the pushed head, read the `static` and `static-windows` logs of the pull request run. Each
   shows `check-no-merge-commits: passed (... since origin/main ...)` before the `just check`
   output.
2. In a scratch clone of the branch, run `git merge --no-ff origin/main` after any commit that
   main has and the branch has not (or an empty commit on a scratch main). Then run
   `just check-no-merge-commits`: it exits 1, names the merge commit and prints
   `git fetch origin && git rebase origin/main && git push --force-with-lease`. Run the printed
   rebase (without the push): the check passes again.
3. Read the new `## Updating a branch` section of the pull-request guideline: it is forge-neutral,
   names GitHub's "Update branch" only as an example and names no process role.

## Open questions

None. Answered by the owner (02-answers.md, no-merge-commits-Q4 and Q5):

1. Full history with `fetch-depth: 0` on both static jobs and the tip rule (section 2, step 3;
   section 4) are confirmed; the head checkout is not used.
2. The edge of the tip rule (a branch with no commit of its own, the base merged in locally,
   passes) is accepted.
