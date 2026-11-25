# StRS acceptance tests, acceptance job and okfreq mode switch (CR-B)

This CR is the second half of the okfreq 0.18 subject. CR-504 (`strs-path-validation`, CR-A)
declared every StRS path and every SwRS scenario, sorted the markers and taught the marker check
the `@accepts_req` verb, still in the old coverage mode. This CR finishes the job:

- every declared SwRS scenario gets a test, or is pruned with a reason;
- every live StRS path gets an acceptance test (`@accepts_req StRS-X#S<n>`), walked in real
  VS Code, one file per e2e group under `test/integration/acceptance/`;
- a new heavy CI job, `acceptance`, runs those files in a matrix by group, one shared window per
  group;
- a gate (D11) fails `just requirements-lint` when a scenario is untested or a path unaccepted;
- the bundle switches to `strs_test_coverage_mode: linked-swrs-and-acceptance-paths` and shows the
  honest number: a StRS is `covered` only when its linked SwRS are covered and every path is
  accepted.

In the owner's terms: after this CR, "covered" on a stakeholder requirement means that a test
walks each of its main paths in the real editor, and every behaviour scenario has its test.

Short name: `strs-acceptance`.

**Depends on CR-504.** This CR is stacked on CR-504's branch
(`chantier/batch-09/cr-504-strs-paths-and-swrs-scenarios-declared-o`) and starts from its head. It
cannot start before CR-504 is final: the `scenarios:` declarations, the `#S<n>` fragments, the
`@accepts_req` marker check (D10) and the viewer cards it builds on are CR-504's. The Chief of Staff
records the dependency in `depends.json`.

Sources:

- this CR folder: `01-intent.md`, `02-answers.md` (acceptance-Q1, acceptance-Q2);
- CR-504's folder, `changes/4-batch/1-pending/504-strs-path-validation/`: `03-change-spec.md`
  (whole, and its last section "Handed to the next CR (CR-B)", which is this CR's scope) and
  `02-answers.md` Q27 to Q42 (Q1, Q3, Q6, Q28, Q30, Q30b, Q32, Q35, Q37, Q39, Q40, Q41, Q42 apply
  here);
- the released okf-schema 0.18.1 documentation, tag `v0.18.1`
  (<https://okf-schema.readthedocs.io/en/stable/>): `reference/okfreq-acceptance-paths` (mode
  comparison, combination table, counters, findings W003 and W004, report fields),
  `explanation/okfreq-acceptance-paths` (execution cost, waiver),
  `reference/okfreq-configuration` (`strs_test_coverage_mode`, `generated_fields`) and
  `reference/okfreq-cli` (`generate-report --output-json`).

The project rules apply as written and this spec does not restate them: the constitution
(`.agents/constitution.md`), `AGENTS.md`, `requirements/guidelines/requirements.guidelines.md`,
`requirements/guidelines/project.guidelines.md` and `.agents/guidelines/ci.guidelines.md`.

## Figures

Figures below come from the Studio's `main` at `80d482fd` (before CR-504) and are indicative only.
CR-504 changes them (new paths for BLOCK-027, TRUST-012, TRUST-014; the marker sort; the SwRS
sweep). The coder recounts every figure on CR-504's head and puts the recounted figures in the PR
body.

- Live StRS: 94 (15 approved, 79 proposed), about 150 paths before CR-504's additions. Paths per
  scope: block-editing 16, code-blocks 3, diagrams 9, frontmatter-editing 4, frontmatter-schema 7,
  gfm 4, layout-width 6, lifecycle-sync 18, myst 15, palette-slash 14, rendering-core 8,
  review-annotations 12, table-editing 12, theme-zoom 4, toolbar-navigation 13, trust-security 5.
- `@tests_req StRS-…` lines: 101 in `test/integration` (46 files), 74 in `test/visual`, 10
  elsewhere. CR-504 turns the ones that walk a path in real VS Code into `@accepts_req`; the sample
  audit predicts about one path in four accepted after CR-504.
- The untested SwRS scenarios are the list in CR-504's PR body ("Scenarios that no marker covers
  after the sweep"), recounted on its head.

## What okf-schema 0.18.1 does in the new mode (the contract)

As released, and only what this CR relies on:

- `strs_test_coverage_mode: linked-swrs-and-acceptance-paths` in `requirements/config.yml`.
- A StRS is `covered` when it has at least one linked SwRS, each `covered` or `exempt` (an
  `annotation_exemption` with a non-blank `exemption_reason`), **and** every declared path has a
  counting `@accepts_req StRS-X#S<n>`, or the StRS carries a justified `acceptance_exemption`.
  "Tested" (`@tests_req StRS-X#S<n>`) is reported and does not change the status.
- A SwRS that declares `scenarios:` is test-covered only when every `S<n>` has a counting
  `@tests_req SwRS-X#S<n>`. A SwRS without `scenarios:` (TRUST-070, TRUST-075, Q39) is covered by a
  fragmentless `@tests_req`, as before.
- Fragment errors (missing fragment on a declaring target, unknown fragment, `@accepts_req` on a
  SwRS) make `okfreq validate` and `okfreq lint` exit 1. W003 (live StRS with no `scenarios:`) and
  W004 (live StRS with no counting `@accepts_req` and no waiver) are printed and never change the
  exit code.
- `okfreq update-coverage` writes, when listed in `generated_fields`: `tested_in_files` on SwRS
  and StRS, and `accepted_in_files` on StRS. CR-504 added `accepted_in_files` to
  `generated_fields`; `tested_in_files` is already there.
- `okfreq generate-report requirements --output-json FILE` writes `format_version` 2. In the new
  mode each record of `requirements[]` carries `frontmatter` (so `req_lifecycle` and `scenarios`),
  `tier`, `diagnostics.exempted`; a StRS adds `stakeholder_test_coverage` with `status`, `paths`
  (`total`, `tested`, `accepted`), `accepted`, `acceptance_tests` and, only with a justified
  waiver, `acceptance_exemption`; a SwRS that declares scenarios adds
  `transitions: {tested: [...], missing: [...]}`. "Live" is every lifecycle except `deprecated`
  and `superseded`.
- `okfreq` counts markers; it never reads test results. The proof that a test passes is its
  bench's CI job (Q35).

## Decisions

### Carried from CR-504's answers (02-answers Q27 to Q42) and its spec

- **Q1:** an automated end-to-end test of a StRS path is an acceptance test.
- **Q3:** one nominal path per acceptance test. It runs end to end in one go and asserts the final
  result, plus the steps no SwRS covers. It never covers edge cases or errors.
- **Q6:** a human step is a simulated input. The test asserts the system's gate (blocked without
  the step, proceeds with it) and the content it can check, never a judgment. Another verification
  method is a rare exception written in the path.
