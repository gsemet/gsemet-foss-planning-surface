# Split the CI visual job in two parts that run in parallel

The CI job `visual` runs out of its 15-minute limit. This change splits its screenshot campaign in
two jobs that run side by side, `visual` and `visual-2`, each about 8 minutes, and merges their
reports in the `report` job. The limit stays at 15 minutes, every check still runs, and no re-run is
needed to pass.

## Goal

Every run of the checks that `visual` runs today ends well under its 15-minute limit: each part
job takes at most 600 s, with `timeout-minutes: 15` unchanged (CI rule 11). No scenario, check or
report is dropped, and no retry is added (CI rules 9 and 12).

## Measured time (the basis of the split)

From run 45773405420, job `visual` 139751185940 (main, 2026-11-26). This is the slowest of the eight
main runs in `intake/request.md`: 890 s of 900.

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

The capture is about 97% of the step. The 4 workers already use the runner's cores, so splitting
the campaign across two runners is the change whose gain the run measures. Making a scenario faster
would first need profiling, which no run gives.

Split at layout-width / theme-zoom:

- Part 1: rendering-core to layout-width, 269 scenarios, 391 s of capture.
- Part 2: theme-zoom to trust-security, 254 scenarios, about 406 s.

Estimated job time: part 1 is 47 + 18 + 391 + 11 (breakout) + 6 ≈ 473 s; part 2 is 47 + 18 + 406 + 6
≈ 477 s. Both are about 53% of the limit. These numbers assume a group costs the same when other
groups run next to it on the same runner. Only the first CI run can confirm that (see "Evidence").

## What changes

### `test/visual/capture.py`

- New option `--part N` (1 or 2). It captures the scenarios of that part's groups, plus the
  canonical scenarios their aliases (`screenshotOf`) need, as `--group` does today.
- The groups of each part are listed in one constant (for example `VISUAL_PARTS`). At startup, the
  script checks that the parts together cover every group of the render manifest exactly once. If a
  group is in no part or in two parts, it exits 2 and names the group. A new group can then never be
  left out without anyone seeing it.
- A part run writes its own files, never the full-run names and never `.partial`:
  `run-manifest.part-N.json`, `INDEX.part-N.md` and `MACHINE-CHECKS.part-N.md` under
  `out/reports/e2e/screenshots/`. A part's manifest has the same fields as `run-manifest.json`,
  plus `"part": N`. It removes only its own scenarios' stale files (the same cleanup as a partial
  run), so the two parts can run one after the other in the same folder.
- The duplicate-PNG check (H1) and every per-scenario check stay as they are, inside each part.
- With no `--part`, `npm run test:visual` (the full run) is unchanged. `scripts/run-e2e.mjs` and the
  Pages fallback suite use it.

### New merge step: `test/visual/merge_parts.py`

Run as `uv run --no-sync --group docs python test/visual/merge_parts.py`. It reads the render
manifest and every `run-manifest.part-*.json`, then writes `run-manifest.json`, `INDEX.md` and
`MACHINE-CHECKS.md`. These have the same format a full run writes today (`partial: false`, results
in manifest order, counts summed, `failures` joined). The index and machine-check writers move into a
shared function so that the full run and the merge produce the same text.

The merge fails (exit 1, with a clear message) when:

- a part manifest is missing;
- a scenario of the manifest is in no part;
- a scenario is in two parts with different results (a canonical scenario pulled in by an alias in
  both parts counts once);
- a part has status `failed`;
- the duplicate-PNG check over the PNGs of both parts finds identical PNGs across the parts.

It keeps `campaignStartedAt` and `startedAt` from the earliest part, and `completedAt` from the
latest.

### `justfile`

- `ci-visual PART=""`. With `PART=1`, it runs `visual:render`, then `capture.py --part 1`, then
  `test:breakout`. With `PART=2`, it runs `visual:render`, then `capture.py --part 2`. With no part,
  it empties `out/reports/e2e/screenshots/`, then runs part 1 and part 2 one after the other. Any
  other value fails with a usage line. Each mode ends with `ci-visual: passed` or `FAILED`, as today
  (CI rule 8). `eval "$(node scripts/e2e-campaign.mjs begin visual)"` stays at the top of every mode.
- `ci-report`: its first step runs `merge_parts.py` (`|| failed=1`), before `compile`,
  `review:finish` and `e2e-campaign.mjs report`.
- `preflight` keeps calling `just ci-visual` (both parts in sequence), then `ci-report` merges. CI
  runs the same steps in parallel (CI rule 7).

### `.github/workflows/ci.yml`

- Job `visual`: its step becomes `just ci-visual 1`. Everything else stays: the name, the output
  `artifact: e2e-visual-attempt-<n>`, the save of the apt cache and the 15-minute timeout.
- New job `visual-2`. It is a copy of `visual` with `just ci-visual 2`, `timeout-minutes: 15` and
  `permissions: contents: read`. It only restores the apt cache, as `viewer-graph` does. It uploads
  `e2e-visual-2-attempt-${{ github.run_attempt }}` and announces that name in its `artifact`
  output.
- `report`: `needs` adds `visual-2`. A step "Download the visual part 2 reports" sits right after
  the visual download. It uses the same form (`if: needs.visual-2.outputs.artifact != ''`,
  `pattern:` that output, `path: out/reports/`, `merge-multiple: true`). The only files the two
  parts both write are `campaign-visual.json` and the render outputs. Both copies carry the run id
  pinned by `STUDIO_E2E_RUN_ID` and come from the same commit, so `e2e-campaign.mjs report` accepts
  whichever copy lands. `e2e-campaign.mjs` does not change.
