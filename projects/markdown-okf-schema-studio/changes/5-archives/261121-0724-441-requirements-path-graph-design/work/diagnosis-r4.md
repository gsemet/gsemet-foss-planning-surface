# Diagnosis r4: the visual job times out at 15 minutes (run 44869064458, PR head d94b5ec)

No file of the worktree was changed. Local timings were taken in the CR worktree
(Windows, warm caches); CI numbers come from `gh api .../jobs` step timestamps and from
`work/ci-visual2.log`, `work/ci-visual3.log`.

## (1) Is anything hung or waiting? No.

- Attempt 1 (job 136739240666, 05:03:45 to 05:19:06): `ci-visual` step 05:04:52 to 05:18:56 (cancelled).
  test:visual ended about 05:17:5x, breakout ended 05:18:01, `okfreq generate-report` ran 05:18:01
  to 05:18:48 (47 s) and logged "Generated"; `okfreq status` had started 05:18:48 and was killed at
  05:18:56 (the timeout), 8 s into a call that takes 14 to 18 s.
- Attempt 2 (job 136743383328, 05:20:09 to 05:35:29): `ci-visual` 05:20:51 to 05:35:20 (cancelled).
  test:visual 05:20:51 to 05:33:55 (13m04), breakout 05:33:55 to 05:34:04 (9 s), generate-report
  05:34:04 to 05:34:57 (53 s), `okfreq status` 05:34:57 to 05:35:15 (18 s, prints 1171 requirements,
  errors 0), then test:viewer-graph started 05:35:15, printed its first test at 05:35:18 and the
  twelve "natural ... box" lines, and was cancelled at 05:35:20, five seconds in. The job was killed
  by the 15-minute limit (05:20:09 + 15 min = 05:35:09 plus cancel latency), while the test was
  progressing normally (the first test passed in 2.5 s).
- No gap between consecutive log lines in either attempt; the orphan-process lists at the end only name
  the process that was running when the cancel arrived (okfreq in attempt 1, the viewer-graph node
  test in attempt 2). Both cancellations are pure budget exhaustion: the total is just over 15 min.

## (2) Healthy duration of each addition

| step | local (this worktree) | CI green 44849558688 | CI cancelled attempts |
|---|---|---|---|
| `okfreq generate-report` with `--output-json` and `--output-summary-md` | 45 s (23 s JSON only, so the Markdown summary costs about 22 s) | about 37 s | 47 s and 53 s |
| `okfreq status requirements` | 14 s | about 19 s (derived) | 18 s |
| `just requirements-report` total | 59.6 s (one run) | about 56 s (with breakout) | about 65 to 71 s |
| `npm run test:viewer-graph` | 16.8 s (node duration_ms 16782; 4 tests: frozen maps 1.9 s, full-ID 0.3 s, every use case of the report at two widths 10.7 s, Play path 3.5 s) | 18.5 s (duration_ms 18548) | not reached (killed at 5 s) |
| both additions | about 76 s | about 75 s | about 90 s |

Why it is cheap in browsers: the test launches Chromium once per `check()` (three calls: frozen, full ID,
report) plus once for the play test, so about 4 launches, not one per page; the pages are visited
sequentially in a single page object. 10.7 s of the 16.8 s is the report-wide test (every use case, 2 widths).
Nothing sleeps or polls. The test is not wasteful; the cost is the report generation, not the browser.

Waste in the additions: `okfreq status` (14 to 18 s) prints counts only and asserts nothing for the viewer
test; `ci-static` already runs the same `just requirements-report` and so does `ci-gallery` (via
`site-assemble`), so the third full parse of 1171 requirements is repeated work. The Markdown summary
(22 s) is not read by `metroMap.browser.test.ts`, which reads only `requirements-report.json`
(`REQUIREMENTS_REPORT_PATH`); nobody in the visual job reads the `.md`.

## (3) Healthy total of the visual job against the 15-minute timeout

Visual job, last green runs (job total from first to last step; ci-visual = the `Run just ci-visual` step):

| run | CR | ci-visual | job |
|---|---|---|---|
| 44870407656 | 445 | 12m51 | 14m05 |
| 44869194660 | 443 | 12m58 | 13m49 |
| 44869184198 | 442 | 12m07 | 12m49 |
| 44869139275 | 444 | 12m48 | 13m31 |
| 44869029183 | 440 | 11m17 | 12m38 |
| 44864898286 | 445 | 13m08 | 14m03 |
| 44861723306 | 444 | 11m54 | 12m58 |
| 44860928294 | 445 | 11m30 | 12m49 |
| 44850923505 | 439 | 11m40 | 12m27 |
| 44849558688 | 441 (with the additions) | 12m48 | 13m57 |
| 44849060999 | 443 | 11m03 | 11m45 |
| 44847400052 | 439 | 12m33 | 13m28 |
| 44838320460 | 440 | 12m45 | 13m44 |
| 44837187125 | 442 | 12m34 | 13m47 |
| 44830737763 | main | 11m47 | 12m53 |
| 44824730554 | 436 | 12m42 | 13m38 |

