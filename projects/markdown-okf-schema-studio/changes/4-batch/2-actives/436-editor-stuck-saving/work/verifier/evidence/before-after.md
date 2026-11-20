# Before and after (CR-436)

Before = base 7c88b89c3d2b062ef574b4b21a69cec777ade95d (detached worktree, new tests copied in; removed at the end).
After = head 9091f929c83ae559fb6b8c4731aba7c29d58f026.

| Pair | Shows | Reproduce |
| --- | --- | --- |
| before-unit.log / after-unit.log | the three new test files: before 16 of 20 fail (matchLineEndings module missing), after all 70 tests of the six related files pass | `node scripts/node-test.mjs unit out/test/page/runtimeBlockEditorLineEndings.test.js out/test/host/editLineEndings.test.js out/test/core/edits/matchLineEndings.test.js` after `npm run compile` |
| before-integration.log / after-integration.log | real window: before, "Timed out waiting for the editor to close (CRLF file, paragraph, left by Done)", exit 1; after, exit 0 | `STUDIO_REAL_INPUT_SCENARIO=line-ending-leave npm run test:integration -- --trusted-only` |

No screenshots (not a visual fix).
