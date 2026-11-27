# The heavy CI finishes faster: integration and stress run in two parts

## Goal

A heavy run (every push to `main`, or `gh workflow run ci.yml --ref <branch> -f heavy=true`) takes
about 20 min because two jobs run their real VS Code windows one after the other: `integration`
(18.2 to 18.8 min) and `stress` (16.1 to 16.3 min) (runs 45893802335 and 45838037906, `request.md`).
Each of them becomes two parts that run side by side, each about 10 min or less. The same tests run
the same number of times, the same gates hold, and `just ci-integration`, `just ci-stress` and
`just preflight` still run everything on one machine.

Place: batch-09 (stack), branch above CR-517 (`chantier/batch-09/cr-517-a-comment-updates-only-its-highlights-an`,
PR 550), below CR-518 `perf-kpi-real-window-tests`. At most 6 rounds (answers, item 3).

## Design in one line

Both jobs keep their names and become a two-leg `strategy.matrix` with `fail-fast: false`, like
`acceptance`. GitHub reports `needs.integration.result` and `needs.stress.result` as `failure` when
one leg fails, so `report`, `gallery`, `tag-release` and `pages` read the same names and keep their
expressions unchanged. The jobs show as `integration (1)`, `integration (2)`, `stress (1)` and
`stress (2)`.

## What changes

### The split of `integration` (`test/integration/run-tests.ts`, `test/shared/runnerArgs.ts`)

Measured inside `integration` (run 45893802335): `scroll-sync-suite` 124 s, trusted launch part 1/2
about 7 min, trusted launch part 2/2 about 8.2 min, the other suites a few seconds each.

