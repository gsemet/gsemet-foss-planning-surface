# Show the target-line arrow in the side preview on a jump

When a jump (a search result, Quick Open `file.md:42`, a problem, a link, a Ctrl+click, Go to
Line, Find, F8, Go to Symbol, Go Back) moves a text editor of a `.md` file to a line while the side
preview follows that editor, the side preview shows the line marker of the Studio tab on that line:
the arrow in the left margin and the light band. A cursor move (arrow keys, a click in the text,
typing) never shows it. A search click with a replace text (the replace preview) marks the line in
the real file.

Origin: verbal (owner). Split off from CR-445 open-at-line-marker, decision 17 (open-at-line-Q12).
No tracker issue. Code base: `origin/main` at `5a84db8b` (release 1.11.0, which ships CR-445),
**stacked after CR side-preview-diff-gaps** (8). Decisions come from `02-answers.md`: jm-Q1 to
jm-Q4 (owner, 2026-11-21) and the points the Chief of Staff settled from "Comme l'onglet Studio"
and CR-445's rules (same file, same day). Every decision is final; section 9 is empty.

## 1. Goal, in the user's terms

- I work in a text editor with the Studio side preview beside it. I click a search result, a
  problem, a link, type Quick Open `doc.md:42` or Go to Line: the text editor goes to the line, and
  the side preview shows me that line with the same arrow and light band as the Studio tab.
- If I clicked a search result with a replace text typed, VS Code shows its replace preview; the
  side preview shows that line of the real `doc.md`, marked.
- When I move my cursor myself (arrow keys, a click in the text, Page Down, typing), the side
  preview behaves as today: no arrow, no band.
- When I then scroll or move the cursor, the marker stays; when I edit the document or the side
  preview switches to another file, it goes.

## 2. Facts at 1.11.0 that shape the design

- The page already has the marker: `src/page/features/lineMarker.ts` (`installLineMarker`, SwRS
  LIFE-178 placement, LIFE-179 lifetime, LIFE-180 edit mode), driven by the host-to-page message
  `previewRevealLine` (`src/core/protocol/hostToPage.ts`, interface `PreviewRevealLineMessage`,
  router entry `previewRevealLine`; page handler in `src/page/features/hostHandlers.ts` line 111:
  `rt.lineMarker.reveal(message.line)`). The reveal always scrolls the line to the reading line.
- The host side is `ScrollSyncController.requestRevealLine` and `postPendingRevealLine`
  (`src/session/features/scrollSync.ts`, SwRS LIFE-181). `postPendingRevealLine` sets the session's
  anchor to the requested line with `owner: "preview"` (line 272). The pending line is posted from
  the page ready handler of `src/session/features/rendering.ts` (line 542).
- `ScrollState.pendingRevealLine` is a bare number: it says neither its document nor its age. The
  Studio tab never changes document; the side preview does (`HostEvents.onActiveEditorChanged`,
  `src/session/hostEvents.ts`, calls `manager.switchAfterFlush`).
- The side preview follows the text editor through the editor's visible ranges only:
  `onDidChangeTextEditorVisibleRanges` (`src/host-vscode/activation.ts`) →
  `HostEvents.onVisibleRangesChanged` → `ScrollSyncController.syncEditorToPreview` (`sourceScroll`
  with the editor's first visible line). On a switch of document, the first render places the page
  at `initialAnchorLine` (the session's anchor of that document, else the editor's first visible
  line when the anchor button is on). No session code listens to selection changes.
- The caret mark (setting `markdownOkfSchemaStudio.preview.markEditorSelection`, off by default,
  SwRS TOOLBAR-128) marks the block of the caret line. It is another mark and stays as it is.
- The only proved jump signal is CR-445's trial T2 (`src/host-vscode/openingWatcher.ts`, glossary
  "Jump"): for a **newly opened** text tab, VS Code shows the editor at 1:1 and then applies the
  requested selection with an `onDidChangeTextEditorSelection` event of kind
  `TextEditorSelectionChangeKind.Command`; a plain reopening restores its view state with an event
  of no kind. `src/host-vscode/keystrokes.ts` reads kind `Keyboard` as typing. The kinds of a jump
  into an editor already open, of the in-file commands and of an extension's API move are not
  observed yet: trial J1.
- When a jump opens a new text tab while the side preview follows the active editor, CR-445 keeps
  the text editor (opening policy rule 6, `src/core/navigation/openingPolicy.ts`, SwRS LIFE-184):
  the side preview only scrolls. This CR keeps that decision and adds the marker.
