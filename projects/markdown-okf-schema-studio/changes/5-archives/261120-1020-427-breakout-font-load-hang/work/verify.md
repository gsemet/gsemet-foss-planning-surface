# CR-427 verification

Head: ebfb7f28603a2688c246349bfc4706b281210993

Branch `chantier/batch-06/cr-427-tablebreakout-tests-a-pinned-font-that-f`, base origin/main
`82c11a472250b6b808476ec797c2106481ddbd15`, PR 433 (draft, base main). First verification. Windows 11,
local. Every run below is from the CR worktree at ebfb7f2 (`git rev-parse HEAD` =
ebfb7f28603a2688c246349bfc4706b281210993), after `just compile`, through
`node <work>/investigator/timed-run.mjs <limit> ...` (ends a hung run by its own PID only). Raw logs:
`work/verifier/logs/`. `git status --short` was empty after every temporary edit was reverted (last
check after the final restore: empty output).

## Code against the specification (ebfb7f2)

`git diff --stat 82c11a47 HEAD`: 4 files, `test/page/{chartCsp.test.ts,chartPage.ts,pinnedFont.ts,tableBreakout.test.ts}`,
127 insertions, 45 deletions; nothing under `src/`, `requirements/`, `.github/` or the justfile. Read
against the spec: `openPage` and `openPreviewPage` call `options.launched?.(browser)` after a
successful launch and wrap every later step in one `try` whose `catch` runs
`await browser.close().catch(() => undefined); throw error;` (original error kept, close error
swallowed); the failed-launch path still returns `undefined`; `pinTestFonts(page, fonts = FONTS)`
reads from and names `fonts`; the two regression tests follow spec steps 1-5 and 1-4 (skip message
identical, `finally` closes a still-connected browser, temp folder removed); no `@tests_req` added;
header and doc comments carry the one clause. VERIFIED.

## Evidence item 1: fails on the previous code (ebfb7f2, with temporary edits)

- 1a. Line `await browser.close().catch(() => undefined);` deleted from `openPage`'s catch (sed on
  line 192), `just compile`, then
  `node <TR> 180 --import ./scripts/register-myst-patches.mjs --test --test-name-pattern="pinned font" out/test/page/tableBreakout.test.js`
  (log `1a-breakout-red.log`): `✖ A pinned font that does not load fails the test and closes the browser`,
  `AssertionError [ERR_ASSERTION]: openPage closed the browser when the font did not load / true !== false`,
  `[timed-run] exited by itself after 1.5 s, code 1`. Red, and the run ends.
- 1b. `git checkout -- test/page/tableBreakout.test.ts`, compile, same command (`1b-breakout-green.log`):
  `✔ ... (952.6804ms)`, `pass 1 fail 0 skipped 0`, `exited by itself after 1.5 s, code 0`.
- 1c. Same line deleted from `openPreviewPage`'s catch (line 185 of `chartPage.ts`), compile,
  `node <TR> 180 --import ./scripts/register-myst-patches.mjs --test --test-name-pattern="closes the browser" out/test/page/chartCsp.test.js`
  (`1c-chart-red.log`): `✖ Opening a chart page closes the browser when its setup fails`,
  `AssertionError [ERR_ASSERTION]: openPreviewPage closed the browser when its setup failed / true !== false`,
  `exited by itself after 1.4 s, code 1`.
- 1d. `git checkout -- test/page/chartPage.ts`, compile, same command (`1d-chart-green.log`):
  `✔ ...`, `pass 1 fail 0 skipped 0`, `exited by itself after 1.4 s, code 0`.

VERIFIED.

## Evidence item 2: the run ends instead of hanging

