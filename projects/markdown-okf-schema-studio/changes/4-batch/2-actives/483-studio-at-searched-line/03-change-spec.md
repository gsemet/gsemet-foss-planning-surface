# Open Studio at a searched line without replacing text tabs

A reader who jumps to a line of a Markdown file (a search result, Quick Open `file.md:42`, a link,
the Problems panel, Go to Symbol) and reads it in Studio sees that line, and an explicit request
for the raw text is never replaced by Studio. Proof first: a real VS Code window shows what VS Code
hands Studio under the `*.md` association; Studio opens at the line where a reliable signal exists,
and an explicit gesture "Open in Studio at This Line" covers the rest. Links, Back and Next followed
inside a Studio tab open their target at its line or anchor, and Back returns to the place left.

Short name: `searched-line`. Origin: verbal (owner, 2026-11-23, split of CR-477
`raw-text-opens-studio`, answer raw-text-Q6). No issue. Priority P1; the owner calls it "une
feature intéressante mais moins importante".

Code repository: `markdown-okf-schema-studio`, `main` at `80d482fd` (version 1.12.1). Read its
`AGENTS.md` and `.agents/constitution.md` before any change; this specification links to those
rules and does not restate them.

## 1. Goal

Today (1.12.1):

- With the shipped default (no editor association), a jump opens the text editor at the line; the
  side preview, when open, marks the line. Nothing opens Studio at a line.
- With `"workbench.editorAssociations": { "*.md": "markdown-okf-schema-studio.editor" }`, a jump
  opens a Studio tab at the top of the file: VS Code opens the custom editor and drops the
  selection (measured by CR-477 on VS Code 1.143). The side preview marks nothing.
- A link, Back or Next followed inside a Studio tab opens its target as VS Code decides: under the
  association a Studio tab at the top, without the line (CR-477 decision raw-text-Q10).

After this change:

- Where VS Code hands Studio a reliable signal of the line, a jump under the association opens
  Studio at that line, with the page's line marker, and the side preview marks it too.
- Where it hands none, the reader has an explicit gesture: the jump opens the text at the line (the
  shipped default) and the command **Open in Studio at This Line** opens Studio there.
- A link, Back or Next followed inside a Studio tab opens the target at its line or anchor, and Back
  returns to the place left.
- An explicit request for the raw text (**Open as Text**, **Open With... > Text Editor**,
  **Reopen Editor With... > Text Editor**) gives the text and it stays. No code of the extension
  closes or replaces a text tab without the reader's own gesture asking for Studio.

## 2. Decisions of the owner (from `02-answers.md`, all carried)

