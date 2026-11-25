# StRS acceptance tests, acceptance job and okfreq mode switch (CR-B)

This CR is the second half of the okfreq 0.18 work. CR-504 (`strs-path-validation`, CR-A) did
four things, still in the old coverage mode:

- it declared every StRS path and every SwRS scenario;
- it sorted the markers;
- it taught the marker check the `@accepts_req` verb;
- it built the viewer cards.

This CR finishes the job:

- every declared SwRS scenario gets a test, or is pruned with a reason;
- every live StRS path gets an acceptance test (`@accepts_req StRS-X#S<n>`) that walks it in real
  VS Code. The tests live in acceptance files, one or more per e2e group, under
  `test/integration/acceptance/`;
- a new heavy CI job, `acceptance`, runs those files in a matrix by group, with one shared window
  per file;
- a gate (D11) fails `just requirements-lint` when a scenario is untested or a path is not
  accepted;
- the bundle switches to `strs_test_coverage_mode: linked-swrs-and-acceptance-paths`. In that mode
  a StRS is `covered` only when its linked SwRS are covered and every path is accepted, so the
  viewer shows the honest number.

For the owner: after this CR, a stakeholder requirement is "covered" when a test walks each of its
main paths in the real editor and every behaviour scenario has its test.

Short name: `strs-acceptance`.

**This CR depends on CR-504.** It is stacked on CR-504's branch
(`chantier/batch-09/cr-504-strs-paths-and-swrs-scenarios-declared-o`) and starts from its head.
It cannot start before CR-504 is final, because it builds on what CR-504 adds:

- the `scenarios:` declarations and the `#S<n>` fragments;
- the `@accepts_req` marker check (D10);
- `accepted_in_files` in `generated_fields`;
- the viewer cards.

The Chief of Staff records the dependency in `depends.json`.

Sources:

- This CR folder: `01-intent.md`, and `02-answers.md` acceptance-Q1 to acceptance-Q3.
  acceptance-Q3 applies every finding of `work/critic-r1.md`.
- CR-504's folder, `changes/4-batch/1-pending/504-strs-path-validation/`:
  - `03-change-spec.md`: the whole spec, and its last section "Handed to the next CR (CR-B)",
    which is this CR's scope;
  - `02-answers.md` Q27 to Q42 (Q1, Q3, Q6, Q28, Q30, Q30b, Q32, Q35, Q37, Q39, Q40, Q41 and Q42
    apply here).
