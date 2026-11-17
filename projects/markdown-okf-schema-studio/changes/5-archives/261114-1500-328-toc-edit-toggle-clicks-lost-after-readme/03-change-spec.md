# Change Specification: the edit toggle loses its clicks right after a preview opens (toc, myst-blocks)

Type: test (harness and real-window scenarios; a product fix only if the evidence proves a cause a
user can hit, brought to the owner first). Automatable: the Chief of Staff settled scope, method and
proof with no user impact (02-answers.md, 2026-11-14). Priority P1, batch-04.
Sources: `01-intent.md`, `02-answers.md`, the CR-326 archive
(`.agents/changes/4-archives/261114-0947-326-flaky-real-window-integration-steps/`), the runs in the
intent's table and the v1.9.1 version push (ci.yml run 43590898224, attempt 1, `myst-blocks`).
Code read at `origin/main` `5a61b0c9` (version 1.9.1).

## Goal

1. The cause of the lost edit-toggle clicks is proved by evidence (where the three real clicks went,
   and what moved just before), written in the commit and the PR.
2. It is fixed with a deterministic state check or a test-setup fix (CI guideline rules 9 and 12): no
   sleep, no retry, no raised timeout, no test removed or skipped.
3. If the proof shows a behaviour a real user can hit (a click on the preview right after the
   preview opens, or right after a layout change, is dropped in a focused window), the work stops
   and the finding goes to the owner before a test-only change ships.
4. Proof: a branch heavy run with `integration` green, and the reproducing loop green over at least
   40 rounds.

## What the code shows (new lead, to confirm in the CR)

Only three real-window steps toggle the side bar back open in their cleanup:
`readme-html` (`test/integration/readmeHtmlWindow.ts`), `toc` (`test/integration/tocWindow.ts`)
and `myst-blocks` (`test/integration/mystBlocksWindow.ts`). They run in that order in the trusted
suite (`test/integration/trusted-suite.ts`, `remainingSteps`). Each one:

- opens the side preview first, then runs `workbench.action.closeSidebar`, then
  `workbench.action.toggleMaximizeEditorGroup`, then `setViewport`, then clicks;
- ends with `toggleMaximizeEditorGroup` and `toggleSidebarVisibility`, which OPENS the side bar
  (VS Code focuses the view it opens), whatever the side bar state was before the step.

Every other real-window step closes the side bar BEFORE it opens its preview (checkboxToggle,
radioChoice, findInPreview, editToolbarCover, previewEditing, tallBlockScroll, pasteUrl, ...), and
none reopens it.

So `closeSidebar` after the preview opened is a real layout change only when the step before left
the side bar open. That matches every observation:

| Case | Side bar when the step opens its preview | Result |
|------|------------------------------------------|--------|
| `readme-html` in integration (earlier steps closed the side bar, `comment-title` does not touch it; to confirm) | closed: `closeSidebar` is a no-op | no failure seen |
| `toc` right after `readme-html` (integration, toc-loop with `STUDIO_TOC_AFTER_README_HTML=1`) | open and focused (readme-html's cleanup) | 3 failures, 2 of 40 in the loop |
| `myst-blocks` right after `toc` (v1.9.1 push) | open and focused (toc's cleanup) | 1 failure |
| `toc` alone in toc-loop (run 43576431799) and in stress (60 rounds) | closed: the loop and the stress wrapper run `closeSidebar` after each `toc` | green |

Two mechanisms can turn that layout change into lost clicks; the CR tells them apart:

- L1, input routing: after the side bar closes and the group is maximized, the webview overlay is
  moved and resized; Chromium routes a real mouse event to an out-of-process frame by the
  compositor's hit-test data, which can be stale for a moment after the layout change. The click then
  lands in the workbench or the webview shell (`index.html`) instead of the content frame, while
  `elementFromPoint` (DOM layout) already answers the toggle. That explains `hitIsToggle: true`,
  `workbenchHit: iframe.webview.ready` and a click counter at 0.
- L2, focus: the side bar held the focus; closing it makes the workbench focus the active editor
  group, and the webview takes the focus through `body` (the `window-blur / window-focus active body`
  pairs and the page blur at 497 ms of the failing round). A click during that hand-off is lost.

L1 would also explain why three clicks in a row are lost (the first ones within the same stale
window), L2 less so. Neither is proved yet: the intent's own guess (a group focus or unlock command
landing late) stays a candidate, and `waitForFirstClickReady` (CR-326) already waits for the window
focus and the group unlocks, and did not stop the failure. Note: `myst-blocks` does not call
`waitForFirstClickReady` at all.

## Link with the sibling CR `palette-heading-focus-bounce`

Likely NOT the same cause, so neither CR waits for the other:

- here the real clicks never reach the content document (capture-phase counter 0, no `mousedown`
  in the page); in palette and alert-dropdown the click does reach the page (B2's trace has the
  alert `mousedown`) and the block editor loses the focus about 290 ms later;
- here the failing steps are exactly the ones that follow a side-bar reopen; palette and
  alert-dropdown run with the side bar closed (the realInput `run()` closes it, and the stress `toc`
  wrapper closes it again).

What they share: the workbench focus moving through `body` around a click, and the same diagnostics
and helpers (`test/integration/windowFocus.ts`, `workbenchFocusDump`, the page trace). Both CRs
will likely touch `windowFocus.ts`, so their PRs stack (requirement files and shared helpers
conflict). If this CR's diagnostics show L2 (a focus hand-off through `body` drops input in a focused
window), the finding is passed to the palette CR's Driver: it is then a candidate for that bounce
too.

## Decisions

