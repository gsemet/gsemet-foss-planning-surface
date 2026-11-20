# Open Studio at a searched line and mark it with an arrow

When a VS Code jump (a search result, Quick Open `file.md:42`, a problem, a link) opens a Markdown
file, Studio shows that file at that line, with an arrow in the left margin and a light band on the
line. Studio does it with two settings of its own instead of VS Code's editor association, migrates
the user's `*.md` association once, introduces the feature once with a notice, adds an "Open as
Text" command, and never pulls a diff view, a raw text editor asked on purpose or the
text-editor-plus-side-preview workflow into Studio.

Origin: verbal (owner, 2026-11-20). No tracker issue. Code base: `origin/main` at `a18bcac1`
(release 1.10.0 plus the CRLF fix). Every decision below comes from `02-answers.md`; decisions 12
to 32 were **decided by the Griller under the owner's autonomy rule**, not by the owner, and the
owner may change any of them at review. The PR body says so (8).

## 1. Goal, in the user's terms

- I search my workspace, click a result in a `.md` file: Studio opens at that line and an arrow
  shows me where it is. Same for Quick Open `doc.md:42`, a problem, a terminal link, a Ctrl+click.
- I keep making Studio my default Markdown editor, and I now land on the right line too; links I
  follow inside Studio keep opening Studio.
- My diffs (Git, Source Control, timeline, Compare with Saved, two-file compare, the search and
  replace preview) stay VS Code's text diffs.
- When I ask for the raw text on purpose ("Open as Text"), I get the raw text. When I work in a
  text editor with the side preview beside it, a jump stays in my text editor.

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
- The extension never writes a setting today: `test/core/configuration/settingsRegistry.test.ts`
  (SwRS-MDOKFSTUDIO-LIFE-149) asserts that no file of `src/` names `ConfigurationTarget` and that
  the only `getConfiguration(` reader is `src/host-vscode/vscodeHost.ts`. The migration
  (decision 12) must write; it does so through a new host port implemented in that same file
  (4.4), and the assertion is narrowed, with its reason (4.10, 6.2).

## 3. Decisions carried

| # | Decision (from `02-answers.md`) | Where in this spec |
| --- | --- | --- |
| 1 | Studio decides itself to open `.md` files; the text editor opens for a moment at the line, then Studio takes its place at that line with the marker | 4.1, 4.2 |
| 2 | Every entry point that opens a text editor at a line, no closed list | 4.1 |
| 3 | File already open in Studio: the same Studio tab scrolls, the marker moves, no new tab | 4.2 |
| 4 | A text editor asked for on purpose ("Reopen Editor With > Text Editor", a Studio action) stays | 4.1 (rules 4, 5), 4.3 ("Open as Text") |
| 5 | "On by default"; a feature introduction notice shown for a few seconds, once, never again even in later sessions; a reusable introduction system with a reset | 4.4, 4.5. **Reading of "on by default"** (decisions 13 and 32): it applies to "Open search results in Studio" (on by default), the setting decision 10 named after Q5; "Open Markdown files in Studio" is off by default and turned on by the migration. The PR says so for the owner's review |
| 6 | Marker: option A of `prototypes/01-arrow-marker/`: an arrow in the left margin at the exact height of the line plus a light band on that line | 4.6 |
| 7 | The marker stays until a click in the page, an edit starts, or another line is requested; scrolling keeps it | 4.7 |
| 8 | As precise as possible; **narrowed by decision 31**: exact line of a paragraph or a code block, unfold a folded heading section or a closed dropdown; otherwise the top of the enclosing block | 4.6 |
| 9 | Set aside in P3 with the drawback that opening the raw text may loop back to Studio | 4.1 (the loop is confined to the opt-in setting), 4.3 ("Open as Text"), 7 |
| 10 | A setting "open searches in Studio", on by default | 4.4 |
| 11 | The diff-view item merged here; diffs tested with this CR, they must not be pulled into Studio | 4.1, 6.3 (T7) |
| 12 | Migrate a `*.md` association to Studio: remove it from its scope, turn on "Open Markdown files in Studio" in the same scope, the notice says so; never touch an entry naming another editor | 4.4 |
| 13 | Two settings: "Open search results in Studio" (on) for jumps only; "Open Markdown files in Studio" (off, on after migration) for every opening | 4.1, 4.4 |
| 14 | Never replace a diff (either side, every diff view), a text editor reopened as text on purpose, or a text editor Studio itself opened; each proved in real VS Code before ready | 4.1, 6.3 |
| 15 | A palette command "Markdown OKF-Schema Studio: Show Feature Introductions Again" | 4.5 |
| 16 | Edit mode: same arrow and band, not covering the list item handle or block actions; no block editor opens on its own; a click opens it as usual and removes the marker | 4.7 |
| 17 | Split off: the marker in the side preview, the side preview's gaps next to a diff. This CR changes nothing in the side preview | 4.3 (the side preview's navigation is unchanged), 5 |
| 18 | Grilled enough; the spec goes through the spec critic on Fable (claude-fable-5-2) | process note, nothing to implement |
| 19 | A jump into a text editor already open stays a text editor | 4.1 (rule 3) |
| 20 | With "Open Markdown files in Studio" on, Studio's own link and Back/Next navigation to a `.md` target opens Studio directly (`vscode.openWith`, at the target line or anchor); with it off, unchanged | 4.3, 6.3 (T10) |
| 21 | If T4 shows VS Code reveals an open Studio tab without the line: a known issue (SwRS "Known issue", `docs/known-limitations.md`, a backlog item filed by the Driver); the rest ships | 4.2, 6.3 (T4), 7 |
| 22 | If T2 finds no signal telling a jump from a plain reopening: ship "Open search results in Studio" off by default, say so in the PR as a deviation from decision 10; the Driver goes on | 4.1, 4.4, 6.3 (T2), 8 |
| 23 | Migration reach: user and workspace scopes, the exact `*.md` key (object form and legacy array form); folder settings and other patterns left alone and documented in `docs/user/open-studio.md` | 4.4, 4.9 |
| 24 | The flash: no threshold; T1 records the duration in the PR's evidence, the owner judges | 6.3 (T1), 8 |
| 25 | While a side preview that follows the active editor is open, a jump stays a text editor (the side preview scrolls as today); Studio replaces a jump only when no such side preview is open | 4.1 (rule 6), 6.3 (T12) |
| 26 | Text tabs restored with the window are never replaced; only the opening that triggered activation counts, if T11 proves its line can be read; otherwise the first jump of a session stays text (known limit) | 4.1 (rule 3), 6.3 (T11), 7 |
| 27 | The migration runs once per scope, automatically, with the notice; a migrated scope is remembered; an association the user adds again later is respected (Studio then opens at the top, as today) | 4.4, 6.3 (T6) |
| 28 | Studio adds an "Open as Text" command from the Studio tab, which opens the text editor itself (kept by the rule on Studio's own openings); docs point to it; if T3 fails, the loop on "Reopen Editor With" is a known limit | 4.3, 6.3 (T3), 7 |
| 29 | Activation on `onLanguage:markdown` starts only the opening watcher and the migration; engine warm-up, watchers and diagnostics wait for the first Studio preview | 4.8 |
| 30 | One CR, narrowed by decision 31 | the whole spec; 5 |
| 31 | Marker on the exact line of a paragraph or code block, unfold a folded heading section or a closed dropdown (`details`), otherwise the top of the enclosing block (table, hidden tab of a tab-set and front matter included); the table row, the hidden `{tab-item}` selection and the front matter property row go to inbox item `line-marker-precision` | 4.6, 5 |
| 32 | "Open Markdown files in Studio" off by default, on after the migration; the PR says how Q5's "on by default" is read | 4.4, 8 |

## 4. What changes

### 4.1 The opening watcher (host, `src/host-vscode/`)

New file `src/host-vscode/openInStudio.ts` (the only place that reads VS Code's tabs for this
feature), created and started by `StudioActivation.start` in `src/host-vscode/activation.ts`.

It listens to `vscode.window.tabGroups.onDidChangeTabs`, `window.onDidChangeVisibleTextEditors`,
`window.onDidChangeActiveTextEditor` and `window.onDidChangeTextEditorSelection`. When it starts, it
records every tab already open as **present at start** (decision 26). For each **newly opened**
text editor tab it gathers facts and asks a pure policy what to do. It reads the two settings
through `host.settings.section("markdownOkfSchemaStudio.open")` (the `Settings` port), never through
`vscode.workspace` directly.

The policy is a pure function in a new file `src/core/navigation/openingPolicy.ts` (no host API, so
it is unit-tested on its own):

- Input facts: the tab's kind (`text`, `diff`, `merge`, `custom`, `other`, from `TabInputText`,
  `TabInputTextDiff`, `TabInputTextMerge`, `TabInputCustom`, anything else), the document's scheme
  and extension, whether it is eligible (`isDocumentEligible`, `src/session/sessionDocuments.ts`),
  whether the tab is new in its group, whether it was present at start, whether it is the opening
  that triggered activation (only when T11 proves the signal, else always false), the requested
  line (or none), the two settings, whether it was reopened as text from a Studio tab, whether
  Studio itself opened it, whether a side preview that follows the active editor is open.
