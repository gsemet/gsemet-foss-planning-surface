# Change Specification: find why a click on a palette list option is lost and closes the block editor

Type: test and ci first (diagnostics, harness, a reproducing loop). A product fix only if the
evidence proves a cause a user can hit, and then only after the owner has chosen it (02-answers.md).
Automatable up to the cause: the owner picked the item for batch-04 and the Chief of Staff decided
the method with no user impact (02-answers.md).
Sources: `01-intent.md`, `02-answers.md`, `intake/request.md`, the CR-326 archive
(`.agents/changes/4-archives/261114-0947-326-flaky-real-window-integration-steps/`, its spec
sections B and B2, PR 398), the sibling CR
`.agents/changes/1-inbox/toc-edit-toggle-clicks-lost-after-readme-html/`, and
`gh run view <id> --log-failed` of runs 43582068953 (attempt 1) and 43576429177. Code read at
`origin/main` `5a61b0c9` (version 1.9.1).

## Goal

The owner's words: « Faisons les 3 CR. Uniquement pose moi les questions impactantes ».

1. The cause of the lost click and the block editor that closes right after it is proved by
   evidence and written in the commit and the PR: either the test host (how the harness or the
   CI display delivers the click) or VS Code / Chromium moving the focus in a focused window,
   which a user could hit.
2. A host cause is fixed in the harness with a state the host or the page reports (CI guideline
   rules 9 and 12), or, only if nothing reportable exists, a documented host-only redo per CR-326's
   Decision 5. No sleep, no raised timeout, no test removed or skipped.
3. A product cause stops the CR before shipping: the fix is the owner's choice (Open questions).
4. Proof: `palette` and `alert-dropdown` green over 60 stress rounds, and a branch heavy run green.

## What the logs prove

| Run, attempt | Commit | Job, round | Scenario | Lost click |
|--------------|--------|------------|----------|------------|
| 43582068953, 1 | `main` `0941cc09` (after PR 398) | stress, round 10/20 | `palette` | the `[data-edit-option='2']` option of the Heading list |
| 43576429177, 1 | CR-326 branch `17454607` | integration | `alert-dropdown` | the Warning option of the type list |
| 43416264245, 1 | `main` `fd8adb9e` | stress, round 15/20 | `alert-dropdown` | the Warning option (CR-326 B2) |
| 43536948441, 1 | CR-323 branch `f12ba53b` | integration | `palette` | the `[data-edit-option='2']` option (CR-326 B) |

The newest failure (43582068953) is the clearest one, because it ran with every readiness wait of
PR 398. Page trace (content page clock; `pageTraceStart` 217 ms on the scenario clock):

- 240 ms: mousedown on the edit toggle, page focus. 354: mousedown on the paragraph, block editor
  opened, then focused at 374. 470: mousedown on Bold (prevented). 620: mousedown on Heading
  (prevented). The Heading list opened (the wait for it passed).
- The click on the option left NO mousedown in the content page. The trace records every mousedown
  that reaches the page (`src/page/pageDiagnostics.ts`, a `window` listener; the option's own
  handler `keepFocus` only prevents the default, it does not stop the event).
- 908 ms: block editor blur `related=none commit active=body pageFocus=true`, 911: page blur
  `pageFocus=false`, 978: content patch and editor closed (commit on leave,
  SwRS-MDOKFSTUDIO-BLOCK-047). 908 is 288 ms after the Heading press: the "about 290 ms" of the
  intent.
- `windowStates: []`: VS Code reported no window focus change during the whole scenario (the window
  was focused from `waitForWorkbenchFocusSettled` to the end). `focusMoves`: no focus command of the
  extension since 3.5 s before the scenario.
- Workbench focus moves at the blur: `window-focus active body`, `window-blur active
  iframe.webview.ready`, `focusin iframe.webview.ready` (twice), `window-focus active
  iframe.webview.ready`. The webview host frame (`index.html`): `window-focus active body` then
  `window-blur active body` 5 ms later.
- End state: the workbench's active element is the webview `<iframe>` and its document has the
  focus, yet the host frame `index.html` reports `hasFocus=false`, active element `body`, and the
  content page's last focus event is the blur.

`alert-dropdown` (43576429177) shows the same sequence: the alert button press reached the page
(470 ms, prevented), the Warning click left no mousedown, then a blur `related=none commit
active=body pageFocus=true` at 669 ms and a page blur at 671.

What this settles:

- CR-326's H1 (the window is not OS-focused yet and the first click activates it late) does not
  explain the newest failure: the window stayed focused, the readiness waits passed, and three
  real clicks reached the page before the fourth one was lost.
- In all four runs the lost click is on an option of a list that a toolbar button has just opened,
  never on the toolbar button, the paragraph or the edit toggle.