| # | Question | Decision | Where |
| --- | --- | --- | --- |
| Q1 | Approach | Proof first, in a real window: find what VS Code hands Studio under the `*.md` association (a `#L<n>` fragment, the search state, Quick Open's line). With a reliable signal, Studio opens at the line; with none, an explicit gesture: the jump opens the text at the line and a button or keybinding "Open in Studio at This Line" opens Studio there. No automatic replacement of a text tab | 4, 5.1, 5.2, 7.1 |
| Q2 | Navigation inside Studio | In scope: a link, Back or Next followed inside Studio opens the target at its line or anchor, and Back returns to the previous position | 5.3 |
| Q3 | Side preview marker under the association | In scope, following Q1: with a signal the side preview marks the line; without one the limitation stays documented | 5.1, 5.6 |
| Q4 | Real-window proofs | Every common entry: a search result, Quick Open `file.md:42`, a link from another file, the Problems panel, Go to Symbol, Back and Next; each with and without the association, and with "Reopen Editor With > Text Editor" to prove the text is never replaced | 7.3 |
| Q5 | Grilled enough | Specify, for the next batch (3-ready). Spec critic: yes (host behaviour and what the owner sees at opening) | this file |
| Q6 | "Open in Studio at This Line" from a text tab | The text tab stays; a Studio tab opens in the same group, at the line | 5.2, 5.4, 7.3 |
| Q7 | Default keybinding | None: the editor title menu and the palette only | 5.2 |
| Q8 | Under the association, an entry with no signal | Accepted: Studio opens at the top, the limitation is documented, the command is the fallback | 5.2, 5.6, 6 |
| Q9 | VS Code's Go Back / Go Forward between Studio tabs | Proved too, in a real window: Go Back returns to the Studio tab left, at its position; Go Forward redoes the jump | 5.3, 7.3 |
| Q10 | A link to another file in a preview that does not follow the editor (TOOLBAR-059) | Studio tabs (the custom editor) record it; fixed previews restored by VS Code keep today's rule; TOOLBAR-059, its test (`test/session/toolbarReq.requirements.test.ts:306`) and the `links.ts:291` comment are amended in this CR | 5.3, 5.5, 7.2 |
| Q11 | Back or Next to a file whose Studio tab is open in another group | Reveal the existing Studio tab in its own group, at the line; proved in a real window (a row in 7.3) | 5.3, 7.3 |
| Q12 | A link reveals a Studio tab already open with its own history | Only a Studio tab the link creates shares the source's history; an existing tab keeps its own and the move is appended to it | 5.3, 7.2, 7.3 |
| Q13 | Default settings, a link in a Studio tab opens the target as text | Not recorded: a Studio tab records a link to another file only when the target opens in a Studio tab; the default stays as today | 5.3, 7.2, 7.3 |
| Q15 | A link (not Back or Next) to a file whose Studio tab is open in another group | Reveal that tab in its own group, at the line, the same rule as Q11: no second Studio tab | 5.3, 7.2, 7.3 |
| 14 | Chief of Staff routine (spec critic F5, F6) | F5: the palette clause is `resourceExtname == .md && !activeCustomEditorId`, and the title-menu placement drops "next to Open as Text" (that entry shows on Studio tabs only). F6: the pending line is taken whenever it is delivered, by `resolve` or to a live session, with that case in the 7.2 unit tests | 5.2, 5.3, 7.2 |

Carried from CR-477 (still binding, `02-answers.md` of CR-477): raw-text-Q3 (an explicit request
for the raw text is never replaced by Studio, even with a line) and raw-text-Q7 (no watcher, no
`open.*` setting comes back).

## 3. Facts found in the code (the Driver starts from these)

- The custom editor is registered in `src/host-vscode/activation.ts`
  (`registerCustomEditorProvider(EDITOR_VIEW_TYPE, { resolveCustomTextEditor })`, `EDITOR_VIEW_TYPE
  = "markdown-okf-schema-studio.editor"`). `resolvePreviewEditor(textDocument, webviewPanel)`
  creates a fixed session (`manager.createSession(..., false)`) and starts its render. VS Code's
  `resolveCustomTextEditor` receives a document, a panel and a token: no selection, no options.
- The page already knows how to reveal and mark a line: `ScrollSyncController.requestRevealLine`
  (`src/session/features/scrollSync.ts`, `pendingRevealLine`, `postPendingRevealLine`, the
  `previewRevealLine` message, `PENDING_LINE_WINDOW_MS = 5000` in
  `src/core/navigation/pendingLine.ts`), SwRS LIFE-181 (today written for the side preview only),
  and the page marker (`src/page/features/lineMarker.ts`, SwRS LIFE-178..180, 192..194).
- Jumps of a text editor: `src/host-vscode/editorJumps.ts` (`startEditorJumps`, `onJump`, SwRS
  LIFE-186) feeds `HostEvents.onEditorJumped` (`src/session/hostEvents.ts`, LIFE-187/188), which
  marks the side preview only.
- Studio's own selections: `src/host-vscode/studioSelections.ts` (`StudioSelections.expect/take`,
  purposes `"no-mark"`, `"marked-by-session"`).
