# Split the CI visual job in two parts that run in parallel

The CI job `visual` runs out of its 15-minute limit. This change splits its screenshot campaign in
two named jobs that run side by side, `visual` and `visual-2`, each about 8 minutes, and merges
their reports in the `report` job. The limit stays at 15 minutes, every check still runs, and no
re-run is needed to pass.

## Base and place in batch-09

Per item 3 of `02-answers.md` (it replaces item 2), the change sits directly above CR-512
(https://github.com/gsemet/markdown-okf-schema-studio/pull/536, restacked on CR-505 at `54d1da62`)
and below CR-511 (https://github.com/gsemet/markdown-okf-schema-studio/pull/537). The branch starts
from `54d1da62`. Every file this specification names is described as it is at that commit. CR-512
adds only a test commit over CR-505's head `9d7e788a`, so the CI files, the justfile, the scripts
and `test/build/` are CR-505's. The main checkout is behind: do not read the CI files there.

If CR-512's own CI cannot pass because of the `visual` limit, this change moves below CR-512
(item 3). The content of this specification stays the same in that case. Only the section
"Compatibility with the pull requests below and above it" changes, and the Driver adds a short
note on the new place to it.

## Goal

Every run of the checks that `visual` runs today ends well under its 15-minute limit. Each part
job takes at most 600 s, with `timeout-minutes: 15` unchanged (CI rule 11). No scenario, check or
report is dropped, and no retry is added (CI rules 9 and 12).

## Measured time (the basis of the split)

The intake lists eight runs on main, at 804 to 890 s of 900. Since then, run 45794366914 (CR-512,
pull request, head `e76c0843`) shows how much the time varies at a single head:

| Attempt | Job | `just ci-visual` step | Capture (first to last scenario) | Result |
| --- | --- | --- | --- | --- |
| 1 (job 139821112935) | 09:41:54 to 09:57:04, 910 s | 09:42:50 to 09:56:55, 845 s | 09:43:19 to 09:56:44, 805 s | `ci-visual: passed` printed at 09:56:55, one second after the 15-minute limit; the job was cancelled, then the report upload ran |
| 2 (job 139831215788) | 10:01:03 to 10:14:35, 812 s | 10:01:55 to 10:14:26, 751 s | 10:02:18 to 10:14:17, 719 s | passed |

At the same head, the capture took 719 s on one runner and 805 s on another, a gap of about 12%.
A re-run that passes is what CI rule 9 forbids as a fix. The split has to absorb this gap below
the limit.

Details of the slowest main run: run 45773405420, job `visual` 139751185940 (main, 2026-11-26),
890 s of 900.

| Part of the job | Time | From the log |
| --- | --- | --- |
| Job setup up to `just ci-visual` (checkout, toolchains, `just dev-ci visual`) | 47 s | 07:10:53 to 07:11:40 |
| `visual:render` (tsc, esbuild, 225 pages, 523 scenarios) | 18 s | to 07:11:58 |
| `test/visual/capture.py` (523 scenarios, 4 worker threads, 412 PNGs) | 806 s | to 07:25:24 |
| `test:breakout` | 11 s | to 07:25:35 |
| Publish reports | 6 s | to 07:25:41 |

`capture.py` runs the scenarios in the manifest's order, which is the group order. Here is when each
group's scenarios passed, in seconds after the first one:

| Group | Scenarios | First | Last |
| --- | --- | --- | --- |
| rendering-core | 33 | 0 | 69 |
| code-blocks | 23 | 45 | 103 |
| gfm | 13 | 81 | 120 |
| myst | 47 | 98 | 188 |
| diagrams | 22 | 164 | 215 |
| frontmatter-schema | 31 | 197 | 256 |
| frontmatter-editing | 9 | 234 | 268 |
| layout-width | 91 | 253 | 391 |
| theme-zoom | 13 | 373 | 409 |
| toolbar-navigation | 45 | 391 | 493 |
| block-editing | 56 | 469 | 571 |
| palette-slash | 43 | 553 | 654 |
| table-editing | 34 | 655 | 707 |
| review-annotations | 36 | 704 | 758 |
| lifecycle-sync | 23 | 759 | 791 |
| trust-security | 4 | 790 | 797 |

The capture takes about 97% of the step. The 4 workers already use the runner's cores, so the
change these runs measure is splitting the campaign across two runners. Making a scenario faster
would first need profiling, and no run gives a profile.

The visual campaign at `54d1da62` is the same as main's: 523 scenarios, and `test/visual/` is
unchanged apart from the details of three scenarios. The split is at layout-width / theme-zoom:

- Part 1: rendering-core to layout-width, 269 scenarios, 391 s of capture.
- Part 2: theme-zoom to trust-security, 254 scenarios, about 406 s.

Estimated job time:

- Part 1: 47 + 18 + 391 + 11 (breakout) + 6 ≈ 473 s.
- Part 2: 47 + 18 + 406 + 6 ≈ 477 s.

Both are about 53% of the limit. With the 12% gap between runners, the slower runner would take
about 530 s, still under the 600 s bound. The pull requests above add scenarios to both parts (see
"Compatibility"), a few seconds each. These numbers assume that a group costs the same whatever
groups run next to it on the same runner. Only the first CI run can confirm that (see "Evidence").

## Decision: two named jobs, not a matrix

Since CR-505 is below, the base has a matrix job, `acceptance`, with a selector for its sharded
artifacts (`scripts/select-acceptance-attempts.mjs`). So the choice was made again. The decision
is two named jobs, `visual` (part 1) and `visual-2` (part 2), for these reasons:

1. **CR-505's selector does not fit the visual artifacts.** It matches only
   `e2e-acceptance-<group>-attempt-<n>`. It copies one `acceptance/<group>/` folder, which only that
   shard writes, onto `out/reports/acceptance/<group>/`. A visual part uploads the whole
   `out/reports/` tree, and the two parts write into the same folders: `out/reports/e2e/screenshots/`,
   `campaign-visual.json` and the render outputs. A matrix would need a second selector that keeps
   the newest attempt of each part, then lays both trees over `out/reports/`. That means a new
   script, new tests and new SwRS rows. Two named jobs need none of this.
2. **Named jobs keep the download form that the base already proves for `visual` and
   `integration`.** Each job announces one exact artifact name in its `artifact` output. `report`
   downloads it by `pattern` with `merge-multiple: true` into `out/reports/`. After "Re-run failed
   jobs" on one part, the other part keeps its output, so `report` gets the newest attempt of each
   part with no selector. `test_every_ci_download_names_the_artifact_of_the_job_it_needs` and
   `test_report_merges_each_stage_from_the_attempt_that_produced_it` already state this rule for a
   job that is not a matrix.
3. **Pages selection stays simple.** `scripts/select_e2e_run.py` finds a single-job stage artifact
   by its exact base name (`e2e-visual`). A named job adds one base name, `e2e-visual-2`. A matrix
   would rename the artifact to `e2e-visual-<part>`, and the visual stage would then need the
   prefix and job-name handling that CR-505 added for `acceptance (<group>)`.
4. **The apt cache.** `visual` saves the Ubuntu package archives and the other jobs only restore
   them. Two matrix shards would both try to save the same key, unless a matrix condition were
   added to the save step.

What a matrix would have given: one YAML block instead of two, and no new name in the `needs`
lists. Two `needs` lists change (`report`, `checks`). The cost of two jobs is about 60 duplicated
lines of YAML, which the tests of `test_workflows.py` keep consistent.

## What changes

### `test/visual/capture.py`

- New option `--part N` (1 or 2). It selects the scenarios of that part's groups, plus the
  canonical scenarios their aliases (`screenshotOf`) need, as `--group` does today.
- The groups of each part are listed in one constant, `VISUAL_PARTS`, in the order of
  `test/shared/e2eGroups.ts`. At startup, the script checks that the parts together cover every
  group of the render manifest exactly once. If a group is in no part or in two parts, it exits 2
  and names the group. A new group can then never be left out without anyone seeing it.
- A part run writes its own files under `out/reports/e2e/screenshots/`, never the full-run names
  and never `.partial`: `run-manifest.part-N.json`, `INDEX.part-N.md` and
  `MACHINE-CHECKS.part-N.md`. A part's manifest has the same fields as `run-manifest.json`, plus
  `"part": N`. As a partial run does, it removes only the stale files of its own scenarios, so the
  two parts can run one after the other in the same folder.
- `--part` cannot be combined with `--scenario` or `--group`. The script exits 2 with a usage line.
- The duplicate-PNG check (H1) and every per-scenario check stay as they are, inside each part.
- With no `--part`, the full run (`npm run test:visual`) is unchanged. `scripts/run-e2e.mjs` and
  the Pages fallback suite use it. Its purge of `SCREENSHOT_DIR/*.json` already removes stale part
  manifests. Add the `*.part-*.md` files to that purge.
- The code that writes the index and the machine-check report moves into a shared module
  (for example `test/visual/capture_report.py`), so that the full run, a part run and the merge
  write the same text. This also keeps `capture.py` (610 lines) well under the 1 500-line limit of
  `scripts/check-file-sizes.mjs`.

### New merge step: `test/visual/merge_parts.py`

It runs as `uv run --no-sync --group docs python test/visual/merge_parts.py`. It reads the render
manifest and every `run-manifest.part-*.json`, then writes `run-manifest.json`, `INDEX.md` and
`MACHINE-CHECKS.md` in the format a full run writes today: `partial: false`, results in manifest
order, counts summed, `failures` joined, `duplicateImages` joined.

- When there is no part manifest and a full `run-manifest.json` exists (`partial: false`, written
  by `npm run test:visual`), it prints `visual parts: none, the full run's manifest stands` and
  exits 0. A local `ci-report` after a full run still works this way.
- It keeps `campaignStartedAt` and `startedAt` from the earliest part and `completedAt` from the
  latest. It records `"parts": [1, 2]`.
- It prints one line per part (`visual part N: <status>, <scenarios> scenarios, <seconds> s`), then
  `visual parts: merged` or the refusal.

The merge fails (exit 1, with a message that names the cause) when:

- a part manifest is missing, and no full manifest stands in for both parts;
- the parts disagree on `revision` or on `runId` (a stale part from an earlier run);
- a scenario of the render manifest is in no part;
- a scenario is in two parts with different results. A canonical scenario pulled in by an alias in
  both parts counts once;
- a part has status `failed`. The merged manifest is still written, with `status: failed`, so that
  `e2e-campaign.mjs report` names the failures as today;
- the duplicate-PNG check over the PNGs of both parts finds identical PNGs under two different file
  names across the parts. The same file of a canonical scenario captured in both parts is one file.

`// @implements_req SwRS-MDOKFSTUDIO-CORE-076` (Python `#` form) goes at the merge function. A
marker block names at most 3 IDs.

### `justfile`

- `ci-visual PART=""`, with the comment above it updated:
  - `PART=1`: `{{ npm }} run test:visual -- --part 1` (npm passes the argument to `capture.py`, the
    last command of the script), then `STUDIO_REQUIRE_CHROMIUM=1 {{ npm }} run test:breakout`.
  - `PART=2`: `{{ npm }} run test:visual -- --part 2`.
  - No part: empty `out/reports/e2e/screenshots/`, run part 1 then part 2 as above, then
    `merge_parts.py`. `just ci-visual` alone then writes the same full `run-manifest.json` as today
    (CI rule 2).
  - Any other value fails with a usage line and exit 2.
  - In every mode the steps run even when an earlier one fails (`|| failed=1`, as today). Each mode
    ends with `ci-visual: passed` or `ci-visual: FAILED` (CI rule 8).
  - `eval "$(node scripts/e2e-campaign.mjs begin visual)"` stays at the top of every mode.
- `ci-report`: `uv run --no-sync --group docs python test/visual/merge_parts.py || failed=1` is its
  first step, before `{{ npm }} run compile` and `review:finish`. `review-index.ts` reads
  `screenshots/run-manifest.json`, so the merge must come first. The steps that follow stay as
  they are: `select-acceptance-attempts.mjs`, then `e2e-campaign.mjs report $only`. The comment
  above the recipe names the merge.
- `preflight` keeps calling `just ci-visual` (both parts in sequence, then the merge) and later
  `just ci-report`, which merges again (the same result). CI runs the same steps in parallel (CI
  rule 7). The preflight test (`test_preflight_skips_only...`) still finds `just ci-visual`.

### `.github/workflows/ci.yml`

- Job `visual`: its step `just ci-visual` becomes `just ci-visual 1`. Everything else stays: the
  name, the output `artifact: e2e-visual-attempt-${{ github.run_attempt }}`, the restore and save
  of the apt cache, and `timeout-minutes: 15`.
- New job `visual-2`, right after `visual`:
  - The same steps as `visual`, but it runs `just ci-visual 2`, with `timeout-minutes: 15` and
    `permissions: contents: read`.
  - It only restores the apt cache (key `apt-archives-visual-…`), as `viewer-graph` does, with no
    save step.
  - It uploads `e2e-visual-2-attempt-${{ github.run_attempt }}` with `if: always()` and announces
    that name in its `artifact` output.
- `report`:
  - `needs` becomes `[release-check, visual, visual-2, integration, acceptance]`.
  - A step "Download the visual part 2 reports" sits right after "Download the visual stage
    reports", in the same form: `if: needs.visual-2.outputs.artifact != ''`, `pattern:` that
    output, `path: out/reports/`, `merge-multiple: true`.
  - The comment above the downloads says that the two visual parts merge into one tree and that
    `ci-report` merges their manifests.
  - Both parts write `campaign-visual.json` and the render outputs. Both copies carry the run id
    pinned by `STUDIO_E2E_RUN_ID` (`pinnedRunId`) and come from the same commit, so
    `e2e-campaign.mjs report` accepts whichever copy lands. `scripts/e2e-campaign.mjs` does not
    change.
- `checks`: `needs` becomes `[static, static-windows, visual, visual-2, viewer-graph, report]`.
- `tag-release` and `pages` do not change. They reach the visual parts through `checks` and
  `report`.
- Comments to update:
  - On `visual`: "Only the jobs "visual", "viewer-graph" and "gallery" install Ubuntu packages"
    adds "visual-2".
  - On `viewer-graph`: "so that the visual job keeps its time budget" becomes "the visual jobs".
  - The `env` comment that names "the visual, integration and acceptance jobs" becomes "the
    visual, integration and acceptance jobs (visual in two parts)".

### `scripts/select_e2e_run.py`

- `STAGE_ARTIFACTS` adds `"e2e-visual-2"`, after `"e2e-visual"`. A run is then selected for Pages
  only when it holds a live part 2 artifact, and when `studio-reports` is not older than the
  newest attempt of either part. A re-run of `visual-2` alone after `report` then makes the run's
  reports stale, as a re-run of `visual` does today.
- Runs made before this change have no `e2e-visual-2` artifact, so Pages runs the suite for them.
  That is the same consequence as CR-505's acceptance artifacts.
- Update the module docstring's list of artifacts.

### Requirements (SwRS-MDOKFSTUDIO-CORE-076)

This is CI behaviour that the bundle already holds in CORE-076 (artifacts, attempts, the report).
The project rule "every behaviour change touches an SwRS" applies to it:

- S2: "whose `visual` job and `acceptance` shards passed" becomes "whose `visual` and `visual-2`
  jobs and `acceptance` shards passed". "`report` merges `e2e-visual-attempt-1`" becomes "merges
  `e2e-visual-attempt-1` and `e2e-visual-2-attempt-1`".
- S3, first row: "`visual`, `visual-2`, `integration` and `report` output that name as
  `artifact`".
- S4: "whose `static`, `visual`, `visual-2` and `report` jobs succeed".
- S6: the stage artifacts the selection needs include `e2e-visual-2`. Add a row, or extend the row
  "newest `studio-reports` attempt expired, or older than the newest attempt of a stage artifact",
  naming both visual parts.
- New scenario `S12 (boundary): Parts of the visual stage`, declared in `scenarios:`, as a table:
  - `visual` runs part 1 (`just ci-visual 1`) and `visual-2` runs part 2; the parts cover every
    e2e group exactly once, and a group in no part or in two parts stops `capture.py` with exit 2
    and names the group;
  - the report merges both part manifests into one full manifest;
  - a missing part, a scenario in no part, parts from another revision or run id, a failed part,
    or identical PNGs across the parts fail the report and name the cause;
  - after "Re-run failed jobs" on one part, the report merges the newest attempt of each part;
  - a full run with no part manifest stands as it is.
- Frontmatter: `implemented_in_files` adds `test/visual/merge_parts.py` (and `test/visual/capture.py`
  if the `--part` check carries a marker). `tested_in_files` adds the merge test file.
- Markers: `@tests_req SwRS-MDOKFSTUDIO-CORE-076#S12` on each merge test and on the new
  `test_workflows.py` tests of the parts. Existing tests that now check `visual-2` keep their
  `#S3` / `#S8` fragments and add `#S2` where they check the re-run case.
- Run `just requirements-update`. Add a dated entry to `requirements/tiers/log.md`.
- No StRS changes.

### Tests

- `test/build/test_workflows.py` (1 228 lines at the base, limit 1 500). These tests read the
  shipped `ci.yml` and `justfile` at the head under test:
  - `test_a_consumed_artifact_is_announced_by_its_job` gets `("visual-2", "e2e-visual-2")`. It also
    asserts `base in module.REQUIRED_ARTIFACTS`, which the `select_e2e_run.py` change makes true.
  - `test_every_ci_download_names_the_artifact_of_the_job_it_needs`: `seen >= 5` (report: visual,
    visual-2, integration, acceptance; gallery).
  - `test_report_merges_each_stage_from_the_attempt_that_produced_it`:
    - expects the patterns of `visual`, `visual-2`, `integration` and `acceptance`, in that order;
    - the unpacking `*steps, shards = steps` and the `zip` over producers cover
      `("visual", "visual-2", "integration")`;
    - a re-run case where only `visual-2` is attempt 2 (`e2e-visual-attempt-1`,
      `e2e-visual-2-attempt-2`).
  - `test_ci_visual_runs_the_table_breakout_width_tests_with_chromium_required`:
    - splits the recipe at its new header `\nci-visual PART="":`;
    - checks that the breakout runs in part 1 and in the no-part mode, after `run test:visual`, and
      not in part 2.
  - `test_ci_viewer_graph_is_its_own_target...` splits at the same new header.
  - New: in `ci.yml`, `visual` runs `just ci-visual 1` and `visual-2` runs `just ci-visual 2`,
    each with `timeout-minutes: 15`. `visual-2` restores the apt cache and has no save step.
    `checks` and `report` need both.
  - New: `ci-report` runs `merge_parts.py` before `run compile` and before `review:finish`.
  - New: `ci-visual` refuses a part other than empty, 1 and 2 (run through `just --dry-run` or the
    recipe's text, as the tests of `ci-stress` do).
- `test/build/test_select_e2e_run.py`:
  - `ATTEMPT_1` and the fixtures built from `REQUIRED_ARTIFACTS` get `e2e-visual-2-attempt-1`;
  - `test_artifacts_without_an_attempt_suffix_are_not_used` lists `e2e-visual-2`;
  - one case where a run lacks `e2e-visual-2` and is not selected;
  - one case where `e2e-visual-2-attempt-2` is newer than `studio-reports-attempt-1` and is
    rejected.
- `test/build/test_visual_parts.py` (new, added to the `pytest` line of the justfile's check
  recipe, next to `test_unpack_vsix.py`):
  - one case on two part manifests that cover the manifest, which writes a full manifest, index
    and machine-check report equal to what the shared writer gives for the same results;
  - one refusal case each: a missing part, a scenario in no part, a part from another revision, a
    failed part (manifest written, exit 1), and identical PNGs across the parts;
  - one case where a canonical scenario captured in both parts counts once;
  - the case "no part manifest, full manifest present" exits 0 and leaves the full manifest
    untouched.
  - The part manifests in these cases are prepared texts. They are used only for these cases,
    which a shipped file cannot hold. A check on the shipped constant goes with them: it reads
    `VISUAL_PARTS` from the shipped `test/visual/capture.py` and the group ids from the shipped
    `test/shared/e2eGroups.ts` at the head under test, and asserts that each group is in exactly
    one part, in group order.

### Docs

- `.agents/guidelines/ci.guidelines.md`:
  - rules 4 and 11 need no edit at this base: rule 4 lists no job by name, and rule 11's "15 for
    the others" covers `visual-2`;
  - "Recovering from a red heavy job", point 4: "(`visual`, `visual-2`, `integration`, `report`)".
    Add one sentence: the two visual parts are two jobs, each with its own output, and `ci-report`
    merges their manifests first (`test/visual/merge_parts.py`).
- `AGENTS.md`, "Main targets", the CI jobs line: `just ci-visual [PART]` (jobs `visual` and
  `visual-2`).
- `CONTRIBUTING.md`:
  - line 22: "only the visual jobs install them";
  - the CI stage list (about line 289): `just ci-visual 1` and `just ci-visual 2` (two jobs in
    parallel; `just ci-visual` runs both locally, then merges);
  - the `ci-report` sentence: it first merges the two visual parts;
  - about line 297: `ci-visual` (in two jobs);
  - about line 303: "so that the visual jobs keep their time budget";
  - "Releases", point 4 (about line 772): the visual stage comes from two artifacts,
    `e2e-visual-attempt-<n>` and `e2e-visual-2-attempt-<n>`.
- `.github/workflows/pages.yml`: the comment "(e2e-visual, e2e-integration and the e2e-acceptance
  shards)" names `e2e-visual-2`.
- `CHANGELOG.md`: nothing. The project lists user-facing changes there, and this change is CI only.
  If `just check` (`test_changelog_refs.py`) asks for an entry, follow it.

## Compatibility with the pull requests below and above it

Below, in merge order: CR-509 (#529), CR-505 (#532), CR-512 (#536). This change is written on
their content (`54d1da62`).

- **CR-512 (#536)**, directly below: it touches `requirements/tiers/log.md`,
  `test/integration/realInput/`, `test/shared/stressPlan.ts`, a clip and TABLE-120. The only file in
  common is `log.md`, where both changes add an entry: append this change's entry below CR-512's.
  If the change moves below CR-512 (item 3), CR-512's rebase meets the same textual case only.

Above, in stack order: CR-511 (#537), CR-513 (#535), then CR-514 and CR-507, which have no pull
request yet:

- **CR-511 (#537)**: it touches `log.md`, LAYOUT-023 and its index, `test/page/codeBlockBreakout.test.ts`
  and `test/page/runtimePageControls.test.ts`. Its rebase meets a textual case in `log.md` only.
  Its breakout tests run in `test:breakout`, which this change keeps in part 1 (`visual`). They
  add a few tests to the 11 s step.
- **CR-513 (#535)**: today its branch carries CR-505's commits plus two of its own. Those two touch
  `CHANGELOG.md`, `log.md`, FMSCHEMA-023/-084, `src/core/preview/styles/propertiesStyles.ts`, tests,
  and four visual scenarios (`frontmatter-schema/v32` to `v35`, scenario count 523 to 527 in
  `test/site/e2eGroups.test.ts`). `frontmatter-schema` is in part 1, so part 1 grows by 4 scenarios.
  These scenarios need no part list change, since `VISUAL_PARTS` lists groups. Its rebase meets a
  textual case in `log.md` only.
- **CR-514** (spec in `4-batch/2-actives/514-…`): it adds and changes visual scenarios in
  `test/visual/alertEditingScenarios.ts` (groups `block-editing` and `gfm`), in the palette-slash
  scenarios and in `test/visual/capture_edit_checks.py`. That is part 2 and part 1, a few scenarios
  each. It does not touch `capture.py`, the CI files or the justfile recipes this change edits. Its
  first CI run is the first run that includes both changes. Its Driver reads both part durations
  there.
- **CR-507** (spec in `4-batch/2-actives/507-…`): its "How we test" page names the simulated bench
  as "`just ci-visual`, job `visual`" and links `ci.yml`. Once this change has merged below it, the
  page must say "`just ci-visual` (jobs `visual` and `visual-2`, one part each)". The Chief of
  Staff passes this to CR-507's Driver. This change does not edit CR-507's page.

The rules that keep every rebase a textual merge:

1. `visual` keeps its name, its output and its artifact name, because `checks`, `report`,
   `gallery`'s comments and `select_e2e_run.py` name them.
2. `scripts/e2e-campaign.mjs`, `scripts/select-acceptance-attempts.mjs` and the acceptance steps of
   `report` stay untouched.
3. The `report` job keeps one download step per producer job, each by that job's `artifact`
   output. Part 2's step sits between visual's and integration's.

## Out of scope

- Raising any timeout, adding retries, or dropping or skipping a scenario.
- Making a scenario faster. That needs a profile, which is not part of this change.
- A matrix for the visual parts (see "Decision").
- `viewer-graph`, `integration`, `acceptance`, `stress`, `gallery`, `tag-release`, `pages` and the
  heavy path, apart from `report` merging the parts and Pages requiring the part 2 artifact.
- The visual campaign's local entry points other than `ci-visual`: `npm run test:visual`,
  `scripts/run-e2e.mjs`, `just site`.
- Changes to CR-507's page or to the specifications of the CRs above.

## Environment of the jobs

- **The part jobs.** `visual` and `visual-2` run on `ubuntu-latest` (image `ubuntu26` in the
  measured runs) and are set up by `just dev-ci visual`. Unlike the owner's Windows machine, a
  runner has no warm npm, uv or Playwright state beyond the setup actions' caches.
- **The apt cache.** `visual-2` only restores the apt archives that `visual` saves. On a cache miss
  it installs from the mirror, as `viewer-graph` does today. Both jobs start at the same time, so
  on a key change (a new runner image or package set) `visual-2` meets the miss in the same run.
- **The report job.** `report` (`just dev-ci`, no Chromium) runs `merge_parts.py` with the `docs`
  group, which `dev-ci` installs.
- **Locally.** On Windows, `preflight` skips the visual stage, so the parts cannot be proven on the
  owner's machine.
- **The pull request path.** On a pull request, only `visual`, `visual-2`, `viewer-graph`, the
  static jobs, `report` (with `visual`) and `checks` run. The heavy path runs on the first push to
  `main` after the merge.

## Evidence

Before the push:

- `just check`. It covers `test_workflows.py`, `test_select_e2e_run.py`, `test_visual_parts.py`,
  the file-size ratchet, the marker checks and the `knip` checks.
- `uv run --no-sync --group requirements okfreq validate --check-links --project-root .`, and
  `just requirements-update` with its generated files committed.
- On Linux or macOS, if one is available: `just ci-visual` followed by `just ci-report visual` ends
  with `ci-visual: passed` and `ci-report: passed`. The merged `run-manifest.json` has a
  `scenarioCount` equal to the render manifest's scenario count, and the same `screenshotCount` as
  `npm run test:visual` at the same head. When no such machine is available, the Driver says so,
  and the first CI run is the proof.

Only the pull request's first CI run proves the following. The Driver reads it with
`gh run view <id> --json jobs` and the job logs, and records it:

1. `visual` and `visual-2` are both green. The job duration of each (completedAt minus startedAt)
   is at most 600 s, against estimates of about 473 s and 477 s.
2. `report` is green. `merge_parts.py` prints both parts and `visual parts: merged`. The merged
   `run-manifest.json` in `studio-reports-attempt-<n>` has every scenario of that head (523 at
   `54d1da62`, plus any the branch adds) and `status: passed`.
3. `checks` is green.
4. `visual-2` finds the apt cache that `visual` saved and installs without contacting the mirror
   (`dev-ci: system packages installed from ...`).

The first CI run of each pull request above (CR-511, CR-513, CR-514, CR-507), once rebased on this
change, repeats point 1 with their added scenarios. A part above 600 s there is reported to the
Chief of Staff.

After the merge, the first push to `main` repeats points 1 to 3 together with the heavy jobs
(`just ci-report all`). `scripts/select_e2e_run.py` accepts that run only if it holds
`e2e-visual-2-attempt-<n>`.

If a part takes more than 600 s, the split is redone with the measured group times (for example
three parts). The timeout is never raised.

## Open questions

None. Item 3 of `02-answers.md` decides the place and when it moves. The Chief of Staff decided
that no spec critic is needed.