- `StudioOpenedTextEditors` (`src/host-vscode/openInStudio.ts`) records a **URI** for a few seconds
  whenever Studio opens a text editor: "Open as Text" (`activation.ts` line 284, with a selection),
  `openPreview`, and `navigation.showDocument` (`src/host-vscode/vscodeHost.ts`, with the link's
  selection). It cannot tell Studio's own selection from a user's jump into the same file a moment
  later, so it is not the discriminator here (4.1).
- The side preview's links (`src/session/features/links.ts`) and Back/Next across documents
  (`history.ts`) call `host.navigation.showDocument(targetId, selection)`; from a Studio tab they
  call `showDocumentInStudio(targetId, line)` and the Studio tab marks the line (SwRS LIFE-182). An
  anchor link or Back/Next inside the same document scrolls the page (`sourceScroll` path) and
  marks nothing in the Studio tab.
- A search click with a replace text opens VS Code's replace preview, a text diff whose original
  side is the real file and whose modified side is a virtual document (CR-445
  `work/diff-view-findings.md`). CR side-preview-diff-gaps adds the reading of "the real file of a
  diff" in `src/host-vscode/` (its section 4.1: modified side when it is an eligible file, else the
  original side, else none); this CR uses it.

## 3. Decisions carried

| # | Decision (from `02-answers.md`) | Where in this spec |
| --- | --- | --- |
| 1 | jm-Q1: "Comme l'onglet Studio": same arrow, same light band, same duration, reusing CR-445's marker; only on a jump, never on a cursor move | 4.1, 4.3 |
| 2 | Owner: once final and ready, added to the running batch-07 | 8 |
| 3 | jm-Q2: with "scroll preview with editor" off, a jump scrolls the side preview to the line and marks it | 4.3 |
| 4 | jm-Q3: moves VS Code cannot tell from a search click (F3, F8, Go to Symbol, Go Back, VSCodeVim `j`/`k`) all mark; Vim is a written known limit; trial J1 runs first and records the real kinds | 4.1, 6.3 (J1), 7 |
| 5 | jm-Q4: a jump into the replace preview marks that line of the real file, if J5 proves the jump can be detected on a diff side; this CR stacks after side-preview-diff-gaps | 4.1 (diff sides), 6.3 (J5), 7, 8 |
| 6 | CoS: every `Command` move with one selection marks; Go to Line and Quick Open `:line` are jumps | 4.1 |
| 7 | CoS: with the anchor on, the editor leads: the reveal marks without its own scroll to the reading line, `postPendingRevealLine` does not take the anchor, and on a switch of document the first render takes the editor's first visible line | 4.2, 4.3 |
| 8 | CoS: scroll and cursor moves keep the marker; an edit of the document or a switch to another document removes it; the PR body says how "same duration" is read | 4.4, 8 |
| 9 | CoS: only the side preview that follows the editor marks | 4.2 |
| 10 | CoS: no setting | 4.2 |
| 11 | CoS: the side preview's own links mark the target line; Back/Next inside the same document do not | 4.5 |
| 12 | CoS: the caret mark and the line marker both show | 4.3 |
| 13 | CoS: a hidden side preview gets the line at its next page ready within `PENDING_LINE_WINDOW_MS`, else it is dropped; a line is posted only to a visible page | 4.2 |

## 4. What changes

### 4.1 Telling a jump from a cursor move (host)

The host reads the kind of the selection change VS Code reports, the signal CR-445 proved for new
tabs. Every `Command` move with one selection is a jump (decisions 4, 6):

