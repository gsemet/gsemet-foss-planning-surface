# Change Specification: fix the flaky real-window integration steps of the v1.9.0 release

Type: test and ci (tests, harness and workflow only; a product fix only if the evidence below proves
a product bug, filed separately first). Automatable: the owner's answer of 2026-11-14 settles the
scope, and the Chief of Staff decided the method with no user impact (02-answers.md).
Sources: `01-intent.md`, `02-answers.md`, the CR-323 archive
(`.agents/changes/4-archives/261114-0709-323-release-v1-9-0/`), `gh run view <id> --log-failed` of
every red heavy run around the v1.9.0 release (table below), the hang dump of run 43500084136
(artifact `e2e-integration-attempt-1`, expires 2027-02-11). Code read at `origin/main` `4b45b45e`
(version 1.9.0).

## Goal

The owner's words: « oui je pense qu'il faut tout corriger et retenter une release ».

1. Every real-window step that failed without a change during the v1.9.0 cycle has a cause proved by
   evidence, written in the commit and the PR, and fixed with a deterministic readiness signal or an
   environment fix (CI guideline rules 9 and 12): no sleep, no retry loop, no raised timeout.
2. A retry stays acceptable only where the cause is the host (VS Code or the X server), and it is
   documented next to the code with the evidence that proves it.
3. No test is removed or skipped.
4. Every fixed scenario is in the stress list, and a branch heavy run plus a stress run on these
   scenarios are green.
5. A real product bug found on the way is filed as its own inbox item and brought back to the owner,
   not fixed silently here.

## Flake log (what failed, and what the logs prove)

| Id | Run, attempt | Event, commit | Job, step | Message | Re-run |
|----|--------------|---------------|-----------|---------|--------|
| A  | 43532691444, 1 | push `main`, `1191fb6c` | integration, `toc` | `STEP failed: toc (7379 ms): Edit mode did not switch to on: the toggle missed 3 clicks.` | attempt 2 green |
| B  | 43536948441, 1 | branch heavy, `f12ba53b` (CR-323) | integration, real-input `palette` (RI-T21, fixture `realinput-t21`) | `Timed out waiting for Heading 2 to prefix the line. Editor state: {"tag":"BODY"}` | attempt 2 green |
| B2 | 43416264245, 1 | push `main`, `fd8adb9e` (docs only) | stress, round 15/20, `alert-dropdown` | `Timed out waiting for Warning to change the type. (no redo: ... commit at 749 ms (related=none commit active=body pageFocus=true): not a blur to nowhere ...)` | none (advisory) |
| C  | 43500084136, 1 | push `main`, `d8ff17d3` | integration, `checkbox-toggle` | `STEP TIMEOUT: checkbox-toggle did not finish within 180000 ms; last progress marker: waiting for the first checkbox render` | none; next push green |

Not counted as flakes (a real change was being fixed, or another cause): branch runs 43476490855
(toolbar cover), 43340259932 and 43334982738 (save key, untrusted, CR-312), 43332702161 (visual),
and 43567601653 (the v1.9.0 version push, red at release/package on the Open VSX OIDC issue, a
separate CR-323 retro item).

### A. `toc`: three clicks in a row never reach the edit toggle

What the logs prove (every one of the three attempts recorded the same state by
`editToggleState` in `test/integration/realInput/harness.ts`):

- render `3@1`, mode `off`, toggle box `1215,16,30,30` in the content frame, `hit` = the toggle's
  `svg`, `hitIsToggle: true`, `workbenchHit: iframe.webview.ready`, focus `body.vscode-light`,
  clicks `0` before and after, no page errors.
- So the page was ready, the toggle was on top at its own centre, and nothing was in flight; the
  mouse events never reached the content document at all (the capture-phase counter stayed at 0).

Leading cause (strong evidence, to confirm in the CR):

- The X server is smaller than the emulated viewport. `ps-forest.txt` of the C hang dump shows
  `Xvfb :99 -screen 0 1280x1024x24`: `xvfb-run --auto-servernum` without `-s` in
  `.github/workflows/ci.yml` (the `integration`, `stress` and `toc-loop` jobs) gives the default
  1280x1024 screen.
- `scenarioToc` (and `run()`) call `page.setViewportSize({ width: 1400, height: 900 })`. This is CDP
  device-metrics emulation: it changes the layout viewport, not the real window.
