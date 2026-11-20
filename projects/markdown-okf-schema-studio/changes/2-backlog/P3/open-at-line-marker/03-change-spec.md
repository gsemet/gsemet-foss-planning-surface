# Open Studio at a searched line and mark it with an arrow

When a VS Code jump (a search result, Quick Open `file.md:42`, a problem, a link) opens a Markdown
file, Studio shows that file at that line, with an arrow in the left margin and a light band on the
line. Studio does it with two settings of its own instead of VS Code's editor association, migrates
the user's `*.md` association, introduces the feature once with a notice, and never pulls a diff
view or a raw text editor asked on purpose into Studio.

Origin: verbal (owner, 2026-11-20). No tracker issue. Code base: `origin/main` at `a18bcac1`
(release 1.10.0 plus the CRLF fix). Every decision below comes from `02-answers.md`; decisions 12
to 18 were **decided by the Griller under the owner's autonomy rule**, not by the owner, and the
owner may change any of them at review.

## 1. Goal, in the user's terms

- I search my workspace, click a result in a `.md` file: Studio opens at that line and an arrow
  shows me where it is. Same for Quick Open `doc.md:42`, a problem, a terminal link, a Ctrl+click.
- I keep making Studio my default Markdown editor, and I now land on the right line too.
- My diffs (Git, Source Control, timeline, Compare with Saved, two-file compare, the search and
  replace preview) stay VS Code's text diffs.
- When I ask for the raw text on purpose, I get the raw text.

## 2. Why the design takes this way (facts at 1.10.0)

- With `workbench.editorAssociations` `"*.md": "markdown-okf-schema-studio.editor"`, VS Code opens
  Studio through `resolveCustomTextEditor(document, webviewPanel, token)`
  (`src/host-vscode/activation.ts`, `StudioActivation.resolvePreviewEditor`). That call carries no
  selection: the requested line is lost before Studio sees it. Only a text editor receives it.
- So Studio lets the text editor open, reads its selection, and puts its own tab in place, at that
  line (decision 1). The VS Code association cannot be kept: Studio's own setting replaces it
  (decisions 1, 12, 13).
- The exploration of the diff views at 1.10.0 (`work/diff-view-findings.md`, scripts
  `experiments/0N-diff-view-*`, screenshots `evidence/diff-view/`, real VS Code 1.147.0) found every
  diff to be VS Code's own text diff, with or without the association. A diff's sides are text
  editors, which is why this CR must exclude them explicitly (decisions 11, 14).

## 3. Decisions carried

| # | Decision (from `02-answers.md`) | Where in this spec |
| --- | --- | --- |
| 1 | Studio decides itself to open `.md` files; the text editor opens for a moment at the line, then Studio takes its place at that line with the marker | 4.1, 4.2 |
| 2 | Every entry point that opens a text editor at a line, no closed list | 4.1 |
| 3 | File already open in Studio: the same Studio tab scrolls, the marker moves, no new tab | 4.2 |
| 4 | A text editor asked for on purpose ("Reopen Editor With > Text Editor", a Studio action) stays | 4.1 (exclusions) |
| 5 | On by default; a feature introduction notice shown for a few seconds, once, never again even in later sessions; a reusable introduction system with a reset | 4.4 |
| 6 | Marker: option A of `prototypes/01-arrow-marker/`: an arrow in the left margin at the exact height of the line plus a light band on that line | 4.5 |
| 7 | The marker stays until a click in the page, an edit starts, or another line is requested; scrolling keeps it | 4.6 |
| 8 | As precise as possible: exact line of a paragraph or code block, the table row, unfold a folded section or admonition; else the top of the block | 4.5 |
| 9 | Set aside in P3 with the drawback that opening the raw text may loop back to Studio | 4.1 (the loop is confined to the opt-in setting), 7 (known limit) |
| 10 | A setting "open searches in Studio", on by default | 4.3 |
| 11 | The diff-view item merged here; diffs tested with this CR, they must not be pulled into Studio | 4.1, 6.3 (trial T7) |
| 12 | Griller (autonomy rule): migrate a `*.md` association to Studio: remove it from its scope, turn on "Open Markdown files in Studio" in the same scope, the notice says so; never touch an entry naming another editor | 4.3 |
| 13 | Griller (autonomy rule): two settings: "Open search results in Studio" (on) for jumps only; "Open Markdown files in Studio" (off, on after migration) for every opening | 4.1, 4.3 |
| 14 | Griller (autonomy rule): never replace a diff (either side, every diff view), a text editor reopened as text on purpose, or a text editor Studio itself opened; each proved in real VS Code before ready | 4.1, 6.3 |
| 15 | Griller (autonomy rule): a palette command "Markdown OKF-Schema Studio: Show Feature Introductions Again" | 4.4 |
| 16 | Griller (autonomy rule): edit mode: same arrow and band, not covering the list item handle or block actions; no block editor opens on its own; a click opens it as usual and removes the marker | 4.6 |
| 17 | Griller (autonomy rule): split off: the marker in the side preview, the side preview's gaps next to a diff. This CR changes nothing in the side preview | 5 |
| 18 | Griller (autonomy rule): grilled enough; the spec goes through the spec critic on Fable (claude-fable-5-2) | process note, nothing to implement |

