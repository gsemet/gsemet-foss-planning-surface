# Change Specification: flaky real-window test realinput-t45, "only the delimiter cell of the first column centred"

## Goal

The real-window scenario RI-T45 (`scenarioTableInsertFromSlash`, fixture `realinput-t45`) failed
once in the heavy CI of batch-06 stack #440 at `2bea4c6` (run 44731534776, job `integration`) and
passed on re-run. The CR finds why, fixes it at its cause and proves the fix by repetition (CI
guidelines, rule 12). The owner decided (02-answers.md, t45-Q1): when the cause is not found, the CR
ships what it proved, plus traces in the CI log that explain the next failure. No automatic retry,
no quarantine, no raised timeout.

Origin: verbal (a CI run, no tracker issue).

## What the failing run shows

Log: `projects/markdown-okf-schema-studio/changes/5-archives/261120-1305-430-myst-numref-captionless-figure/work/ci-44731534776.log`
in the planning surface (lines 838 to 990 once the `dbus/` lines are filtered out).

- The failing wait is the last `expectState` before the save
  (`test/integration/realInput/tableInsertSlash.ts`, line 100): `Timed out waiting for only the
  delimiter cell of the first column centred. Editor state: undefined`. Every earlier wait of the
  scenario passed: the 3 x 2 table was inserted, the caret was after `Column 1`, the slash menu
  listed Column alignment first, the align popover showed its Center option, and the `/align`
  query was removed. The only action between the last passing wait and the failing one is the
  press on the Center option:
  `withCurrentFrame(page, (frame) => frame.locator("[data-edit-popover=\"align\"] [data-edit-option=\"center\"]").click())`.
- `Editor state: undefined` is read once more after the 10 s wait. It is not a wrong value: the
  text box or the current frame was gone. `editorState` returns undefined when
  `findCurrentFrame` (`test/integration/realInput/harness.ts`) finds no frame whose
  `data-sphinx-preview-document-version` and `data-sphinx-preview-request-id` equal the host's last
  render request (`getActivePreviewForTests()`), or when the frame has no
  `[data-sphinx-preview-block-editor] textarea`.
- The workbench focus dump at the failing step (read over CDP) shows, about 10 s before the
  failure, that is at the moment of the Center press:

  ```text
  -10068 ms window-focus active body
  -10068 ms window-blur active iframe.webview.ready
  -10068 ms focusin iframe.webview.ready
  -10068 ms focusin iframe.webview.ready
  -10068 ms window-focus active iframe.webview.ready
  ```

  The workbench document took the focus (`window-focus active body`) and then put it on the
  webview's iframe element (`focusin iframe.webview.ready`): the press reached the workbench
  document. The earlier click of the scenario on "Second paragraph." (at -10942 ms) shows only
  `window-blur active iframe.webview.ready`, with no `focusin` in the workbench. The webview host
  frame (outer `index.html`) shows `window-focus` then `window-blur` at -10063 ms, its document
  `hasFocus=false`.
- After the cleanup, the dump shows `focusout iframe.webview.ready` at -1532 ms and an empty editor
  group: that is the scenario's own cleanup (`withDocument` closes all editors), not a cause.
- What the log does not hold: the page's editor trace (`window.__studioDiagnostics.trace()`, see
  `src/page/modules/editorTrace.ts`), the host's render request and document version, the source
  buffer, and where the press landed (`readLandingSummary`). The trace would name what closed the
  editor (`block editor blur related=... commit`, `content patch request a -> b`, `mousedown ...
  prevented=...`). RI-T45 prints none of them.

## Likely causes the CR must prove or rule out

### C1 (lead): the Center press routed to the workbench, the block editor committed on the blur