- Output: `keep`, `studio-at-line` (with the 1-based line) or `studio` (no line).

Rules, in this order:

1. Keep anything that is not a `text` tab: every diff editor (both sides) of Git, Source Control,
   timeline, Compare with Saved, two-file compare and the search and replace preview
   (`TabInputTextDiff`), the merge editor, other custom editors (decision 14).
2. Keep a document that is not an eligible saved `file:` `.md` (an `untitled:` buffer, a `git:`
   version, a non-Markdown file).
3. Keep a tab that is not new (decisions 19, 26):
   - a jump into a text editor tab that was already open (Go to Line in the active text editor, a
     search result in a file already open as text) opens no text editor and stays where it is;
   - a tab present when the watcher started (the tabs VS Code restores with the window, and those
     open before activation) is never replaced, under either setting. Only exception: the opening
     that triggered the activation (`onLanguage:markdown`, 4.8), and only when trial T11 proves a
     signal that tells it from a restored tab (candidates: the tab is active and its
     `onDidChangeTextEditorSelection` of kind `Command` arrives after activation; the tab is not in
     the set of tabs stored at the previous shutdown in the workspace state). No proved signal: it
     stays text, and "the first jump of a session that activates the extension stays a text
     editor" is a known limit (7).
4. Keep a text editor Studio itself opened (decision 14): before Studio opens a text editor it
   records the URI for a short window (a registry in `openInStudio.ts`); the watcher skips that URI.
   Studio's openings: `openPreview` (`showTextDocument` of a menu URI, `activation.ts`),
   `navigation.showDocument` (`src/host-vscode/vscodeHost.ts`, used by link navigation in
   `src/session/features/links.ts` and Back/Next across documents in
   `src/session/features/history.ts`, when 4.3 keeps them on the text editor), and the new "Open
   as Text" command (4.3, decision 28).
5. Keep a text editor reopened as text on purpose: "Reopen Editor With > Text Editor" from a Studio
   tab (decisions 4, 14). Signal (unproved, trial T3): in the same tab-change event, or within a
   short window, a Studio tab (`TabInputCustom`, view type `markdown-okf-schema-studio.editor`) of
   the same URI closed in the same group. No proved signal: the rule is dropped, the loop on
   "Reopen Editor With" with "Open Markdown files in Studio" on is a known limit (7), and "Open as
   Text" is the documented way to the raw text (decision 28).
6. Keep a jump (an opening that carries a line) while a side preview that follows the active editor
   is open (decision 25): a live session with `followsActiveEditor` true
   (`manager.latest((preview) => preview.followsActiveEditor)`, as `openPreview` reads it). The
   side preview then scrolls to the line as today (`scrollPreviewWithEditor`, scroll sync). This
   rule applies under either setting; a plain opening (no line) goes on to rule 7.
7. With "Open Markdown files in Studio" on: `studio-at-line` when the opening carries a line,
   else `studio` (decision 13).
