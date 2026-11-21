# CR-454 diagnosis: round 2 frontmatter-title loses all 3 edit-toggle clicks after paste-url and drop-files

## Reproduction

Heavy CI dispatch on the PR head (`gh workflow run ci.yml --ref <branch> -f heavy=true`), default
stress: `just ci-stress` = 11 rounds x 21 scenarios. Failed 2 of 2 (runs 44899492187 and its rerun) at
the same place. Narrow, cheaper repro to dispatch (needs the stress `scenarios` input, as run
44899494477 used):
`STUDIO_STRESS_SCENARIOS=paste-url,frontmatter-rename,frontmatter-title STUDIO_STRESS_REPEAT=6`
(expected red in round 2). Controls: `drop-files,frontmatter-rename,frontmatter-title` and
`checkbox-toggle,frontmatter-rename,frontmatter-title` (the latter expected green: it is main's order).

## What the logs prove (work/ci-44899492187.log and -b.log)

1. Rounds are identical up to the failure: round 1 passes all 21; round 2 `frontmatter-rename` passes
   but takes 7667 ms (b: 7230 ms) against 3662 ms (b: 3010 ms) in round 1; round 2 `frontmatter-title`
   fails. The only thing between round 1's start and round 2's start that differs from main's stress
   (which ended each round with checkbox-toggle and passes) is the tail `paste-url`, `drop-files`.
   The doubled rename time is the lost-click retries of `setEditMode` (1.5 s wait per lost click),
   so the first scenario after drop-files is already hit and recovers, the second does not.
2. The failure is the same in both runs, byte for byte in the click state: mode off, toggle visible,
   `pointerEvents auto`, `hit: svg`, `hitIsToggle: true`, click point (1283,99) three times.
   Routing: `content [pointerdown 0 ...] host [0 ...] workbench [pointerdown 4 -> 5 -> 6 -> 7]`. So
   each Playwright click (CDP `Input.dispatchMouseEvent`) is delivered to the workbench main frame
   although `elementFromPoint` says the point is on the webview iframe (`workbenchHit:
   iframe.webview.ready`). A click that lands on an iframe normally never reaches the parent
   document, and here the content frame and its host frame get nothing. That is a routing mismatch
   between the page's layout (renderer) and the browser-side hit test of the input router, not a page
   state problem (no errors, render 1@1, toggle enabled, no tab or side bar leftover: layout says
   side bar hidden, iframe and group boxes equal; tabs: only smoke.md preview).
3. The layout in the failure is 1400 wide (iframe 724..1395), the size the stress run set on the
   main page (`run.ts` `setViewport(page, 1400x900)`). The scenario that ran before in the same
   window, `drop-files` (and `paste-url`), connects a second CDP client and emulates a different
   viewport: `setViewport(page, { width: 1200, height: 800 })` on its own connection, then
   `browser.close()` in its `finally` (pasteUrl.test.ts line 101, dropFiles.test.ts line 95).
   `checkbox-toggle` also opens its own connection but sets 1400x900, the size the main page already
   has, so main's stress never exercised a size change by a second client. All other stress
   scenarios use the `page` of the run.
4. Ruled out: leftover editor tab or dirty document (both closed: after cleanup `active editor tab:
   none`, tabs read `smoke.md` only), edit mode left on (mode is `off`, as wanted), focus (the
   focus dump shows the webview focused and the window focused; the host frame `hasFocus=false` is
   the normal state of the host frame in earlier passes of this dump), side bar (hidden).
   The `CodeWindow: failed to load (code -3)` lines are noise (they occur in every round, before
   passing scenarios too).

## Cause (best supported, mechanism not reproduced)

`paste-url` and `drop-files` leave the shared VS Code window with a viewport emulation that was set
and then dropped by a second CDP client (1200x800, then client closed), while the run's own client
still believes 1400x900 (and the renderer lays out at 1400). Emulation is per target, not per
client: when client B disconnects, Chromium clears the device-metrics override that B applied
(replacing the one A applied), so the browser-side compositor/hit-test data no longer matches the
renderer's layout. Clicks are then routed by the input router to the main frame instead of the
out-of-process webview iframe. The loss of 1-2 clicks in the next scenario and of all 3 in the
second one matches a mismatch that is re-synchronised only by a later layout event.

I could not reproduce the mechanism locally: Chromium cannot be spawned from this session
(`spawn UNKNOWN`, also for `chrome.exe --version`), so `emulation-probe.cjs` in this folder
(two CDP clients on one page with an out-of-process iframe, click routing counted before, during
and after the second client) was written but never ran. Treat the mechanism as a hypothesis the
experiment below must confirm; the log facts in 1 to 4 are certain.

Rejected alternative: the leftover `colorTheme` and stored-choice changes of paste-url/drop-files
(light theme then `originalTheme`, `previewThemeMode` cream then current). They explain a late
re-render, but a re-render does not make the click arrive at the workbench instead of the webview,
the toggle state is stable over 4.5 s, and the `setEditMode` wait for the theme is the older
CR 328 fix of a different symptom (click lost with the side bar open). It stays the second suspect
if the viewport fix does not turn the runs green.

## Place and minimal fix (test code only)

- `test/integration/pasteUrl.test.ts` and `test/integration/dropFiles.test.ts`: both set
  `setViewport(page, { width: 1200, height: 800 })`. Preferred fix: use the run's size,
  `{ width: 1400, height: 900 }`, as `checkbox-toggle` does, so the second client never changes the
  emulation of the shared window (the scenarios work on live bounding boxes; the paste-url and
  drop-files screenshots only change size). Then nothing is left to clean.
- Equivalent in the stress loop, if the sizes must stay: in `runStress`
  (`test/integration/realInput/run.ts`), after each scenario that opens its own connection
  (`checkbox-toggle`, `paste-url`, `drop-files`), re-apply the run's emulation on the main page,
  `await setViewport(page, { width: 1400, height: 900 })`, and wait until the frame reports it
  (`window.innerWidth` of the workbench is 1400). A cleanup of the shared window, never a retry.
- Do not touch `setEditMode`, the stress lists or the plan (ruled out by the card).

## Proof to run after the fix

Dispatch the heavy CI on the fixed head: default stress (11 rounds, 21 scenarios), plus the narrow
repro above with `STUDIO_STRESS_REPEAT=20`. Before the fix it fails in round 2 (2 of 2); after it,
round 2 and all later `frontmatter-rename`/`frontmatter-title` must pass, with
`frontmatter-rename` back near 3 s in rounds 2 and later (the doubled time is the cheap signal of a
lost click). If it still fails with the same routing line (`content 0`, `workbench` rising), the
viewport premise is wrong: test the premise by running `paste-url` alone before `frontmatter-title`
with the viewport already 1400x900, then look at the theme suspect.
