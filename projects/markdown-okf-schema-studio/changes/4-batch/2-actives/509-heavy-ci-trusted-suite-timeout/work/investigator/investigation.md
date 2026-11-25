# CR-509 investigation (before round 1, read only)

Paths are relative to the worktree `C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-09-CR-509`
(HEAD 3ea161ce) unless absolute. "Folder" is the CR planning folder. Nothing was run on the code;
every statement is from reading code, logs and artifacts.

## Verdict

- **Take the spec split** (part 1 = setup, preview-smoke, project-features..find-in-preview, then all
  38 `remainingSteps`; part 2 = setup, preview-smoke, real-input, preview-editing). No state
  dependency found in either direction (static reading; timing and window warm-up only a heavy run
  can show). The contiguous split misses the 600 s bar on a slow runner.
- Two gaps between the spec and the code: no log line names a launch on a green run (evidence item
  4), and the dump folder is named after the step, not the launch (section 2).
- The attempt-2 artifact neither confirms nor contradicts the blank-frame theory.

## 0. Files and entry points

| File | What is there |
| --- | --- |
| `test/integration/trusted-suite.ts` | `run()` L69-71, `runTrustedSuite` L222-342, scenario early returns L230-264, `onlyRealInput` L265, 13 first-group steps L267-287, real-input L288-293, early return L294, preview-editing L295-300, `remainingSteps` L301-340 |
| `test/integration/run-tests.ts` | `runScenario` L90-174 (`browserSuite` L114, heartbeat L117, port L119, `watchLaunch` L135, `extensionTestsPath` L138, env L139-149, frontmatter block L154-167), `main` L235-262, manifest scope L271-272 |
| `test/integration/stepWatchdog.ts` | `withSuiteWatchdog` L50-73 (suite label goes to the heartbeat only) |
| `test/shared/launchWatchdog.ts` | reason lines L101-105 (use `options.name`), dump folder step L115 |
| `test/shared/hangWatchdog.ts` | `STEP_BUDGETS_MS` comment L48-52, `heartbeatFileFor` L252, `safeName` L326-328 (60 chars) |
| `test/integration/realInput/harness.ts` | `waitFor` L51-68, `findCurrentFrame` L127-147, `frameCall` L149-161, `currentPreviewFrame` L209-229 |
| `test/integration/previewEditing.test.ts` | texts L1173 and L1498 |
| `test/build/hangWatchdog.test.ts` | names at L151-158, L232-237, L286-289 |
| `CONTRIBUTING.md` | trusted window mentioned at L302, L387, L482, L489, L497, L500 |

Today's full trusted list is 55 step names: setup, preview-smoke, 13, real-input, preview-editing, 38.
Part 1 holds 53, part 2 holds 4.

## 1. State dependencies between the two groups

### Does a `remainingSteps` step rely on `real-input` or `preview-editing`? None found.

- Fixtures and modules: every user of `realInput/common.ts` (module state `workbenchPage` L79-84,
  failure dump L86-97, `leaveEditModeOff` L103-116, `withDocument` L125-146) is under
  `test/integration/realInput/`. No remaining step imports it. `linkedTargetSave` is imported only
  by `previewEditing.test.ts` L19 and `realInput/run.ts` L17. Fixtures are per step
  (`createFixture`, `harness.ts` L70-91, disposed).
- Evidence files: no remaining step reads another step's evidence.
- Viewport: both steps close their CDP connection (`previewEditing.test.ts` L1486,
  `realInput/run.ts` L377), and Chromium drops that client's emulation on disconnect
  (`realWindowViewport.ts` L63-68). So the 2400x1100 viewport does not carry into `edit-keys`.
- Stored choices: pins are `previewThemeMode: current`, `toolbarCollapsed: false`,
  `paletteMode: myst` (`storedChoices.ts` L11-19). The one difference found: `preview-editing`
  toggles the preview theme and leaves it **dark** (`previewEditing.test.ts` L1405-1416,
  L1428-1442; its `finally` L1481-1495 does not restore it). So today `edit-keys`, `save-key` and
  `grid-card-editor-blur` run under "dark" until `paste-url` re-pins (`pasteUrl.test.ts` L168-169).
  After the move they run under "current". A grep found no theme assertion in the three.