RI-T45 presses the option of a list that has just opened without hovering it first. CI guidelines
rule 12 ("Real-window clicks on a just-opened list option hover first") and the comment of
`clickListOption` (`test/integration/realInput/clickRouting.ts`) describe this exact failure (CI
stress run 43608210974, CR 330, commit `fbd00676`): a synthesized press with no preceding hover can
be routed to the workbench instead of the webview process, it lands on `iframe.webview.ready` in the
workbench document, the webview sees no mousedown, the text box loses the focus with no related
target, and the block editor commits (`blockSourceEditor.ts`, the text box's `blur` listener:
`traceBlur("commit")` then `blockEditor.saveBlockEdit()`, SwRS-MDOKFSTUDIO-BLOCK-047). The final
save closes the editor, the host renders the block again, and from then on the frame has no text
box: `Editor state: undefined` for the whole wait. The focus moves above match that signature.

The two other list-option presses of the real-input suite already use `clickListOption`
(`editorWidgets.ts` line 309, alert type; `textEditing.ts` line 716, heading level); RI-T45 does
not.

Proof the CR brings: a failure of RI-T45 under the traces below whose page editor trace shows
`block editor blur related=none commit` (or `related=` an element outside the editor frame) right
after the press, with no `mousedown` on the Center option in the content frame, and whose landing
summary shows the press in the workbench document.

### C2: a render reached the page while the block editor was open

`applyContentPatch` (`src/page/features/contentPatch.ts`) closes the open block editor without a
save (`rt.blockEditor.closeBlockEdit(false)`), and while the host's render request is ahead of the
page `findCurrentFrame` returns undefined. Paths to check: the autosave of the `/align` query
removal (`editPalette.ts`, `runMenuEntry`: `deps.applyTextEdit` of the removal, then
`blockEditor.autosaveBlockEdit()`, a non-final `previewEditSave` 400 ms later,
`AUTOSAVE_DELAY_MS` in `src/page/pageSettings.ts`) landing at the time of the press; a late watcher
or dependency event from the previous step (`table-editing/r08-cell-bold-shortcut`, then its
fixture cleanup) that the host should defer while an editor is open
(`edits.deferWhileEditing` in `src/session/hostEvents.ts`).

Proof or exclusion: the page editor trace shows (or does not show) `content patch request a -> b`
between the press and the failure; the host's request id and document version at the failure
against the frame's attributes.

### C3: the press landed in the content frame, outside the editor frame

If the align popover moved between Playwright's box read and the press (its position is computed
from the caret and the bar, `openPopover` in `editPalette.ts`), the press could land on the preview
outside the editor frame: a `mousedown` the page does not cancel, then a blur commit with a related
target outside the frame. Proof or exclusion: the editor trace's `mousedown` entry (target and
`prevented=`) at the press.

### Ruled out by the log

- A caret in the wrong column (the second column centred, or no alignment applied) would leave the
  text box open with a defined state; the final state is undefined.
- `alignColumn` (`src/page/modules/tableEditActions.ts`) rewrites `| --- | --- |` to
  `| :---: | --- |` deterministically for a caret in the first column; nothing in it depends on
  time.

The code the scenario drives is the same at `origin/main` (`5a84db8b`) as at `2bea4c6` for the test,
the harness, `clickRouting.ts` and `editPalette.ts`; `blockEditor.ts`, `blockSourceEditor.ts` and
`contentPatch.ts` changed since (CRLF line endings, delete-when-empty, blank-lines block), none of
it on the path of a non-empty paragraph editor in an LF file. The Driver confirms this with
`git diff 2bea4c6 origin/main` on those files before the first run.

## What changes

### 1. Failure traces in RI-T45 (always shipped)

File: `test/integration/realInput/tableInsertSlash.ts`.

Every wait and assertion of the scenario that can fail on a race (each `waitFor`, each
`expectState`, the final `assert` calls) fails with one message built by a single helper of the
scenario (as `explain` in `test/integration/realInput/editorWidgets.ts`, around line 230), which
appends, in this order:

- the steps the scenario passed, each with its time in milliseconds since the scenario started
  (for example `press End`, `type /tab`, `slash menu open`, `size grid`, `table inserted`,
  `caret after Column 1`, `type /align`, `align choices`, `query removed`, `Center pressed`);
- the host's render request: `getActivePreviewForTests()` `requestId`, `documentVersion` and
  `phase`;
