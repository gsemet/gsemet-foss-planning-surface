# The site shows the performance KPI scores of the latest heavy run

## Goal

The owner asked for performance KPI scores on complex rendering cases, shown on the project's GitHub
Pages site (`intake/request.md`). The KPI job, the maximums and their requirement come first, in the
CR below this one, `perf-kpi-real-window-tests`; this CR adds what a reader of the site sees: a
"Performance" page with the scores of the latest heavy run, linked from the site header.

Each score is shown as the median time in milliseconds and its ratio to the maximum, 1 or less
meaning met. The page shows the latest run only, with no history.

## Place in the stack

- Destination: the running batch batch-09, in the stack, directly above `perf-kpi-real-window-tests`
  (which sits above CR-516 `perf-547-slow-comment-selection` and CR-517
  `perf-547-comment-update-and-author`). This CR is written against what that CR delivers at the head
  where it is merged, and never repeats it.
- What this CR reads from the CR below, unchanged:
  - `test/shared/perfKpi.ts`: `PERF_KPIS` (ids `comment-selection` then `comment-create`, each with
    its `title`, its `requirement` `<the REVIEW SwRS of perf-kpi-real-window-tests>#S1` or `#S2`, and
    `maximumMs`).
  - `out/reports/perf/kpi.json`, written by `test/integration/perfKpiCampaign.ts`:
    `{ "schema": 1, "commit", "runId" (the run id, or "local"), "startedAt", "machine": { "os",
    "cpuModel", "cpus" }, "launches": 3, "kpis": [ { id, title, requirement, samples, medianMs,
    maximumMs, ratio, met } ] }`.
  - The path of `kpi.json` into the site: `ci-report` copies the perf stage into
    `out/reports/perf/`, so the merged `studio-reports-attempt-<n>` artifact holds `perf/kpi.json`;
    the `gallery` job and the release Pages build (`pages`, `reports_from_caller`,
    `scripts/select_e2e_run.py`) take their reports from that artifact. See open question 1.
- With CR-507 (`How we test`, PR 543, its H2): CR-507 adds "How we test" to the site header between
  "How we ship" and "Gallery". The header reads, in either merge order: Home, Contributing, How we
  ship, How we test, Gallery, Performance, Requirements. When CR-507 is below this CR, this CR inserts
  "Performance" after "Gallery" in CR-507's header and updates CR-507's tests of the header list.
  When this CR merges first, its header reads Home, Contributing, How we ship, Gallery, Performance,
  Requirements, and CR-507 inserts "How we test" between "How we ship" and "Gallery".

## Decisions (from `02-answers.md`)

1. Score form (perf-kpi-Q5, "A. ms et ratio (reco.)"): the page shows, per KPI, the median time in
   ms, the maximum in ms and the ratio measured / maximum; 1 or less means met.
2. Two CRs (perf-kpi-Q8, "A. Deux CR (reco.)"): the page is its own CR, above the KPI job, in
   batch-09; the job, maximums and requirement merge without waiting for it.
3. History (text before the questions, no objection): the site shows the latest run only, no
   history.

## What changes

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
    `data-met="false"` (its CSS colour is the `--ref` token, the palette of the failed capture
    status). The KPI title links to its requirement's page in the requirements viewer: the
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
  numbers right-aligned with tabular figures) and `.perf-table [data-met="false"]` in `--ref`.
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
- `SwRS-MDOKFSTUDIO-CORE-086` (proposed): its normative text, S1 and S2 name the header links with
  "Performance" after "Gallery" ("five links" becomes "six links", or "seven links" with CR-507's
  "How we test" when CR-507 is below this CR), and S1's list of main pages gains the Performance
  page. Its verification notes are unchanged in substance.
- No approved requirement's authored text changes, so no owner agreement is needed (project
  guidelines, "Approved requirements").

### Docs and glossary

- `CONTRIBUTING.md`, the "Performance KPIs" section that the CR below adds: one sentence, "The
  published site's Performance page shows the scores of the latest heavy run (`performance.html`,
  built by `test/site/perfPage.ts`)."
- `.agents/glossary/common.md`: **Performance page** (the page `performance.html` of the published
  site, the KPI scores of the latest heavy run, from `out/reports/perf/kpi.json`).
- `CHANGELOG.md`, `## Unreleased`: one line for the page, in the form of the pull request guideline
  ("CHANGELOG line"); commit type `feat`, as for the earlier site pages (`797deff2`, `1ca60e83`).
- The writing skill `skills/writing-for-markdown-okf-schema-studio/` is not touched: no rendered
  syntax changes.

## Out of scope

- The KPI job, the campaign script, the maximums, `kpi.json` and `kpi.md`, the `perf` job, its place
  in `report`, `tag-release`, `pages` and `select_e2e_run.py`, and the REVIEW SwRS
  (`perf-kpi-real-window-tests`).
- The fix of issue 547 and its measure (CR-516, CR-517).
- A history of scores across runs or releases (decision 3); a mark out of 100 (decision 1).
- A social card for the Performance page.
- When the Pages site deploys: it stays on a release tag, from that tag's heavy run, so "the latest
  heavy run" on the published site is the heavy run of the latest release.
- `docs/how-we-test.md`: the page names test levels and CI jobs, not site pages; this CR adds no CI
  job.

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
- Requirements: `just requirements-update`, `just requirements-lint`, `just check-markers`, and
  `okfreq validate --check-links --project-root .` with CI's okfreq version.
- Site build: `just site-assemble` with a `kpi.json` produced by `just perf-kpi` (Linux, macOS or
  Windows, per the CR below) or copied from a heavy run's `e2e-perf-attempt-<n>` artifact: open
  `out/site/performance.html`, see the two rows and the header link; `out/site/site-manifest.json`
  has `"performance": true`. Without the file: the "No performance run" text and `false`.
- Heavy run on the branch (`gh workflow run ci.yml --ref <branch> -f heavy=true`): the
  `studio-site-attempt-<n>` artifact of the `gallery` job holds `performance.html` with the two rows
  and the run's commit and id. The run id goes in the PR's test plan, with a screenshot of the page
  (pull request guideline).
- `just preflight` (on Windows the static stage only; CI runs the others).
- What only a release proves: the page on the published site appears at the next release tag's
  Pages deploy.

No host or default matrix: nothing in this CR depends on the agent host or on a shipped default
versus a configured setting.

## Open questions for the Chief of Staff

1. The split note says the CR below "ends at the report files (`kpi.json`, `kpi.md`), the job, the
   maximums and their requirement". This specification assumes the CR below still carries the path
   of `kpi.json` into the site, as its specification did before the split: the `ci-report` copy of
   the perf stage into `out/reports/perf/`, the `report` download of `e2e-perf-attempt-<n>`, `pages`
   and `reports_from_caller` needing `perf`, and `select_e2e_run.py` requiring `perf` and
   `e2e-perf`. If the CR below's final specification drops any of these, do they move into this CR?
   Without them the page always says "No performance run in these reports.".