| Selection change | Read as |
| --- | --- |
| kind `Keyboard` (arrow keys, Page Down, Ctrl+End, typing, a keybinding) | cursor move, never a jump |
| kind `Mouse` (a click or a drag in the text) | cursor move, never a jump |
| no kind (a restored view state, undo or redo, an edit's side effect) | not a jump |
| kind `Command`, several selections | not a jump |
| kind `Command`, one selection, matching an expected Studio selection (below) | not a jump (Studio already handles it) |
| kind `Command`, one selection, in an editor of an eligible saved `file:` `.md` document | a jump into that document, at line `selections[0].start.line + 1` |
| kind `Command`, one selection, in a side of a text diff whose real file is an eligible `.md` | a jump into the real file, at the line of 4.1 "Diff sides" |
| anything else | not a jump |

The line is always the first selection's start line: for Find on a match, the match's line; for a
search result, the match's line.

Kinds VS Code reports are taken as they are (decision 4): Go to Line, Quick Open `:line` in the
active file, Find (Enter, F3), Go to Next Problem (F8), Go to Symbol, Go to Definition in the same
file, Go Back / Go Forward and a cursor move by another extension through the API all mark when J1
shows they carry `Command` with one selection; whatever J1 shows carries another kind does not, and
J1's table goes in the docs.

**Expected Studio selections (the discriminator).** New class `StudioSelections` in
`src/host-vscode/openInStudio.ts`, separate from `StudioOpenedTextEditors` (which keeps its CR-445
role in the opening watcher, unchanged):

- `expect(uri, line0, purpose)` is called just before Studio opens a text editor **with a
  selection**: "Open as Text" (purpose `no-mark`, `activation.ts`), and `navigation.showDocument`
  when it carries a selection (purpose `marked-by-session`, `vscodeHost.ts`; the session marks the
  line itself, 4.5).
- `take(uri, line0)` returns and removes the entry only when the URI **and** the 0-based line match,
  within `STUDIO_SELECTION_WINDOW_MS` (1000 ms: T2 measured the selection a few milliseconds after
  the editor shows) of `expect`. An entry is used once; unmatched entries expire.
- So a user's jump into the same file within seconds of "Open as Text" is never swallowed: it is
  another event (the entry is already used) or another line. The case left is a user jump to the
  very same line within the first second, which is marked as Studio's own (stated in the SwRS).

**Diff sides** (decision 5). When the event's editor is a side of the active tab and that tab is a
`vscode.TabInputTextDiff` (its `original` or `modified` URI equals the editor's document URI), the
jump goes to the diff's real file as side-preview-diff-gaps reads it. The line: the selection's line
when the selection is on the real file's side; when it is on the other side, the same line number
(the line of a match in the replace preview is the same on both sides unless an earlier replacement
in the file adds or removes lines: a known limit, 7). A diff with no real file gives no jump. J5
proves which side receives the selection and whether a `Command` change comes at all; if none comes,
a jump into a diff does not mark and that is a known limit (7), the rest ships.

**Where it lives.**

- The rules are a pure function in a new file `src/core/navigation/jumpSignal.ts` (no host API):
  input: the change kind (`keyboard`, `mouse`, `command`, `none`), the number of selections, the
  first selection's 0-based start line, the target (`file` with eligibility, `diff-side` with the
  real file's eligibility and which side, or `other`), and whether it matched an expected Studio
  selection; output `{ jump: false }` or `{ jump: true, line }` (1-based, in the target real file).
- New file `src/host-vscode/editorJumps.ts`, the only listener of
  `vscode.window.onDidChangeTextEditorSelection` for jumps: it builds the facts (the kind from
  `vscode.TextEditorSelectionChangeKind`, the diff tab and its real file through
  side-preview-diff-gaps's reading, `StudioSelections.take`), asks `jumpSignal`, and fires
  `onJump({ uri, line, at })` with the real file's URI. Created in `StudioActivation.start`
  before the opening watcher.
- The opening watcher (`openingWatcher.ts`) stops listening to the selection itself: its
  `watchJumps` listener is replaced by a subscription to `editorJumps.onJump`. Its own narrower use
  stays: it reads a jump only for a text tab it just saw open, inside `JUMP_SETTLE_MS`, and every
  CR-445 decision is unchanged. A jump `editorJumps` drops as Studio's own (an "Open as Text"
  selection) was already kept by the watcher's rule 4 (`StudioOpenedTextEditors`), so the watcher
  sees no change. Its existing tests and `test/integration/openAtLine.test.ts` pass unchanged.

### 4.2 From the jump to the side preview

- New host-neutral event `HostEvents.onEditorJumped(documentId: string, line: number)` in
  `src/session/hostEvents.ts`, wired in `activation.ts` from `editorJumps.onJump`
  (`host.documents` gives the id of the URI).
- It targets only the side preview that follows the editor (decision 9): the latest live session
  with `followsActiveEditor` true (`manager.latest((preview) => preview.followsActiveEditor)`). A
  Studio tab, or an older side preview that no longer follows, marks nothing. No setting gates it
  (decision 10). With no side preview open, nothing happens here (CR-445 puts the Studio tab in
  place with its marker, as today).
- When that side preview shows the document, or will show it because the jump makes its editor
  active, the session calls `manager.scroll.requestRevealLine(preview, line, { documentId,
  scroll })` (4.3 for `scroll`).
- `ScrollState.pendingRevealLine` becomes `{ line: number; documentId: string; at: number; scroll:
  RevealScroll }`. `postPendingRevealLine` posts only when all hold: the session's stage shows that
  document (`preview.documentUri === documentId`), the page is ready for the current stage, the
  panel is visible (`PreviewPanel.visible`, `src/host-api/previewPanel.ts`), and the line is younger
  than `PENDING_LINE_WINDOW_MS` (5000 ms; moved from `openInStudio.ts` to a host-neutral module the
  session imports, for example `src/core/navigation/`). A line past the window is dropped.
- A jump and the switch of document arrive in either order: the line waits on the session and is
  posted at the page ready of the render that shows its document (`rendering.ts`, the existing
  call), or at once when the page already shows it and is visible.
- A hidden side preview (decision 13): the line waits; a hidden webview reloads when shown and
  reports ready, and the line is posted then if still inside the window, else dropped.
- The Studio tab's calls (`activation.ts` lines 90 and 406) pass their own document and
  `scroll: "reading-line"`; their behaviour is unchanged (LIFE-181), apart from the visibility
  condition, which holds for them (a Studio tab is revealed before its line is sent).
- A jump that opens a new text tab while the side preview is open goes through CR-445 rule 6 (the
  text editor stays) and, through `editorJumps`, marks the side preview like any other jump.

### 4.3 The marker in the side preview and the scroll

- Same page feature, same look, same placement (decision 1): `lineMarker.ts`, the styles of
  `src/core/preview/styles/lineMarkerStyles.ts`, SwRS LIFE-178 (placement) and LIFE-180 (edit mode)
  apply; unfolding a folded section or a closed dropdown that hides the line happens as in the
  Studio tab.
- **Protocol.** `PreviewRevealLineMessage` gains an optional field `scroll?: "reading-line" |
  "if-off-screen"` (absent means `"reading-line"`, so a page or a message of CR-445 behaves as
  today). The router accepts only these two values and refuses any other. `hostHandlers.ts`
  passes it: `rt.lineMarker.reveal(message.line, message.scroll ?? "reading-line")`.
- **Page.** `LineMarker.reveal(line, scroll)`: with `"reading-line"`, as today. With
  `"if-off-screen"`, it unfolds, measures, draws the marker, and scrolls (to the reading line, the
  same silent scroll) **only** when the line's box is not inside the viewport below the sticky
  heading band; otherwise the page does not move. Neither posts `previewScroll`.
- **Which scroll the host asks** (decisions 3, 7), decided in the session from the side preview's
  live anchor setting (`preview.configuration.scrollPreviewWithEditor`, which the anchor button
  changes):
  - anchor on: `"if-off-screen"`. The editor leads: scroll sync places the page from the editor's
    reveal of the line as today, and the marker is drawn where the line is. `postPendingRevealLine`
    does **not** set `preview.scroll.anchor` for a following side preview with the anchor on; on a
    switch of document the first render keeps today's `initialAnchorLine` (the editor's first
    visible line).
  - anchor off: `"reading-line"`; the page scrolls to the line and marks it, and the session's
    anchor takes the line (`owner: "preview"`), as for the Studio tab.
- The page must end still on one place where the marked line is visible, with no back-and-forth
  between the reveal and scroll sync (J2 records the scroll position frame by frame).
- With `markEditorSelection` on, the caret mark and the line marker both show (decision 12).

### 4.4 Lifetime in the side preview

Decision 8, "same duration" read with CR-445's rules:

- Kept: scrolls of the page or of the text editor, cursor moves in the text editor, re-renders,
  content patches without an edit of the document, layout changes (LIFE-179).
- Removed: a pointer press in the page and an edit started in the page (LIFE-179, unchanged); **an
  edit of the document from the text editor** (any `DocumentChange` of the shown document that the
  page did not post); a **switch of the side preview to another document**. Moved: by the next jump.
- Host: the session remembers that its page shows a marker (`ScrollState.markedLine?: { line,
  documentId }`, set when `previewRevealLine` is posted). `HostEvents.onDocumentChanged` (the
  existing handler of `host.documents.onDidChange`), for the following side preview whose marked
  document changed, posts a new message `previewLineMarkerClear` (`hostToPage.ts`, addressing
  `render`, no payload beyond the envelope; router entry next to `previewRevealLine`) and clears
  `markedLine`. On a switch of document, `markedLine` and any pending line of the old document are
  cleared, and the page of the new document draws no marker (the page's marker belongs to its
  `context.documentId`; the page's `installLineMarker` clears on a render of another document).
- Page: `hostHandlers.ts` maps `previewLineMarkerClear` to `rt.lineMarker.clear()`.
- The Studio tab's lifetime is not changed: the clear message is sent only to the following side
  preview.

### 4.5 The side preview's own links and history

Decision 11. In `src/session/features/links.ts` and `src/session/features/history.ts`, when the
session is the following side preview and it calls `host.navigation.showDocument(targetId,
selection)` with a selection (a link to another file, with or without a heading or a line; Back/Next
to another document), it also calls `manager.scroll.requestRevealLine(preview, selection.start.line +
1, { documentId: targetId, scroll })`, with `scroll` per 4.3. The line is given explicitly, as the
Studio tab's navigation passes it to `showDocumentInStudio`, and `showDocument` records the expected
selection in `StudioSelections` (purpose `marked-by-session`), so `editorJumps` does not mark it a
second time. A link with no line or heading (the top of a file) gives no selection and no marker, as
in the Studio tab. An anchor link or Back/Next inside the same document keeps today's in-page
scroll and marks nothing, as in the Studio tab.

### 4.6 Documentation

- `docs/user/open-studio.md`, section "Open at a line": the sentence on jumps that stay text while
  the side preview is open says the side preview now scrolls to the line and marks it with the
  arrow and band; the anchor button's effect (on: the preview follows the editor; off: the preview
  scrolls to the line); cursor moves and scrolls keep the marker, an edit or another file removes
  it; the side preview's links mark their target; a search click with a replace text marks the real
  file's line; J1's table of what marks.
- `docs/known-limitations.md`: the limits of section 7.
- `.agents/glossary/common.md`:
  - "Jump": "a move of a Markdown text editor to a line by a command (a search result, Quick Open
    `file.md:40`, a problem, a link, Go to Line, Find, F8): a selection change of kind Command with
    one selection (`src/core/navigation/jumpSignal.ts`); a cursor move by keyboard or mouse is never
    a jump. The opening watcher uses only the jumps into a text tab it just saw open."
  - "Line marker": "… in a Studio tab or in the side preview that follows the editor; in the side
    preview an edit of the document or a switch of file also removes it."