- **Q27:** switch the mode and show the honest number.
- **Q28:** the bench convention: `@tests_req StRS-X#S<n>` = the path walked on the simulated bench
  (every PR); `@accepts_req StRS-X#S<n>` = the path walked in real VS Code (`test/integration`,
  pushes to `main`). The only exception is D7.
- **Q30, Q30b:** a SwRS never keeps a scenario without a test. The coder writes the test by
  default. It removes a scenario only when another scenario or SwRS already says the same, or when
  the scenario cannot be observed. Every removal is listed in the PR with its reason and logged in
  `requirements/tiers/log.md`.
- **Q32, D15:** a waiver (`acceptance_exemption`) is only for a StRS with no step that can be
  automated. Waiver candidates: **none**. CORE-006: the agent's writing is a simulated input.
  CORE-007: its acceptance test stops before CORE-078, the maintainer's review. The coder never
  writes a waiver.
- **Q35:** counts are marker-based, as okfreq counts. The proof that a test passes is its bench's
  CI job.
- **Q37:** the acceptance budget: one shared window per e2e group; a group may use several
  launches, each with its own budget under the 15-minute launch deadline; the job is sharded by
  group in a matrix; the spec states the expected step duration; no stress-plan entry, and the
  spec says so; no fresh window per test; no raised timeouts.
- **Q39:** TRUST-070 and TRUST-075 (exempt) have no `scenarios:`; D11 does not ask anything of
  them.
- **Q40:** D11 runs `okfreq generate-report --output-json` into `out/` itself, and lands with the
  switch.
- **Q41, D7:** CORE-007 (the release), CORE-008 (the site) and TRUST-014 (the built VSIX) may be
  accepted on the test closest to that product, under `test/build`, `test/security`, `test/site`
  or `test/core`. CORE-006 (the writing skill) and every other StRS, TRUST-012 included, are
  accepted in real VS Code.
- **Q42:** the CI wiring belongs to this CR: `test:acceptance` includes `npm run bundle`;
  `ci-acceptance` opens the e2e campaign like `ci-integration`; `tag-release`, the pages build,
  `report` and `checks` take the acceptance results; ci.guidelines rules 11, 13 and 14 apply; the
  AGENTS.md CI list and CONTRIBUTING's CI section are updated; the per-attempt artifact is named
  `-attempt-<n>` and announced through a job output.
- **D8:** the acceptance layout (B3 below gives the details).
- **D11:** the scenario coverage gate (B9).
- **D14 completion:** project.guidelines "Benches" gets the acceptance layout and the job (B11).
- **acceptance-Q1:** scope and decisions come from CR-504; this CR depends on it.
- **acceptance-Q2:** the delivery is as large as the Driver can make it in 3 rounds. If the Driver
  reports that it cannot finish, the Chief of Staff splits the rest per e2e group, and the first
  group's PR adds the acceptance job. The mode switch and the D11 gate land last.

