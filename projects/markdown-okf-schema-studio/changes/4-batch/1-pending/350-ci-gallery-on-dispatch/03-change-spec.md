# Build the gallery and site on a heavy CI dispatch

Short name: `ci-gallery-dispatch`. Origin: verbal (a finding of CR-342's Verifier, batch-06,
2026-11-17). Go: the owner's word of 2026-11-17 adding the inbox items to batch-06
(`02-answers.md`, Q1). Spec critic: no.

## Goal

When a developer runs the heavy jobs on a branch by hand,
`gh workflow run ci.yml --ref <branch> -f heavy=true`, the run also builds the gallery and the
site and uploads them as the `studio-site-attempt-<n>` artifact, so the site of a branch (for
example the use case diagrams of the requirements site) can be checked without editing the
workflow on that branch. When a job the gallery needs failed, the `gallery` job does not run.

## Why it fails today

Two causes, both in `.github/workflows/ci.yml`, job `gallery` (around line 439):

1. Its `if` is `github.event_name == 'workflow_dispatch' && inputs.gallery && inputs.heavy`. It has
   no status function, so GitHub adds the implicit `success()`. `success()` is false when an
   ancestor job was skipped, and `release-check` (`if: github.event_name == 'push' && github.ref ==
   'refs/heads/main'`) is always skipped on a dispatch. `gallery` needs `report`, which needs
   `release-check` and `integration`, so `gallery` is skipped on every dispatch. `integration`,
   `stress`, `report`, `checks`, `tag-release` and `pages` already avoid this with `!cancelled()`
   and explicit `needs.<job>.result` checks (the comments on `integration` and `pages` say
   so).
2. The `gallery` dispatch input defaults to `false`, so `-f heavy=true` alone would not ask for
   the gallery even with cause 1 fixed.

The test that should have caught cause 1,
`test_every_job_after_a_skippable_job_opts_out_of_the_implicit_success` in
`test/build/test_workflows.py`, skips every job whose `if` mentions `inputs.heavy`, with the
comment "runs only when the heavy ancestors ran, so nothing above it is skipped". That is false:
`release-check` sits above `report` and is skipped on every dispatch. The exemption hid the bug.

## What changes

### `.github/workflows/ci.yml`

- Input `gallery` (under `on.workflow_dispatch.inputs`): `default: true`. Description: "Build the
  gallery and the site from the end-to-end reports (heavy only; false skips it)".
- Job `gallery`:
  - `needs: [integration, report]`.
  - `if: ${{ !cancelled() && github.event_name == 'workflow_dispatch' && inputs.heavy &&
    inputs.gallery && needs.integration.result == 'success' && needs.report.result == 'success'
    }}` (one line or a folded scalar, as the other jobs write it).
  - Rewrite its comment: the gallery needs the real-window captures of the heavy jobs; it runs on
    a heavy dispatch unless `gallery` is false; `!cancelled()` because `release-check`, an
    ancestor through `report`, is skipped outside a push to `main`; it runs only when
    `integration` and `report` succeeded.
  - Steps, the artifact name `studio-site-attempt-${{ github.run_attempt }}`, `timeout-minutes:
    15` and permissions are unchanged.
- No other job changes. `gallery` stays out of `checks` and out of the push-to-`main` path.

### `test/build/test_workflows.py`

- In `test_every_job_after_a_skippable_job_opts_out_of_the_implicit_success`, remove the
  `inputs.heavy` exemption and its comment. Every job below a skippable job, `gallery` included,
  then needs `!cancelled()` (or `always()`) and an explicit `needs.<job>.result` check, unless it
  is in `REPORTS_WHATEVER_HAPPENED`. Today only `gallery` used the exemption: `integration` and
  `stress` already pass without it.
- New test, marked `# @tests_req SwRS-MDOKFSTUDIO-CORE-076`, for example
  `test_gallery_runs_on_a_heavy_dispatch_when_integration_and_report_passed`. It evaluates the
  `gallery` `if` with `_run_if` and `_context`, adding `inputs.gallery` and the results of
  `integration` and `report` to the context:
  - true: dispatch, `heavy` true, `gallery` true, `integration` and `report` `success`;
  - false: `integration` `failure`; `report` `failure`; `report` `skipped`; `heavy` false;
    `gallery` false; event `pull_request`; event `push`.
  It also asserts that `gallery` needs `integration` and `report`, and that the `gallery` input
  is a boolean with `default` `True` (read as
  `yaml.safe_load(CI.read_text())[True]["workflow_dispatch"]["inputs"]["gallery"]`, as the stress
  input test does).
- `test_every_needs_reference_names_a_job_the_job_needs` must keep passing (it checks that
  `needs.integration` is declared in `needs`).

### Documentation

- `.agents/guidelines/ci.guidelines.md`, rule 13: replace "(add `-f gallery=true` for the gallery
  and site)" with: the gallery and site artifact (`studio-site-attempt-<n>`) are built too when
  `integration` and `report` succeed; `-f gallery=false` skips them (for example in a stress
  loop).
