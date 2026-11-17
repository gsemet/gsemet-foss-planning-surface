# Diagnosis: red unit test on CR-336 branch

Verdict: the CR is not responsible. The test fails identically on origin/main (16105e0f) without the CR.

## Reproduction (single test file, the project's runner)

    node scripts/node-test.mjs unit "out/test/page/tableBreakout.test.js"

(`node --test` alone is wrong: without `--import ./scripts/register-myst-patches.mjs` five other tests of the file fail with
"Cannot find module .../markdown-it/lib/common/utils.js". Use node-test.mjs.)

## Result, 3 runs each, identical every time

- CR worktree (5f828f02): pass 5, fail 1
- Detached worktree of origin/main (16105e0f), fresh `npm ci` + `tsc -p .`: pass 5, fail 1

Both fail on:

    test/page/tableBreakout.test.ts:398 "Auto measures a table again on a real resize while a cell is edited"
    AssertionError: light: the breakout follows the pane (705 then 727 px)

Deterministic (same 705/727 values every run). It is a Playwright Chromium layout test (viewport 760 wide, `layoutPass`
dispatches a resize and waits two animation frames): after narrowing the viewport the table got wider (705 -> 727), the
assertion `narrower.width < open.width` fails. The test and its code (`293366d0`, last touched in main before the CR) are not
touched by the CR; it is a pre-existing failure on main in this machine's environment (Windows, local Chromium). Whether it
is a product bug in the breakout re-measure or a Windows/Chromium timing or font issue is not determined here; it needs its own CR.

## Does the alias change resolution?

CR diff of package-lock.json: +9 lines, only the new `node_modules/@types/vscode-min` entry (alias of @types/vscode 1.95.0)
and its line in the root devDependencies.

`npm ls --all --parseable` on both trees (logs: work/debugger/ls-main.log 569 lines, work/debugger/ls-cr.log 570 lines):

    Compare-Object main cr  ->  only  ROOT\node_modules\@types\vscode-min  (=> CR side)

No other package is added, removed or moved. markdown-it, playwright-core and the rest resolve the same.

## Place to fix

Not in CR-336. File the failing test as a separate bug (tableBreakout re-measure on resize while a cell is edited) and
either let the CR's gate record it as a known red on main, or wait for that fix.

Scratch worktree used: C:/Users/gaeta/AppData/Local/Temp/claude/scratch-main (to remove by the caller if still present).
