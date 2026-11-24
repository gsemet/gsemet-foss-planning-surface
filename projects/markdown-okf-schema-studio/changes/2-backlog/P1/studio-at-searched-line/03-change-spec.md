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
  (`followsActiveEditor`) records history and asks `requestJumpMarker`.
- Back and Next: `src/session/features/history.ts`, one `NavigationHistory`
  (`src/core/state/navigationHistory.ts`) per panel in a `WeakMap<PreviewPanel, ...>`; a target in
  another file goes through `host.navigation.showDocument(target.uri, lineSelection(...))`.
- `createVscodeNavigation.showDocument` (`src/host-vscode/vscodeHost.ts`) runs `vscode.open` with
  the selection in the group that already shows a text tab of the file, else column One.
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

### 5.2 Without a signal: the command "Open in Studio at This Line" (Q1)

- Command `markdown-okf-schema-studio.openInStudioAtLine`, title **Open in Studio at This Line**,
  category "Markdown OKF-Schema Studio". Registered in `StudioActivation.start()` (one line there;
  the body in its own host module).
- It runs on the active text editor of an eligible Markdown file (`isDocumentEligible`). It opens
  the file in a Studio tab with `vscode.openWith(uri, EDITOR_VIEW_TYPE, { viewColumn: <the text
  editor's group>, preview: false })` and hands the Studio tab the 1-based line of the editor's
  active selection: `requestRevealLine` on the session `resolvePreviewEditor` creates, or on the
  live session when a Studio tab of the file is revealed. The hand-off is a pending line by URI
  with an age (`PENDING_LINE_WINDOW_MS`), taken once, as the old `StudioLineRequests` did.
- Whether the text tab closes is open question 1 (section 9); until answered, the specification's
  proposal is: the text tab stays, the Studio tab opens in the same group.
- Without an eligible Markdown text editor, it opens nothing and shows the information message
  "Open a Markdown file as text to open it in Studio at a line." (same pattern as "Open as Text").
- `package.json` (hand-edited contributions; settings are not touched):
  - `commands`: the new command;
  - `menus.commandPalette`: `when` `editorLangId == markdown && !activeCustomEditorId`
    (the Driver checks the clause in the real window: shown on a Markdown text editor, hidden on a
    Studio tab and on other files);
  - `menus.editor/title`: on a Markdown text editor (`resourceExtname == .md && activeEditor ==
    workbench.editors.files.textFileEditor`), group `1_markdown@2`, next to "Open as Text";
  - a default keybinding only if open question 2 says so.
- With default settings this is the whole path from a search to Studio at the line: the jump opens
  the text at the line (unchanged), the reader runs the command.

### 5.3 Links, Back and Next inside a Studio tab (Q2)

A Studio tab is a session with `followsActiveEditor === false` opened by the custom editor. Today a
link or a history move from it calls `showDocument`, and under the association VS Code opens the
target's Studio tab at the top.

- Link to another Markdown file with a line (`markerLine`) or an anchor (`#heading`, resolved by
  `markdownFragmentRange`): the target opens **at that line**:
  - when VS Code opens the target in a Studio tab (the association), the Studio tab reveals and
    marks the line: before `showDocument`, the session records the target's line as a pending
    line for that URI (the same hand-off as 5.2); `resolvePreviewEditor` takes it for a new tab;
    after the open, if the active tab is a live Studio tab of the target, the line goes to that
    session. When a text editor opened instead, the pending line is dropped;
  - when VS Code opens a text editor (no association), unchanged: the text editor at the line.
  The extension does not read `workbench.editorAssociations` to decide: VS Code opens what it opens,
  and the line follows. The Port change (a pending-line hand-off reachable from `src/session`)
  goes through `src/host-api/navigation.ts` (for example an optional `line` handed to
  `showDocument`, or a separate port method), implemented in `host-vscode`, `host-memory` and the
  test fakes; never a `vscode` import outside `src/host-vscode/`.
- Anchor in the same document: unchanged (`navigateAnchor`).
- History: a link followed from a Studio tab records the place left and the target, as the side
  preview does (`recordNavigation`); today only the side preview records a link to another file.
  When the target opens in a Studio tab, that tab's panel shares the source tab's
  `NavigationHistory` (the `WeakMap` maps the new panel to the same object), so:
  - **Back** in the target tab returns to the source file at the line it left: the Studio tab of the
    source is revealed when still open, else opened, and it reveals that line (same hand-off);
  - **Next** in the source tab then returns to the target at its line.
  A Studio tab opened any other way (Explorer, Open With, a jump) starts with its own empty history,
  as today.
