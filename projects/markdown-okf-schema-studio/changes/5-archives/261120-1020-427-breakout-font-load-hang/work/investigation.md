# CR-427 investigation: close Chromium when a test page fails to open

Worktree `C:\Users\gaeta\Projets\markdown-okf-schema-studio.worktrees\batch-06-CR-427`, branch
`chantier/batch-06/cr-427-tablebreakout-tests-a-pinned-font-that-f`, head = base `82c11a47`
(origin/main). Read only; nothing was built or run in the worktree.

## Base check: the spec's head and this head are the same tree

- `git rev-parse cbb5093b^{tree} 82c11a47^{tree}` gives `1501f35d…` twice: main's `82c11a47` is
  CR-351's reviewed head `cbb5093b` rebased onto main, with an identical tree. Every line reference
  in "Where the code is" holds at this head, and "on CR-351's head (`cbb5093b`)" in evidence item 2
  can be read as "at the base `82c11a47`, before the fix" (same files).
- The spec's "branch starts from main" case applies; the PR targets `main`, not stacked (the
  stacked-PR paragraph of the spec is moot).
- The worktree has no `node_modules/` and no `out/`: run `just dev` first (AGENTS.md "Setup",
  local-worktree guideline). Playwright's browser cache exists (`%LOCALAPPDATA%\ms-playwright`).

## Spec claims, checked against the head

| Claim | Verdict |
| --- | --- |
| `pinnedFont.ts`: `pinTestFonts(page: Page): Promise<void>` (line 29), `FONTS` = `<root>/node_modules/katex/dist/fonts` (line 15, module-private, not exported), `readFileSync` per face (line 30), error `the pinned test font did not load: <file> (<status>), ... from ${FONTS}` (line 55) | Confirmed. Only caller: `tableBreakout.test.ts:178`. |
| `tableBreakout.test.ts`: `openPage(markdown, themeId)` "around line 129" | Confirmed: line 129–181. Launch in `try/catch → undefined` at 161–166; unguarded `newPage` 167, `addInitScript` 168, `goto` 173, `THEMES.find(...)!` 174, `evaluate` 175, `pinTestFonts` 178, `waitForFunction` 179, return 180. |
| Callers close only after `openPage` returns | Confirmed: tests 1 (l. 241) and 2 (l. 281) call it directly inside their theme loop, before their `try/finally`; tests 3–6 go through `withPage` (l. 365–382), same shape. |
| Header comment | Lines 1–9; line 7–8 name `pinnedFont.ts` and the skip. `pinnedFont.ts` doc comment lines 1–8 ("A face that does not load is an error, never a silent fallback…"), `pinTestFonts` JSDoc line 28. |
| `chartPage.ts`: `openChartPage(markdown, files, themeId, mode?)` delegates to exported `openPreviewPage(markdown, files, themeId, mode, runtime)` | Confirmed: l. 86–88 and 95–178. Launch in `try/catch → undefined` 147–152; unguarded `newPage` 153, listeners 155–158, `addInitScript` 159, `goto` 165, `THEMES.find(...)!` 166, `evaluate` 167–170, return object 171–177. |
| `chartPage.ts` "is the same on main" | Confirmed (identical tree). |
| Callers: `chartCsp.test.ts` (twice via `openChartPage`), `mermaidLabelFit.test.ts` (via `openPreviewPage`), `test/probe/chartShots.ts` | Confirmed: `chartCsp.test.ts:17,64`; `mermaidLabelFit.test.ts:42` (5 positional args, `undefined` mode, `"mermaid"`); `chartShots.ts:13` via `openChartPage`. No other caller in `src/`, `test/` or `scripts/`. |
| `chartCsp.test.ts` skip message, `CHART_DOCUMENT`/`CHART_DATA` | Confirmed: skip message is exactly `no Chromium can start here (run \`just dev\` to install it)` (l. 19, 66), same text as the breakout tests. `CHART_DOCUMENT`, `CHART_DATA` exported from `chartPage.ts` l. 23, 74; `chartCsp.test.ts` imports `CHART_DATA, CHART_DOCUMENT, openChartPage` (l. 10): add `openPreviewPage` (and `type Browser` from `playwright-core`) to its imports. |
| `"no-such-theme"` throws after launch, `newPage` and `goto` | Confirmed: `THEMES.find(...)!` returns `undefined` at l. 166, and `theme.variables` (l. 170, argument of `page.evaluate`) throws a Node `TypeError: Cannot read properties of undefined (reading 'variables')` before the evaluate runs. Real failure, no hook needed. |
| `svgBreakout.test.ts` pattern (try after the launch, close on the way out) | Confirmed: l. 49–55 launch/skip, l. 56–76 `try { … } finally { await browser.close(); }`. Note: it closes in a `finally` (the browser is owned by the test); `openPage`/`openPreviewPage` must close only on error (`catch`), since on success they hand the browser to the caller. |
| `scripts/node-test.mjs` passes no `--test-force-exit` | Confirmed (l. 16–29). |