8. With "Open search results in Studio" on and the opening carries a line (a jump):
   `studio-at-line` (decisions 10, 13).
9. Else `keep` (a plain opening stays a text editor, decision 13).

**A jump versus a plain opening** (unproved, trial T2). Candidate signals: the first selection of
the new editor is not at line 1, column 1; the `onDidChangeTextEditorSelection` event kind
(`TextEditorSelectionChangeKind.Command`) right after the opening. A plain reopening restores the
last view state (`workbench.editor.restoreViewState`), so a non-zero cursor alone may not tell them
apart. The Driver picks the signal T2 proves. If no signal tells a restored view state from a jump
(decision 22): the default of `open.searchResultsInStudio` ships `false` (registry, 4.4), the SwRS
and the docs say so, the PR names it as a deviation from decision 10 for the owner's review, and
the Driver goes on; `open.markdownFilesInStudio` is unaffected.

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
reveals the Studio tab and loses the line again (T4: if it loses the line, decision 21: the SwRS
states it as "Known issue: …", `docs/known-limitations.md` names it, the Driver files a backlog item
in the planning surface, and the rest ships); closing a text tab whose document is dirty while
Studio holds the same document asks nothing and loses nothing (T8); a second search result opened
in the reused preview tab (T9).

### 4.3 Studio's own navigation and "Open as Text"

**Navigation from a Studio tab** (decision 20). In `src/session/features/links.ts` (the
`host.navigation.showDocument(targetId, selection)` call) and `src/session/features/history.ts`
(Back/Next to another document), when all of these hold:

- the session is an Open With Studio tab (`followsActiveEditor` false), not the side preview;
- the target's path ends in `.md` (case-insensitive);
- `markdownOkfSchemaStudio.open.markdownFilesInStudio` is on (read through `host.settings`);

the session calls the new port method `host.navigation.showDocumentInStudio(targetId, line)`
instead of `showDocument`, where `line` is the 1-based start line of the selection already computed
(the marker line or the anchor's heading range), or none. Otherwise it calls `showDocument` as
today (a text editor, kept by rule 4).

- `src/host-api/navigation.ts`: `Navigation` gains `showDocumentInStudio(documentId: string, line?:
  number): PromiseLike<void>`, documented as "shows the document in the host's Studio editor tab,
  at `line` when given".
- `src/host-vscode/vscodeHost.ts` implements it by calling the same "put Studio in place" code as
  4.2, with no text tab to close: an open Studio tab of the target (its group first) is revealed
  and gets the line through its session; otherwise the pending line is recorded and
  `vscode.openWith(uri, EDITOR_VIEW_TYPE, { viewColumn, preview: false })` opens it, in the group
  `showDocument` would pick (the group that already shows the target, else the first group). No
  text editor is opened, so nothing is replaced and nothing flashes.
- A memory host (`src/host-memory/`) and the test fakes that build a `Navigation` record the call.
- The side preview's navigation is unchanged (decision 17: this CR changes nothing in the side
  preview; its history assumes the side preview follows the text editor it opens).
- A history move inside the same document keeps today's `sourceScroll` path.

**"Open as Text"** (decision 28). New command `markdown-okf-schema-studio.openAsText`, title "Open
as Text", category "Markdown OKF-Schema Studio":

- declared in `package.json` `contributes.commands`; shown in `commandPalette` and in
  `editor/title` (an overflow entry, not a navigation icon) with the `when` clause
  `activeCustomEditorId == 'markdown-okf-schema-studio.editor'`; registered in `activation.ts`
  (`@implements_req` of its new SwRS).
- It acts on the active Studio tab: records its URI in rule 4's registry, opens the text editor in
  the same group (`vscode.window.showTextDocument(document, { viewColumn, preview: false,
  selection })`) at the source line shown at the top of the Studio page when the session knows it,
  else at the top, then closes the Studio tab (`vscode.window.tabGroups.close`). The document and
  its unsaved changes are the same `TextDocument`, so nothing is lost.
- The text editor it opens stays text under both settings (rule 4).

### 4.4 The two settings and the migration

**Settings** (registry `src/core/configuration/settingsRegistry.ts`, schema generated into
`package.json` by `just generate-settings`, checked by `just check-settings`): a new section `open`
in `SETTING_CATEGORIES`, title "Opening Files", order 6, host-only settings (`setting<boolean>`,
not sent to the page), window scope (no `scope: "resource"`):

