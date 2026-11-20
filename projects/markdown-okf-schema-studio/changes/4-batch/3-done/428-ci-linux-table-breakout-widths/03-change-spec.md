# Change specification: run the table breakout width tests on Linux in CI

Origin: `intake/request.md` (follow-up filed by CR-351, PR 429, "Known gaps"); owner decisions in
`02-answers.md` (2026-11-20). No tracker issue.

## Goal

CR-351 (PR 429) makes `test/page/tableBreakout.test.ts` draw its tables in pinned KaTeX fonts, so
the widths and the twelve owner-reviewed verdicts should be the same on every machine. Its
specification asks for Linux widths within 1 px of the Windows ones. Today no CI job proves that:
the Linux and Windows `static` jobs run the test through `just check`, but no Chromium is installed
there, so all its tests skip with "no Chromium can start here". The widths were measured on Windows
only.

After this CR, the existing Linux `visual` CI job, which has Chromium, runs the table breakout
tests on every pull request and every push to `main`. A missing Chromium fails that job instead of
skipping the tests. The Linux widths are printed in the job's log and recorded in the PR body next
to the Windows ones.

## Base

The CR edits the test that CR-351 rewrote (`pinTestFonts`, the pinned-font comments, case 11's new
text). Batch-06 is a series of PRs, one after the other: this CR's branch sits on top of CR-427's
branch (font-load hang fix), which sits on CR-351's branch. If PR 429 is not merged when the Driver
starts, the branch still contains CR-351's commit `cbb5093b` ("test: draw the table breakout tests
in one bundled font") through that chain. The Driver checks it is there
(`git merge-base --is-ancestor cbb5093b HEAD`, or the same patch after a rebase) before any
measurement.

## Decisions carried from `02-answers.md`

1. **Where:** in the existing Linux `visual` CI job (Chromium installed by `just dev-ci visual`).
   No new job and no xvfb job. (Owner: "Travail visuel".)
2. **Stop rule:** if a Linux width differs from the Windows width by more than 1 px, or one of the
   twelve owner verdicts changes on Linux, the Driver stops and asks the owner, giving the widths.
   It does not change a verdict, a case, the column, the pane or a threshold to make the job pass.
   (Owner: "S'arrêter et demander".)
3. **Record of the widths:** the widths stay printed on every run, through `t.diagnostic` in the
   committed test, and the PR body keeps the Windows/Linux table. (Chief of Staff, under the
   owner's standing autonomy grant.)

## Environment of the job

- Job `visual` of `.github/workflows/ci.yml`: `ubuntu-latest`, timeout 15 minutes. It runs on every
  pull request and on every push to `main`, and is part of the required `checks` job (through
  `report`). Steps: checkout with LFS, Node.js from `.nvmrc`, uv, just 1.58.0, the apt archive
  cache, `just dev-ci visual`, `just ci-visual`, upload of `out/reports/` as
  `e2e-visual-attempt-<n>`.
- `just dev-ci visual` on Linux runs `npm ci` (which installs `katex` in `node_modules`, the source
  of the pinned fonts, and `playwright-core` 1.64.1), `uv sync`, then installs Chromium with
  `playwright install chromium` (Python Playwright 1.64.1 from `uv.lock`: the same version as
  `playwright-core`, so the same browser build, which `chromium.launch()` in the Node test finds in
  the shared Playwright cache). Its system libraries and fonts come from the cached apt archives
  (fast path) or `playwright install --with-deps chromium` (full path). It ends by launching
  Chromium once from Python.
- What the job lacks compared with a developer's Windows machine: Segoe UI, Consolas and the other
  Windows fonts (the pinned KaTeX fonts replace them; glyphs they lack, such as `✓` in the tick
  matrix, fall back to the runner's fonts, for example DejaVu or Noto); a display (headless
  Chromium does not need one); a compiled `out/` at the start (`npm run test:visual` compiles it
  through `visual:render`).
- What only the first CI run can prove: that `playwright-core` launches the Chromium installed by
  the Python Playwright on the runner; that the KaTeX fonts load there; the Linux widths
  themselves; that the job stays well inside its 15 minutes (the breakout tests take about 10 s on
  Windows). The PR's own `visual` job is that first run: no heavy dispatch is needed.

## What changes

### `test/page/tableBreakout.test.ts`

- **Fail instead of skip when Chromium is required.** When the environment variable
  `STUDIO_REQUIRE_CHROMIUM` is `1`, a Chromium that cannot start fails the test, with the launch
  error's message, instead of calling `t.skip("no Chromium can start here ...")`. This covers the
  three places that skip today (test 1, test 2 and the shared helper used by the edit tests).
  `openPage` keeps the launch error instead of dropping it in its `catch`, so the failure can name
  it. Without the variable (every `just check`, the `static` jobs, a developer machine without
  Chromium), the tests still skip as today.
- **Print the measured widths.** Each test that measures a width the stop rule compares reports it
  with `t.diagnostic(...)` (Node test runner diagnostics: printed by the spec reporter and kept in
  the JUnit report), one line per measure, with the theme. The values printed:
  - test 1: the twelve case widths and their verdicts, for example
    `light cases 688s 688s 688s 688s 1068W 735W 748W 338s 537s 719W 894W 824W` (the same format as
    CR-351's measurements: `W` breaks out of the 688 px column, `s` stays in it);
  - test 2: the three widths of the cells that cannot shrink;
  - test 5 (real resize while a cell is edited): the tick matrix's width with the editor open
    (`open.width`) and after the resize to 600 px (`narrower.width`).
  No assertion, number, verdict, case, threshold, column or pane changes. The `@tests_req` markers
  stay where they are.
- The header comment says that the `visual` CI job runs these tests on Linux with
  `STUDIO_REQUIRE_CHROMIUM=1`. Test 5's comment, which gives the tick matrix's natural width (719 px
  in the pinned fonts), says it was measured on Windows and on Linux, with the Linux value when it
  differs by 1 px or less.

### `package.json`

- New script `test:breakout`:
  `node scripts/node-test.mjs breakout out/test/page/tableBreakout.test.js`. The spec report goes to
  stdout and the JUnit report to `out/reports/breakout/tests-breakout.xml`. The `visual` job
  already uploads all of `out/reports/`.

### `justfile`, recipe `ci-visual`

- After `npm run test:visual` (which compiles `out/`), the recipe runs
  `STUDIO_REQUIRE_CHROMIUM=1 {{ npm }} run test:breakout`. It runs even when `test:visual` failed,
  so one run reports both. The recipe ends with `ci-visual: passed` only when both pass, otherwise
  `ci-visual: FAILED` and exit 1 (CI guideline rule 8).
- The comment above the recipe says it also runs the table breakout width tests in Chromium, with
  their report under `out/reports/breakout/`.
- `.github/workflows/ci.yml` does not change: the job still calls only `just dev-ci visual` and
  `just ci-visual` (CI guideline rules 1 and 3). `just preflight` gets the step through `ci-visual`
  on Linux and macOS (rule 7); on Windows its static stage skips `ci-visual` as before.

### `test/build/test_workflows.py`

- New test: it reads the `ci-visual` recipe from the repository's `justfile` as it ships (the way
  `test_preflight_skips_only_the_stages_that_need_linux_or_macos_on_windows` reads `preflight`), and
  asserts that the recipe runs `test:breakout` with `STUDIO_REQUIRE_CHROMIUM=1` after
  `test:visual`. It also reads `package.json` and asserts that `test:breakout` targets
  `out/test/page/tableBreakout.test.js`. No prepared text: both files are read from the repository.

### `CONTRIBUTING.md`

- Where it lists what `just ci-visual` runs ("Playwright/Chromium against a mock host"), add the
  table breakout width tests, the variable `STUDIO_REQUIRE_CHROMIUM=1`, and that the `static` jobs
  skip them for lack of Chromium.

### Recording the Linux widths

- PR body, Deliverables: a table with the Windows and Linux widths for each value printed above
  (twelve cases per theme, test 2's three widths, test 5's open and narrower widths), with the
  verdicts and the difference. Windows: a local run at the CR's head (CR-351's PR body gives the
  expected values: cases `688 688 688 688 1068 735 748 338 537 719 894 824`, test 2
  `1068 972 1068`, tick matrix 719). Linux: read from the PR's `visual` job log
  (`gh run view <id> --job <visual job id> --log`), naming the run.