### Taken by this spec

- **B1. Where a missing SwRS scenario test goes.** On the bench where that SwRS's other scenario
  tests live (the files that already carry `@tests_req SwRS-X#S<m>`). When the SwRS has none, the
  cheapest bench that can observe the scenario: `test/core`, `test/page`, `test/host-memory`,
  `test/session`, `test/node-services`, `test/site` or `test/build` for logic, `test/visual` for
  what only a rendered page shows, `test/integration` only when only a real window can observe it.
  The test carries `// @tests_req SwRS-X#S<n>` (and a companion line where the marker check
  asks for one). A scenario is "not observable" when no bench can reach the state it names without
  changing `src/`; that is a valid reason to prune, written as such.
- **B2. Which paths get a new acceptance test.** Every declared path of a live StRS that has no
  counting `@accepts_req StRS-X#S<n>` on CR-504's head. A path already accepted by an existing
  `test/integration` test (re-marked by CR-504) keeps that test, which stays where it is. Waived
  StRS: none (D15).
- **B3. Acceptance layout (D8).**
  - Each e2e group of `test/shared/e2eGroups.ts` that has a path to accept in real VS Code gets
    `test/integration/acceptance/<group>.acceptance.ts`. The StRS of a scope go in the file of the
    group with the same id (scope `rendering-core` → `rendering-core.acceptance.ts`).
  - **One file = one launch = one window.** Every test of the file runs in that one window, in
    sequence, one `step()` per test (`test/integration/stepWatchdog.ts`). No test opens a fresh
    window.
  - A group that needs another kind of window (Restricted Mode, the built VSIX) or that passes the
    launch budget (B6) gets a second file `<group>.<kind>.acceptance.ts`, for example
    `trust-security.restricted.acceptance.ts`, `trust-security.vsix.acceptance.ts`,
    `lifecycle-sync.2.acceptance.ts`. Each file stays under the `test/` limit of
    `scripts/check-file-sizes.mjs` (1500 lines) and is split when needed; nothing is added to the
    size baseline.
  - Each file exports `run(): Promise<void>` and its window kind (`trusted`, `restricted`,
    `vsix`). The window kind decides how `run-tests.ts` launches it: `trusted` as `runScenario`
    does today (workspace file, test profile, CDP port when the file needs one), `restricted` as
    `runUntrustedScenario`, `vsix` as in B5.
  - `test/integration/acceptance-suite.ts` is the extension-tests entry of every acceptance
    launch. It reads the file to run from `STUDIO_ACCEPTANCE_FILE` (passed in
    `extensionTestsEnv`), wraps it in `withSuiteWatchdog`, and fails when the file does not exist.
  - Each acceptance test has a JSDoc line naming the path in words, then one
    `// @accepts_req StRS-X#S<n>` marker (one path per test, Q3). It reuses the existing helpers
    (`extensionApi.ts`, `windowFocus.ts`, `storedChoices.ts`, `previewEditingHelpers.ts`,
    `realInput/`), and its fixtures go under `test/integration/fixtures/acceptance/<group>/`.
  - The test asserts the final result of the path (the file on disk, the rendered page, the
    message posted), plus the steps no SwRS covers; it waits only on states the product reports
    (ci.guidelines rule 12), never on time.