Nothing in the spec needs correcting beyond the base (main, not the CR-351 branch).

## Smallest change

1. `test/page/pinnedFont.ts`: `pinTestFonts(page: Page, fonts: string = FONTS)`; read
   `path.join(fonts, face.file)`; error message `from ${fonts}`. One clause in the doc comment (a face
   that does not load fails the test, and the test page closes its browser).
2. `test/page/tableBreakout.test.ts`:
   - `openPage(markdown, themeId, options: { fonts?: string; launched?: (browser: Browser) => void } = {})`.
   - After the launch block: `options.launched?.(browser);` then `try { …l. 167–179…, pinTestFonts(page, options.fonts) } catch (error) { await browser.close().catch(() => undefined); throw error; }`, return after the `try` (or inside it). `browser.close().catch(() => undefined)` keeps the original error.
   - New test (spec steps 1–5), placed at the end of the file; it needs `documentOf`, `CASES` (both
     defined above), `fs`, `os`, `path` (already imported). The bad files: `fs.writeFileSync(path.join(dir, name), "not a font")` for the three names (the names are the `FACES` files; they are not exported from `pinnedFont.ts`, write them as literals or export `FACES`' names — literals avoid a new export).
   - Header comment clause.
3. `test/page/chartPage.ts`: `openPreviewPage(..., runtime, options: { launched?: (browser: Browser) => void } = {})`; `options.launched?.(browser)` after the launch; `try { …l. 153–177… } catch (error) { await browser.close().catch(() => undefined); throw error; }`. `openChartPage` unchanged (it never passes the option).
4. `test/page/chartCsp.test.ts`: the new test (spec steps 1–4), importing `openPreviewPage` and `type Browser`.

Estimated sizes after the change: `tableBreakout.test.ts` 480 → about 530, `chartPage.ts` 181 →
about 190, `chartCsp.test.ts` 89 → about 120, `pinnedFont.ts` 56 → 57.

## Risks

- **File-size ratchet** (`scripts/check-file-sizes.mjs`, 1 500 lines in `test/`): none of the four
  files is near the limit or on `scripts/file-size-baseline.json`; ~530 lines max. No risk.
- **Unused exports** (`scripts/check-unused-exports.mjs`): it checks only exports of `src/`; test
  files are consumers, never subjects. The new optional parameters and any new test export cannot
  trip it. There is **no knip** in this project; `just check`'s equivalents are `check-exports` and
  `check-boundaries`.
- **dependency-cruiser** (`check-boundaries`): runs over `src/` only; `test/` imports are not
  checked. No risk. `check-min-vscode` includes only `src/`.
- **TypeScript** (`strict`, no `noUnusedLocals`/`noUnusedParameters`): `let browser: Browser`
  assigned inside the launch `try` is already definitely-assigned after the `catch { return }`; the
  `catch (error)` variable is `unknown` and `throw error` rethrows it unchanged. Keep the catch
  binding named (`catch (error)`), not `catch {}`.
- **Markers** (`check-markers`): the new tests have no `@tests_req` (spec); rule 2 (≤ 3 IDs per
  block) is untouched as long as the new tests are not placed directly under an existing marker
  block without a code line between (put each new test after the last test's closing `});`).
  `chartCsp.test.ts`'s first test already carries 4 IDs in one block (l. 12–15); do not touch it.
- **The regression test must never hang itself**: its `finally` closes the kept browser when still
  connected — that is what lets evidence item 1's red run end.
- **`launched` before or inside the `try`**: call it before the `try`, right after the launch, so a
  throw in the callback (it should not) is not a concern; either placement satisfies the spec.
- **Order of `browser.close()` vs `isConnected()`**: `isConnected()` turns `false` once `close()`
  resolves; the `catch` awaits `close()` before rethrowing, so the assertion is deterministic.
- **`chartCsp` new test cost**: `openPreviewPage` bundles the Vega runtime with esbuild before the
  launch (a few seconds); acceptable, and in CI it runs that bundle even when Chromium cannot start
  (as the two existing tests already do).
- **Same leak elsewhere, out of scope**: `mermaidLabelFit.test.ts:47` creates a temp folder before
  its `try` (a leak, not a hang); `svgBreakout.test.ts` is already correct.
- **Batch conflict**: CR-428 (`ci-linux-table-breakout-widths`, pending in batch-06) also touches
  `tableBreakout.test.ts`; whichever lands second rebases. No action for CR-427.
- No value other code measures from changes (no product or layout change); nothing to search for.

## Questions for the user

None.

## Evidence plan

Kind of change: test harness only, no visible change; the proof is command output and timing. Run
everything from the worktree in PowerShell after `just dev`. Raw logs go to `work/gates/*.log`;
the recorded excerpts and timings, each with its commit, go to `evidence/`. The helper
`work/investigator/timed-run.mjs` (checked: `node --check`, and a 3 s smoke run that it ended by
PID) runs a node command, prints the elapsed time and whether it exited by itself, and after N
seconds ends the run and its whole process tree **by its own PID** (`taskkill /PID <pid> /T /F`),
never by name. Below, `$TR` stands for
`C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/427-breakout-font-load-hang/work/investigator/timed-run.mjs`
(write the full path in each command; no variable assignment). Create the bad-font folder once
outside the repo, e.g. `C:\Users\gaeta\AppData\Local\Temp\cr427-bad-fonts\` holding
`KaTeX_SansSerif-Regular.woff2`, `KaTeX_SansSerif-Bold.woff2`, `KaTeX_Typewriter-Regular.woff2`
with the text `not a font` (the Write tool, not a shell redirect).

Order matters: take item 2's "before" runs **first**, at the base, before any code change.

2a. Before the fix (base `82c11a47`, tree identical to `cbb5093b`):
   - Temporarily set `FONTS` in `test/page/pinnedFont.ts` to `"C:/does-not-exist/fonts"`; `just compile`;
     `node $TR 120 --import ./scripts/register-myst-patches.mjs --test out/test/page/tableBreakout.test.js`
     → expected `[timed-run] HUNG: ended by timed-run after 120.x s`, with the tests reported
     failing on `ENOENT` before the hang. Log: `work/gates/hang-before-enoent.log`.
   - Same with `FONTS` = `"C:/Users/gaeta/AppData/Local/Temp/cr427-bad-fonts"` → HUNG, failures
     name `the pinned test font did not load`. Log: `work/gates/hang-before-badfont.log`.
   - Revert the edit (`git checkout -- test/page/pinnedFont.ts`, that file only); `git status` clean.
2b. After the fix (CR head): the same two temporary edits, `just compile`, same command with a 120 s
   limit → expected `exited by itself after <~10–40> s, code 1`; six breakout tests fail (ENOENT /
   font message), the new regression test passes (it brings its own folder). Logs
   `work/gates/nohang-after-enoent.log`, `work/gates/nohang-after-badfont.log`. Revert; `git status`
   clean of `pinnedFont.ts`.
1. Fails on the previous code (at the CR head, then restored):
   - In `openPage`'s `catch`, delete only the `await browser.close()…` line (keep `throw error` and
     the options); `just compile`;
     `node $TR 180 --import ./scripts/register-myst-patches.mjs --test --test-name-pattern="pinned font" out/test/page/tableBreakout.test.js`
     → red on the `isConnected() === false` assertion, and `exited by itself`. Restore, compile,
     rerun → green.
   - In `openPreviewPage`'s `catch`, the same deletion; compile;
     `node $TR 180 --import ./scripts/register-myst-patches.mjs --test --test-name-pattern="closes the browser" out/test/page/chartCsp.test.js`
     → red on `isConnected() === false`, exits by itself. Restore, compile, rerun → green.
     (Adjust `--test-name-pattern` to the final test names.) Four outputs, four logs in
     `work/gates/`; `git diff` empty for both files afterwards.
3. `just check` green on Windows (`work/gates/check.log`); in its spec report, both new tests are
   listed with ✔ and not `# SKIP`, and the six breakout tests plus the chartCsp and
   mermaidLabelFit tests pass. `just check` itself hangs only if the fix is wrong; if in doubt, run
   the unit stage alone under the helper first, which ends a hung run by PID:
   `node $TR 900 scripts/node-test.mjs unit "out/test/{build,core,host,host-memory,host-vscode,node-services,page,session,site}/**/*.test.js"`.
4. `just preflight` at the pushed head (Windows: static stage), log `work/gates/preflight.log`.
5. CI on the PR (`gh pr checks <n>`): `static`, `static-windows`, `visual`, `report`, `checks`
   green. From the `static`/`static-windows` logs, record whether the two new tests ran or skipped
   (expected: breakout skips; chart test: record what the log shows). PR body: CI skips the
   breakout tests, so the breakout fix is proven by items 1 and 2 on Windows only; Linux/macOS
   local UNVERIFIED.

Cannot be shown: the fix on Linux or macOS locally (no machine); the breakout fix in CI (Chromium
does not start there).
