Head: 8b8651581e78e31cc4e0cca65296eef6af98ef8e

Verdict: NOT VERIFIED

Claims (all judged at 8b86515):

1. Heavy run at the head is green (acceptance 5). VERIFIED.
   `gh run view 45238430594 --json headSha,conclusion,jobs` -> headSha 8b8651581e78e31cc4e0cca65296eef6af98ef8e,
   conclusion success; integration, stress, visual, static, static-windows, viewer-graph, report, gallery: success.
2. Local project gate. VERIFIED. work/gates/preflight-8b86515.log ends `ci-static: passed` and `EXIT 0`
   (project gate is local `just preflight`, handed back with --no-gate; ship recorded "no long gate passed", expected).
3. Fix matches spec. VERIFIED by diff (`git diff origin/main...HEAD`): `pendingShow` in rendering.ts, awaited
   after the queue request in `requestDocument` (previewManager.ts) with `@implements_req SwRS-MDOKFSTUDIO-LIFE-003`;
   tests in test/host/openCompletes.test.ts with `@tests_req`; no CI file touched; preview-smoke (trusted-suite.ts) untouched.
   Not run by me: that the host tests fail on 2e2efa6c (an ad hoc `tsx --test` run here failed in the harness without
   `just check`'s compile step, so it proves nothing; not claimed).
4. PR #495 description, as posted at this head. NOT VERIFIED.
   `gh pr view 495 --json body`:
   - Known gaps still says "**UNVERIFIED:** the heavy run ... of the final head is not read yet ... At the previous head
     (39b2232) ... integration failed later". Stale: the heavy run 45238430594 is green at 8b86515, so the claim and the
     gap text are wrong.
   - No heavy run number or link anywhere (spec acceptance 1 and 5 ask for the run of the proof and of the fixed head).
   - Changes lists no round 4-6 work: the `shownRequestId`/`hasPendingShow` wait in `sendPreviewMessageForTests` is
     described only partly, and the RI-T34 test-side waits and the counter sweep of work/r6.md
     (test/integration/realInput/renderPatching.ts, +18 lines at 8b86515) are unmentioned.
   - Test plan boxes are all unchecked; no Review box (`Review: approved at <sha7>`); the Driver log's approvals
     (r6 inspector at 3a32623, committed as 8b86515) are not cited in the body.
   - Description still reads as draft body written at 39b2232 ("PR body refresh not done" per the Driver's own 18:22 note).
   Fix: refresh the body at 8b86515 (run link, causes, test-side waits and sweep list from r6.md, Known gaps rewritten
   or removed, Review box), then run the description pass again.