- **B4. Runner, scripts and targets.**
  - `test/integration/run-tests.ts` gains `--acceptance-only` and `--group <id>`.
    `--acceptance-only` runs only acceptance files (no `scroll-sync`, `untrusted`, `trusted`,
    `standalone`, reverse-migration or reload suite). `--group <id>` keeps the files of that group;
    an id that `isGroupId` refuses fails before any VS Code starts. Without `--group`, every
    group's files run in `GROUPS` order.
  - Reports go under `out/reports/acceptance/<group>/`: `acceptance-manifest.json` with the shape
    of `integration-manifest.json` (`status`, `command`, `campaignCommand`, `runId`, `instanceId`,
    `campaignStartedAt`, `startedAt`, `completedAt`, `revision`, `dirty`, `scope`, where `scope` is
    the group id), plus `launches: [{file, kind, status, durationMs}]` so the first CI run gives
    the measured durations. A new `ACCEPTANCE_REPORT_ROOT` in `test/reportPaths.ts`
    (`out/reports/acceptance`).
  - `package.json`: `"test:acceptance": "npm run compile && npm run bundle && node
    out/test/integration/run-tests.js --acceptance-only"`; a group is passed after `--`.
  - `scripts/e2e-campaign.mjs`: a third stage, `acceptance`. `begin acceptance` behaves as
    `begin integration` (pinned `STUDIO_E2E_RUN_ID` wins, campaign file
    `out/reports/e2e/campaign-acceptance.json`). The two-stage assumptions (`sibling`) become "the
    other stages". `report` (all stages) requires the acceptance stage: it reads every
    `out/reports/acceptance/<group>/acceptance-manifest.json`, fails when a group of the matrix
    (B7) has no manifest or a manifest not `passed`, and writes the merged
    `out/reports/acceptance/acceptance-manifest.json` (one entry per group). `report --visual-only`
    lists `acceptance` as skipped beside `integration`.
  - `justfile`:
    - `ci-acceptance GROUP=""`: `_require-unlocked-screen "ci-acceptance"`, then
      `eval "$(node scripts/e2e-campaign.mjs begin acceptance)"`, then
      `{{ npm }} run test:acceptance` (with `-- --group "$GROUP"` when a group is given), ending in
      `ci-acceptance: passed` or `ci-acceptance: FAILED`. The group comes in as a quoted argument,
      never spliced into the script.
    - `preflight` runs `just ci-acceptance` after `just ci-integration` and before `ci-report`, with
      the same screen-locked handling (exit 3 skips report and gallery with a line naming
      acceptance). On Windows it stays skipped with the existing line, which now names acceptance.
    - `ci-hang-dump` is reused unchanged in the acceptance job.
  - `scripts/run-e2e.mjs` (`just e2e`) is not changed: `preflight` is the full local gate.
- **B5. The built-VSIX window (TRUST-012).** TRUST-012's path starts from the built VSIX (Q15) and
  is accepted in VS Code (D7). `trust-security.vsix.acceptance.ts` runs in a launch whose
  extension under test is the unpacked VSIX: the runner calls `npm run package`, unzips the VSIX's
  `extension/` folder into the run's temporary folder and passes that folder as
  `extensionDevelopmentPath`. The test then checks what the reader sees from that package (the
  declared icon file and its 256 by 256 PNG, the visible texts named by the path). Packaging
  happens before the launch, so the launch deadline does not count it.
- **B6. Budget (Q37).**
  - Expected healthy duration: an acceptance step (one path) takes **5 to 30 s** (open a fixture,
    open the preview, a few inputs, assert the file and the page); a window start takes about
    1 minute. The largest group on the base (lifecycle-sync, 18 paths, fewer once CR-504's
    accepted paths are subtracted) is then at most about 10 minutes in one launch.
  - Each step uses the default budget `STEP_BUDGET_DEFAULT_MS` (3 min). No acceptance step goes
    into `STEP_BUDGETS_MS`. Each launch keeps `LAUNCH_DEADLINE_MS` (15 min); no
    `STUDIO_LAUNCH_TIMEOUT_MS` is set.
  - Split rule: a launch whose healthy duration (local, or the first CI run) passes 7.5 minutes,
    half its deadline, is split into a second file of the group (B3). A step whose healthy
    duration passes 90 s is split into two paths' worth of steps if it holds two, else reported
    (stop list).
  - **No stress-plan entry**: the acceptance tests are not added to `test/shared/stressPlan.ts`;
    they are walks of paths already locked by SwRS tests, not new flake-prone real-window
    scenarios. A flake found later follows ci.guidelines rule 12 like any real-window test.
- **B7. CI job `acceptance` (`.github/workflows/ci.yml`).**
  - Trigger: the same `needs` and `if` as `integration` (`needs: release-check`; push to `main`,
    or a heavy dispatch).
  - `runs-on: ubuntu-latest`, `permissions: contents: read`, the same setup steps as
    `integration` (checkout with LFS, LFS pull and fsck, setup-node from `.nvmrc`, setup-uv,
    setup-just 1.58.0, `just dev-ci`).
  - `strategy: matrix: group: [...]` with `fail-fast: false`. The list is the groups that have at
    least one `test/integration/acceptance/<group>*.acceptance.ts` file, in `GROUPS` order (all 16
    once the CR is complete).
  - Test step: `xvfb-run --auto-servernum -s "-screen 0 2600x1440x24" just ci-acceptance
    "${{ matrix.group }}"` with `STUDIO_VIEWPORT_GUARD: strict`. Timeouts start at the job's 30 and
    the step's 20 minutes (rule 11 for VS Code jobs); after the first heavy dispatch they are set
    to about twice the slowest shard's measured healthy duration, never above 30 and 20, and never
    raised to make a run pass.
  - Then `just ci-hang-dump` (`if: always()`), then the upload (`if: always()`) of `out/reports/`
    as `e2e-acceptance-${{ matrix.group }}-attempt-${{ github.run_attempt }}`.
  - Job output `artifact: e2e-acceptance-*-attempt-*`. A matrix job has one output for all its
    shards, and "Re-run failed jobs" re-runs only the failed shards, so a consumer can hold
    attempt 1 of one group and attempt 2 of another. The consumer therefore downloads every
    acceptance artifact of the run and keeps, per group, the newest attempt (B8).
  - The `heavy` input's description names the acceptance job beside integration and stress.