- The click never reaches the content page. The focus then leaves the content page and comes back
  to the webview `<iframe>` in the workbench, but not into the host frame or the content page. This
  is what happens when a mouse press lands in the workbench document over the iframe instead of
  going to the webview's own process.

What the logs do not prove: where the press landed (the workbench document, the host frame, or
nowhere), when Playwright sent it relative to the list's appearance, and whether a real mouse can
hit the same thing.

## Shared cause with the sibling CR (lost edit-toggle clicks)

The two are likely to share a cause. Both show the same thing:

- real CDP mouse clicks over the webview that the content page never receives (toc: click count 0
  with `hitIsToggle: true` and `workbenchHit: iframe.webview.ready`; palette: no mousedown for the
  option);
- a content page blur around the click while VS Code reports the window focused;
- the same end state: the workbench's active element is the webview `<iframe>`, but the host frame
  `index.html` has `hasFocus=false` and active element `body`;
- the same `window-blur / window-focus active body` pairs in the workbench focus moves.

They differ in timing. In toc all three clicks right after a preview opens are lost (the state lasts
seconds). In palette one click is lost about 150 to 300 ms after a list opens, after three clicks
that went through. A shared mechanism, for example the press being routed to the workbench and not
to the webview's process while the webview's frame is being created or changes, would explain both.
Nothing proves it yet.

Recommendation (no user impact, for the Chief of Staff): run the two CRs in sequence, with the
sibling first. Its loop reproduces more often (2 of 40 `toc-loop` rounds, against about 1 in 80
stress rounds for palette and alert-dropdown). The landing probe of Decision 1 is the same code for
both and is written once, in whichever CR runs first. This CR then checks whether the sibling's
cause and fix also explain `palette` and `alert-dropdown`, and adds what is specific to them. If
the two run in parallel, they share the probe through the stack (stacked-prs guideline), not as
two copies.

## Hypotheses (the CR tells them apart before choosing a fix)

- H2, product (VS Code or Chromium): in a focused window, a press over the webview goes to the
  workbench, which focuses the webview `<iframe>` element and blurs the content page. A user's
  click on a list option would then close the block editor and lose the choice.
- H3, host (synthesized input on CI): the press is a CDP `Input.dispatchMouseEvent` sent by
  Playwright on the workbench page. It has no hover moves before it and arrives right after the
  list appears, on Xvfb with no GPU and no window manager. Chromium's routing of that event to
  the webview's out-of-process frame can then fall back to the workbench. A real mouse arrives
  after hover moves, on a composited display, and may never hit this.
- Lead to test, not a hypothesis yet: the list opens with an opacity and translate transition
  (`propertiesStyles.ts`, `data-sphinx-preview-motion="on"` after the first press). A click during a
  compositor animation inside the webview frame may be where the routing goes wrong. The toc case
  has no such transition, so this lead alone would not explain both CRs.

## Decisions

1. **Landing probe (shared with the sibling).** For the duration of a real-window scenario, the
   harness installs over CDP capture-phase `pointerdown` / `mousedown` / `focusin` recorders in the
   workbench document and in each webview host frame (`index.html`). Each record holds the time, the
   target and the client point. These read-only recorders never focus or click anything (same rule
   as `test/shared/workbenchFocusDump.ts`). A failure message then says where the lost press landed:
   the workbench (on which element), the host frame, or nowhere.
2. **Click timing.** `scenarioPalette` and `scenarioAlertDropdown` get a step mark right before
   and right after each click on a list option, and record the list's appearance time from the
   page (the menu's insertion, and its `transitionend` when motion is on). That puts the press, the
   list's appearance and the blur on one clock.
3. **A reproducing loop.** Reuse the stress job with
   `stress_scenarios=palette,alert-dropdown` and a high `stress_repeat`, or widen the sibling's
   loop to these two scenarios if the sibling CR does so. No new CI job if the stress inputs are
   enough (CI guideline rule 13). Run it first with the probe and no fix.
4. **Discriminating runs, after the first failure with the probe.**
   - The press landed in the workbench or the host frame with the window focused: run the same loop
     with the clicks sent as real hover-then-press sequences (a `mouse.move` to the point, a wait
     for the page to report the `pointerover` / `mouseover` on the option, then the press). This
     waits on a page event, not a delay. If the failure stops, the cause is H3's synthesized
     input. If it does not, H2 stays open.
   - A run with `prefers-reduced-motion: reduce` emulated (CDP `Emulation.setEmulatedMedia`) tests
     the transition lead. This is a diagnostic only: the tests keep running with motion on.
   - A local real-window run of the same loop on macOS (a composited display with a window manager)
     helps decide on a user impact: if it never fails over 60 rounds while CI fails, that points
     to the host.
5. **Host cause (H3 proved).** The harness fix is the readiness the evidence names, for example
   the hover-then-press click in `test/integration/realInput/harness.ts` for options of a list that
   has just opened, or a wait for the list's appearance to finish (`transitionend`, or no running
   animation reported by the page). The rule is written in the harness doc comment with the run
   ids. A redo in `test/shared/editorBlurInterruption.ts` comes only if no reportable state exists,
   per CR-326's Decision 5, with the evidence in its doc comment and unit tests.