## 4. What changes

### 4.1 The opening watcher (host, `src/host-vscode/`)

New file `src/host-vscode/openInStudio.ts` (the only place that reads VS Code's tabs for this
feature), created and started by `StudioActivation.start` in `src/host-vscode/activation.ts`.

It listens to `vscode.window.tabGroups.onDidChangeTabs`, `window.onDidChangeVisibleTextEditors`,
`window.onDidChangeActiveTextEditor` and `window.onDidChangeTextEditorSelection`, and once at
activation reads the tabs already open (the activation by `onLanguage:markdown`, 4.7, happens after
the first Markdown text editor opened). For each **newly opened** text editor tab it gathers facts
and asks a pure policy what to do.

The policy is a pure function in a new file `src/core/navigation/openingPolicy.ts` (no host API, so
it is unit-tested on its own):

- Input facts: the tab's kind (`text`, `diff`, `merge`, `custom`, `other`, from `TabInputText`,
  `TabInputTextDiff`, `TabInputTextMerge`, `TabInputCustom`, anything else), the document's scheme
  and extension, whether it is eligible (`isDocumentEligible`, `src/session/sessionDocuments.ts`),
  whether the tab is new in its group, the requested line (or none), the two settings, whether it
  was reopened as text from a Studio tab, whether Studio itself opened it.
- Output: `keep`, `studio-at-line` (with the 1-based line) or `studio` (no line).

Rules, in this order:

1. Keep anything that is not a `text` tab: every diff editor (both sides) of Git, Source Control,
   timeline, Compare with Saved, two-file compare and the search and replace preview
   (`TabInputTextDiff`), the merge editor, other custom editors (decision 14).
2. Keep a document that is not an eligible saved `file:` `.md` (an `untitled:` buffer, a `git:`
   version, a non-Markdown file).
3. Keep a text editor reopened as text on purpose: "Reopen Editor With > Text Editor" from a Studio
   tab (decision 4, 14). Signal (unproved, trial T3): in the same tab-change event, or within a short
   window, a Studio tab (`TabInputCustom`, view type `markdown-okf-schema-studio.editor`) of the same
   URI closed in the same group.
4. Keep a text editor Studio itself opened (decision 14): before Studio opens a text editor it
   records the URI for a short window; the watcher skips that URI. Studio's openings today:
   `openPreview` (`showTextDocument` of a menu URI, `activation.ts`), and
   `navigation.showDocument` (`src/host-vscode/vscodeHost.ts`, used by link navigation in
   `src/session/features/links.ts` and Back/Next across documents in
   `src/session/features/history.ts`). See open question 2 about link navigation.
5. Keep a tab that is not new: a jump into a text editor tab that was already open (for example
   Go to Line in the active text editor, a search result in a file already open as text) opens no
   text editor and stays where it is. This reads decision 13's "opened"; see open question 1.
6. With "Open Markdown files in Studio" on: `studio-at-line` when the opening carries a line,
   else `studio` (decision 13).
7. With "Open search results in Studio" on and the opening carries a line (a jump):
   `studio-at-line` (decisions 10, 13).
8. Else `keep` (a plain opening stays a text editor, decision 13).