- **B8. Consumers of the acceptance results.**
  - `report`: `needs: [release-check, visual, integration, acceptance]`. A download step
    (`if: needs.acceptance.outputs.artifact != ''`) takes `pattern:
    ${{ needs.acceptance.outputs.artifact }}` into `out/ci-artifacts/acceptance/` without
    `merge-multiple`, so each artifact keeps its own folder. `ci-report` then copies, for each
    group, `out/reports/acceptance/<group>/` from the folder with the highest attempt into
    `out/reports/acceptance/<group>/`, before `e2e-campaign.mjs report`. That selection lives in a
    script called by `ci-report` (rule 1 and 3: no inline logic in the workflow), not in the
    workflow. A red acceptance shard fails `report`, so `checks`.
  - `checks`: unchanged list; it takes acceptance through `report` (as it takes integration).
  - `tag-release`: `needs: [checks, release-check, integration, acceptance, stress]`. On a version
    change it tags only when `checks`, `integration`, `acceptance` and `stress` are `success`; the
    "Release not tagged" summary lists the acceptance result.
  - `pages`: `needs` adds `acceptance`; `reports_from_caller` also requires
    `needs.acceptance.result == 'success'`. The merged `studio-reports` artifact of `report`
    carries the acceptance stage, so `pages.yml` and `scripts/select_e2e_run.py` need no other
    change.
  - `gallery`: unchanged (it reads integration captures only).
- **B9. Scenario coverage gate (D11).** `scripts/check_scenario_coverage.py`:
  - runs `okfreq generate-report requirements --output-json
    out/reports/requirements/scenario-coverage-report.json` itself (through the same
    `uv run --no-sync --group requirements okfreq` command as the justfile), then reads it;
  - for each record of `requirements[]` whose `frontmatter.req_lifecycle` is live:
    - a SwRS that is not exempt (`diagnostics.exempted` false) with a non-empty
      `transitions.missing` → one line `<path>: SwRS-X: scenarios not tested: S2, S3`;
    - a StRS with `stakeholder_test_coverage.paths.accepted < paths.total` and no
      `acceptance_exemption` → `<path>: StRS-X: paths not accepted: <ids>` (the ids are the
      declared ones with no counting `@accepts_req`, from the report's per-path data or, when the
      report gives counts only, from `okfreq trace requirements --json` `scenario_markers`);
    - a StRS with no `scenarios:` in its frontmatter → `<path>: StRS-X: no scenarios: declared`;
  - fails (exit 1) when it prints any gap; it refuses a report whose
    `stakeholder_test_coverage.mode` is not `linked-swrs-and-acceptance-paths` (exit 2, one line
    naming the mode found);
  - on success prints `scenario coverage: <s> SwRS scenarios tested, <p>/<P> StRS paths accepted,
    all complete`;
  - runs as the last line of `just requirements-lint`
    (`uv run --no-sync --group requirements python scripts/check_scenario_coverage.py
    requirements`);
  - tests: `test/build/test_check_scenario_coverage.py`, added to `just release-tests`. One case
    per failure rule and one for the wrong mode use prepared reports (a refusal the shipped bundle
    cannot hold), and one case runs the script on the shipped `requirements/` bundle at the head
    and expects the success line.
  - It lands in the same commit as the switch (B10).
- **B10. Mode switch (Q27).** In one commit, the last of the CR:
  - `requirements/config.yml`: `strs_test_coverage_mode: linked-swrs-and-acceptance-paths`;
  - B9's script and its `requirements-lint` line;
  - `just requirements-update`, and every file it generates committed (`tested_in_files` and
    `accepted_in_files` on StRS, the coverage and OKF fields, the Links);
  - a `requirements/tiers/log.md` entry (B12);
  - the viewer's "StRS covered" card caption: it follows the new rule ("covered: linked SwRS
    covered or exempt, and every path accepted"), with its `home.test` updated, and the viewer's
    SwRS updated to say so.

  Generated fields are not normative: writing `tested_in_files` and `accepted_in_files` on the 15
  approved StRS changes neither `approved_at` nor `approved_by` and needs no owner agreement.
