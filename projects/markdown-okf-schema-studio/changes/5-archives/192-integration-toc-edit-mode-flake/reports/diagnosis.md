# 192 — diagnosis (Coder rounds 1-2)

Worktree: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-192`, from origin/main `cb1f2adc`.

## Evidence

| Run | Branch | Failing call | Step time |
|-----|--------|--------------|-----------|
| [40784022530](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40784022530) | CR 173 | `harness.js:265` from `tocWindow.js:168` | `STEP failed: toc (6935 ms)` |
| [40790025503](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40790025503) | CR 187 | `harness.js:265` from `tocWindow.js:168` | no step markers on that branch |

- **Proven**: compiled `out/test/integration/tocWindow.js:168` is
  `await (0, harness_1.setEditMode)(page, false)` in the theme loop, i.e. `tocWindow.ts:160`, the call
  right after `setHostTheme`. Not 169 (`setEditMode(true)`) and not 184. Both runs fail at the same call.
- **Proven**: `harness.js:265` is the `click === maxClicks` throw. The old helper read the mode on a
  current frame four times, and it was never `off`. It clicked three times. After each click it waited 1.5 s
  for a current frame showing `off`.
- **Proven**: the artifacts (`a1/`, `a2/`) hold no toc screenshot, no page trace and no hang dump for
  this step. The scenario writes screenshots only with `STUDIO_TOC_SHOTS`. The old error message held
  no state. **The page side of the failure was never recorded.**
- **Inferred (timing)**: the toc step took 6.9 s. The three attempts cost about 3 × (click + 1.5 s) ≈ 4.7 s.
  That leaves about 2.2 s for opening the preview, closing the sidebar, maximizing and `setHostTheme`. So
  the failure is most likely in the first (cream) iteration. That iteration is the first edit-mode toggle of
  a preview that opened in edit mode, right after a Dark→Light host theme change. Each mode read returned
  quickly, which means no long frame gap: a current frame was available at once each time.

## Code paths that can produce "three clicks, mode never off"

- Toggle: `src/page/features/editMode.ts` `bindButton`. The click handler posts `previewEditModeChanged`,
  then calls `applyEditMode(next)`, then `setState({ editMode })`. `applyEditMode(false)` first closes
  the selection, the label rename, the hover, the frontmatter editor and the block editor. Only after that
  does it set `state.editMode` and `data-sphinx-preview-edit-mode`.
- Host theme change: `hostEvents.onThemeChanged` → `viewState.notifyTheme` posts `themeChanged` and
  queues `refreshPreviewDocument` (deferred while editing). The result goes out as a content patch when
  the shell key matches; edit mode and theme are deliberately not in the key. Otherwise the whole page
  loads again: `runtime.ts` boots `state.editMode` from `vscode.getState().editMode`, else from
  `initialEditMode` = the host's stored choice.
- `previewEditModeChanged` uses the `page-state` gate. A message from an older render (`requestId` ≠
  stage) is dropped silently (`pageMessages.handlePageState` → `reportStaleEdit` does nothing for this
  type). In that case the host keeps the old stored choice.
- `setHostTheme` (test) waits only for the `vscode-light` body class, which VS Code sets itself. It does not
  wait for the theme render the host queued. That render can land during `setEditMode`.

## Ranked causes (none proven: the failing runs recorded no page state)

Round 2 correction: round 1 claimed that a workbench element covering the webview loses a click
silently. That is wrong. Playwright 1.64.1 (`_checkFrameIsHitTarget` in
`node_modules/playwright-core/lib/coreBundle.js`) checks, before every non-forced click, that each
iframe element up the frame chain to the workbench is the hit target at the click point, and retries
until the action timeout if not. A lasting cover gives a click *timeout* ("… intercepts pointer
events"), not a lost click and a 6.9 s step. The causes are re-ranked below.

1. **Inferred. The click reached the toggle, but `applyEditMode(false)` threw before it set the
   attribute.** This would be a product bug. It fits "same result three times", because
   `state.editMode` stays true and every click takes the same failing path, with no re-render between
   the reads. The webview error goes to the webview console, which CI does not capture. The flake
   would come from a transient page state after the theme patch, such as an editor or selection left
   half-closed.
2. **Inferred. The page runtime had not booted (or its boot failed) when the helper clicked.**
   `data-sphinx-preview-edit-mode` is set only at runtime, by `contentPatch.ts` `initializeContent`,
   which runs after `rt.editMode.bindButton()` (`runtime.ts`). No server HTML sets it, and
   `findCurrentFrame` matches on server-rendered attributes only. The old helper did not tell a null
   mode from `on`: four reads of `null` and three clicks on an unbound toggle give exactly the observed
   message. A boot that threw before `initializeContent` would leave it null for good (product bug); a
   slow boot would need about 5 s, which the timing makes less likely.
3. **Inferred. The toggle is not idempotent and the old helper's re-click cancelled a late click.**
   If click 1 was handled after the 1.5 s window, the re-click turned the mode back (off → on), and so
   on. Three late deliveries in a row are unlikely, but the new counter makes it visible (`clicks`
   moves by 2 for one attempt).
4. **Inferred, least likely. The click event was lost between Playwright's hit check and the page:**
   a cover or relayout (editor-group maximize, theme relayout) between the hit-target check and the
   dispatched mouse events, or input routing to the webview's out-of-process iframe dropping the event.
   Three misses in a row need this to repeat for about 5 s.
5. **Inferred, unlikely. The toggle worked, then a render restored edit mode.** This needs a full page
   load with the old `initialEditMode`, with the click's `previewEditModeChanged` dropped as stale and
   the webview state not yet persisted, three times in a row. The timing (no frame gap) argues against
   it. If it happened, it is a product bug: a theme change undoes the user's toggle.

Not supported by the code: a collapsed toolbar hiding the toggle (Playwright would wait for
visibility and fail with a timeout, not with this message); `aria-disabled` (the preview is trusted).

## What the test change does (test-side, `harness.ts` `setEditMode` only)

**This CR is instrumentation plus stress coverage, not a proven fix.** No cause above is proven.
The change makes the next failure name its cause and puts `toc` under stress (CI rule 12); it does
not by itself remove the flake. The backlog item stays open (or gets a follow-up) until a run records
the state. Heavy and stress logs must be grepped for `setEditMode … switched on click #`: a retried
click on a green run is still evidence.