- Links followed in a page: `src/session/features/links.ts` computes the target's `selection` (a
  `markerLine`, or `markdownFragmentRange` for `#anchor`) and calls
  `host.navigation.showDocument(targetId, selection)`; only the side preview
  (`followsActiveEditor`) records a link to another file in the history (comment at
  `links.ts:291`: "A locked preview does not follow the opened file, so only anchor jumps are
  recorded.") and asks `requestJumpMarker`. SwRS TOOLBAR-059 states this rule (refusal row "A link
  to second.md followed in a locked preview ... the history is unchanged"), tested by "a locked
  preview records anchor jumps only" (`test/session/toolbarReq.requirements.test.ts:305-320`).
- A session does not know today whether it is a Studio tab: `followsActiveEditor === false` holds
  both for a Studio tab (`resolvePreviewEditor`, `createSession(..., false)`) and for an older side
  preview restored with the window (`deserializePreviewPanel`, LIFE-038, sets
  `earlier.followsActiveEditor = false`). The rule of Q10 needs that distinction: the Driver adds
  it (for example a read-only `inStudioTab` flag on `PreviewSession`, set only by
  `resolvePreviewEditor`, kept by `previewManager.ts` when it recreates a session).
- Back and Next: `src/session/features/history.ts`, one `NavigationHistory`
  (`src/core/state/navigationHistory.ts`) per panel in a `WeakMap<PreviewPanel, ...>`; a target in
  another file goes through `host.navigation.showDocument(target.uri, lineSelection(...))`.
- `createVscodeNavigation.showDocument` (`src/host-vscode/vscodeHost.ts`) runs `vscode.open` with
  the selection in the group that already shows a text tab of the file, else column One. The port
  is `showDocument(documentId, selection?): PromiseLike<void>` (`src/host-api/navigation.ts`): it
  reports nothing about what opened.
- "Open as Text": `StudioActivation.openAsText()` in `activation.ts` (SwRS LIFE-177).
- The code CR-477 removed (commit `1ced0ced`) held a line hand-off to a Studio tab
  (`StudioLineRequests` in the old `src/host-vscode/openInStudio.ts`: `recordPending`,
  `takePending`, `deliver`, `bindLiveSessions`) and Studio-tab placement
  (`studioPlacement.ts`). They may serve as a reference (`git show 1ced0ced^:<path>`); the opening
  watcher, `openingPolicy.ts` and the `open.*` settings do not come back.
- The real-window opening test is `test/integration/openAtLine.test.ts`, a step `open-at-line` of
  `test/integration/trusted-suite.ts`, with `withAssociation(associated, body)` that sets and
  restores the user `workbench.editorAssociations`. It records today's two rows: a jump under the
  association opens Studio at the top with no marker; a jump to a file already open as text keeps
  that text tab and opens a Studio tab beside it.
- `activation.ts` is 507 lines (limit 800, constitution section 2): new host code goes in its own
  module under `src/host-vscode/`, not in `activation.ts`.

## 4. Step 0: the probe (the Driver's first step, before any product code)

Prove, in a real VS Code window, what reaches the extension when VS Code opens a Markdown file at a
line in the Studio custom editor because of the `*.md` association. The rest of the change depends
on the result.

### 4.1 Entries probed

Each entry targets line 42 of a fixture `target.md` (at least 80 lines), with the association set:

| Entry | How the probe drives it |
| --- | --- |
| Search result | the Search view with a query that matches line 42 only, then the command that opens the result (`search.action.focusNextSearchResult`, "Go to Next Search Result") |
| Quick Open `file.md:42` | `workbench.action.quickOpen` with the text `target.md:42`, then accept the item |
| Link from another file | in a text editor of `source.md`, a link `target.md#L42` opened with `editor.action.openLink`; and a link `target.md#heading` |
| Problems panel | a diagnostic at line 42 of `target.md` (a MyST diagnostic the extension already reports, or a test diagnostic collection), opened from the Problems panel (`editor.action.marker.nextInFiles` or the panel's open action) |
| Go to Symbol | `workbench.action.showAllSymbols` with the name of a heading at line 42, then accept |
| Plain jump (the reference CR-477 measured) | `vscode.open` with `{ selection }` on line 42 |

Each entry is probed twice: `target.md` not open anywhere, and `target.md` already open in a
Studio tab of another group.

### 4.2 Candidate signals recorded for each entry

1. The URI the custom editor receives (`textDocument.uri` in `resolveCustomTextEditor`, and
   `TabInputCustom.uri` of the new tab): a fragment such as `L42` or a query.
2. Any `onDidChangeTextEditorSelection` event for `target.md` around the opening (a text editor
   created and dropped by VS Code), with its kind and line.
3. `vscode.window.activeTextEditor` and `visibleTextEditors` at the moment of `resolve`: a text
   editor of `target.md` with a selection on line 42.
4. The search state: any public command or API of the pinned VS Code version that names the match
   last opened from the Search view.
5. Quick Open's line: any public command or API that names the line typed after `:`.

Only public, stable API counts (no proposed API, no command whose name starts with `_`).

### 4.3 What counts as a reliable signal

A signal is reliable for an entry when it is present in every run of that entry, carries the exact
line (42, never a neighbour), cannot be produced by an opening without a line (a plain Explorer
click gives no signal), and was observed both in the Linux `integration` job and in a local Windows
window.

### 4.4 Output of the probe

- A table, entry by entry and case by case (4.1), of what each candidate signal (4.2) showed,
  committed as the header comment of the real-window test (as `openAtLine.test.ts` does today) and
  copied in the PR body, with the VS Code version.
- Per entry, the verdict: **signal** (5.1 applies to that entry) or **no signal** (the entry is
  covered by 5.2 only).
- The probe code itself is a throwaway or the first version of the real-window test of 7.3; it is
  not product code.

If no entry has a reliable signal, 5.1 is not built, and the change is 5.2, 5.3, 5.4 to 5.6 only.
If at least one entry has no reliable signal, 5.2 is built (it is built in every case where 5.1
does not cover all the entries of 4.1).

## 5. What changes, area by area

### 5.1 With a signal: a jump under the association opens Studio at the line (Q1, Q3)

Only for the entries the probe marked **signal**.

- A new host module (for example `src/host-vscode/studioLineSignal.ts`) reads the signal found by
  the probe and turns it into a 1-based line for the Studio tab of that file. The pure part
  (reading a fragment, choosing the line, the age window) lives in `src/core/navigation/` with
  unit tests; only the module under `src/host-vscode/` touches `vscode`.
- A new Studio tab: `resolvePreviewEditor` asks the module for the file's line and, when there is
  one, calls `manager.scroll.requestRevealLine(preview, line, { documentId })` on the new session
  (scroll `"reading-line"`): the page reveals the line and draws the marker once ready, through
  LIFE-181.
- A Studio tab already open that the jump reveals (no `resolve`): the line goes to that live
  session the same way.
- The side preview (Q3): when it is open and follows the editor, it marks the same line as for a
  text editor jump (`HostEvents.onEditorJumped`, LIFE-187/188, switching to the file first when it
  shows another one).
- What the signal never does: close, replace or reopen any tab; act when the tab that opened is a
  text editor; act on an opening without a line.

### 5.2 Without a signal: the command "Open in Studio at This Line" (Q1, Q6, Q7, Q8)

- Command `markdown-okf-schema-studio.openInStudioAtLine`, title **Open in Studio at This Line**,
  category "Markdown OKF-Schema Studio". Registered in `StudioActivation.start()` (one line there;
  the body in its own host module).
- It runs on the active text editor of an eligible Markdown file (`isDocumentEligible`). It opens
  the file in a Studio tab with `vscode.openWith(uri, EDITOR_VIEW_TYPE, { viewColumn: <the text
  editor's group>, preview: false })` and hands the Studio tab the 1-based line of the editor's
  active selection: `requestRevealLine` on the session `resolvePreviewEditor` creates, or on the
  live session when a Studio tab of the file is revealed. The hand-off is a pending line by URI
  with an age (`PENDING_LINE_WINDOW_MS`), as the old `StudioLineRequests` did. The pending line is
  taken (removed) whenever it is delivered: by `resolvePreviewEditor` for a new tab, or to the live
  session of a Studio tab the open revealed (routine 14, F6); it never stays pending after a
  delivery, so a later unrelated opening of the file cannot pick it up.
- The text tab stays open (Q6): the Studio tab opens in the same group as the text editor, and the
  command closes no tab.
- Without an eligible Markdown text editor, it opens nothing and shows the information message
  "Open a Markdown file as text to open it in Studio at a line." (same pattern as "Open as Text").
- `package.json` (hand-edited contributions; settings are not touched):
  - `commands`: the new command;
  - `menus.commandPalette`: `when` `resourceExtname == .md && !activeCustomEditorId` (routine 14,
    F5; the Driver checks it in the real window: shown on a Markdown text editor, hidden on a
    Studio tab and on other files);
  - `menus.editor/title`: on a Markdown text editor (`resourceExtname == .md && activeEditor ==
    workbench.editors.files.textFileEditor`), group `1_markdown`. It is not placed "next to Open as
    Text": that entry shows on Studio tabs only (`activeCustomEditorId ==
    'markdown-okf-schema-studio.editor'`), so the two never show together (routine 14, F5);
  - no default keybinding (Q7); the reader can bind one.
- With default settings this is the whole path from a search to Studio at the line: the jump opens
  the text at the line (unchanged), the reader runs the command. Under the association, an entry
  the probe marked **no signal** opens Studio at the top; that is accepted and documented, and the
  command is the fallback from a text editor (Q8).

### 5.3 Links, Back and Next inside a Studio tab (Q2, Q9 to Q13)

A Studio tab is a session opened by the custom editor (`resolvePreviewEditor`), marked as such
(section 3, the `inStudioTab` flag or equivalent). Today a link or a history move from it calls
`showDocument`, and under the association VS Code opens the target's Studio tab at the top.

**What opened.** The Port change (`src/host-api/navigation.ts`, implemented in `host-vscode`,
`host-memory` and the test fakes; never a `vscode` import outside `src/host-vscode/`) lets a
session hand a line with the open and learn what opened: for example an optional `line` given to
`showDocument` and a result naming the outcome, `"studio-created"` (a new Studio tab of the target,
whose `resolvePreviewEditor` took the pending line), `"studio-existing"` (a Studio tab of the
target already open, revealed, the line delivered to its live session) or `"other"` (a text editor
or anything else; the pending line is dropped). The extension does not read
`workbench.editorAssociations` to decide: VS Code opens what it opens, and the line and the history
follow the outcome.

- **Link to another Markdown file** with a line (`markerLine`), an anchor (`#heading`, resolved by
  `markdownFragmentRange`) or neither (line 1):
  - the target opens at that line. When a Studio tab of the target is already open in any group,
    that tab is revealed in its own group and receives the line, by the same host path as Back and
    Next below (Q15, the rule of Q11): no second Studio tab of the target opens, and the outcome is
    `"studio-existing"`. Otherwise, in a new Studio tab (the association) the tab reveals and marks
    the line through the pending-line hand-off of 5.2, taken whenever delivered (routine 14, F6).
    As a text editor (no association, no Studio tab of the target open), unchanged: the text editor
    at the line;
  - history (Q10, Q12, Q13): a Studio tab records the link only when the target opens in a Studio
    tab:
    - `"studio-created"`: the source tab records the place left and the target
      (`recordNavigation`), and the new tab's panel shares the source tab's `NavigationHistory`
      (the `WeakMap` of `HistoryController` maps the new panel to the same object; for example a
      `shareHistory(source, created)` method of `HistoryController`, called when the hand-off that
      created the tab came from a link);
    - `"studio-existing"`: the existing tab keeps its own history (Q12). The source tab records the
      move in its own history, and the move is appended to the existing tab's history: it departs
      from its current place, then the place left in the source and the target place are pushed,
      so Back in that tab returns to the place left in the source and further Back walks its own
      older places;
    - `"other"` (default settings, the target opened as text): nothing is recorded (Q13); the
      history is unchanged, as today.
  - A fixed preview that is not a Studio tab (an older side preview restored by VS Code, LIFE-038)
    keeps today's rule: a link to another file opens it and the history is unchanged (Q10).
- **Anchor in the same document**: unchanged (`navigateAnchor`, recorded as today).
- **Back and Next** from a Studio tab, to a place in another file:
  - when a Studio tab of the target file is open in any group, that tab is revealed in its own
    group (not a new tab in column One) and receives the stored line (Q11; links use the same path,
    Q15): for example the host
    finds the `TabInputCustom` with `viewType` `EDITOR_VIEW_TYPE` and the target URI in
    `vscode.window.tabGroups.all` and runs `vscode.openWith(uri, EDITOR_VIEW_TYPE, { viewColumn:
    <its group> })`, then delivers the line to its live session;
  - otherwise `showDocument` with the stored line, as for a link: under the association a new
    Studio tab at that line, else the text editor at the line (as today).
  - With a shared history: **Back** in the target tab returns to the source Studio tab at the place
    left (revealed in its group when still open, else opened); **Next** in the source tab then
    returns to the target tab at its line.
- **VS Code's Go Back / Go Forward** (`workbench.action.navigateBack` / `navigateForward`), after a
  link followed from a Studio tab to another Studio tab: Go Back makes the Studio tab left active
  again, at the position it had; Go Forward redoes the jump, the target Studio tab active at its
  line (Q9). The Driver proves it in the real window (7.3). If VS Code's editor history already
  does it, no product code is added for it; if it does not and only proposed or internal API could
  make it hold, the Driver stops and reports the measurement.
- A Studio tab opened any other way (Explorer, Open With, a jump, the command of 5.2) starts with
  its own empty history, as today.
- The side preview (`followsActiveEditor`): unchanged (LIFE-191, TOOLBAR-059 as today).
- The `links.ts:291` comment is rewritten to the new rule (a Studio tab records a link to another
  file when the target opens in a Studio tab; any other fixed preview records anchor jumps only).

### 5.4 The hard constraint, in code

- No new listener closes a tab, and no code path of this change calls `tabGroups.close`: the
  command of 5.2 leaves the text tab open (Q6).
- "Open as Text", "Open With... > Text Editor" and "Reopen Editor With... > Text Editor" are not
  touched; a pending line never applies to a text editor; a line signal (5.1) never acts when the
  tab that opened is a text editor.

### 5.5 Requirements (okfreq)

Rules: `requirements/guidelines/requirements.guidelines.md`, the baseline it links to,
`requirements/guidelines/project.guidelines.md` ("During a change"), skill `.agents/skills/okfreq`.
Run okfreq as `uv run --no-sync --group requirements okfreq`. New IDs come from `okfreq new` (never
reused: LIFE-182 and LIFE-183 are deprecated and stay so). All in `lifecycle-sync`.

| Requirement | Action |
| --- | --- |
| SwRS LIFE-181 (a requested line reaches the page) | amend: from "the side preview that follows the editor" to every session that holds a requested line (the side preview, a Studio tab given a line by 5.1, 5.2 or 5.3); the 5-second window, "only once", "only to a visible page that shows that document" stay |
| New SwRS: a link, Back or Next from a Studio tab opens the target at its line or anchor | `okfreq new ... --lifecycle proposed`, derives from StRS LIFE-023; markers on `links.ts`, `history.ts` and the host hand-off; scenarios: a pending line taken once whenever delivered (by `resolve` or to a live session), a link, Back or Next to a file whose Studio tab is open in another group reveals that tab in its group, no second Studio tab (Q11, Q15) |
| New SwRS: the history of a link from a Studio tab | new, as above: recorded only when the target opens in a Studio tab (Q13); a created tab shares the source's history, an existing tab keeps its own and the move is appended to it (Q12); Back returns to the place left, Next goes forward again; VS Code's Go Back / Go Forward between the two Studio tabs (Q9) |
| SwRS TOOLBAR-059 (scope `toolbar-navigation`) | amend (it is `proposed`, Q10): the statement says a link to another Markdown document is recorded in a preview that follows the active editor, or in a Studio tab when the target opens in a Studio tab (cite the new SwRS for the details); the refusal row "A link to second.md followed in a locked preview" becomes "followed in a fixed preview restored by VS Code (not a Studio tab)", and a row is added "followed in a Studio tab and opened as text: the history is unchanged"; verification notes updated. StRS TOOLBAR-009 lines 82-88 checked and reworded only where false |
| New SwRS: Open in Studio at This Line | new, only when 5.2 is built: the command, its palette and title-menu entries, no default keybinding, the text tab stays and the Studio tab opens in its group, the refusal message |
| New SwRS: a jump under the association opens Studio at the line, per entry found | new, only when 5.1 is built; it names the entries covered and states that the side preview marks the line (Q3) |
| SwRS LIFE-177 (Open as Text) | check: it still holds; add nothing unless a scenario changes |
| SwRS LIFE-186..191 | check; reword only a sentence this change makes false |
| StRS LIFE-023 | amend (it is `proposed`): the title, statement, user need and Mermaid diagram take back "a reader opens Studio at a searched line" (by the signal or by the command, as built) and "navigation inside Studio keeps the line and the history"; new main paths cite only in-force SwRS; the rationale line "With the `*.md` association set, a jump opens a Studio tab at the top of the file, and the side preview marks nothing then" is rewritten to what remains true after the probe |

No requirement of `lifecycle-sync` is `approved`; no owner re-approval is required by the okfreq
rule. If the Driver finds a requirement with `req_lifecycle: approved` that must change, they stop
and report it. After the edits: markers follow the code (at most three IDs per block),
`just requirements-lint`, `just requirements-update`, a dated entry in `requirements/tiers/log.md`.

### 5.6 Documentation

- `docs/user/open-studio.md`, "Open at a line": say how to open Studio at a searched line (the
  entries 5.1 covers, if any; the command of 5.2 with its editor title entry and palette entry, no
  default keybinding, the text tab staying beside the new Studio tab); that a link, Back or Next
  inside a Studio tab keeps the line, that Studio's Back returns to the place left and VS Code's Go
  Back returns to the Studio tab left; that with default settings a link from a Studio tab opens the
  text and is not added to Studio's history; that "Open as Text", "Open With... > Text Editor" and
  "Reopen Editor With... > Text Editor" always give the text.
  Keep "With the side preview open" and its table; update its sentence on the association to what
  the probe proved (Q3).
- `docs/known-limitations.md`, "Opening Files": keep, for each entry the probe marked **no signal**,
  that a jump under the association opens Studio at the top and the side preview marks nothing
  (Q3, Q8: the limitation stays documented), now with the command of 5.2 as the way to Studio at
  the line; remove it for the entries 5.1 covers. Re-measure "A jump to a file that is already open as
  text keeps that text tab and opens a Studio tab beside it" and keep only what the real window
  shows. Give the VS Code version measured.
- `.agents/glossary/common.md`: add a term for the line handed to a Studio tab (for example
  "Line hand-off") if the code names one; keep "Jump".
- `CHANGELOG.md`, `## Unreleased`: one user-facing line in the format of "CHANGELOG line" of
  `.agents/guidelines/pull-request.guidelines.md`, ending with `(CR-<number> searched-line, PR
  #<number>)`: Studio opens at the line of a link, Back or Next inside Studio; the new command; the
  entries opened at the line under the association, if any.
- The writing skill `skills/writing-for-markdown-okf-schema-studio/`: no rendered syntax changes,
  no update.
- Commit type `feat`, scope `vscode` (`.agents/guidelines/git-commit-allowed-scopes.md`).

## 6. Resulting behaviour, in the user's terms

| Gesture | `*.md` → Studio associated | Shipped default (no association) |
| --- | --- | --- |
| A jump from an entry the probe marked **signal** | Studio tab at the line, line marked; side preview, if open, marks it | text editor at the line; side preview marks it (unchanged) |
| A jump from an entry marked **no signal** | Studio tab at the top, nothing marked (accepted, documented limitation, Q8) | text editor at the line; side preview marks it (unchanged) |
| Open in Studio at This Line, from a Markdown text editor (5.2) | Studio tab in the same group at the caret's line, line marked; the text tab stays | same |
| Link with a line or anchor, inside a Studio tab | target's Studio tab at that line, marked; recorded in Studio's history | text editor at the line; not recorded (unchanged) |
| Back in the target Studio tab | source Studio tab at the place left (revealed in its own group when open) | as today |
| Next in the source Studio tab after Back | target Studio tab at its line | as today |
| VS Code Go Back after that link, then Go Forward | the Studio tab left, at its position; then the target Studio tab at its line | as today |
| Link, Back or Next inside a Studio tab to a file whose Studio tab is already open in another group | that tab revealed in its own group at the line, no second Studio tab (Q11, Q15); for a link, its own history kept, the move appended to it (Q12) | same: the rule does not depend on the association |
| Open as Text, Open With > Text Editor, Reopen Editor With > Text Editor | text editor, stays | text editor, stays |
| Explorer click (no line) | Studio tab at the top, no marker | text editor |

## 7. Evidence

The gate is `just preflight` (on Windows: the static stage; CI runs the others). The real-window
tests run in the existing `integration` job (Linux), which a pull request does not run: dispatch it
with `gh workflow run ci.yml --ref <branch> -f heavy=true` and give the run's link in the PR. No CI
job is added or changed.

### 7.1 The probe (section 4)

Its table and verdicts are in the PR body and the test's header comment, with the VS Code version,
from one `integration` run on Linux and one local Windows window.

### 7.2 Static, unit and host tests (each fails on `main` at `80d482fd`)

- `just check` green (TypeScript, import boundaries, file size, unused exports, settings schema).
- The manifest test (`test/security/package-contract.test.ts`) reads the shipped `package.json` of
  the branch, not a fixture: the command `openInStudioAtLine` is declared with its palette and
  `editor/title` `when` clauses (when 5.2 is built); `openAsText` unchanged; no
  `markdownOkfSchemaStudio.open.*` property.
- Pure core (`src/core/navigation/`): the pending-line hand-off (taken once, by URI, dropped past
  the window, a second request replaces the first) and, when 5.1 is built, the signal reader (one
  test per signal shape the probe found, and one per shape that must give no line).
- Host hand-off, delivery (routine 14, F6): a pending line delivered by `resolvePreviewEditor` is
  gone afterwards; a pending line delivered to the live session of a revealed Studio tab is gone
  afterwards too, so a `resolvePreviewEditor` of the same URI right after asks the page to reveal
  nothing; a text editor opening drops it.
- Session, memory ports: a link with a `markerLine` and with `#heading` from a Studio tab hands the
  target's line with the open; with the outcome `"studio-created"` the source records the move and
  the created panel shares the source's `NavigationHistory` (same object); with
  `"studio-existing"` the existing panel keeps its own history object and gains the place left and
  the target, the source records the move in its own (Q12); with `"other"` nothing is recorded in
  either (Q13); Back from the target panel hands the source line; Next hands the target line again;
  a link, Back or Next to a file whose Studio tab is open in another group asks the host to reveal
  that tab (Q11, Q15; the memory host records the request); the side preview's behaviour is unchanged (existing
  LIFE-191 tests green, assertions untouched).
