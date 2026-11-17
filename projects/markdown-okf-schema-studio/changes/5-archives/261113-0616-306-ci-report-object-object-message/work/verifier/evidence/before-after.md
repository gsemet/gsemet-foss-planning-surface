# Before / after (CR-306), head 5b45842
Run from the worktree root; test is node:test (`node --test`).
1. before-test.txt: origin/main + only the new test file: new test fails, stdout `FAILED visual: [object Object]; [object Object]`. after-test.txt: head, 10/10 pass.
   Reproduce: `node --test test/site/e2eCampaign.test.ts`.
2. after-report-line.txt: `node scripts/e2e-campaign.mjs report --visual-only` on a hand-made out/reports/e2e with {page,detail} failures prints `FAILED visual: home: blank; toc: overflow`. (Before is the `[object Object]` line in before-test.txt.)
