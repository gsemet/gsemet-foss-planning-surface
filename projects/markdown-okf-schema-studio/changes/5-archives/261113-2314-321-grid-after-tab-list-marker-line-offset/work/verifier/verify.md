# Verify CR-321 at f0151505b629ac56f2798d14b48040f737b1b9f7
- Head: 50 rows in gridCardTitleSourceLine.test.js pass; all 531 render unit tests pass (`node scripts/node-test.mjs unit "out/test/core/render/*.test.js"`).
- Base (detached origin/main 5a5f6745 + head test file): 12 fail, 38 pass. The failures are the dash-tab, star-tab, ordered-tab, dash-space-with-tab and tab-panel rows; the regression and CR-308/CR-319 rows pass.
- Heavy CI on the branch: success (given by the caller, not re-run).
Verdict: VERIFIED