**A jump versus a plain opening** (unproved, trial T2). Candidate signals: the first selection of
the new editor is not at line 1, column 1; the `onDidChangeTextEditorSelection` event kind
(`TextEditorSelectionChangeKind.Command`) right after the opening. A plain reopening restores the
last view state (`workbench.editor.restoreViewState`), so a non-zero cursor alone may not tell them
apart. The Driver picks the signal T2 proves. If no signal tells a restored view state from a jump,
the Driver stops and reports to the Chief of Staff (open question 4): a plain reopening must not be
pulled into Studio for users who only have the default search setting on.

The requested line is the selection's start line plus one (VS Code lines are 0-based, Studio
source lines are 1-based).

### 4.2 Putting Studio in place

New code in `src/host-vscode/openInStudio.ts`, on `studio-at-line` or `studio`:

- **No Studio tab for that file yet:** record the pending line for the URI (consumed by
  `resolvePreviewEditor`, dropped after a few seconds), open Studio with
  `vscode.commands.executeCommand("vscode.openWith", uri, EDITOR_VIEW_TYPE, { viewColumn, preview,
  preserveFocus })` in the text tab's group, keeping the text tab's preview state (`tab.isPreview`)
  and focus, then close the text tab with `vscode.window.tabGroups.close(tab, true)`.
- **A Studio tab for that file is open** (decision 3): prefer the one in the text tab's group, else
  any group. Reveal it (`vscode.openWith` with its `viewColumn`), close the text tab, and send the
  line to its live session. No new tab.
- `resolvePreviewEditor` (`activation.ts`) passes the pending line to the new session; the session
  posts it once the page is ready. The page-ready handler is in `src/session/features/rendering.ts`
  (where `manager.scroll.markEditorSelectionInPreview` is called); the new
  `postPendingRevealLine(preview)` goes in `src/session/features/scrollSync.ts`. The requested line
  wins over the reading place a Studio tab restores for its document (SwRS-MDOKFSTUDIO-LIFE-014's
  family).
- New host-to-page message `previewRevealLine` in `src/core/protocol/hostToPage.ts`:
  `{ line: number }` (1-based), addressing `render`, valid only when `line` is a safe integer
  `>= 1`; registered in the router table next to `sourceScroll`.

Unproved points (trials): the brief text editor flash and the tab position (T1); whether VS Code
opens a text tab at all when a Studio tab of that file is already open in the active group, or
reveals the Studio tab and loses the line again (T4: if it loses the line, the Driver records it as
a known issue and reports, open question 3); closing a text tab whose document is dirty while
Studio holds the same document asks nothing and loses nothing (T8); a second search result opened
in the reused preview tab (T9).

### 4.3 The two settings and the migration

**Settings** (registry `src/core/configuration/settingsRegistry.ts`, schema generated into
`package.json` by `just generate-settings`, checked by `just check-settings`): a new section `open`,
category title "Opening Files", order 6, host-only settings (`setting<boolean>`, not sent to the
page):

| Setting | Default | Meaning |
| --- | --- | --- |
| `markdownOkfSchemaStudio.open.searchResultsInStudio` (title "Open search results in Studio") | `true` | A `.md` file opened in a new text editor at a line by a jump (search, Quick Open `:line`, Problems, links, Ctrl+click, …) is replaced by the Studio tab at that line, with the marker. A plain opening stays a text editor. |
| `markdownOkfSchemaStudio.open.markdownFilesInStudio` (title "Open Markdown files in Studio") | `false` | Every `.md` file opened in a new plain text editor is replaced by the Studio tab, at the line when there is one. Diffs and "Reopen Editor With > Text Editor" stay text. |

Each `markdownDescription` (at most 700 characters, SwRS-MDOKFSTUDIO-LIFE-156) says what On and Off
do and, for `markdownFilesInStudio`, how to get the raw text (Reopen Editor With > Text Editor from
the Studio tab) and that it replaces VS Code's `workbench.editorAssociations` entry for Studio.

**Migration** (decision 12), at each activation, before the watcher starts:

- Read `vscode.workspace.getConfiguration("workbench").inspect("editorAssociations")`, its
  `globalValue` (user) and `workspaceValue` (workspace).
- In each of those scopes, when the value has the key `*.md` whose value is exactly
  `markdown-okf-schema-studio.editor`: write the value back without that key (`undefined` when
  nothing is left) with `ConfigurationTarget.Global` or `ConfigurationTarget.Workspace`, then set
  `markdownOkfSchemaStudio.open.markdownFilesInStudio` to `true` in the same target.
