# CR 195 — Inspector review, round 2

Worktree: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-195 (uncommitted diff).

## Verdict: APPROVE

Round-1 finding 1 (major) is fixed: every untagged version change now reaches the refuse step and
writes "Release not tagged", including the realistic integration failure ⇒ `report` ⇒ `checks`
chain. No new defect in the round-2 workflow logic. The remaining findings are minor or
informational and do not block.

## Round-1 findings: status

1. **Fixed.** Integration failure on a version change.
   - tag-release `if`: `!cancelled() && release-check == success && push && main && (checks ==
     success || bump == 'true')`.
     - bump=false, checks red: skipped, as before.
     - bump=false, checks green: runs. The refuse step is skipped (`bump == 'true'` is false) and
       the tag step runs (`bump != 'true'`).
     - bump=true: always runs, whatever `checks`, `integration` and `stress` report. `!cancelled()`
       is a status function, so a failed ancestor adds no implicit `success()`.
   - Refuse step `if`: `bump == 'true' && !(checks && integration && stress all success)`. It
     cannot fire on a non-bump push. It writes `- checks: $CHECKS` plus the two heavy results,
     prints `::error::` with all three, then exits 1.
   - Tag step `if`: `checks == success && (bump != 'true' || integration == stress == success)`.
     Checks green but heavy red on a bump cannot tag. The step also has the implicit `success()`,
     so it is skipped once the refuse step has failed.
   - Refuse and tag are exact complements on every bump=true combination. The new truth-table
     test enumerates checks × integration × stress over {success, failure, cancelled, skipped},
     for bump true and false, and asserts that complement.
   - Tests: a parametrized table covers the realistic combinations: integration failure with
     checks failure, a cancelled integration, and a checks failure alone. The summary script runs
     for real under bash.
   - Locally: 108 passed (test_workflows, test_select_e2e_run, test_release).
   - Docs: the SwRS-076 boundary row, CONTRIBUTING step 4 and ci.guidelines rule 14 now name
     `checks` and state that an integration failure fails `report`, then `checks`, and that the
     summary is still written.
2. **Fixed.** The SwRS-076 table now has a "`release-check` failed or was cancelled" row (no
   summary, run red), and ci.guidelines rule 14 says the same. That matches the job `if`
   (`needs.release-check.result == 'success'`).
3. **Fixed.** The ci.yml `checks` comment and the ci.guidelines rule 13 title now carry the
   version-change exception.
4. **Documented.** The pre-existing re-run-after-tag limit is now covered by recovery step 5 in
   CONTRIBUTING and ci.guidelines, and in the design note.
5. **Acknowledged.** The release latency is listed as an open point in the design note.

`okfreq validate requirements --check-links`: 1067 requirements, 0 errors, 0 warnings.

## Checked and OK (round-2 additions)

- **Recovery docs** (CONTRIBUTING "Recovering from a red heavy job", ci.guidelines section, refuse
  summary text).
  - Steps match the job graph:
    - After a stress failure, the jobs that re-run are stress, tag-release, release and pages.
    - After an integration failure, they are integration, report, checks, tag-release, release
      and pages.
    - release-check is not re-run and keeps `bump=true`.
  - **2-hour caveat:** accurate. `scripts/e2e-campaign.mjs report` rejects
    `|visual.startedAt - integration.startedAt| >= 2 h` (`maxCampaignAgeMs`). "Re-run failed jobs"
    does not re-run `visual`, so attempt 1's visual campaign is compared with attempt 2's
    integration start.
    - The docs say "more than two hours after this run started". That is slightly conservative,
      because visual starts a little after the run, so it is safe advice.
    - A stress-only failure is unaffected (`report` does not need stress). The design note says
      so.
  - "Re-run all jobs only while no tag exists" is correct. release-check recomputes bump=true
    from the same `event.before`.
- **Doc quotes** (design.md), checked against the fetched pages in
  /private/tmp/claude-502/cr195-driver/docs:
  - Found verbatim in rerun.html:
    - "Re-runs use the privileges of the actor who initially triggered the workflow"
    - "use the same GITHUB_SHA (commit SHA) and GITHUB_REF (git ref) of the original event" (the
      HTML has `<code>` tags around the variable names)
    - "up to 30 days after its initial run"
    - "maximum of 50 times"
    - the `--failed` CLI sentence and `gh run rerun RUN_ID --failed`
  - Found verbatim in rest.html:
    - "Re-run all of the failed jobs and their dependent jobs"
    - "Re-run a job and its dependent jobs"
  - The design note correctly says that the user-facing page does not state the dependents rule.
    This is now backed by an official source.