- The values also stay in every later `visual` run's log and in `tests-breakout.xml`.

## Stop rule (owner decision 2)

If the PR's `visual` job shows a Linux width more than 1 px away from its Windows value, or a
verdict that differs from `CASES` (the job is then red), the Driver changes nothing in the test's
cases, verdicts, column, pane or thresholds. It writes the Windows and Linux widths in the PR body
(Known gaps) and in its handback, and stops for the Chief of Staff, who asks the owner. The same
applies if the KaTeX fonts do not load on Linux.

## Out of scope

- A new CI job, an xvfb job, or a change to `.github/workflows/ci.yml`.
- Running Chromium in the `static` jobs (`just dev-ci` without `visual` stays as it is).
- The other browser unit tests (`svgBreakout`, `chartCsp`, `mermaidLabelFit`, the site tests):
  they still skip in the `static` jobs.
- The font-load hang when a pinned font fails to load (CR-427, before this CR in the series).
- `src/`, the visual baselines, `test/visual/` and the pinned-font helper `test/page/pinnedFont.ts`.
- Requirements: no behaviour of the extension changes. No SwRS edit and no
  `requirements/tiers/log.md` entry; the `@tests_req` markers of the test stay unchanged.

## Evidence

No host and default matrix: nothing in this CR depends on the agent host or on a configured value.

Before the push (Windows, the Driver's machine; CI guideline rule 2 as far as Windows allows, since
`preflight` skips `ci-visual` on Windows):

1. `fnm exec -- npm run compile`, then `STUDIO_REQUIRE_CHROMIUM=1 fnm exec -- npm run
   test:breakout`: all tests of the file pass, the diagnostics print the widths, and
   `out/reports/breakout/tests-breakout.xml` exists. These are the Windows widths of the PR table.
2. The same command with Chromium out of reach (`PLAYWRIGHT_BROWSERS_PATH` set to an empty
   folder): the tests fail and name the launch error. Without `STUDIO_REQUIRE_CHROMIUM` and the same
   empty folder: they skip with "no Chromium can start here", as before.
3. `uv run --group docs --group release --group requirements pytest test/build/test_workflows.py`:
   passes, including the new test. The new test fails on the previous `justfile`
   (constitution, section 3): shown by running it with the recipe change reverted.
4. `just preflight` passes (on Windows, its static stage, which runs `just check`).

After the push (Linux, proved only there):

5. The PR's CI: `visual` passes, and its log shows the breakout tests running (not skipped), their
   diagnostics with the Linux widths, and `ci-visual: passed`. `static`, `static-windows`, `report`
   and `checks` pass.
6. Each Linux width is within 1 px of its Windows width and every verdict matches `CASES`;
   otherwise the stop rule applies.

Commit type: `ci:` for the `justfile`, `package.json`, `test_workflows.py` and `CONTRIBUTING.md`
changes, `test:` for the test file; no scope
(`.agents/guidelines/git-commit-allowed-scopes.md`). One commit of type `ci:` is also acceptable.