- Every other key, and a `*.md` entry naming another editor, is left as it is. The legacy array
  form (`[{ viewType, filenamePattern }]`) is handled the same way: only the element with
  `filenamePattern` `*.md` and `viewType` `markdown-okf-schema-studio.editor` is removed.
- The rewrite of the value is a pure function in a new file
  `src/core/configuration/editorAssociationMigration.ts` (input: the scope's value; output:
  `{ changed, value }`); the VS Code reads and writes stay in `src/host-vscode/openInStudio.ts`.
- A failed write is logged to the Studio output channel and shown once as a warning naming the
  setting; nothing else changes.
- When a migration wrote anything, the migration notice of 4.4 is shown.

Unproved (trial T6): removing the entry from real user and workspace settings files, keeping the
other keys, with no prompt.

### 4.4 Feature introductions (reusable)

New file `src/session/featureIntroductions.ts`, host-neutral (ports `KeyValueStore` and `HostUi`):

- A table of introductions by id; this CR adds one, `openInStudio`. Another feature adds a row.
- `showOnce(id, message)`: when the store has no `markdownOkfSchemaStudio.introductions.<id>`
  key, store `true` first, then show the message with `host.ui.showInformation` and no buttons
  (decision 5: shown for a few seconds, never again after it closes or disappears, even in later
  sessions).
- `resetAll()`: removes every introduction key; each introduction shows once more.
- The store is the **global** state (`context.globalState`, a `vscode.Memento`, already shaped like
  `KeyValueStore`), not the workspace state that `WorkspaceChoices` uses, so "once" holds across
  workspaces and sessions. Created and loaded by `StudioActivation.start`.

Messages (English, plain text, no button; final wording may be tightened, the content may not):

- First replacement by Studio (any `studio` or `studio-at-line`), when no migration ran: "Markdown
  files opened from a search or a jump now open in Markdown OKF-Schema Studio at that line. Change
  this in Settings: Markdown OKF-Schema Studio > Opening Files."
- After a migration wrote a setting (decision 12; shown each time the migration actually changes a
  setting, and it marks `openInStudio` as shown): "Markdown OKF-Schema Studio replaced your editor
  association for *.md with its own setting 'Open Markdown files in Studio', so Markdown files
  still open in Studio, now at the searched line. Change this in Settings: Markdown OKF-Schema
  Studio > Opening Files."

Command (decision 15): `markdown-okf-schema-studio.showFeatureIntroductionsAgain`, title "Show
Feature Introductions Again", category "Markdown OKF-Schema Studio", in the command palette always;
it calls `resetAll()` and shows "Markdown OKF-Schema Studio will show its feature introductions
again." Declared in `package.json` `contributes.commands`, registered in `activation.ts`.

Unproved (trial T5): an information notification without buttons hides on its own after a few
seconds; the trial records how many.

### 4.5 The marker in the page

New file `src/page/features/lineMarker.ts`, installed with the other page features, handling
`previewRevealLine` (registered in `src/page/features/hostHandlers.ts`). `scrollCore.ts` (583
lines) and `pageRuntime.ts` (743 lines) only gain the hooks they must expose; the 800-line ratchet
holds.

Placing the line (decision 8), in order:

1. Find the innermost mapped block that contains the line (the layout of `scrollCore`'s
   `parseMappings`); a line between blocks or outside every block takes the block with the nearest
   edge, the same rule as `markSourceLine` (SwRS-MDOKFSTUDIO-TOOLBAR-128).
2. A target inside a folded heading section, or inside a closed `details` (dropdown admonition),
   is unfolded first (`rt.parts.headingFold.reveal`, `details.open = true`), then the layout is
   measured again.