- **Proof workflow** /private/tmp/claude-502/cr195-driver/zz-rerun-proof.yml.
  - It is valid YAML. actionlint is not installed locally, so I checked the expressions by hand
    and they are valid.
  - Job graph:
    - `ok`: no needs, outputs `bump` and `attempt`.
    - `flaky`: fails on attempt 1 and uploads always.
    - `dependent`: `!cancelled() && needs.flaky.result == 'success'`, so it is skipped on attempt 1.
    - `final`: `!cancelled() && needs.ok.result == 'success'`. It downloads by `name:` with
      `continue-on-error`, writes the summary, and its refuse step fails when dependent is not
      success.
  - Expected attempt 1: ok success, flaky failure, dependent skipped, final failure.
  - `--failed` should re-run flaky, dependent (a skipped dependent) and final. That is exactly
    the open question.
  - The inline `${{ github.run_attempt }}` and `${{ needs.dependent.result }}` in `run:` are not
    attacker-controlled.
- **Pages:**
  - `needs: [tag-release, integration, stress]` and `reports_from_caller: integration == success
    && stress == success` are correct.
  - When tag-release refuses, pages is skipped. A non-bump push outputs no tag, so pages is
    skipped there too.
  - Boolean input from an expression is fine.
- **New-defect hunt:**
  - Checks not green but bump=true: the refuse step runs and the tag step is skipped (two
    independent reasons).
  - Non-bump push with checks red: the job is skipped. With checks green, only the tag step runs.
  - Dispatch or PR: tag-release is skipped. `stress.continue-on-error` evaluates `'' != 'true'`,
    which is true, so stress stays advisory.
  - release-check failing on a non-bump push (unreachable `before`) makes the run red. Before this
    CR, `--tag-before` failed the same way in tag-release, so the behaviour is equivalent.
  - No defect found.

## Findings

1. **[MINOR] design.md cites the wrong artifact code path for Pages.**
   - What design.md says:
     - "download-artifact v4 lists with `latest: true` ... `filterLatest` keeps only the latest
       artifact for each name".
     - "pages gets the newest `studio-reports`".
   - What the code does:
     - That is the list path, which is used for `pattern:`. That covers `report` (`pattern:
       e2e-*`), and it is correct there.
     - Pages downloads with `name: studio-reports`. A single-name download takes the
       `artifactClient.getArtifact(name)` branch (dl.ts around line 75), not `listArtifacts({latest:
       true})`. get-artifact.ts was not fetched, so this case has no source.
   - Impact:
     - I expect getArtifact to return the newest artifact of that name as well.
     - Also, after a stress-only re-run, `studio-reports` exists only from attempt 1 (report is not
       re-run). After an integration re-run, both attempts have it, and the newest is the one to
       pick.
     - The proof workflow's `final` job downloads `proof-flaky` by `name:` on attempt 2, so its
       run settles this case.
   - Fix: correct the citation and point to the proof run's summary ("artifact: attempt 2") as the
     evidence for the name path. No code change.

2. **[NIT] CONTRIBUTING.md line 253 now contradicts itself.**
   - Line 253 says "On push and pull request, CI runs only the simulated tests". Five lines later,
     the new sentence says that a version-change push runs the heavy jobs.
   - Suggest "On a pull request and on an ordinary push, CI runs only the simulated tests".

3. **[NIT] Line length.**
   - .agents/guidelines/ci.guidelines.md line 60, the rule 13 title, is now 140 characters. It
     was rewrapped onto one line, while the rest of the list wraps at 100.
   - Rewrap after "(rule 14).**".

4. **[INFO] Proof workflow handling.**
   - `workflow_dispatch` works only once the file exists on the default branch, so the `push` +
     `paths` trigger on the CR branch is the effective one. That is fine.
   - Make sure the file is deleted from the branch before the CR is squashed or merged.
   - It does not exercise the job-level `continue-on-error` expression on stress. That behaviour
     follows from the expression and is covered by the unit test, so this is acceptable.

5. **[INFO] Re-runs keep the 30-day / 50-attempt limits** (documented in design.md). The release
   push has no other expiry, so a forgotten red release can be recovered within 30 days. After
   that, the only path is a new version. Optionally say so in CONTRIBUTING.

Nothing left running.
