# Verify CR-425 (round 1, second pass on the description)

Head: ae78222488c50c41ea12e9cb12f3d622f04e7418

Verdict: VERIFIED at ae78222 (second pass: the posted description now matches work/pr-body.md; every code and CI claim of the first pass is carried, the head is unchanged).

Raw log: `work/verifier/run-44719877177.log` (gh run view 44719877177 --log).

## Claims

1. Diff matches the spec (A: waits removed in pasteUrl, dropFiles, findInPreview, comment and SwRS-PALETTE-264 Method
   updated, integrationEditModeRestore docblock; B: checkboxToggle uses harness `currentPreviewFrame`, `waitFor`,
   `waitForRender` with the `myst-checkbox` condition, `markProgress` before each frame lookup, Known issue in BLOCK-058;
   C: MutationObserver recorder in previewEditing; stress plan). Judged at ae78222.
   Command: `git diff --stat origin/main...HEAD` and `git diff origin/main...HEAD -- <paths>` (13 files, test-only plus
   requirements text; no `src/` change). `storedEditModeForTests` is still read by findInPreview.test.ts:109,151, so keeping the hook is right
   (`git grep -n storedEditModeForTests`). Pass.
2. Default stress list unchanged, paste-url and drop-files on demand only. ae78222.
   `STRESS_ON_DEMAND_SCENARIOS` is not in `STRESS_SCENARIOS_BY_HOST.trusted`; `hostStressPlan` adds them only when
   `STUDIO_STRESS_SCENARIOS` is set; test `test/build/stressPlan.test.ts` covers it. The justfile "19" count matches the
   plain-run stress log, which lists 19 default names (runs 44719883032 etc.). Pass.
3. Stress proof, carried from 6fffa85 (clean rebase onto 7644edd9, range-diff `=`, `carry` event in `$CHANTIER log`).
   Run 44719877177 conclusion success at headSha 6fffa859...; stress job log: `STUDIO_STRESS_REPEAT: 30`,
   `STUDIO_STRESS_SCENARIOS: paste-url,drop-files,checkbox-toggle`, `stress: 30 round(s) of paste-url, drop-files,
   checkbox-toggle`, `stress: 30 round(s) passed`, `ci-stress: passed (30 rounds)`; no STEP TIMEOUT. Pass.
4. Integration proof, carried from 6fffa85, same reason. Runs 44719877177, 44719883032, 44719890659, 44719897362 all
   `success` (`gh run view <id> --json conclusion,headSha,jobs`); each integration log has `STEP done:` for paste-url,
   drop-files, find-in-preview, preview-editing and checkbox-toggle (e.g. 44719877177: 2847, 1949, 3680, 32500, 2132 ms);
   stock-coexistence then checkbox-toggle ran in order with no timeout. Pass. Limit: four green runs show no regression,
   they cannot prove a flake gone; the CR states this itself (checkbox-toggle cause not found, Known issue).
5. PR checks at ae78222 (`gh pr view 435 --json statusCheckRollup`): static, static-windows, visual, report, checks
   SUCCESS; integration, stress, gallery skipped (PR path). Pass.
6. Long gate: gate log first line `gate CR-425 ... head 6fffa8597c90fff9f22bbdcda03d3a3dbdb1d435`, `$ just preflight`,
   result pass in `$CHANTIER log` (driver gate, 10:37:45Z), carried to ae78222 by the `carry` event (clean rebase). Pass.
7. Review box: `$CHANTIER log` has "r1 inspector approved at 82c11a4 ... committed as d7da84bf" and "move
   d7da84b..6fffa85 inspector approved at 6fffa85". No note of an approval at ae78222 itself; the body's
   "approved at ae78222 (carried from 6fffa85)" is backed by the `carry` event. Pass.
8. Impacts: "No visual change", no screenshots due; no image in the description. Pass.
9. Description as posted on PR 435, judged at ae78222 (pass 2). Command: `gh pr view 435 --json body,headRefOid -q
   '.headRefOid, .body'`; output: headRefOid `ae78222488c50c41ea12e9cb12f3d622f04e7418` and the body of work/pr-body.md.
   The Test plan names `ae78222 (carried from 6fffa85)` for local gates, review, heavy dispatches and CI; the heavy and
   CI boxes are checked (proofs: claims 3 to 6); the first box (new tests) is unchecked by design and says the
   real-window changes are proved by the heavy dispatches. No `d7da84b`, no STALE mark. Sections render; the mermaid
   and ts blocks are fenced; no image. Summary, Deliverables, Changes match the diff (claim 1); Known gaps has its three
   bullets (on-demand stress, checkbox cause unfound, no local real-window run). Role names: none outside Internal
   references. PASS. (Pass 1 failed this claim only on the stale Test plan.)

## Evidence

No before/after: test-only change, no UI. Real-window proof is CI (claims 3 and 4).