- With the sidebar closed and the editor group maximized, the toggle centre (about x=1230 in the
  webview, plus the 48 px activity bar) is at about x=1278 or more in the page: at or past the
  1280 px edge of the real screen. The CDP screenshot of the C dump (also 1400 px wide) shows the
  floating toolbar's pencil toggle at about x=1283.
- Input dispatched outside the real window surface can be dropped before it reaches the
  out-of-process webview frame, while the renderer's `elementFromPoint` still answers the iframe.
  A few pixels of layout variation (scroll bar, toolbar width, font metrics) decide whether the
  point is inside: this explains both the three lost clicks in a row and the intermittency, and why
  280 `toc-loop` rounds (CR-207, `reports/repro-attempts.md`) did not reproduce the old suspect.
- Other steps emulate widths over 1280 too: commentContrastWindow, readmeHtmlWindow,
  tableEmptyColumn, untrusted-suite, radioChoice (1400), mystBlocksWindow (1400x1000),
  reload-suite (1440), previewEditing (2400x1100), editToolbarCover and tallBlockScroll (variable).
  Any click they make past x=1280 has the same exposure.

What the logs do not prove: the real window bounds at the time (not logged), and whether the host
frame `index.html` saw the events (not probed). The CR adds both diagnostics before relying on the
cause.

### B and B2. Block editor closes right after a click in the webview: a focus bounce

What the logs prove:

- B (palette): the workbench focus dump shows `window-focus active body` at -10061 ms then
  `focusin iframe.webview.ready` / `window-focus active iframe.webview.ready` at -10060 ms, right
  around the click on `[data-edit-option='2']`, about 620 ms after the webview was entered. The host
  frame `index.html` reports `hasFocus=false`, active element `body`. At the end the content page's
  active element is `BODY`: the text box lost the focus, the editor committed on leave
  (SwRS-MDOKFSTUDIO-BLOCK-047) and Heading 2 was never applied.
- B2 (alert-dropdown): page trace: alert `mousedown` at 529 ms (prevented); the Warning click left
  no `mousedown` at all; block editor blur at 749 ms with `pageFocus=true`; page blur at 751; content
  patch at 819; editor closed at 820. Host window states: `{ at: 1014, focused: true }`;
  `pageTraceStart` is 269, so page 749 is host 1018. The VS Code window became focused at that very
  moment, and the workbench re-focus went through `body` and blurred the text box.
- The redo proof `editorBlurBeforePress` (`test/shared/editorBlurInterruption.ts`) accepts only a
  window focus loss (`pageFocus=false`, page blur within 50 ms, host blur within 1000 ms), so B2 got
  no redo. `scenarioPalette` has no redo, no `waitForPageSettled`, no `waitForTextInput`, and
  records neither window states nor the page trace, so B explains itself less than B2.

Hypotheses (the CR separates them with the new diagnostics before choosing the fix):

- H1, host: on xvfb without a window manager the VS Code window is not OS-focused at the start of
  the scenario; `ensureTestWindowFocused()` (`test/integration/windowFocus.ts`) is a no-op off
  macOS. The first real click activates the window late, and the workbench restores its focus
  through `body` and back to the webview, blurring the content element. A real user's window is
  focused before they click, so this is a test-environment race.
- H2, product: VS Code's webview focus handling (group activation, then a pane or webview focus that
  bounces through the workbench `body`) blurs the content element even in a focused window, for
  example when the click moves focus from the text editor group to the preview group, or a group
  unlock focus command (`src/host-vscode/groupLock.ts`, `groupFocus.ts`) lands late. A real user
  could then see a block editor close right after it opened.

### C. `checkbox-toggle`: a hang past two 10 s timeouts

What the dump proves: the screenshot shows the preview rendered; host state: window `focused: true`,
`active: false`; group 2 holds `preview.md`, `preview-other.md` and `Studio · tasks.md` (active),
group 1 `tasks.md` and a dirty `feature-contract.md`; CDP targets: one page, one webview iframe,
three service workers. The last marker is `waiting for the first checkbox render`, followed by
`waitForRender(document)` (10 s) and `currentPreviewFrame(page)` (10 s `waitFor`), yet the step
ran 180 s.

