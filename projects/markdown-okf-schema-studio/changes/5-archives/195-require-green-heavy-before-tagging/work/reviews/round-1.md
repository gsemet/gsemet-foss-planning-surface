# CR 195 — Inspector review, round 1

Worktree: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-195 (uncommitted diff vs
origin/change-requests/182-pages-reuse-review-fixes).

## Verdict: CHANGES NEEDED

One major defect: when **integration** fails on a version-change push, no "Release not tagged"
summary is written. That is the most likely heavy failure (the known integration hang). Everything
else is sound.

## Checked and OK

- `continue-on-error: ${{ needs.release-check.outputs.bump != 'true' }}` is valid. GitHub's
  context availability table lists `github, needs, strategy, vars, matrix, inputs` for
  `jobs.<job_id>.continue-on-error`. With a job-level `continue-on-error: true` a failed job
  surfaces to dependants as success, so turning it off on bump=true is the right way to make
  `needs.stress.result` show the failure. On a dispatch or PR, release-check is skipped, its output
  is `''`, and `'' != 'true'` keeps stress advisory as before.
- `!cancelled()` on integration and stress is needed now that they `need` release-check, which is
  skipped outside a push to main. The conditions are correct:
  - pull_request: skipped;
  - dispatch without heavy: skipped;
  - dispatch with heavy: runs;
  - push with bump=false: skipped;
  - push with bump=true: runs.
- tag-release on a push without a version change: release-check succeeds and outputs bump=false.
  The refuse step is skipped and the tag step runs; `tag_release` returns None, so `release` and
  `pages` are skipped. This is unchanged behaviour. `version_changed` and `tag_release` share
  `pushed_versions`, so the two decisions cannot diverge.
- Pages `reports_from_caller`:
  - The input exists only under `workflow_call`, so a manual dispatch or a tag push cannot set it.
  - A called workflow runs inside the caller's run (same `github.run_id`). `download-artifact`
    without `run-id` therefore reads the caller's `studio-reports`, which the `report` job uploaded
    before `checks` → `tag-release` → `pages`.
  - A failed download keeps the safe fallback: `continue-on-error`, a warning, then the suite runs.
  - The FOUND and DOWNLOAD expressions evaluate correctly in both paths.
- `select_e2e_run.py`: no checks were weakened.
  - Dispatch runs keep exactly the old checks.
  - Push runs also need `head_branch == main`, a completed green run, both `integration` and
    `stress` at `success`, and the three artifacts.
  - Push runs without a version change are rejected because their heavy jobs are skipped.
  - The explicit `--run-id` path still fails closed.
  - One query per event is correct.
- Recovery ("Re-run failed jobs" on the same push run, attempt 2):
  - The failed heavy job re-runs with every dependant: `report` and `checks` (for integration),
    then `tag-release`, `release` and `pages`.
  - release-check is not re-run. Its outputs from attempt 1 carry over, and
    `github.event.before`/`github.sha` are the same event payload.
  - Artifact names repeat across attempts. `download-artifact` v4 resolves a name to the newest
    artifact. The repo already relies on this (`STUDIO_E2E_RUN_ID` comment), so it is not a new risk.
- Tests: 104 pass locally (test_workflows, test_select_e2e_run, test_release). The new tests fail on
  the old code: there is no `release-check` job, push runs are rejected, and `--bump-since` is
  unknown. No assertion was weakened, and requirement markers are present.
  `okfreq validate --check-links`: 0 errors, 0 warnings.

## Findings

1. **[MAJOR] An integration failure on a version-change push produces no "Release not tagged"
   summary, and the docs and SwRS say it does.**
   - **Chain of events:**
     - `report` needs `integration` and runs `just ci-report all`.
     - `scripts/e2e-campaign.mjs report` sets `exitCode = 1` when the integration stage failed or
       its manifest is missing (justfile `ci-report`; e2e-campaign.mjs lines 156/162/172).
     - So `report` fails, then `checks` fails, and `tag-release` (`needs.checks.result ==
       'success'`) is **skipped**.
     - The refuse step never runs: no summary and no explanation. This hits the integration hang
       case (timeout → manifest missing), which the design note calls the likely release blocker.
     - Only a stress failure reaches the refuse step.
   - **Test gap:** `test_tag_release_needs_the_heavy_jobs_and_runs_on_every_push_to_main` and the
     parametrized step test use `checks="success"` with `integration="failure"`. That combination
     cannot occur.
   - **Wrong docs:**
     - The SwRS-076 boundary row "version change, `integration` or `stress` not `success` →
       tag-release ... writes 'Release not tagged'" does not hold for integration.
     - The same applies to CONTRIBUTING step 4 and ci.guidelines rule 14.
   - **Fix (suggested):**
     - tag-release `if`: `!cancelled() && needs.release-check.result == 'success' && push && main
       && (needs.checks.result == 'success' || needs.release-check.outputs.bump == 'true')`.
     - Refuse step `if`: `bump == 'true' && !(checks == 'success' && integration == 'success' &&
       stress == 'success')`. Add `- checks: $CHECKS` to the summary and the `::error::`.
     - Tag step `if`: `needs.checks.result == 'success' && (bump != 'true' || (integration ==
       'success' && stress == 'success'))`.
     - Add tests with the realistic combinations: integration failure ⇒ checks failure, which must
       produce the summary; checks failure alone on a version change must also produce it.
     - Keep the no-bump path: checks red ⇒ tag-release skipped, as before.
     - Update the SwRS boundary rows, CONTRIBUTING and ci.guidelines to match.
     - As an alternative, keep tag-release as it is and add a small summary step or job that runs
       when bump == 'true' and checks failed. Either way, every no-tag outcome on a version change
       must leave a summary.

2. **[MINOR] Cancellation and release-check failure leave no summary.**
   - If the run is cancelled (`!cancelled()` false) or release-check itself fails (for example,
     `before` is unreachable after a force push), tag-release is skipped silently.
   - The run is red or cancelled, so this is acceptable. Document it in the SwRS boundary table:
     the "cancelled" row exists, but there is no "release-check failed" row. Adding a summary is
     optional.

3. **[MINOR] Stale wording.**
   - ci.yml `checks` comment (lines 305-306): "the real VS Code jobs are manual and optional".
   - ci.guidelines rule 13 title "Real VS Code jobs are manual".
   - Both now have an exception (version-change pushes). Adjust them, for example "manual, except
     on a version-change push (rule 14)".

4. **[INFO, pre-existing, not introduced] Partial failure after tagging.**
   - Suppose tag-release pushed the tag and then `release` or `pages` failed. A re-run of the failed
     jobs re-runs only those jobs, which keep `needs.tag-release.outputs.tag` from attempt 1, so it
     works.
   - But if tag-release itself is re-run after pushing the tag, `tag_release` prints "already
     exists" and outputs no tag, so release and pages are skipped.
   - This is unchanged by this CR. Optional backlog follow-up.

5. **[INFO] Release latency.** On a version-change push, `checks` now waits for integration
   (report needs it), and tag-release waits for stress (about 30 min). This is intended, and the
   design note's open point acknowledges it.
