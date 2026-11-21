# Windows long paths in `just dev`, no sign-off in CONTRIBUTING release

Two small fixes merged into one CR by the owner (2026-11-21): on Windows, `just dev` turns on
`core.longpaths` for the repository so a base checkout or a new worktree never fails with
"Filename too long"; and CONTRIBUTING.md "How to Release" stops signing off the version commit,
as the release guideline already says. No tracker issue (verbal, from the batch-06 retro and the
CR-434 release Driver).

## Goal

- A Verifier, a Driver or a contributor on Windows can always check out the base (`origin/main`)
  or add a worktree of this repository: the batch-06 retro counted five blocked checkouts
  (CR-348, CR-350, CR-427, CR-431, CR-432) whose fail-before claims went into PR bodies as
  UNVERIFIED. The fix lives in `just dev`, the command every new checkout or worktree already runs
  first, so nobody has to remember a manual step (owner, lp-Q1: "just dev le règle").
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

- On Windows only (`os_family() == "windows"`, the test the justfile already uses for `npm.cmd` at
  line 4), `dev` runs `git config core.longpaths true`. On Linux and macOS it runs no `git config`
  command at all.
- It runs first in the recipe, before `fnm install`, so a later step that fails still leaves the
  setting in place.
- The form is the Driver's choice, as long as `just --dry-run dev` shows the command on Windows and
  not elsewhere: an inline `{{ if os_family() == "windows" { "git config core.longpaths true" } else { "" } }}`
  line, or a private `[windows]` recipe (with an empty `[unix]` twin) that `dev` depends on. Both
  were probed with just 1.59.0 on Windows: `just --dry-run` prints `git config core.longpaths true`.
- The recipe comment says it, for example: "Set up Node.js, JavaScript and Python dependencies, and
  Chromium for tests; on Windows, also turn on Git long paths (`core.longpaths`) for the repository."
- `git config` with no `--global`/`--worktree` writes the repository's shared config (the main
  checkout's `.git/config`, also when `just dev` runs inside a linked worktree), so one run in the
  main checkout covers every worktree added afterwards. The command is idempotent.
- `install: dev` (line 104) inherits it. `dev-ci` is unchanged (CI's checkout is done by
  `actions/checkout` before any recipe runs).

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

### 4. `CONTRIBUTING.md`, "How to Release", step 3 (line 629)

```bash
git commit --amend --no-edit -s CHANGELOG.md
```

becomes

```bash
git commit --amend --no-edit CHANGELOG.md
```

and the sentence before the block ("...then amend the version commit:") says the version commit
carries no `Signed-off-by` trailer, so the amend has no `-s`, in the words of
release-process.guidelines.md line 79. Nothing else in "How to Release" changes. `git grep` at
`origin/main` finds no other `-s` or `--signoff` commit in the repository's docs; a Driver checks it
again at its own base.

## Commits and delivery

- One PR. Suggested commits: `build: turn on Git long paths in just dev on Windows` (justfile, its
  test, AGENTS.md, local-worktree guideline) and `docs: drop the sign-off from the release amend in
  CONTRIBUTING` (CONTRIBUTING.md). No scope on `build`
  (`.agents/guidelines/git-commit-allowed-scopes.md`); messages follow
  `.agents/guidelines/git-commit-message.guidelines.md`, with no `Signed-off-by`.
- No `CHANGELOG.md` line: build and documentation commits get none (CONTRIBUTING, step 2).
- No rendered syntax changes: the writing skill is untouched.

## Out of scope

- A global setting (`git config --global`) or any change outside this repository's config.
- A shorter worktree root (the planning surface's `checkout.yml` keeps
  `../../../markdown-okf-schema-studio.worktrees/`).
- `dev-ci`, the CI workflows and the Windows CI job.
- Release-process.guidelines.md (already right), `scripts/version.py` and `just bump-version`
  (already commit with no trailer, SwRS-MDOKFSTUDIO-CORE-075).

## Host matrix

The change depends on the host (Windows or not). One line per cell:

- Windows (local machine, and CI job `static-windows` on `windows-latest`, which runs `just check`
  through `just ci-static`): `just --dry-run dev` lists `git config core.longpaths true`; a real
  `just dev` leaves `git config --get core.longpaths` at `true` in the repository.
- Linux (CI job `static`, `ubuntu-latest`) and macOS (a contributor's machine, not run in CI):
  `just --dry-run dev` lists no `git config` command; `just dev` leaves the repository config
  untouched.

## Evidence

- New test in `test/build/test_workflows.py` (run by `just release-tests`, so by `just check` on
  both CI static jobs). It runs the shipped `justfile` from the repository at the head under test,
  not a copy, in the style of `_locked_screen_run` (line 329): `just --justfile <ROOT>/justfile
  --dry-run dev`, and asserts on its output (just prints dry-run commands on stderr):
  - on Windows (`sys.platform == "win32"` or `os.name == "nt"`): a line
    `git config core.longpaths true` is listed, before the `fnm install` line;
  - elsewhere: no line contains `git config`.
  `--dry-run` runs nothing, so the test changes no config and installs nothing. If the dry run turns
  out to need `fnm` or `uv` on `PATH` in CI, the Driver says so; it is not expected (dry run only
  prints).
- Fail before: on the local Windows machine, the new test fails on the base (no `git config` line)
  and passes on the head; the Driver records both runs. The Linux cell passes before and after (it
  guards against a leak of the command to other hosts).
- Real run on Windows: in a fresh worktree of the head, `git config --unset core.longpaths` in the
  repository (the shared config; restore it afterwards if it was set), run `just dev`, then
  `git config --get --show-origin core.longpaths` prints `true` from the main checkout's
  `.git/config`. Then `git worktree add <path> origin/main --detach` succeeds and removes cleanly.
- Docs: `git grep -n -e "commit.*-s\b" -e "--signoff" -- CONTRIBUTING.md .agents AGENTS.md` finds
  no sign-off in a commit command; the AGENTS.md Setup and local-worktree guideline diffs name
  `core.longpaths`.
- `just preflight` passes (on Windows, the static stage; CI runs the others), and the PR's CI
  `static` and `static-windows` jobs are green: `static-windows` is the CI proof of the Windows
  cell, `static` of the Linux cell.

## Open questions for the owner

1. A fresh `git clone` on Windows checks out before `just dev` can run, so a clone that hits a long
   path still fails. Should AGENTS.md Setup (and CONTRIBUTING "Windows") also tell to clone with
   `git clone -c core.longpaths=true ...`, or is `just dev` alone enough (the repository's longest
   tracked path today is 129 characters, under
   `.agents/skills/markdown-studio-exploratory-qa-claude/scenarios/`)?
2. Requirements: does this setup step need an SwRS (with `@implements_req` in the justfile and
   `@tests_req` on the new test, like SwRS-MDOKFSTUDIO-CORE-075 does for the version script), or is
   it development tooling outside the product contract, with no SwRS and no `tiers/log.md` entry?
3. When `just dev` runs outside a Git work tree (an unpacked source archive), `git config` fails
   and stops `dev`. Should the step be skipped there (guarded by
   `git rev-parse --is-inside-work-tree`), or is failing acceptable?
4. CONTRIBUTING.md "Windows" (line 26), which AGENTS.md Setup points to for Windows: should it
   mention `core.longpaths` too, or stay as is (the grill named only AGENTS.md and the
   local-worktree guideline)?
5. Should a test guard CONTRIBUTING.md against a signed-off release commit coming back (for example
   in `test/build/test_release.py`), or is the doc fix alone enough?
