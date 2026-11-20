# Change specification: a browser test whose page setup fails ends the run instead of hanging

Origin: found in CR-351 (`font-independent-layout-tests`, PR 429, "Known gaps" of its body);
`intake/request.md` and `02-answers.md` here (short name `font-hang`, no grill question). No
tracker issue.

## Goal

When the font that the table breakout tests pin does not load, the test run fails with the
font's error message and ends. Today it hangs: `openPage` in `test/page/tableBreakout.test.ts`
starts Chromium, then `pinTestFonts` throws, and nothing closes the browser. The Chromium process
keeps the Node test process alive, so `npm run test:unit`, `just check` and `just preflight` never
end unless Node runs with `--test-force-exit` (which `scripts/node-test.mjs` does not pass).
`test/page/chartPage.ts` has the same gap in the helper that opens the chart and Mermaid test
pages, so this CR closes the browser there too (`02-answers.md`).

## Where the code is

This CR builds on CR-351, which is not on `main` yet:

- Branch below: `chantier/batch-06/cr-351-change-specification-layout-tests-that-d` (PR 429,
  itself stacked on CR-350's branch, PR 428). Head reviewed for this specification: `cbb5093b`
  ("test: draw the table breakout tests in one bundled font"). Read-only reference worktree:
  `C:\Users\gaeta\Projets\markdown-okf-schema-studio.worktrees\batch-06-CR-351`.
- CR-427's branch starts from the CR-351 branch head, and its PR targets that branch, as the
  stacked PRs guideline says (`.agents/guidelines/stacked-prs.guidelines.md`: the PR sits above
  PR 429). If PR 429 has merged by the time the Driver starts, the branch starts from `main`
  instead.

The files involved (the first two come from CR-351; `chartPage.ts` is the same on `main`):

- `test/page/pinnedFont.ts`: `pinTestFonts(page: Page): Promise<void>` reads the three KaTeX
  woff2 files from `FONTS` (`<extension root>/node_modules/katex/dist/fonts/`) with
  `fs.readFileSync`, adds them to the page with `FontFace`, and throws
  `the pinned test font did not load: <file> (<status>), ... from <folder>` when a face is not
  `loaded`. A missing file throws earlier, from `readFileSync` (`ENOENT`).
- `test/page/tableBreakout.test.ts`: `openPage(markdown, themeId)` (around line 129) writes the
  page, then `browser = await chromium.launch()` (returns `undefined` when no Chromium can start:
  the tests skip), then, with no guard, `browser.newPage`, `page.addInitScript`, `page.goto`, the
  theme variables (`page.evaluate`), `await pinTestFonts(page)` and
  `page.waitForFunction(... data-sphinx-preview-width === "auto")`, and only then returns
  `{ browser, page, close }`. The callers (tests 1 and 2 directly, tests 3 to 6 through
  `withPage`) close the browser in a `finally`, but only once `openPage` has returned: a throw
  inside `openPage` leaves the browser open.
- `test/page/chartPage.ts`: `openChartPage(markdown, files, themeId, mode?)` delegates to the
  exported `openPreviewPage(markdown, files, themeId, mode, runtime)` (runtime `"vega"` or
  `"mermaid"`). After `browser = await chromium.launch(...)` (which returns `undefined` when it
  fails), it calls `browser.newPage`, adds the `console` and `pageerror` listeners,
  `page.addInitScript`, `page.goto`, looks the theme up with `THEMES.find(...)!` and sets the theme
  variables with `page.evaluate`, then returns the `ChartPage`, all without a guard. Its callers
  are `test/page/chartCsp.test.ts` (twice, through `openChartPage`),
  `test/page/mermaidLabelFit.test.ts` (through `openPreviewPage`) and `test/probe/chartShots.ts`.

## What changes

### `test/page/tableBreakout.test.ts`: `openPage` closes Chromium when its setup fails

- Every step of `openPage` after `chromium.launch()` succeeds (from `browser.newPage` to the
  `waitForFunction` on Auto) runs inside one `try`; its `catch` closes the browser
  (`await browser.close()`) and throws the same error again, unchanged, so the test fails with the
  font's message (`the pinned test font did not load: ...`) or the `ENOENT` of a missing file.
  The pattern is the one `test/page/svgBreakout.test.ts` already uses (a `try` after the launch,
  `browser.close()` on the way out). Covering the whole setup, not only the `pinTestFonts` call,
  is the same error path: any of these steps throwing after the launch leaves the same open
  browser (for example the 30 s timeout of `waitForFunction`).
- An error raised by `browser.close()` itself in that `catch` does not hide the setup's error:
  the original error is the one thrown.
- The "no Chromium can start here" path is unchanged: a failed launch still returns `undefined`
  and the tests skip.
- The return value and the callers do not change: on success `openPage` returns the same
  `Opened`, and the callers keep closing it in their `finally`.

### A way to make the pin fail, for the regression test

- `pinTestFonts` takes the fonts folder as an optional second argument, defaulting to the
  current `FONTS`: `pinTestFonts(page: Page, fonts: string = FONTS): Promise<void>`. It reads the
  three files from that folder and names that folder in its error message, as today.
- `openPage` takes an optional third argument, an options object, for the regression test only:
  `{ fonts?: string; launched?: (browser: Browser) => void }`. `fonts` is passed to
  `pinTestFonts`; `launched` is called with the browser right after a successful launch, so the
  test can see whether the browser was closed. The six existing tests do not pass it. Names are
  the Driver's choice; the behaviour above is the requirement.

### New regression test in `test/page/tableBreakout.test.ts`

One test, named in the file's style, for example "A pinned font that does not load fails the
test and closes the browser":

1. Writes, in a temporary folder (`fs.mkdtempSync(path.join(os.tmpdir(), ...))`), three files
   with the face file names (`KaTeX_SansSerif-Regular.woff2`, `KaTeX_SansSerif-Bold.woff2`,
   `KaTeX_Typewriter-Regular.woff2`) whose content is not a font (a few bytes of text). This drives
   the real font-load error path (`FontFace.load` fails, status `error`), not a stand-in.
2. Calls `openPage` on a small document (for example `documentOf(CASES.slice(0, 1))`) and the
   `light` theme, with that folder and a `launched` callback that keeps the browser.
3. When `openPage` resolves to `undefined` (no Chromium here): `t.skip` with the same message as
   the other tests ("no Chromium can start here (run `just dev` to install it)"). When it resolves
   to an `Opened`: close it and fail (the bad font was accepted).
4. When it rejects: asserts the message matches `/the pinned test font did not load: KaTeX_/`,
   that `launched` was called, and that the kept browser is closed
   (`browser.isConnected() === false`), with a message naming what is checked.
5. In a `finally`: closes the kept browser if it is still connected (so the test itself never
   hangs the run when it is red), and removes the temporary folder.

No `@tests_req` marker: the test guards the test harness, not a product behaviour; the six tests
keep their `SwRS-MDOKFSTUDIO-LAYOUT-044` and `LAYOUT-023` markers unchanged.

### `test/page/chartPage.ts`: `openPreviewPage` closes Chromium when its setup fails

- The same pattern as `openPage`. Every step after `chromium.launch()` succeeds, from
  `browser.newPage` to building the returned `ChartPage`, runs inside one `try`. The `catch` closes
  the browser and throws the original error again, unchanged. An error from `browser.close()`
  does not hide that original error. A failed launch still returns `undefined` (callers skip).
  This covers `openChartPage`, which only delegates.
- To see the browser from a test, `openPreviewPage` takes an optional last argument
  `{ launched?: (browser: Browser) => void }`, called right after a successful launch. The current
  callers do not pass it. The name is the Driver's choice.

### New regression test for `chartPage.ts`, in `test/page/chartCsp.test.ts`

One test, for example "Opening a chart page closes the browser when its setup fails":

1. Calls `openPreviewPage(CHART_DOCUMENT, { "data/series.csv": CHART_DATA }, "no-such-theme",
   undefined, "vega", { launched })`. A theme id that is not in `THEMES` makes the setup throw
   after the launch, the `newPage` and the `goto` (reading `.variables` of `undefined`). That is a
   real failure of the existing code, so the test needs no other hook.
2. Resolves to `undefined` (no Chromium here): `t.skip` with the message the file already uses
   for that case. Resolves to a `ChartPage`: close it and fail.
3. Rejects: asserts that `launched` was called and that the kept browser is closed
   (`browser.isConnected() === false`), with a message naming what is checked.
4. In a `finally`: closes the kept browser if it is still connected, so the test never hangs the
   run when it is red.

No `@tests_req` marker (test harness); the existing markers of `chartCsp.test.ts` stay.

### Comments

- The header comment of `tableBreakout.test.ts` and the doc comment of `pinTestFonts` say, in one
  short clause each, that a face that does not load fails the test (the browser is closed), not
  how it used to behave.

### Requirements, docs, CI

- No change under `requirements/`, `src/`, `.github/` or the `justfile`; no SwRS changes (a
  test-harness fix). No entry in `requirements/tiers/log.md` (not substantive for the bundle).
- No change to the writing skill (no rendered syntax changes) and no visual change.
- Commit: type `test`, no scope (scopes are only for `feat` and `fix`), per
  `.agents/guidelines/git-commit-message.guidelines.md`; for example
  `test: end the browser tests when a test page fails to open`.

## Decisions carried from `02-answers.md`

- The request stands as written: close Chromium on the font-load error path so the run fails
  instead of hanging.
- Open question 1, decided by the Chief of Staff: `test/page/chartPage.ts` (`openChartPage`, by
  way of `openPreviewPage`) is in this CR. It gets the same try, close and rethrow pattern and its
  own regression check that the browser is closed when a failure happens after the launch.

## Out of scope

- The raw `ENOENT` of a missing font file, which comes before the custom message (a CR-351
  Inspector minor note): its message is not changed; only the browser is closed on it.
- The temporary folders that `openPage` and `openPreviewPage` create for each page are never
  removed. That is an existing leak, not a hang, and stays unchanged.
- Running the breakout tests on Linux: CR-428 (`ci-linux-table-breakout-widths`).
- Adding `--test-force-exit` or a timeout to `scripts/node-test.mjs`: the fix closes the
  resource; it does not hide a leak.

## Host matrix

The tests run only where Chromium can start; elsewhere they skip:

- Windows, local (`just check`, `just preflight`): both new tests run and must pass. This is
  where the evidence below is taken.
- Linux CI, `just ci-static` (`static` job), and Windows CI (`static-windows` job): the breakout
  tests skip ("no Chromium can start here", as CR-351's Verifier found). The new breakout test
  skips too. Whether the chart tests run there is for the Driver to record from the CI log (spec
  report of `chartCsp.test.ts`).
  CI green proves only that nothing else broke; it does not prove the fix.
- Linux and macOS, local: no machine available; UNVERIFIED, said so in the PR body.

## Evidence

The Driver records each item with the commit it was taken at.

1. Fails on the previous code (constitution, section 3): at the CR's head, with only the `catch`
   of `openPage` removed (the `browser.close()` taken out, the new options kept), the new test is
   red on the `isConnected() === false` assertion and the run still ends (the test's own
   `finally` closes the browser). Restored, it is green. Do the same for `chartPage.ts`: with
   the `catch` of `openPreviewPage` removed, the new chart test is red on `isConnected() ===
   false`, and the run ends. Restored, it is green. Record all four outputs.
2. The run ends instead of hanging: build (`just compile`), then, with `FONTS` in
   `test/page/pinnedFont.ts` temporarily pointed at a folder that does not exist (local only,
   never committed), run the file alone:
   `node --import ./scripts/register-myst-patches.mjs --test out/test/page/tableBreakout.test.js`.
   With the fix: the process exits by itself, non-zero, each test failing with the `ENOENT` or the
   font message, in well under a minute (record the time). Repeat with the folder pointed at the
   bad-bytes files of evidence item 1's kind: same outcome with
   `the pinned test font did not load`. On CR-351's head (`cbb5093b`) the same run does not exit
   (stop it after 2 minutes and record that). Revert the temporary edit; `git status` is clean
   of it.
3. The six existing breakout tests still pass in both themes with the real KaTeX fonts, and the
   existing tests of `chartCsp.test.ts` and `mermaidLabelFit.test.ts` still pass: `just check` is
   green on Windows. Check in the spec report that both new tests ran and did not skip.
4. `just preflight` passes at the head that is pushed (constitution, section 4; on Windows its
   static stage).
5. CI on the PR: the simulated jobs green (`static`, `static-windows`, `visual`, `report`,
   `checks`). The PR body says that CI skips the breakout tests, so the breakout fix is proven
   only by items 1 and 2 on Windows.