- New launcher argument `--part <1|2>`, integration mode only, parsed by `parseRunnerArgs` before any
  manifest is written or any VS Code starts.
  - Part 1: `scroll-sync-suite`, `untrusted-suite`, trusted launch 1, `standalone-suite`,
    `reverse-migration-suite`, reload campaign. That is today's order without trusted launch 2.
    Estimate: about 9.7 min of tests.
  - Part 2: trusted launch 2 only (`real-input`, `preview-editing`). Estimate: about 8.5 min of tests.
  - Without `--part`, the run is unchanged (all launches in today's order).
  - Refused with an error that names the argument, as `--group` is today: a `--part` value other than
    1 or 2, `--part` given twice, and `--part` together with any scope flag (`--trusted-only`,
    `--untrusted-only`, `--scroll-only`, `--reload-only`, `--reverse-migration-only`) or with
    `--acceptance-only`.
- The launch list of a run comes from one pure function, for example `integrationLaunches(suites, part)`
  beside `trustedLaunches` in `test/shared/trustedParts.ts`. `main` follows that list, so a unit test
  can show that parts 1 and 2 together are exactly the full run.
- `integration-manifest.json` gains `part: "1" | "2"` when a part runs. Its name and place do not change.

### `justfile`

- `ci-integration PART=""` works like `ci-visual PART`. It accepts `""`, `1` or `2`, and anything
  else fails with `usage: just ci-integration [1|2]; got '<value>'` and exit 2. It still checks the
  screen first (`_require-unlocked-screen`) and begins the `integration` campaign. With a part it
  runs `npm run test:integration -- --part <PART>`. Its comment names the CI jobs
  `integration (1)` and `integration (2)`.
- `ci-stress REPEAT=env("STUDIO_STRESS_REPEAT", "11") SHARD=env("STUDIO_STRESS_SHARD", "")`. It
  accepts `""`, `1` or `2`, and anything else fails with `ci-stress: SHARD must be 1 or 2 (or empty),
  got <value>` and exit 2. It exports `STUDIO_STRESS_SHARD`. The `passed` line names the shard when
  one is set.
- `ci-report`: the integration parts are merged first, beside `test/visual/merge_parts.py` and before
  `review:finish`, which reads `integration-manifest.json` (new script, next section).
- `preflight` does not change: it calls `just ci-integration` with no part.

### The stress shards (`test/shared/stressPlan.ts`)

Share the scenarios between the shards, not the rounds (answers, item 2). Every scenario keeps all
its rounds in one VS Code window.

- `hostStressPlan` reads `STUDIO_STRESS_SHARD` (`""`, `1` or `2`; any other value throws, naming the
  variable). With a shard set, the trusted plan (the default or the one `STUDIO_STRESS_SCENARIOS`
  narrows) keeps the scenarios at positions 0, 2, 4 and so on for shard 1, and 1, 3, 5 and so on for
  shard 2, in plan order. The untrusted window (`untrusted-read-only`) belongs to shard 2. A shard
  with nothing left for a window returns `undefined`, as a narrowed plan does today. The window then
  logs `stress: no scenario of the ... window was asked for`.
- The launch deadline (`launchDeadlineMs` and `stressDeadlineLine` in `test/shared/hangWatchdog.ts`)
  already comes from `hostStressPlan`. It therefore follows the shard with no change of its own.
- The default plan has 21 trusted scenarios at 11 rounds. Shard 1 gets 11 of them, about 8 min.
  Shard 2 gets 10 of them plus the untrusted window, about 7.5 min. `DEFAULT_STRESS_REPEAT` stays 11.
- In a shard, the scenarios of a round have different neighbours than before. A failure caused by
  that is a flake to fix at its cause (CI rule 12). It is never a reason to change the sharding.

### New script `scripts/merge-integration-parts.mjs`

This script plays the role of `scripts/select-acceptance-attempts.mjs` for the integration parts
(same layouts, same "newest attempt wins" rule), and adds the manifest merge.

- It reads every `e2e-integration-<part>-attempt-<n>` folder under `out/ci-artifacts/integration/`.
  It also reads the layout where a single artifact was extracted straight into that folder.
- Per part, it keeps the newest attempt even when that attempt holds no report. An older attempt
  never stands in for it.
- It copies each kept part's tree into `out/reports/`, except its `e2e/integration-manifest.json`
  and `e2e/campaign-integration.json`.
- It writes `out/reports/e2e/integration-manifest.json` as a full run would:
  - `scope` `all`, no `part`;
  - `status` `passed` only when both parts are present and `passed`; otherwise `failed`, with an
    `error` naming each missing or failed part and its attempt;
  - `startedAt` from the earliest part and `completedAt` from the latest;
  - its campaign fields and `campaign-integration.json` aligned on the earliest part, under the run
    id pinned by `STUDIO_E2E_RUN_ID`. That is what `_align_campaign` in `test/visual/merge_parts.py`
    does for the visual parts, so `scripts/e2e-campaign.mjs report` and
    `test/integration/review-index.ts` accept the result as one campaign.
- With no download (a local `ci-report` after `just ci-integration`), it changes nothing.
- Only `ps.txt` under `e2e/hang-dumps/post-step/` is written by both parts. The merged tree keeps
  one copy (diagnostics only), and each part's own artifact keeps its own. The evidence checks that
  no other file is written by both parts.
- It carries `// @implements_req SwRS-MDOKFSTUDIO-CORE-076` at the merge function.

### `.github/workflows/ci.yml`

- `integration`:
  - `strategy: { fail-fast: false, matrix: { part: [1, 2] } }`;
  - test step `xvfb-run --auto-servernum -s "-screen 0 2600x1440x24" just ci-integration "${{ matrix.part }}"`;
  - upload name `e2e-integration-${{ matrix.part }}-attempt-${{ github.run_attempt }}`;
  - output `artifact: e2e-integration-*-attempt-*` (a pattern, as `acceptance` does);
  - its comment explains the split.

  Timeouts stay as they are: job 30, step 20. Rule 11's text names those values, and a part of
  about 10 min stays below them.
- `stress`:
  - `strategy: { fail-fast: false, matrix: { shard: [1, 2] } }`;
  - `STUDIO_STRESS_SHARD: ${{ matrix.shard }}` in the env of its step, which stays `just ci-stress`;
  - upload name `stress-integration-${{ matrix.shard }}-attempt-${{ github.run_attempt }}`.

  `continue-on-error` and the job timeout of 30 stay as they are.
- `report`: the step "Download the integration stage reports" uses `pattern: ${{ needs.integration.outputs.artifact }}`
  and `path: out/ci-artifacts/integration/`, with no `merge-multiple`.
- `heavy` input description: the new durations (about 10 min for each integration and stress part,
  2 min for acceptance).
- Not touched: `checks`, `gallery`, `tag-release`, `release`, `pages`, `release-check`, and every
  other job.

### `scripts/select_e2e_run.py` (the green heavy run that a later Pages build reuses)

- A green heavy run needs `integration (1)`, `integration (2)`, `stress (1)` and `stress (2)` to
  succeed. A run made before this change still qualifies with its bare `integration` and `stress`
  jobs.
- The stage artifacts become `e2e-integration-1` and `e2e-integration-2`, or the bare
  `e2e-integration` of a run made before this change. They are checked in the "older than
  `studio-reports`" test as they are today.

### Requirements, guidelines, docs

- `SwRS-MDOKFSTUDIO-CORE-076` (proposed, so its text may change):
  - S2 names the artifacts `e2e-integration-1-attempt-<n>` and `e2e-integration-2-attempt-<n>`
    (re-running the failed part only);
  - S3's table says `integration` outputs a pattern;
  - S6's table names the parts;
  - S12 is retitled "Parts of the visual, integration and stress jobs" and gains their lines.

  It gets no new scenario ID. Then `just requirements-update`, and a dated entry in
  `requirements/tiers/log.md`.
- `.agents/guidelines/ci.guidelines.md`:
  - rule 11: the step of 20 holds for each integration part;
  - rule 12: `stress` runs in two shards that share the scenarios;
  - rule 13: the leg names, and that a red part fails `report`;
  - the recovery section: "Re-run failed jobs" re-runs the failed part only, and `report` keeps the
    newest attempt of each part.

  Rule 14 does not change.
- `AGENTS.md`, "Main targets": `just ci-integration [PART]` and `just ci-stress [REPEAT] [SHARD]`.
  `CONTRIBUTING.md` changes wherever it describes the two jobs or their targets.
  `docs/how-we-test.md` (rule 16) changes wherever it describes how the two jobs run, and shows
  `just ci-stress [REPEAT] [SHARD]` (line 56).
- The commands that read a heavy run by job name must list the legs `integration (1)`,
  `integration (2)`, `stress (1)` and `stress (2)`: `.agents/guidelines/release-process.guidelines.md`
  (step 4, lines 66-72, and the stack variant near line 166) and `CONTRIBUTING.md` near line 668. As
  written today they would list no red leg.

## Decisions (`02-answers.md`)

1. A CR of its own, in batch-09, after CR-517 and before CR-518. The invariants are the same tests,
   the same repetitions, the same gates and the same local targets. This specification chooses how
   the work is shared.
2. Keep the change small: split what the two jobs already do, and reuse the targets and the report
   merge (`ci-visual PART`, `select-acceptance-attempts.mjs`, `merge_parts.py`). Share the stress
   scenarios between the shards, never their rounds. The heavy run that proves the change runs on
   this CR's own branch.
3. At most 6 rounds.

## Out of scope

The pull-request jobs, `visual` and `visual-2`, `acceptance`, `toc-loop`, CR-517's `perf-547` job,
any change to a test step, a scenario, a timeout budget or the product, and any change to the
trusted parts (`TRUSTED_PART_STEPS`).

## Evidence

Environment: the parts run on `ubuntu-latest` under `xvfb-run`, from a fresh checkout. There is no
local VS Code and no warm npm or uv cache beyond the setup actions. On the owner's Windows machine
the real-window stages do not run (`preflight` runs only `ci-static`), so the split itself is proved
by CI.

Before the push, on the head under test (`just check`):

- `test/build/runnerArgs.test.ts` covers:
  - `--part 1` and `--part 2` are parsed;
  - every refusal listed above is refused;
  - parts 1 and 2 together give the full run's launch list in its order, and do not overlap.
- `test/build/stressPlan.test.ts` covers:
  - shards 1 and 2 of the default plan, and of a narrowed plan, together give the unsharded plan
    with the same `repeat`, and do not overlap;
  - `untrusted-read-only` is only in shard 2;
  - an invalid `STUDIO_STRESS_SHARD` throws;
  - the computed deadline of each shard is at most the unsharded one.
- A new test of `scripts/merge-integration-parts.mjs` (beside `test/build/selectAcceptanceAttempts.test.ts`)
  covers these cases:
  - both parts passed: the result is `passed`, with scope `all` and the earliest start;
  - one part failed: the result is `failed`, naming the part;
  - one part missing: the result is `failed`, naming the part;
  - attempt 2 of a part without a report beats its attempt 1: the result is `failed`;
  - the campaign is aligned under a pinned run id;
  - with no download, nothing changes.
- `test/build/test_workflows.py`, reading `.github/workflows/ci.yml` and the `justfile` at the head:
  - both matrices, with `fail-fast: false`;
  - the step commands and envs, the artifact names and the pattern;
  - the `report` download;
  - `ci-integration` and `ci-stress` reject a bad PART or SHARD with exit 2, and still stop on a
    locked screen.

  The existing tests of `tag-release`, `pages`, `gallery` and `checks` pass unchanged: that is the
  proof that the gate expressions did not change. `test/build/test_select_e2e_run.py` covers the
  part jobs and artifacts, and a run made before this change.
- `just requirements-lint`, and `just preflight` (on Windows, its static stage).

After the push: one heavy dispatch on this CR's branch,
`gh workflow run ci.yml --ref <branch> -f heavy=true`.

- It is green: `integration (1)`, `integration (2)`, `stress (1)`, `stress (2)`, `acceptance`,
  `report` and `gallery`.
- The PR body holds a table with the whole run's duration and each job's duration, next to runs
  45893802335 and 45838037906.
- The logs show the same work as before:
  - the launches of `integration (1)` plus `integration (2)` are the launches of the run before the
    split;
  - the `PASS stress <r>/11 <name>` lines of both stress legs, together, give 21 trusted scenarios
    plus `untrusted-read-only`, 11 rounds each;
  - the `report` log accepts the merged integration manifest.
- A listing of the two `e2e-integration-*` artifacts shows that no file other than the manifest,
  the campaign and the hang-dump `ps.txt` is written by both parts.

Only the first CI run can prove the durations, the pattern download layout, the matrix job names
returned by the API, and that both parts start on separate runners. No host or default matrix
applies: no product behaviour changes.

That one red leg turns `needs.<job>.result` to `failure` is expected GitHub behaviour that this
repository does not prove (its only matrix has one leg). It matters most for `stress` on a version
change, whose only gate at `tag-release` is `needs.stress.result`. The Coder cites the GitHub
documentation sentence in the PR; if none says it, one dispatch with a forced red integration leg
(reverted afterwards) must show `gallery` skipped.

## What CR-518 then adapts

The gate expressions and job names stay, so CR-518's design holds. Its rebase meets these points:

- `test/shared/runnerArgs.ts` and `main` in `test/integration/run-tests.ts`:
  - CR-518's `--perf-only --launch <k>` goes beside `--part`;
  - `--perf-only` is also refused together with `--part`;
  - its launch path stays outside `integrationLaunches`.
- `perf`, "built like `integration`": it copies the setup steps and the `if`, not the `strategy`
  matrix. It stays one job, with its own `timeout-minutes`.
- `SwRS-MDOKFSTUDIO-CORE-076`: its new `S13` stays free, since this CR adds no scenario ID. S5 and
  S6 gain `perf` in the wording this CR leaves there (part names in S6).
- `.agents/guidelines/ci.guidelines.md`: its rule 11 and 13 edits rebase on the wording above; rule
  14's "three heavy jobs" is unchanged here.
- The `heavy` input description: it adds the perf job to the new durations.
- Its heavy runs: with `perf` about as long as a part, the run's length stays about the same.

## What CR-519 then adapts

CR-519 `perf-kpi-pages` is written with the bare job names. Its rebase must:

- write `REQUIRED_JOBS` and its S6 rows in the leg form (`integration (1)`/`(2)`, `stress (1)`/`(2)`),
  never putting the bare names back;
- place its `perf` download step beside the integration pattern download in `report`;
- add its rule 13 sentence on the report downloads to the wording this CR leaves.

## Settled questions (`02-answers.md`, items 4 and 5)

- The visual jobs stay out of this CR; a heavy run of about 13 to 14 min is accepted.
- If a part measures clearly above 11 min, it is the Coder's call from the measured run (move a suite
  to the other part, or add a third part), with the same tests, repetitions, gates and local targets,
  and the choice written in the PR.
