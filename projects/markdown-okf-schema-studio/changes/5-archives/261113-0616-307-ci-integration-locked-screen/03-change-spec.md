# Change Specification: stop ci-integration at once on a locked screen

Triage: automatable (short specification, not reviewed by the owner). Code read at `origin/main`
(`cb968299 chore: version 1.7.1`); cut the worktree from `origin/main`.

## Goal

On macOS, when the screen is locked, the real VS Code window never becomes active and
`ci-integration` fails after minutes, then `ci-report` and `ci-gallery` fail from it without
naming the cause (v1.7.1 retro). After this change, `ci-integration` checks for a locked screen
before anything else and stops at once with that cause and the two ways out: unlock the screen,
or dispatch the branch heavy run. `preflight` says why `ci-report` and `ci-gallery` did not run,
and the release procedure says to dispatch the branch heavy run at once in that case.

## What changes

### 1. `justfile`: a private lock check recipe

Add a private recipe `_require-unlocked-screen` (bash shebang, `set -uo pipefail`):

- The screen counts as locked when `STUDIO_SCREEN_LOCKED=1` (test override, read on every OS), or
  when `os()` is `macos` and `ioreg -n Root -d1` contains `"CGSSessionScreenIsLocked" = Yes`
  (the same probe as `macFocusDiagnostics` in `test/integration/macWindow.ts`; whitespace-tolerant
  match). No new dependency. On Linux and Windows without the override it does nothing.
- When locked, it prints to stderr, then exits with code **3**:

  ```text
  <stage>: screen locked, the VS Code window cannot become active; the real VS Code tests did not run.
  Unlock the screen and run it again, or prove the branch in CI at once:
    gh workflow run ci.yml --ref <branch> -f heavy=true
  To keep the screen from locking during an unattended run, see "App-window tests" in
  .agents/guidelines/local-worktree.guidelines.md (caffeinate).
  ```

  `<stage>` is the calling recipe's name (pass it as a recipe parameter, for example
  `_require-unlocked-screen STAGE="ci-integration"`). The wording may be tightened; it must name the
  cause, both ways out with the exact `gh workflow run` command, and `caffeinate`.
- When not locked, it prints nothing and exits 0.

### 2. `justfile`: callers of the check

- `ci-integration` (line 272): the check runs **before** `eval "$(node scripts/e2e-campaign.mjs
  begin integration)"` (as a recipe dependency or as the first line of the script), because `begin`
  deletes the previous integration manifest, `review.json` and `e2e-manifest.json`: a refused run
  must not erase evidence. On a locked screen `ci-integration` exits 3. Its existing pass/fail lines
  and `exit 1` stay unchanged, so code 3 means only "screen locked".
- `ci-stress` (line 316): the same check, before its tests (after the `REPEAT` validation is fine).
- `integration` (line 206) and `e2e` (line 214): the same check, as a dependency, if it costs one
  line each (it does with a dependency).
- `ci-visual`, `ci-toc-loop`, `ci-hang-dump`: unchanged.

### 3. `justfile`: `preflight` (line 386)

- After the Windows early exit and before `just ci-visual`: if the screen is already locked, print
  one warning line (for example `preflight: the screen is locked; ci-integration will stop unless
  it is unlocked before then`) and go on. Reuse the same probe (call `just _require-unlocked-screen
  preflight` with its output silenced and test its exit code, or an equivalent).
- Replace the integration, report and gallery lines so that when `just ci-integration` exits 3:
  - print `ci-report: skipped, integration did not run (screen locked)` and
    `ci-gallery: skipped, integration did not run (screen locked)`, and run neither;
  - count the failure: `preflight` still ends with `N preflight stage(s) failed` and exits 1
    (constitution 4: a locked screen never turns preflight green).
  - Any other exit code of `ci-integration` keeps today's behaviour (report and gallery still run).
- The Windows branch stays exactly as it is: `just ci-static`, then the `"{{ os() }}" == "windows"`
  test with `exit "$failures"`, before `just ci-visual` (the existing test
  `test_preflight_skips_only_the_stages_that_need_linux_or_macos_on_windows` must still pass).

Run `just format` after editing: it rewrites the justfile.

### 4. Tests: `test/build/test_workflows.py`