- **B11. Docs.**
  - `requirements/guidelines/project.guidelines.md` "Benches" (D14 completion): the acceptance
    layout (B3), the window kinds, the `acceptance` job and its matrix, `just ci-acceptance
    [GROUP]`, the budget and split rule (B6), the D11 gate, and the new-mode meaning of
    "covered". The "added by the acceptance CR" wording of CR-504 is replaced.
  - `CONTRIBUTING.md`: the CI section lists the `acceptance` job (heavy, matrix by group, push to
    `main` and heavy dispatch), `just ci-acceptance [GROUP]`, how to run one group locally, and the
    D11 gate in the checks section.
  - `AGENTS.md` "Main targets": the CI jobs line names `just ci-acceptance [GROUP]` (heavy, in
    parallel in CI, in sequence in `just preflight`).
  - `.agents/guidelines/ci.guidelines.md`: rule 11 names the acceptance job's timeouts (job and
    step, and that they come from the measured duration); rule 13 lists `acceptance` with
    `integration` and `stress` as real VS Code jobs (push to `main`, heavy dispatch, never a pull
    request) and says a red shard fails `report` then `checks`; rule 14 and "Recovering from a red
    heavy job" name `acceptance` among the jobs `tag-release` requires, and item 4 explains the
    per-group artifacts and the newest-attempt selection (B8).
  - `.agents/glossary/common.md`: "acceptance job", "acceptance file" (one file, one window).
  - No change to the writing skill `skills/writing-for-markdown-okf-schema-studio/`: no rendered
    syntax changes.
- **B12. Log.** `requirements/tiers/log.md`, one entry under `## 2026-11-<day>` with
  `### Topic` sub-headings: the scenario tests and every pruned scenario with its reason (Q30b);
  the mode switch with the before and after figures (StRS covered, paths accepted, scenarios
  tested).
- **B13. No SwRS for tooling.** The acceptance runner, the CI job and the D11 script are
  development tooling, like `scripts/check_main_paths.py` and `run-tests.ts`: they get no SwRS and
  no `@implements_req`. The viewer caption (B10) updates the viewer SwRS that CR-504 touched.
- **B14. `src/` is out of reach.** A path or scenario that the product does not do as written is
  not fixed here (stop list).

## What changes, area by area

### 1. SwRS scenario tests and prunings (Q30, Q30b, B1)

- Start from CR-504's PR-body list of untested scenarios, recounted on its head with
  `okfreq trace requirements --json` (`scenario_markers`) against the `scenarios:` of every live,
  non-exempt SwRS.
- For each: write the test (B1) with `@tests_req SwRS-X#S<n>`, or prune the scenario: remove its
  `scenarios:` entry and its `### Scenario S<n> …` body section; ids are never reused. A proposed
  SwRS may be pruned by the coder with the reason; an approved one goes to the owner (stop list).
- The PR body has a table: SwRS, scenario, outcome (test file, or pruned with its reason).

### 2. Acceptance tests (Q1, Q3, Q6, Q32, D7, B2, B3, B5)

- For each path of B2, one test, in the group file of B3, or on the D7 bench for CORE-007, CORE-008
  and TRUST-014.
- CORE-006: the agent's writing is a simulated input: the test writes the Markdown that the skill
  teaches into a fixture and walks the path in the window.
- CORE-007 S1: the test walks the release path up to the review and stops before CORE-078 (the
  maintainer's review); it asserts the gate (no release without the review input) and the content
  it can check.
- The PR body has a table: StRS, path, test file, bench.

### 3. Runner and targets (B4, B5, B6)

`test/integration/run-tests.ts`, `test/integration/acceptance-suite.ts`,
`test/integration/acceptance/*.acceptance.ts`, `test/reportPaths.ts`, `package.json`,
`scripts/e2e-campaign.mjs`, the acceptance-artifact selection script called by `ci-report`,
`justfile` (`ci-acceptance`, `preflight`, `ci-report`). Unit tests for the new runner arguments
(group refused before launch), the campaign stage and the newest-attempt selection go in
`test/build/` next to the existing ones (`hangWatchdog.test.ts`, `stressPlan.test.ts`).

### 4. CI (B7, B8)

`.github/workflows/ci.yml` (`acceptance`, `report`, `tag-release`, `pages`, the `heavy`
description). `test/build/test_workflows.py` gains, reading the shipped `ci.yml`, `justfile` and
`test/shared/e2eGroups.ts`:

- the `acceptance` job has a `timeout-minutes` and its test step a smaller one, runs under
  `xvfb-run` with the 2600x1440x24 screen, has the same `if` as `integration`;
- its matrix equals the groups that have an acceptance file, in `GROUPS` order;
- its upload name ends with `-attempt-${{ github.run_attempt }}`, its `artifact` output matches
  that name, and `report` downloads by that output without `merge-multiple`;
- `report`, `tag-release` and `pages` need `acceptance`, the tag condition and
  `reports_from_caller` require its success;
- `ci-acceptance` stops on a locked screen (the existing parametrised test gains it), and
  `preflight` runs it after `ci-integration` and before `ci-report`.

### 5. Gate and switch (B9, B10)

`scripts/check_scenario_coverage.py`, `test/build/test_check_scenario_coverage.py`,
`justfile` (`requirements-lint`, `release-tests`), `requirements/config.yml`, the generated
requirement files, `requirements/tiers/log.md`, `test/site/requirementsViewer/home.ts` and its
test.

### 6. Docs (B11)

`requirements/guidelines/project.guidelines.md`, `CONTRIBUTING.md`, `AGENTS.md`,
`.agents/guidelines/ci.guidelines.md`, `.agents/glossary/common.md`. After the changes,
`just requirements-update`, and the generated files committed.

## Commit order

Every commit leaves `just check` and `just requirements-lint` green, and passes CR-504's scratch
new-mode validation (a copy of `requirements/` with the new mode, `okfreq validate <scratch>
--check-links --project-root .`) with 0 errors, until the switch makes it the real one.

1. The runner, the campaign stage, `test:acceptance`, `ci-acceptance`, `preflight`, the `acceptance`
   job and its consumers, `test_workflows.py`, and the first group's acceptance file (the group the
   coder picks to prove the job; `trust-security` is advised, since it exercises all three window
   kinds). The matrix lists that group only.
