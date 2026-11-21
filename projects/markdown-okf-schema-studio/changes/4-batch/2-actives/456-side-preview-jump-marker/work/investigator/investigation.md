# Investigation, CR-456 side-preview jump marker

Read only. Worktree base: CR-455 head (`61737fd3`, "preview the real file next to a text diff" is
`1933d79f`). Rules read: constitution, requirements guidelines (okfreq), stacked-prs, glossary
(via `$CHANTIER rules` list); nothing in them contradicts the spec.

## 1. Where the spec's references stand at this base

| Spec says | At this base |
| --- | --- |
| `scrollSync.ts` `requestRevealLine` / `postPendingRevealLine`, anchor set at "line 272" | `src/session/features/scrollSync.ts` ~251 / 267, anchor line ~273. `pendingRevealLine?: number` at line 39 (bare number, as the spec says) |
| page ready call `rendering.ts` line 542 | unchanged, `manager.scroll.postPendingRevealLine(preview)` |
| `hostHandlers.ts` line 111 | unchanged: `rt.lineMarker.reveal(message.line)` |
| `PreviewRevealLineMessage`, router entry | `hostToPage.ts` 187 and 455 (`isValid` on `line` only), unchanged |
| `activation.ts` lines 90 and 406 (Studio tab calls) | now 91 (`bindLiveSessions`, filters `!followsActiveEditor`) and 451 (`takePending` at session creation); file is 529 lines, so the 800 ratchet holds with room |
| `PENDING_LINE_WINDOW_MS` | non-exported const at `openInStudio.ts` 34, used by `StudioLineRequests` only; to move to `src/core/navigation/` as the spec says |
| `StudioOpenedTextEditors`, `openAtText` etc. | as in 1.11.0; `StudioSelections`, `editorJumps.ts`, `jumpSignal.ts`, `markedLine`, `previewLineMarkerClear`, `onEditorJumped` do not exist yet (all new) |
| `onDidChangeTextEditorSelection` listeners | two today: `openingWatcher.ts` 75 (`watchJumps`, Command only, keeps a `jumps` map) and `keystrokes.ts` 18 (Keyboard, test hook). `editorJumps.ts` becomes the third reader; the watcher swap is as specified |
| "real file of a diff" reading | exists: `src/host-vscode/diffRealFile.ts` (CR-455): `isEligibleUri` (moved out of `openingWatcher.ts`, which now imports it), `activeDiffInput`, `isDiffSide(input, uri)`, `realSideOfDiff(input, activeUri)` (sync), `realFileOfDiff(input, activeUri)` (async, adds a `stand-in` kind via `fs.stat`) |

## 2. What CR-455 changes in the plan

1. **Diff reading is ready-made; use `realSideOfDiff`, not `realFileOfDiff`.** The side preview
   follows a diff through `StudioActivation.followActiveDiff` (activation.ts ~340), which uses
   `realSideOfDiff(diff, activeEditor uri)` and never the stand-in. So `editorJumps` must use the same
   sync function: a `stand-in` target would be a document the side preview is not showing (and its
   lines may differ). A diff with no eligible side gives no jump. Spec 4.1 says "as side-preview-diff-gaps
   reads it" without naming the function: name it in the briefing.
2. **Pass the event's editor URI as `activeUri`, not `window.activeTextEditor`.** `realSideOfDiff`
   picks the active side when both sides are files (a two-file compare). For a jump the relevant side
   is the one that got the selection event; the selection can land on a side that is not the active
   editor (J5 question). `isDiffSide(input, event.textEditor.document.uri)` is the "editor is a side of
   the active tab" test of 4.1.
3. **`activeDiffInput()` reads the active tab of the active group.** A jump in a diff in a non-active
   group is not seen as a diff side. Acceptable (a jump activates its group); note it in the SwRS.
4. **Jump and switch race is worse with diffs.** Opening a diff fires `onDidChangeTabs` and
   `followActiveDiff` awaits `openTextDocument` before `onActiveDocumentChanged`; the jump's `Command`
   selection can arrive before the side preview has switched. The spec's document-keyed pending line
   (posted at the render's page ready for that document) covers this; the session test "jump before
   the switch" must use the diff path too (`onActiveDocumentChanged`, new in `hostEvents.ts`).
5. **`hostEvents.ts`**: CR-455 split `onActiveEditorChanged` into `onActiveEditorChanged` +
   `onActiveDocumentChanged(document)` (hostEvents 443-465). `onEditorJumped` goes next to them;
   `manager.latest(followsActiveEditor)` and `switchAfterFlush` are used the same way. No merge
   conflict expected beyond adjacent edits. The stack makes the "rebase on final head" note of spec 8
   a no-op today; a later CR-455 head still needs a rebase.
6. **`scrollSync.ts`**: CR-455 changed only `revealEditorLine` (the `file:` id filter, ~line 118).
   `requestRevealLine` / `postPendingRevealLine` / `ScrollState` are untouched, so 4.2-4.3 apply as
   written. `syncEditorToPreview` matches `documentUri === sourceEditor.document.id`, so a virtual diff
   side never drives scroll sync: the editor-leads claim for "anchor on" holds only when the real
   file's side is a visible editor (it is, in a replace preview's original side). With the anchor on
   and the selection on the virtual side, scroll sync may not move the page at all, and `if-off-screen`
   is then the only scroll: a good reason to keep that mode.
