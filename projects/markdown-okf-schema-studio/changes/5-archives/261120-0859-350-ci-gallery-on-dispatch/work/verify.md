# Verify CR-350, Build the gallery and site on a heavy CI dispatch

Head: 412ca69b05bff98bc3fcbe7b2453543726856656

Third pass (description only) at 412ca69, below; the sections after it are the pass at 768570c,
carried.

## Description pass at 412ca69

Head: `git rev-parse HEAD` = `gh pr view 428 --json headRefOid` = 412ca69b05bff98bc3fcbe7b2453543726856656,
base `chantier/batch-06/cr-349-name-the-stuck-tooltip-when-the-capture-` (eabbe0f). Behaviour
(C1-C10, gate) carried from 768570c: clean rebase, same patch (`$CHANTIER log CR-350`: `driver carry
head=412ca69... verdict_from=768570c... gate_from=768570c...`). `git diff --name-only eabbe0f HEAD` =
the same six files, each named in Changes. Posted body = `work/pr-body.md` (diff: trailing newline only).

E1. Heavy dispatch box. PASS at 412ca69.
`gh run view 44694304978 --json headSha,event,attempt,conclusion,jobs` -> `412ca69b05bff98bc3fcbe7b2453543726856656
workflow_dispatch attempt=2 success`; integration, stress, report, gallery, checks = success;
release-check = skipped. `--attempt 1` -> `failure`: integration=failure, report=failure,
checks=failure, gallery=skipped, stress=success. `--attempt 1 --log-failed`: `STEP failed:
checkbox-toggle (180469 ms): STEP TIMEOUT: ... last progress marker: waiting for the first checkbox
render`. `gh api .../runs/44694304978/artifacts` -> `studio-site-attempt-2 108991148 expired=false`
at head_sha 412ca69 (no studio-site-attempt-1 in that run). `gallery` ran only because its `if`
needs `workflow_dispatch && inputs.heavy` (C1), so `-f heavy=true` holds.
Earlier dispatch 44690391950: `412ca69... workflow_dispatch a=2 failure`, integration=failure,
gallery=skipped; attempt 1 the same (steps per the driver notes, preview-editing then paste-url).
PR run 44690331953: `412ca69... pull_request success`, gallery=skipped, checks=success.

E2. Review box `approved at 412ca69 (carried from 768570c)`: note `r1 approved at abeb761, committed
as 768570c` (C9) and the carry event above. PASS.

E3. Known gaps "None." PASS at 412ca69: the body holds no `**UNVERIFIED:**`, `before-after.md` lists
both pairs captured, no claim of this note failed and was accepted; the red attempts are
unrelated real-window flakes in files this diff does not touch (no `src/` or `test/integration/`
file in the diff above), reported in the Test plan. No `STALE` mark; no image; renders.

Verdict at 412ca69: VERIFIED.

## Pass at 768570c (carried)

Head then: 768570c0f6c317b0bacdb9360a96e50f3c136dd6