6. **Product cause (H2 proved).** Stop before shipping. File the evidence (traces, run ids, the
   landing probe output, a local manual repro if one exists) in this CR's `work/`, and bring the
   choice of fix to the owner through the Chief of Staff. The diagnostic commits can ship on their
   own.
7. **Shared cause with the sibling.** If the sibling's fix is the same mechanism, this CR takes it
   as a dependency (stacked on the sibling's PR) and only adds the palette and alert-dropdown proof
   and anything specific to them.

## What changes (expected; the final list depends on the proved cause)

- `test/integration/windowFocus.ts` or a new `test/shared/inputLandingProbe.ts` (pure formatter,
  unit-tested in `test/build` or `test/unit`) plus its CDP installer in the integration layer: the
  landing probe (Decision 1). It is reported by `windowFocusReport` and `workbenchFocusDump`.
- `test/integration/realInput/textEditing.ts` (`scenarioPalette`) and
  `test/integration/realInput/editorWidgets.ts` (`scenarioAlertDropdown`): step marks around the
  option click and the list's appearance time (Decision 2). Same expectations, same timeouts.
- `test/integration/realInput/harness.ts`: the click helper of Decision 5 if H3 is proved.
- `test/shared/editorBlurInterruption.ts` and its unit tests: only under Decision 5's fallback.
- `.agents/guidelines/ci.guidelines.md`: one sentence naming the cause and the click rule, if the
  harness changes how real-window tests click.
- Requirements: no SwRS change for a host cause. `@tests_req` markers stay on their scenarios.
  Run `just requirements-update`. A product cause touches SwRS-MDOKFSTUDIO-BLOCK-047 (commit on
  leave) and possibly the palette SwRS of the list options. That change waits for the owner's
  choice.
- `src/`: untouched unless the owner chooses a product fix.

## Out of scope

- Removing, skipping or narrowing a test or an assertion. Raising a timeout or a step budget.
- A retry or redo without a proved host cause.
- Turning motion off in the tests as the fix (Decision 4 uses it only as a diagnostic).
- The sibling's own scope (edit-toggle clicks after a preview opens), except the shared probe.
- Cursor compatibility (the third batch-04 item).

## Commits

Scopes per `.agents/guidelines/git-commit-allowed-scopes.md` (`test` and `ci` take no scope):

1. `test: record where a real press lands in the workbench and the webview host frame` (unless it
   already landed through the sibling CR).
2. `test: mark the palette and alert-dropdown option clicks and the list appearance`.
3. The fix commit, named after the proved cause (for example `test: hover a just-opened list
   option before pressing it`), or nothing more if the product route applies.

## Evidence

- Before the fix: `gh workflow run ci.yml --ref <branch> -f heavy=true -f stress_repeat=60 -f
  stress_scenarios=palette,alert-dropdown`, repeated until it fails at least once with the probe.
  The PR quotes the failing round's landing records and timing.
- The discriminating runs of Decision 4 and their result, in the PR.
- After the fix:
  - `gh workflow run ci.yml --ref <branch> -f heavy=true -f stress_repeat=60 -f
    stress_scenarios=palette,alert-dropdown`: green.
  - `gh workflow run ci.yml --ref <branch> -f heavy=true`: integration and stress green.
- `just check`, `just requirements-update` and `just preflight` pass locally.
- If no failure reproduces over three 60-round loops with the probe in place, the CR ships the
  diagnostics only, says so in the PR, and stays open in the inbox as the probe's follow-up. It does
  not claim a fix.

## Open questions

- User impact, conditional (only if H2 is proved): a user's click on a list option (Heading level,
  callout type) would close the block editor and lose the choice. The owner chooses the fix before
  the CR ships. Possible routes:
  - (a) keep the block editor open when the focus leaves the content page and comes straight back
    to the same webview `<iframe>`. This changes SwRS-MDOKFSTUDIO-BLOCK-047, so a real leave still
    commits but a bounce no longer does.
  - (b) report the bug upstream to VS Code or Chromium and accept the behaviour until it is fixed
    there.
  - (c) another route the evidence suggests.
  Not blocking: the diagnostic work starts now.
- No other open question with a user impact. The order of the two CRs (sibling first) is the Chief
  of Staff's call.