- After (ebfb7f2), `FONTS` in `test/page/pinnedFont.ts` line 15 set to `"C:/does-not-exist/fonts"`,
  compile, `node <TR> 120 --import ./scripts/register-myst-patches.mjs --test out/test/page/tableBreakout.test.js`
  (`2b-after-missing.log`): `tests 8, pass 1, fail 7`; the 7 breakout tests fail with
  `Error: ENOENT: no such file or directory, open 'C:\does-not-exist\fonts\KaTeX_SansSerif-Regular.woff2'`;
  the regression test passes; `[timed-run] exited by itself after 3.2 s, code 1`.
- After (ebfb7f2), `FONTS` set to a scratch folder of three `not a font` files named as the KaTeX
  faces (`2b-after-badbytes.log`): `tests 8, pass 1, fail 7`; failures
  `Error: the pinned test font did not load: KaTeX_SansSerif-Regular.woff2 (error), KaTeX_SansSerif-Bold.woff2 (error), KaTeX_Typewriter-Regular.woff2 (error) from <folder>`;
  `exited by itself after 3.5 s, code 1`.
- Reverted: `git checkout -- test/page/pinnedFont.ts`; `git status --short`: empty.
- Before (82c11a47): carried from 82c11a4: the Coder's round-1 runs at the base, same command,
  `work/evidence-r1/2a-base-82c11a47-missing-folder.log` (`[timed-run] HUNG: ended by timed-run after 120.7 s`)
  and `2a-base-82c11a47-bad-bytes.log` (`HUNG ... after 120.1 s`). Not taken again: the detached
  base worktree under `work/scratch` failed on path length
  (`error: unable to create file .agents/skills/markdown-studio-exploratory-qa-claude/scenarios/ux-38-invalid-field-does-not-block-others.json: Filename too long`,
  `fatal: Could not reset index file to revision 'HEAD'.`), a stop under the Verifier card. The
  base files are what item 1a/1c reproduce at the head: without the close the browser stays
  connected after the throw, which is what keeps Node alive.

VERIFIED (after at ebfb7f2; before carried from 82c11a4 as above). Pairs: `work/verifier/evidence/before-after.md`.

## Evidence item 3: existing tests still pass, new tests run (ebfb7f2)

- `node <TR> 300 --import ./scripts/register-myst-patches.mjs --test out/test/page/tableBreakout.test.js out/test/page/chartCsp.test.js out/test/page/mermaidLabelFit.test.js`
  with the real fonts (`3-head-files.log`): `tests 12, pass 12, fail 0, skipped 0`, all 7 breakout
  tests, the 2 existing chartCsp tests, the Mermaid label test and both new tests `✔`;
  `exited by itself after 18.3 s, code 0`.
- `just check` at ebfb7f2: not run again by the Verifier; cited from the Driver's
  `work/fast-check-ebfb7f2.log` and covered by the long gate below (which includes `ci-static`).

VERIFIED.

## Evidence item 4: long gate (ebfb7f2)

`work/gates/20261120-103743.log`, first line:
`gate CR-427 branch chantier/batch-06/cr-427-tablebreakout-tests-a-pinned-font-that-f head ebfb7f28603a2688c246349bfc4706b281210993`;
last line `result: pass at ebfb7f28603a2688c246349bfc4706b281210993` (`ci-static: passed`; visual,
integration, report and gallery stages skipped on Windows, CI runs them). Driver log:
`gate result=pass head=ebfb7f28603a2688c246349bfc4706b281210993 command=just preflight`. VERIFIED.

## Evidence item 5 and Host matrix: CI (ebfb7f2)

- `gh pr checks 433`: `checks`, `report`, `static`, `static-windows`, `visual` pass; gallery,
  integration, pages, release, release-check, stress, tag-release, toc-loop skipping (PR run).