Without the additions the job is already 11m45 to 14m05 (median about 13m30) against the 15-minute limit:
the margin is 1 to 3 minutes before this CR. The additions cost about 75 to 90 s, so the CR's job is
expected at 13m00 to 15m30 and the cancelled attempts landed at 15m on a loaded evening (five PR runs
started within the same 22 minutes, 05:03 to 05:25). The real cause is that the dominant step,
`test:visual` (484 scenarios in one Playwright run, 11m03 to 13m08 of ci-visual), already uses about 90 %
of the budget; the additions are the last straw, not the cause. The rule-11 healthy duration is about half
the timeout; the job has not been healthy for a while (about 13m on a 15m limit), which is a separate
finding for the steering session.

## (4) Options that respect ci.guidelines.md, ranked

Rule 1 (one job, at most two targets), 5 (jobs independent, share through artifacts), 7 (preflight runs the
same `ci-*` targets in sequence) and 11 (no timeout raise) are respected by each option below. A per-step
timeout (the third idea) is not a fix: rule 11 allows a step timeout only below the job's to name where a
hang stopped; it saves 0 s and would only turn a job-timeout cancel into a step-timeout cancel.

A. Own CI job and `ci-*` target for the two additions (the structural fix; the visual job returns to its
   pre-CR 11m45 to 14m05, and the new job runs in parallel in about 3 min: 40 to 45 s setup with
   `just dev-ci visual`, then about 75 s of additions). Saves about 75 to 90 s in the visual job and
   removes the CR's addition to its risk entirely. Files to change:
   - `justfile`: new `ci-viewer-graph` (requirements-report, then
     `STUDIO_REQUIRE_CHROMIUM=1 STUDIO_REQUIRE_REQUIREMENTS_REPORT=1 npm run test:viewer-graph`, pass/fail
     line, reports under `out/reports/viewer-graph/`); remove the two lines and the comment paragraph from
     `ci-visual`; add `just ci-viewer-graph || failures=$((failures + 1))` to `preflight` (rule 7).
   - `.github/workflows/ci.yml`: new job (copy of the visual job's setup: checkout with LFS, node, uv, just,
     package cache restore, `just dev-ci visual`, `just ci-viewer-graph`, publish reports artifact with
     `-attempt-${{ github.run_attempt }}`, `timeout-minutes: 10` or 15), add it to `checks.needs`
     (rule 6 keeps `checks` the stable aggregate); `report` needs it only if its reports are merged there.
   - `test/build/test_workflows.py`: the tests at lines about 286 to 333 (preflight order, `ci-visual`
     recipe asserts, the breakout test at 292) and the artifact-name test at about 849 (job and artifact
     parametrisation), plus a new test for the new job (timeout, needs in `checks`, target name).
   - Documentation that names the CI jobs: `AGENTS.md` and `CONTRIBUTING.md` (job list in "Main targets"),
     and `scripts/e2e-campaign.mjs`, `test/integration/review-index.ts`, `test/site/reviewIndexText.test.ts`
     only if they enumerate the CI job reports (they mention `ci-visual`; check before changing).
   - Requirement anchor: `requirements/tiers/swrs/rendering-core/SwRS-MDOKFSTUDIO-CORE-081.md` names
     `ci-visual`; its text must name the new target.
B. Trim what the additions do in `ci-visual` (cheapest, smallest diff, partial): add a `requirements-report-json`
   recipe (JSON only, no Markdown summary, no `okfreq status`) and call it from `ci-visual`. Saves about 22 s
   (Markdown) + 14 to 18 s (status) = about 36 to 40 s of the 65 to 70 s; the additions drop from about
   75 to 90 s to about 40 to 50 s. Files: `justfile` (new recipe; `requirements-report` can depend on it or
   share the command), `test/build/test_workflows.py` (if its recipe assertions look at `just requirements-report`
   in `ci-visual`; none do today), the doc comment of `ci-visual`. Estimated job: 12m30 to 14m50 on the loaded
   evening, so it fits but keeps the job within about 10 to 30 s of the limit on a slow runner: it does not give back
   the margin and is not robust on its own.
C. Reuse the report that `ci-static` already writes (rule 5: share through an artifact): needs a workflow
   artifact download in `visual`, and `ci-visual` would still have to generate the report when run locally
   (rule 2), so it adds a workflow branch for about 45 to 60 s saved. Not recommended; A is the clean
   form of the same saving.
D. Run the viewer test inside `ci-static` (the report is generated there already, static ends in about
   5m30 and has a 15-minute limit): saves the whole 75 to 90 s in `visual` and the generation, but `static`
   and `static-windows` do not install Chromium (needs `dev-ci visual` or a Chromium install in `ci-static`
   on two machines), which breaks rule 4's "a job sets up only what its target uses" for the Windows job.
   Not recommended.

Recommendation: A (own job `viewer-graph`, target `ci-viewer-graph`), and add B's JSON-only report to that
new target (about 40 s faster again). B alone is the fallback if the steering session wants a minimal diff,
with the 10 to 30 s margin caveat above.

Reproduction commands used: `just requirements-report`; `okfreq generate-report requirements --output-json ...`
(with and without `--output-summary-md`); `okfreq status requirements`;
`STUDIO_REQUIRE_CHROMIUM=1 STUDIO_REQUIRE_REQUIREMENTS_REPORT=1 npm run test:viewer-graph`
(all in the CR worktree; the test left `out/reports/requirements-viewer-graph/` captures there, ignored by git).