3. The exact line's top and height:
   - a paragraph: the line tops of `measureLineTops` (SwRS-MDOKFSTUDIO-LIFE-119);
   - a code block: the matching `.myst-code-line` span (`src/core/render/highlight.ts`,
     `data-line-number`), counted from the block's source range (the Driver proves the mapping with
     a unit test on a backtick fence, a tilde fence and a `{code-block}` with options);
   - a table: the row of that line (header row on the table's first line, the delimiter line maps
     to the header row, body row `n` on the table's line plus `n + 1`);
   - otherwise: the top of the block and its first line height.
4. Scroll so the line sits at the reading line below the sticky heading band, as a table of
   contents jump does (`revealElement`), silently: the page does not post `previewScroll` back.

Look (decision 6, option A of `prototypes/01-arrow-marker/`): one overlay element in the content
column, decorative (`aria-hidden="true"`), drawn with the theme tokens of
`src/core/preview/themeTokens.ts` (accent colour; readable in light, dark, cream, white and high
contrast): an arrow pointing right in the left margin, vertically centred on the line, and a light
band across the content column at the line's top and height. The target block gets
`aria-current="location"`, as `markSourceLine` does. No animation. Styles go with the other page
styles in `src/core/preview/styles/` (a new `lineMarkerStyles.ts`, or the closest existing file).

### 4.6 Lifetime of the marker and edit mode

- It stays when the reader scrolls (decision 7) and is placed again on its source line after a
  re-render, a content patch or a layout change (width, zoom, fold).
- It goes when the reader presses the pointer anywhere in the page, when an edit starts (a block
  editor, a table cell editor or a frontmatter field opens, or the page posts any source edit), or
  when another line is requested (it moves to the new line).
- Edit mode (decision 16): same arrow and band, placed so they cover neither the list item handle
  (`src/page/features/listItemMove.ts`), the table row handle (`src/page/features/tableRowMove.ts`)
  nor the block actions; no block editor opens on its own; a click on the block opens it as usual
  and removes the marker.

### 4.7 Activation

`package.json` `activationEvents` gains `onLanguage:markdown`, so the watcher and the migration
are live when a Markdown text editor opens. The warm-ups of `start` stay as they are; the trial
records the activation time. This changes SwRS-MDOKFSTUDIO-LIFE-001 (4.9) and the assertion of
`test/security/lifeReq.requirements.test.ts` "the extension activates only on its commands, its
Open With editor and panel restore": its intent changes because the feature needs activation on a
Markdown file (constitution, section 3: say why). The manifest still contributes no language, no
grammar and no `markdown.` command.

### 4.8 Documentation

- `docs/user/open-studio.md`: a section "Open at a line": the two settings, the marker, the
  migration, how to get the raw text, the reset command.
- `docs/known-limitations.md`: the brief text editor flash; "Open With... > Text Editor" from the
  Explorer with "Open Markdown files in Studio" on (7); whatever T3, T4 or T8 prove to be a limit.
- The writing skill `skills/writing-for-markdown-okf-schema-studio/` is not touched: no rendered
  syntax changes (`.agents/guidelines/writing-skill-maintenance.guideline.md`).
- `.agents/glossary/common.md`: add "line marker" (the arrow and band) and "feature introduction".

### 4.9 Requirements (okfreq)

Rules: `requirements/guidelines/requirements.guidelines.md` and `project.guidelines.md` ("During a
change"). New requirements are created with `okfreq new … --lifecycle proposed`, IDs allocated by
okfreq, markers at the code and at each test, `just requirements-update`, a dated entry under
`## 2026-11-2x` in `requirements/tiers/log.md`.

**Approved requirements changed: none.** No `approved` requirement is altered (the 14 approved
ones are StRS of BLOCK, DIAG, GFM, LAYOUT, PALETTE, CORE, REVIEW and TABLE). New SwRS derive from
lifecycle-sync StRS only, not from the approved StRS-MDOKFSTUDIO-BLOCK-003.

New (scope `lifecycle-sync`, all `proposed`):

- StRS "A reader opens a Markdown file at a searched line and sees that line marked in Studio",
  with a use case diagram (`sequenceDiagram`: the reader, VS Code, the text editor, Studio) and
  main paths (search to marked line; Studio as default editor after the migration).
- SwRS: a new text editor of a `.md` file opened at a line by a jump is replaced by the Studio tab
  at that line when `open.searchResultsInStudio` is on (default); a plain opening stays text.
- SwRS: with `open.markdownFilesInStudio` on, every new plain text editor of a `.md` file is
  replaced by the Studio tab, at the line when there is one.
- SwRS: never replaced: diff and merge editors (both sides, every diff view), non-file or
  non-Markdown documents, a text editor reopened as text from a Studio tab, a text editor Studio
  opened, a text editor tab that was already open.
- SwRS: a Studio tab of the file already open scrolls to the new line and moves the marker; no new
  tab.
- SwRS: the `*.md` association migration (user and workspace scopes, other entries untouched,
  failed write warned).
- SwRS: feature introductions shown once across sessions and workspaces, and the "Show Feature
  Introductions Again" command.
- SwRS: the line marker: placement precision (paragraph line, code line, table row, unfold, block
  top fallback), look, scroll to the reading line.
- SwRS: the marker's lifetime (scroll keeps it; pointer press, edit start, new line remove or move
  it) and its placement in edit mode.

Changed (all `proposed`, no approval needed; listed for the reviewer):

- StRS-MDOKFSTUDIO-LIFE-001: the rationale bullet "The Studio is never the default editor of
  Markdown files; the reader opts in for each file" and the user need's "without changing the
  editor that Markdown files open in by default" become: Studio never registers itself as VS
  Code's default editor; it takes the place of a text editor only through its own settings
  (search results, on by default; every Markdown file, off by default).
- SwRS-MDOKFSTUDIO-LIFE-001: activation events now include `onLanguage:markdown`; the scenario "A
  Markdown file alone: the extension stays inactive" changes to "activates, opens nothing".
- SwRS-MDOKFSTUDIO-LIFE-018: the scenario line "a .md file opened with a double click opens in the
  text editor, never in the Studio" gains "unless `open.markdownFilesInStudio` is on".
- SwRS-MDOKFSTUDIO-LIFE-156: the groups are Preview 1, Editing 2, Frontmatter 3, Comments 4,
  PlantUML 5, Opening Files 6.

The PR body's Tests section lists every requirement ID added or changed with its source and test
files; `okfreq validate --check-links --project-root .` and coverage run as CI runs them before the
PR opens.

## 5. Out of scope

- The side preview (decision 17): no marker in the side preview on a jump, no scroll sync from a
  diff, "Open Preview to Side" from the replace preview still refuses, Studio's title button stays
  hidden on a diff. These are new inbox items, not this CR.
- A rendered diff inside Studio.
- Any change to VS Code's diff editors.
- Release notes (written at release time).

## 6. Evidence

### 6.1 Host and default matrix

The behaviour depends on the shipped defaults versus configured values, and on the host. One line
per cell; every cell is checked by the real VS Code suite (6.3) unless marked.

| Cell | Settings at start | Expected |
| --- | --- | --- |
| Shipped defaults | search on, files off, no association | jump: Studio at the line with the marker; plain opening: text editor |
| Search off | search off, files off | everything stays a text editor (today's behaviour without association) |
| Files on, set by the user | search on, files on | jump: Studio at the line; plain opening: Studio at the top or its restored place |
| Files on, search off | search off, files on | jump: Studio at the line (rule 6); plain opening: Studio |
| User association to Studio | `*.md` → Studio in user settings | at activation: entry removed from user settings, files on in user settings, migration notice; then as "Files on" |
| Workspace association to Studio | `*.md` → Studio in workspace settings | same, in the workspace scope; user settings untouched |
| Association to another editor | `*.md` → another view type | untouched; VS Code opens that editor; Studio sees no text editor and does nothing |
| Host VS Code desktop, Windows and Linux | any | checked (CI integration runs Linux; trials on Windows) |
| Host VS Code for the Web, Remote, macOS, the Agents window | any | untested; labelled untested in the PR |

### 6.2 Unit and contract tests (fail on the previous code)

- `test/core/navigation/openingPolicy.test.ts`: the truth table of 4.1 (each rule, each tab kind,
  each setting pair, reopened as text, opened by Studio, tab not new, no line).
- `test/core/configuration/editorAssociationMigration.test.ts`: object form with `*.md` → Studio
  (removed, other keys kept, empty becomes `undefined`), `*.md` → another editor (unchanged), no
  `*.md` (unchanged), legacy array form, non-object garbage (unchanged).
- `test/core/configuration/settingsRegistry.test.ts`: the `open` section, its two settings and
  defaults; `just check-settings` proves `package.json` matches the registry (it reads the shipped
  `package.json`).
- `test/security/lifeReq.requirements.test.ts`: activation events now include
  `onLanguage:markdown` (changed assertion, reason in 4.7); still no language, grammar or
  `markdown.` command. `test/security/package-contract.test.ts`: the new command is declared. Both
  read the shipped `package.json` at the head under test.
- `test/session/featureIntroductions.test.ts` (memory host, `src/host-memory/`): shown once, the
  key stored before the message, not shown again after a reload of the store, `resetAll` shows it
  once more, a failed store write still shows the message once in that session.
- Protocol: `previewRevealLine` accepted with a line `>= 1`, refused with `0`, a negative, a
  fraction, a string or no line.
- Session: a pending line is posted once after the page is ready and wins over the restored
  reading place; a line for an open Studio session is posted at once.
- Page, `test/page/runtimeLineMarker.test.ts`: the line lands at the reading line; the marker is
  on the exact paragraph line, code line, table row; a folded section and a closed dropdown are
  opened; fallback to the block top; nearest block for a line outside every block; scrolling keeps
  the marker; a re-render re-places it; pointer press, block editor open, cell editor open and a
  new line remove or move it; no `previewScroll` is posted by the reveal.

### 6.3 Real VS Code: trials and integration tests

New file `test/integration/openAtLine.test.ts`, run in the trusted suite
(`test/integration/trusted-suite.ts`, which gets `STUDIO_CDP_PORT`), driving the window with
Playwright over CDP through `test/integration/realInput/harness.ts` (`connectWorkbench`, `waitFor`),
the same way as `experiments/0N-diff-view-*` of this CR drove a real window. A row is added to
`INTEGRATION_TESTS` in `test/shared/e2eGroups.ts` (group `lifecycle-sync`). Settings are set in
the test with `vscode.workspace.getConfiguration(...).update(...)` and restored after each case.

Each item below marked **unproved** rests on VS Code behaviour nobody has seen yet; the trial that
settles it runs in real VS Code before the CR is ready (decision 14), on Windows locally and in the
CI integration job (Linux; heavy run on the branch:
`gh workflow run ci.yml --ref <branch> -f heavy=true`). Its result (pass, or the limit found) goes
in the PR's evidence, with screenshots.

| Trial | Unproved behaviour | Steps | Settles |
| --- | --- | --- | --- |
| T1 | The brief text editor flash before Studio replaces it | Defaults; Search view: search a word of `doc.md` line 30, click the result. Poll the workbench DOM every frame for a visible `.monaco-editor` versus the Studio webview in that group | The time the text editor is visible (recorded; the owner judges, open question 6), the Studio tab sits where the text tab was, no empty group, the marker on line 30 |
| T2 | Telling a jump from a plain opening | Close `doc.md` with the cursor on line 30; reopen it from the Explorer (restored view state); then Quick Open `doc.md:30`; then `vscode.open` with a selection (the path of Problems and links) | Which signal of 4.1 separates them: the plain reopening stays text, the two jumps go to Studio. No signal: stop, open question 4 |
| T3 | Telling "Reopen Editor With > Text Editor" apart | Files on; a Studio tab of `doc.md`; run Reopen Editor With > Text Editor. Then the Explorer's "Open With... > Text Editor" on `other.md` | The reopened text editor stays text (required). The Explorer case: stays text if a signal exists, else documented known limit (7) |
| T4 | An already open Studio tab in the group | A Studio tab of `doc.md` active; Search view click on a match at line 40; Quick Open `doc.md:40` | VS Code opens a text tab (then: the same Studio tab scrolls to line 40, marker moved, no new tab) or reveals the Studio tab without the line (then: known issue, open question 3) |
| T5 | A notification without buttons hides after a few seconds | Fresh global state; first takeover; watch `.notification-toast` | The introduction appears once, hides on its own (seconds recorded), never again after a window reload; "Show Feature Introductions Again" makes it show once more |
| T6 | Removing a user and a workspace `editorAssociations` entry | Write `{"*.md": "markdown-okf-schema-studio.editor", "*.txt": "default"}` in user and workspace settings; run the migration through a test hook | Only `*.md` removed in each scope, `*.txt` kept, `open.markdownFilesInStudio` true in the same scope, migration notice shown, no prompt; an entry naming another editor untouched |
| T7 | Diffs stay text diffs with both settings on | Git: Open Changes; Source Control click; Timeline click; Compare Active File with Saved (edit typed in a text editor, and in a Studio tab); Compare Active File With... `other.md`; Search and replace: click a match (replace preview); Replace All with a Studio tab open; the diff's "Open File" button | Every diff stays a `.monaco-diff-editor` with no Studio tab opened by it; Replace All re-renders Studio as at 1.10.0; "Open File" from a diff is a jump and opens Studio at the line |
| T8 | Replacing a text tab whose document is dirty | `doc.md` dirty in a text editor of group 2; Search view click in group 1 | No save prompt, the unsaved text is kept and shown by Studio |
| T9 | The reused preview tab | Search view single click on a result in `doc.md`, then on one in `other.md` | Each lands in Studio at its line; no stray text tab remains |
| T10 | Text editors Studio opens itself | Files on; from a Studio page follow a link to `other.md#heading`; Back/Next to another document; Explorer "Open Preview to Side" on a non-active `.md` | Each text editor Studio opened stays text (decision 14; see open question 2) |

Merge editor, staged changes and multi-file "Open All Changes": covered by rule 1 of the policy
and its unit test, not run in a window (untested, labelled so in the PR).

### 6.4 Visual captures

New file `test/visual/lineMarkerScenarios.ts` (imported by `test/visual/scenarios.ts`), group
`lifecycle-sync`, light and dark, each scenario sending `previewRevealLine` through `hostMessages`
like the `toolbar-navigation/v37` scenarios of `test/visual/scenarioDefinitions1.ts`:

- the third line of a soft-wrapped paragraph;
- a line inside a long code block with line numbers;
- a table body row;
- a line inside a folded section (shown unfolded) and inside a closed dropdown admonition;
- edit mode on a list item and on a table row: assertion that the arrow's box intersects neither
  the list item handle nor the row handle nor the block actions;
- high contrast once.

The PR's Impacts section shows before/after captures (light and dark) per
`.agents/guidelines/pull-request.guidelines.md`.

### 6.5 Gate

`just check` (formatting, types, import boundaries, file size, unused exports, settings schema,
markers, unit and contract tests), `just requirements-update` and `just requirements-lint`, then
`just preflight` (on Windows the static stage; CI runs visual and integration). The real VS Code
suite runs on the branch with the heavy CI run before the PR leaves draft.

## 7. Known limits stated in the SwRS and the docs

- The text editor shows for a moment before Studio takes its place (decision 1); T1 measures it.
- With "Open Markdown files in Studio" on, a raw text editor opened from the Explorer's "Open
  With... > Text Editor" is replaced by Studio unless T3 finds a signal (decision 9's drawback,
  confined by decision 13 to users who chose Studio as their default). The raw text stays
  reachable with "Reopen Editor With > Text Editor" from the Studio tab, or by turning the setting
  off.
- Whatever T4 or T8 prove VS Code does not allow, written as "Known issue: …" in the SwRS, its fix
  to the backlog.

## 8. Delivery notes for the Driver

- Commits: Conventional Commits with the allowed scopes (`feat(vscode)` for the watcher, settings,
  migration, introductions and command; `feat(render)` for the marker), per
  `.agents/guidelines/git-commit-message.guidelines.md`.
- Only `src/host-vscode/` imports `vscode`; no dependency-cruiser exception.
- New worktree: `just dev` first (`.agents/guidelines/local-worktree.guidelines.md`).

## 9. Open questions for the Chief of Staff

1. **A jump into a text editor already open.** The spec keeps it a text editor (rule 5: no text
   editor is opened, so nothing is replaced). Should a search result in a file already open as
   text instead move to Studio? This matters for writers who edit in the text editor next to the
   side preview.
2. **Link and Back/Next navigation from Studio with "Open Markdown files in Studio" on.** Today,
   with the association, a link followed in Studio opens the target `.md` in Studio. Decision 14,
   read literally, keeps the text editor Studio opened, so after the migration those links open the
   text editor: a change for the owner. The spec follows decision 14 as written. Alternative: when
   that setting is on, Studio's navigation opens the target directly with `vscode.openWith` (no text
   editor, so nothing to replace).
3. **If T4 shows VS Code reveals an open Studio tab without a text editor** (the line is lost),
   decision 3 cannot hold for that case: accept it as a known issue for this CR?
4. **If T2 finds no signal that tells a jump from a plain reopening with a restored cursor**, the
   default search setting would pull plain reopenings into Studio for every user. The Driver stops
   there; what then (accept, or ship the search setting off by default)?
5. **Reach of the migration.** Decision 12 names the user and workspace scopes and the `*.md` key.
   Left untouched by this spec: a multi-root folder's own settings, and other patterns naming Studio
   (`**/*.md`, `docs/*.md`). Confirm.
6. **The flash.** No acceptable duration was decided; T1 records it and the owner judges at review.