- `test_ci_integration_stops_on_a_locked_screen`: run `just --justfile <ROOT>/justfile
  --working-directory <tmp_path> ci-integration` with `STUDIO_SCREEN_LOCKED=1` in the environment
  (use `_bash()`-style care for Windows if needed; the static job runs on Windows too). Assert:
  exit code 3; stderr names the locked screen; it contains `gh workflow run ci.yml --ref` and
  `-f heavy=true`, and the unlock way out; `tmp_path` has no `out/` (no campaign file written).
- The same for `ci-stress` (exit 3, no tests started) is welcome but optional.
- A text test of the `preflight` recipe (same style as the Windows test: split the recipe out of the
  justfile): the exit code 3 of `just ci-integration` is tested; both skip lines
  (`ci-report: skipped, integration did not run (screen locked)` and the `ci-gallery` one) are
  present; the locked path does not run `just ci-report` or `just ci-gallery`; the failure counter
  is incremented on that path.
- No test may depend on the real lock state of the machine: without the override, Linux and Windows
  take the "not locked" path, and the tests set the override explicitly.

### 5. Documents

- `.agents/guidelines/release-process.guidelines.md`, step 5 (the version commit): when the local
  `just preflight` stops at `ci-integration` because the screen is locked, do not wait: dispatch
  `gh workflow run ci.yml --ref <branch> -f heavy=true` at once on the release branch and go on; its
  `integration` job is the real-window proof. Write it as one short sentence or bullet in the
  guideline's style.
- `CONTRIBUTING.md`, "How to Release" step 4 (`just preflight` before pushing the version commit):
  the same sentence. Optionally one line near "`just preflight` runs every stage and returns a
  failure if any stage fails" saying that on macOS a locked screen stops `ci-integration` at once
  and skips report and gallery.
- `.agents/guidelines/local-worktree.guidelines.md`: no change. Its sentence "app-window tests then
  fail fast" becomes true with this change.
- Another CR of the same batch (changelog-line-in-each-pr) and the release-flow update of this
  batch also edit these two release documents: keep the edit to the locked-screen sentence and
  rebase on the CR below in the stack. If the release flow there now dispatches the heavy run on the
  stack's top branch, word the sentence so it fits whichever step runs the local `just preflight`.

## Decisions carried from the answers and the advisor

- macOS only for the real probe; the override works on every OS for tests (answers, round 1, item 2;
  advisor 1, 6).
- Check before the run, stop with the cause and both ways out (answers, item 2; advisor 2).
- `preflight` names `ci-report` and `ci-gallery` as skipped because integration did not run, and
  still fails (answers, item 2; advisor 3).
- `ci-stress`, and `integration`/`e2e` at one line each, get the check (advisor 4).
- Early warning line in `preflight`, without stopping (advisor 5).
- A screen that locks during the run is out of scope; the message names `caffeinate` (advisor 7).
- No requirement: developer tooling, not extension behaviour (advisor 8).
- Release guideline step 5 and CONTRIBUTING step 4 say to dispatch the branch heavy run at once
  (answers, item 2; advisor 9).

## Out of scope

- A screen that locks during the run (the `caffeinate` advice covers it).
- `scripts/e2e-campaign.mjs`, `test/integration/macWindow.ts` and the CI workflows: unchanged (the
  CI runners are Linux and never take the locked path; exit code 3 never reaches a CI job).
- `.agents/guidelines/ci.guidelines.md`: unchanged.
- Any SwRS or StRS, `requirements/tiers/log.md`: no requirement covers `preflight` or the `ci-*`
  targets.
- `CHANGELOG.md`: no line (CI and build changes get none).

## Evidence

- `just format`, then `just check` green (includes `test/build/test_workflows.py`).
- `STUDIO_SCREEN_LOCKED=1 just ci-integration; echo $?` prints the message and `3`, and
  `out/reports/e2e/` is untouched (compare its listing before and after).
- `STUDIO_SCREEN_LOCKED=1 just ci-stress 1; echo $?` prints the message and `3`.
- Without the override on an unlocked Mac, `just ci-integration` starts the run as before.
- `just preflight` green on an unlocked machine (completion gate). A run of `preflight` with
  `STUDIO_SCREEN_LOCKED=1` exported shows the early warning, the `ci-integration` message, both skip
  lines, `1 preflight stage(s) failed` and exit 1 (paste the tail in the PR as evidence).
- CI `checks` green on the PR (Linux and Windows static jobs run the new tests).
- PR: commit type `ci:` (no scope), "No behaviour change" in the requirements part of the template.

## Open questions

None.
