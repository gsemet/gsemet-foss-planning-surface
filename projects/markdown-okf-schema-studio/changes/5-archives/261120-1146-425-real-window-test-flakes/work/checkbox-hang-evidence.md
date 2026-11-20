# checkbox-toggle hang: what the two dumps prove (step B.1)

Downloaded 2026-11-20, both artifacts present (not expired):

- `work/artifacts-44651927198/e2e/hang-dumps/20261120T011906047Z-checkbox-toggle/` (run 44651927198,
  attempt 1, `main` 24c9eef)
- `work/artifacts-44694304978/e2e/hang-dumps/20261120T072718222Z-checkbox-toggle/` (run 44694304978,
  attempt 1, CR-350 branch 412ca69)
- Failed logs: `work/ci-44651927198.log`, `work/ci-44694304978.log` (attempt 1; run 44694304978 was
  re-run and its attempt 2 is green, so `--log-failed` without `--attempt 1` returns nothing).

Each dump holds: `summary.json`, `heartbeat.json`, `host-state.json`, `cdp-targets.json`,
`dump-errors.txt` ("none"), `ps-forest.txt`, `ps-vscode.txt`, VS Code log tails under `logs/`, and one
screenshot `screenshot-cdp-1.png`. Both dumps are the same in every point below.

## Timeline (from the logs)

| | run 44651927198 | run 44694304978 |
| --- | --- | --- |
| `stock-coexistence` done | 01:16:06.117 | 07:24:18.282 |
| `checkbox-toggle` start | 01:16:06.120 (3 ms later) | 07:24:18.283 (1 ms later) |
| marker "waiting for the first checkbox render" | 01:16:06.569 (+449 ms) | 07:24:18.720 (+437 ms) |
| last heartbeat | 01:19:03.741 | 07:27:15.680 |
| dump | 01:19:06.047 | 07:27:18.222 |

No line at all is logged by the step between its start and the timeout: no `Timed out waiting for ...`.

## What the dumps prove

1. **The test process was alive, not busy.** The heartbeat (`heartbeat.json`, pid 4801 / 4836, the
   process the dump names) was written 2.3 s and 2.5 s before the dump, i.e. every 5 s through the
   whole 180 s. The extension host's event loop ran; the step was awaiting a promise that never settled.
2. **The step hung inside its `try`, after the marker, in `currentPreviewFrame` (local copy) or its
   failure path.** The `finally` of `run()` (`checkboxToggle.test.ts:230-236`) starts with
   `disposeActivePreviewForTests()` (`manager.disposeAll(true)`), then closes `tasks.md`. In both
   screenshots and in `host-state.json` the `Studio · tasks.md` tab is still open and active, and
   `tasks.md` is still open in group 1: the `finally` never ran. After the marker, `waitForRender`
   (line 152) has a synchronous predicate and a 10 s deadline: it returns or throws within 10 s. So the
   awaited promise that never settled is a Playwright call of the local `currentPreviewFrame`
   (lines 39-65: `locator.count`, `frame.frameElement`, `isVisible`, `getAttribute`, none bounded), or,
   if its `waitFor` timed out after 10 s, a call of the failure path `windowFocusReport(page)`
   (`windowFocus.ts:156`, an unbounded `frame.evaluate` per frame and `page.evaluate`). The dumps do not
   tell which of the two.
3. **The preview rendered, and is visible.** Both screenshots (`screenshot-cdp-1.png` of each dump)
   show the Studio preview of `tasks.md` in group 2, fully rendered: the heading, the two task
   checkboxes (unchecked, checked), the table with its two checkbox cells, the toolbar. The render the
   step waits for exists (at dump time at least).
4. **Only one webview frame is alive at dump time.** `cdp-targets.json`: one `page` (the workbench,
   title "Studio · tasks.md"), exactly one `iframe` target (`vscode-webview://14b60.../index.html`,
   resp. `0tem6.../index.html`, extension `GaetanSemet.markdown-okf-schema-studio`), three webview
   `service_worker` targets (three distinct webview origins were created in this window session; two
   of them no longer have a frame), two workers. No leftover Studio or stock preview webview remains.
