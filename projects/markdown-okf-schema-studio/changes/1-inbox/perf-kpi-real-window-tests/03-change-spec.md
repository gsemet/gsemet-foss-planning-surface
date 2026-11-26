# Real-window performance KPI job with maximums, shown on the site

## Goal

The owner wants performance measured in a real VS Code window on a complex rendering case, given as
KPI scores, published on the project's GitHub Pages site, with requirements that set the maximum each
score must meet (`intake/request.md`, `02-answers.md`).

First scope: the document of issue 547 (https://github.com/gsemet/markdown-okf-schema-studio/issues/547),
two paths: text selection and comment creation. Each score is a median time in milliseconds and its
ratio to the maximum (1 or less means met). The campaign runs in GitHub CI, where an exceeded maximum
turns the job red and so blocks a release, and by a local command, to compare. The site shows the
latest run only.

This CR is the upper of a stack of two in batch-09. The lower CR, CR-516
`perf-547-slow-comment-selection` (its `03-change-spec.md`, Part 1), fixes the issue and adds the
real-window measure of selection and comment creation on that document, with the document's
deterministic generator in `test/probe/`: the scenario `perf-547`
(`STUDIO_REAL_INPUT_SCENARIO=perf-547`, beside `test/integration/performanceProbe.ts`), one window
launch per run, which writes `out/reports/probe/perf-547.json` with every sample and the median per
interaction, among them `selectionRelease` (from the mouse release that ends a selection to the
Comment button shown) and `commentCreate` (from the save of a new comment to its highlight drawn). It
sets no limit and leaves the maximums to this CR. This CR builds on that measure, at the head where
it is merged, and never repeats it: it runs the scenario three times, turns its samples into scores,
checks them against the maximums, runs it in CI and shows it on the site.

## Decisions (from `02-answers.md`)

1. Answer 1 (next batch) is replaced by answer 2: the campaign goes into the running batch batch-09,
   with the fix of issue 547 (owner, in perf547-Q1: "Tu vas en profiter de ce fix pour rajouter la
   campagnes de PKI demander").
2. Where it runs (answer 3, "C. Les deux"): in GitHub CI, which carries the maximums, and by a local
   command used to compare.
3. An exceeded maximum (answer 4, "A. Job rouge"): requirements with a maximum and a wide margin;
   exceeding it fails the heavy job, so it blocks a release. The margin is about twice the median
   measured after the fix.
4. First cases (answer 5, "B. Ticket 547 seul"): selection and comment creation on the issue 547
   document only; other cases later.
5. Score form (answer 6, "A. ms et ratio"): the median time and the ratio measured / maximum; 1 or
   less means met.
6. History (text before the questions, no objection): the Pages site shows the latest run only, no
   history.

Repetition: the owner asked for the real-window analysis to be run "2 ou 3 fois pour avoir un peu de
stabilité" (perf547-Q1). The campaign follows it: three window launches per run.

## What changes

### The KPI definitions and the maximums: `test/shared/perfKpi.ts` (new)

- `PERF_KPIS`, one entry per KPI, in this order:
  - `comment-selection`: "Text selection on the issue 547 document": the samples `selectionRelease`
    of `perf-547.json` (from the mouse release that ends a text selection to the Comment button
    shown).
  - `comment-create`: "Comment creation on the issue 547 document": the samples `commentCreate` of
    `perf-547.json` (from the save of a new comment to its highlight drawn).
  Each entry holds its id, title, the requirement scenario it checks (`SwRS-...#S1`, `#S2`, see
  "Requirements") and `maximumMs`.
- The KPI reads the samples of the report as CR-516 writes them; it never reads the report's own
  medians, since it pools the samples of three launches.
- `maximumMs` is about twice the median of the first heavy CI run of this branch made after the fix
  (the CI runner, not a local machine), rounded up to the next 10 ms. The run id that gave each
  value is written in a comment next to it, and in the SwRS's rationale.
- Pure functions, no I/O: `median(samples)` (odd count: the middle; even: the mean of the two
  middle values), `scoreKpi(kpi, samples)` giving `{ id, title, requirement, samples, medianMs,
  maximumMs, ratio, met }` with `ratio = medianMs / maximumMs` rounded to two decimals and `met`
  true when `medianMs <= maximumMs`. No sample for a KPI is an error that names the KPI, never a
  score of 0.

### The campaign script: `test/integration/perfKpiCampaign.ts` (new, compiled to `out/test/integration/perfKpiCampaign.js`)

- Reads the reports of the three launches from `out/reports/perf/runs/run-<k>.json` (k = 1, 2, 3:
  `out/reports/probe/perf-547.json`, copied there by the target after each launch), pools the
  samples `selectionRelease` and `commentCreate` over the three launches, scores them with `scoreKpi`.
- Writes `out/reports/perf/kpi.json`:
  `{ "schema": 1, "commit": <full sha>, "runId": <STUDIO_E2E_RUN_ID, or "local">, "startedAt",
  "machine": { "os", "cpuModel", "cpus" }, "launches": 3, "kpis": [ <one score per KPI> ] }`,
  and `out/reports/perf/kpi.md`, the same table in Markdown.
- Prints one line per KPI: `<id>: median <m> ms, maximum <M> ms, ratio <r> (<met|OVER>)
  [<n> samples]`.
- `--enforce` (CI): exit 1 when a KPI is over its maximum, last line
  `perf KPI: FAILED, <id> <m> ms > <M> ms` (every KPI over, comma-separated); else last line
  `perf KPI: all <n> KPIs within their maximums`. Without `--enforce` (local comparison): exit 0
  whatever the ratios, an over KPI marked `OVER (CI maximum)`, last line
  `perf KPI: compared on this machine, the maximums hold for the CI runner`.
- Either mode: a missing run report or a KPI without samples exits 1 and names the launch or KPI.
- Carries `@tests_req <the new REVIEW SwRS>#S1` at the check of `comment-selection` and `#S2` at
  the check of `comment-create` (one marker per scenario, at the comparison).

### Justfile

- `ci-perf: (_require-unlocked-screen "ci-perf")` (new), the CI job's target: removes
  `out/reports/perf/`, runs the measure's real-window scenario of `perf-547-slow-comment-selection`
  three times, one window launch each (`STUDIO_REAL_INPUT_SCENARIO=<that scenario> npm run
  test:integration -- --trusted-only`, the form `performanceProbe.ts` documents), copies each
  launch's report to `out/reports/perf/runs/run-<k>.json`, then runs
  `node out/test/integration/perfKpiCampaign.js --enforce`. Last line `ci-perf: passed` or
  `ci-perf: FAILED` (CI guideline rule 8). A launch that fails stops the target red; there is no
  retry (rule 9).
- `perf-kpi` (new), the local comparison command: the same three launches and the same report
  files, then the script without `--enforce`; last line `perf-kpi: done`. It fails only when a
  launch or the measure fails.
- Both stop with exit code 3 on a locked screen, like `ci-integration`. On Windows both stop before
  any launch with `ci-perf: the real VS Code stages run on Linux and macOS only` (and `perf-kpi: ...`),
  exit 2: the real-window stages do not run on Windows today (CONTRIBUTING.md, "Windows"; see the
  open questions).
- `preflight`: runs `just ci-perf` after `just ci-acceptance`, counted in the failures, with the
  locked-screen handling of the two stages before it (CI rule 7: preflight runs every `ci-*`
  target CI runs). The Windows skip line becomes `preflight: visual, viewer-graph, integration,
  acceptance, perf, report and gallery stages skipped on Windows; CI runs them`.
- `ci-report`: after `select-acceptance-attempts.mjs`, when `out/ci-artifacts/perf/perf/` exists,
  copies it to `out/reports/perf/` (only that folder). The perf stage never fails `ci-report`: a
  missing perf report is printed as `perf stage: no report (skipped or failed)`.

### CI workflow: `.github/workflows/ci.yml`

- New heavy job `perf`, built like `integration` (CI guideline rules 1, 3, 11, 13): `needs:
  release-check`, the same `if` as `integration` (every push to `main`, a dispatch with `heavy`,
  never a pull request), `runs-on: ubuntu-latest`, `timeout-minutes: 15`, output `artifact:
  e2e-perf-attempt-${{ github.run_attempt }}`. Steps: checkout with LFS, LFS pull and fsck, Node,
  uv, just, `just dev-ci`, then `xvfb-run --auto-servernum -s "-screen 0 2600x1440x24" just ci-perf`
  with `timeout-minutes: 10` and `STUDIO_VIEWPORT_GUARD: strict`, then `just ci-hang-dump` and the
  upload of `out/reports/` as `e2e-perf-attempt-<n>`, both `if: always()`. Both timeouts are set
  again to about twice the healthy duration of the first CI run (rule 11), the step's below the
  job's.
- `report`: `needs` gains `perf`; a step "Download the perf stage reports", `if:
  needs.perf.outputs.artifact != ''`, downloads that pattern into `out/ci-artifacts/perf/` (not
  merged into `out/reports/`, so the perf job's `e2e/hang-dumps/post-step/` does not overwrite the
  integration job's).
- `tag-release`: `needs` gains `perf`. The refusal step and the tag step require
  `needs.perf.result == 'success'` on a version change, like `stress`; the "Release not tagged"
  summary and the `::error::` line list `perf: $PERF`.
- `pages`: `needs` gains `perf`; `reports_from_caller` also requires `needs.perf.result ==
  'success'`.
- The `heavy` input's description names the perf job.
- `checks` is unchanged: `perf` is not one of its needs (the real VS Code jobs are not, CI rule 13),
  so a red `perf` on a push without a version change shows as a red job and does not fail `checks`.
  Its red blocks a version change at `tag-release` (decision 3).

### Pages report selection: `scripts/select_e2e_run.py`

- `REQUIRED_JOBS` becomes `("integration", "stress", "perf")` and `STAGE_ARTIFACTS` gains
  `"e2e-perf"`, so a later Pages deploy reuses only a heavy run whose perf job succeeded and whose
  `studio-reports` is not older than its newest `e2e-perf` attempt. The module docstring says so. A
  run made before the job has no `perf` job: it is not selected and the suite runs, as for a run
  before the second visual part.

### The site page: `test/site/perfPage.ts` (new), `test/site/buildSite.ts`, `test/site/siteHeader.ts`

- `perfPage.ts` builds the body of `performance.html` from `out/reports/perf/kpi.json`:
  heading "Performance"; one line "Latest heavy run: commit `<short sha>`, run `<id>` (a link to the
  Actions run when the id is not `local`), `<date>`, `<os>, <cpus> CPUs`"; one sentence "Median time
  of three window launches on the CI runner; a ratio of 1 or less meets the maximum."; a table KPI |
  Median (ms) | Maximum (ms) | Ratio | Met, one row per KPI in `PERF_KPIS` order, the KPI title
  linked to its requirement's page in the requirements viewer (the URL form of
  `test/site/requirementsViewer/urls.ts`), a row over its maximum marked "over its maximum". Without
  `kpi.json`: "No performance run in these reports." A `kpi.json` with another `schema` or a KPI
  unknown to `PERF_KPIS` fails the site build with the file and the reason.
- `buildSite.ts` writes `performance.html` with `pageDocument`, and `site-manifest.json` gains
  `"performance": <true when kpi.json was read>`.
- `siteHeader.ts`: a "Performance" link after "Gallery", before "Requirements".
- The page carries `@implements_req <the new CORE SwRS>`; `test/site/perfPage.test.ts` carries its
  `@tests_req` markers.

### Requirements (okfreq)

Created with `okfreq new ... --lifecycle proposed` (IDs from okfreq, never by hand), then
`just requirements-update` and a dated entry in `requirements/tiers/log.md` under the date of the change.

- New SwRS in scope `review-annotations`, derives from `StRS-MDOKFSTUDIO-REVIEW-003` ("A reviewer
  comments, replies, resolves and deletes...", approved; its authored text is not changed). Title:
  "Selection and comment creation on a large document stay under their maximums". Scenarios:
  - `S1 (nominal): Text selection` - GIVEN the generated issue 547 document in the preview of a real
    VS Code window on the CI runner (`ubuntu-latest`, virtual screen) - WHEN a text selection ends by
    a mouse release, over three window launches - THEN the median time to the Comment button shown
    is at most `<maximumMs of comment-selection>` ms.
  - `S2 (nominal): Comment creation` - the same GIVEN - WHEN a new comment is saved, over three
    window launches - THEN the median time to its highlight drawn is at most `<maximumMs of
    comment-create>` ms.
  `verification_method: test`; criteria: `just ci-perf` on the CI runner. Rationale: the maximums
  are about twice the post-fix medians of the named CI run; a machine other than the CI runner
  compares, it does not judge. `@implements_req` sits at the code that produces the two paths at
  the head under test: the selection handling of `src/page/modules/commentCompose.ts` and
  `handleCreate` of `src/session/features/comments.ts` (where `perf-547-slow-comment-selection`
  leaves them).
- New SwRS in scope `rendering-core`, derives from `StRS-MDOKFSTUDIO-CORE-008` (proposed). Title:
  "The published site shows the performance KPI scores of its heavy run". Scenarios: S1 (nominal)
  the table from `kpi.json`; S2 (boundary) no `kpi.json`; S3 (boundary) a KPI over its maximum is
  marked; S4 (refusal) another schema or an unknown KPI fails the build.
- `SwRS-MDOKFSTUDIO-CORE-076` (proposed): the normative text names `perf` among the heavy jobs a
  version change needs; new scenario `S13 (boundary): The performance KPI job` (the job runs where
  `integration` runs; a red `perf` on a version change makes `tag-release` refuse and list it; it
  does not fail `checks`; `report` takes its stage from `out/ci-artifacts/perf/`; Pages needs it
  green; `select_e2e_run.py` requires it). S5's table and S6's table gain `perf` where they list the
  heavy jobs.
- No approved requirement's authored text changes, so no owner agreement is needed (project
  guidelines, "Approved requirements").

### Guidelines and docs

- `.agents/guidelines/ci.guidelines.md`: rule 11 (the `perf` job, 15 minutes, its test step 10,
  set to twice its healthy duration once measured); rule 13 (`perf` is a real VS Code job run on
  every push to `main` and on a heavy dispatch; it is not part of `checks`); rule 14 (`tag-release`
  needs `checks` and the four heavy jobs; "Release not tagged" lists `perf`); the recovery section
  (`perf` among the jobs re-run by "Re-run failed jobs"; its artifact output).
- `CONTRIBUTING.md`: a short "Performance KPIs" section: what is measured, the score (median, ratio
  to the maximum), `just ci-perf` (CI, enforces) and `just perf-kpi` (local, compares), the report
  folder `out/reports/perf/`, and that a maximum changes in `test/shared/perfKpi.ts` and its SwRS in
  the same PR.
- `AGENTS.md`, "Main targets": `just perf-kpi` and `just ci-perf` added to the CI job list.
- `.agents/glossary/common.md`: **KPI score** (a median time in ms of one measured path and its
  ratio to its maximum, `scoreKpi` in `test/shared/perfKpi.ts`) and **Performance maximum** (the
  time a KPI's median must not pass on the CI runner, set by a SwRS and `PERF_KPIS`).

## Out of scope

- The fix of issue 547 and its measure and generator (`perf-547-slow-comment-selection`).
- Other complex rendering cases, documents or paths (decision 4).
- A history of scores across runs or releases (decision 6); a mark out of 100 (decision 5); counts in
  place of times, a CPU calibration or a dedicated machine.
- When the Pages site deploys: it stays on a release tag, from that tag's heavy run, so "the latest
  run" shown is the heavy run of the latest release.
- `npm run probe`, `test/probe/` and `test/integration/performanceProbe.ts`: unchanged, no limit
  added.
- A claim of conformance to a standard (the request asked about "ISO 28149"; see the open questions).
- Real-window launches on Windows.

## Evidence

- Unit (`just check`):
  - `test/build/perfKpi.test.ts`: `median` with odd and even counts; `scoreKpi` at the maximum (met,
    ratio 1.00), 1 ms over (not met), no sample (error naming the KPI); the shipped `PERF_KPIS` has
    the two ids in order; the maximums of the shipped `test/shared/perfKpi.ts` equal the numbers in
    S1 and S2 of the new REVIEW SwRS, read from that file at the head under test.
  - The campaign script on prepared run reports in a temporary folder (a prepared text only for the
    refusal cases the shipped files cannot hold: a KPI over its maximum, a missing run, a run without
    samples): `--enforce` exits 1 with the FAILED line naming the KPI, without `--enforce` exits 0
    with `OVER (CI maximum)`, a missing run exits 1 in both. Paired with the shipped-file check
    above.
  - `test/site/perfPage.test.ts`: S1 to S4 of the new CORE SwRS, on a `kpi.json` written by the
    campaign script's own writer.
  - `test/site` header test: the "Performance" link in place on every page.
  - `test/build/test_workflows.py`: the `perf` job's `if` for each event (push to `main`, heavy and
    plain dispatch, pull request); its artifact name carries the attempt and `report` downloads its
    `artifact` output; the `tag-release` truth table with `perf` (a version change tags only with
    `checks` and the four heavy jobs `success`; every other `perf` result runs the refusal step,
    whose summary lists `perf`); `pages` and `reports_from_caller` need `perf`; `checks` does not;
    every `needs.<job>` reference is a need; `preflight` runs `ci-perf` after `ci-acceptance` and
    prints the new Windows skip line; `ci-perf` and `perf-kpi` stop with exit 3 on a locked screen
    (`STUDIO_SCREEN_LOCKED=1`) and `ci-perf` ends with its passed or FAILED line.
  - `test/build/test_select_e2e_run.py`: a run whose `perf` is skipped, failed or absent is not
    selected; one with a green `perf` and its live `e2e-perf` artifact is; `studio-reports` older
    than the newest `e2e-perf` attempt is not.
- Requirements: `just requirements-update`, `just requirements-lint`, `just check-markers`, and
  `okfreq validate --check-links --project-root .` with CI's okfreq version.
- Real window, on the branch (CI guideline rule 13): `gh workflow run ci.yml --ref <branch> -f
  heavy=true`. First run: the `perf` job measures; its medians set `maximumMs` and the SwRS numbers
  (decision 3), and its duration sets the two timeouts (rule 11). Second run, at the head with the
  maximums: `perf` green with both ratios at most 1; the `e2e-perf-attempt-<n>` artifact holds
  `perf/kpi.json` and the three run reports; `studio-reports-attempt-<n>` holds `perf/kpi.json`; the
  `studio-site-attempt-<n>` artifact of the `gallery` job holds `performance.html` with the two rows
  and the run's commit and id. The two run ids go in the PR's test plan.
- `just preflight` (on Windows the static stage only; CI runs the others).
- What only CI proves, and when: the timings under the virtual screen and their spread between
  runner instances (first heavy runs of the branch); the job's healthy duration (same); the red of an
  exceeded maximum in a real run is not forced (no knob is added to lower a maximum), it is proved by
  the unit tests of the exit code and the `ci-perf` FAILED line; the Pages page itself appears only at
  the next release tag's deploy.

No host or default matrix: nothing in this CR depends on the agent host or on a shipped default
versus a configured setting.

## Open questions for the Chief of Staff

1. The measure of `perf-547-slow-comment-selection` is not specified yet: will its report give the
   per-sample times of the two spans used here (mouse release to the Comment button shown; Save to
   the highlight drawn), in one window launch per run, and under which scenario name and report
   path? This spec adds only a missing span; if the lower CR measures other spans, which ones are the
   KPIs?
2. The local command runs where the real-window stages run, Linux and macOS; the owner's machine is
   Windows, where they do not run today. Is a Linux or macOS machine the local comparison the owner
   meant, or does "your machine" call for Windows real-window launches (a larger change, not in this
   spec)?
3. A red `perf` blocks a version change at `tag-release` but, on a push without a version change,
   does not fail `report` or `checks` (it is not a test of behaviour that `report` gathers). Should
   it also fail `report` and `checks`, as a red `integration` does?
4. The request asked "Ça se fait en iso 28149?". The intake found no such standard and points to
   ISO/IEC/IEEE 29148 (requirements), ISO/IEC 25010 (time behaviour) and ISO/IEC 25023 (response
   time adequacy, measured against a target, the ratio chosen here). The grill left it unanswered:
   does the owner want that answer, or a mention in the SwRS rationale?