- Before the first click, it waits on state until the current frame's runtime has booted (the edit
  mode attribute is set). A frame whose mode is still null is never clicked, and that attempt is not
  counted (bounded: at most three such waits). This keeps a pre-boot click from being blamed on the
  product (cause 2 then shows as a boot timeout naming the last mode and `webviewReady`).
- Before each click, it reads one state object on the current frame. The object holds `render`
  (requestId@version), `<html>` mode, the toggle's `data-edit-mode`, `aria-pressed`, `aria-disabled`,
  visibility, `pointer-events`, box, the element at the toggle centre in the webview and in the
  workbench (a short, non-fatal read: `unreadable` if the toggle vanished), `activeElement`, and a
  probe. The probe is a capture-phase click counter at `document` for targets inside the toggle, plus
  a window `error` listener. It only records. A counted click proves the click reached the toggle in
  the page, not that the toggle's own listener ran.
- After the click, it reads the outcome on the clicked frame, by state, not by time:
  - the frame was replaced, or the counter did not move: the click is proven lost, and the helper
    retries (3 attempts at most);
  - the counter moved but the mode is not the wanted one: it fails at once (cause 1 or 3, product);
  - the mode switched but the current render later shows the old mode: it fails at once (cause 5,
    product).
- Every failure message carries the before and after state of each attempt. A green run with a
  retried click logs the attempts too.
- The toc scenario is added to the stress plan (CI rule 12). Its stress wrapper closes the sidebar that
  the scenario reopens.

The next failure names the cause. If it is a product cause, the fix belongs in `editMode.ts`
(`applyEditMode`), the page boot (`runtime.ts`), or the theme-render path, not in the test.
