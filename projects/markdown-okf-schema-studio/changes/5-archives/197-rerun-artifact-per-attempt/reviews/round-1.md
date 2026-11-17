# CR 197: Inspector review, round 1

Worktree: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-197 (uncommitted Coder changes)

## Verdict: APPROVE

No blocking findings. The design holds on a real `--failed` re-run, the consumers all read the
producer's announced name, tests would fail without the fix, and the gates are green.

## Gates run (inspector)

- `uv run --no-sync pytest test/build -q`: 136 passed, 0 skipped
  (/private/tmp/claude-502/cr197-inspector-pytest.log)
- `npm run compile` then `node --test out/test/site/e2eCampaign.test.js`: 9/9 pass, 0 skipped
- `just check`: exit 0. okfreq validate: 1067 requirements, 0 errors. lint and update-coverage:
  no change (/private/tmp/claude-502/cr197-inspector-just-check.log)

## What I checked

- **Design on `--failed`.** Job-level `outputs.artifact` is a static expression using
  `github.run_attempt`, so it is set even when the job fails. Jobs that are not re-run keep their
  attempt-1 outputs. `report` depends on `integration`, so GitHub re-runs it with it. Only `stress`
  re-run: `report` is not re-run, and Pages still gets `studio-reports-attempt-1`, which is
  correct. A skipped, cancelled or never-started producer has an empty output. The new
  `if: needs.X.outputs.artifact != ''` guards prevent an empty `pattern` from downloading every
  artifact, and an exact-name `pattern` with no match downloads nothing. `ci-report` then reports
  the missing stage. On a PR, `integration` is skipped, so `report` downloads only visual, the same
  result as the old `e2e-*`.
- **pages.yml.** In the caller path, an empty `reports_artifact` falls back to the suite, which is
  safe and tested. The selection path writes `run_id=` and `artifact=` lines to GITHUB_OUTPUT, and
  both download steps use `steps.reports.outputs.artifact`. The decide step is unchanged.
  `pages` in ci.yml now `needs` report. Its `if` is unchanged and its `needs.*` references are
  covered by the existing test.
- **Selector.** It picks the newest attempt by numeric compare (tested 9 vs 10). It fails closed
  when the newest report has expired (no fallback to an older attempt) or when a stage attempt is
  newer than the report. Names without the suffix are rejected, so the suite runs. Jobs are queried
  with the default `filter=latest`, which is consistent with this. `--reports-artifact-of`
  (site-from-run) uses `{owner}/{repo}`, which gh api expands. The recipe is a bash shebang
  recipe, so `$artifact` persists between its lines.
- **Gap relaxation.** The gap is waived only when both campaign files carry `pinnedRunId: true`
  and the same `runId`. Locally, `begin visual` exports STUDIO_E2E_RUN_ID only into its own recipe
  shell. Even inside one shell, the first stage is never marked pinned, so local campaigns keep the
  2 h limit (tested: three negative combinations). `NaN` still fails.
- **Coverage of the old names.** No consumer of the old fixed names is left (git grep over
  .github, scripts, justfile and docs). release.yml and release-notes.yml upload their own
  artifacts, which nothing downloads across attempts.
- **Requirements.** Only SwRS-MDOKFSTUDIO-CORE-076 (proposed) and log.md changed. None of the 16
  locked StRS were touched, and coverage generation changed nothing.
- **Tests.** No weakened assertion. Existing assertions were updated to the new output format
  (`run_id=`/`artifact=`). New tests would fail on the old code: unsuffixed upload names,
  `has_artifacts` with fixed names, and no `pinnedRunId`. The workflow tests check that every
  download is `needs.<producer>.outputs.artifact` of a job it needs, and that this output matches
  the upload. The pages find step runs as real bash with a fake `uv`.
- **Docs.** CONTRIBUTING step 4 and ci.guidelines step 4 match the behaviour. The "Re-run all
  jobs after 2 h" advice was removed consistently, and so was the tag-release summary text.

## Non-blocking notes

1. **The proof has not run yet.** `.github/workflows/rerun-proof-197.yml` is untracked. The Driver
   must push it, run `gh run rerun <id> --failed`, and record the run URL plus the attempt-2
   summary before deleting it. The summary should show `stable-attempt-1` and `flaky attempt 2`.
   The proof already shows the two key assumptions: a failed job's static output is set (consumer,
   attempt 1), and a job that is not re-run keeps its outputs (attempt 2).
2. **Suggested addition to the proof (recommended, cheap).** Add `permissions: actions: read` and a
   consumer step that lists `gh api repos/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID/artifacts
   --jq '.artifacts[].name'` into the summary. The selector assumes this endpoint lists the
   artifacts of all attempts. If it listed only the latest attempt, the selector would fail closed
   on re-run runs: the suite would run (safe), but site-from-run would refuse. A second step with
   `pattern: proof-missing-attempt-1` would also prove that a no-match pattern download succeeds,
   which `report` relies on for a cancelled producer.
3. scripts/e2e-campaign.mjs:59: `pinned` is any non-empty STUDIO_E2E_RUN_ID, including one a
   developer exports in their shell or in `.env` (justfile has `set dotenv-load`). Such campaigns
   would skip the 2 h check. To be stricter, also require `GITHUB_RUN_ID` (or
   `GITHUB_ACTIONS=true`). This is low risk, so it is optional.
4. .github/workflows/ci.yml:318 (gallery): `name: ${{ needs.report.outputs.artifact }}` has no
   empty guard. That is fine today, because gallery runs only after a successful `report` (no
   `!cancelled()`), but it is worth a one-line comment, or the same `!= ''` guard for symmetry.
5. Runs made before this change (unsuffixed names) can no longer be used by `just site-from-run`
   or the Pages selection, which falls back to the suite. This is documented in the SwRS boundary
   table. Mention it in the PR body.
6. test/build/test_select_e2e_run.py:264 lacks a `@tests_req` tag (cosmetic).
