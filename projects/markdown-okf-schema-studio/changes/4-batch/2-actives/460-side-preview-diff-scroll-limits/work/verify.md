# Verify CR-460

Head: 39f2419d132633ebaeacbb3ace6a9357c042765a

All claims judged at 39f2419d132633ebaeacbb3ace6a9357c042765a (the 42d01082 verdict is void after the rebase and is rejudged).

1. Gate pass at the head. `work/gates/20261121-230530.log` first line: `gate CR-460 branch chantier/batch-07/cr-460-side-preview-scroll-follows-only-the-rea head 39f2419d132633ebaeacbb3ace6a9357c042765a`, last line `result: pass at 39f2419d132633ebaeacbb3ace6a9357c042765a` (`just preflight`). Worktree `git rev-parse HEAD` is the same SHA; `git status --short` empty.

2. Real-window tests pass at the head. `gh run view 44951690958 --json headSha,conclusion,jobs`: headSha 39f2419d..., conclusion success, jobs integration, stress, visual, static, static-windows, report, gallery all success. Log of that run: `STEP start: diff-preview-scroll` 21:59:06, `STEP done: diff-preview-scroll (5059 ms)`, `ci-integration: passed`. The step runs D1 (inline layout scroll follows) and D2 (staged-like diff opens the working-tree preview, no scroll following), which closes both gaps of 02-answers.md. Limit: the suite logs per step, not per case.

3. Tests only. `git diff --stat origin/main...HEAD -- src` is empty; the 8 files are requirements markers and log, test/host/diffPreview.requirements.test.ts, test/integration/diffPreviewScroll.test.ts, trusted-suite.ts, test/shared/e2eGroups.ts, test/site/e2eGroups.test.ts. (The 42d01082..HEAD range lists src/page/runtime.ts and others only because the base moved by rebase, not from this CR.)

4. PR description (`gh pr view 473`, headRefOid = 39f2419d...): sections render; Summary and Changes match the diff; no image; Deliverables "None (tests only)"; no unverified claim stated as fact, so no Known gaps needed; Internal references hold CR ids only. Unticked Review and CI green boxes are the Driver's to tick.

No visual deliverable, so no before/after evidence.

VERIFIED
