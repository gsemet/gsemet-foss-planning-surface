# CR-516 investigation (code at 5f0746d7, read only, nothing built or run)

`W` = `C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-09-CR-516`.
`CR` = this change's folder (parent of `work/`). Line numbers are at 5f0746d7.
Round 1 = specification Part 1, committed alone. Round 2 = Part 2 and the rest.

Questions only the user can answer: none, for either round.

## For both rounds: overlap with PR #540 (CR-514) and PR #543 (CR-507)

- #540: base main, open, clean, head f9dc2c630b852635e8bffcd0b00b42cc886b293c.
- #543: stacked on #540, open, DIRTY, head 6c5106e4589592002f828b6feb3d545a442591aa.
- Neither changes `ci.yml`, `justfile`, `contentLayoutStyles.ts`, `contentBlockStyles.ts`,
  `commentCompose.ts`, `scrollCore.ts`, `editMode.ts`, `codeCopy.ts`, `performanceProbe.ts`
  or `realInput/run.ts`. This CR can stay on `origin/main`.
- Possible shared files: `.agents/guidelines/ci.guidelines.md` and `CONTRIBUTING.md` (#543,
  round 1); `src/page/features/pageRuntime.ts`, `test/page/runtimeHarness.ts` (#540, #543),
  `test/visual` `scenarioIds.ts`, `CHANGELOG.md`, `requirements/tiers/log.md` (round 2).
- `docs/how-we-test.md` exists only in #543. Whichever change is higher in the stack adds the
  new job there (Driver to track; if this CR is lower, #543 must add it).

---

# Round 1: measure in a real window

## Files and entry points (under `W`)

- Generator source: `CR/experiments/gen.mjs`. Seeded `mulberry32` (seed 547); writes
  `report.md`, `svg/chart-NN.svg` (1100x560, about 16 kB) and `report.comments.json`
  (`{version:1, document, threads:[{id:"t_...", anchor:{line,endLine,quote,prefix,suffix},
  resolved, createdAt, comments:[{id:"c_...",author,createdAt,body}]}]}`). "full" =
  22 sections, 197 table rows, 11 images, 464 lines, 9 threads.
- Measure method used at intake: `CR/experiments/measure.cjs` (about l.40-428).
- `test/probe/` (`largeChapter.ts`, `frameProbe.ts` are the existing probe inputs).
- `test/integration/performanceProbe.ts`: `scenarioPerformanceProbe(page)`. Pattern:
  `createFixture`, `openSidePreview`, `waitForRender`, `currentPreviewFrame`, a local
  `settle()` (l.55, preview `ready`, no deferred work, 800 ms stable), CDP session on the
  page, report under `REPORTS_ROOT/probe/`, `closeAllEditors()` and `fixture.dispose()` in
  `finally`.
- `test/integration/realInput/run.ts`: `run()` connects the workbench, sets 1400x900, closes
  side bars; the `single` map picks the scenario from `STUDIO_REAL_INPUT_SCENARIO`
  (`toolbar`, `stress`, `toc-loop`, `probe`, ...). An unknown name silently runs the whole
  campaign.
- `test/integration/realInput/harness.ts`: `connectWorkbench()` is
  `chromium.connectOverCDP` on `STUDIO_CDP_PORT`; `createFixture` (l.76) creates sub-folders,
  so `svg/...` keys work.
- `test/integration/trusted-suite.ts`: default steps `setup`, `preview-smoke`, `real-input`;
  no change needed. A named scenario gives one window launch (`trustedParts.ts`).
- Budgets (`test/shared/hangWatchdog.ts` l.56-57, l.142): `real-input` step 10 min, launch
  deadline 15 min. Do not raise them; size the sample count to stay well under (target 5 min).
- `justfile`: `_require-unlocked-screen` (l.232), `ci-stress`, `ci-toc-loop` (about l.450-466).
- `.github/workflows/ci.yml`: 8 `workflow_dispatch` inputs; job `toc-loop` (about l.462-536).
- `test/build/test_workflows.py`; `.agents/guidelines/ci.guidelines.md` (rules 1, 3, 8, 9,
  11, 13); `CONTRIBUTING.md` (about l.328 toc-loop, l.434 probe command, l.553).

## Which input, which systems

- The real-window scenarios drive the pointer with Playwright `page.mouse` over CDP to the VS
  Code window. By Playwright's design these events are injected in the renderer and do not
  move the desktop's OS cursor; no OS-level mouse tool was seen in the harness. Not verified
  by a run here.
- Real VS Code stages run on Linux (CI, under xvfb) and macOS (local, unlocked screen).
  `CONTRIBUTING.md` l.28-29: not on Windows. This host is Windows, and
  `local-worktree.guidelines.md` "App-window tests" speaks of macOS: report local desktop runs
  as not run.

## Smallest change

1. `test/probe/perf547Document.ts` (new): pure TypeScript port of `gen.mjs`, returning a
   `Record<relativePath, content>` for `createFixture`, so round 2's test imports the same
   document. Drop the unused variants. Raise density (inline code and bold in cells, some
   blockquotes) to about 3000 page elements (reporter: 3160, of which 856 code, 864 strong,
   21 blockquote, 620 cells; intake "full": 1873). Keep 464 lines, 22 tables, about 197 rows,
   11 images, 9 threads (some in cells; check each quote still anchors after adding markup).
   No text from the reporter's gist.
2. `test/integration/perf547.ts` (new, beside `performanceProbe.ts`; mind the 1500-line test
   limit) and one `single` entry `"perf-547"` in `run.ts`. Steps: fixture, side preview,
   settle, assert 9 highlights and the element count; per sample scroll the target into view,
   `mouse.move/down`, paced moves (intake: 40 moves, 30 ms), `mouse.up`; running text and
   table cells; then click `[data-okf-comment-create]`, fill
   `[data-okf-comment-compose-input]`, click Save with the mouse.
3. Timing is taken inside the preview frame (one clock, no CDP round trip):
   - `selectionRelease`: capture listener on `window` for `mouseup` (runs before the page's
     document listener `released`, which refreshes synchronously) to the frame after
     `[data-okf-comment-create]` appears (MutationObserver, then rAF).
   - `commentCreate`: Save press to the frame after the count of
     `mark[data-okf-comment-thread], [data-okf-comment-badge]` grows and the box is gone.
     This includes the host round trip (author lookup, sidecar write, threads post).
   - Longest task per drag and release (`PerformanceObserver` `longtask` in the frame, or
     trace durations): point 4 of the specification depends on the 50 ms threshold.
4. Restyled elements: trace around the comment creation, sum `UpdateLayoutTree`
   `args.elementCount ?? args.endData.elementCount` (categories as in `measure.cjs`).
5. `out/reports/probe/perf-547.json`; the campaign CR reads the names, so keep them stable:
   `{schema, document:{lines,tables,rows,images,threads,elements}, interactions:{
   selectionRelease:{unit,samples,median}, commentCreate:{unit,samples,median}, <drag and
   longest-task entries>}, commentCreateRestyledElements:{samples,median}}`. No author name,
   no absolute path. No limit asserted; assert only what the measure needs to run.
6. `justfile`: `ci-perf-547: (_require-unlocked-screen "ci-perf-547")`, exports
   `STUDIO_REAL_INPUT_SCENARIO=perf-547`, runs
   `npm run test:integration -- --trusted-only`, prints finished or FAILED. One recipe serves
   the local command and CI. Optionally add it to the locked-screen parametrization of
   `test_workflows.py` (l.444-458).
7. `ci.yml`: boolean input `perf_547`; job `perf-547` copied from `toc-loop`
   (`if: !cancelled() && workflow_dispatch && inputs.perf_547`, `contents: read`,
   `timeout-minutes`, pinned actions, `just dev-ci`, `xvfb-run ... just ci-perf-547` with a
   step timeout below the job's, `just ci-hang-dump` and upload of `out/reports/` under
   `if: always()`, artifact `perf-547-attempt-${{ github.run_attempt }}`). Not in `checks`.
8. Docs: rule 13 on-demand jobs line in `ci.guidelines.md`; the command in `CONTRIBUTING.md`.

## Checks that constrain the new job (`test/build/test_workflows.py`)

SHA-pinned actions with tag comment (l.39); job permissions (l.49, l.55); needs of skippable
jobs (l.187); locked screen (l.446); `needs` references (l.795); xvfb screen size (l.861);
artifact names carry the attempt (l.1140); no fixed artifact download (l.1307); the toc-loop
input tests (l.1321) are the model for a `perf_547` test. Also `just check-markers` if a test
gets a requirement marker. Round 1 changes no `src/` behaviour; the toc-loop tool has no SwRS
found under `requirements/`.

## Risks

- `browser.startTracing` over `connectOverCDP` to Electron is not verified. The workbench and
  the webview may share a renderer (comment in `performanceProbe.ts`): filter trace events by
  the preview frame id (`args.beginData.frame`, CDP `Page.getFrameTree`), or the restyle count
  includes workbench work. Check in the first CI run that the count is plausible (headless
  intake: about 1900 on the smaller document, 3222 on the reporter's). If tracing is refused,
  report it; do not replace the number silently.
- Each `commentCreate` sample adds a thread. Use the same fixed count before and after and
  record it (or restore the sidecar between samples with a deterministic wait).
- The author falls back to git `user.name`, OS user, "Anonymous" (`core/comments/author.ts`):
  no prompt. Leave the setting unset so the measured path is the user's (the next CR changes
  it). On a local run the fixture sidecar and any screenshot carry that name: keep them out of
  evidence (floor rule 8).
- Selections must be made so that the previous button, box or selection does not affect the
  next sample (clear, settle).
- The "before" commit must be final before the three runs; if the branch is rebased between
  before and after, record both bases.
- A dispatch also runs the ungated jobs of `ci.yml`. No `concurrency` key was found in
  `ci.yml`, so three runs on one ref should not cancel each other.

## Evidence plan, round 1 (test and CI tooling; nothing visible to a user)

- Three runs on the Part 1 commit: `gh workflow run ci.yml --ref <branch> -f perf_547=true`,
  three times; keep each `perf-547.json` (`gh run download <id>`) in `CR/evidence/before/`
  with run id, URL and commit SHA; a table of each run, medians, restyle count, longest
  drag/release task.
- Local: test output of `test_workflows.py` and type check. Real-window local run: not run
  (Windows host).
- Cannot be shown: the reporter's machine and document; OS-level mouse behaviour; absolute
  timings comparable to a desktop (hosted runner, xvfb, no GPU).

---

# Round 2: the fixes

## Files and entry points (under `W`)

### Point 1: the three content-root `:has()` rules

- `src/core/preview/styles/contentLayoutStyles.ts`: `ALIGNED_FLOAT` l.39 (not exported);
  `TOOLBAR_FLOAT_CSS`; l.67 `:not(:has(ALIGNED_FLOAT)) > :not(...) {clear:right}`; l.76
  `:has(ALIGNED_FLOAT)::before {display:none}`.
- `src/core/preview/styles/contentBlockStyles.ts` l.19: literal copy,
  `:has(...) > :is(h1..h6) {clear:both}` (companion `.markers.ts` files).
- Other `:has()` rules are not on the content root and are out of scope.

Surfaces carrying these sheets (from a grep of the consumers):

| Surface | How the CSS arrives | Where the attribute is set |
|---|---|---|
| Preview first load | `preview.css` bundle (`core/preview/pageBuildEntry.ts`), or inline; `session/webview.ts` l.307-313 | host at render, then page at startup |
| Page built without `scrollContext` (`webview.ts` l.341) | same | host only. Callers seen: `rendering.ts` and `baselineDiff.ts` both pass a context |
| Content patch | page `features/contentPatch.ts` l.72 replaces the children of `main` only | page, in `initializeContent` before `firstClearance.update()` (l.126) |
| Runtime content changes (editors, moves, diagrams, comments, side by side) | same sheet | page MutationObserver |
| HTML export (no script) | `core/export/htmlExport.ts` l.68; body is the page's `main.outerHTML` (`page/modules/exportSnapshot.ts`) | kept from the page: `exportContent.ts` removal list does not match `data-okf-aligned-float` |
| Visual tests and the restyle test | same sanitizer and sheets (`test/visual/renderFixtures.ts` l.148, l.363; `buildPreviewWebviewHtml` in the model test) | host |

### Points 2 and 3

- `src/page/modules/commentCompose.ts` (474 lines): `blockBefore` l.121-133; `readSelection`
  l.136-173; `place` l.175; `showButton` l.204; `refresh` l.262-272; `released` l.401-408;
  listeners l.409 (`selectionchange`), l.410 (window scroll), l.412 (box follows, keep),
  l.417-419.
- `src/page/features/editMode.ts`: `setEditHover` l.18-24, `editHoverTarget` l.29-50,
  `bindHover` l.264-288.
- `src/page/modules/codeCopy.ts`: `pointTo` l.151-159, `mouseover`/`mouseout`/`mousemove`
  l.160-171; its scroll path is already framed (l.197-225).
- `src/page/features/scrollCore.ts` (569 lines): `stateSnapshot` l.33-76 (selection to text
  l.41-42), `postScroll` about l.324-360 (the only throttled path). Other callers are not
  throttled: `contentPatch.ts` l.157, l.163; `pageInput.ts` l.57, l.184.

## Smallest change

1. Aligned float. One shared constant pair (selector and attribute `data-okf-aligned-float`)
   in `core`, used by both sheets, the host and the page.
   - CSS, same specificity (0,1,1) as `:has(X)`:
     `#id:not(main[data-okf-aligned-float]) > ...`,
     `#id:is(main[data-okf-aligned-float])::before`, and the same `:is(...)` for headings.
     A bare attribute selector would be (0,1,0) and could change which `clear` rule wins
     (see `core/directives/figure.ts` l.35-70).
   - Host: set it on `main` in `core/security/html-sanitizer.ts` `rewriteSphinxHtml`
     (about l.549-564), after the `id` (`webview.ts` l.157 requires `id` first). Match
     `img|figure|table` with class `align-left|align-right`, or `align` equal to left/right,
     case-insensitive. This covers first paint and pages without the script.
   - `core/preview/contentPatch.ts` `analyze` (l.87-97): drop this attribute of `main` from
     the shell key. Without that, adding or removing the last float forces a full reload.
   - Page: new small module, installed in `runtime.ts` before `installFirstClearance`
     (l.209), updated synchronously in `initializeContent` before l.126, plus a
     MutationObserver (childList, subtree, attributes `class`/`align`) that queries again only
     when a changed, added or removed node is or contains `img|figure|table`. A comment mark
     then costs nothing.
2. `selectionchange`: one pending `requestAnimationFrame` calling `refresh`. `released`,
   `later`, `result`, `dismiss`, `open` stay synchronous (`selectionRelease` path). Scroll:
   return if the box is open; if `pointerDown || busy()`, clear and hide as today; else if
   `current`, place the button from `current.live()` (not the stored `rect`), hiding it when
   the live rect is gone (`isGone`).
3. a. `blockBefore`: walk back from `end` (previous siblings, then parents; ancestors of
      `end` are skipped); inside a sibling search its children last to first and stop at the
      first mapped element with a span; then climb to the outermost mapped parent not
      containing `end`. Same result as the pre-order search, no document query, and no
      `querySelectorAll` over a large sibling. The fake DOM has `previousSibling`, not
      `previousElementSibling`.
   b. `editMode` and `codeCopy`: keep the latest pointer target and apply once per frame;
      evaluate `figureEditButton.owns` and keep `pointerX/Y` at event time; any direct
      `setEditHover`/`hide`/`show` (content patch, edit mode off, click, focus) cancels the
      pending pointer update; `mouseout` with no related target still hides.
   c. `scrollCore`: cache the selected text; mark it stale on `selectionchange`, on content
      replacement, and when anchor/focus node or offset differ (`selectionchange` is
      asynchronous); non-throttled snapshots always recompute.
4. Only if a "before" run shows a drag or release task above 50 ms.

File limit is 800 lines for `src/` (baseline empty): `contentBlockStyles.ts` 748,
`html-sanitizer.ts` 697, `contentLayoutStyles.ts` 689; `commentThreads.ts` is at 800, do not
add to it.

## Restyle test without a VS Code window

- New `test/page/commentRestyle.test.ts` on the model of `test/page/tableBreakout.test.ts`
  (`openPage` l.206-267: real render pipeline, `buildPreviewWebviewHtml`,
  `pageRuntimeScript()`, Chromium, stubbed `acquireVsCodeApi`;
  `chromiumUnavailable` l.192-198 skips unless `STUDIO_REQUIRE_CHROMIUM=1`).
- Flow: generated document; post `{type:"previewComments", threads, documentId, revision,
  requestId}` with the initial threads (`session/features/comments.ts` about l.237); wait to
  settle; start tracing; post the same list plus one thread; wait for the new mark and two
  frames; stop; sum `UpdateLayoutTree` element counts; assert <= 100. Assert also that the
  count is above 0 and the mark exists, so an empty trace cannot pass.
- Add the file to `package.json` `test:breakout` (l.480): `just ci-visual 1` runs it with
  Chromium required. Update `test_workflows.py` l.359-360 (`endswith(breakout_files)`) and
  check the wording of CORE-076#S12. `test:unit` (so `just check`) also globs `test/page`,
  but `just dev-ci` without `visual` installs no Chromium (`justfile` l.53), so only the
  visual stage guarantees it.
- Intake: 1893 elements before; 16 with the `:has()` rules removed; 205 with only l.67
  removed, so all three must go. Unverified on the denser document: confirm both numbers.

## Requirements and tests

| Behaviour | SwRS (markers) | Tests |
|---|---|---|
| Aligned float layout | LAYOUT-043 (S2, S5, S6; verification notes l.105-108; implemented/tested file lists), LAYOUT-011; LIFE-069/071 for the shell key | `test/page/modules/firstClearance.test.ts` l.338-391; visual `toolbarFloatScenarios.ts` v88, v89, v90 (fixtures 75, 76); `test/core/render/mystPaletteRendering.test.ts` l.197; `test/core/frontmatter/propertiesTable.test.ts` matches the `main` tag; CSS-text test model `test/core/preview/gridCardEditStyles.test.ts` |
| Comment button | REVIEW-038, 044, 049 (S3 triple click), 217, 218 | `commentCompose.test.ts` (fake window has no rAF: add and flush), `commentEditorBehaviour.test.ts`, `diagReq.diagrams.requirements.test.ts` |
| Hover actions | BLOCK-017, BLOCK-109, BLOCK-262, TRUST-001 | `runtimeBlockEditor`, `runtimeListItemMove`, `linkEditModeClick`, `blockReq.requirements`, `fmtableReqFrontmatter` tests (harness `frameQueue` about l.923 to flush) |
| Copy button | CODE-017, CODE-019 | `codeCopy.test.ts` (`flushFrames` l.189; helpers assert right after the event), `renderReq.codeCopy.requirements.test.ts` |
| Restored selection | LIFE-069, 108, 125 | `test/host/lifeReq.requirements.test.ts` about l.1134, `test/core/state/previewState.test.ts`; no page test found that asserts the posted `selectedText`: add one (changed, unchanged, patched) |

New or amended SwRS for every changed behaviour, including the 100-element limit; no StRS
change; at most 3 ids per marker block (`just check-markers`); `just requirements-update` and
a log entry.

New tests needed: host sets/omits the attribute; page switches it after adding and removing
the last float (patch and runtime change) with the computed `clear` and `::before` unchanged
from today; shell key equal across the switch; export keeps the layout; frame coalescing and
scroll-only behaviour; `blockBefore` cases (nested list, table, first block).

## Risks and derived values

- Values derived from the `:has()` rules: `page/modules/firstClearance.ts` l.154-176 reads the
  first block's computed `clear === "right"` and `::before` `display === "none"`. It measures
  at install and at each patch, so the attribute must be right before both; its observer filter
  (l.331: link state, `hidden`, `href`) does not see the new attribute, so after a
  runtime-only switch call `firstClearance.update()`.
- Without the host attribute, the first paint before `preview.js` (script at end of body,
  `webview.ts` l.85-103) would lay out a floated document wrongly.
- A hidden webview delivers no animation frames: the framed updates then wait until it is
  visible. Tests that expect the button or hover immediately need a flush; real-window tests
  should already wait.
- Scroll no longer re-reading: a button whose text was removed or whose selection collapsed
  must still disappear (selectionchange plus the `isGone` check).
- Existing fake selections without anchor/focus fields would look "unchanged": dispatch
  `selectionchange` in the harness.
- Listeners of `linkTooltip`, the TOC column and the figure panel are not named by the
  specification: leave them.

## Evidence plan, round 2 (performance fix; no intended visual change)

- Restyle test: output failing on the pre-fix source (count above 100), then passing, both
  counts kept in `CR/evidence/`.
- Layout and behaviour tests green; visual v88-v90 unchanged. PR Impacts: "No visual change"
  with this reason.
- Three `perf_547` runs on the head, in `CR/evidence/after/`; PR body and evidence give the
  six runs, medians per interaction and the restyle counts; "not separable from runner noise"
  when the ranges overlap; explain anything slower beyond the spread; state whether the 50 ms
  selection stall was seen.
- `just preflight` (Windows: static stage only, say so) and a green heavy CI run of the head
  (`-f heavy=true`).
- PR references issue 547 without a closing keyword; nothing posted on the issue.
- Cannot be shown: the reporter's machine and document; local desktop runs (Windows); a
  timing target (none set).