- `checks`: `needs` adds `visual-2`.
- Update the comments that list the jobs that install Ubuntu packages, and the comment on
  `viewer-graph` ("so that the visual job keeps its time budget").

### Tests and docs

- `test/build/test_workflows.py`:
  - `test_a_consumed_artifact_is_announced_by_its_job` gets `("visual-2", "e2e-visual-2")`.
  - `test_report_merges_each_stage_from_the_attempt_that_produced_it` expects the patterns of
    `visual`, `visual-2` and `integration`, and a re-run case where only `visual-2` is attempt 2.
  - `test_ci_visual_runs_the_table_breakout...` reads the recipe from its new header (`ci-visual
    PART=""`) and checks that the breakout runs in part 1 and in the no-part mode.
  - New: the parts in `ci.yml` (`visual` runs part 1, `visual-2` runs part 2) and `checks` needs
    both.
  - These tests read the shipped `ci.yml` and `justfile` at the head under test.
- A Python test of `merge_parts.py` (in `test/build/`, added to the pytest line of the justfile):
  - one case on two part manifests that cover the manifest, which writes a full manifest;
  - one refusal case each for a missing part, a missing scenario, a cross-part duplicate PNG and a
    failed part.
  - The part manifests here are prepared texts, used only for these cases that a shipped file
    cannot hold. A check on the shipped constant goes with them: the shipped `VISUAL_PARTS` covers
    every group of `test/shared/e2eGroups.ts` exactly once.
- `.agents/guidelines/ci.guidelines.md` rule 4 (the jobs that install Ubuntu packages) adds
  `visual-2`. `AGENTS.md` "CI jobs" and `CONTRIBUTING.md` (where they list the CI jobs) name
  `visual-2` and `just ci-visual [PART]`.

## Compatibility with the pull requests above it in batch-09

This change sits below #529 and #532:

- **#529** touches no CI file that this change edits (only `CONTRIBUTING.md` and test files). If
  both edit the CI job list in `CONTRIBUTING.md`, the conflict is textual only.
- **#532** edits the same blocks as this change. Keep these three points so that its rebase is a
  textual merge:
  1. The `report` job keeps one download step per producer job, each by that job's `artifact`
     output. #532 adds its acceptance download (into `out/ci-artifacts/acceptance/`) after
     integration's.
  2. In `ci-report`, `merge_parts.py` runs first. #532 adds `select-acceptance-attempts.mjs` to
     the same list.
  3. `e2e-campaign.mjs` and its stage names stay untouched (#532 rewrites that file), and
     `visual` keeps its name and its output, because `checks`, `report`, `tag-release` and #532's
     `needs` lists name it.

  #532's edits to `test_report_merges_each_stage_from_the_attempt_that_produced_it` and to the
  `needs` lists then add acceptance next to `visual-2`.

## Out of scope

- Raising any timeout, adding retries, or dropping or skipping a scenario.
- Making a scenario faster. That needs a profile, not part of this change.
- A matrix for the visual parts. One job has one output for all its shards, which is the problem
  #532 solves with its own attempt selector. Two named jobs keep the existing "one output per
  producer" form until #532 lands.
- `viewer-graph`, `integration`, `stress` and the heavy path, apart from `report` merging the
  parts.
- Requirements: CI only, no product behaviour, no SwRS changes.

## Environment of the jobs

`visual` and `visual-2` run on `ubuntu-latest` (image `ubuntu26` in the measured run), set up by
`just dev-ci visual`. Unlike the owner's Windows machine, a runner has no warm npm, uv or
Playwright state beyond the setup actions' caches. `visual-2` only restores the apt archives that
`visual` saves, so on a cache miss it installs from the mirror, as `viewer-graph` does today. The
`report` job (`just dev-ci`, no Chromium) runs `merge_parts.py` with the `docs` group, which
`dev-ci` installs. On Windows, `preflight` skips the visual stage, so the parts cannot be proven
locally on the owner's machine.

## Evidence

Before the push:

- `just check`, which covers `test_workflows.py`, the merge tests, the file-size ratchet and the
  `knip` checks.
- On Linux or macOS if one is available: `just ci-visual` followed by `just ci-report visual` ends
  with `ci-visual: passed` and `ci-report: passed`. The merged `run-manifest.json` has
  `scenarioCount` equal to the render manifest's scenario count, and the same `screenshotCount` as
  `npm run test:visual` at the same head.

Only the pull request's first CI run proves the following. The Driver reads them from
`gh run view <id> --json jobs` and the job logs, and records them:

1. `visual` and `visual-2` are both green. Each one's job duration (completedAt minus startedAt)
   is at most 600 s, against estimates of about 473 s and 477 s.
2. `report` is green. `merge_parts.py` reports both parts, and the merged `run-manifest.json` in
   `studio-reports-attempt-<n>` has every scenario of that head (523 at main 3478f099, plus any the
   branch adds) and `status: passed`.
3. `checks` is green.
4. `visual-2` finds the apt cache that `visual` saved and installs without contacting the mirror
   (`dev-ci: system packages installed from ...`).

After the merge, the first push to `main` repeats points 1 to 3 together with the heavy jobs
(`report ... all`).

If a part takes more than 600 s, the split is redone with the measured group times (for example
three parts). The timeout is never raised.