1. **Reproduce the exact adjacency first.** The toc-loop gets a knob for the steps of a round
   (for example `STUDIO_TOC_LOOP_STEPS=readme-html,toc,myst-blocks`; the current
   `STUDIO_TOC_AFTER_README_HTML=1` becomes the default value of that list), so one dispatch also
   covers the step after `toc`. A control knob runs the same round with `closeSidebar` before each
   step (side bar already closed): if the control is green over 40 rounds while the adjacency loop
   fails, the side-bar lead is confirmed. Rounds and the launch deadline: the deadline is computed
   from rounds and steps per round, as `6ed39735` did for stress, so 40 rounds of three steps fit
   (`MAX_TOC_LOOP`, the `toc-loop` job's step and job timeouts follow).
2. **Diagnostics that say where the click went (rule 12).** `setEditMode`'s probe adds capture-phase
   `pointerdown`/`mousedown`/`click` counters on the workbench document and on the host frame
   (`index.html`), next to the content frame's counter, plus at each attempt: the webview iframe's
   box against its editor group container's box, the side-bar visibility and the focused part. A
   failure then says: the event reached the workbench (L1, routed outside), the shell (L1 or L2), or
   nothing. Each step logs the side-bar state at its start.
3. **Fix by what the proof shows, never by a retry:**
   - side-bar lead confirmed (L1 or L2): the three scenarios close the side bar BEFORE opening the
     preview, like every other real-window step, and leave the window as they found it (read the
     side-bar visibility at the start from the workbench DOM, restore that state, never a blind
     toggle). The maximize stays after the preview opens (it needs the preview group); the first
     click waits for a state that proves the layout landed (the webview iframe box equals its group
     container's box, `waitForFirstClickReady` passed). `myst-blocks` and `readme-html` call
     `waitForFirstClickReady` as `toc` does;
   - another cause (late focus or unlock command, theme restore of the previous step): the matching
     state wait, with the evidence in the doc comment;
   - a host-only cause proved (X server, Chromium routing that no user window can hit): a documented
     redo as CR-326's Decision 5 allows, with the evidence next to the code.
4. **Product question.** If the proof shows a real user can lose a click (the preview opens or the
   layout changes, the user clicks within that window, nothing happens), stop and report to the
   Chief of Staff before shipping the test-only fix (open question below).
5. **Stress list.** `myst-blocks` and `readme-html` join `toc` in the stress scenarios
   (`STRESS_SCENARIOS` in `test/integration/realInput/run.ts`, `test/shared/stressPlan.ts`), each with
   the same side-bar handling as the trusted suite.

## What changes

- `test/integration/tocWindow.ts`, `readmeHtmlWindow.ts`, `mystBlocksWindow.ts`: side-bar handling
  per Decision 3; `waitForFirstClickReady` in all three; same assertions and sizes.
- `test/integration/realInput/harness.ts`: the extra click counters and layout facts in
  `editToggleState` / `setEditMode`; a helper that reads and restores the side-bar visibility; a
  layout-landed wait if Decision 3 needs it.
- `test/integration/windowFocus.ts`: only if the layout wait belongs in `waitForFirstClickReady`
  (shared with the palette CR: stack).
- `test/integration/realInput/run.ts` (`runTocLoop`, `STRESS_SCENARIOS`), `test/shared/tocLoop.ts`
  (step list and control knobs, validated, with unit tests in `test/unit`), `test/shared/stressPlan.ts`.
- `justfile` `ci-toc-loop` and `.github/workflows/ci.yml` `toc-loop`: pass the new knobs (inputs
  validated as today), deadline from rounds and steps; `test/build/test_workflows.py` if it checks
  the job's inputs.
- `.agents/guidelines/ci.guidelines.md`: the `toc-loop` paragraph (rule 13) names the cause and the
  new knobs.
- Requirements: no SwRS change expected (tests only); the `@tests_req` markers stay on their
  scenarios; `just requirements-update`. SwRS-MDOKFSTUDIO-BLOCK-047 is not involved unless the proof
  shows an editor commit on leave.

## Out of scope

- Removing, skipping or narrowing a test or assertion; raising a timeout or step budget.
- A retry without a proved host cause.
- The palette and alert-dropdown focus bounce (sibling CR), except passing on an L2 finding.
- A product change, unless the owner decides it (open question).

## Commits

Scopes per `.agents/guidelines/git-commit-allowed-scopes.md` (`ci` and `test` take no scope):

1. `test: say where a lost edit-toggle click went` (counters, layout facts, side-bar state log).
2. `ci: loop the steps after readme-html with a side-bar control` (knobs, deadline, workflow, guideline).
3. `test: close the side bar before the preview opens in the readme, toc and myst steps` (or the fix
   the proof points to).
4. `test: stress the readme-html and myst-blocks steps`.

## Evidence

- Before the fix (commits 1 and 2 only): `gh workflow run ci.yml --ref <branch> -f toc_loop=40`
  with the adjacency steps, and once with the control; the failing rounds' counters and timelines are
  quoted in the PR.
- After the fix: `gh workflow run ci.yml --ref <branch> -f heavy=true` (`integration` and `stress`
  green); the adjacency loop green over 40 rounds;
  `-f heavy=true -f stress_repeat=60 -f stress_scenarios=readme-html,toc,myst-blocks` green.
- `just check`, `just requirements-update`, `just preflight` pass locally.

## Open questions

- User impact, conditional: if the proof shows that VS Code drops a real click on a webview for a
  moment after a layout change or a focus hand-off in a focused window (L1 or L2 outside the test
  host), a user who closes the side bar or opens the preview and clicks the edit toggle right away
  sees nothing happen. Studio cannot fix that inside VS Code. The owner decides: document it and file
  it upstream, or look for a mitigation in the page. Not blocking: the CR starts now and stops at that
  point only if the proof gets there.