2. Per e2e group, in `GROUPS` order (one commit per group, or several): that scope's SwRS
   scenario tests and prunings, its acceptance file(s) or D7 tests, its matrix entry, its
   log lines.
3. The docs (B11).
4. Last: the gate and the switch (B9, B10), `just requirements-update`, the log entry.

After commit 1, the coder runs a heavy dispatch on the branch (`gh workflow run ci.yml --ref
<branch> -f heavy=true`) to measure the first shard, then sets the job and step timeouts (B7).

**Partial delivery (acceptance-Q2).** When the coder sees that the remaining groups do not fit in
its 3 rounds, it stops after a green commit of step 2, with the mode unchanged and no D11 gate,
and reports the groups done and the groups left. The Chief of Staff then splits the rest per group;
the switch and the gate land in the last of those CRs.

## Out of scope

- Any change to `src/`: a bug found on the way is filed and reported (stop list), not fixed here.
- Any change to okf-schema itself.
- A simulated walk for every path (D9): `@tests_req StRS-X#S<n>` stays where CR-504 left it.
- Counting passing tests rather than markers (Q35).
- Retired requirements beyond CR-504's D5 exemptions.
- Normative changes to approved requirements, including pruning a scenario of one.
- A stress-plan entry for the acceptance tests (B6).
- `scripts/run-e2e.mjs` (`just e2e`) and the `gallery` job.
- A waiver on any StRS (D15).

## CI environment

- **Where the job runs.** `acceptance` runs on `ubuntu-latest` GitHub runners, one runner per
  group, under `xvfb-run` with a 2600x1440x24 screen, set up by `just dev-ci` from the lock files
  (the npm and uv caches of the setup actions, as `integration`). It runs on pushes to `main` and on
  a heavy dispatch, never on a pull request (rule 13).
- **What the runner lacks that a developer's machine has.** No installed VS Code, no
  `STUDIO_VSCODE_EXECUTABLE`, no warm `.vscode-test` folder: each shard downloads VS Code through
  `@vscode/test-electron` before its first launch (the launch deadline does not count it). No
  `out/` build: `test:acceptance` compiles and bundles; the vsix window also packages. No real
  display or GPU: Xvfb. No screen lock. Network access is needed for the VS Code download and
  `just dev-ci`.
- **Local proof before the push.** The coder works on Windows, where `just preflight` runs the
  static stage only and skips acceptance (`ci-acceptance` needs Linux or macOS). Before the push:
  `just check` and `just requirements-lint` (static), `just release-tests` (the workflow and gate
  tests read the shipped `ci.yml`, `justfile`, `e2eGroups.ts` and `requirements/`), and
  `just ci-static`. On a macOS or Linux machine, `just ci-acceptance <group>` gives the same result
  as the CI shard.
- **What only the first CI runs prove.** The real durations per shard (they set the timeouts,
  B7); that 16 parallel shards each download VS Code and pass; the `vsix` window built and unpacked
  on the runner; the per-group artifacts and the newest-attempt selection on a real re-run (check
  10 below).

### Host matrix

| Host | `just preflight` | `just ci-acceptance [GROUP]` |
|---|---|---|
| Windows (developer) | static stage only; prints that acceptance is skipped and CI runs it | not run (the recipes need Linux or macOS VS Code launch support, as `ci-integration`) |
| macOS (developer) | runs `ci-acceptance` after `ci-integration`; exit 3 on a locked screen | runs, one window at a time |
| Linux CI, pull request | not run | not run (`report` lists acceptance as skipped) |
| Linux CI, push to `main` or heavy dispatch | not run | one shard per group, in parallel |

