# Verify CR-460

Head: 42d01082d2850fedfbdffd5c60f6e62d9fa668f7

Claims, each judged at 42d01082d2850fedfbdffd5c60f6e62d9fa668f7.

1. Gate pass at the head. `chantier log CR-460` line: `driver gate result=pass head=42d01082d2850fedfbdffd5c60f6e62d9fa668f7 command=just preflight run=20261121-215516-13712`. Worktree `git rev-parse HEAD` = the same SHA; `git status --short` empty.

2. Real-window tests ran and passed. `gh run view 44949474643 --json headSha,conclusion` gives headSha 42d01082d2850fedfbdffd5c60f6e62d9fa668f7, conclusion success; jobs integration and stress success. Integration job log (`gh run view 44949474643 --log --job 136984002960`, saved to work/scratch/integ.log):
   - `STEP start: diff-preview-scroll` 21:16:05, `STEP done: diff-preview-scroll (4899 ms)` 21:16:10
   - `Extension host test runner exit code: 0`, `ci-integration: passed`, no "skip" line in the log.
   The step is registered in `test/integration/trusted-suite.ts` (`["diff-preview-scroll", runDiffPreviewScroll]`, in the diff). The suite logs per step, not per case; the step runs D1 (inline scroll follows) and D2 (staged-like diff, both layouts) in sequence in `test/integration/diffPreviewScroll.test.ts` (read at the head), each ending in an assert or waitFor that throws on failure; a failure would fail the step and exit code. Limit: D1 and D2 are not logged individually.

3. Tests only, no behaviour change. `git diff --stat origin/main...HEAD`: only requirements markers and log, test/host/diffPreview.requirements.test.ts, test/integration/diffPreviewScroll.test.ts, trusted-suite.ts, test/shared/e2eGroups.ts, test/site/e2eGroups.test.ts; nothing under `src/`.

4. PR description (posted, `gh pr view 473`, headRefOid = the head): renders with sections; Summary, Changes match the diff (D1/D2 test file, host test, trusted suite and e2e groups, requirements markers and log); no image; Deliverables "None (tests only)"; Known gaps absent and nothing unverified is claimed as fact (the real-window run is said to be heavy CI only, proved by claim 2); Internal references holds only CR ids. Unchecked boxes Review/CI green are the Driver's to tick.

No visual deliverable, so no before/after evidence.

VERIFIED
