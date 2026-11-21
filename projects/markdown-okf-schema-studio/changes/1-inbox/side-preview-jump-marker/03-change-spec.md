# Show the target-line arrow in the side preview on a jump

When a jump (a search result, Quick Open `file.md:42`, a problem, a link, a Ctrl+click) moves a text
editor of a `.md` file to a line while the side preview follows that editor, the side preview shows
the line marker of the Studio tab on that line: the arrow in the left margin and the light band,
with the same lifetime. A cursor move (arrow keys, a click in the text, typing) never shows it.

Origin: verbal (owner). Split off from CR-445 open-at-line-marker, decision 17 (open-at-line-Q12).
No tracker issue. Code base: `origin/main` at `5a84db8b` (release 1.11.0, which ships CR-445). The
decisions below come from `02-answers.md` (jm-Q1, answered by the owner on 2026-11-21). The points
the grill leaves open are listed in section 9 for the owner; where the text depends on one, it
names the question (Qn) and holds no answer of its own.

## 1. Goal, in the user's terms

- I work in a text editor with the Studio side preview beside it. I click a search result, a
  problem, a link, or type Quick Open `doc.md:42`: the text editor goes to the line, and the side
  preview shows me that line with the same arrow and light band as the Studio tab.
- When I move my cursor myself (arrow keys, a click in the text, Page Down, typing), the side
  preview behaves as today: no arrow, no band.

## 2. Facts at 1.11.0 that shape the design

- The page already has the marker: `src/page/features/lineMarker.ts` (`installLineMarker`, SwRS
  LIFE-178 placement, LIFE-179 lifetime, LIFE-180 edit mode), driven by the host-to-page message
  `previewRevealLine` (`src/core/protocol/hostToPage.ts`). The host side is
  `ScrollSyncController.requestRevealLine` and `postPendingRevealLine`
  (`src/session/features/scrollSync.ts`, SwRS LIFE-181), with the pending line posted from the page
  ready handler of `src/session/features/rendering.ts` (line 542 at `5a84db8b`). The marker is
  per page, so the side preview (a webview panel with `followsActiveEditor` true) can show it with
  no page change.
- `ScrollState.pendingRevealLine` is a bare number on the session: it does not say which document
  it belongs to. The Studio tab never changes document, so CR-445 did not need it; the side preview
  does change document (`HostEvents.onActiveEditorChanged`, `src/session/hostEvents.ts`, calls
  `manager.switchAfterFlush`), so a line must carry its document (4.2).
- The side preview follows the text editor only through the editor's visible ranges:
  `vscode.window.onDidChangeTextEditorVisibleRanges` (`src/host-vscode/activation.ts`) →
  `HostEvents.onVisibleRangesChanged` → `ScrollSyncController.syncEditorToPreview`, which posts
  `sourceScroll` (the editor's first visible line, and the caret line for the optional caret mark).
  No session code listens to selection changes today.
- The caret mark (setting `markdownOkfSchemaStudio.preview.markEditorSelection`, off by default,
  SwRS TOOLBAR-128) marks the block of the caret line, refreshed on an editor scroll or a re-render,
  not on every cursor move. It is a different mark from the line marker and stays as it is (Q9).
- The only proved jump signal is CR-445's trial T2 (`src/host-vscode/openingWatcher.ts`, glossary
  "Jump"): for a **newly opened** text tab, VS Code shows the editor at 1:1, then applies the
  requested selection with a `onDidChangeTextEditorSelection` event of kind
  `TextEditorSelectionChangeKind.Command`; a plain reopening restores its view state with an event
  of no kind. `src/host-vscode/keystrokes.ts` already reads kind `Keyboard` as the reader's typing.
  Nothing proves yet what kind a jump into a text editor **already open** carries (a search result
  in a file already open as text, a problem in the active file), nor what kind the in-file
  commands carry (Go to Line, Find, Go to Symbol, Go to Next Problem), nor other extensions'
  cursor moves (VSCodeVim moves the cursor through the API). Trial J1 settles it (6.3).
