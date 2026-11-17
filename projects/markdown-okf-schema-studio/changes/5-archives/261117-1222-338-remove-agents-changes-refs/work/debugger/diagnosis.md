# Diagnosis: tableBreakout "Auto measures a table again on a real resize while a cell is edited" (Windows)

Reproduction (in the CR worktree, out/ compiled at f6482d0):
node --import ./scripts/register-myst-patches.mjs --test --test-name-pattern="Auto measures a table again" out/test/page/tableBreakout.test.js
Result: 3 of 3 runs fail: "light: the breakout follows the pane (705 then 727 px)", actual false, expected true.

Evidence the diff is not the cause:
- git diff origin/main...HEAD -- src test shows only: a removed Python test (test/build/test_generate_orchestrator.py)
  and two comment-only edits (test/shared/captureRegistry.ts, test/shared/e2eGroups.ts). No file under src/ or test/page/.
- The failing test's require closure (out/test/page/tableBreakout.test.js: src/core/protocol/bootContext,
  src/core/render/renderPipeline, src/session/webview, test/shared/fakeAssets, test/visual/themes, ./runtimeHarness)
  includes neither changed test file; git diff origin/main --stat -- src test/page test/visual test/shared/fakeAssets.ts is empty.
  So the code the test runs is byte-identical to origin/main (merge-base 68f36c3).
Not done: a run on a detached origin/main worktree. The debugger card forbids creating a worktree and the
writes line names only the CR worktree and CR folder. The proof is by identity of the executed code, not by a base run.
Place to fix: not in this CR. A Windows-only layout/timing flake or defect in the page test or breakout resize code
(test/page/tableBreakout.test.ts, the "real resize" step); belongs to its own CR (CR-339 "On Windows the unit test Auto measures a ...").
