# Design: require a green heavy run before tagging

## Job graph (ci.yml)

```
release-check (push to main only) --bump--> integration --+--> report --> checks --+
                                  \-------> stress -------+                        |
static, visual ------------------------------------------> report/checks          |
tag-release  needs [checks, release-check, integration, stress] <-----------------+
release      needs tag-release
pages        needs [tag-release, integration, stress]
```

- `release-check`: `if: push && refs/heads/main`; runs `scripts/version.py --bump-since
  $BEFORE_SHA` and outputs `bump=true|false`. `--bump-since` uses `version_changed()`, which shares
  `pushed_versions()` with `tag_release()`: the same test decides "heavy runs" and "tag".
- `integration`, `stress`: `needs: release-check`,
  `if: !cancelled() && ((dispatch && inputs.heavy) || needs.release-check.outputs.bump == 'true')`.
  `!cancelled()` because release-check is skipped on PRs and dispatches.
- `stress`: `continue-on-error: ${{ needs.release-check.outputs.bump != 'true' }}`. It stays
  advisory everywhere except on a version change, where it blocks. Reason: with a job-level
  `continue-on-error: true`, a failed job can surface as `success` to `needs.<job>.result`, so
  tag-release could not see a red stress run.
- `report`: also needs release-check; merges `all` stages on a version change.
- `tag-release` (round 2, review finding 1): `if: !cancelled() && needs.release-check.result ==
  'success' && push && main && (needs.checks.result == 'success' || bump == 'true')`. Without a
  version change, red checks skip it as before. On a version change it always runs (an integration
  failure fails `report`, then `checks`), so it can say why:
  - step "Refuse to tag a version change without a green heavy run":
    `if: bump == 'true' && !(checks == 'success' && integration == 'success' && stress ==
    'success')`; writes "Release not tagged" with the three results and
    `gh run rerun <run_id> --failed` to `GITHUB_STEP_SUMMARY`, `::error::`, exit 1.
  - step `tag`: `if: checks == 'success' && (bump != 'true' || (integration == 'success' && stress
    == 'success'))`.
  - Tested by a truth table over every result (success/failure/cancelled/skipped) of checks,
    integration and stress, for bump true and false.
- `release-check` failed (e.g. `before` unreachable) or run cancelled: heavy jobs, tag-release,
  release, pages skipped, no summary; the run is red/cancelled (documented in SwRS-076).
- `pages`: passes `reports_from_caller: integration == 'success' && stress == 'success'`.

## pages.yml

New `workflow_call` input `reports_from_caller` (boolean, default false). When true, the find step
skips the selector (the calling run is still in progress, so the API selection cannot find it)
and a new step downloads `studio-reports` from the current run (no `run-id`); the decide step
uses that outcome; failure falls back to the suite with a warning, as before. Other paths
(tag push, manual dispatch, explicit `run_id`) are unchanged.

## select_e2e_run.py

Also accepts a `push` run: `head_branch == 'main'`, same sha, completed, conclusion success,
and both `integration` and `stress` jobs with conclusion `success` (skipped/failed/absent
rejected), plus the existing artifact checks. Dispatch runs keep their exact checks (integration
only). The automatic query runs once per event (the API filters on one event).

## What happens when 1.0.1 merges

1. Push to main with package.json 1.0.0 -> 1.0.1. Jobs: static, visual, release-check (bump=true);
   then integration and stress (stress blocking); report (`all`); checks.
2. tag-release runs after all of them.
   - Green (checks, integration, stress success): `version.py --tag-before` tags v1.0.1; release
     publishes; pages builds the site from this run's `studio-reports` (no suite re-run).
   - Red heavy (e.g. stress failure): the run is red, tag-release writes "Release not tagged"
     (integration: X, stress: Y) to the summary and fails; no tag, release and pages skipped.
     Only this push can tag 1.0.1 (a later push has no version change): re-run the failed jobs
     (tag-release re-runs with them) or fix and release 1.0.2.
   - checks red (including after an integration failure): tag-release refuses with the summary.
   - No version change and checks red: tag-release skipped (as before).
3. A later manual Pages dispatch of v1.0.1 finds this push run through the selector.

Release (release.yml) builds its own VSIX and uses no e2e reports: nothing to change there.

## Recovery: "Re-run failed jobs" on the same run

### Official sources (fetched 2026-10-29)

- Requested page, https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-workflow-runs/re-running-workflows-and-jobs
  (301 to https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs). It does NOT state that dependent jobs re-run. It
  states, verbatim:
  - "Re-runs use the privileges of the actor who initially triggered the workflow, not the
    privileges of the actor who initiated the re-run."
  - "The workflow will also use the same GITHUB_SHA (commit SHA) and GITHUB_REF (git ref) of the
    original event that triggered the workflow run."
  - "You can re-run a workflow run, all failed jobs in a workflow run, or specific jobs in a
    workflow run up to 30 days after its initial run."
  - "A workflow run can be re-run a maximum of 50 times."
  - CLI: "To re-run failed jobs in a workflow run, use the run rerun subcommand with the --failed
    flag." (`gh run rerun RUN_ID --failed`)