- When the target opens as a text editor (no association), the Studio tab's history still records
  the move; Back in that Studio tab then has nothing in another tab to return to and behaves as
  today for a target in another file (`showDocument` at the stored line).
- The side preview (`followsActiveEditor`): unchanged (LIFE-191).

### 5.4 The hard constraint, in code

- No new listener closes a tab, and no code path calls `tabGroups.close` on a text tab except where
  the reader's own command asks for Studio (5.2, only if open question 1 says the text tab closes).
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
| New SwRS: a link, Back or Next from a Studio tab opens the target at its line or anchor | `okfreq new ... --lifecycle proposed`, derives from StRS LIFE-023; markers on `links.ts`, `history.ts` and the host hand-off |
| New SwRS: a link from a Studio tab that opens a Studio tab shares the history, so Back returns to the place left and Next goes forward again | new, as above |
| New SwRS: Open in Studio at This Line | new, only when 5.2 is built: the command, its menus, its refusal message |
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
  entries 5.1 covers, if any; the command of 5.2 with its button and palette entry); that a link,
  Back or Next inside a Studio tab keeps the line and Back returns to the place left; that "Open as
  Text", "Open With... > Text Editor" and "Reopen Editor With... > Text Editor" always give the text.
  Keep "With the side preview open" and its table; update its sentence on the association to what
  the probe proved (Q3).
- `docs/known-limitations.md`, "Opening Files": keep, for each entry the probe marked **no signal**,
  that a jump under the association opens Studio at the top and the side preview marks nothing
  (Q3: the limitation stays documented), now with the command of 5.2 as the way to Studio at the
  line; remove it for the entries 5.1 covers. Re-measure "A jump to a file that is already open as
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
| A jump from an entry marked **no signal** | Studio tab at the top, nothing marked (documented limitation) | text editor at the line; side preview marks it (unchanged) |
| Open in Studio at This Line, from a Markdown text editor (5.2) | Studio tab at the caret's line, line marked | same |
| Link with a line or anchor, inside a Studio tab | target's Studio tab at that line, marked | text editor at the line (unchanged) |
| Back in the target Studio tab | source Studio tab at the place left | as today |
| Next in the source Studio tab after Back | target Studio tab at its line | as today |
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
- Session, memory ports: a link with a `markerLine` and with `#heading` from a Studio tab hands the
  target's line before `showDocument`; the history of a Studio tab records the move; Back from the
  target panel hands the source line; Next hands the target line again; the side preview's
  behaviour is unchanged (existing LIFE-191 tests green, assertions untouched).
- Host (`test/host/fakeVscode.ts`): `resolvePreviewEditor` with a pending line asks the page to
  reveal it; without one asks nothing; the command of 5.2 runs `vscode.openWith` with the Studio
  view type in the text editor's group and the caret's line, refuses on a non-Markdown editor and
  on a Studio tab with the message, and closes no tab (unless open question 1 decides otherwise).
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
- Open in Studio at This Line on a text editor at line 42 (when 5.2 is built), associated and
  default: a Studio tab marked at 42; no text tab closed (or closed, per open question 1).
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
   Run **Open in Studio at This Line** from the editor title menu: Studio at that line, an arrow on
   it.
2. In that Studio tab, click a link to a heading of another Markdown file: with default settings
   the text at the heading. Set the `*.md` association, click it again: a Studio tab at the
   heading, marked. Click **Back**: the first Studio tab at the place you left. Click **Next**: the
   second one again, at the heading.
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

1. **Open in Studio at This Line and the text tab.** Does the command leave the text tab open and
   add a Studio tab in the same group (the specification's proposal, nothing replaced), or does the
   Studio tab take the text tab's place, as "Open as Text" does the other way round?
2. **Button or keybinding.** Q1 says "a button or keybinding". The specification proposes the
   editor title menu entry and the palette, with no default keybinding (the reader can bind one).
   Should a default keybinding ship too, and which?
3. **Under the association, an entry without a signal.** The specification reads Q1's fallback
   ("the jump opens the text at the line") as the shipped default's behaviour, with the command
   from there, and Q3's "the limitation stays documented" as: under the association such a jump
   still opens Studio at the top. Confirm that nothing else is wanted there (Studio opening the
   text instead would be the extension replacing a Studio tab automatically).
4. **"Back and Next" in Q4.** The specification proves Studio's own Back and Next. Should VS Code's
   **Go Back** / **Go Forward** (`workbench.action.navigateBack` / `navigateForward`) between Studio
   tabs also be proved, and with which expected result?