Likely cause (unconfirmed): `waitFor` checks its deadline only between predicate calls, and the
predicate `findCurrentFrame` loops over `page.frames()` with Playwright calls that have no timeout
(`locator.count`, `frameElement().isVisible`, attribute reads). A call on a frame of a hidden or
detaching preview tab can wait forever. The leftover tabs from earlier steps (`preview.md`,
`preview-other.md`, the dirty `feature-contract.md`) also show `closeAllEditors` did not leave a
clean window before this step.

## Decisions

1. **Environment first (A).** Give the X server a screen larger than every emulated viewport:
   `xvfb-run --auto-servernum -s "-screen 0 2560x1440x24"` for the `integration`, `stress` and
   `toc-loop` jobs (2560 covers the 2400 px of previewEditing). This is a platform concern (CI rule
   3: "a display server for GUI tests"), not a retry. If the justfile or `scripts/` own the Xvfb
   launch for local Linux runs, they use the same size.
2. **Guard, so the cause cannot come back silently (A).** The harness checks, after every
   `setViewportSize` it makes or once per connected page, that the emulated viewport fits inside the
   real window and screen (CDP `Browser.getWindowForTarget` bounds and `screen.width/height`), and
   fails with both sizes in the message otherwise. A test never clicks a point it cannot reach.
3. **Diagnostics before fixes (A, B, B2, C).** Each failure message names what the host and the page
   held (rule 12): window bounds and the click point in `setEditMode`; a host frame (`index.html`)
   probe in `editToggleState`; window states, focus moves and the page trace in `scenarioPalette`
   as in `scenarioAlertDropdown`.
4. **Focus readiness on every platform (B, B2).** Before a real-input scenario opens a block editor,
   it waits for a state the host and page report: `vscode.window.state.focused` true, the webview is
   the workbench's active element, the content `document.hasFocus()`, no group unlock focus command
   pending (`previewGroupUnlocksSettledForTests`), then `waitForPageSettled` and `waitForTextInput`
   on the editor. `ensureTestWindowFocused()` gets a Linux path that focuses the window and waits for
   `onDidChangeWindowState` to report it, instead of returning at once.
5. **Redo rule only if the host is proved (B2).** If the new diagnostics show the blur is the
   window's late activation (H1), `editorBlurBeforePress` may also accept a window focus gain that
   lands within its windows, with the evidence written in its doc comment. If they show H2, no redo
   is added: a product bug is filed (Decision 8).
6. **Bounded frame lookup (C).** Each Playwright call inside `findCurrentFrame` gets its own timeout,
   or the predicate runs under `bounded()` (`test/shared/hangWatchdog.ts`), so a stuck call fails
   the step in about 10 s with the call named, instead of hanging to the step budget. `closeAllEditors`
   asserts the window has no tabs left after it runs, and says which remain.
7. **Stress list.** Add `palette` (`scenarioPalette`) and `checkbox-toggle` to the stress scenarios
   (`STRESS_SCENARIOS` in `test/integration/realInput/run.ts`, through `test/shared/stressPlan.ts`);
   `toc` and `alert-dropdown` are already there.
8. **Product bug.** If H2 is proved (a focused window, a click inside the preview, and the editor
   closes because the workbench re-focused through `body`), file it as a new inbox item with the
   page trace and the host window states, and report it to the Chief of Staff for the owner. The
   test then waits for the readiness of Decision 4 and stays in place.

## What changes

- `.github/workflows/ci.yml`: the `xvfb-run` lines of `integration` (line 234), `stress` (line 284)
  and `toc-loop` (line 337) pass `-s "-screen 0 2560x1440x24"`.
- `test/build/test_workflows.py`: a test that every `xvfb-run` call of `ci.yml` sets a screen at
  least 2560x1440 (or at least the largest width a real-window test emulates).
- `test/integration/realInput/harness.ts`:
  - a `realWindowBounds(page)` helper (CDP session, `Browser.getWindowForTarget`) and a viewport
    guard (Decision 2), used by a harness `setViewport(page, size)` that every real-window test calls
    instead of `page.setViewportSize`;
  - `editToggleState` adds the host frame probe (`index.html`: `hasFocus`, active element,
    `elementFromPoint` at the click point) and the window bounds;
  - `setEditMode` logs the click point in page coordinates in its failure message;
  - `findCurrentFrame` and `currentPreviewFrame` bound each Playwright call (Decision 6);
  - `closeAllEditors` checks no tab is left.