- The dependent-jobs sentence is in the REST reference,
  https://docs.github.com/en/rest/actions/workflow-runs, endpoint "Re-run failed jobs from a
  workflow run", verbatim: "Re-run all of the failed jobs and their dependent jobs in a workflow
  run using the id of the workflow run." (and "Re-run a job from a workflow run": "Re-run a job and
  its dependent jobs in a workflow run.")
- `gh run rerun --help` (local gh): "--failed       Rerun only failed jobs, including dependencies".
- Not stated by any doc: that *skipped* dependents (dependent, release, pages) re-run, and that
  jobs not re-run keep their outputs. The throwaway proof workflow below shows both on CI.

### Conditions on attempt 2 (checked)

- `github.run_attempt`: 2; `github.run_id` unchanged. `STUDIO_E2E_RUN_ID` is `github.run_id` on
  purpose (ci.yml comment), so attempt 2 keeps the campaign id.
- Same sha / ref: documented (quote above). `github.event.before`: same event payload (the re-run
  replays the original push event); shown by the proof workflow. tag-release's `--tag-before
  $BEFORE_SHA` therefore computes the same version change.
- release-check outputs: release-check succeeded, so it is not re-run; its `bump=true` output is
  read from attempt 1 (proof workflow: `ok` output read by `final`).
- Artifact names: upload-artifact v4 artifacts are immutable and a name cannot be uploaded twice
  in one attempt, but a re-run attempt creates a new artifact of the same name; download-artifact
  v4 looks an artifact up by `name:` and, if several share the name, takes the latest (not
  verified against the source here). `report` downloads by `pattern:` and pages downloads
  `studio-reports` by `name:` (a different code path from the `pattern:` one), so whether a re-run
  produces a name conflict for `studio-reports` is settled by the proof run, not assumed. The
  expected result is that `report` gets attempt 2's `e2e-integration` and attempt 1's
  `e2e-visual`. The proof workflow uploads `proof-flaky` on both attempts and downloads it in `final`.
- GITHUB_TOKEN for tagging: the token permissions come from the workflow file at the same sha
  (tag-release `contents: write`), and re-runs use the privileges of the original actor (quote
  above). No problem.
- tag-release idempotency: after "Release not tagged" no tag exists, so attempt 2 tags normally.
  Known limit (review finding 4, pre-existing, out of scope): if tag-release is re-run after it
  pushed the tag (e.g. "Re-run all jobs" after a release failure), `tag_release` prints "Tag vX
  already exists" and outputs no tag, so release and pages are skipped. Recovery for that case:
  "Re-run failed jobs" (re-runs only release/pages, which keep `needs.tag-release.outputs.tag` from
  the attempt that tagged) or dispatch Release VSIX with the tag (CONTRIBUTING "Recovery and
  Release Notes"). Documented in CONTRIBUTING and ci.guidelines.
- REAL LIMIT FOUND, documented (not changed): `scripts/e2e-campaign.mjs report` fails when the
  visual and integration stages started 2 hours apart or more (`maxCampaignAgeMs`). "Re-run failed
  jobs" after an integration failure does not re-run `visual` (it passed), so a re-run started
  more than ~2 hours after the run fails `report`, hence `checks`, hence no tag. Recovery then:
  "Re-run all jobs" (`gh run rerun <id>`), safe while no tag exists (same sha, same `before`,
  release-check recomputes bump=true). A stress-only failure is not affected (report does not
  depend on stress). Written in the refusal summary, CONTRIBUTING and ci.guidelines. Possible
  follow-up: relax the gap check when both stages carry the same CI run id.
- Re-runs are possible for 30 days, at most 50 times.

### Proof workflow (throwaway, outside the repo)

`/private/tmp/claude-502/cr195-driver/zz-rerun-proof.yml`: jobs `ok` (passes, outputs bump and
its attempt), `flaky` (fails on attempt 1, uploads `proof-flaky` always), `dependent` (needs
flaky, `!cancelled() && needs.flaky.result == 'success'`), `final` (needs ok+dependent,
`!cancelled()`, writes run_attempt/sha/event.before/ok outputs/artifact to the summary, refuses
when dependent is not success). Expected attempt 1: ok success, flaky failure, dependent skipped,
final failure. After `gh run rerun <id> --failed`: ok not re-run (ok_attempt=1), flaky, dependent,
final success; summary shows run_attempt 2, same sha and event.before, artifact "attempt 2".

## Open points

- `just version` / release checklist: no dispatch-and-wait added; the push run itself is the
  heavy run.
- The known integration hang (P1) would now block a release push until fixed or re-run.
