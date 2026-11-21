# Windows long paths in `just dev`, no sign-off in CONTRIBUTING release

Two small fixes merged into one CR by the owner (2026-11-21): on Windows, `just dev` turns on
`core.longpaths` for the repository so a base checkout or a new worktree never fails with
"Filename too long"; and CONTRIBUTING.md "How to Release" stops signing off the version commit,
as the release guideline already says. No tracker issue (verbal, from the batch-06 retro and the
CR-434 release Driver).

## Goal

- A Verifier, a Driver or a contributor on Windows can always check out the base (`origin/main`)
  or add a worktree of this repository: the batch-06 retro counted five blocked checkouts
  (CR-348, CR-350, CR-427, CR-431, CR-432), all `git worktree add`, whose fail-before claims went
  into PR bodies as UNVERIFIED. The fix lives in `just dev`, the command every new checkout or
  worktree already runs first, so nobody has to remember a manual step (owner, lp-Q1: "just dev le
  règle").
- Whoever follows CONTRIBUTING.md to release gets a version commit with no `Signed-off-by`
  trailer, the same as `.agents/guidelines/release-process.guidelines.md` step 5 (line 79: "The
  version commit carries no `Signed-off-by` trailer: amend it without `-s`.") and as
  `just bump-version` already produces (SwRS-MDOKFSTUDIO-CORE-075, `test/build/test_release.py`).
  The owner put it in this CR (lp-Q2: "Avec longpaths").

## Decisions carried from the grill (`02-answers.md`)

- lp-Q1: on Windows, `just dev` runs `git config core.longpaths true` in the repository, so every
  new worktree is covered; AGENTS.md (Setup) and the local-worktree guideline say so.
- lp-Q2: same CR. CONTRIBUTING "How to Release" matches release-process.guidelines.md: the version
  commit carries no `Signed-off-by` (today line 629 runs
  `git commit --amend --no-edit -s CHANGELOG.md`).
- lp-Q3: the Evidence also runs `just dev` and one unit test inside a base worktree whose paths pass
  260 characters (the CR's `work/scratch/base`); if that fails, the CR comes back to the owner with
  the result.
- lp-Q4: no guard test against `-s` in CONTRIBUTING.md: the text fix only.
- Settled by the Chief of Staff from the spec critic (recorded in `02-answers.md`):
  - no `git clone -c core.longpaths=true` advice: all five failures were `git worktree add`, which
    the shared config covers;
  - no SwRS and no `requirements/tiers/log.md` entry: contributor tooling, outside the product
    contract (constitution, section 1), and `just check-markers` does not scan the root `justfile`;
  - the `git config` step is skipped outside a Git work tree (an unpacked source archive keeps
    working with `just dev`);
  - one sentence in the CONTRIBUTING.md "Windows" section.

## What changes

Read at `origin/main` 5a84db8b (`chore: version 1.11.0`).

### 1. `justfile`, recipe `dev` (line 15)

Today:

```just
# Set up Node.js, JavaScript and Python dependencies, and Chromium for tests.
dev:
    fnm install
    {{ npm }} ci
    uv sync --group docs --group release --group requirements
    uv run --no-sync --group docs playwright install chromium
```

- A private recipe, for example `_git-long-paths`, in two twins:
  - `[windows]`: when the working directory is inside a Git work tree
    (`git rev-parse --is-inside-work-tree` succeeds), it runs `git config core.longpaths true`;
    outside one it does nothing and exits 0;
  - `[unix]`: an empty body (Linux and macOS run no `git config`).
- `dev` depends on it (`dev: _git-long-paths`), so it runs before `fnm install` and a later step that
  fails still leaves the setting in place. `install: dev` (line 104) inherits it.
- The private-recipe form is required (not an inline conditional) so the test below can run that
  one step for real in a temporary folder without installing anything. The recipe name is the
  Driver's.
- The `dev` comment says it, for example: "Set up Node.js, JavaScript and Python dependencies, and
  Chromium for tests; on Windows, also turn on Git long paths (`core.longpaths`) for the
  repository."
- `git config` with no `--global`/`--worktree` writes the repository's shared config (the main
  checkout's `.git/config`, also when `just dev` runs inside a linked worktree), so after one run in
  the main checkout every worktree added afterwards is covered. The command is idempotent.
- `dev-ci` is unchanged (CI's checkout is done by `actions/checkout` before any recipe runs).

### 2. `AGENTS.md`, section "Setup" (lines 57 to 68)

The `just dev` bullet (line 63) says that on Windows it also sets `git config core.longpaths true`
in the repository, so a base checkout or a new worktree does not fail with "Filename too long". The
wording is the Driver's; it names the command and the reason, and stays in the existing bullet or a
new one next to it.

### 3. `.agents/guidelines/local-worktree.guidelines.md`, section "One worktree per change"

The paragraph after the code block ("`just dev` runs first in a new worktree or a clean checkout...")
adds: on Windows, `just dev` sets `core.longpaths` in the repository's shared config, so once it
has run in the main checkout, `git worktree add` and a checkout of the base (`origin/main`) do not
fail on long paths. The two-line `bash` example stays as is.

### 4. `CONTRIBUTING.md`, section "Windows" (line 26)

One sentence: `just dev` sets `git config core.longpaths true` in the repository, so worktrees and
checkouts whose paths pass Windows' 260-character limit do not fail with "Filename too long".

### 5. `CONTRIBUTING.md`, "How to Release", step 3 (line 629)

```bash
git commit --amend --no-edit -s CHANGELOG.md
```

becomes

```bash
git commit --amend --no-edit CHANGELOG.md
```

and the sentence before the block ("...then amend the version commit:") says the version commit
carries no `Signed-off-by` trailer, so the amend has no `-s`, in the words of
release-process.guidelines.md line 79. Nothing else in "How to Release" changes. At `origin/main`
no other commit command in the repository's docs carries `-s` or `--signoff`; the Driver checks it
again at its own base (see Evidence).

## Commits and delivery

- One PR. Suggested commits: `build: turn on Git long paths in just dev on Windows` (justfile, its
  test, AGENTS.md, local-worktree guideline, CONTRIBUTING "Windows") and `docs: drop the sign-off
  from the release amend in CONTRIBUTING` (CONTRIBUTING.md step 3). No scope on `build`
  (`.agents/guidelines/git-commit-allowed-scopes.md`); messages follow
  `.agents/guidelines/git-commit-message.guidelines.md`, with no `Signed-off-by`.
- No `CHANGELOG.md` line: build and documentation commits get none (CONTRIBUTING, step 2).
- No SwRS, no requirement markers, no `tiers/log.md` entry (decision above).
- No rendered syntax changes: the writing skill is untouched.
- Landing step, after the merge: run `just dev` (or the single `git config core.longpaths true`)
  once in the main checkout on the Windows machine, since "every new worktree is covered" holds only
  once the shared config carries the setting. The Chief of Staff or the Driver records that it was
  done (`git config --get --show-origin core.longpaths` printing `true` from the main checkout's
  `.git/config`).

## Out of scope

- A global setting (`git config --global`) or any change outside this repository's config.
- `git clone -c core.longpaths=true` advice.
- A shorter worktree root (the planning surface's `checkout.yml` keeps
  `../../../markdown-okf-schema-studio.worktrees/`).
- `dev-ci`, the CI workflows and the Windows CI job.
- A test guarding CONTRIBUTING.md against `-s` (lp-Q4).
- Release-process.guidelines.md (already right), `scripts/version.py` and `just bump-version`
  (already commit with no trailer, SwRS-MDOKFSTUDIO-CORE-075).

## Host matrix

The change depends on the host (Windows or not). One line per cell:

- Windows, inside a Git work tree (local machine; CI job `static-windows` on `windows-latest`, which
  runs `just check` through `just ci-static`): `just dev` sets `core.longpaths` to `true` in the
  repository's shared config.
- Windows, outside a Git work tree (an unpacked archive): the step does nothing, exits 0, and
  `just dev` goes on.
- Linux (CI job `static`, `ubuntu-latest`) and macOS (a contributor's machine, not run in CI): no
  `git config` command runs; the repository config is untouched.

## Evidence

### Automated test (shipped justfile, both CI static jobs)

New tests in `test/build/test_workflows.py` (run by `just release-tests`, so by `just check` on
both CI static jobs). They run the shipped `justfile` from the repository at the head under test,
not a copy, in the style of `_locked_screen_run` (line 329):
`just --justfile <ROOT>/justfile --working-directory <tmp> <recipe>`.

- `just --dry-run dev` lists the long-paths step before `fnm install` on Windows
  (`os.name == "nt"`), and lists no `git config` elsewhere. `--dry-run` runs nothing.
- The private step run for real in a `git init` temporary repository: on Windows,
  `git -C <tmp> config --local --get core.longpaths` prints `true` afterwards; elsewhere it stays
  unset.
- The private step run for real in a temporary folder that is not a Git work tree: exit 0 on every
  host, and no `.git` is created there.
- Fail before: on the local Windows machine the Windows assertions fail on the base (no such
  recipe, no `git config` line) and pass on the head; the Driver records both runs. The Linux cell
  passes before and after (it guards against a leak to other hosts).

### Real run on Windows in a long base worktree (lp-Q3)

A short path already succeeds, so the run uses a worktree root deep enough that the repository's
longest tracked path (129 characters today, under
`.agents/skills/markdown-studio-exploratory-qa-claude/scenarios/`) passes 260: the CR's
`work/scratch/base` (about 162 characters in the batch's `4-batch/2-actives/<cr>/` folder; add
folders if `len(root) + 1 + 129` is not above 260). The Driver prints the root's length and the
longest resulting path's length.

1. In the main checkout, save the current value of `core.longpaths`, then
   `git config --unset core.longpaths` (restore the saved value at the end).
2. `git worktree add <long root> origin/main --detach` fails with "Filename too long" (the
   fail-before, recorded with its message); remove the half-made worktree
   (`git worktree remove --force` and `git worktree prune`).
3. From a short worktree of the head, run `just dev`; `git config --get --show-origin
   core.longpaths` prints `true` from the main checkout's `.git/config`.
4. `git worktree add <long root> origin/main --detach` now succeeds.
5. In that long worktree: `just dev` passes, then `just compile` and one compiled unit test file of
   the Driver's choice under `out/test/core/`, run with
   `fnm exec -- node scripts/node-test.mjs unit "<that file>"`, passes. The Driver names the file
   and records the output.
6. Remove the long worktree and restore `core.longpaths` from step 1.

If step 4 or 5 fails, the CR goes back to the owner with the result (lp-Q3); no workaround.

### Docs

- AGENTS.md Setup, the local-worktree guideline and CONTRIBUTING "Windows" name `core.longpaths`
  (diff).
- Command lines only: CONTRIBUTING.md holds the line `git commit --amend --no-edit CHANGELOG.md`,
  and no line of the repository's Markdown docs that starts (after indentation) with `git commit`
  carries `-s` or `--signoff`, for example
  `git grep -nE '^\s*git commit\b.*(\s-s\b|--signoff)' -- '*.md'` prints nothing, while
  `git grep -nF 'git commit --amend --no-edit CHANGELOG.md' -- CONTRIBUTING.md` prints the line.

### Gate

`just preflight` passes (on Windows, the static stage; CI runs the others), and the PR's CI
`static` and `static-windows` jobs are green: `static-windows` is the CI proof of the Windows
cells, `static` of the Linux cell.