5. **Window and tabs** (`host-state.json`): window `focused: true`, `active: false`; group 1 (inactive):
   `tasks.md` (active), `feature-contract.md (dirty)`; group 2 (active): `preview.md`,
   `preview-other.md`, `Studio · tasks.md` (active). The screenshots show `preview.md` and
   `preview-other.md` as text-editor tabs (file icon; `preview-other.md` in italics, a preview tab), not
   webviews. `activeTextEditor: null`, one visible text editor (`tasks.md`).
6. **The step is the first CDP connection after `stock-coexistence` disposed its webviews.**
   `stock-coexistence`'s `finally` closes the MyST editor tabs and the stock preview tabs, then calls
   `disposeActivePreviewForTests()` (`stockCoexistence.test.ts:256-272`); `checkbox-toggle` starts 1-3 ms
   later and its first action is `chromium.connectOverCDP` (line 113), a new Playwright connection that
   attaches to the frame tree while those webviews are being torn down. None of the steps before it
   in the trusted suite (`preview-smoke`, `project-features`, `hostile-html`, `stock-coexistence`)
   connects over CDP.

## What they do not prove

- Which Playwright call never settled, and on which frame: the dump lists CDP targets from the
  DevTools `/json` endpoint, not the frames of the step's own Playwright connection (`page.frames()`),
  and it holds no stack of the pending call.
- The host's preview state at the hang (phase, version, request id of the active preview): the dump's
  `host-state.json` has no preview field. So whether the frame lookup was matching nothing (version or
  request id mismatch) or blocked on its first call is not shown.
- The frame tree in the first seconds of the step: by dump time (180 s later) the teardown is over.
- VS Code's own logs do not name the hang: in run 44651927198, `renderer.log`, `exthost.log` and
  `main.log` (tails of 300 lines) hold nothing after 01:16:06.422 but D-Bus noise (the last lines are
  the extension's configuration-scope warnings of the new preview). Run 44694304978's logs were not
  read line by line.

## Candidates of B.3 against the evidence

| Candidate | Verdict |
| --- | --- |
| A Studio webview that never finishes loading (product bug) | **Contradicted** at dump time: the screenshot shows the preview fully rendered and visible, and the only webview iframe is this preview's. (It cannot rule out a load that finished late, but a late load would not keep an already-pending Playwright call blocked forever unless that call targeted a frame that went away.) |
| A leftover preview frame from `stock-coexistence` or earlier steps still in the window, touched by the scan | **Contradicted as a lasting leftover**: no second webview target at dump time; the leftover tabs are text tabs. **Supported in its transient form**: the step connects 1-3 ms after `stock-coexistence` disposed its webviews, so the new connection's `page.frames()` can hold a frame that is detaching; an unbounded `locator.count` / `frameElement` / `evaluate` on such a frame can wait forever for an execution context that never comes. Three service workers for one live iframe show that two webviews existed and went away. Not proven: the dumps cannot show the frame list of the connection. |
| The local unbounded copy of the frame lookup (lead of B) | **Supported**: the hang is in `currentPreviewFrame` or its failure report (point 2), both unbounded; the harness's bounded `findCurrentFrame` would have failed in about 10 s naming the call and the frame URL. This is the diagnostic (B.2), not a cause by itself. |
| Suite order (state left by earlier steps) | **Supported**: same predecessor in both runs, start within 3 ms of its teardown; the `stress` job (no `stock-coexistence` before it) is green. |
| Event loop blocked / host busy | **Contradicted**: the heartbeat ran to the end. |

## What would prove it next

B.2's bounded lookup (with the frame URL in the message) and a `markProgress` between `waitForRender`
and `currentPreviewFrame`, plus bounding `windowFocusReport`'s per-frame `evaluate` (or using the
harness `currentPreviewFrame`, whose failure dump is bounded): the next failure then names the call
and the frame. A deterministic fix consistent with the supported candidate: the step that disposes
webviews waits until they are gone before it ends (for example the harness `closeAllEditors`, which
awaits `previewGroupUnlocksSettledForTests()` and asserts no tab is left), and the frame scan skips
frames whose document id is not the active preview's (the harness `findCurrentFrame` checks
`data-sphinx-preview-document-id`, the local copy does not).
