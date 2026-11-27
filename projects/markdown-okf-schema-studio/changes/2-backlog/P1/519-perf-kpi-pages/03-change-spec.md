# The site shows the performance KPI scores of the latest heavy run

## Goal

The owner asked for performance KPI scores on complex rendering cases, shown on the project's GitHub
Pages site (`intake/request.md`). The KPI job, the maximums and their requirement come first, in the
CR below this one, `perf-kpi-real-window-tests`; this CR brings its report to the site and adds what
a reader sees there: a "Performance" page with the scores of the latest heavy run, linked from the
site header.

Each score is shown as the median time in milliseconds and its ratio to the maximum, 1 or less
meaning met. The page shows the latest run only, with no history.

## Place in the stack

- Destination: the running batch batch-09, in the stack, directly above `perf-kpi-real-window-tests`
  (itself above CR-517 `perf-547-comment-update-and-author` and CR-516
  `perf-547-slow-comment-selection`). This CR is written against what that CR delivers at the head
  where it is merged, and never repeats it.
- What this CR reads from the CR below, unchanged:
  - `test/shared/perfKpi.ts`: `PERF_KPIS` (ids `comment-selection` then `comment-create`, each with
    its `title`, its `requirement` `<the REVIEW SwRS of perf-kpi-real-window-tests>#S1` or `#S2`, and
    `maximumMs`), and `scoreKpi`.
  - `out/reports/perf/kpi.json` and `kpi.md`, written by `test/integration/perfKpiCampaign.ts` (the
    contract that CR names for this one): `{ "schema": 1, "commit", "runId" (the run id, or
    "local"), "startedAt", "machine": { "os" (`linux`, `darwin` or `win32`), "cpuModel", "cpus" },
    "launches": 3, "kpis": [ { id, title, requirement, samples, medianMs, maximumMs, ratio, met } ] }`.
  - The heavy job `perf` of `.github/workflows/ci.yml` (same `if` as `integration`, output
    `artifact: e2e-perf-attempt-${{ github.run_attempt }}`, an upload of the whole `out/reports/`,
    `if: always()`), already a need of `tag-release`, and the scenario `S13 (boundary): The
    performance KPI job` it adds to `SwRS-MDOKFSTUDIO-CORE-076`.