- The tests that call `page.setViewportSize` (tocWindow, commentContrastWindow, readmeHtmlWindow,
  tableEmptyColumn, untrusted-suite, radioChoice, mystBlocksWindow, reload-suite, previewEditing,
  editToolbarCover, tallBlockScroll): call the harness helper; no size or assertion changes.
- `test/integration/windowFocus.ts`: `ensureTestWindowFocused()` works on Linux too and waits for
  the reported focus; a `waitForWorkbenchFocusSettled(page)` helper for Decision 4.
- `test/integration/realInput/textEditing.ts` `scenarioPalette`: records window states, focus moves
  and the page trace like `scenarioAlertDropdown`; waits for focus readiness, `waitForPageSettled`
  and `waitForTextInput` before the clicks; its failure message carries those diagnostics. Same
  expectations as today.
- `test/integration/realInput/editorWidgets.ts` `scenarioAlertDropdown`: the same focus readiness
  wait before opening the editor.
- `test/shared/editorBlurInterruption.ts`: only under Decision 5 (H1 proved), with its unit tests
  in `test/unit` and the evidence in the doc comment.
- `test/integration/realInput/run.ts` (`STRESS_SCENARIOS`) and `test/shared/stressPlan.ts` (doc and
  unit tests if names are validated there): add `palette` and `checkbox-toggle`.
- `.agents/guidelines/ci.guidelines.md`: rule 13's `toc-loop` paragraph says the toggle flake's
  cause (the screen size) and that the loop stays as a repro tool; rule 3 or 11 names the Xvfb
  screen size requirement in one sentence.
- Requirements: no SwRS change expected (tests and CI only). The `@tests_req` markers stay on their
  scenarios; run `just requirements-update`. If Decision 8 fires, the bug item names the SwRS
  (SwRS-MDOKFSTUDIO-BLOCK-047, commit on leave).

## Out of scope

- Removing, skipping or narrowing any test or assertion.
- Raising any timeout or step budget.
- A retry or redo without a proved host cause.
- Fixing a product bug in this CR (it is filed, Decision 8).
- The Open VSX OIDC failure of run 43567601653 (separate retro item).
- The `wide-table-tab` stress exclusion (already under its own investigation).

## Commits

Scopes per `.agents/guidelines/git-commit-allowed-scopes.md` (`ci` and `test` take no scope):

1. `ci: give xvfb a screen larger than the emulated viewports` (workflow, workflow test, CI guideline).
2. `test: guard emulated viewports and log real window bounds` (harness helper and guard, the test
   files switched to it, `editToggleState` host frame probe).
3. `test: wait for window and webview focus before opening a block editor` (windowFocus, palette,
   alert-dropdown; redo rule only if Decision 5).
4. `test: bound the preview frame lookup and check editors are closed` (C).
5. `test: stress the palette and checkbox-toggle scenarios`.

## Evidence

- Before the fix, on the branch with commits 2 to 4 only (diagnostics, no screen change):
  `gh workflow run ci.yml --ref <branch> -f toc_loop=40` and one heavy run, to record the real window
  bounds (1280 wide expected) and, if it fails, the toggle click point. Written in the PR.
- After the fix:
  - `gh workflow run ci.yml --ref <branch> -f heavy=true`: `integration` and `stress` green.
  - `gh workflow run ci.yml --ref <branch> -f heavy=true -f stress_repeat=60 -f stress_scenarios=toc,palette,alert-dropdown,checkbox-toggle`:
    green (rule 12 proof).
  - `gh workflow run ci.yml --ref <branch> -f toc_loop=40`: green.
- `just check`, `just requirements-update`, `just preflight` pass locally.
- Scenario: the window bounds line in a heavy run log shows 2560x1440 and every emulated viewport
  inside it; a forced viewport larger than the screen (unit or local run) fails with both sizes named.

## Open questions

- User impact, conditional: if the CR proves H2 (in a focused VS Code window, a click in the preview
  makes the workbench re-focus through `body` and the block editor closes right after it opened),
  that is a product bug users can hit. It is filed as a new inbox item and the owner decides whether
  it goes before the v1.9.1 release. Not blocking: the CR can start now.
- No other open question.