## Evidence

Every check on a shipped file reads it from the repository at the head under test.

### Checks

1. On the head, `requirements/config.yml` has `strs_test_coverage_mode:
   linked-swrs-and-acceptance-paths`.
2. `just requirements-lint` passes. Its output ends with `scenario coverage: <s> SwRS scenarios
   tested, <P>/<P> StRS paths accepted, all complete`, and `okfreq validate` prints no error, no
   W003 and no W004. The PR body quotes those lines.
3. `out/reports/requirements/scenario-coverage-report.json` (written by the gate on the head)
   shows, for every live StRS, `paths.accepted == paths.total` and `status: covered`; for every
   live, non-exempt SwRS, an empty `transitions.missing`; no StRS carries `acceptance_exemption`.
   The PR body gives "live StRS covered M/M, paths accepted P/P, scenarios tested S/S".
4. `just release-tests` passes, with `test_check_scenario_coverage.py` (each failure rule and the
   wrong mode fail on prepared reports; the shipped bundle passes) and the new
   `test_workflows.py` cases.
5. `just check` passes: check-markers with CR-504's D10 rules (every `@accepts_req` under
   `test/integration/` or on a D7 StRS, every fragment declared), check-limits (no acceptance file
   over 1500 lines, no baseline growth), the new unit tests of the runner, campaign and selection.
6. A scan of `test/integration/acceptance/` shows one `@accepts_req` per test, each naming a
   declared path, and no `@tests_req StRS-…`.
7. Every pruned scenario is in the PR table and in `requirements/tiers/log.md` with its reason; no
   approved requirement lost a scenario.
8. `just preflight` passes (on Windows the static stage; CI runs the rest).
9. A heavy dispatch on the branch head is green for `integration`, `report` and every `acceptance`
   shard (16 at the end). The PR body gives the run link, each shard's measured duration, the
   timeouts set from them, and each `acceptance-manifest.json` `launches` durations.
10. On that run, `gh run rerun <run-id> --job <job-id of one acceptance shard>`: the re-run shard
    uploads `-attempt-2`, `report` re-runs and merges attempt 2 of that group with attempt 1 of the
    others (its log names the attempt kept per group). The PR body gives the run link.

### Scenario steps (owner's view)

1. Build the site from the heavy run's reports (`just ci-report`, `just ci-gallery`) and open the
   requirements viewer home: "StRS paths accepted" shows P/P, "StRS covered" M/M, "SwRS scenarios
   tested" S/S, and the "StRS covered" caption states the new rule.
2. Open StRS-MDOKFSTUDIO-LIFE-023: each of S1 to S4 lists an accepted file under
   `test/integration/`.
3. Open StRS-MDOKFSTUDIO-CORE-007: S1 lists its D7 acceptance test.
4. Remove the `@accepts_req` line of one acceptance test and run `just requirements-lint`: it
   fails with `StRS-X: paths not accepted: S<n>` and W004 appears if it was the StRS's only one.
   Restore the file.
5. In Actions, open a heavy run: the `acceptance` job shows one shard per group, each with its
   `e2e-acceptance-<group>-attempt-<n>` artifact.

## Self-containment

The coder needs this spec, CR-504's `03-change-spec.md` and `02-answers.md`, CR-504's PR body (the
untested scenarios list and the marker sort table), the okf-schema 0.18.1 docs named at the top
and the repository's own rules.

## The coder stops and reports to the Foreman when

- CR-504 is not final, or its head differs from what this spec builds on (no `scenarios:`, no D10
  rules, no `accepted_in_files` in `generated_fields`).
- A path or scenario cannot pass because the product does not do what it says: the coder files the
  bug with the failing step and reports; it neither fixes `src/` nor changes the requirement.
- A scenario or path of an **approved** requirement would have to be removed or reworded, or an
  approved SwRS turns up.
- A StRS seems to have no step that can be automated (a waiver candidate): it goes to the owner;
  the coder never writes `acceptance_exemption`.
- A step's healthy duration needs more than its default budget, or a launch cannot stay under the
  15-minute deadline after the B6 split: the coder reports instead of raising a timeout.
- The vsix window (B5) cannot be built or loaded on the runner.
- `okfreq` 0.18.1 behaves differently from its released docs on a point this spec relies on (the
  report fields read by B9, W003 or W004, the covered rule).
- The remaining groups do not fit in its 3 rounds (partial delivery, above).

## Open questions

None. Every point the answers left open is decided above (B1 to B14) and named as this spec's
decision; the owner said "no question".