- Settings: `preview-editing` restores `allowOutsideWorkspaceLinks` (L1491-1495); other workspace
  setting changes are restored by their own steps (`lifecycle.test.ts` L251-262,
  `openAtLineHelpers.ts` L44-57, `radioChoice.test.ts` L369-385).
- Tabs and clipboard: `preview-editing` closes only the active editor, so it can leave tabs behind;
  `edit-keys` makes its own fixture, opens its own preview and closes all editors
  (`editKeys.test.ts` L44-116). Each clipboard read in the remaining steps follows its own write.
- Side bar: `closeSidebar` / `closeAuxiliaryBar` are already run by earlier part-1 steps.

### Reverse: do `real-input` or `preview-editing` rely on what part 1 now holds? None found.

- The first group leaves the stored choices as after `setup`: the steps that change them re-pin
  (`tableEmptyColumn` L207-208, `tallBlockScroll` L398-399, `findInPreview` L371-372,
  `editToolbarCover` L232-233, `blockActionsFollowSelection` L197-198). No step of that group changes zoom, width,
  comments or toc preferences.
- `real-input` sets up its own page: `realInput/run.ts` L207-218 (connect, evidence, focus trace,
  viewport 1400x900, close both side bars).
- `preview-editing` still follows `real-input` directly, as today.

### Does part 2 work as the existing real-input-only path shows? Only partly shown.

`setup`, `preview-smoke`, `real-input` is the `stress` / `toc-loop` / named-scenario path
(L224-294). CI runs it with the **subset** `STRESS_SCENARIOS` (`realInput/run.ts` L81-115). The
**full** real-input campaign has never run on CI in that window, and `preview-editing` never runs on
that path (L294). The first scenarios of `real-input` will meet a colder window, with the
`preview.md` text tab of `preview-smoke` still open (L74-126), as on the stress path. The heavy run
is the proof.

### Durations (log `<folder>/work/scratch/run-45713440510-integration.log`, green, 17b779d)

- setup start 22:31:06.97 to find-in-preview done 22:35:44.17 (L889): 277 s.
- real-input 405 s (L1748); preview-editing 32 s (L2759); edit-keys to workspace-disposal
  (22:43:01.93 to 22:44:57.51, L2929): 116 s. Whole trusted window about 831 s.

| Layout | Part 1 | Part 2 green | Part 2 slow runner (real-input 455 s) |
| --- | --- | --- | --- |
| spec split | about 393 s (about 420 slow, estimate) | about 439 s | about 495 s |
| contiguous | about 277 s | about 555 s | about 620 s (estimate), over 600 |

## 2. Does anything rely on exactly one trusted launch?

Nothing downstream does. `standalone`, `reverse-migration` and `reload` make their own directories
(`run-tests.ts` L181-233); each `runScenario` makes a new user-data dir, workspace file and port
(L95-119); `review-index.ts` L43-70, `scripts/e2e-campaign.mjs` L140-187 and
`test/site/reportPruner.ts` L16 read manifests or folder prefixes, not launches. One suite file
stays, so `test/shared/e2eGroups.ts` L61/L66, `@tests_req` markers and SwRS method lines stay valid.
`main()` awaits in sequence, so a part-1 failure stops part 2 (same stop-at-first-failure as today).

Smallest change:

1. New pure module in `test/shared/` (no `vscode` import): the step names of each part, the part read
   from `STUDIO_TRUSTED_PART` (unknown fails; missing fails only when
   `STUDIO_REAL_INPUT_SCENARIO === undefined`, the same predicate as L265, so an empty string counts
   as a scenario), and the launch descriptors (suite file, launch name, heartbeat suite name, runs
   preview-editing or not).
2. `trusted-suite.ts`: a name to runner map typed on the names (a missing runner fails to compile),
   run the part's list; early-return scenario paths unchanged; suite label for `withSuiteWatchdog`
   names the part.
3. `run-tests.ts`: separate the suite **file** (`trusted-suite.js`, used at L114, L138) from the
   launch **name** (L135, e.g. `trusted-suite.js part 2/2`) and the heartbeat suite name (L117, use
   a clean one such as `trusted-suite-part-2`; `heartbeatFileFor` strips only a trailing `.js`).
   Pass `STUDIO_TRUSTED_PART`. Frontmatter block L154: condition = the launch that runs
   preview-editing (on scenario paths it finds nothing to rewrite today too, because
   preview-editing does not run). `main()` L244 and L258: both parts, unless a scenario is set.