- When a jump opens a new text tab while the side preview follows the active editor, CR-445 keeps
  the text editor (opening policy rule 6, `src/core/navigation/openingPolicy.ts`, SwRS LIFE-184):
  the side preview only scrolls. The watcher reads the jump's line (`jumpLineOf`) and drops it on
  `keep`. This CR does not change that decision; it adds the marker in the side preview.
- The side preview's own link and Back/Next navigation open a text editor through
  `host.navigation.showDocument(targetId, selection)` (`src/host-vscode/vscodeHost.ts`, used by
  `src/session/features/links.ts` and `history.ts`); that selection reaches the editor like a jump
  (Q8).

## 3. Decisions carried

| # | Decision (from `02-answers.md`) | Where in this spec |
| --- | --- | --- |
| 1 | jm-Q1: "Comme l'onglet Studio": the same arrow in the left margin and the same light band, same duration, reusing the marker of CR-445 open-at-line-marker (merged in v1.11.0); only on a jump, never on a cursor move | 4.1 (jump versus cursor move), 4.2 (routing), 4.3 (same marker, same lifetime) |
| 2 | Owner: "Et tout ça partira dans le batch en cours": once final and ready, added to the running batch-07 | process note, nothing to implement (8) |

The intake's list of jumps (search, Quick Open `:line`, Problems, links, Ctrl+click) is the
owner's; any move beyond it is Q1 or Q2.

## 4. What changes

### 4.1 Telling a jump from a cursor move (host)

The host tells them apart by the kind of the selection change that VS Code reports, the same signal
CR-445 proved for new tabs:

| Selection change | Read as | Why |
| --- | --- | --- |
| kind `Keyboard` (arrow keys, Page Down, Ctrl+End, typing, a keybinding) | cursor move, never a jump | the reader moves the cursor in the editor |
| kind `Mouse` (a click or a drag in the text) | cursor move, never a jump | same |
| no kind (`undefined`: a restored view state, undo or redo, an edit's side effect) | not a jump | CR-445 T2: a plain reopening restores with no kind |
| kind `Command` with one selection, in a text editor of an eligible saved `file:` `.md` document | a jump, at line `selections[0].start.line + 1` | CR-445 T2 for a new tab; trial J1 for an editor already open |
| kind `Command` with several selections | not a jump | a jump sets one selection (J1 checks each listed entry point gives one) |
| a selection Studio itself set, other than a navigation (the "Open as Text" editor, `activation.ts` line 284) | not a jump | the editor of "Open as Text" replaces a Studio tab; no side preview marks from it |

The rules are a pure function in a new file `src/core/navigation/jumpSignal.ts` (no host API,
unit-tested on its own):

- input: the change kind (`keyboard`, `mouse`, `command`, `none`), the number of selections, the
  first selection's 0-based start line, whether the document is an eligible saved `file:` `.md`,
  whether Studio itself set that selection as a non-navigation opening;
- output: `{ jump: false }` or `{ jump: true, line }` (1-based).

Q1 and Q2 may add an input and a rule to this function (for example "the line was outside the
editor's visible range before the change", or a cursor move by another extension); the table above
is what the owner's words settle, nothing more.

New file `src/host-vscode/editorJumps.ts`, the only listener of
`vscode.window.onDidChangeTextEditorSelection` for jumps: it maps each event to the facts above
(the kind from `vscode.TextEditorSelectionChangeKind`; "Studio set it" from the registry
`StudioOpenedTextEditors` of `src/host-vscode/openInStudio.ts`, which `openAsText` already fills),
asks `jumpSignal`, and fires `onJump({ uri, viewColumn, line, at })`. Created in
`StudioActivation.start` (`activation.ts`) before the opening watcher.

The opening watcher (`openingWatcher.ts`) stops listening to the selection itself: its
`watchJumps` listener is replaced by a subscription to `editorJumps.onJump`, so "jump" has one
definition (glossary). Its waiting logic (`jumpLineOf`, `JUMP_SETTLE_MS`) and every CR-445
decision stay as they are; the `@implements_req SwRS-MDOKFSTUDIO-LIFE-185` marker stays on
`startOpeningWatcher`. Its existing tests and integration test (`test/integration/openAtLine.test.ts`)
must pass unchanged.

### 4.2 From the jump to the side preview

- New host-neutral event `HostEvents.onEditorJumped(documentId: string, line: number)` in
  `src/session/hostEvents.ts`, wired in `activation.ts` from `editorJumps.onJump`
  (`host.documents` gives the document id of the URI, as the other events do).
- It targets the side preview: the latest live session with `followsActiveEditor` true
  (`manager.latest((preview) => preview.followsActiveEditor)`, as `onActiveEditorChanged` reads it).
  Other Studio views of the same document (a Studio tab beside the text editor, an older side preview
  that no longer follows) are Q6; until the owner answers, only the following side preview marks.
- If that side preview shows the document, or will show it because the jump made its editor active
  (the side preview follows only eligible Markdown documents, as today), the session asks the page
  to mark the line: `manager.scroll.requestRevealLine(preview, line, documentId)`.
- `requestRevealLine` and `ScrollState.pendingRevealLine` gain the document:
  `pendingRevealLine?: { line: number; documentId: string; at: number }`.
  `postPendingRevealLine` posts only when the session's stage shows that document
  (`preview.documentUri === documentId`), and drops a line older than CR-445's window
  (`PENDING_LINE_WINDOW_MS` of `openInStudio.ts`, moved to a host-neutral place the session can
  import, or passed in), so a line never lands on another document or late. The Studio tab's
  calls (`activation.ts` lines 90 and 406) pass their own document; their behaviour is unchanged
  (LIFE-181).
- The jump and the switch of document arrive in either order (the selection event may come before
  or after `onDidChangeActiveTextEditor`): the line waits on the session and is posted at the page
  ready of the render that shows its document (`rendering.ts`, the existing
  `postPendingRevealLine` call), or at once when the page already shows it.
- A side preview hidden behind another tab of its group at the jump: Q10.
- A jump that opens a new text tab while the side preview is open goes through CR-445 rule 6 (the
  text editor stays) and, through `editorJumps`, marks the side preview like any other jump. A jump
  while no side preview is open changes nothing (CR-445 puts the Studio tab in place, with its
  marker, as today).
- Whether a setting turns this off: Q7. Until answered, no setting gates it.

### 4.3 The marker in the side preview

- Same page feature, same look, same placement as the Studio tab (decision 1): `lineMarker.ts`,
  `lineMarkerStyles.ts`, SwRS LIFE-178 and LIFE-180 apply as they are. No page code changes for the
  look; no change to the writing skill (no rendered syntax changes).
- Same lifetime in the page (decision 1, "same duration", SwRS LIFE-179): it stays through scrolls
  of the page, is drawn again after a re-render, a content patch or a layout change, goes on a
  pointer press in the page or when an edit starts in the page, and moves when another jump comes.
  Whether a cursor move, typing or a scroll in the **text editor** removes it is Q5; until
  answered, nothing on the host side removes it.
- Where the line ends on screen: `previewRevealLine` scrolls silently so the line sits at the
  reading line (LIFE-178) and sets the session's anchor (`owner: "preview"`). In the side preview,
  scroll sync then moves the page with the editor's own reveal (`sourceScroll`). Which of the two
  places wins, and what a jump does when the anchor button is off (`scrollPreviewWithEditor` false),
  are Q3 and Q4. Whatever the answer, the page must end still, on one place, in which the marked line
  is visible: no back-and-forth between the two scrolls (J2 records it frame by frame).
- The caret mark (`markEditorSelection` on) and the line marker on the same line: Q9; until
  answered, both show.

### 4.4 Documentation

- `docs/user/open-studio.md`, section "Open at a line": the sentence on jumps that stay text while
  the side preview is open says the side preview now scrolls to the line **and marks it** with the
  arrow and band; cursor moves never mark; whatever J1 proves about in-file commands and other
  extensions (and Q1, Q2) is written there.
- `docs/known-limitations.md`: the limits of section 7 that the trials confirm.
- `.agents/glossary/common.md`: "Jump" becomes "a move of a Markdown text editor to a line asked
  from outside the text (a search result, Quick Open `file.md:40`, a problem, a link), whether it
  opens the editor or moves one already open; the host tells it from a cursor move by a selection
  change of kind Command (`src/core/navigation/jumpSignal.ts`)", adjusted to the answers of Q1 and
  Q2. "Line marker": "in a Studio tab or in the side preview".
- `CHANGELOG.md`: one user-facing line under `## Unreleased`, at the end of the list
  (`.agents/guidelines/release-process.guidelines.md`): "The side preview now marks the line a
  search result, Quick Open `file.md:42`, a problem or a link jumps to, with the same arrow and band
  as the Studio tab; moving the cursor does not."
- The writing skill `skills/writing-for-markdown-okf-schema-studio/` is not touched.

### 4.5 Requirements (okfreq)

Rules: `requirements/guidelines/requirements.guidelines.md` and `project.guidelines.md` ("During a
change"); okfreq run as `uv run --no-sync --group requirements okfreq`. New requirements created
with `okfreq new … --lifecycle proposed`, IDs allocated by okfreq, markers at the code and at each
test, `just requirements-update`, a dated entry in `requirements/tiers/log.md`.

Approved requirements changed: none (the changed ones below are `proposed`; the Driver checks each
one's lifecycle before editing and, if one is `approved`, stops and reports it).

New (scope `lifecycle-sync`, `proposed`):

- SwRS "The host tells a jump from a cursor move": the table of 4.1 (Keyboard and Mouse are cursor
  moves; no kind is not a jump; Command with one selection in an eligible `.md` editor is a jump at
  its first selection's line; several selections or a selection Studio set are not), plus what Q1
  and Q2 add. `@implements_req` on `jumpSignal.ts` and `editorJumps.ts`.
- SwRS "The side preview marks the line of a jump": with the side preview following the editor of
  a `.md` document, a jump into that document or into a document the side preview then switches
  to makes the side preview reveal and mark the line with the line marker of LIFE-178, LIFE-179 and
  LIFE-180; a jump while no side preview is open changes nothing here. Scenarios: search result in a
  file already open; Quick Open `other.md:55` (switch of document); Problems; a link in a text
  editor; a new tab kept by CR-445 rule 6. Plus what Q3 to Q10 add.
- SwRS "A cursor move never marks the side preview": arrow keys, a click in the text, Page Down,
  Ctrl+End, typing, undo leave the side preview without a line marker (and, until Q5 says
  otherwise, leave an existing one where it is).

Changed (each with its reason):

- SwRS-MDOKFSTUDIO-LIFE-181: the requested line belongs to a document; it is posted only when the
  session shows that document, and dropped after the pending window. Why: the side preview changes
  document (4.2).
- SwRS-MDOKFSTUDIO-LIFE-185: the watcher reads the jump from the host's jump signal (the new SwRS)
  instead of its own selection listener. Why: one definition of a jump (4.1). Its behaviour is
  unchanged.
- StRS-MDOKFSTUDIO-LIFE-023 (CR-445's StRS): a main path "with the side preview open, the text
  editor goes to the line and the side preview marks it". Why: decision 1.
- Any CR-445 SwRS or doc that says the side preview "scrolls as today" on a jump (LIFE-184's rule
  6 scenario, `docs/user/open-studio.md`) gains "and marks the line". The policy decision itself
  (keep the text editor) is unchanged.

## 5. Out of scope

- Any change to the opening policy or to when Studio replaces a text editor (CR-445).
- The marker's extra precision (table row, hidden `{tab-item}`, front matter property row): inbox
  item `line-marker-precision`.
- The side preview's gaps next to a diff (scroll sync from a diff, "Open Preview to Side" from the
  replace preview, the title button on a diff): inbox item `side-preview-diff-gaps`. A jump into a
  diff editor is not a jump here (`jumpSignal` requires an eligible saved `file:` `.md` editor; a
  diff side reports its own document scheme, J5 checks a `git:` side).
- A new look or a new lifetime for the marker; a mark on cursor moves.
- The release notes of `docs/releases-notes/` (written at release time).

## 6. Evidence

### 6.1 Host and default matrix

The behaviour depends on settings (shipped defaults versus configured values) and on the host. One
line per cell; "Q" cells take the owner's answer before the trial's expected result is fixed.

| Cell | Settings at start | Expected | Checked by |
| --- | --- | --- | --- |
| Shipped defaults, side preview open | `preview.scrollPreviewWithEditor` on, `preview.markEditorSelection` off, `open.searchResultsInStudio` on, `open.markdownFilesInStudio` off | jump: text editor at the line (CR-445 rule 6), side preview marks the line; cursor move: no marker | J2 to J5, J7 |
| Anchor off | `scrollPreviewWithEditor` off (setting, or the panel's anchor button) | per Q4 | J6 |
| Caret mark on | `markEditorSelection` on | per Q9; the caret mark keeps its own refresh rules | J6 |
| Files on, side preview open | `open.markdownFilesInStudio` on | as shipped defaults (rule 6 applies under either setting) | J7 |
| Search off, side preview open | `open.searchResultsInStudio` off | as shipped defaults, unless Q7 ties the marker to this setting | J7 |
| No side preview | defaults | CR-445 unchanged: Studio tab at the line with its marker | existing `openAtLine.test.ts` |
| Studio tab beside a text editor of the same file | defaults | per Q6 | J6 |
| Host VS Code desktop, Windows and Linux | any | checked (trials on Windows locally, CI integration on Linux) | all trials |
| VS Code for the Web, Remote, macOS, the Agents window | any | untested, labelled so in the PR | none |

If Q7 adds a setting: one more pair of cells (setting on, off), and the settings test reads the
shipped `package.json` (`just check-settings`), not a prepared copy.

### 6.2 Unit and contract tests (each fails on the code at `5a84db8b`)

- `test/core/navigation/jumpSignal.test.ts`: the truth table of 4.1: each kind (`keyboard`,
  `mouse`, `none`, `command`), one and several selections, eligible and not (`untitled:`, `git:`,
  `.txt`), set by Studio and not, the 1-based line; plus the rows Q1 and Q2 add.
- `test/host-vscode/` (fake `vscode` of `test/host/fakeVscode.ts`, whose
  `onDidChangeTextEditorSelection` is fired through `events.changeSelection`): `editorJumps` fires `onJump` for a Command
  event and not for Keyboard, Mouse or no kind; the opening watcher still reads a jump's line
  through it (its existing tests unchanged and green).
- `test/session/` (memory host, `src/host-memory/`): `onEditorJumped` on a side preview that shows
  the document posts `previewRevealLine` once with the line; on a side preview that shows another
  document and then switches to it, posts it once at the page ready of the switched render and not
  before; never posts to a session with `followsActiveEditor` false (until Q6); a pending line of
  document A is not posted when the session renders document B; an expired pending line is
  dropped; with no side preview, does nothing.
- `test/session/` (scroll sync): the Studio tab paths of LIFE-181 (pending line at page ready,
  posted at once when ready, wins over the restored place) still hold with the document-keyed
  pending line.

### 6.3 Real VS Code trials

In `test/integration/openAtLine.test.ts` (trusted suite, `test/integration/realInput/harness.ts`,
`connectWorkbench`, `waitFor`), or a new `test/integration/sidePreviewJump.test.ts` in the same
suite with a row in `INTEGRATION_TESTS` of `test/shared/e2eGroups.ts` (group `lifecycle-sync`).
Settings set with `getConfiguration(...).update(...)` and restored after each case. Each trial runs
on Windows locally and in the CI integration job (Linux; heavy run on the branch:
`gh workflow run ci.yml --ref <branch> -f heavy=true`); results and screenshots in the PR's
evidence. The marker is read in the side preview's webview as `.sphinx-preview-line-marker` (the
class the visual scenarios of CR-445 check).

| Trial | Unproved behaviour | Steps | Settles |
| --- | --- | --- | --- |
| J1 | The kind each entry point carries into an editor already open | `doc.md` open as text, side preview open. Record the `onDidChangeTextEditorSelection` kind and selection count (a test hook in `src/host-vscode/testHooks.ts`) for: Search view click on a match of `doc.md`; Quick Open `doc.md:42` (active file); Problems click on a problem of `doc.md`; Ctrl+click in a text editor on a link `other.md#heading` and on a link to a heading of `doc.md`; a terminal link `doc.md:42`; Go to Line (Ctrl+G); Go to Symbol (`@`); Find (Ctrl+F, Enter, F3); Go to Next Problem (F8); Go Back (Alt+Left); arrow keys; a mouse click; Page Down; Ctrl+End; typing; undo; an API move (`editor.selection = …` from the test, as another extension does) | The table of kinds goes in the PR and in `docs/user/open-studio.md`. Every listed entry point (search, Quick Open `:line`, Problems, links, Ctrl+click) must give `Command` with one selection; one that does not is a known limit (7). The in-file commands and the API move feed Q1 and Q2 with facts |
| J2 | A search result in a file already open marks the side preview | Defaults; `doc.md` in a text editor, side preview open on it; Search view click on a match at line 40. Poll the side preview's scroll position every frame for 2 s | The marker on line 40 in the side preview; the page ends still on one place (Q3) with line 40 visible; the text editor at line 40 |
| J3 | A jump to another file switches and marks | Same start; Quick Open `other.md:55` | The side preview shows `other.md`, the marker on line 55, never on `doc.md` |
| J4 | Cursor moves never mark | Same start, no marker shown; arrow keys over 20 lines, a click on line 70, Page Down, Ctrl+End, typing a word, undo | No `.sphinx-preview-line-marker` in the side preview at any point; the page follows the editor as at 1.11.0 |
| J5 | Problems, links, Ctrl+click, a diff | Problems click on a problem of `doc.md` line 30; Ctrl+click on a link `other.md#heading` in a text editor; a terminal link `doc.md:42`; Source Control Open Changes on `doc.md` then a click in the diff | Each listed jump marks its line in the side preview; the diff marks nothing |
| J6 | The Q cells | Anchor off, then a search click (Q4); caret mark on, then a search click (Q9); a Studio tab of `doc.md` in group 2 beside the text editor, then a search click (Q6); the side preview in a background tab of its group, then a search click, then show it (Q10); after a marker shows, an arrow key, typing, a scroll of the text editor (Q5) | Each per the owner's answer |
| J7 | A new tab kept by CR-445 rule 6 | Defaults, side preview open on `other.md`, `doc.md` not open; Search view click on a match of `doc.md` line 30; then the same with `open.markdownFilesInStudio` on, and with `open.searchResultsInStudio` off | The text editor of `doc.md` stays (no Studio tab), the side preview switches to `doc.md` and marks line 30, in all three settings (unless Q7 ties the last one) |

### 6.4 Visual captures

The look is CR-445's and its scenarios (`test/visual/lineMarkerScenarios.ts`) stay. One new scenario
in that file: the side preview page (with its anchor button) after `previewRevealLine` sent as a
`pageActions` host message (the way CR-445's round 5 fixed the find-bar check), light and dark. The
PR's Impacts section shows a before (1.11.0: the side preview after a search click, no marker; CR-445
evidence `ta-defaults-06-t12-side-preview-jump.png` shows it) and an after from J2, per
`.agents/guidelines/pull-request.guidelines.md`.

### 6.5 Gate

`just check`, `just requirements-update`, `just requirements-lint`, then `just preflight` (on Windows
the static stage; CI runs visual and integration). The heavy CI run on the branch before the PR
leaves draft.

## 7. Known limits to state in the SwRS and the docs (as the trials prove them)

- A listed entry point that J1 shows gives no `Command` change into an open editor does not mark
  the side preview.
- Depending on Q1 and Q2: in-file commands (Go to Line, Find, Go to Symbol, F8) and cursor moves
  made by other extensions through the API (VSCodeVim) carry the same `Command` kind as a jump; the
  host cannot tell them from a search result by the kind alone.

## 8. Delivery notes for the Driver

- Batch: added to the running batch-07 once final and ready (decision 2).
- Commits: Conventional Commits with the allowed scopes (`feat(vscode)` for the jump signal and the
  routing), per `.agents/guidelines/git-commit-message.guidelines.md`.
- Only `src/host-vscode/` imports `vscode`; `jumpSignal.ts` stays in `src/core/` with no host API;
  no dependency-cruiser exception. The 800-line ratchet: `activation.ts` gains only the wiring.
- New worktree: `just dev` first (`.agents/guidelines/local-worktree.guidelines.md`).
- Run J1 first: its table decides the known limits and gives the owner the facts for Q1 and Q2 if
  they are still open.

## 9. Open questions for the owner

1. **Q1, in-file moves.** Do these count as a jump (marker in the side preview): Go to Line
   (Ctrl+G, and Quick Open `:42` in the file already active), Go to Symbol (`@`), Find in the file
   (Enter, F3), Go to Next Problem (F8), Go to Definition or a Ctrl+click to a place in the same
   file, Go Back / Go Forward (Alt+Left)? They are expected to carry the same `Command` kind as a
   search result (J1 will confirm). Options: (a) every `Command` move marks (simplest, all of them
   mark); (b) a move marks only when its line was outside the text editor's visible range before
   (Find hits and search results already on screen then do not mark either); (c) a closed list of
   entry points only, which the extension API cannot tell apart, so it is (a) or (b) in practice.
2. **Q2, other extensions.** VSCodeVim and similar extensions move the cursor through the API: each
   `j`/`k` would look like a jump and mark. Options: accept it as a known limit; exclude a move of
   one line, or within the visible range (as Q1 (b)); exclude while such an extension is active.
3. **Q3, where the line sits.** With scroll sync on, after a jump: the side preview follows the
   editor (the line where the editor shows it), or puts the line at the reading line under the
   sticky headings as the Studio tab does (the editor and the page then show it at different
   heights)?
4. **Q4, anchor off.** With "scroll preview with editor" off (setting or the panel's anchor
   button): on a jump, the side preview scrolls to the line and marks it; marks it only if it is
   already on screen; or does nothing?
5. **Q5, what removes it.** "Same duration" read literally keeps CR-445's rules (scroll keeps it; a
   pointer press in the page, an edit in the page or a new jump removes or moves it). In the side
   preview, should a cursor move in the text editor, typing in the text editor, or a scroll of the
   text editor also remove it?
6. **Q6, other Studio views.** Should a Studio tab of the same file shown beside the text editor,
   or an older side preview that no longer follows the active editor, mark the jump too, or only the
   side preview that follows the editor?
7. **Q7, a setting.** Always on with no setting; a new setting (for example "Mark jumps in the side
   preview", on by default); or tied to an existing one (`open.searchResultsInStudio`, or
   `preview.markEditorSelection`)?
8. **Q8, the side preview's own links.** A link or Back/Next followed in the side preview opens the
   text editor at the target heading, and the side preview follows: mark the target line (it is a
   link the reader followed), or not (the reader clicked in the side preview and already sees
   where they go)?
9. **Q9, the caret mark.** With `preview.markEditorSelection` on, the caret mark and the arrow and
   band fall on the same line after a jump: show both, or hide the caret mark while the line marker
   shows?
10. **Q10, a hidden side preview.** If the side preview is in a background tab of its group at the
    jump: mark the line when it is shown again (only within the few seconds of CR-445's pending
    window, or whenever it is shown next), or never?