- `CHANGELOG.md`: one user-facing line under `## Unreleased`, at the end of the list
  (`.agents/guidelines/release-process.guidelines.md`): "The side preview now marks the line a
  search result, Quick Open `file.md:42`, a problem, a link or another jump moves the text editor
  to, with the same arrow and band as the Studio tab; moving the cursor does not."
- The writing skill `skills/writing-for-markdown-okf-schema-studio/` is not touched (no rendered
  syntax changes).

### 4.7 Requirements (okfreq)

Rules: `requirements/guidelines/requirements.guidelines.md` and `project.guidelines.md` ("During a
change"); okfreq as `uv run --no-sync --group requirements okfreq`. New requirements with `okfreq
new … --lifecycle proposed`, IDs allocated by okfreq, markers at the code and at each test, `just
requirements-update`, a dated entry in `requirements/tiers/log.md`.

Approved requirements changed: none (LIFE-178 to LIFE-185 and StRS-MDOKFSTUDIO-LIFE-023 are
`proposed`; the Driver checks each lifecycle before editing and stops and reports an `approved` one).

New (scope `lifecycle-sync`, `proposed`):

- SwRS "The host tells a jump from a cursor move": the table of 4.1, expected Studio selections
  (URI and line, once, within 1 s; the same-line-within-a-second case stated), diff sides through
  the real file. `@implements_req` on `jumpSignal.ts`, `editorJumps.ts`, `StudioSelections`.
- SwRS "The side preview that follows the editor marks the line of a jump": routing (only the
  following side preview, document-keyed line, either order of jump and switch, visible page,
  hidden page within the window, else dropped), no setting. Scenarios: search result in a file
  already open; Quick Open `other.md:55`; Problems; Go to Line; a new tab kept by CR-445 rule 6; the
  replace preview (or "Known issue" per J5).
- SwRS "The side preview's scroll on a jump follows the anchor setting": anchor on, `if-off-screen`,
  no anchor taken, first render at the editor's line; anchor off, reading line, anchor taken.
- SwRS "The line marker of the side preview goes on an edit of the document or a switch of file":
  4.4, with "cursor moves and scrolls keep it".
- SwRS "A cursor move never marks the side preview": Keyboard and Mouse moves, no-kind changes.
- SwRS "Links and Back/Next followed in the side preview mark their target line": 4.5.

Changed (each with its reason):

- SwRS-MDOKFSTUDIO-LIFE-178: the reveal takes an optional scroll mode; `if-off-screen` scrolls only
  when the line is off screen. Why: decision 7.
- SwRS-MDOKFSTUDIO-LIFE-181: the requested line belongs to a document and an age, is posted only to
  a visible page showing that document within the window, and takes the anchor except for a
  following side preview with the anchor on. Why: decisions 7 and 13.
- SwRS-MDOKFSTUDIO-LIFE-185: the watcher reads jumps from the host's jump signal instead of its own
  listener; behaviour unchanged. Why: one definition of a jump.
- StRS-MDOKFSTUDIO-LIFE-023: a main path "with the side preview open, the text editor goes to the
  line and the side preview marks it". Why: decision 1.
- LIFE-184's rule 6 scenario and `docs/user/open-studio.md` ("the side preview scrolls as today")
  gain "and marks the line". The policy decision (keep the text editor) is unchanged.

Sibling CR line-marker-precision changes `lineMarker.ts` placement (table row, hidden tab, front
matter row). This CR reuses the placement as it is and changes only `reveal`'s scroll mode and the
clear message; whichever of the two merges second rebases and renumbers its visual scenarios and its
new LIFE ids.

## 5. Out of scope

- Any change to the opening policy or to when Studio replaces a text editor (CR-445).
- The placement precision of line-marker-precision.
- The side preview next to a diff beyond the jump (title button, "Open Preview to Side" from the
  replace preview, scroll from a diff): CR side-preview-diff-gaps, on which this CR stacks.
- A mark in a Studio tab or in a side preview that no longer follows (decision 9); a setting
  (decision 10).
- A new look for the marker; a mark on cursor moves.
- The release notes of `docs/releases-notes/` (written at release time).

## 6. Evidence

### 6.1 Host and default matrix

| Cell | Settings at start | Expected | Checked by |
| --- | --- | --- | --- |
| Shipped defaults, side preview open | `preview.scrollPreviewWithEditor` on, `preview.markEditorSelection` off, `open.searchResultsInStudio` on, `open.markdownFilesInStudio` off | jump: text editor at the line (CR-445 rule 6), side preview marks the line where scroll sync places it; cursor move: no marker | J2 to J5, J7 |
| Anchor off (setting off, or the panel's anchor button off) | `scrollPreviewWithEditor` off | jump: the side preview scrolls the line to the reading line and marks it | J6 |
| Caret mark on | `markEditorSelection` on | both marks on the jump line | J6 |
| Files on, side preview open | `open.markdownFilesInStudio` on | as shipped defaults (rule 6 applies under either setting) | J7 |
| Search off, side preview open | `open.searchResultsInStudio` off | as shipped defaults (no setting gates the side preview marker) | J7 |
| No side preview | defaults | CR-445 unchanged: Studio tab at the line with its marker | existing `openAtLine.test.ts` |
| Studio tab beside a text editor of the same file, no side preview | defaults | the Studio tab marks nothing on a jump into the open text editor | J6 |
| Host VS Code desktop, Windows and Linux | any | checked (trials on Windows locally, CI integration on Linux) | all trials |
| VS Code for the Web, Remote, macOS, the Agents window | any | untested, labelled so in the PR | none |

### 6.2 Unit and contract tests (each fails on the code at `5a84db8b`)

- `test/core/navigation/jumpSignal.test.ts`: every row of 4.1: each kind, one and several
  selections, eligible and not (`untitled:`, `git:`, `.txt`), matched Studio selection, diff side
  on the real file's side and on the other side, diff with no real file, the 1-based line.
- `StudioSelections` (host test with the fake `vscode` of `test/host/fakeVscode.ts`, whose
  `onDidChangeTextEditorSelection` is fired through `events.changeSelection`): `take` matches only
  the same URI and line inside 1 s, once; after "Open as Text" records line 10, a `Command` event on
  line 40 of the same URI within the window is a jump; a second event on line 10 after the first was
  taken is a jump.
- `editorJumps`: fires `onJump` for a `Command` event with one selection, not for Keyboard, Mouse,
  no kind or several selections; maps a diff side to the real file's URI (fake
  `TabInputTextDiff`). The opening watcher's existing tests stay green through the subscription.
- Protocol (`test/core/protocol/`): `previewRevealLine` accepts `scroll` absent, `"reading-line"`
  and `"if-off-screen"`, refuses any other value; `previewLineMarkerClear` is accepted with the
  render envelope.
- Page (`test/page/runtimeLineMarker.test.ts`): `reveal(line, "if-off-screen")` with the line on
  screen draws the marker and leaves `scrollY` unchanged; with the line off screen scrolls it to the
  reading line; unfolds a folded section in both modes; posts no `previewScroll`;
  `previewLineMarkerClear` removes the marker; absent `scroll` behaves as CR-445 (its tests
  unchanged).
- Session (`test/session/`, memory host `src/host-memory/`): `onEditorJumped` on the following side
  preview showing the document posts `previewRevealLine` once, with `"if-off-screen"` when the anchor
  is on and `"reading-line"` when off; anchor on: `preview.scroll.anchor` is not changed by the post,
  and a switch of document renders at the editor's first visible line; anchor off: the anchor takes
  the line; a jump before the switch posts at the switched render's page ready, not before; a
  pending line of document A is not posted when B renders; a hidden panel gets the line at its next
  page ready inside 5 s and not after; nothing posted to a session with `followsActiveEditor` false;
  a text-editor edit of the marked document posts `previewLineMarkerClear` once; a page-posted edit
  does not post it; a cursor move or scroll does not; links and Back/Next to another document from
  the side preview request the target line, inside the same document they do not.
- Scroll sync: LIFE-181's Studio tab paths (pending line at page ready, at once when ready, wins over
  the restored place, takes the anchor) still hold.

### 6.3 Real VS Code trials

In the trusted suite (`test/integration/trusted-suite.ts`, `test/integration/realInput/harness.ts`,
`connectWorkbench`, `waitFor`), a new `test/integration/sidePreviewJump.test.ts` with a row in
`INTEGRATION_TESTS` of `test/shared/e2eGroups.ts` (group `lifecycle-sync`). Settings set with
`getConfiguration(...).update(...)` and restored after each case. Each trial runs on Windows locally
and in the CI integration job (Linux; heavy run on the branch: `gh workflow run ci.yml --ref
<branch> -f heavy=true`); results and screenshots in the PR's evidence. The marker is read in the
side preview's webview as `.sphinx-preview-line-marker`. **J1 runs first.**

| Trial | Unproved behaviour | Steps | Settles |
| --- | --- | --- | --- |
| J1 | The kind each move carries | `doc.md` open as text, side preview open. A test hook in `src/host-vscode/testHooks.ts` records each `onDidChangeTextEditorSelection` kind, selection count and first line, and each `onJump`, for: Search view click on a match of `doc.md`; Quick Open `doc.md:42` (active file); Go to Line (Ctrl+G); Problems click; Ctrl+click on a link `other.md#heading` and on a link to a heading of `doc.md` in a text editor; a terminal link `doc.md:42`; Go to Symbol (`@`); Find on a match (Ctrl+F, Enter, F3); Go to Next Problem (F8); Go Back (Alt+Left); a link and a Back/Next followed in the side preview; an edit committed from the page in edit mode; a cursor command run from the Command Palette ("Go to Bracket"); Ctrl+A; Ctrl+D; Format Document; arrow keys; a mouse click; Page Down; Ctrl+End; typing; undo; an API move (`editor.selection = …` from the test, as VSCodeVim does) | The table of kinds and of which moves marked goes in the PR and in `docs/user/open-studio.md`. The owner's list (search, Quick Open `:line`, Problems, links, Ctrl+click) must mark; one that gives another kind is a known limit (7). Ctrl+A, Ctrl+D, Format Document, typing, an edit from the page must not mark (if one carries `Command` with one selection it marks by decision 6, and J1 records it as a limit). A link or Back/Next followed in the side preview marks once, not twice |
| J2 | A search result in a file already open, anchor on | Defaults; `doc.md` in a text editor, side preview open; Search view click on a match at line 40. Poll the side preview's `scrollY` every frame for 2 s | The marker on line 40; the page ends still on one place with line 40 visible, placed by scroll sync (no move to the reading line when line 40 is already on screen); the text editor at line 40 |
| J3 | A jump to another file switches and marks | Same start; Quick Open `other.md:55` | The side preview shows `other.md`, first render at the editor's first visible line, the marker on line 55, never drawn on `doc.md` |
| J4 | Cursor moves never mark; the marker's lifetime | Same start, no marker; arrow keys over 20 lines, a click on line 70, Page Down, Ctrl+End, typing, undo; then a search click to line 40 (marker shown), arrow keys, a scroll of the editor and of the page, then a word typed in the text editor; then a new marker and Quick Open `other.md` (switch) | No marker during the first moves; the marker stays through the arrows and scrolls; it goes on the typed word; it goes on the switch and does not come back on returning to `doc.md` |
| J5 | Problems, links, the replace preview | Problems click on a problem of `doc.md` line 30; Ctrl+click on a link `other.md#heading`; a terminal link `doc.md:42`; Search with a replace text, click a match at line 25 of `doc.md` (replace preview opens); Source Control Open Changes on `doc.md` | Each marks its line. Replace preview: the side preview (on the real `doc.md`) marks line 25; J5 records which side got the `Command` change. No `Command` change on a diff side: the replace preview case is a known limit (7), the rest ships. Whatever Open Changes reports is recorded (a `Command` change marks by decision 6) |
| J6 | Other cells | Anchor off (panel button), search click on line 40 with line 40 off screen in the page; caret mark on, search click; no side preview, a Studio tab of `doc.md` in group 2 beside its text editor, search click; side preview in a background tab of its group, search click, show it within 5 s, then again showing it after 6 s | Anchor off: the page scrolls line 40 to the reading line, marker on it. Caret mark: both marks. Studio tab: no marker. Hidden: marker after showing within 5 s; none after 6 s |
| J7 | A new tab kept by CR-445 rule 6 | Defaults, side preview open on `other.md`, `doc.md` not open; search click on a match of `doc.md` line 30; again with `open.markdownFilesInStudio` on; again with `open.searchResultsInStudio` off | In all three, the text editor of `doc.md` stays (no Studio tab), the side preview switches to `doc.md` and marks line 30 |

### 6.4 Visual captures

CR-445's scenarios (`test/visual/lineMarkerScenarios.ts`) stay. One new scenario in that file: the
side preview page (with its anchor button) after `previewRevealLine` with `scroll: "if-off-screen"`
sent as a `pageActions` host message (the way CR-445's round 5 avoided the find-bar check clearing
the marker), light and dark. The PR's Impacts section shows a before (1.11.0: the side preview after
a search click, no marker; CR-445 evidence `ta-defaults-06-t12-side-preview-jump.png`) and an after
from J2, per `.agents/guidelines/pull-request.guidelines.md`.