4. **Dump folder gap:** L115 of `launchWatchdog.ts` names the folder after the heartbeat step
   (attempt 1's folder is `...-diff-preview-scroll`), not after `options.name`. `setup` and
   `preview-smoke` exist in both parts, so the spec's "dump folder say which part stopped" needs a
   change here, e.g. an optional label in the watch options, put **before** the step name (60-char
   cut), set only for the trusted parts so other dump names do not change.
5. **Log gap:** `STEP start/done` lines carry no suite name (`hangWatchdog.ts` L229-244), and
   `watchLaunch` logs only on failure (L106). Evidence item 4 ("each part's log shows its own launch
   name") needs one added line per launch, best printed in the extension host from the received part
   (proves the variable arrived).
6. Texts: `previewEditing.test.ts` L1173, L1498; `STEP_BUDGETS_MS` comment L48-52 (the old value
   "265 to 400 s" appears only there in the code); CONTRIBUTING.md lines above.
7. Unit test in `test/build/` (`test:unit` globs `out/test/build`): hard-code today's 55 names;
   every name is in exactly one part **except `setup` and `preview-smoke`, one in each** (the spec's
   "exactly once" needs this exception stated); each part keeps today's relative order; distinct
   launch names, heartbeat file names and dump labels; unknown and missing part fail.

## 3. What the attempt-2 artifact and log show about the `locator.count` timeout

Log `<folder>/work/scratch/artifacts-45706313890/run-45706313890-attempt-2-failed.log`:

```
L367 22:10:11.271 CodeWindow: failed to load (reason: <unknown>, code: -3)
L369 22:10:13.493 STEP done: stock-coexistence (3526 ms)
L371 22:10:13.498 STEP start: open-at-line
L374 22:10:26.050 STEP failed: open-at-line (12624 ms): TIMEOUT: locator.count did not return within 10000 ms (frame )
L376             at Timeout.<anonymous> (.../out/test/integration/realInput/harness.js:194:41)
L377-378         at listOnTimeout / at process.processTimers
```

Proven:

- A `locator.count` wrapped by `frameCall` did not return in 10 s, on a frame whose `url()` was the
  empty string when the timer fired (`harness.ts` L156).
- It is a step failure about 12.6 s into `open-at-line`; setup, preview-smoke, project-features,
  hostile-html and stock-coexistence had passed in that window (L357-369).
- The artifact `e2e-integration-attempt-2` holds `integration-manifest.json` (status failed, scope
  all, runId 45706313890, 22:07:34 to 22:10:26), `campaign-integration.json`,
  `hang-dumps/post-step/ps.txt` and only scroll and untrusted screenshots.

Inferred, not proven (the stack has no caller): the call is `findCurrentFrame` from `pageMarks`
(`openAtLine.test.ts` L40, `openAtLineHelpers.ts` L89, `harness.ts` L132). The count started about
2.5 s into the step, which fits the first block (two opens and `settle(1500)`, L28-36) then L37-40.

Not proven: which frame it was, why it had no URL, whether it was the Studio frame in transit, the
frame list, any link to `stock-coexistence`. `ps.txt` was taken after the step ended (22:10:26) and
lists no VS Code, Electron or Xvfb process, so it says nothing about the window at failure. There is
no in-window dump, no CDP target list, no trusted screenshot and no VS Code log.

- `code: -3` is a weak lead: the attempt-2 log has one during the passing `untrusted-suite` (L307),
  and the green run has 16 such lines, in passing steps (e.g. L684, L690, L759, L923).
- Related earlier incident (same class, same predecessor):
  `C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/5-archives/261120-1146-425-real-window-test-flakes/work/checkbox-hang-evidence.md`
  (an unbounded frame call hung just after `stock-coexistence` disposed webviews; this led to the
  bound). `stockCoexistence.test.ts` L258-275 does not wait for webview frames to go.
- Attempts 1 and 3 (downloaded beside it, `artifacts-45706313890-attempt-1`, `-attempt-3`) are the
  launch timeouts; they contain nothing about this failure.

The theory is not contradicted, so the spec's fix stands. The PR should say "empty URL observed,
frame identity unknown".

## 4. URL shape of a Studio webview frame

Evidence:

- Real window, Windows, VS Code 1.147.0
  (`C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/5-archives/261121-1528-453-flaky-realinput-t45/work/forced-failure.md` L6):
  workbench `vscode-file://...` has no content; `vscode-webview://<auth>/index.html?id=...&extensionId=GaetanSemet.markdown-okf-schema-studio&platform=electron...`
  has **no** content; `vscode-webview://<auth>/fake.html?id=...` **has** `#sphinx-myst-preview-content`.
  `test/shared/workbenchFocusDump.ts` L190-214 and `test/build/workbenchFocusDump.test.ts` L129-132
  encode the same two shapes.
- CI Linux, VS Code 1.148.0 (`cdp-targets.json` in the attempt-1 and attempt-3 dumps): workbench
  `vscode-file://vscode-app/...`, service workers `vscode-webview://<authority>/service-worker.js?...`.
  No iframe target is listed, so the **scheme** is confirmed on CI, the content frame URL is not.
- The content is written into the `fake.html` frame; `document.write` does not change the URL.
  Playwright (`node_modules/playwright-core/lib/coreBundle.js` in the main checkout): a Frame starts
  with `_url = ""` (L24747-24774), changes only on navigation events (L38941-38958, L39136-39153),
  and initial empty out-of-process documents are skipped (L39105-39107). So `""` = "no navigation
  seen yet".
- No evidence of any content frame with an empty or `about:blank` URL in this project's logs.

Safe filter:

- Keep **every** URL that starts with `vscode-webview://` (do not narrow to `fake.html`; do not use
  `isWebviewHostFrameUrl`, which matches the host `index.html`, the frame without content). Skip
  `""`, `about:blank` and all else, from `frame.url()` only, before any other call.
- A frame still at `""` is picked up by the next poll once it commits (`waitFor` already polls).
- Self-diagnosing: have `findCurrentFrame` record its last scan (each URL, kept or skipped and why:
  URL, no content, hidden, attribute mismatch) and have `harness.waitFor` append it to
  `Timed out waiting for ...` **only when that scan happened during this wait**. Appending in
  `currentPreviewFrame` alone is not enough: most direct callers use
  `waitFor(findCurrentFrame ...)`, e.g. `openAtLine.test.ts` L91 and `openAtLineHelpers.ts` L88;
  none of the direct callers defines its own `waitFor`. If the real shape differed, the first heavy
  run would then print the URLs it skipped.
- Apply the same predicate to the failure dump `harness.ts` L216-222 (already bounded and caught;
  today a blank frame only delays it 10 s).
- Testability: put the predicate and the candidate selection in `test/shared/` so a unit test can
  give fake frames and prove that a blank frame gets no call other than `url()`.

Callers of `findCurrentFrame` (`test/integration/`): definition `realInput/harness.ts` L127.
Direct: `commentContrastWindow` 168; `commentTitleWindow` 62; `editKeys.test` 28, 90;
`listItemMoves` 48, 65; `mystBlocksWindow` 98; `openAtLine.test` 91; `openAtLineHelpers` 89;
`readmeHtmlWindow` 98; `realWindowGaps` 56, 301, 336; `saveKey.test` 47; `scenarioTrace` 49;
`tableMoves` 78, 102; `tableStructureReal` 64, 87, 144; `tocWindow` 93; `windowFocus` 101; in
`realInput/`: `alertPickProbe` 79; `blockKeys` 47, 322, 563, 591, 620, 628, 663, 687, 717; `common`
42, 52, 107; `editorWidgets` (71 to 952); `findAfterClick` 46, 66; `findWideTable` 53;
`flushBeforeNavigate` 85-377; `frontmatterFields` 103-724; `harness` 166, 212, 401, 529, 534;
`labelRenameAboveTable` 54, 90, 95; `linkEditMode` 104; `previewWindow` 84-322; `qa210Replays` 190,
302; `rawCopy` 156; `renderPatching` 68-736; `tableEscape` 50; `tableInsertSlash` 26-144;
`tableStaleRender` 77, 107; `tableTabRow` 48-67; `textEditing` 98-847; `wideTableTab` 76, 125. Many
more go through `currentPreviewFrame`, `withCurrentFrame`, `waitForEditor`, `setEditMode` (about 290
occurrences in 46 files). `liveChart.ts` on origin/main uses `withCurrentFrame` only, no own scan.

Other `page.frames()` scans, **not** covered by changing `findCurrentFrame`, with unbounded calls on
every frame (a blank frame could hang them to the step budget): `openAtLine.test.ts` 117 (inside
open-at-line itself; `.catch(() => 0)` does not stop a hang), `blockActionsFollowSelection.test` 30,
`editToolbarCover.test` 37, `findInPreview.test` 35, `tableEmptyColumn.test` 34, 54,
`tallBlockScroll.test` 32, `previewEditingHelpers` 36, `realInput/renderPatching` 413, 710,
`reload-suite` 47, 151, `scroll-sync-suite` 33, `windowFocus` 158 (diagnostic `evaluate`). The spec
names only `findCurrentFrame`. Driver decision: apply the predicate at least to
`openAtLine.test.ts` 117 (the spec asks that the open-at-line steps pass), and list the rest in Known
gaps or filter them with the same one-line predicate.

## Risks

- Part 2's full real-input campaign plus preview-editing is new on CI (colder window).
- `edit-keys`, `save-key`, `grid-card-editor-blur` change preview theme (dark to current) and run in
  a window without the preceding long campaign; a hidden warm-up dependency shows only in a heavy run.
- Whole step: about 1002 s today plus about 15 to 20 s (second window, repeated setup and smoke):
  about 1020 s green, near 1100 s on a slow runner (estimate), against 1200 s.
- A filter that skips the real frame breaks every step; the scan diagnostics are the safety net.
- Base is stale (origin/main 17b779d ahead): after the rebase, re-check that `trusted-suite.ts` has
  the same 55 names. Today's difference adds `realInput/liveChart.ts`, 4 lines in `realInput/run.ts`,
  one capture entry and a `ci.yml` comment; the green durations (17b779d) already include it.
- Derived from the single-launch assumption, to update together: `suiteName === "trusted-suite.js"`
  (L114, L154), heartbeat name, `STEP_BUDGETS_MS` comment, previewEditing texts, CONTRIBUTING.md.
  No budget, deadline or `timeout-minutes` value changes.

## Questions only the user can answer

None. Open Driver decisions: dump-folder label and launch log line (section 2, points 4 and 5), and
the scope of the filter for the other scans (section 4).

## Evidence plan

Kind of change: test infrastructure and CI reliability; no product behaviour, no SwRS change, no
visible UI change (no screenshots to compare).

Before (already available):

- Durations from runs 45476952370 (63ef752) and 45713440510 (17b779d); failures 45580228461 and
  45706313890 attempts 1 and 3 (LAUNCH TIMEOUT), attempt 2 (the quoted lines of section 3).
- New `test/build` tests written first and seen failing: part lists (55 names), part selection
  errors, distinct launch/heartbeat/dump names, frame URL predicate on the two real URL shapes, and
  "a blank or about:blank frame receives no call but url()".

After, local (Windows):

- `just check` (includes the new tests, file size, boundaries, unused exports), `just preflight`
  (static stage), `just requirements-lint` and `just requirements-update` with no unexpected diff.

After, CI only: two runs in a row on the same head,
`gh workflow run ci.yml --ref <branch> -f heavy=true`, `integration` and `stress` green. For each,
from `gh run view <id> --log`:

- the launch line of each part, then its `STEP` lines; duration from its `STEP start: setup` to its
  last `STEP done`, at most 600 s;
- the `STEP done` names of both parts compared with the 63ef752 log: same set, `setup` and
  `preview-smoke` twice, order kept inside each part;
- whole `just ci-integration` step duration under 1200 s, stated with its margin;
- table before/after: trusted launch, each part, real-input, open-at-line-probe, whole step, run ids;
- in the `e2e-integration-attempt-<n>` artifact: `integration-manifest.json` passed, the
  `frontmatter-e2e-*/manifest.json` with `suiteResult: passed` and `FRONTMATTER-LATEST.md` (proves the
  frontmatter block ran after part 2);
- `stress` log: one trusted launch on the scenario path.

Cannot be shown: a real-window run on the Windows machine; that the frame lookup is fixed (one
failure in many runs, two green runs prove little; the unit test proves only that blank frames are
skipped); the frame filter's message on CI unless a wait times out; a wider step margin than about
15 % (known gap).
