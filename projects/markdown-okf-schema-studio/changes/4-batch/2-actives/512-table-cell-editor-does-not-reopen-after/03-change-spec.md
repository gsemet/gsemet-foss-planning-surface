# Cell editor reopen after a grid paste: reproduce, then fix or record

Short name: `cell-reopen`. Destination: the running batch batch-09 (its stack). No tracker issue.

## Goal

SwRS-MDOKFSTUDIO-TABLE-120 says a spreadsheet paste into a table cell fills the cells and **reopens
the cell editor in the start cell**. While filming the `paste-spreadsheet-cells` clip (CR-489), the
table filled correctly but the editor did not reopen on the header cell "Task" (3 of 3 runs, also
with Ctrl+A first), while the real-window integration test passes its reopen check. The owner's
decision (cell-reopen-Q1): reproduce with real input in a real window; if it is a bug, fix it with a
test; if it is an artefact of the driving tool, record it (in the requirement or the clip
guidelines). Either way, the "may or may not reopen" wording in the clip ends.

## What is known before starting (read from origin/main)

The premise "CDP input versus real input" does not separate the two runs: both press keys the same
way.

- The integration test `test/integration/realInput/tableGridPaste.ts`
  (`scenarioTableGridPaste`) presses Ctrl+A and Ctrl+V with `press()` of
  `test/integration/realInput/harness.ts`, which is `page.keyboard.press()`: CDP key events into a
  real VS Code window.
- The clip `docs/demo-video/clips/paste-spreadsheet-cells/scenario.mjs` presses Ctrl+V with
  `t.press()` of `docs/demo-video/clip-kit/lib/take.mjs`, which is also `page.keyboard.press()`
  (unless `CLIP_KEY_COMMANDS=1`).

What does differ between the passing test and the failing clip:

| Condition | Integration test (reopens) | Clip (does not reopen) |
| --- | --- | --- |
| Start cell | a body cell (`row five`, rendered row 4, column 1) | the header cell "Task" (rendered row 0, column 0: SwRS S3's case) |
| Grid against the table | 2 lines x 3 values: adds 1 column and 1 row | 5 lines x 3 values into a 2-column, 1-body-row table: adds 1 column and 3 rows |
| Clipboard source | `vscode.env.clipboard.writeText` (text only) | Ctrl+C in VS Code's text editor on `tasks.tsv` (also puts `text/html` and VS Code's editor data on the clipboard) |
| Auto-save | the test profile's default | the clip profile's `files.autoSave: afterDelay`, `files.autoSaveDelay: 200` (`docs/demo-video/clip-kit/lib/profile.mjs`) |
| Before the paste | Ctrl+A | none in the take (the intake reports Ctrl+A tried too, same result) |
| Reopen check | waits until the cell text box shows `a` (the harness's `waitFor` deadline) | no wait: 250 ms after the paste, then at most 3 s for the table shape, then at 4.0 s a look for the Done button |

The reopen path in the page: the `paste` listener of the cell text box in `renderTableCellEditor`
(`src/page/features/tableCellEditor.ts`, marked `@implements_req SwRS-MDOKFSTUDIO-TABLE-120`) calls
`structural(() => fillGrid(...))`; `structural` calls `blockEditor.rememberPendingBlockNavigation(
edit.target, "end", undefined, { tableRowIndex, tableColumnIndex, tableRank })` then
`blockEditor.postBlockEditSave(true)` (and clears the pending navigation when the save is not
posted). The pending navigation is kept in `state` and in the webview state
(`src/page/features/blockEditor.ts`), restored after a full reload (`src/page/runtime.ts`), and
consumed by `resumePendingBlockNavigation` (`src/page/features/editMode.ts`), called from
`initializeContent` (`src/page/features/contentPatch.ts`) and from the detached save path
(`src/page/features/detachedSave.ts`). It finds the block by `blockId`, else by source line and
tag, then the cell as `table.rows[tableRowIndex].cells[tableColumnIndex]`, and opens it with
`openMappedEditor`. The unit test `test/page/runtimeTableCellPaste.test.ts` checks only that the
pending navigation is stored (body cell `[2, 1]`), not that it is consumed; no test covers a reopen
from the header row after a grid paste.

None of this proves a bug or an artefact: it names the suspects for the reproduction.

## What changes

### 1. Reproduce in a real window (always)

Add a second real-window scenario to `test/integration/realInput/tableGridPaste.ts`, with the
clip's conditions, keys through the harness's `press()` as the existing scenario does:

- the document of the clip's stage, `docs/demo-video/clips/paste-spreadsheet-cells/stage/release-checklist.md`
  (a heading, then `| Task | Owner |`, one body row), inlined in the test like `READING_DOCUMENT`;
- the clipboard holding the text of `stage/tasks.tsv` (5 lines of 3 tab-separated values);
- a click on the header cell "Task", the cell editor open on it, then Ctrl+V (platform modifier as
  in the existing scenario), no Ctrl+A;
- checks: the source equals the clip's `EXPECTED` text (`scenario.mjs`), then
  `waitFor("the editor open in the header cell Task", ...)` on the cell text box showing `Task`
  (the start cell's new text: the first value of the first pasted line is `Task`), and the open
  editor's cell is the header cell of column 0.

Name it in the file's pattern (for example `scenarioTableGridPasteFromHeader`), carry
`@tests_req SwRS-MDOKFSTUDIO-TABLE-120#S3` on it, and run it from the same `"table-grid-paste"`
entry of the single-scenario map in `test/integration/realInput/run.ts` and from the full trusted
run, next to `scenarioTableGridPaste`.

Run it locally in a real window:
`STUDIO_REAL_INPUT_SCENARIO=table-grid-paste fnm exec -- npm run test:integration -- --trusted-only`
(Windows: from Git Bash, per CONTRIBUTING.md "Windows"; the screen unlocked, no other app-window
test running, per `.agents/guidelines/local-worktree.guidelines.md`, "App-window tests").

When this scenario passes on the first try, narrow the remaining differences one at a time, each
as a temporary variant of the scenario (not committed), until one makes the reopen fail or none
does:

1. the clipboard filled by Ctrl+C in VS Code's text editor on a `tasks.tsv` opened beside Studio
   (the clip's own copy, `text/html` included);
2. `files.autoSave: afterDelay` with `files.autoSaveDelay: 200` on the fixture's workspace;
3. the clip's timing: no wait after the paste beyond the clip's 250 ms, then the clip's check.

Then run the clip itself twice: `just clip paste-spreadsheet-cells` with its current scenario, and
once with `CLIP_KEY_COMMANDS=1` (the editing command riding on the key event,
`pressWithCommands` in `take.mjs`), recording for each take whether the Done button is present
at 4.0 s (`cellEditorOpen` before the Done click: add that record next to the existing
`t.record("cellEditorOpen", ...)`, as `cellEditorOpenAfterPaste`).

Keep a record of each run (condition, result, the trace of `editorTrace` when the reopen fails:
"cell editor closed" / "cell editor focused" lines) in the CR's `work/` folder, and summarize it in
the PR body.

### 2a. Outcome "bug" (the reopen fails in a real window under a condition a writer meets)

A condition a writer meets: a header-row start, a grid that adds several rows, a copy from VS
Code's text editor, auto-save on, or the paste timing. Then:

- Fix the cause in the page code the investigation names (the reopen path above; the fix stays in
  `src/page/`, in its layer, per CONTRIBUTING.md "Architecture"), with `@implements_req
  SwRS-MDOKFSTUDIO-TABLE-120` on the changed code.
- The real-window scenario of section 1, set to the failing condition, is the regression test: it
  fails before the fix and passes after it (both runs recorded).
- When the cause is in the page logic the runtime harness can reach (for example the pending
  navigation lost, or not consumed, for row 0 or after rows are added), add a unit test to
  `test/page/runtimeTableCellPaste.test.ts` that pastes from the header cell and asserts the
  editor reopens in that cell after the save's content patch (not only that the pending
  navigation is stored), with `@tests_req SwRS-MDOKFSTUDIO-TABLE-120#S3`.
- `requirements/tiers/swrs/table-editing/SwRS-MDOKFSTUDIO-TABLE-120.md`: S3's THEN gains "and the
  editor reopens in the header cell"; its verification notes name the new real-window scenario.
- The clip: in `docs/demo-video/clips/paste-spreadsheet-cells/scenario.mjs`, the comment before the
  Done click (line "The cell editor of TABLE-120 may or may not be reopened ...") says the editor
  reopens on "Task" and the Done click closes it; in `clip.md`, the note "The cell editor may or may
  not reopen in "Task" after the paste ..." and the Shot row's "If the cell editor is open after the
  paste" say the same. The Done click stays (it is still needed: an open editor hides "Due").

### 2b. Outcome "artefact" (the reopen holds in a real window, and only the clip's driving misses it)

- `requirements/tiers/swrs/table-editing/SwRS-MDOKFSTUDIO-TABLE-120.md`: the verification notes
  name the new real-window scenario (header-row start), which keeps S3's reopen covered.
- `docs/demo-video/guidelines/feature-clip-process.guidelines.md`: in the part on the kit and a
  take (section "1. The kit and a take", next to the `press(chord, badgeId)` description), one
  sentence on what the investigation found (what in the take's driving or timing makes the editor
  look closed, and how a take waits for it), so a later clip does not report it as a bug again.
- The clip: the comment in `scenario.mjs` and the note in `clip.md` replace "may or may not
  reopen ... with synthetic input" with the established cause, and the take waits for the state it
  films the way the guideline sentence says (the Done click kept when the editor is open).

### 2c. Outcome "cannot reproduce at all" (neither the scenario nor the clip fails any more)

Treated as 2b: the new scenario is committed as coverage of S3's reopen, the guideline sentence
says the clip's earlier miss did not reproduce on the head under test (the commit named), and the
clip's wording drops "may or may not".

### Requirements and log (every outcome)

- Per `requirements/guidelines/requirements.guidelines.md` and
  `requirements/guidelines/project.guidelines.md` ("During a change"): TABLE-120 is proposed, not
  approved, so the edits above need no re-approval. Then `just requirements-update` and a dated
  entry in `requirements/tiers/log.md` naming the outcome.
- The writing skill `skills/writing-for-markdown-okf-schema-studio/` is not touched: no rendered
  syntax changes.
- A user-visible fix (outcome 2a) gets its line in the changelog / release notes in the way the
  batch's other fixes do (the release ships this CR's fix, per the owner's answer).

## Out of scope

- Re-filming or re-rendering the clip's outputs (GIF, MP4, frames, contact sheet): the scenario
  already handles both states; only its comment, its `clip.md` notes and the new record change.
- Any change to the grid paste itself (values, added rows and columns, one save, one undo).
- Other cell-editor reopen paths (structural buttons, Tab), unless the fix of 2a is shared code
  they use; then their existing tests must stay green.
- An OS-level keystroke tool (neither CDP nor Playwright) in the harness.

## Evidence

- The real-window scenario of section 1, committed, passing locally (run named, with its
  `STUDIO_REAL_INPUT_SCENARIO=table-grid-paste` command) and in CI's real-window jobs (on a branch:
  `gh workflow run ci.yml --ref <branch> -f heavy=true`; a pull request runs only the simulated
  jobs).
- Outcome 2a: the same scenario failing on the base and passing with the fix (both runs recorded);
  the unit test when one applies, failing before and passing after.
- The record of the narrowing runs and of the two clip takes (`cellEditorOpenAfterPaste` per take),
  summarized in the PR body.
- The guards read the shipped files: the scenario's expected text is the clip's `EXPECTED` and its
  document is the clip's stage text, copied verbatim from the head under test (a mismatch between
  the copy and `stage/` is a test failure the Driver resolves by reading `stage/` again).
- `just requirements-lint`, `just requirements-update`, then `just preflight` (on Windows the static
  stage; CI runs the others).

Host and default matrix (the outcome depends on the auto-save value, a configured setting):

- auto-save off (VS Code's shipped default), header-row start: the editor reopens on "Task".
- auto-save `afterDelay` 200 ms (the clip profile), header-row start: the editor reopens on "Task"
  (outcome 2a fixes it if not).
- auto-save off, body-cell start: the existing `scenarioTableGridPaste` stays green.