- `gh run view 44712984273 --job 136209117290 --log` (static, Linux) and `--job 136209116930`
  (static-windows); both logs name `ebfb7f28603a2688c246349bfc4706b281210993`. In **both** jobs every
  browser test skips with `# no Chromium can start here (run `just dev` to install it)`: the breakout
  tests and the new breakout test, **and** the chart tests: `﹣ a Vega-Lite and a Vega chart ...`,
  `﹣ a theme change draws the charts again ...`, `﹣ Opening a chart page closes the browser when its setup fails`,
  `﹣ every Mermaid label fits its box ...`. So CI exercises neither fix; both are proven by items 1
  and 2 (and 3) on Windows only.

VERIFIED (CI green). Linux and macOS local: no machine, UNVERIFIED (the body says so).

## PR description (posted body, `gh pr view 433 --json title,body`, at ebfb7f2)

- Title `test: end the browser tests when a test page fails to open`: Conventional Commit, says what
  changes. Renders (sections, code fence, table, checklist). No images. No internal ids in the text;
  `#429` only under Internal references. Summary, Deliverables (code sketch matches the
  `tableBreakout.test.ts` shape) and Changes match the 4-file diff, nothing missing or extra.
  Impacts: "No visual change: test harness only". OK.
- Review box `Review: approved at ebfb7f2`: `$CHANTIER log 427` has
  `r1 approved at 82c11a47..., committed as ebfb7f28603a2688c246349bfc4706b281210993`. Proven.
- Test plan boxes "New or changed tests ... at ebfb7f2" and "Local gates ... at ebfb7f2": proven by
  items 1, 3, 4 above.
- `CI green` box is unchecked in the posted body although CI is green; the local `work/pr-body.md`
  has it checked with the job list and is not posted (diff of posted vs local: only that box and a
  trailing blank line). Not a failure by itself; post it.
- **FAIL: the before/after table names no SHA.** The rows "still running after 120 s, then stopped"
  and "exits by itself in about 3 s" are proofs with no commit: the before was taken at 82c11a4 (by
  the round's Coder, carried) and the after at ebfb7f2. Each proof in the description must name its
  SHA. Fix: say, under or in the table, before at `82c11a4` (main, before this change), after at
  `ebfb7f2`.
- **FAIL: Known gaps understates what CI skips.** It says CI skips the table breakout tests "so the
  breakout fix is proven only by the local runs", which leaves the chart-page fix looking covered by
  CI; the CI logs above show the chart tests, including the new one, skip too in `static` and
  `static-windows`. Fix: one bullet saying CI starts no Chromium, so all browser tests (breakout and
  chart/Mermaid page tests) skip there and both fixes are proven only by the local Windows runs.

## Round 2: PR description judged again (same head)

Head: ebfb7f28603a2688c246349bfc4706b281210993. `gh pr view 433 --repo gsemet/markdown-okf-schema-studio --json title,body,headRefOid`:
`headRefOid` = ebfb7f28603a2688c246349bfc4706b281210993 (no move). Code, tests and evidence items 1-5
above: carried from ebfb7f2 (same head, nothing touched).

- Before/after table: header `Before (82c11a4)` / `After (ebfb7f2)`; the SHAs match item 2 (before
  carried from 82c11a4, after at ebfb7f2). FIXED.
- Known gaps: first bullet now says CI runs neither the breakout tests nor the chart page tests, the
  two new tests included, so both fixes are proven only by local Windows runs; matches the CI logs in
  item 5 (chart tests skip in `static` and `static-windows`). Linux/macOS UNVERIFIED bullet kept. FIXED.
- `CI green` box is checked, jobs named, VS Code note; matches `gh pr checks` in item 5. FIXED.
- Renders (sections, code fence, table, checklist); no images; no role names; `#429` only under
  Internal references; Summary, Deliverables, Changes match the 4-file diff; Review box proven by the
  `r1 approved ... committed as ebfb7f28...` log note (above); no STALE mark.

PR description: VERIFIED at ebfb7f28603a2688c246349bfc4706b281210993.

## Verdict

Code, tests, evidence items 1-5 and PR description: VERIFIED at ebfb7f28603a2688c246349bfc4706b281210993.

VERIFIED