- the source document: `document.version`, `document.isDirty` and `document.getText()` (the smoke
  document is short; the whole text is printed);
- `editorState(page)` (kept from today's message);
- `windowFocusReport(page)` (`test/integration/windowFocus.ts`). The suite already prints the
  workbench focus dump at the failing step (`takeFailureFocusDump`, `realInput/run.ts` line 362,
  the dump quoted above); what this report adds is, for every frame, its document id, version,
  request id and visibility, and the page's editor trace, plus the VS Code window state and the
  page's own focus;
- `pageTraceStart`: the page's `__studioDiagnostics.startedAt()` against the scenario's clock, so
  the editor trace entries line up with the steps (as in `editorWidgets.ts`);
- `readLandingSummary(page, frame, startedAt, startedAt)`
  (`test/integration/realInput/clickRouting.ts`), with `installLandingProbe(page, frame)` called
  once the paragraph editor is open (after `waitForEditor`).

A read that fails while the message is built (frame detached, CDP error) prints `unreadable:
<error>` for that part and never hides the original error. The message reaches the CI log through
the suite's existing `Real-input integration failed:` line. Nothing else is added to a passing run,
except the `hover recovered after re-move (CR 330)` line that `clickListOption` logs when its hover
had to be redone (`clickRouting.ts` line 354).

### 2. Stress registration (always shipped)

The sibling CR `flaky-paste-url-drop-files` (same planning folder, `1-inbox`) moves `paste-url` and
`drop-files` out of `STRESS_ON_DEMAND_SCENARIOS` (`test/shared/stressPlan.ts` line 93,
`test/integration/realInput/run.ts` lines 103 to 114, `test/build/stressPlan.test.ts` lines 61 to
69) and may delete that constant. Both CRs go in batch-07, the sibling first. This section holds
whichever CR lands first:

- `test/shared/stressPlan.ts`: the on-demand list `STRESS_ON_DEMAND_SCENARIOS` holds
  `"table-insert-slash"`, with a comment naming this CR. The constant is kept when it exists, or
  created again when the sibling deleted it (the default plan is at the deadline margin that
  `test/build/hangWatchdog.test.ts` keeps, which is why the name is on demand, as CR 425 did).
  `hostStressPlan` keeps reading it for the trusted window.
  Owner, t45-Q2 ("t45 à la demande, 11 tours"): `table-insert-slash` runs on demand only, never in
  the default plan, which keeps the sibling's 21 scenarios at 11 rounds; RI-T45 is proved by its own
  dispatches (Evidence).
- `test/integration/realInput/run.ts`: `STRESS_SCENARIOS` gets `"table-insert-slash": (page) =>
  scenarioTableInsertFromSlash(page)`. Its key order follows the lists of `stressPlan.ts` as they
  are at that point (default trusted names, then the on-demand names), which `runStress` asserts.
- `test/build/stressPlan.test.ts`: a test of its own for `table-insert-slash`: it is on demand in the
  trusted window (named in `STUDIO_STRESS_SCENARIOS`, the trusted plan runs it) and never in the
  default plan. It does not depend on the CR 425 test, which the sibling may change or remove.

### 3. The fix, from what the traces prove

- **C1 (the lead):** the Center press goes through `clickListOption(page, frame, "center",
  "[data-edit-action='columnAlign']")` inside `withCurrentFrame`, as rule 12 requires for a
  just-opened list option. The trigger is the palette's Column alignment button: the slash menu
  opens the align popover anchored to it (`activate(action, buttons.find(...data-edit-action...))`
  in `editPalette.ts`). This change is made whether C1 is proved or not, because the rule asks for
  it; the delivery says whether C1 was proved.
- **C2 or C3 proved:** the product is fixed at the cause (an editor must not close when it should
  not, rule 12), with the SwRS work the requirements guidelines ask for
  (`requirements/guidelines/requirements.guidelines.md` and `project.guidelines.md`, "During a
  change"): the SwRS that the fix touches, `@implements_req` and `@tests_req` markers, `just
  requirements-update`, a dated entry in `requirements/tiers/log.md`. A product fix that changes
  an existing published requirement (not one that only adds an SwRS or extends one) comes back to
  the Chief of Staff with the trace that proves the cause, before it ships.
- **No cause proved:** sections 1, 2 and the C1 click change ship; the delivery states plainly that
  the cause is not proved, what the stress runs showed, and that the traces will name it at the next
  failure. No retry, no quarantine, no raised timeout, no sleep.

## Evidence

Observed rate: RI-T45 failed once over the heavy runs that ran it, about 1 in 20 or more (the
failing run 44731534776 and its green re-run; the Driver counts the heavy runs of `main` and of
batch branches that ran RI-T45 and writes the exact count in `work/`). The rounds are sized from
that rate: at 1 in 20, 60 rounds can easily miss the race, so each phase runs about 300 rounds.
A dispatch of this one scenario allows up to 100 rounds (`MAX_STRESS_REPEAT`, under the 220 scenario
runs per window of the workflow input), as long as the computed launch deadline holds (2 min plus
6 s per scenario run, at most 24 min, rule 11): the Driver reads RI-T45's healthy duration from a
passing round (`PASS stress ... table-insert-slash (<ms> ms)`) and lowers the rounds per dispatch
when it does not hold, adding dispatches to keep the total.

What the stress runs can show: they repeat RI-T45 alone, so they reach C1 and C3 (the press itself)
only. C2 (a late event from RI-T44, `scenarioTableCellBold`, reaching the page during RI-T45) needs
RI-T45 in its place after RI-T44: only the full integration job and the new traces cover it.

1. **Before the fix, the traces only (sections 1 and 2, the old direct click kept):** heavy
   dispatches on the CR branch, `gh workflow run ci.yml --ref <branch> -f heavy=true -f
   stress_scenarios=table-insert-slash -f stress_repeat=100 -f gallery=false`, three of them (300
   rounds), or more with fewer rounds each when the deadline asks for it. A red round's message is
   the proof of the cause (C1 or C3); the Driver copies the failing run id and the trace lines that
   prove it into `work/`. 300 green rounds mean the race did not reproduce: it is reported, not
   taken as a proof either way.
2. **A forced failure, local, not committed:** change the expected text of one `expectState` of
   RI-T45, run the scenario once in the real window, and copy the failure message into `work/`: it
   holds every part of section 1 (steps with times, host request, buffer, editor state, focus report
   with the editor trace, page trace start, landing summary). Then revert the change.
3. **After the fix:** the same stress dispatches, 300 rounds in total, all green, on the branch
   head that will merge. The run ids go in the delivery.
4. **The unit checks:** `test/build/stressPlan.test.ts` passes with `table-insert-slash` on demand.
5. **The project gates:** `just check` and `just preflight` (the static stage on Windows; CI runs
   the others), and the heavy integration job (`gh workflow run ci.yml --ref <branch> -f
   heavy=true`) green on the branch head: the full real-input suite, RI-T45 in its usual place after
   RI-T44 (`scenarioTableCellBold`). This is the only run that can show C2; a C2 failure there
   explains itself through the traces of section 1.

The stress and integration jobs run on GitHub's Ubuntu runner under `xvfb-run` (screen 2600 x 1440
x 24), with no D-Bus session (the `dbus/bus.cc` errors of the log are normal there); a local Windows
run proves the traces' content (step 2), not the race, which only the CI runs can show.

## Out of scope

- Any automatic retry, quarantine, skip or raised timeout of RI-T45 or of the stress job (owner,
  t45-Q1; CI guidelines rules 9, 11 and 12).
- The other real-input scenarios, including the direct clicks of other steps that are not on a
  just-opened list option.
- `wide-table-tab` (out of the stress plan for its own unstable click).
- Adding `table-insert-slash` to the default stress plan (owner, t45-Q2: it stays on demand).
- The size of the default stress plan: the sibling's 21 scenarios at 11 rounds (owner, t45-Q2),
  set by the sibling CR, not here.