- `CONTRIBUTING.md`, around line 283: the same change to "(add `-f gallery=true` for the gallery
  and site artifact)".
- The comment above `integration` in `ci.yml` is unchanged.

### Requirements

- `requirements/tiers/swrs/rendering-core/SwRS-MDOKFSTUDIO-CORE-076.md` (`req_lifecycle:
  proposed`, so it can be edited without re-approval): add rows to the table of "Scenario
  (boundary): Failure, cancellation and other events":
  - "a dispatch with `heavy` (and `gallery` not false) whose `integration` and `report` succeed" ->
    "`gallery` runs and uploads the gallery and site as `studio-site-attempt-<n>`";
  - "a dispatch with `heavy` whose `integration` or `report` did not succeed, or with `gallery`
    false" -> "`gallery` is skipped".
  Add one sentence to "Normative behavior": a heavy dispatch SHALL build the gallery and site
  unless `gallery` is false, and only when `integration` and `report` succeed. Adjust the
  `description` front matter only if the project guidelines ask the description to cover every
  normative sentence.
- Run `just requirements-update`, and add a dated entry to `requirements/tiers/log.md` (CR
  number as the Driver gets it), in the style of the recent entries: "Changed:
  SwRS-MDOKFSTUDIO-CORE-076 ...", "Sources: `.github/workflows/ci.yml`", "Tests:
  `test/build/test_workflows.py`".
- Read `requirements/guidelines/requirements.guidelines.md` and
  `requirements/guidelines/project.guidelines.md` ("During a change") first, as `AGENTS.md`
  asks.

### Release notes

A CI-only change that ships nothing in the VSIX: no release note, unless
`just release-notes-check` or the release-process guideline asks for one.

## Choices settled here, with reasons

- **`gallery` defaults to `true` rather than being removed.** The goal names
  `-f heavy=true` alone; a default of `true` meets it and keeps an opt-out for dispatches that only
  loop stress scenarios (`-f stress_repeat=60 ...`), where the site costs a runner for nothing.
  "Run workflow" in the Actions tab then shows the box ticked.
- **`gallery` needs `integration` explicitly, not only through `report`.** `ci-report all` fails
  when the integration stage is missing or failed, so `report` success already implies it today;
  naming `integration` makes "a needed job failed" explicit and keeps the gallery off if `report`
  ever tolerates a red integration stage. `visual` is not added: `report` already fails without a
  passing visual stage, and the gallery does not read the visual artifact directly.
- **No new SwRS.** The behaviour is CI wiring already covered by CORE-076 and its tests; a row in
  its table is the smallest true statement.

## Out of scope

- Running the gallery on a pull request or on a push to `main` (Pages builds the site of a tag).
- Changes to `ci-gallery`, `ci-report`, the site build, `pages.yml` or `release.yml`.
- The `toc-loop` and `stress` jobs.

## Environment of the job

- `gallery` runs on GitHub's `ubuntu-latest`, only on a `workflow_dispatch`. It installs
  `just dev-ci visual` (Chromium for the social cards, plantuml, graphviz) from the Ubuntu package
  archives that the `visual` job saves in the Actions cache; on a branch it restores the cache of
  that branch or of the default branch, and installs from the mirror on a miss. It downloads the
  merged reports artifact named by `report`'s `artifact` output and uploads `out/site/`.
- The owner's machine is Windows: `just preflight` runs only the static stage there and skips
  `ci-gallery`, so the gallery cannot be run locally on it. GitHub's evaluation of `if`
  (implicit `success()`, skipped ancestors), the default of a boolean input on `gh workflow run`
  and the artifact upload exist only on GitHub.
- Before the push, the evidence is the local checks below (the workflow tests evaluate the
  condition). Only the first dispatch run proves that GitHub runs `gallery` and uploads the
  artifact.

## Evidence

1. Local, before the push: `just check` (it runs `release-tests`, so `test/build/test_workflows.py`
   with the removed exemption and the new test), `just requirements-lint`,
   `just requirements-update`, then `just preflight` (static stage on Windows). Before the fix,
   the strengthened skip-propagation test fails on `gallery` (the Driver may show that red run in
   the PR body, or state it).
2. On GitHub, after pushing the PR branch: `gh workflow run ci.yml --ref <branch> -f heavy=true`
   (no `-f gallery`). In that run: `release-check` skipped, `integration` and `report` green,
   `gallery` green, and the run's artifacts list `studio-site-attempt-1` with `out/site/` content
   (`gh run view <run-id>` and `gh api repos/{owner}/{repo}/actions/runs/<run-id>/artifacts`).
   The Driver puts the run link in the PR body, Test plan section.
3. The failure branch (gallery skipped when `integration` or `report` failed) is proved by the
   new unit test; no deliberately broken CI run is required. If the dispatch run of step 2 happens
   to have a red `integration`, it shows `gallery` skipped: record that, fix or re-run per CI rule
   12, and dispatch again for the green proof.
4. The PR's own `pull_request` run stays green and does not run `gallery`.

## Open questions

None.