- The released okf-schema 0.18.1 documentation, tag `v0.18.1`
  (<https://okf-schema.readthedocs.io/en/stable/>):
  - `reference/okfreq-acceptance-paths`: mode comparison, combination table, counters, findings
    W003 and W004, report fields;
  - `explanation/okfreq-acceptance-paths`: execution cost and the waiver;
  - `reference/okfreq-configuration`: `strs_test_coverage_mode` and `generated_fields`;
  - `reference/okfreq-cli`: `generate-report --output-json` and `trace --json`.

The project rules apply as written, and this spec does not restate them: the constitution
(`.agents/constitution.md`), `AGENTS.md`, `requirements/guidelines/requirements.guidelines.md`,
`requirements/guidelines/project.guidelines.md` and `.agents/guidelines/ci.guidelines.md`.

## Figures

The figures below were counted on `origin/main` at `4a47151e`, the commit CR-504's spec counts
on. CR-504 has not started, so they are counted before its changes. CR-504 changes them in three
ways: new paths for BLOCK-027, TRUST-012 and TRUST-014; the marker sort; and the SwRS sweep. The
coder recounts every figure on CR-504's head and puts the recounted figures in the PR body.

- **Live StRS:** 95 (15 approved, 80 proposed), with 151 paths ("live" excludes deprecated and
  superseded).

  | Scope | Live StRS | Paths |
  | --- | --- | --- |
  | block-editing | 9 | 16 |
  | code-blocks | 2 | 3 |
  | diagrams | 5 | 9 |
  | frontmatter-editing | 3 | 4 |
  | frontmatter-schema | 4 | 7 |
  | gfm | 3 | 4 |
  | layout-width | 3 | 6 |
  | lifecycle-sync | 9 | 19 |
  | myst | 9 | 15 |
  | palette-slash | 9 | 14 |
  | rendering-core | 6 | 8 |
  | review-annotations | 7 | 12 |
  | table-editing | 8 | 12 |
  | theme-zoom | 3 | 4 |
  | toolbar-navigation | 9 | 13 |
  | trust-security | 6 | 5 |

- **`@tests_req StRS-…` lines: 185.**
  - 101 are in `test/integration`, in 46 files;
  - 74 are in `test/visual`;
  - 10 are elsewhere: 4 in `test/security`, 2 in `test/build`, 2 in `test/core`, 1 in `test/page`
    and 1 in `test/site`.
  - No `@accepts_req` exists yet.
  - CR-504 turns into `@accepts_req` the lines whose test walks a path in real VS Code. Its sample
    audit predicts that about one path in four is accepted after CR-504.
- **The untested SwRS scenarios** are the list in CR-504's PR body ("Scenarios that no marker
  covers after the sweep"), recounted on its head.
- **Generated fields on StRS.** In the old mode, `okfreq update-coverage` removes
  `tested_in_files` and `accepted_in_files` from every StRS, even when they are listed in
  `generated_fields`. So on CR-504's head no StRS carries either field. The mode switch (B10)
  writes them for the first time. In the new mode, a SwRS's `tested_in_files` lists only the files
  with counting markers, so some SwRS lists can shrink. The coder gives these figures after
  `just requirements-update`.

## What okf-schema 0.18.1 does in the new mode (the contract)

This section covers the released behaviour, and only what this CR relies on.

- **The setting:** `strs_test_coverage_mode: linked-swrs-and-acceptance-paths` in
  `requirements/config.yml`.
- **When a StRS is `covered`:** both conditions hold.
  - It has at least one linked SwRS, and each one is `covered` or `exempt`. A SwRS is exempt when
    it has an `annotation_exemption` with a non-blank `exemption_reason`.
  - Every declared path has a counting `@accepts_req StRS-X#S<n>`, or the StRS has a justified
    `acceptance_exemption`.

  "Tested" (`@tests_req StRS-X#S<n>`) is reported, but it does not change the status.
- **When a SwRS is test-covered:**
  - a SwRS that declares `scenarios:` needs a counting `@tests_req SwRS-X#S<n>` for every `S<n>`;
  - a SwRS without `scenarios:` (TRUST-070 and TRUST-075, Q39) is covered by a `@tests_req`
    without a fragment, as before.
- **Errors and warnings:**
  - Fragment errors make `okfreq validate` and `okfreq lint` exit 1: a declaring target without a
    fragment, an unknown fragment, or `@accepts_req` on a SwRS.
  - The schema check also requires the SwRS schema to refuse `accepted_in_files`.
  - W003 (a live StRS with no `scenarios:`) and W004 (a live StRS with no counting `@accepts_req`
    and no waiver) are printed and never change the exit code.
- **Generated fields:** in the new mode, `okfreq update-coverage` writes the fields listed in
  `generated_fields`:
  - `tested_in_files` (counting files only) on SwRS and StRS;
  - `accepted_in_files` on StRS.
- **The JSON report:** `okfreq generate-report requirements --output-json FILE` writes
  `format_version` 2.
  - Each record of `requirements[]` carries `frontmatter` (so `req_lifecycle` and `scenarios`),
    `tier` and `diagnostics.exempted`.
  - A StRS adds `stakeholder_test_coverage`, with `status`, `paths` (counts only: `total`,
    `tested`, `accepted`), `accepted` and `acceptance_tests`. It adds `acceptance_exemption` only
    when a justified waiver is set.
  - A SwRS that declares scenarios adds `transitions: {tested: [...], missing: [...]}`.
- **The trace:** `okfreq trace requirements --json` gives, for each requirement, its
  `scenario_markers`, the markers per fragment. This is where a gap's path ids are read.
- "Live" means every lifecycle except `deprecated` and `superseded`.
- `okfreq` counts markers; it never reads test results. The proof that a test passes is its
  bench's CI job (Q35).

## Decisions

### Carried from CR-504's answers (02-answers Q27 to Q42) and its spec

- **Q1:** an automated end-to-end test of a StRS path is an acceptance test.
- **Q3:** one nominal path per acceptance test.
  - The test runs end to end in one go.
  - It asserts the final result, plus the steps that no SwRS covers.
  - It never covers edge cases or errors.
- **Q6:** a human step is a simulated input.
  - The test asserts the system's gate (blocked without the step, proceeds with it) and the
    content it can check, never a judgment.
  - Another way to verify a step is a rare exception, written in the path.
- **Q27:** switch the mode and show the honest number.
- **Q28:** the bench convention.
  - `@tests_req StRS-X#S<n>` means the path is walked on the simulated bench, which runs on every
    PR.
  - `@accepts_req StRS-X#S<n>` means the path is walked in real VS Code (`test/integration`, run
    on pushes to `main`).
  - The only exception is D7.
- **Q30, Q30b:** a SwRS never keeps a scenario without a test.
  - By default, the coder writes the test.
  - It removes a scenario only when another scenario or SwRS already says the same thing, or when
    the scenario cannot be observed.
  - Every removal is listed in the PR with its reason and logged in `requirements/tiers/log.md`.
- **Q32, D15:** a waiver (`acceptance_exemption`) is only for a StRS with no step that can be
  automated.
  - There are **no** waiver candidates, and the coder never writes a waiver.
  - CORE-006: the agent's writing is a simulated input.
  - CORE-007: its acceptance test stops before CORE-078, the maintainer's review.
- **Q35:** counts are based on markers, as okfreq counts them. The proof that a test passes is its
  bench's CI job.
- **Q37:** the acceptance budget.
  - One shared window per e2e group.
  - A group may use several launches, each with its own budget under the 15-minute launch
    deadline.
  - The job is sharded by group in a matrix.
  - The spec states the expected step duration.
  - No stress-plan entry, and the spec says so.
  - No fresh window per test, and no raised timeouts.
- **Q39:** TRUST-070 and TRUST-075 (both exempt) have no `scenarios:`. D11 asks nothing of them.
- **Q40:** D11 runs `okfreq generate-report --output-json` into `out/` itself, and lands with the
  switch.
- **Q41, D7:** three StRS may be accepted on the test closest to their product, under
  `test/build`, `test/security`, `test/site` or `test/core`:
  - CORE-007 (the release);
  - CORE-008 (the site);
  - TRUST-014 (the built VSIX).

  CORE-006 (the writing skill) and every other StRS, TRUST-012 included, are accepted in real
  VS Code.
- **Q42:** the CI wiring belongs to this CR.
  - `test:acceptance` includes `npm run bundle`.
  - `ci-acceptance` opens the e2e campaign the way `ci-integration` does.
  - `tag-release`, the pages build, `report` and `checks` take the acceptance results.
  - ci.guidelines rules 11, 13 and 14 apply.
  - The AGENTS.md CI list and CONTRIBUTING's CI section are updated.
  - The artifact of each attempt is named `-attempt-<n>` and announced through a job output.
- **D8:** the acceptance layout. B3 below gives the details.
- **D11:** the scenario coverage gate (B9).
- **D14 completion:** the "Benches" section of project.guidelines gets the acceptance layout and
  the job (B11).
- **acceptance-Q1:** scope and decisions come from CR-504, and this CR depends on it.
- **acceptance-Q2:** the delivery is as large as the Driver can make it in 3 rounds.
  - If the Driver reports that it cannot finish, the Chief of Staff splits the rest per e2e group,
    and the first group's PR adds the acceptance job.
  - The mode switch and the D11 gate land last.
- **acceptance-Q3:** every finding of the spec critic's round 1 is applied.
  - SwRS-MDOKFSTUDIO-CORE-076 is updated by this CR; there is no exception for tooling.
  - The docs about the job wiring land in commit 1.
  - The Foreman counts rounds (one round = one coder-to-Inspector cycle) and decides a partial
    delivery.

### Taken by this spec

- **B1. Where a missing SwRS scenario test goes.**
  - By default, on the bench where that SwRS's other scenario tests live: the files that already
    carry `@tests_req SwRS-X#S<m>`.
  - When the SwRS has none, on the cheapest bench that can observe the scenario:
    - for logic: `test/core`, `test/page`, `test/host-memory`, `test/session`,
      `test/node-services`, `test/site` or `test/build`;
    - for what only a rendered page shows: `test/visual`;
    - only when a real window alone can observe it: `test/integration`.
  - The test carries `// @tests_req SwRS-X#S<n>`, plus a companion line where the marker check
    asks for one.
  - A scenario is "not observable" when no bench can reach the state it names without changing
    `src/`. That is a valid reason to prune, and the reason is written as such.
- **B2. Which paths get a new acceptance test.**
  - Every declared path of a live StRS that has no counting `@accepts_req StRS-X#S<n>` on
    CR-504's head.
  - A path already accepted by an existing `test/integration` test (re-marked by CR-504) keeps
    that test, which stays where it is.
  - Waived StRS: none (D15).
- **B3. Acceptance layout (D8).**
  - **File per group.** Each e2e group of `test/shared/e2eGroups.ts` with a path to accept in
    real VS Code gets `test/integration/acceptance/<group>.acceptance.ts`. A scope's StRS go in
    the file of the group with the same id: scope `rendering-core` goes in
    `rendering-core.acceptance.ts`.
  - **Groups with no file.** A group whose paths are all accepted by tests that stay in place
    (B2), or by D7 tests on another bench, has no acceptance file.
  - **One file = one launch = one window.** Every test of the file runs in that one window, in
    sequence, one `step()` per test (`test/integration/stepWatchdog.ts`). No test opens a fresh
    window.
  - **A second file for a group.** A group gets a second file `<group>.<kind>.acceptance.ts` when
    it needs another kind of window (Restricted Mode, the built VSIX), or when it passes the launch
    budget (B6). Examples: `trust-security.restricted.acceptance.ts`,
    `trust-security.vsix.acceptance.ts`, `lifecycle-sync.2.acceptance.ts`.
  - **Size limit.** Each file stays under the `test/` limit of `scripts/check-file-sizes.mjs`
    (1500 lines), and is split (as above) when it would pass it. Nothing is added to the size
    baseline.
  - **What a file exports.** `run(): Promise<void>`, and its window kind: `trusted`, `restricted`
    or `vsix`. The kind decides how `run-tests.ts` launches it:
    - `trusted`: the way `runScenario` does today, through `@vscode/test-electron` `runTests`
      (workspace file, test profile, CDP port when the file needs one);
    - `restricted`: the way `runUntrustedScenario` does, by spawning VS Code directly;
    - `vsix`: as in B5, also spawned directly.
  - **The suite entry.** `test/integration/acceptance-suite.ts` is the extension-tests entry of
    every acceptance launch.
    - It reads the file to run from `STUDIO_ACCEPTANCE_FILE`. For a `trusted` launch the variable
      is passed in `extensionTestsEnv`; for the `restricted` and `vsix` launches it is passed in
      the `spawn` environment.
    - It wraps the file in `withSuiteWatchdog`, and fails when the file does not exist.
  - **Each test.**
    - A JSDoc line names the path in words, followed by one `// @accepts_req StRS-X#S<n>` marker
      (one path per test, Q3).
    - Trusted and restricted files reuse the existing helpers (`extensionApi.ts`,
      `windowFocus.ts`, `storedChoices.ts`, `previewEditingHelpers.ts`, `realInput/`). The vsix
      file does not (B5).
    - Fixtures go under `test/integration/fixtures/acceptance/<group>/`.
    - The test asserts the final result of the path (the file on disk, the rendered page, the
      message posted), plus the steps no SwRS covers.
    - It waits only on states the product reports, never on time.
  - **Not in the integration list.** Acceptance files are not rows of `INTEGRATION_TESTS` in
    `test/shared/e2eGroups.ts`, so its 41-row assertion in `test/site/e2eGroups.test.ts`, the
    gallery and the e2e listing do not change.
- **B4. Runner, scripts and targets.**
  - **Arguments.** Argument parsing moves out of `test/integration/run-tests.ts` into a pure
    module, `test/shared/runnerArgs.ts`.
    - It accepts the existing flags plus `--acceptance-only` and `--group <id>`.
    - It refuses an id that `isGroupId` refuses, and `--group` without `--acceptance-only`.
    - Its unit tests run before any VS Code starts.
    - `run-tests.ts` keeps its behaviour for the existing flags.
  - **`--acceptance-only`.**
    - It runs only acceptance files: no `scroll-sync`, `untrusted`, `trusted`, `standalone`,
      reverse-migration or reload suite.
    - It writes only the acceptance manifests, never `out/reports/e2e/integration-manifest.json`.
      The top-level manifest code of `run-tests.ts` (today it always writes that file on import)
      chooses the manifest by mode.
    - `--group <id>` keeps that group's files. Without `--group`, every group's files run in
      `GROUPS` order.
  - **Manifests.** Each group writes
    `out/reports/acceptance/<group>/acceptance-manifest.json`.
    - The shape is that of `integration-manifest.json`: `status`, `command`, `campaignCommand`,
      `runId`, `instanceId`, `campaignStartedAt`, `startedAt`, `completedAt`, `revision`,
      `dirty`, and `scope` (the group id).
    - It adds `pinnedRunId` (true when `STUDIO_E2E_RUN_ID` was pinned), so each group manifest
      carries its own campaign identity.
    - It adds `launches: [{file, kind, status, durationMs}]`, so the first CI run gives the
      measured durations.
    - A new `ACCEPTANCE_REPORT_ROOT` in `test/reportPaths.ts` (`out/reports/acceptance`).
  - **Hang dumps.** Acceptance launches keep the profile naming `/tmp/studio-*-d-*`, so
    `ci-hang-dump` finds them. The dumps go to `out/reports/e2e/hang-dumps/`, inside the shard's
    uploaded `out/reports/`.
  - **`package.json`:**
    `"test:acceptance": "npm run compile && npm run bundle && node out/test/integration/run-tests.js --acceptance-only"`.
    A group is passed after `--`.
  - **`scripts/e2e-campaign.mjs`** gets a third stage, `acceptance`.
    - `begin acceptance` behaves like `begin integration`: a pinned `STUDIO_E2E_RUN_ID` wins, and
      the campaign file is `out/reports/e2e/campaign-acceptance.json`.
    - Like every `begin`, it deletes `review.json` and `e2e-manifest.json`. That is intended: a new
      stage invalidates the last merged report.
    - The runner copies the campaign identity into every group manifest. `report` reads the
      acceptance identity from the group manifests, never from `campaign-acceptance.json`, which
      a CI report job does not have.
    - The two-stage assumptions are fixed: `sibling` becomes "the other stages", the
      `stageNames.join(" or ")` message lists the three stages, and the usage line reads
      `begin <visual|integration|acceptance>|report [--visual-only]`.
  - **`report` (all stages)** requires the acceptance stage.
    - **Expected groups.** The groups with at least one
      `test/integration/acceptance/<group>*.acceptance.ts` file in the checkout. This is the same
      list as the CI matrix, and the `test_workflows.py` check (B7) keeps the two equal.
    - **Failures.** `report` fails when an expected group has no manifest (a missing shard
      artifact), when a manifest is not `passed`, or when a group's identity is not valid. A valid
      identity is either the run id pinned by the visual and integration campaigns
      (`pinnedRunId` on all of them), or a `campaignStartedAt` less than two hours from the visual
      campaign's start (the existing rule).
    - **Output.** It writes the merged `out/reports/acceptance/acceptance-manifest.json`, with one
      entry per group, and adds the acceptance stage to `e2e-manifest.json`.
    - `report --visual-only` lists `skipped: ["integration", "acceptance"]`, with one console line
      for each.
  - **`justfile`:**
    - `ci-acceptance GROUP=""` runs:
      - `_require-unlocked-screen "ci-acceptance"`;
      - `eval "$(node scripts/e2e-campaign.mjs begin acceptance)"`;
      - `{{ npm }} run test:acceptance`, with `-- --group "$GROUP"` when a group is given.

      It ends with `ci-acceptance: passed` or `ci-acceptance: FAILED`. The group comes in as a
      quoted argument, never spliced into the script.
    - `preflight` runs `just ci-acceptance` after `just ci-integration` and before `ci-report`
      (rule 7), with the same handling of a locked screen: exit 3 skips report and gallery, with
      a line that names acceptance.
    - On Windows it stays skipped. The skip line reads "visual, viewer-graph, integration,
      acceptance, report and gallery stages skipped on Windows; CI runs them".
    - `ci-hang-dump` is reused unchanged.
  - `scripts/run-e2e.mjs` (`just e2e`) does not change. It does not run acceptance (B8 gives what
    that means for the Pages fallback).
- **B5. The built-VSIX window (TRUST-012).** TRUST-012's path starts from the built VSIX (Q15),
  and it is accepted in VS Code (D7).
  - **Packaging.** Before the launch, the runner calls `node scripts/package-extension.mjs`
    directly, which writes `out/reports/package/markdown-okf-schema-studio.vsix`.
    - It reuses the compile and bundle that `test:acceptance` already did. There is no
      `vscode:prepublish` script, so vsce rebuilds nothing.
    - It does not call `npm run package`, which would compile and bundle again.
    - Packaging time counts against the shard's 20-minute test step, not against the launch
      deadline.
  - **Unpacking.** A new `scripts/unpack_vsix.py` (Python standard library `zipfile`, run as
    `uv run --no-sync python -I scripts/unpack_vsix.py <vsix> <folder>`) extracts the VSIX's
    `extension/` folder into the run's temporary folder.
    - There is no new dependency.
    - It works on Linux, macOS and Windows, where Git Bash has no `unzip`.
  - **The launch.** `trust-security.vsix.acceptance.ts` runs in a VS Code spawned with that folder
    as `extensionDevelopmentPath`, and with `acceptance-suite.js` from the repository's `out/` as
    the tests path.
  - **What the file may use.** Only the public `vscode` API
    (`vscode.extensions.getExtension(<publisher>.<name>)`, its `exports`, `vscode.commands`) and
    file checks on the unpacked folder: the declared icon file is a 256 by 256 PNG, and the visible
    texts named by the path are there. It never imports `extensionApi.ts`, which requires the
    repository's `../../bundle/extension`, nor the `realInput/` helpers.
- **B6. Budget (Q37).**
  - **Expected healthy durations.**
    - One acceptance step (one path) takes **5 to 30 s**: open a fixture, open the preview, a few
      inputs, assert the file and the page.
    - A window start takes about 1 minute.
    - One launch therefore takes about 1 minute plus 30 s per path at most.
  - **Budgets.**
    - Each step uses the default budget, `STEP_BUDGET_DEFAULT_MS` (3 min). No acceptance step goes
      into `STEP_BUDGETS_MS`.
    - Each launch keeps `LAUNCH_DEADLINE_MS` (15 min), and no `STUDIO_LAUNCH_TIMEOUT_MS` is set.
  - **Split rule.**
    - A launch whose healthy duration (locally or on the first CI run) passes 7.5 minutes, half its
      deadline, is split into a second file of the group (B3). Files are also split before they
      pass 1500 lines.
    - A step whose healthy duration passes 90 s is split if it holds two paths' worth of steps;
      otherwise the coder reports it (stop list).
  - **Planned splits.**
    - lifecycle-sync has up to 19 paths, about 10 minutes in one launch. It starts with two files,
      `lifecycle-sync.acceptance.ts` and `lifecycle-sync.2.acceptance.ts`.
    - trust-security has three launches (trusted, restricted, vsix) plus packaging, on top of the
      shard's compile, bundle and VS Code download. That is estimated at 10 to 12 minutes against
      the 20-minute step. If a shard comes near its step timeout, the remedy is splitting files
      so each launch is smaller. If the shard as a whole still passes half its step timeout, the
      coder reports it. A cap is never raised.
  - **CI cost.** 16 parallel shards each run the LFS checkout and `just dev-ci`, about 3 to 5
    minutes per runner. That is about 1 hour of extra runner time on each heavy run, but no extra
    wall-clock time: the shards run in parallel with `integration`.
  - **Local cost.** `just preflight` on macOS gains about 17 window starts and about 150 paths,
    roughly 40 to 60 more minutes. Preflight runs acceptance because CI does (rule 7).
  - **No stress-plan entry.** The acceptance tests are not added to `test/shared/stressPlan.ts`:
    they walk paths that SwRS tests already lock, and `ci-stress` cannot loop acceptance launches.
    A flaky acceptance path is handled by reproducing its flaky step in the stress plan, as an
    integration test that `ci-stress` loops, then fixing it there (rule 12).
- **B7. CI job `acceptance` (`.github/workflows/ci.yml`).**
  - **Trigger:** the same `needs` and `if` as `integration` (`needs: release-check`; a push to
    `main` or a heavy dispatch).
  - **Setup:** `runs-on: ubuntu-latest`, `permissions: contents: read`, and the same setup steps as
    `integration`:
    - checkout with LFS, then LFS pull and fsck;
    - setup-node from `.nvmrc`;
    - setup-uv;
    - setup-just 1.58.0;
    - `just dev-ci`.
  - **Matrix:** `strategy: matrix: group: [...]` with `fail-fast: false`.
    - The list is every group that has an acceptance file, in `GROUPS` order. It is not all 16
      groups, since some groups' paths are accepted elsewhere (B3).
    - `test_workflows.py` checks that the list equals the groups that have files on disk.
  - **Test step:**
    `xvfb-run --auto-servernum -s "-screen 0 2600x1440x24" just ci-acceptance "${{ matrix.group }}"`,
    with `STUDIO_VIEWPORT_GUARD: strict`.
  - **Timeouts:**
    - They start at 30 minutes for the job and 20 for the step (rule 11 for VS Code jobs).
    - After the first heavy dispatch, they are set to about twice the slowest shard's measured
      healthy duration, never above 30 and 20.
    - They are never raised to make a run pass.
  - **After the test step:** `just ci-hang-dump` (`if: always()`, the third target, as in
    `integration`). Then an upload (`if: always()`) of `out/reports/` as
    `e2e-acceptance-${{ matrix.group }}-attempt-${{ github.run_attempt }}`.
  - **Job output:** `artifact: e2e-acceptance-*-attempt-*`.
    - A matrix job has one output for all its shards, so the output is a pattern.
    - The rule for a matrix producer: its output, matched with `fnmatch`, covers the upload name
      `e2e-acceptance-${{ matrix.group }}-attempt-${{ github.run_attempt }}`, and consumers
      download it without `merge-multiple`.
    - The reason: "Re-run failed jobs" re-runs only the failed shards, so a consumer can hold
      attempt 1 of one group and attempt 2 of another, and keeps the newest attempt per group (B8).
  - The `heavy` input's description names the acceptance job beside integration and stress, with
    its expected duration.
- **B8. Consumers of the acceptance results.**
  - **`report`:** `needs: [release-check, visual, integration, acceptance]`.
    - A download step, `if: needs.acceptance.outputs.artifact != ''`, takes
      `pattern: ${{ needs.acceptance.outputs.artifact }}` into `out/ci-artifacts/acceptance/`,
      without `merge-multiple`, so each artifact keeps its own folder.
    - `ci-report` calls a new script, `scripts/select-acceptance-attempts.mjs`, before
      `e2e-campaign.mjs report`. For each group, the script copies
      `out/reports/acceptance/<group>/` from the folder with the highest attempt number into
      `out/reports/acceptance/<group>/`. It prints the attempt kept per group.
    - This logic lives in the script, not in the workflow (rules 1 and 3).
    - A red or missing acceptance shard fails `report`, and so `checks`.
  - **`checks`:** its list does not change. It takes acceptance through `report`, as it takes
    integration.
  - **`tag-release`:** `needs: [checks, release-check, integration, acceptance, stress]`.
    - On a version change it tags only when `checks`, `integration`, `acceptance` and `stress` are
      all `success`.
    - The "Release not tagged" summary lists the acceptance result.
  - **`pages`:**
    - its `needs` adds `acceptance`;
    - `reports_from_caller` also requires `needs.acceptance.result == 'success'`;
    - the merged `studio-reports` artifact of `report` carries the acceptance stage;
    - the comments in `pages.yml` that say "both stage artifacts" name the three stages.
  - **`scripts/select_e2e_run.py`** (the Pages selection of a later deploy):
    - the required jobs become `integration`, `stress` and every job whose name starts with
      `acceptance (` (the matrix names its jobs `acceptance (<group>)`). At least one such job must
      exist, and all of them must be `success`. This is a prefix match, chosen over relying on the
      run's conclusion only, so a run without the acceptance job is refused;
    - this applies to push runs and to dispatch runs;
    - the stage artifacts it compares with `studio-reports` add every `e2e-acceptance-<group>`
      name;
    - `REQUIRED_ARTIFACTS` and the module docstring are updated.
  - **The Pages fallback** (`xvfb-run just site`, used when no green heavy run exists) runs
    `just e2e`, which has no acceptance stage. The fallback site therefore lacks acceptance
    results and shows the stage as not run. That is accepted: the fallback is a degraded site.
  - **`gallery`:** unchanged. It reads integration captures only.
- **B9. Scenario coverage gate (D11): `scripts/check_scenario_coverage.py`.**
  - **Input.** The script runs these two commands itself, through the same
    `uv run --no-sync --group requirements okfreq` command as the justfile, then reads both
    outputs:
    - `okfreq generate-report requirements --output-json out/reports/requirements/scenario-coverage-report.json`;
    - `okfreq trace requirements --json`.
  - **Gap rules.** For each record of `requirements[]` whose `frontmatter.req_lifecycle` is live,
    it prints one line per gap:
    - a SwRS that is not exempt (`diagnostics.exempted` false) and has a non-empty
      `transitions.missing`: `<path>: SwRS-X: scenarios not tested: S2, S3`;
    - a StRS with `stakeholder_test_coverage.paths.accepted < paths.total` and no
      `acceptance_exemption`: `<path>: StRS-X: paths not accepted: S1, S3`. The report gives
      counts only, so the path ids are the declared `scenarios:` ids that have no counting
      `@accepts_req` in the trace's `scenario_markers`;
    - a StRS with no `scenarios:` in its frontmatter: `<path>: StRS-X: no scenarios: declared`.
  - **Exit codes and output.**
    - It exits 1 when it prints any gap.
    - It exits 2, with one line naming the mode found, when the report's
      `stakeholder_test_coverage.mode` is not `linked-swrs-and-acceptance-paths`.
    - On success it prints
      `scenario coverage: <s> SwRS scenarios tested, <p>/<P> StRS paths accepted, all complete`.
  - **Where it runs.** As the last line of `just requirements-lint`:
    `uv run --no-sync --group requirements python scripts/check_scenario_coverage.py requirements`.
  - **Tests:** `test/build/test_check_scenario_coverage.py`, added to `just release-tests`.
    - Each failure rule and the wrong mode have a case with a prepared report and trace (refusals
      the shipped bundle cannot hold).
    - One case runs the script on the shipped `requirements/` bundle at the head, and expects the
      success line.
  - It lands in the same commit as the switch (B10).
- **B10. Mode switch (Q27).** One commit, the last of the CR, contains:
  - `requirements/config.yml`: `strs_test_coverage_mode: linked-swrs-and-acceptance-paths`;
  - B9's script and its `requirements-lint` line, with its SwRS (B13);
  - the SwRS schema declaration that refuses `accepted_in_files`, if `okfreq validate` asks for
    it (CR-504's scratch validation should have added it already);
  - `just requirements-update`, with every file it generates committed: `tested_in_files` and
    `accepted_in_files` written on StRS for the first time (see Figures), the SwRS
    `tested_in_files` reduced to counting files, the coverage and OKF fields, and the Links;
  - a `requirements/tiers/log.md` entry (B12);
  - the "StRS covered" card caption of the viewer: it states the new rule ("covered: linked SwRS
    covered or exempt, and every path accepted"). `test/site/requirementsViewer/home.ts` and its
    `home.test` are updated, and so is the viewer SwRS that CR-504 touched.

  Generated fields are not normative. Writing `tested_in_files` and `accepted_in_files` on the 15
  approved StRS changes neither `approved_at` nor `approved_by`, and needs no owner agreement.
- **B11. Docs.** The docs that describe the job wiring land in commit 1 (acceptance-Q3):
  - **`.agents/guidelines/ci.guidelines.md`:**
    - rule 1: the exception for a third target (`ci-hang-dump`, which only collects files) names
      `acceptance` beside `integration`;
    - rule 11: the timeout text "30 for the VS Code integration and stress jobs" names
      acceptance. The job and step timeouts come from the measured duration;
    - rule 13 lists `acceptance` with `integration` and `stress` as real VS Code jobs (push to
      `main`, heavy dispatch, never a pull request), and says a red shard fails `report`, then
      `checks`;
    - rule 14 and "Recovering from a red heavy job" name `acceptance` among the jobs
      `tag-release` requires. Item 4 explains the per-group artifacts and the selection of the
      newest attempt (B8).
  - **`AGENTS.md` "Main targets":** the CI jobs line names `just ci-acceptance [GROUP]` (heavy;
    in parallel in CI, in sequence in `just preflight`), and the heavy dispatch.
  - **`CONTRIBUTING.md`:**
    - the CI section lists the `acceptance` job (heavy, matrix by group, push to `main` and heavy
      dispatch) and `just ci-acceptance [GROUP]`;
    - "Recovering from a red heavy job" names it;
    - the checks section names the D11 gate (written with the switch).

  The docs on authoring acceptance tests land with the groups (commit order, step 3):
  - **`requirements/guidelines/project.guidelines.md` "Benches"** (D14 completion):
    - the acceptance layout (B3) and the window kinds;
    - how to run one group locally;
    - the budget and the split rule (B6);
    - the D11 gate, and the new-mode meaning of "covered".

    It replaces CR-504's wording "added by the acceptance CR".
  - **`.agents/glossary/common.md`:** "acceptance job", and "acceptance file" (one file, one
    window).

  No change to the writing skill `skills/writing-for-markdown-okf-schema-studio/`: no rendered
  syntax changes.
- **B12. Log.** `requirements/tiers/log.md`, with entries under `## 2026-11-<day>` and
  `### Topic` sub-headings:
  - the scenario tests, and every pruned scenario with its reason (Q30b);
  - the CORE-076 change, and the new gate SwRS (B13);
  - the mode switch, with the before and after figures (StRS covered, paths accepted, scenarios
    tested).
- **B13. Requirements for the tooling (acceptance-Q3, no exception for tooling).**
  - **SwRS-MDOKFSTUDIO-CORE-076** (proposed, derived from StRS-CORE-007) is updated in commit 1.
    It already covers the heavy jobs, `tag-release`, the artifact names, the report merge, the
    two-hour rule and the Pages selection.
    - **Text:** the heavy jobs are `integration`, `acceptance` and `stress`.
    - **Scenarios** (new or changed `S<n>` entries in its `scenarios:`, with body sections):
      - the acceptance stage: one shard per group; the runner refuses an unknown group before any
        VS Code starts;
      - the matrix producer's artifact output pattern;
      - `report` keeps the newest attempt per group, and fails on a missing, failed or out-of-run
        group;
      - `tag-release` needs `acceptance`;
      - the Pages selection requires every `acceptance (<group>)` job.
    - **Markers:** each scenario is tested with `@tests_req SwRS-MDOKFSTUDIO-CORE-076#S<n>` in
      `test/build/test_workflows.py`, `test/build/test_select_e2e_run.py`,
      `test/site/e2eCampaign.test.ts` and the runner-argument tests. The new scripts
      (`select-acceptance-attempts.mjs`, `unpack_vsix.py`) and the changed `e2e-campaign.mjs`
      carry `@implements_req SwRS-MDOKFSTUDIO-CORE-076`.
    - **StRS-CORE-007** (proposed) is checked: its path step "The version commit has a green heavy
      run" still holds. Its text is changed only if it names the heavy jobs.
  - **A new proposed SwRS for the D11 gate,** derived from StRS-MDOKFSTUDIO-CORE-007, scope
    `rendering-core`, with the next free CORE number. Its title: "The requirements check refuses
    an untested scenario or a path not accepted".
    - It has one scenario per gap rule and one for the wrong mode.
    - `scripts/check_scenario_coverage.py` carries `@implements_req`, and
      `test_check_scenario_coverage.py` carries `@tests_req …#S<n>`.
    - It lands in the switch commit.
  - The viewer caption (B10) updates the viewer SwRS.
- **B14. `src/` is out of reach.** A path or scenario that the product does not do as written is
  not fixed here (stop list).

## What changes, area by area

### 1. SwRS scenario tests and prunings (Q30, Q30b, B1)

- Start from CR-504's PR-body list of untested scenarios. Recount it on CR-504's head, with
  `okfreq trace requirements --json` (`scenario_markers`) against the `scenarios:` of every live,
  non-exempt SwRS.
- For each scenario, either write the test (B1) with `@tests_req SwRS-X#S<n>`, or prune the
  scenario.
  - To prune: remove its `scenarios:` entry and its `### Scenario S<n> …` body section. Ids are
    never reused.
  - The coder may prune a proposed SwRS's scenario, with the reason. An approved one goes to the
    owner (stop list).
- The PR body has a table: SwRS, scenario, outcome (the test file, or pruned with its reason).

### 2. Acceptance tests (Q1, Q3, Q6, Q32, D7, B2, B3, B5)

- For each path of B2, one test: in the group file of B3, or on the D7 bench for CORE-007,
  CORE-008 and TRUST-014.
- CORE-006: the agent's writing is a simulated input. The test writes into a fixture the Markdown
  that the skill teaches, and walks the path in the window.
- CORE-007 S1: the test walks the release path up to the review, and stops before CORE-078 (the
  maintainer's review). It asserts the gate (no release without the review input) and the content
  it can check.
- The PR body has a table: StRS, path, test file, bench.

### 3. Runner and targets (B4, B5, B6)

The files that change:

- `test/shared/runnerArgs.ts` (new) and `test/integration/run-tests.ts`;
- `test/integration/acceptance-suite.ts` and `test/integration/acceptance/*.acceptance.ts`;
- `test/reportPaths.ts`;
- `package.json`;
- `scripts/e2e-campaign.mjs`, `scripts/select-acceptance-attempts.mjs` and
  `scripts/unpack_vsix.py`;
- `justfile`: `ci-acceptance`, `preflight` (the run and the Windows skip line) and `ci-report`.

Unit tests:

- the runner arguments (a refused group and the flag combinations): `test/build/runnerArgs.test.ts`,
  next to `hangWatchdog.test.ts` and `stressPlan.test.ts`;
- the campaign stage, the identity of each group and the `--visual-only` skip list:
  `test/site/e2eCampaign.test.ts`;
- the selection of the newest attempt: a test next to them in `test/build/`;
- `unpack_vsix.py`: a case in `test/build/`.

### 4. CI (B7, B8)

`.github/workflows/ci.yml` (`acceptance`, `report`, `tag-release`, `pages`, the `heavy`
description), `.github/workflows/pages.yml` (comments) and `scripts/select_e2e_run.py`.

`test/build/test_workflows.py` reads the shipped `ci.yml`, `justfile` and the files under
`test/integration/acceptance/`.

These existing tests are modified:

- `test_every_ci_download_names_the_artifact_of_the_job_it_needs`: it accepts a matrix producer's
  pattern output, matched with `fnmatch` against the upload name (B7);
- `test_report_merges_each_stage_from_the_attempt_that_produced_it`: the visual and integration
  downloads keep `merge-multiple: true` into `out/reports/`. The acceptance download is the
  pattern, without `merge-multiple`, into `out/ci-artifacts/acceptance/`;
- `test_a_consumed_artifact_is_announced_by_its_job`: it adds `("acceptance", "e2e-acceptance")`,
  with the `fnmatch` rule, and `REQUIRED_ARTIFACTS` gains it;
- `test_heavy_jobs_run_on_every_push_to_main_and_on_a_heavy_dispatch`: the parameters add
  `acceptance`;
- `test_ci_integration_and_stress_stop_on_a_locked_screen`: the parameters add
  `["ci-acceptance", "trust-security"]`;
- `test_preflight_skips_only_the_stages_that_need_linux_or_macos_on_windows` and
  `test_preflight_skips_report_and_gallery_when_the_screen_is_locked`: they cover acceptance;
- the `tag-release` and Pages tests: `test_tag_release_needs_the_heavy_jobs_and_runs_on_every_push_to_main`,
  `test_tag_step_requires_checks_and_both_heavy_jobs_on_a_version_change`,
  `test_refused_tag_names_each_heavy_result_in_the_job_summary`,
  `test_pages_reuses_the_reports_of_the_release_run_when_its_heavy_jobs_are_green` and
  `test_report_merges_the_real_window_stage_of_every_push_to_main`. They gain the acceptance
  results.

New cases:

- the `acceptance` job has a `timeout-minutes`, and its test step a smaller one;
- it runs under `xvfb-run` with the 2600x1440x24 screen, has the same `if` as `integration`, and
  has `fail-fast: false`;
- its matrix equals, in `GROUPS` order, the groups that have an acceptance file on disk;
- its upload name ends with `-attempt-${{ github.run_attempt }}`;
- `preflight` runs `ci-acceptance` after `ci-integration` and before `ci-report`.

`test/build/test_select_e2e_run.py` gains the `acceptance (` prefix cases: a missing job, a failed
shard, and all shards green.

### 5. Gate and switch (B9, B10, B13)

- `scripts/check_scenario_coverage.py` and `test/build/test_check_scenario_coverage.py`;
- `justfile`: `requirements-lint` and `release-tests`;
- `requirements/config.yml`;
- the new gate SwRS;
- the generated requirement files;
- `requirements/tiers/log.md`;
- `test/site/requirementsViewer/home.ts` and its test.

### 6. Docs (B11)

- Commit 1: `.agents/guidelines/ci.guidelines.md`, `AGENTS.md` and `CONTRIBUTING.md` (CI and
  recovery).
- Later: `requirements/guidelines/project.guidelines.md` and `.agents/glossary/common.md`.
- After each change under `requirements/`: run `just requirements-update` and commit the generated
  files.

## Commit order

Every commit must leave these green:

- `just check` and `just requirements-lint`;
- CR-504's scratch validation in the new mode (a copy of `requirements/` with the new mode,
  `okfreq validate <scratch> --check-links --project-root .`), with 0 errors, until the switch
  makes it the real validation.

Every commit that touches markers or requirements runs `just requirements-update` and commits the
result, so that `update-coverage --check` in `just check` passes.

1. **Infrastructure and the first group.**
   - Code: the runner and `runnerArgs.ts`, the campaign stage, `test:acceptance`,
     `ci-acceptance`, `preflight`, the `acceptance` job and its consumers, `select_e2e_run.py`,
     `select-acceptance-attempts.mjs` and `unpack_vsix.py`.
   - Tests: the `test_workflows.py`, `test_select_e2e_run.py` and `e2eCampaign.test.ts` changes,
     and the unit tests.
   - Requirements and docs: the CORE-076 update and its markers, the job-wiring docs (B11, commit
     1 part), and its log line.
   - The first group's acceptance file or files. `trust-security` is advised, because it uses all
     three window kinds. The matrix lists that group only.
2. **Per e2e group, in `GROUPS` order** (one or more commits per group):
   - that scope's SwRS scenario tests and prunings;
   - its acceptance files or D7 tests;
   - its matrix entry;
   - its log lines.
3. **The authoring docs:** the "Benches" section and the glossary (B11, later part).
4. **Last:** the gate, its SwRS and the switch (B9, B10, B13), `just requirements-update`, and the
   log entry.

After commit 1, the coder runs a heavy dispatch on the branch
(`gh workflow run ci.yml --ref <branch> -f heavy=true`) to measure the first shard. It then sets
the job and step timeouts (B7).

**Rounds and partial delivery (acceptance-Q2, acceptance-Q3).**

- A round is one cycle from the coder to the Inspector. The Foreman counts the rounds.
- When the remaining groups will not fit in 3 rounds, the coder gives the Foreman its estimate.
  The Foreman decides to stop.
- The coder then stops after a green commit of step 2. The mode is unchanged and the D11 gate is
  not on.
- It reports the groups done and the groups left. The Chief of Staff splits the rest per group,
  and the switch and the gate land in the last of those CRs.

**Evidence for a partial delivery** (a subset of the checks below):

- check 4 for the tests delivered;
- checks 5, 6 and 8;
- check 9 for the delivered shards;
- check 10;
- `requirements/config.yml` still in the old mode, and no D11 line in `requirements-lint`;
- the scratch validation in the new mode with 0 errors;
- the PR body lists the groups delivered, with their paths accepted, and the groups left.

## Out of scope

- Any change to `src/`. A bug found on the way is filed and reported (stop list), not fixed here.
- Any change to okf-schema itself.
- A simulated walk for every path (D9): `@tests_req StRS-X#S<n>` stays where CR-504 left it.
- Counting passing tests instead of markers (Q35).
- Retired requirements, beyond CR-504's D5 exemptions.
- Normative changes to approved requirements, including pruning one of their scenarios.
- A stress-plan entry for the acceptance tests (B6).
- `scripts/run-e2e.mjs` (`just e2e`), the Pages fallback's suite, and the `gallery` job.
- A waiver on any StRS (D15).

## CI environment

- **Where the job runs.**
  - `acceptance` runs on `ubuntu-latest` GitHub runners, one runner per group.
  - It runs under `xvfb-run`, with a 2600x1440x24 screen.
  - Each runner is set up by `just dev-ci` from the lock files, with the npm and uv caches of the
    setup actions, as `integration` is.
  - It runs on pushes to `main` and on a heavy dispatch, never on a pull request (rule 13).
- **What a runner lacks that a developer's machine has.**
  - No installed VS Code, no `STUDIO_VSCODE_EXECUTABLE` and no warm `.vscode-test` folder. Each
    shard downloads VS Code through `@vscode/test-electron` before its first launch; the launch
    deadline does not count this, but the step timeout does.
  - No `out/` build: `test:acceptance` compiles and bundles, and the vsix window also packages
    (B5).
  - No real display or GPU: Xvfb stands in.
  - No screen lock.
  - The VS Code download and `just dev-ci` need network access.
- **Local proof before the push.** The coder works on Windows. There, `just preflight` runs only
  the static stage, and skips acceptance because `ci-acceptance` needs Linux or macOS. Before the
  push it runs:
  - `just check` and `just requirements-lint`;
  - `just release-tests`: the workflow, selection and gate tests read the shipped `ci.yml`,
    `justfile`, acceptance files and `requirements/`;
  - `just ci-static`.

  On a macOS or Linux machine, `just ci-acceptance <group>` gives the same result as the CI shard.
- **What only the first CI runs prove.**
  - The real duration of each shard. These durations set the timeouts (B7).
  - That parallel shards each download VS Code and pass.
  - That the vsix window is built, unpacked and loaded on the runner.
  - The per-group artifacts, and the selection of the newest attempt on a real re-run (check 10).

### Host matrix

| Host | `just preflight` | `just ci-acceptance [GROUP]` |
| --- | --- | --- |
| Windows (developer) | Static stage only. Prints that acceptance is skipped and that CI runs it. | Not run. The recipe needs a Linux or macOS VS Code launch, as `ci-integration` does. |
| macOS (developer) | Runs `ci-acceptance` after `ci-integration` (about 40 to 60 more minutes). Exits 3 on a locked screen. | Runs one window at a time. |
| Linux CI, pull request | Not run. | Not run. `report` lists acceptance as skipped. |
| Linux CI, push to `main` or heavy dispatch | Not run. | One shard per group, in parallel. |

## Evidence

Every check on a shipped file reads it from the repository at the head under test.

### Checks

1. On the head, `requirements/config.yml` has
   `strs_test_coverage_mode: linked-swrs-and-acceptance-paths`.
2. `just requirements-lint` passes.
   - Its output ends with
     `scenario coverage: <s> SwRS scenarios tested, <P>/<P> StRS paths accepted, all complete`.
   - `okfreq validate` prints no error, no W003 and no W004.
   - The PR body quotes those lines.
3. `out/reports/requirements/scenario-coverage-report.json`, written by the gate on the head,
   shows:
   - for every live StRS: `paths.accepted == paths.total` and `status: covered`;
   - for every live, non-exempt SwRS: an empty `transitions.missing`;
   - no StRS with `acceptance_exemption`.

   The PR body gives "live StRS covered M/M, paths accepted P/P, scenarios tested S/S".
4. `just release-tests` passes, with:
   - `test_check_scenario_coverage.py`: each failure rule and the wrong mode fail on prepared
     inputs, and the shipped bundle passes;
   - the modified and new `test_workflows.py` and `test_select_e2e_run.py` cases.
5. `just check` passes, including:
   - check-markers with CR-504's D10 rules: every `@accepts_req` is under `test/integration/` or
     on a D7 StRS, and every fragment is declared;
   - check-limits: no acceptance file over 1500 lines and no baseline growth;
   - the new unit tests (`runnerArgs.test.ts`, `e2eCampaign.test.ts`, the selection and the
     unpacking);
   - `update-coverage --check`.
6. A scan of `test/integration/acceptance/` shows one `@accepts_req` per test, each naming a
   declared path, and no `@tests_req StRS-…`.
7. Every pruned scenario is in the PR table and in `requirements/tiers/log.md`, with its reason.
   No approved requirement lost a scenario.
8. `just preflight` passes. On Windows that is the static stage; CI runs the rest.
9. A heavy dispatch on the branch head is green for `integration`, `report` and every
   `acceptance` shard (every group that has an acceptance file). The PR body gives:
   - the run link;
   - each shard's measured duration and the timeouts set from them;
   - the `launches` durations of each `acceptance-manifest.json`.
10. On that run, `gh run rerun <run-id> --job <job-id of one acceptance shard>`:
    - the re-run shard uploads `-attempt-2`;
    - `report` re-runs, and merges attempt 2 of that group with attempt 1 of the others. Its log
      names the attempt kept for each group.

    The PR body gives the run link.

### Scenario steps (owner's view)

1. Build the site from the heavy run's reports (`just ci-report`, then `just ci-gallery`) and open
   the requirements viewer home.
   - "StRS paths accepted" shows P/P, "StRS covered" shows M/M, and "SwRS scenarios tested" shows
     S/S.
   - The "StRS covered" caption states the new rule.
2. Open StRS-MDOKFSTUDIO-LIFE-023. Each of S1 to S4 lists an accepted file under
   `test/integration/`.
3. Open StRS-MDOKFSTUDIO-CORE-007. S1 lists its D7 acceptance test.
4. Remove the `@accepts_req` line of one acceptance test and run `just requirements-lint`.
   - It fails with `StRS-X: paths not accepted: S<n>`.
   - W004 also appears if that was the StRS's only acceptance.

   Restore the file.
5. In Actions, open a heavy run. The `acceptance` job shows one shard per group that has an
   acceptance file, each with its `e2e-acceptance-<group>-attempt-<n>` artifact.

## Self-containment

The coder needs:

- this spec;
- CR-504's `03-change-spec.md` and `02-answers.md`;
- CR-504's PR body: the list of untested scenarios and the table of the marker sort;
- the okf-schema 0.18.1 docs named at the top;
- the repository's own rules.

## The coder stops and reports to the Foreman when

- CR-504 is not final, or its head differs from what this spec builds on: no `scenarios:`, no D10
  rules, or no `accepted_in_files` in `generated_fields`.
- A path or scenario cannot pass because the product does not do what it says. The coder files
  the bug with the failing step and reports. It does not fix `src/`, and it does not change the
  requirement.
- A scenario or path of an **approved** requirement would have to be removed or reworded, or an
  approved SwRS turns up.
- A StRS seems to have no step that can be automated (a waiver candidate). It goes to the owner;
  the coder never writes `acceptance_exemption`.
- A step's healthy duration needs more than its default budget, or a launch cannot stay under the
  15-minute deadline after the B6 split, or a shard stays above half its step timeout after the
  splits. The coder reports instead of raising a timeout.
- The vsix window (B5) cannot be built, unpacked or loaded on the runner.
- `okfreq` 0.18.1 behaves differently from its released docs on a point this spec relies on: the
  report and trace fields that B9 reads, W003 or W004, the covered rule, or the generated fields.
- Its estimate shows the remaining groups will not fit in 3 rounds. The Foreman decides on a
  partial delivery (above).

## Open questions

None. Every point the answers left open is decided above, as B1 to B14. The owner said "no
question".