- TOOLBAR-059 (Q10): "a locked preview records anchor jumps only"
  (`test/session/toolbarReq.requirements.test.ts:306`) is amended to the new rule: a fixed preview
  that is not a Studio tab records anchor jumps only (its assertions kept); a Studio tab whose link
  opens as text keeps its history unchanged; a Studio tab whose link opens in a Studio tab records
  it.
- Host (`test/host/fakeVscode.ts`): `resolvePreviewEditor` with a pending line asks the page to
  reveal it; without one asks nothing; the command of 5.2 runs `vscode.openWith` with the Studio
  view type in the text editor's group and the caret's line, refuses on a non-Markdown editor and
  on a Studio tab with the message, and closes no tab (Q6); Back or Next to a file whose Studio tab
  is in another group runs `openWith` with that group's column (Q11); a link to such a file does
  the same, opens no new tab and reports `"studio-existing"` (Q15).
- The manifest test also asserts: no `keybindings` entry for `openInStudioAtLine` (Q7); the palette
  `when` is exactly `resourceExtname == .md && !activeCustomEditorId` (routine 14, F5).
- `just requirements-lint` green, `just requirements-update` leaves no diff, the log entry is there.

### 7.3 Real VS Code window (Q4)

Host and default matrix: one host (VS Code desktop); the behaviour depends on a configured value
(the `*.md` association) against the shipped default, so each row runs in both columns. The rows
extend the step `open-at-line` of `test/integration/trusted-suite.ts`
(`test/integration/openAtLine.test.ts`, split into a second file if it passes the 1 500-line test
limit), with `withAssociation` restoring the user value in a `finally`. "Stays" means: still the
active tab, of the same kind, after 2 s. "Marked" means the page's line marker is on line 42 (read
from the page, as `sidePreviewJump.test.ts` does).