| Setting | Default | Meaning |
| --- | --- | --- |
| `markdownOkfSchemaStudio.open.searchResultsInStudio` (title "Open search results in Studio") | `true` (`false` only in decision 22's case, 4.1) | A `.md` file opened in a new text editor at a line by a jump (search, Quick Open `:line`, Problems, links, Ctrl+click, …) is replaced by the Studio tab at that line, with the marker. A plain opening stays a text editor. A jump stays a text editor while the side preview is open. |
| `markdownOkfSchemaStudio.open.markdownFilesInStudio` (title "Open Markdown files in Studio") | `false` | Every `.md` file opened in a new plain text editor is replaced by the Studio tab, at the line when there is one. Diffs, restored tabs and the text editor of "Open as Text" stay text. |

Each `markdownDescription` (at most 700 characters, SwRS-MDOKFSTUDIO-LIFE-156) says what On and Off
do and, for `markdownFilesInStudio`, how to get the raw text ("Open as Text" from the Studio tab)
and that it replaces VS Code's `workbench.editorAssociations` entry for Studio.

**The host port for settings scopes.** New file `src/host-api/settingScopes.ts`, exported from
`src/host-api/index.ts`, an **optional** port of the host (`settingScopes?: SettingScopes`, like
`previewRenderer?`), so the many test hosts that build a `Settings` inline are untouched:

```ts
export type SettingScope = "user" | "workspace";
export interface SettingScopes {
  /** The values `section.key` holds in the user and the workspace settings (undefined when unset). */
  inspect(section: string, key: string): { user?: unknown; workspace?: unknown };
  /** Writes `section.key` in one scope (`undefined` removes it). Refuses any other key than
   *  `workbench.editorAssociations` and the `markdownOkfSchemaStudio.*` settings. */
  write(section: string, key: string, value: unknown, scope: SettingScope): PromiseLike<void>;
}
```

`src/host-vscode/vscodeHost.ts` implements it (`createVscodeSettingScopes()`, next to
`createVscodeSettings()`): `vscode.workspace.getConfiguration(section).inspect(key)` (its
`globalValue` and `workspaceValue`) and `.update(key, value, vscode.ConfigurationTarget.Global` or
`.Workspace)`; a key outside the allowed list rejects without writing. So
`src/host-vscode/vscodeHost.ts` stays the only `getConfiguration(` reader and becomes the only file
that names `ConfigurationTarget` (4.10, 6.2).

**Migration** (decisions 12, 23, 27), host-neutral, in a new file
`src/session/associationMigration.ts` (ports `SettingScopes`, `KeyValueStore`, `HostUi`, `Logger`,
and the feature introductions of 4.5), run by `StudioActivation.start` before the watcher starts:

- For each scope, `user` then `workspace`: skip it when its "migrated" mark is set (decision 27):
  `markdownOkfSchemaStudio.migrations.editorAssociation` in the global state (`context.globalState`)
  for `user`, the same key in the workspace state (`context.workspaceState`) for `workspace`.
- Read `settingScopes.inspect("workbench", "editorAssociations")`. When the scope's value has the
  key `*.md` whose value is exactly `markdown-okf-schema-studio.editor`: write the value back
  without that key (`undefined` when nothing is left), then write
  `markdownOkfSchemaStudio.open.markdownFilesInStudio` `true` in the same scope, then set the
  scope's "migrated" mark.
- Every other key, and a `*.md` entry naming another editor, is left as it is. The legacy array
  form (`[{ viewType, filenamePattern }]`) is handled the same way: only the element with
  `filenamePattern` `*.md` and `viewType` `markdown-okf-schema-studio.editor` is removed. Folder
  settings of a multi-root workspace and other patterns naming Studio (`**/*.md`, `docs/*.md`) are
  left alone (decision 23) and documented (4.9).
- A scope with nothing to migrate gets no mark, so a later activation checks it again. Once a
  scope is marked, an association the user adds again is respected: Studio does not touch it, and
  VS Code opens Studio through it, at the top, as today (decision 27).
- The rewrite of the value is a pure function in a new file
  `src/core/configuration/editorAssociationMigration.ts` (input: the scope's value; output:
  `{ changed, value }`).
- A failed write is logged to the Studio output channel and shown as a warning naming the setting
  (once per activation); the scope gets no mark, so the next activation tries again; nothing else
  changes.
- When a migration wrote anything, the migration notice of 4.5 is shown.
- A host without `settingScopes` (the memory host by default) skips the migration.

Unproved (trial T6, through a real activation): removing the entry from real user and workspace
settings files, keeping the other keys, with no prompt, once per scope.

### 4.5 Feature introductions (reusable)

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
- After a migration wrote a setting (decision 12; shown each time the migration of a scope actually
  changes a setting, which happens once per scope, decision 27, and it marks `openInStudio` as
  shown): "Markdown OKF-Schema Studio replaced your editor association for *.md with its own
  setting 'Open Markdown files in Studio', so Markdown files still open in Studio, now at the
  searched line. Use 'Open as Text' for the raw text. Change this in Settings: Markdown OKF-Schema
  Studio > Opening Files."

Command (decision 15): `markdown-okf-schema-studio.showFeatureIntroductionsAgain`, title "Show
Feature Introductions Again", category "Markdown OKF-Schema Studio", in the command palette always;
it calls `resetAll()` and shows "Markdown OKF-Schema Studio will show its feature introductions
again." Declared in `package.json` `contributes.commands`, registered in `activation.ts`.

Unproved (trial T5): an information notification without buttons hides on its own after a few
seconds; the trial records how many.

### 4.6 The marker in the page

New file `src/page/features/lineMarker.ts`, installed with the other page features, handling
`previewRevealLine` (registered in `src/page/features/hostHandlers.ts`). `scrollCore.ts` (583
lines) and `pageRuntime.ts` (743 lines) only gain the hooks they must expose; the 800-line ratchet
holds.

Placing the line (decisions 8 and 31), in order:

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
   - otherwise, the top of the enclosing visible block and its first line height: a table (any of
     its lines), a line inside a tab-set (the tab-set's top, whichever tab is shown; no tab is
     selected), the front matter (the top of the front matter block), and every other block.
4. Scroll so the line sits at the reading line below the sticky heading band, as a table of
   contents jump does (`revealElement`), silently: the page does not post `previewScroll` back.

Look (decision 6, option A of `prototypes/01-arrow-marker/`): one overlay element in the content
column, decorative (`aria-hidden="true"`), drawn with the theme tokens of
`src/core/preview/themeTokens.ts` (accent colour; readable in light, dark, cream, white and high
contrast): an arrow pointing right in the left margin, vertically centred on the line, and a light
band across the content column at the line's top and height. The target block gets
`aria-current="location"`, as `markSourceLine` does. No animation. Styles go with the other page
styles in `src/core/preview/styles/` (a new `lineMarkerStyles.ts`, or the closest existing file).

### 4.7 Lifetime of the marker and edit mode

- It stays when the reader scrolls (decision 7) and is placed again on its source line after a
  re-render, a content patch or a layout change (width, zoom, fold).
- It goes when the reader presses the pointer anywhere in the page, when an edit starts (a block
  editor, a table cell editor or a frontmatter field opens, or the page posts any source edit), or
  when another line is requested (it moves to the new line).
- Edit mode (decision 16): same arrow and band, placed so they cover neither the list item handle
  (`src/page/features/listItemMove.ts`), the table row handle (`src/page/features/tableRowMove.ts`)
  nor the block actions; no block editor opens on its own; a click on the block opens it as usual
  and removes the marker.

### 4.8 Activation

`package.json` `activationEvents` gains `onLanguage:markdown`, so the watcher and the migration
are live when a Markdown text editor opens. The manifest still contributes no language, no
grammar and no `markdown.` command.

What starts (decision 29): `StudioActivation.start` (`src/host-vscode/activation.ts`) keeps, at
activation, the registrations (commands, the custom editor provider, the panel serializer, the
event wiring), `manager.choices.load`, the feature introductions, the migration and the opening
watcher. The engine warm-up and the background services move into a new private method
`ensureServicesStarted()`, run once, by the first Studio preview: at the start of `openPreview`
(once it has an eligible document), `resolvePreviewEditor` and `deserializePreviewPanel`. It
holds `preloadMystEngine()`, `host.previewRenderer?.warm()`, the `manager.events.watchStemRoot`
loop, `manager.diagnostics.start()` and the `**/conf.py` watcher with its three handlers (their
disposables go to the activation's `context.subscriptions` as today). `stop()` stops only what was
started. A test hook `servicesStartedForTests()` in `src/host-vscode/testHooks.ts` reports it.
Activation by a Studio command or editor behaves as today, since the first preview follows at
once.

Old rules this changes (constitution, section 3: each said why):

- `test/security/lifeReq.requirements.test.ts`, "the extension activates only on its commands, its
  Open With editor and panel restore": the sorted list gains `onLanguage:markdown`, and the check
  `!event.startsWith("onLanguage")` becomes "the only `onLanguage` event is `onLanguage:markdown`"
  (still no `workspaceContains`). Why: the feature must see a Markdown text editor open before any
  Studio entry point is used; the intent kept is that the built-in Markdown support is neither
  activated nor replaced, and that a Markdown activation starts nothing heavy (new host test, 6.2).
- `docs/known-limitations.md` lines 65-66, "Files under `src/` do not auto-activate the
  extension.": becomes "Opening a Markdown file activates the extension, which then starts only
  its opening watcher and the editor association migration; the preview engine, watchers and
  diagnostics start with the first Studio preview. Other files do not activate it." Why: the
  sentence is no longer true once `onLanguage:markdown` is declared.

### 4.9 Documentation

- `docs/user/open-studio.md`: a section "Open at a line": the two settings and their defaults, the
  marker, jumps that stay text (a file already open as text, a side preview open, restored tabs),
  the migration (once per scope, what it changes; folder settings of a multi-root workspace and
  patterns other than `*.md` are left alone, decision 23; an association added again later is
  respected and opens Studio at the top, decision 27), "Open as Text" for the raw text, the reset
  command.
- `docs/known-limitations.md`: the activation sentence (4.8); the brief text editor flash; the
  Explorer's "Open With... > Text Editor" with "Open Markdown files in Studio" on (7); whatever T3,
  T4, T8 or T11 prove to be a limit.
- The writing skill `skills/writing-for-markdown-okf-schema-studio/` is not touched: no rendered
  syntax changes (`.agents/guidelines/writing-skill-maintenance.guideline.md`).
- `.agents/glossary/common.md`: add "line marker" (the arrow and band), "feature introduction" and
  "jump" (an opening of a text editor at a line).

### 4.10 Requirements (okfreq)

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
  main paths (search to marked line; Studio as default editor after the migration; raw text with
  "Open as Text").
- SwRS: a new text editor of a `.md` file opened at a line by a jump is replaced by the Studio tab
  at that line when `open.searchResultsInStudio` is on (default, or off in decision 22's case); a
  plain opening stays text.
- SwRS: with `open.markdownFilesInStudio` on, every new plain text editor of a `.md` file is
  replaced by the Studio tab, at the line when there is one.
- SwRS: never replaced: diff and merge editors (both sides, every diff view), non-file or
  non-Markdown documents, a text editor tab that was already open, a tab present at start
  (restored), a text editor Studio opened ("Open as Text", its own reveals and navigation), a text
  editor reopened as text from a Studio tab (or "Known issue" if T3 fails), a jump while a side
  preview that follows the active editor is open.
- SwRS: a Studio tab of the file already open scrolls to the new line and moves the marker; no new
  tab (or "Known issue" if T4 shows the line is lost).
- SwRS: with `open.markdownFilesInStudio` on, link and Back/Next navigation from a Studio tab to a
  `.md` target opens Studio directly at the target line; off, or from the side preview, it opens a
  text editor as today.
- SwRS: the "Open as Text" command.
- SwRS: the `*.md` association migration (user and workspace scopes, once per scope and
  remembered, other entries untouched, an association added again respected, failed write
  warned and retried).
- SwRS: feature introductions shown once across sessions and workspaces, and the "Show Feature
  Introductions Again" command.
- SwRS: the line marker: placement precision (paragraph line, code line, unfold, enclosing block
  top for a table, a tab-set and the front matter, nearest block), look, scroll to the reading line.
- SwRS: the marker's lifetime (scroll keeps it; pointer press, edit start, new line remove or move
  it) and its placement in edit mode.

Changed (all `proposed`, no approval needed; listed for the reviewer, each with its reason):

- StRS-MDOKFSTUDIO-LIFE-001:
  - the user need's "without changing the editor that Markdown files open in by default" and the
    rationale bullet "The Studio is never the default editor of Markdown files; the reader opts in
    for each file" become: Studio never registers itself as VS Code's default editor; it takes the
    place of a text editor only through its own settings (search results, on by default; every
    Markdown file, off by default). Why: a jump now opens Studio by default (decision 10).
  - the rationale bullet "The Studio changes none of the built-in settings" becomes "The Studio
    changes none of the built-in Markdown preview's settings; outside its own settings, the only
    VS Code setting it writes is the user's `workbench.editorAssociations` entry for `*.md` that
    names Studio, removed once per scope by the migration." Why: decision 12.
- SwRS-MDOKFSTUDIO-LIFE-001: activation events now include `onLanguage:markdown`; the boundary
  scenario "A Markdown file alone: the extension stays inactive" becomes "the extension activates
  and starts only the opening watcher and the migration; it opens nothing with both opening
  settings off"; the criterion "exactly four entries" becomes five. Why: 4.8.
- SwRS-MDOKFSTUDIO-LIFE-018: the scenario line "a .md file opened with a double click opens in the
  text editor, never in the Studio" gains "unless `open.markdownFilesInStudio` is on".
- SwRS-MDOKFSTUDIO-LIFE-149:
  - the boundary scenario "Native diff" loses its parenthesis "so the extension is not yet active
    at that moment" (no longer true: the diff's Markdown documents activate the extension) and
    becomes "GIVEN the Studio active and both opening settings on, WHEN the reader opens a text
    diff of two Markdown files, THEN the native text diff opens as usual and no Studio tab opens".
    `test/integration/stockCoexistence.test.ts` keeps its assertion (the diff tab opens) and gains
    the check that no `TabInputCustom` of `markdown-okf-schema-studio.editor` appeared; its
    comment about the inactive extension goes. Why: `onLanguage:markdown` (4.8); the intent (the
    native diff is untouched) is kept and widened.
  - the verification note "one reader" stays; "it is checked by reading the code, where no write
    to a markdown.* key exists" becomes "the only file that writes a setting is
    `src/host-vscode/vscodeHost.ts` (the `SettingScopes` port), which refuses any key other than
    `workbench.editorAssociations` and the `markdownOkfSchemaStudio.*` settings". Why: decision 12.
- SwRS-MDOKFSTUDIO-LIFE-156: the groups are Preview 1, Editing 2, Frontmatter 3, Comments 4,
  PlantUML 5, Opening Files 6.

The PR body's Tests section lists every requirement ID added or changed with its source and test
files; `okfreq validate --check-links --project-root .` and coverage run as CI runs them before the
PR opens.

## 5. Out of scope

- The side preview (decision 17): no marker in the side preview on a jump (inbox item
  `side-preview-jump-marker`), no scroll sync from a diff, "Open Preview to Side" from the replace
  preview still refuses, Studio's title button stays hidden on a diff (inbox item
  `side-preview-diff-gaps`); the side preview's link and history navigation is unchanged.
- The marker's extra precision (decision 31, inbox item `line-marker-precision`): the table row of
  the line, selecting a hidden `{tab-item}`, the front matter property row.
- Migrating folder settings of a multi-root workspace, or patterns other than the exact `*.md` key
  (decision 23).
- A rendered diff inside Studio. Any change to VS Code's diff editors.
- Release notes (written at release time).

## 6. Evidence

### 6.1 Host and default matrix

The behaviour depends on the shipped defaults versus configured values, and on the host. One line
per cell, with the trial that checks it in real VS Code (6.3); a cell marked "unit only" is checked
by the policy's truth table (6.2) and labelled so in the PR.

| Cell | Settings at start | Expected | Checked by |
| --- | --- | --- | --- |
| Shipped defaults | search on, files off, no association | jump: Studio at the line with the marker; plain opening: text editor | T1, T2, T9 |
| Shipped defaults, decision 22's case | search off by default, files off | everything stays a text editor | T12 (as "Search off") |
| Search off | search off, files off | everything stays a text editor (today's behaviour without association) | T12 |
| Files on, set by the user | search on, files on | jump: Studio at the line; plain opening: Studio at the top or its restored place | T3, T10, T12 |
| Files on, search off | search off, files on | jump: Studio at the line (rule 7); plain opening: Studio | T12 |
| Side preview open | defaults, side preview open on `doc.md` | jump: text editor at the line, side preview scrolled as today | T12 |
| Window restored with `.md` text tabs | files on | restored tabs stay text | T11 |
| Cold window, first jump activates the extension | defaults, extension inactive | Studio at the line if T11 proves the signal, else text (known limit) | T11 |
| User association to Studio | `*.md` → Studio in user settings | at activation: entry removed from user settings, files on in user settings, migration notice; then as "Files on"; not repeated after a reload; an association added again is kept | T6 |
| Workspace association to Studio | `*.md` → Studio in workspace settings | same, in the workspace scope; user settings untouched | T6 |
| Association to another editor | `*.md` → another view type in user settings | untouched after activation; VS Code opens that editor; Studio sees no text editor and does nothing | T6 (second launch) |
| Host VS Code desktop, Windows and Linux | any | checked (CI integration runs Linux; trials on Windows) | all trials |
| Host VS Code for the Web, Remote, macOS, the Agents window | any | untested; labelled untested in the PR | none |

### 6.2 Unit and contract tests (fail on the previous code)

- `test/core/navigation/openingPolicy.test.ts`: the truth table of 4.1 (each rule in order, each
  tab kind, each setting pair, reopened as text, opened by Studio, tab not new, present at start,
  activation opening, side preview open with and without a line, no line).
- `test/core/configuration/editorAssociationMigration.test.ts`: object form with `*.md` → Studio
  (removed, other keys kept, empty becomes `undefined`), `*.md` → another editor (unchanged), no
  `*.md` (unchanged), `**/*.md` → Studio (unchanged), legacy array form, non-object garbage
  (unchanged).
- `test/session/associationMigration.test.ts` (memory ports with an in-memory `SettingScopes`):
  both scopes migrated and marked; a marked scope is skipped even when the association is back; a
  scope with nothing to migrate is not marked; a failed write warns, marks nothing and leaves the
  other scope's result; the notice is shown when something was written; a host without
  `settingScopes` does nothing.
- `test/core/configuration/settingsRegistry.test.ts`:
  - the `open` section, its two settings and defaults; `just check-settings` proves `package.json`
    matches the registry (it reads the shipped `package.json`).
  - **Changed assertion** (SwRS-MDOKFSTUDIO-LIFE-149, lines 144-160): the loop
    `assert.ok(!/ConfigurationTarget/u.test(text), … "writes no setting")` becomes: the list of
    files naming `ConfigurationTarget` equals `["src/host-vscode/vscodeHost.ts"]`. The `readers`
    assertion (`["src/host-vscode/vscodeHost.ts"]`) and the `markdown.preview` check are unchanged.
    Why (constitution, section 3): decision 12 needs one write path; the intent kept is that
    settings are reached through one host file and no `markdown.*` key is written.
- `test/host-vscode/settingScopes.test.ts` (or the closest existing host test file, with the fake
  `vscode` of `test/host/fakeVscode.ts`, whose `getConfiguration` gains `inspect` and `update`):
  `write` refuses a `markdown.preview.*` key and any key outside the allowed list without calling
  `update`; `inspect` maps `globalValue` and `workspaceValue`.
- `test/security/lifeReq.requirements.test.ts`: activation events include `onLanguage:markdown`
  (changed assertion, reason in 4.8); still no other `onLanguage`, no `workspaceContains`, no
  language, grammar or `markdown.` command. `test/security/package-contract.test.ts`: the two new
  commands are declared, `openAsText` with its `when` clause. Both read the shipped `package.json`
  at the head under test.
- Host test (`test/host/lifeReq.requirements.test.ts` or a new `test/host/openAtLine.test.ts`): an
  activation with no preview leaves `servicesStartedForTests()` false and calls neither the
  renderer warm-up nor `diagnostics.start`; the first `openPreview` starts them once; a second
  preview does not start them again.
- `test/session/featureIntroductions.test.ts` (memory host, `src/host-memory/`): shown once, the
  key stored before the message, not shown again after a reload of the store, `resetAll` shows it
  once more, a failed store write still shows the message once in that session.
- Session navigation (`test/session/`): from a Studio tab with files on, a link to `other.md#h`
  and a Back/Next to another document call `showDocumentInStudio` with the heading's line; with
  files off, or from the side preview, they call `showDocument` as today.
- Protocol: `previewRevealLine` accepted with a line `>= 1`, refused with `0`, a negative, a
  fraction, a string or no line.
- Session: a pending line is posted once after the page is ready and wins over the restored
  reading place; a line for an open Studio session is posted at once.
- Page, `test/page/runtimeLineMarker.test.ts`: the line lands at the reading line; the marker is
  on the exact paragraph line and code line; a folded section and a closed dropdown are opened; a
  line in a table, in a hidden tab of a tab-set and in the front matter marks the enclosing block's
  top and selects no tab; nearest block for a line outside every block; scrolling keeps the marker;
  a re-render re-places it; pointer press, block editor open, cell editor open and a new line
  remove or move it; no `previewScroll` is posted by the reveal.

### 6.3 Real VS Code: trials and integration tests

Two new places, both driving a real window with Playwright over CDP, the same way as
`experiments/0N-diff-view-*` of this CR drove one:

- `test/integration/openAtLine.test.ts`, run in the trusted suite
  (`test/integration/trusted-suite.ts`, which gets `STUDIO_CDP_PORT`), through
  `test/integration/realInput/harness.ts` (`connectWorkbench`, `waitFor`): T1 to T5, T7 to T10, T12.
  Settings are set in the test with `vscode.workspace.getConfiguration(...).update(...)` and
  restored after each case.
- `test/integration/openAtLineCampaign.ts`, a campaign that launches its own windows from outside
  (no host suite), like `runReloadCampaign` of `test/integration/reload-suite.ts`: it writes the
  user `settings.json` before the launch (`writeTestProfileSettings` of `test/shared/testProfile.ts`
  gains an optional object of extra user settings) and a temporary workspace with its own
  `.vscode/settings.json`, starts VS Code with the extension inactive, drives it, reloads the
  window, and reads the settings files back from disk. Called by `run-tests.ts` after the reload
  campaign, with an `--open-at-line-only` flag, under `watchLaunch` with its own deadline: T6 and
  T11.

Both get a row in `INTEGRATION_TESTS` of `test/shared/e2eGroups.ts` (group `lifecycle-sync`).

Each item below marked **unproved** rests on VS Code behaviour nobody has seen yet; the trial that
settles it runs in real VS Code before the CR is ready (decision 14), on Windows locally and in the
CI integration job (Linux; heavy run on the branch:
`gh workflow run ci.yml --ref <branch> -f heavy=true`). Its result (pass, or the limit found) goes
in the PR's evidence, with screenshots.

| Trial | Unproved behaviour | Steps | Settles |
| --- | --- | --- | --- |
| T1 | The brief text editor flash before Studio replaces it | Defaults; Search view: search a word of `doc.md` line 30, click the result. Poll the workbench DOM every frame for a visible `.monaco-editor` versus the Studio webview in that group | The time the text editor is visible, recorded in the PR's evidence with no threshold (decision 24); the Studio tab sits where the text tab was, no empty group, the marker on line 30 |
| T2 | Telling a jump from a plain opening | Close `doc.md` with the cursor on line 30; reopen it from the Explorer (restored view state); then Quick Open `doc.md:30`; then `vscode.open` with a selection (the path of Problems and links) | Which signal of 4.1 separates them: the plain reopening stays text, the two jumps go to Studio. No signal: decision 22 (search setting off by default, PR deviation), the Driver goes on |
| T3 | The raw text on purpose | Files on; a Studio tab of `doc.md`: run "Open as Text"; then a Studio tab of `doc.md`: Reopen Editor With > Text Editor; then the Explorer's "Open With... > Text Editor" on `other.md` | "Open as Text": the text editor stays text, at the page's top line, the Studio tab closed (required). Reopen Editor With: stays text if a signal exists, else a known limit (decision 28). Explorer case: same |
| T4 | An already open Studio tab in the group | A Studio tab of `doc.md` active; Search view click on a match at line 40; Quick Open `doc.md:40` | VS Code opens a text tab (then: the same Studio tab scrolls to line 40, marker moved, no new tab) or reveals the Studio tab without the line (then: decision 21, known issue, backlog item, the rest ships) |
| T5 | A notification without buttons hides after a few seconds | Fresh global state; first takeover; watch `.notification-toast` | The introduction appears once, hides on its own (seconds recorded), never again after a window reload; "Show Feature Introductions Again" makes it show once more |
| T6 | The migration at a real activation (campaign) | Launch 1: user `settings.json` and workspace `.vscode/settings.json` each hold `{"*.md": "markdown-okf-schema-studio.editor", "*.txt": "default"}` in `workbench.editorAssociations`; the extension inactive (`isActive` false, read over CDP from the extension host or by the absence of its output channel); open `doc.md` from the Explorer (the real `onLanguage:markdown` activation). Then add the `*.md` association again in user settings, reload the window. Launch 2: user settings hold `*.md` → the built-in Markdown preview's custom editor (view type read from the built-in extension's `package.json`); open `doc.md` | Launch 1: in each file only `*.md` removed, `*.txt` kept, `open.markdownFilesInStudio` true in the same file, migration notice shown, no prompt; after the reload the re-added entry is still there, no notice, `doc.md` opens in Studio at the top. Launch 2: the entry unchanged, no Studio setting written, no notice, the built-in preview opens and no Studio tab |
| T7 | Diffs stay text diffs with both settings on | Git: Open Changes; Source Control click; Timeline click; Compare Active File with Saved (edit typed in a text editor, and in a Studio tab); Compare Active File With... `other.md`; Search and replace: click a match (replace preview); Replace All with a Studio tab open; the diff's "Open File" button | Every diff stays a `.monaco-diff-editor` with no Studio tab opened by it; Replace All re-renders Studio as at 1.10.0; "Open File" from a diff is a jump and opens Studio at the line |
| T8 | Replacing a text tab whose document is dirty | `doc.md` dirty in a text editor of group 2; Search view click in group 1 | No save prompt, the unsaved text is kept and shown by Studio |
| T9 | The reused preview tab | Search view single click on a result in `doc.md`, then on one in `other.md` | Each lands in Studio at its line; no stray text tab remains |
| T10 | Studio's own openings and navigation | Files on: from a Studio tab follow a link to `other.md#heading`; Back/Next to another document; from the side preview follow the same link; Explorer "Open Preview to Side" on a non-active `.md`. Files off: from a Studio tab follow the same link | Files on, Studio tab: Studio opens `other.md` at the heading and no `TabInputText` of `other.md` ever appears (decision 20); Back/Next lands in Studio. Side preview link and "Open Preview to Side": the text editor Studio opened stays text. Files off: the link opens a text editor that stays text |
| T11 | Window start and the first activation (campaign) | Launch 3: files on in user settings; open `doc.md` in a text editor at line 30 with Reopen Editor With > Text Editor (or "Open as Text"); reload the window. Launch 4: defaults, no tab open, extension inactive; Search view click on a match in `doc.md` line 30 | After the reload the restored `doc.md` tab stays text (required). Launch 4: Studio at line 30 if a signal of rule 3 tells the activating opening from a restored tab, else it stays text and the known limit is written (decision 26) |
| T12 | The other matrix cells | Search off, files off: Search view click and Explorer open on `doc.md`. Search off, files on: the same two. Defaults with the side preview open on `doc.md` (from "Open Preview to Side"): Search view click on line 30 of `doc.md` and of `other.md` | Search off, files off: both stay text, no Studio tab. Search off, files on: the click lands in Studio at line 30, the Explorer opening in Studio. Side preview open: each jump stays a text editor at the line and the side preview scrolls to it, as at 1.10.0 (decision 25) |

Merge editor, staged changes and multi-file "Open All Changes": covered by rule 1 of the policy
and its unit test, not run in a window ("unit only", labelled so in the PR).

### 6.4 Visual captures

New file `test/visual/lineMarkerScenarios.ts` (imported by `test/visual/scenarios.ts`), group
`lifecycle-sync`, light and dark, each scenario sending `previewRevealLine` through `hostMessages`
like the `toolbar-navigation/v37` scenarios of `test/visual/scenarioDefinitions1.ts`:

- the third line of a soft-wrapped paragraph;
- a line inside a long code block with line numbers;
- a line inside a table (the marker at the table's top);
- a line inside a folded section (shown unfolded) and inside a closed dropdown admonition;
- edit mode on a list item and on a table: assertion that the arrow's box intersects neither
  the list item handle nor the row handle nor the block actions;
- high contrast once.

The PR's Impacts section shows before/after captures (light and dark) per
`.agents/guidelines/pull-request.guidelines.md`.

### 6.5 Gate

`just check` (formatting, types, import boundaries, file size, unused exports, settings schema,
markers, unit and contract tests), `just requirements-update` and `just requirements-lint`, then
`just preflight` (on Windows the static stage; CI runs visual and integration). The real VS Code
suite and the open-at-line campaign run on the branch with the heavy CI run before the PR leaves
draft.

## 7. Known limits stated in the SwRS and the docs

- The text editor shows for a moment before Studio takes its place (decision 1); T1 measures it.
- With "Open Markdown files in Studio" on, a raw text editor opened from the Explorer's "Open
  With... > Text Editor", or by "Reopen Editor With > Text Editor" when T3 finds no signal, is
  replaced by Studio (decision 9's drawback, confined by decision 13 to users who chose Studio as
  their default; decision 28). The raw text stays reachable with "Open as Text" from the Studio
  tab, or by turning the setting off.
- If T11 finds no signal: the first jump of a session that activates the extension stays a text
  editor (decision 26).
- If T4 shows the line is lost: "Known issue: a jump to a file already open in a Studio tab
  reveals the tab without moving to the line", with its backlog item (decision 21).
- Whatever T8 proves VS Code does not allow, written as "Known issue: …" in the SwRS, its fix to
  the backlog.

## 8. Delivery notes for the Driver

- Commits: Conventional Commits with the allowed scopes (`feat(vscode)` for the watcher, settings,
  migration, introductions, navigation and commands; `feat(render)` for the marker), per
  `.agents/guidelines/git-commit-message.guidelines.md`.
- Only `src/host-vscode/` imports `vscode`; no dependency-cruiser exception.
- New worktree: `just dev` first (`.agents/guidelines/local-worktree.guidelines.md`).
- The PR body says, for the owner's review: decisions 12 to 32 were decided by the Griller under
  the owner's autonomy rule; open-at-line-Q5's "on by default" is read as the search setting's
  default (decisions 13, 32); in decision 22's case, the search setting ships off as a deviation
  from decision 10; the flash duration measured by T1 (decision 24); every known limit or known
  issue the trials found, with its backlog item.

## 9. Open questions for the Chief of Staff

None. The six open questions of the first version were decided in series 5 (decisions 19 to 24)
and the spec critic's questions in series 6 (decisions 25 to 32).