Second Verifier pass, at the same pushed head as the first. Base:
`abeb761a9ea8815888f2bb59d3e114ef83979598` (CR-349's branch). The move is the PR description
only: `git log --oneline abeb761..HEAD` = one commit, `768570c0 ci: build the gallery and site on
every heavy dispatch`; `git rev-parse HEAD` = the Head line; `gh pr view 428 --json headRefOid` =
`768570c0f6c317b0bacdb9360a96e50f3c136dd6`; `git status --short` empty before and after the checks.
So C1-C9 are carried; D1 and D2 (the failed claims) and the posted description are judged again.

Verdict: VERIFIED.

## Gate

Carried from 768570c: no code change. Gate log `work/gates/20261120-013404.log`, first line
`gate CR-350 branch chantier/batch-06/cr-350-build-the-gallery-and-site-on-a-heavy-ci head 768570c0f6c317b0bacdb9360a96e50f3c136dd6`,
`$ just preflight`, last line `result: pass at 768570c0f6c317b0bacdb9360a96e50f3c136dd6`.

## Claims carried from the first pass

Each is carried from 768570c: no code change (same head, no commit since); the full command and
output of each stays as recorded at that head by the first pass:

- C1. Workflow change matches the spec, no other job changed (`git diff abeb761 768570c -- .github/workflows/ci.yml`). PASS, carried from 768570c: no code change.
- C2. The removed exemption fails on the base workflow. PASS, carried from 768570c, and now proved by a run too (C10).
- C3. Unit tests, the new test included (`4 passed, 71 deselected`). PASS, carried from 768570c: no code change.
- C4. `just check` exit 0 (pytest `176 passed`, node tests fail 0, requirements valid). PASS, carried from 768570c: no code change.
- C5. Requirements (CORE-076 sentence and rows, log entry; lint 0 errors). PASS, carried from 768570c: no code change.
- C6. Docs (`ci.guidelines.md` rule 13, `CONTRIBUTING.md` lines 283-285). PASS, carried from 768570c: no code change.
- C7. A heavy dispatch builds the gallery and uploads `studio-site-attempt-1` (run 44652636266). PASS, carried from 768570c: no code change.
- C8. The pull request run stays green, `gallery` skipped (run 44647678655). PASS, carried from 768570c: no code change.
- C9. Review box "Review: approved at 768570c": `$CHANTIER log CR-350` note `r1 approved at abeb761, committed as 768570c`. PASS, carried from 768570c: no code change, the note is unchanged.

Run states re-read at 768570c:
`gh run view 44652636266 --json headSha,event,conclusion` -> `768570c0f6c317b0bacdb9360a96e50f3c136dd6 workflow_dispatch success`;
`gh run view 44647678655 --json headSha,event,conclusion` -> `768570c0f6c317b0bacdb9360a96e50f3c136dd6 pull_request success`.

## New claim

C10. The skip-propagation test of the head fails on the base workflow and passes on the head's.
PASS at 768570c (spec Evidence 3, before/after pair 2, captured now). `git show
abeb761:.github/workflows/ci.yml > work/scratch/base-ci.yml`; `git hash-object` of it =
`0254a4b960c0b2a2e8c6052cc1cad08b9ae4bb87` = `git rev-parse abeb761:.github/workflows/ci.yml`.
A probe imports `test/build/test_workflows.py` from the worktree, sets its `CI` to the workflow
given and calls `test_every_job_after_a_skippable_job_opts_out_of_the_implicit_success`:
`uv run --no-sync python work/scratch/probe_base.py . work/scratch/base-ci.yml` ->
`FAILED against base-ci.yml: gallery: needs a skippable job but has no !cancelled()`, exit 1;
`uv run --no-sync python work/scratch/probe_base.py . .github/workflows/ci.yml` ->
`PASSED against ci.yml`, exit 0. Scratch removed after.

## PR description (as posted: `gh pr view 428 --repo gsemet/markdown-okf-schema-studio --json body,headRefOid,baseRefName,isDraft`)

Draft, base `chantier/batch-06/cr-349-name-the-stuck-tooltip-when-the-capture-`, headRefOid
768570c. Summary, Deliverables (Mermaid flowchart, YAML sketch, table), Changes, Impacts and Blast
radius are unchanged in substance from the first pass and match the diff:
`git diff --name-only abeb761 768570c` = `.agents/guidelines/ci.guidelines.md`,
`.github/workflows/ci.yml`, `CONTRIBUTING.md`, `requirements/tiers/log.md`,
`requirements/tiers/swrs/rendering-core/SwRS-MDOKFSTUDIO-CORE-076.md`,
`test/build/test_workflows.py`, each named in Changes; nothing claimed is missing. No image, no
role name outside an internal-references context. Renders: sections, list continuation lines,
links.

D1. Test plan complete, each proof with its SHA. PASS at 768570c (was FAIL).
- "CI green at 768570c": links run 44647678655; proved by C8 and the re-read above
  (`pull_request success` at 768570c).
- "Dispatch run on this branch at 768570c": links run 44652636266, `release-check` skipped,
  `integration`, `report`, `gallery` green, `studio-site-attempt-1` uploaded: proved by C7.
  "no `-f gallery`": the run API has no inputs (as the first pass said); the default `true` is
  proved by C1 and C3, so the outcome stands either way.
- Earlier dispatch 44647675614 at the same commit: `gh run view 44647675614 --json
  headSha,event,attempt,conclusion,jobs` -> headSha 768570c, `workflow_dispatch`, attempt 2,
  `integration=failure` (step `Run xvfb-run ... just ci-integration`), `report=failure`,
  `checks=failure`, `gallery=skipped`. `gh run view 44647675614 --log-failed`:
  `STEP start: paste-url` ... `STEP failed: paste-url (12422 ms): Timed out waiting for the
  workspace to remember edit mode off.` at `out/test/integration/pasteUrl.test.js:175`. "Which
  this change does not touch": the diff above holds no file under `src/` or `test/integration/`.
  "Passed on the next dispatch": 44652636266 `integration=success` (C7).
- "Local gates ... at 768570c": the gate and C4. "Review: approved at 768570c": C9.
  "Requirements": C5. "Changelog: No user-facing change": CI only, per C1 and C6.

D2. Tests item and Known gaps. PASS at 768570c (was FAIL). The item now says the test failed with
"gallery: needs a skippable job but has no !cancelled()" with the exemption removed and the
workflow not yet changed, run while making the change and not re-run on the base commit since.
The failure it states is proved by C10 (the same test function, at the head, on the base's
workflow, same message), and the narrowing is exact (no checkout of the base commit was run).
`work/verifier/evidence/before-after.md` now records both pairs as captured, and no claim of this
note failed and was accepted, and the description holds no `**UNVERIFIED:**` claim: Known gaps
"None." is right.

No `STALE` mark in the description.

## Evidence

`work/verifier/evidence/before-after.md`: pair 1 (heavy dispatch, base run 44651923296 vs head
run 44652636266) and pair 2 (the head's test on the base and head workflows, C10), both captured.