Cells, one line each:

- Search result, associated: Studio tab, marked at 42 if **signal**, else at the top and not marked.
- Search result, default: text editor at 42, stays.
- Quick Open `target.md:42`, associated: as the search result row, by its own verdict.
- Quick Open `target.md:42`, default: text editor at 42, stays.
- Link `target.md#L42` and `target.md#heading` from a text editor of `source.md`, associated: by its
  verdict.
- Same links, default: text editor at the line, stays.
- Problems panel at line 42, associated: by its verdict.
- Problems panel, default: text editor at 42, stays.
- Go to Symbol to the heading at 42, associated: by its verdict.
- Go to Symbol, default: text editor at the heading's line, stays.
- Every associated row above with the side preview open on `target.md`: the side preview marks 42 if
  **signal**, else marks nothing (Q3).
- Link with `#heading` from a Studio tab of `source.md`, associated: target Studio tab marked at the
  heading's line.
- Same link, default: text editor at the heading's line.
- Studio Back in that target tab (driven by the page's `previewHistoryGo` message), associated: the
  source Studio tab is active and marked at the place left.
- Studio Next in the source tab, associated: the target Studio tab is active and marked at its line.
- Studio Back and Next, default: as today (the existing `previewHistory.test.ts` stays green).
- Back in the target tab while the source Studio tab is open in another group (moved there by the
  test), associated: that existing source tab, in its own group, is active and marked at the place
  left; no second Studio tab of the source opens (Q11).
- Link from a Studio tab of `source.md` to `target.md` whose Studio tab is already open in another
  group with its own history (a previous in-page anchor jump), associated: that existing tab, in
  its own group, is active and marked at the line; no second Studio tab of `target.md` opens in any
  group (Q15); its Back returns first to the place left in `source.md`, then to its own earlier
  place (Q12).
- Link from a Studio tab, default (opens as text): Studio's Back and Next of the source tab stay
  as they were (Q13).
- VS Code Go Back (`workbench.action.navigateBack`) after a link from a Studio tab of `source.md` to
  the Studio tab of `target.md`, associated: the source Studio tab is active, at the position it had
  (its page's reading line unchanged); Go Forward (`workbench.action.navigateForward`): the target
  Studio tab is active at its line (Q9).
- Open in Studio at This Line on a text editor at line 42 (when 5.2 is built), associated and
  default: a Studio tab in the text editor's group, marked at 42; the text tab still open in that
  group (Q6).
- "Reopen Editor With... > Text Editor" (`workbench.action.reopenTextEditor`) right after each
  associated row that ended in a Studio tab: text editor, stays.
- `vscode.openWith(target, "default")` after each associated row: text editor, stays.
- A jump from every entry while `target.md` is already open in a text editor, associated: that text
  tab is not closed and not replaced; what else opens is recorded, and the documents (5.6) say it.
- An Explorer-style opening without a line (`vscode.open` without selection), associated: Studio tab
  at the top, no marker (a signal never fires without a line).

The rows are registered in `test/shared/e2eGroups.ts` (group `lifecycle-sync`, the "locks" text of
the `open-at-line` row updated) and the counts in `test/site/e2eGroups.test.ts`.

### 7.4 Manual scenario for the owner (five minutes, on the VSIX built from the branch)

1. Default settings. Search a word of a long Markdown file, click the result: the text at the line.
   Run **Open in Studio at This Line** from the editor title menu: Studio at that line in the same
   group, an arrow on it; the text tab is still there.
2. In that Studio tab, click a link to a heading of another Markdown file: with default settings
   the text at the heading. Set the `*.md` association, click it again: a Studio tab at the
   heading, marked. Click **Back**: the first Studio tab at the place you left. Click **Next**: the
   second one again, at the heading. Run VS Code's **Go Back** (Alt+Left on Windows): the first
   Studio tab at its position; **Go Forward**: the second again.
3. With the association, click a search result, then Quick Open `file.md:42`: Studio at the line
   for each entry the PR body lists as **signal**; at the top for the others, as the known
   limitations say.
4. Right-click the Studio tab > **Reopen Editor With... > Text Editor**: the text, and it stays.
   **Open With... > Text Editor** from the Explorer: the text, and it stays.

## 8. Out of scope

- Any automatic replacement of a text tab by Studio, any opening watcher, any `open.*` setting
  (CR-477 raw-text-Q7; Q1 "no automatic replacement").
- Proposed or internal VS Code API to get the selection.
- Diff editors, Source Control, the merge editor, VS Code's built-in Markdown preview.
- Changing what "Open as Text" does, the side preview's behaviour without the association, or the
  page's line marker drawing.
- The release itself (version, notes, tag): a release CR.

## 9. Open questions

None: answers Q1 to Q15 and routine line 14 settle every point.