- What the CR below leaves to this one, by its own text ("`report`, `pages`, `reports_from_caller`
  and `scripts/select_e2e_run.py` are not touched here: bringing the perf report into
  `studio-reports` and the site belongs to `perf-kpi-pages`"): see "The perf report into the merged
  reports" and "The Pages report selection" below. `intake/from-split-spec.md` holds the earlier text
  of these parts; it is checked here against the lower specification and the repository (main
  5f0746d), and corrected where the repository differs (the download folder, the local preflight
  case).
- With CR-507 (`How we test`, PR 543, its H2): CR-507 adds "How we test" to the site header between
  "How we ship" and "Gallery". The header reads, in either merge order: Home, Contributing, How we
  ship, How we test, Gallery, Performance, Requirements. When CR-507 is below this CR, this CR inserts
  "Performance" after "Gallery" in CR-507's header and updates CR-507's tests of the header list.
  When this CR merges first, its header reads Home, Contributing, How we ship, Gallery, Performance,
  Requirements, and CR-507 inserts "How we test" between "How we ship" and "Gallery". CR-507's drift
  test of `docs/how-we-test.md` checks CI jobs; this CR adds no job, so the page is not touched.

## Decisions (from `02-answers.md`)

1. Score form (perf-kpi-Q5, "A. ms et ratio (reco.)"): the page shows, per KPI, the median time in
   ms, the maximum in ms and the ratio measured / maximum; 1 or less means met.
2. Two CRs (perf-kpi-Q8, "A. Deux CR (reco.)"): the page is its own CR, above the KPI job, in
   batch-09; the job, maximums and requirement merge without waiting for it.
3. History (text before the questions, no objection): the site shows the latest run only, no
   history.

The Chief of Staff settled where the parts that only serve the site go (2026-11-26, after the lower
specification's final form): the perf download in `report`, the copy in `ci-report`, `pages` and
`reports_from_caller` needing `perf`, and `scripts/select_e2e_run.py` requiring `perf` and
`e2e-perf`, with their requirement text, CI guideline lines and tests, are in this CR.

## What changes

### The perf report into the merged reports: `.github/workflows/ci.yml` (`report`) and the `justfile` (`ci-report`)

- `report`: `needs` becomes `[release-check, visual, visual-2, integration, acceptance, perf]`. Its
  `if: ${{ !cancelled() }}` is unchanged, so a failed or skipped `perf` does not skip `report`. A new
  step after "Download the acceptance stage reports", in the form of the others:
  "Download the perf stage reports", `if: needs.perf.outputs.artifact != ''`,
  `actions/download-artifact` (the same pinned version as the other steps) with
  `pattern: ${{ needs.perf.outputs.artifact }}`, `path: out/ci-artifacts/perf/` and
  `merge-multiple: true` (one exact name, so the artifact's tree lands directly in that folder and
  `kpi.json` is at `out/ci-artifacts/perf/perf/kpi.json`; without `merge-multiple` the action adds a
  folder named after the artifact). Not into `out/reports/`: the perf job's upload holds its own
  `e2e/hang-dumps/post-step/` and `probe/`, which must not overwrite the integration stage's. A
  comment above the step says so.
- `ci-report` (both `STAGES` values), after `node scripts/select-acceptance-attempts.mjs` and before
  `node scripts/e2e-campaign.mjs report`, one step that never sets `failed`:
  - `out/ci-artifacts/perf/perf/` exists: it replaces `out/reports/perf/` with a copy of it (only
    that folder) and prints `perf stage: report of the perf job`;
  - else `out/reports/perf/kpi.json` exists (a local `just preflight`, where `ci-perf compare` wrote
    it just before): it keeps it and prints `perf stage: local report`;
  - else it prints `perf stage: no report (skipped or failed)`.
  The perf stage never fails `ci-report`: the red of an exceeded maximum belongs to the `perf` job
  and `tag-release`.
- A `perf` job that went red still uploads its reports (`if: always()`, from the CR below); its
  `kpi.json`, when written, reaches `studio-reports` and the gallery's site, where a KPI over its
  maximum is marked (see the page). `checks` is unchanged and does not need `perf` (CI rule 13).

### The Pages report selection: `.github/workflows/ci.yml` (`pages`), `.github/workflows/pages.yml`, `scripts/select_e2e_run.py`

- `pages` in `ci.yml`: `needs` gains `perf`
  (`[tag-release, integration, acceptance, stress, perf, report]`); `reports_from_caller` becomes
  `needs.integration.result == 'success' && needs.acceptance.result == 'success' &&
  needs.stress.result == 'success' && needs.perf.result == 'success'`. The comments above `needs`
  and `reports_from_caller` name `perf`.
- `pages.yml`: only the comment of "Find the end-to-end reports of this commit" changes ("after its
  heavy jobs (integration, acceptance, stress and perf) succeeded"). When the suite runs instead of
  reusing reports (no qualifying run), it does not run `perf`: the site then has no `kpi.json` and the
  page says so.
- `scripts/select_e2e_run.py`: `REQUIRED_JOBS` becomes `("integration", "stress", "perf")` and
  `STAGE_ARTIFACTS` gains `"e2e-perf"` (so `REQUIRED_ARTIFACTS` holds it too), so a later Pages
  deploy reuses only a heavy run whose `perf` job succeeded, whose `e2e-perf-attempt-<n>` artifact is
  live, and whose newest `studio-reports` attempt is not older than its newest `e2e-perf` attempt.
  The module docstring names `perf` among the heavy jobs and `e2e-perf` among the report artifacts.
  A run made before the job has no `perf` job: it is not selected and the suite runs, as for a run
  made before the second visual part.

### The page body: `test/site/perfPage.ts` (new)

- `perfPageBody(report: unknown | undefined, model: ViewerModel | undefined): string`, pure, no I/O,
  and `readKpiReport(reportsRoot: string): unknown | undefined`, which reads
  `<reportsRoot>/perf/kpi.json` (`undefined` when the file is absent; a file that is not JSON fails
  with the file's path and the parse error).
- With a report, the body holds, in this order:
  - `<h1>Performance</h1>`;
  - one line: "Latest heavy run: commit `<first 7 characters of commit>`, run `<runId>`,
    `<startedAt as YYYY-MM-DD>`, `<machine.os>, <machine.cpus> CPUs`". The run id is a link to
    `<REPOSITORY_URL>/actions/runs/<runId>` (`REPOSITORY_URL` from `test/site/siteLinks.ts`), except
    when it is `local`, which is plain text;
  - the sentence "Median time of three window launches on the CI runner; a ratio of 1 or less meets
    the maximum.";
  - a table with the header KPI | Median (ms) | Maximum (ms) | Ratio | Met, one row per KPI in
    `PERF_KPIS` order (not the order of the file). The ratio is written with two decimals. Met reads
    "met" for `met: true`; a row with `met: false` reads "over its maximum" and carries
    `data-met="false"`. The KPI title links to its requirement's page in the requirements viewer: the
    requirement id without its `#S<n>` part, through `requirementDir` of
    `test/site/requirementsViewer/urls.ts` and `relativeFolderLink` of `test/site/siteLinks.ts`, from
    `performance.html`. When the viewer has no active page for that id (no model, or the id unknown
    to it), the title is plain text.
- Without a report: `<h1>Performance</h1>` and `<p class="status">No performance run in these
  reports.</p>`.
- Refusals, thrown as an error that names `perf/kpi.json` and the reason, which fails the site build:
  a `schema` other than 1; a KPI id unknown to `PERF_KPIS`; a KPI of `PERF_KPIS` missing from the
  file; a KPI entry without a number `medianMs`, `maximumMs` or `ratio`, or without a boolean `met`.
- Every text from the file is escaped (`escapeHtml` of `test/site/socialCard.ts`).
- Carries `@implements_req <the new CORE SwRS>` (see "Requirements").

### The site build: `test/site/buildSite.ts`

- `main()` reads the report with `readKpiReport(REPORTS_ROOT)`, loads the viewer model with
  `loadRequirementsModel(REQUIREMENTS_REPORT_PATH(EXTENSION_ROOT))`, and writes
  `out/site/performance.html` with `pageDocument("performance", "performance.html",
  perfPageBody(report, model))`. No social card is added for this page.
- The table's style joins the `pageDocument` stylesheet: a `.perf-table` rule (borders in `--line`,
  numbers right-aligned with tabular figures) and `.perf-table [data-met="false"]` in `--ref` (the
  colour of the failed capture status).
- `site-manifest.json` gains `"performance": <true when kpi.json was read, else false>`.
- The file stays under the test-file size limit of `scripts/check-file-sizes.mjs`.

### The site header: `test/site/siteHeader.ts`

- A "Performance" link to `performance.html` (relative to the current page, `relativeSitePath`),
  after "Gallery" and before "Requirements"; the JSDoc lists the links in the new order. Every page,
  the requirements viewer included, carries it, since they all use `siteHeader`.

### Requirements (okfreq)

Run as `uv run --no-sync --group requirements okfreq`; IDs from `okfreq new`, never by hand. Then
`just requirements-update` and a dated entry in `requirements/tiers/log.md` under the date of the
change.

- New SwRS in scope `rendering-core`, `--lifecycle proposed`, derives from
  `StRS-MDOKFSTUDIO-CORE-008` ("A reviewer reads the published site and its requirements",
  proposed). Title: "The published site shows the performance KPI scores of its heavy run".
  Normative text: when a maintainer builds the Pages site, the site SHALL hold a Performance page
  that shows, for each KPI of the latest heavy run's `kpi.json`, the median time, the maximum and
  their ratio, and whether the maximum is met. Scenarios:
  - `S1 (nominal): The scores of a heavy run` - GIVEN a `kpi.json` of schema 1 with the two KPIs -
    WHEN the site is built - THEN `performance.html` shows the run's short commit, its run id linked
    to the Actions run, its date and machine, and one row per KPI in `PERF_KPIS` order with the
    median, the maximum, the ratio with two decimals and "met", the KPI title linked to its
    requirement's page.
  - `S2 (boundary): No performance run` - GIVEN reports without `perf/kpi.json` - WHEN the site is
    built - THEN the page says "No performance run in these reports." and the manifest has
    `"performance": false`.
  - `S3 (boundary): A KPI over its maximum` - GIVEN a KPI with `met: false` - WHEN the page is
    written - THEN its row reads "over its maximum" and is marked.
  - `S4 (refusal): A report the page cannot read` - GIVEN a `kpi.json` of another schema, with an
    unknown KPI or with a KPI of `PERF_KPIS` missing - WHEN the site is built - THEN the build fails
    with `perf/kpi.json` and the reason.
  `verification_method: test`; criteria: the unit tests of `test/site/perfPage.test.ts`. Its
  `@implements_req` sits in `test/site/perfPage.ts`.
- `SwRS-MDOKFSTUDIO-CORE-076` (proposed), as far as the report and Pages concern `perf`:
  - S13 (added by the CR below): its THEN gains "`report` takes the perf stage from
    `out/ci-artifacts/perf/` and a missing perf report does not fail it; `pages` takes the reports of
    the calling run only when `perf` succeeded; `scripts/select_e2e_run.py` requires `perf` and its
    `e2e-perf` artifact".
  - S6's table: "`integration`, `stress` and every acceptance shard (S11) succeeded" becomes
    "`integration`, `stress`, `perf` and every acceptance shard (S11) succeeded" in the two "yes"
    rows; the "no" row reads "whose `integration`, `stress` or `perf` is skipped, failed or absent";
    the stale-report row lists `e2e-perf` among the stage artifacts; a new row "a run made before the
    `perf` job (no `perf` job) | no; the suite runs".
  - S1 ("`pages` builds the site from the merged reports artifact of the same run") and S10 ("only
    when `checks` and the three heavy jobs succeed ... `pages` take the reports of the calling run"):
    the reuse of the calling run's reports names `perf` among the jobs that must succeed.
  - Verification notes: `test/build/test_select_e2e_run.py` "checks the run selection, including runs
    with several attempts, acceptance shards and the perf job"; `test/build/test_workflows.py` checks
    the perf download of `report` and the perf step of `ci-report`.
  - `scripts/select_e2e_run.py` already carries `@implements_req SwRS-MDOKFSTUDIO-CORE-076`; the new
    tests carry `@tests_req SwRS-MDOKFSTUDIO-CORE-076#S6` or `#S13`.
- `SwRS-MDOKFSTUDIO-CORE-086` (proposed): its normative text, S1 and S2 name the header links with
  "Performance" after "Gallery" ("five links" becomes "six links", or "seven links" with CR-507's
  "How we test" when CR-507 is below this CR), and S1's list of main pages gains the Performance
  page. Its verification notes are unchanged in substance.
- No approved requirement's authored text changes, so no owner agreement is needed (project
  guidelines, "Approved requirements").

### CI guideline: `.agents/guidelines/ci.guidelines.md`

- Rule 13: after "a red `integration` or a red `acceptance` shard fails `report`, then `checks`", one
  sentence: "`report` also merges the `perf` stage when it ran; a red or missing `perf` never fails
  `report`."
- Recovery section, item 4: `perf` joins the jobs whose `artifact` output a consumer downloads
  (`visual`, `visual-2`, `integration`, `perf`, `report`); one sentence: "`report` downloads the
  perf artifact into `out/ci-artifacts/perf/` and `ci-report` copies only its `perf/` folder into
  the merged reports, so the perf job's hang dumps do not overwrite the integration stage's"; and
  Pages (`reports_artifact`, or `scripts/select_e2e_run.py`) reuses a run's reports only when its
  `perf` job succeeded too.
- Recovery section, item 3: after a `perf` failure on a version change, the re-run jobs are `perf`,
  then `report`, `tag-release`, `release` and `pages` (the line already lists the order; `perf` is
  named with the heavy job).

### Docs and glossary

- `CONTRIBUTING.md`, the "Performance KPIs" section that the CR below adds: one sentence, "The
  published site's Performance page shows the scores of the latest heavy run (`performance.html`,
  built by `test/site/perfPage.ts` from the `perf/kpi.json` of the merged reports)."
- `.agents/glossary/common.md`: **Performance page** (the page `performance.html` of the published
  site, the KPI scores of the latest heavy run, from `out/reports/perf/kpi.json`).
- `CHANGELOG.md`, `## Unreleased`: one line for the page, in the form of the pull request guideline
  ("CHANGELOG line"); commit type `feat`, as for the earlier site pages (`797deff2`, `1ca60e83`).
- The writing skill `skills/writing-for-markdown-okf-schema-studio/` is not touched: no rendered
  syntax changes.

## Out of scope

- The KPI job itself, the campaign script, the maximums, `kpi.json` and `kpi.md`, `ci-perf` and
  `perf-kpi`, `perf` in `tag-release`, its timeouts, the REVIEW SwRS and the lines of S13 that the CR
  below writes (`perf-kpi-real-window-tests`).
- The fix of issue 547 and its measure (CR-516, CR-517).
- A history of scores across runs or releases (decision 3); a mark out of 100 (decision 1).
- A social card for the Performance page.
- Running `perf` in the Pages workflow's fallback suite.
- When the Pages site deploys: it stays on a release tag, from that tag's heavy run, so "the latest
  heavy run" on the published site is the heavy run of the latest release.
- `docs/how-we-test.md`: it names test levels and CI jobs; this CR adds no job.

## Evidence

- Unit (`just check`):
  - `test/site/perfPage.test.ts`, with `@tests_req <the new CORE SwRS>#S1` to `#S4`, on a `kpi.json`
    written in a temporary folder by the writer of `test/integration/perfKpiCampaign.ts` (the
    function that writes `kpi.json` in the CR below, exported if it is not, its output unchanged),
    from `scoreKpi` results of the shipped `PERF_KPIS`:
    - S1: the heading, the short commit, the run link `.../actions/runs/<id>`, the date, the
      machine, two rows in `PERF_KPIS` order (the file written in the reverse order), ratios with two
      decimals, "met", and each title linked to `requirements/review-annotations/<id>/` (relative
      from `performance.html`) when a model holds the requirement, plain text when none does; a
      `runId` of `local` gives no link.
    - S2: `readKpiReport` on a folder without `perf/kpi.json` gives `undefined`, and the body says
      "No performance run in these reports.".
    - S3: a KPI scored above its maximum gives "over its maximum" and `data-met="false"`.
    - S4: schema 2, an unknown KPI id and a missing KPI each throw an error naming `perf/kpi.json`
      and the reason (prepared texts, since the writer cannot produce them; paired with the S1 check
      on the writer's own output). A title holding `<` is escaped.
  - `test/site/siteTheme.test.ts`: the expected header list gains "Performance" after "Gallery", on
    a main page and on a viewer page (with CR-507 below: Home, Contributing, How we ship, How we
    test, Gallery, Performance, Requirements). Any other test that lists the header links (CR-507's
    included when it is below) is updated the same way.
  - `test/site/siteLinks.test.ts` or the header test: "Performance" resolves to `performance.html`
    from the root page and to `../performance.html` from `docs/how-we-ship.html`.
  - `test/build/test_workflows.py`, on the shipped `.github/workflows/ci.yml` and `justfile` at the
    head under test:
    - `report` needs `perf`; its perf download step has `if: needs.perf.outputs.artifact != ''`,
      `pattern` equal to `needs.perf.outputs.artifact`, `path: out/ci-artifacts/perf/` and
      `merge-multiple: true`; the existing check "every download names the `artifact` output of a job
      it needs" covers it.
    - `pages` needs `perf`, and `reports_from_caller` is true only when `integration`, `acceptance`,
      `stress` and `perf` are all `success` (each other `perf` result gives false); `checks` still
      does not need `perf`; every `needs.<job>` reference is a need.
    - `ci-report` run on prepared folders: with `out/ci-artifacts/perf/perf/kpi.json` it copies the
      folder to `out/reports/perf/` and prints `perf stage: report of the perf job`, and leaves the
      artifact's `e2e/` untouched in `out/reports/`; with only `out/reports/perf/kpi.json` it keeps it
      and prints `perf stage: local report`; with neither it prints `perf stage: no report (skipped
      or failed)`; the perf step never makes `ci-report` fail (or, if running the recipe is too
      heavy for a unit test, the recipe's text is checked for the three branches and the order after
      `select-acceptance-attempts.mjs`, said as such in the PR).
  - `test/build/test_select_e2e_run.py`: a run whose `perf` job is skipped, failed or absent is not
    selected (the parametrized "every green heavy job" test gains `perf`); one with a green `perf` and
    a live `e2e-perf-attempt-<n>` is; a green `perf` without its artifact is not; `studio-reports`
    older than the newest `e2e-perf` attempt is not; the shipped `REQUIRED_JOBS` and
    `STAGE_ARTIFACTS` name `perf` and `e2e-perf`.
- Requirements: `just requirements-update`, `just requirements-lint`, `just check-markers`, and
  `okfreq validate --check-links --project-root .` with CI's okfreq version.
- Site build: `just site-assemble` with a `kpi.json` produced by `just perf-kpi` (Linux, macOS or
  Windows, per the CR below) or copied from a heavy run's `e2e-perf-attempt-<n>` artifact: open
  `out/site/performance.html`, see the two rows and the header link; `out/site/site-manifest.json`
  has `"performance": true`. Without the file: the "No performance run" text and `false`.
- Heavy run on the branch (`gh workflow run ci.yml --ref <branch> -f heavy=true`): the `report` log
  prints `perf stage: report of the perf job`; `studio-reports-attempt-<n>` holds `perf/kpi.json`;
  the `studio-site-attempt-<n>` artifact of the `gallery` job holds `performance.html` with the two
  rows and the run's commit and id. Then `just site-run gsemet/markdown-okf-schema-studio <head sha>`
  prints that run's id and its `studio-reports` name (the selection accepts a run with a green
  `perf`). The run id goes in the PR's test plan, with a screenshot of the page (pull request
  guideline).
- `just preflight` (on Windows the static stage only; CI runs the others).
- What only a release proves: `pages` taking the calling run's reports with `perf` green, and the page
  on the published site, appear at the next release tag's Pages deploy.

No host or default matrix: nothing in this CR depends on the agent host or on a shipped default
versus a configured setting.

## Open questions for the Chief of Staff

None.
