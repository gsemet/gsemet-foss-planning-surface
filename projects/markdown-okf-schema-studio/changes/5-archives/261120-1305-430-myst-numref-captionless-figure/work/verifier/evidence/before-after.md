# CR-430 before / after

Before: base 9f17229b0332fe6bee07726f3584aca0e55d792a (CR-428 branch, detached worktree, removed).
After: pushed head 2bea4c6a035e124bc7a0c5889af41db485e88d92 (same detached worktree, checked out at the head).

No visible change (test and requirement text only), so the pair is text, no screenshot.

| Pair | Before | After | Shows |
| --- | --- | --- | --- |
| MyST feature unit tests | before-9f17229.log | after-2bea4c6.log | Before: only "references to captionless figures and tables stay readable", tests 45, pass 45. After: that test and "a numref to a captionless figure or table shows its number", tests 46, pass 46. |

Reproduce, in a checkout of each SHA with node_modules installed:

```sh
node node_modules/typescript/bin/tsc -p .
node scripts/node-test.mjs unit out/test/core/render/mystFeatures.test.js
```
