# Verify CR-464

Head: 7aafa2bc815eebba69b49c2be9526c89ffd356b8

Verdict: VERIFIED (judged at 7aafa2bc815eebba69b49c2be9526c89ffd356b8)

Claims, each at the head above:

1. The patch is test-only and the scope is as stated. `git diff origin/main...HEAD --stat`: 4 files
   (`test/build/stressPlan.test.ts`, `test/integration/diffPreviewScroll.test.ts`,
   `test/integration/realInput/run.ts`, `test/shared/stressPlan.ts`), 98 insertions, 13 deletions. No `src/` file.
2. The D1 step now picks a new editor of the diff (not one open before the diff), scrolls with the awaited
   `revealLine` command, and its timeout message carries the window state. Read in `git show HEAD`
   (`scrollEditorTo`, `windowState`, `isDiffEditor`).
3. `diff-preview-scroll` is an on-demand stress scenario. Heavy run 44963768100 (workflow_dispatch, head 7aafa2bc,
   STUDIO_STRESS_REPEAT 60, STUDIO_STRESS_SCENARIOS diff-preview-scroll): `stress` success. The log has 60 lines
   `PASS stress n/60 diff-preview-scroll` and no FAIL. Its `visual` and `integration` jobs are success too.
   `static-windows` ran the new `CR 464` stressPlan test, which passed.
4. Heavy CI green on several consecutive runs at the head:
   - 44963768100: completed, success (stress, visual, integration, static, static-windows, report, checks success).
   - 44963770208: completed, success (same jobs success).
   - 44963750854 (pull_request): completed, success (static, static-windows, visual, viewer-graph, report, checks).
   - 44963772463 (heavy): in progress at check time, with static, static-windows, stress, visual, viewer-graph and
     integration already success; not counted as proof.
5. Gate: `work/gates/20261122-004452.log`, first line `gate CR-464 branch ... head 7aafa2bc815eebba69b49c2be9526c89ffd356b8`,
   `$ just preflight`, last line `result: pass at 7aafa2bc815eebba69b49c2be9526c89ffd356b8` (Windows: static stage).
6. PR #476 description (`gh pr view 476`): draft, base main. Summary, Changes, Impacts and Blast radius match the diff
   (4 test files, no extension change). Review box unchecked, so no "approved" claim to prove. No Known gaps claim is
   missing: no UNVERIFIED mark in it.

Limit: the root cause is judged by the evidence of repeated green runs, not by a local red-then-green (the PR states
this). Main's red run was not reproduced here.