### 6.5 Gate

`just check`, `just requirements-update`, `just requirements-lint`, then `just preflight` (on Windows
the static stage; CI runs visual and integration). The heavy CI run on the branch before the PR
leaves draft.

## 7. Known limits stated in the SwRS and the docs

- Cursor moves made by other extensions through the API (VSCodeVim `j`/`k`) carry the same `Command`
  kind as a jump and mark the side preview (decision 4; always written).
- In-file commands that carry `Command` with one selection (Find, F8, Go to Symbol, Go Back, and any
  other J1 lists) mark, as a search result does (decision 4).
- A listed jump that J1 shows gives no `Command` change does not mark.
- A user jump to the very line Studio just selected, within one second of "Open as Text" or of a
  side preview link, is taken as Studio's own.
- Replace preview: if J5 finds no detectable `Command` change on a diff side, a search click with a
  replace text does not mark; when it does, the line is the match's line number, which is off when
  an earlier replacement in the same file adds or removes lines.

## 8. Delivery notes for the Driver

- **Stacking:** this CR stacks **after** CR side-preview-diff-gaps
  (`.agents/guidelines/stacked-prs.guidelines.md`): its branch starts from that CR's branch and its
  PR's base is that CR's branch, because 4.1 uses the real-file reading of a diff that
  side-preview-diff-gaps adds. Both touch `scrollSync.ts` and `hostEvents.ts`; rebase on its final
  head before the gate.
- Batch: added to the running batch-07 once final and ready (decision 2).
- Run J1 first: its table fixes the known limits and the docs.
- Commits: Conventional Commits with the allowed scopes (`feat(vscode)` for the jump signal and the
  routing, `feat(render)` for the page's scroll mode and clear message), per
  `.agents/guidelines/git-commit-message.guidelines.md`.
- Only `src/host-vscode/` imports `vscode`; `jumpSignal.ts` stays in `src/core/` with no host API;
  no dependency-cruiser exception. The 800-line ratchet: `activation.ts` gains only the wiring.
- New worktree: `just dev` first (`.agents/guidelines/local-worktree.guidelines.md`).
- The PR body says, in one line, how "same duration" is read (decision 8): in the side preview the
  marker keeps CR-445's rules and also goes on an edit of the document from the text editor or a
  switch to another file; scrolls and cursor moves keep it.
- The PR body says decisions 6 to 13 were settled by the Chief of Staff from the owner's "Comme
  l'onglet Studio" and CR-445's rules.

## 9. Open questions for the owner

None.