7. **Tests**: `test/host/fakeVscode.ts` already fires `changeSelection` with `kind: 3` when
   `options.line` is set (line ~754), has `TabInputTextDiff`, `TextEditorSelectionChangeKind {Keyboard 1,
   Mouse 2, Command 3}` and an `activeDiff` hook (~467, ~787); `test/host/diffPreview.requirements.test.ts`
   is the model for the `editorJumps` diff-side host test. In `test/integration/diffPreview.test.ts`
   the helpers are `openDiff(original, modified)` (waits for the requested diff to be the active tab and
   a text editor active), `focusOriginalSide` (command `workbench.action.compareEditor.focusSecondarySide`,
   the original side; the spec's name `focusSecondarySide` is this constant), `virtualOf(file, side)`
   (scheme `studio-diff-test` at the file's path), `withLayout(sideBySide, body)`. They are module-local
   (not exported): J5 either moves them to `test/integration/realInput/harness.ts` or a small shared
   `diffHarness.ts`, or the new test copies them. Prefer extracting (the diff suite and
   `sidePreviewJump.test.ts` both need them); keep the diff suite's behaviour unchanged. A selection
   made by the test through the API (`editor.selection = ...`) gives no `Command` kind: J5's replace
   preview needs the real Search view click or `vscode.open` with a selection, and the original side
   of the replace preview holds the real file (as in CR-445 `diff-view-findings.md`).

## 3. Smallest change meeting the spec

The spec's design is already minimal; keep it. Ordered by dependency:

1. `src/core/navigation/jumpSignal.ts` (pure) + `test/core/navigation/jumpSignal.test.ts`.
2. `StudioSelections` in `openInStudio.ts` (expect/take, 1000 ms, URI + line, once), wired where the
   spec says (`activation.ts` Open as Text ~284; `vscodeHost.ts` `showDocument` ~285, only when a
   selection is carried). Move `PENDING_LINE_WINDOW_MS` to `src/core/navigation/` and import it from
   both places.
3. `src/host-vscode/editorJumps.ts` (only host user of the selection event for jumps; uses
   `diffRealFile.ts`), created in `StudioActivation.start` before the opening watcher; the watcher's
   `watchJumps` becomes a subscription (jumps map and `JUMP_SETTLE_MS` logic kept).
4. Protocol: `scroll?` on `PreviewRevealLineMessage` + router check; new `previewLineMarkerClear`
   (render addressing); page: `hostHandlers.ts` pass-through and clear; `lineMarker.ts`
   `reveal(line, scroll)` with the `if-off-screen` mode and `clear()` (verify `clear` is already
   exported from `installLineMarker`, else add).
5. Session: `ScrollState.pendingRevealLine` object, `markedLine`; `requestRevealLine(preview, line,
   {documentId, scroll})`; `postPendingRevealLine` gate (document, ready, `panel.visible`, age);
   anchor not taken for a following side preview with the anchor on; `HostEvents.onEditorJumped`;
   `onDocumentChanged` clear; switch clears pending and marked; links/history call (4.5).
   Existing callers: only `activation.ts` 91 and 451 (both pass their own document, `"reading-line"`).
6. Docs, glossary, CHANGELOG, requirements (4.6, 4.7).

Smaller-than-spec options worth a decision in the first round: none needed; every piece is used by a
requirement of the spec.

## 4. Risks

- **Values derived from `PENDING_LINE_WINDOW_MS` (5000):** searched for `5000` use: only
  `openInStudio.ts` 34 (const), 56 and 65 (uses). Moving it keeps both users on one value. Doc/SwRS text
  that says "five seconds" for the Studio line (LIFE-181, `docs/user/open-studio.md`): grep before editing.
- **`pendingRevealLine` type change** breaks every reader of the bare number: `scrollSync.ts`
  251-273 only (grep done: no other file reads it); tests in `test/session/lifeReq.requirements.test.ts`
  and `test/host/lifeReqHarness.ts` that set it must be updated (search `pendingRevealLine` in `test/`
  before starting).
- **Visibility gate is new for the Studio tab too** (`panel.visible`): a Studio tab opened at a line in
  a background group could now wait for its next ready. The spec says it holds; check the memory host
  `PreviewPanel.visible` default is `true` so existing LIFE-181 tests stay green.
- **Anchor on does not take the anchor** while Studio-tab behaviour keeps it: a branch on
  `preview.followsActiveEditor && configuration.scrollPreviewWithEditor`; the Studio tab path must not
  change (LIFE-181 tests are the guard).
- **Double mark / double reveal:** `showDocument` from the side preview's own links (4.5) is marked by
  the session and by `editorJumps` unless the `StudioSelections.expect` is recorded before `vscode.open`;
  the order inside `showDocument` matters (record, then open). `showDocumentInStudio` is not affected.
- **Opening watcher regressions:** `watchJumps` swap; its tests (`test/host/openingWatcher.test.ts`,
  `openAtLine.test.ts`) stay unchanged by design: run them first after step 3.
- **Same-URI `Command` event from Studio's own "Open as Text"** is swallowed by `StudioSelections` only
  on URI + line; the watcher's rule 4 already keeps it. Add the test the spec lists.
- **J1 may contradict decision 4.** Several moves (Find, Go to Symbol, Go Back) may carry no kind or
  `Keyboard`; the spec accepts that as known limits, so J1 output decides the docs, not the code.
  Ctrl+A / Format Document carrying `Command` would mark by decision 6: record, do not special-case.
- **Preview-tab replacement in tests:** a new diff replaces the open one in its group (preview tab);
  CR-455's `openDiff` already waits for the requested one; reuse it, do not count tabs.
- Constitution points to honour: import boundaries (`vscode` only in `src/host-vscode/`, dependency-cruiser
  no exceptions), file size ratchet, unused exports check, settings schema untouched (no setting),
  `@implements_req` / `@tests_req` markers on new files, `just requirements-update`, dated
  `requirements/tiers/log.md` entry. The LIFE-178..185 and StRS-LIFE-023 files are all `req_lifecycle:
  proposed` today (checked: 178-185 and 023), so editing them needs no re-approval; the Driver re-checks
  before editing.
- CR-455's own requirement edits (LIFE-003, 026, 100, 108) are not touched by this CR, but 4.7's SwRS for
  jumps on diffs should cite LIFE-003/026 for the real-file reading.

## 5. Questions only the user can answer

None. (Spec section 9 empty, all decisions final.) Two choices left to the Driver, both settled here:
use `realSideOfDiff` (no stand-in) for jumps; extract the diff test helpers to a shared test module.

## 6. Evidence plan

Kind of change: a behaviour change visible in the real side preview (host routing, page marker,
scroll mode) plus new host signal code.

| What | Before / after | Technique | Notes |
| --- | --- | --- | --- |
| Marker in the side preview after a search click (J2, J3, J7, J6, J4) | Before: the CR-445 evidence `ta-defaults-06-t12-side-preview-jump-*.png` (no marker), or re-run J2 on the base; after: J2 screenshot of the side preview with the arrow and band on line 40 | New `test/integration/sidePreviewJump.test.ts` in the real VS Code window (trusted suite, `realInput/harness.ts`, `connectWorkbench`, `waitFor`), marker read as `.sphinx-preview-line-marker` in the webview; screenshot through the harness evidence capture | Run on Windows locally; Linux through the heavy CI run (`gh workflow run ci.yml --ref <branch> -f heavy=true`) |
| Table of kinds per move (J1) | none before; after: a table in the PR and `docs/user/open-studio.md` | Test hook in `src/host-vscode/testHooks.ts` recording `{kind, selections, firstLine}` and each `onJump`; the J1 test writes the log to `*.log` under `work/gates/` and the table is derived from it | Run first. Raw log is not published; the table is |
| Frame-by-frame scroll (J2) | none before | Poll the side preview `scrollY` every frame for 2 s, written to a log | Proves "ends still, no back-and-forth" |
| Replace preview (J5) | none before | Real Search view replace click; record which diff side received the `Command` event; screenshot of the side preview marking line 25 | Result may be "no `Command` change": then the case is a recorded known limit, not a failure. This suite already has the diff helpers from CR-455 |
| Visual scenario | before: CR-445 scenarios stay; after: new scenario in `test/visual/lineMarkerScenarios.ts`, side preview page after `previewRevealLine` with `scroll: "if-off-screen"` sent as a `pageActions` message, light and dark | Playwright visual suite (`just ci-visual`, Linux and macOS CI; does not run on Windows) | Cannot be captured locally on Windows |
| Unit/host/session/page/protocol tests | each fails on the base (no new modules / fields) | `just check` locally; show red-on-base by running the new tests against the base (stash-free: run before the source commits, or on a checkout of the base) | Spec 6.2 lists them |
| Gate | `just check`, `just requirements-update`, `just requirements-lint`, `just preflight` (Windows: static stage) | commands output kept in `work/gates/*.log` | Heavy CI run before the PR leaves draft |

Cannot be shown: Web, Remote, macOS, the Agents window (untested, labelled in the PR); VSCodeVim moves
(an API move is simulated by the test, not the extension); a Linux visual capture from Windows.

For the PR Impacts section (pull-request.guidelines): a before (side preview after a search click,
base, no marker) and an after (J2) pair, cropped to the side preview.
