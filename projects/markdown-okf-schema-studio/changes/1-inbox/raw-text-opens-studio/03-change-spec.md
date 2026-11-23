# Remove the opening watcher: the raw text stays text (1.12.1)

An urgent fix, released at once as 1.12.1. The extension no longer replaces a text tab by a Studio
tab. Opening every Markdown file in Studio goes back to VS Code's own setting
`workbench.editorAssociations`. The side preview's line marker on a jump and the command "Open as
Text" stay.

Short name: `raw-text`. Origin: verbal (owner, bug day 2026-11-23, batch-09). No issue.

Code repository: `markdown-okf-schema-studio`, `main` at `2e2efa6` (tag `v1.12.0` is the published
version). Read its `AGENTS.md` and `.agents/constitution.md` before any change; this spec links to
those rules and does not restate them.

## 1. Goal

Today (published 1.12.0), a reader who asks for the raw text of a Markdown file does not get it.
With the setting "open Markdown files in Studio" on, "Open With... > Text Editor" (or "Reopen
Editor With... > Text Editor", or another editor) opens the text for an instant, then Studio takes
its place.

After this change:

- An explicit request for the raw text always gives the text, and it stays: "Open as Text", "Open
  With... > Text Editor", "Reopen Editor With... > Text Editor", with or without a line.
- No code of the extension ever closes or replaces a text tab to put Studio in its place.
- A user who wants every Markdown file in Studio uses VS Code's native association
  (`"workbench.editorAssociations": { "*.md": "markdown-okf-schema-studio.editor" }`), as before the
  opening feature.
- A user who had turned the Studio setting on keeps the same daily behaviour without doing
  anything: the extension puts the native association back for them, silently.

## 2. Facts found in the code (the Driver starts from these)

### 2.1 A correction of the brief: the feature shipped in 1.11.0, not in 1.12.0

- `e883dfb6` (open a Markdown file at its line in Studio), `60036628` and `782c69a1` are in
  `v1.11.0` (2026-11-21). They brought: the opening watcher, the two settings
  `open.searchResultsInStudio` and `open.markdownFilesInStudio`, the association migration, the
  command "Open as Text", the activation event `onLanguage:markdown`, the feature introductions
  mechanism.
- `dfc07437` (the side preview marks the line of a jump; it also added the rule "a jump is never
  reopened as text") is in `v1.12.0` (2026-11-22).
- So the state "before the feature" is **1.10.0**, not 1.11. The bug is reported on 1.12.0 and
  exists since 1.11.0. Release texts must say "since 1.11.0" where they name the origin. The
  CHANGELOG section of 1.11.0 and `docs/releases-notes/2026-11-21-v1.11.0/` are history: not
  rewritten.

### 2.2 Why the text is replaced

`src/core/navigation/openingPolicy.ts`, `openingDecision`: a text editor of a Markdown file that
becomes active is replaced by Studio unless one of nine rules says no. "Open With... > Text Editor"
matches none of them when `open.markdownFilesInStudio` is on, so the watcher
(`src/host-vscode/openingWatcher.ts`) closes the text tab and opens Studio
(`src/host-vscode/studioPlacement.ts`, `putStudioInPlace`). The owner chose not to add a tenth rule
but to remove the mechanism.

### 2.3 What the kept features really use

| Kept feature | Uses | Does not use |
| --- | --- | --- |
| Side preview line marker on a jump (SwRS LIFE-186..191) | `src/host-vscode/editorJumps.ts`, `src/core/navigation/jumpSignal.ts`, class `StudioSelections` of `src/host-vscode/openInStudio.ts`, `requestJumpMarker` / `requestRevealLine` / `pendingRevealLine` in `src/session/features/scrollSync.ts`, `src/core/navigation/pendingLine.ts` | the watcher, `StudioLineRequests`, `StudioOpenedTextEditors`, `StudioClosedTabs` |
| Line marker drawn in the page (SwRS LIFE-178..180, 192..194) | `src/page/features/lineMarker.ts`, `lineMarkerPlacement.ts`, `src/core/preview/styles/lineMarkerStyles*.ts`, `previewRevealLine` in `src/core/protocol/hostToPage.ts` | anything of the watcher |
| "Open as Text" (SwRS LIFE-177) | `StudioActivation.openAsText()` in `src/host-vscode/activation.ts`, `StudioSelections.expect(uri, line, "no-mark")` so the side preview does not mark that opening | `openedByStudio.record(...)` (only the watcher read it) |
| Links, Back and Next followed in the side preview (SwRS LIFE-191) | `host.navigation.showDocument(...)`, `selections.expect(..., "marked-by-session")`, `requestJumpMarker` | `showDocumentInStudio`, `navigatesInStudio` |

`StudioLineRequests` (the line handed to a Studio tab that opens) has one producer only:
`putStudioInPlace`. Once the watcher and `showDocumentInStudio` are gone it has no producer, so it
goes too.

## 3. Decisions of the owner (from `02-answers.md`, all carried)

| # | Question | Decision | Where in this spec |
| --- | --- | --- | --- |
| 1 | Gesture | "Open With... > Text Editor" (or another editor) on a Markdown file: Studio takes its place at once | 1, 2.2, 7.3 |
| 2 | Version | The published 1.12.0 | 2.1 |
| 3 | Expected | Always the text: an explicit request for the raw text (Open as Text, Open With / Reopen Editor With > Text Editor) opens the text and is never replaced by Studio, even with a line | 1, 7.3 |
| 4 | Design | The native association (`workbench.editorAssociations`) | 4, 5 |
| 5 | Jumps under the native association | Open at the line: split out to the P1 CR `studio-at-searched-line` | 6 |
| 6 | Delivery | Two CRs; this one is the revert, released as 1.12.1 | 4.9, 6 |
| 7 | Scope | Remove the whole watcher; both settings go; the side preview's line marker on a jump (`dfc07437`) and "Open as Text" stay | 4 |
| 8 | Migration | On the first activation of 1.12.1, a user whose `open.markdownFilesInStudio` is on gets the `*.md` → Studio entry back in `workbench.editorAssociations`, and the setting is removed, without a question | 5 |

## 4. What changes, area by area

This is a removal by hand, not a `git revert`: `dfc07437` and later commits are built on the same
files and must stay.

### 4.1 `src/host-vscode`

- Delete `openingWatcher.ts` (`startOpeningWatcher`) and `studioPlacement.ts`
  (`trackStudioActivation`, `putStudioInPlace`).
- `openInStudio.ts`: delete the classes `StudioOpenedTextEditors`, `StudioLineRequests` and
  `StudioClosedTabs`. Keep `StudioSelections` unchanged (`expect`, `take`,
  `STUDIO_SELECTION_WINDOW_MS`, purposes `"no-mark"` and `"marked-by-session"`, marker
  `@implements_req SwRS-MDOKFSTUDIO-LIFE-186`). The module then holds one class: rename the file to
  `studioSelections.ts` (the test is already `test/host/studioSelections.test.ts`) and update the
  imports and the "Implementation" list of SwRS LIFE-186.
- `activation.ts` (`StudioActivation`):
  - remove the fields `openedByStudio`, `lineRequests`, `closedStudioTabs`, the call
    `lineRequests.bindLiveSessions(...)`, the calls `startOpeningWatcher({...})` and
    `trackStudioActivation()`;
  - `createVscodeHost(...)` takes the selections only;
  - `openAsText()`: remove `this.openedByStudio.record(documentUri)`; keep everything else (the
    `studioSelections.expect(documentUri, line, "no-mark")`, `showTextDocument` with the selection
    in the same column, closing the Studio tab);
  - `openPreview()`: remove `this.openedByStudio.record(...)`;
  - `resolvePreviewEditor`: remove `this.lineRequests.takePending(...)` and the
    `requestRevealLine` call that only served it, with their `@implements_req LIFE-181` markers;
  - keep `startEditorJumps({ selections })` and `editorJumps.onJump(...)` (LIFE-187), the command
    `markdown-okf-schema-studio.openAsText` (LIFE-177), `ensureServicesStarted()` (LIFE-004);
  - the migration call stays at the same place in `start()` but calls the new reverse migration
    (section 5).
- `vscodeHost.ts`: `createVscodeNavigation` and `createVscodeHost` take the selections only;
  `showDocument` no longer records `openedByStudio` and keeps `selections.expect(...,
  "marked-by-session")`; delete `showDocumentInStudio`. Keep `isWritableSetting` and
  `createVscodeSettingScopes()` (the reverse migration writes through them); the allowed writes
  stay `workbench.editorAssociations` and `markdownOkfSchemaStudio.*`.
- `editorJumps.ts`: no behaviour change. Update the comments that name the opening watcher.

### 4.2 `src/core`

- Delete `navigation/openingPolicy.ts` (`studioTargetFor`, `openingDecision`).
- `navigation/jumpSignal.ts`, `navigation/pendingLine.ts`: kept; update comments that name the
  watcher.
- `configuration/settingsRegistry.ts`: remove `DEFAULT_SEARCH_RESULTS_IN_STUDIO`, `OPEN_SETTINGS`
  and the category `{ section: "open", title: "Opening Files", order: 6 }`. Then run
  `just generate-settings`: `package.json` loses the group "Opening Files" and the properties
  `markdownOkfSchemaStudio.open.searchResultsInStudio` and
  `markdownOkfSchemaStudio.open.markdownFilesInStudio`. (See open question 3 for the fallback if
  VS Code refuses to remove a value of an undeclared key.)
- `configuration/editorAssociationMigration.ts`: replace `removeStudioMarkdownAssociation` by its
  pure inverse (section 5.2). Keep `STUDIO_EDITOR_VIEW_TYPE`.

### 4.3 `src/session` and `src/host-api`

- `host-api/navigation.ts`: remove `showDocumentInStudio` from the `Navigation` port, and from
  every implementation (`host-memory`, test fakes).
- Delete `session/features/studioNavigation.ts` (`navigatesInStudio`). Its two callers,
  `session/features/links.ts` and `session/features/history.ts`, always call
  `host.navigation.showDocument(...)` again. Their `requestJumpMarker` calls for the side preview
  (`@implements_req LIFE-191`) stay.
- `session/associationMigration.ts`: replaced by the reverse migration (section 5).
- `session/featureIntroductions.ts`: `showOnce` is called nowhere in `src/`; the only use is
  `markShown("openInStudio")` from the old migration. With the feature gone the mechanism is dead.
  Proposed: delete it, with the command `markdown-okf-schema-studio.showFeatureIntroductionsAgain`
  ("Show Feature Introductions Again": `package.json` `commands` and `commandPalette`,
  registration in `activation.ts`) and SwRS LIFE-176. This removes a palette command the answers
  do not name: open question 2. If the owner says keep, leave the file, the command and LIFE-176
  as they are and only drop the `openInStudio` entry's use by the migration.

### 4.4 `package.json`

- Settings: regenerated (4.2). Never edited by hand.
- `activationEvents`: keep `onLanguage:markdown`. The users to migrate have no association left,
  so their Markdown files open as text; this event is what activates the extension for them.
- Commands: `openAsText` stays as it is (palette `when activeCustomEditorId ==
  'markdown-okf-schema-studio.editor'`, `editor/title` group `1_markdown@1`).
- `version` stays 1.12.0 in this CR: the version commit belongs to the release CR.

### 4.5 Resulting behaviour, in the user's terms

| Gesture | Association `*.md` → Studio set | Association not set (shipped default) |
| --- | --- | --- |
| Click a Markdown file in the Explorer | Studio tab (VS Code does it) | text editor |
| "Open With... > Text Editor", "Reopen Editor With... > Text Editor" | text editor, stays | text editor |
| "Open as Text" from a Studio tab | text editor at the top visible line, stays; the Studio tab closes | same |
| Search result, Go to Definition, problem, link from another file (a jump with a line) | what VS Code does natively: Studio tab, at the top (the line is not shown). Known gap, owned by `studio-at-searched-line` | text editor at the line |
| Same jump, side preview open on that file | text editor at the line and the side preview marks the line (unchanged) | same |
| Link, Back or Next followed inside a Studio tab | the target opens as VS Code decides: Studio tab, at the top (open question 1) | text editor at the line |
| Diff editor, Source Control, merge editor | untouched by the extension | untouched |

### 4.6 Tests

Per the constitution: a behaviour change needs a test that fails on the previous code, and the
intent of an assertion is never changed silently. Removing a test whose behaviour is removed is
stated in the PR body, test by test.

- Delete: `test/host/openingWatcher.test.ts`, `test/host/putStudioInPlace.test.ts`,
  `test/core/navigation/openingPolicy.test.ts`, `test/core/navigation/openingPolicy.holes.test.ts`,
  `test/session/featureIntroductions.test.ts` (only if 4.3's proposal is accepted).
- Rewrite: `test/session/associationMigration.test.ts`,
  `test/core/configuration/editorAssociationMigration.test.ts` (section 5 and 7.2).
- Replace `test/integration/openAtLine.test.ts` (real window) by the real-window test of 7.3. Keep
  it registered: step in `test/integration/trusted-suite.ts` (today `open-at-line`), row in
  `test/shared/e2eGroups.ts` (group `lifecycle-sync`, new "locks" text), count in
  `test/site/e2eGroups.test.ts`.
- Amend `test/host/openAtLine.test.ts`: keep the activation tests (LIFE-001, LIFE-004), the
  setting writer tests, the "Open as Text" tests without "records the file as opened by Studio"
  and without the registry window test; remove the LIFE-176 test (if accepted) and the three
  `StudioLineRequests` tests.
- Amend: `test/core/configuration/settingsRegistry.test.ts` (the `open` category and its two
  settings), `test/security/package-contract.test.ts` (the two properties, the command list),
  `test/security/lifeReq.requirements.test.ts`, `test/session/toolbarReq.requirements.test.ts`
  (fixture `markdownFilesInStudio`, the `showDocumentInStudio` cases), `test/host/fakeVscode.ts`,
  `test/session/memoryPorts.ts`.
- Unchanged and still green: `test/integration/sidePreviewJump.test.ts`,
  `test/host/editorJumps.test.ts`, `test/host/studioSelections.test.ts` (import path only),
  `test/core/navigation/jumpSignal.test.ts`, the line marker tests of the page.
- Every `@tests_req` marker of a removed or moved test follows the requirement changes of 4.7.

### 4.7 Requirements (okfreq)

Rules: `requirements/guidelines/requirements.guidelines.md`, the okfreq baseline it links to,
`requirements/guidelines/project.guidelines.md` ("During a change"), skill `.agents/skills/okfreq`.
Run okfreq as `uv run --no-sync --group requirements okfreq`. Never delete a requirement file,
never hand-edit generated fields or the Links block. A published requirement is deprecated with
`okfreq archive <ID> --path requirements --yes` or replaced with `okfreq supersede <OLD> <NEW>
--yes`; `okfreq retire` is only for a draft that was never published. All IDs below are in
`requirements/tiers/.../lifecycle-sync/`.

| Requirement | Today | Action |
| --- | --- | --- |
| SwRS LIFE-174 (the two settings) | proposed | archive |
| SwRS LIFE-175 (move the association to the setting) | proposed | supersede by a new SwRS "restore the `*.md` association from the retired setting" (`okfreq new ... --lifecycle proposed`, then `okfreq supersede`); it states section 5 and carries the markers of `vscodeHost.ts` (setting writer) and of the migration |
| SwRS LIFE-176 (feature introductions) | proposed | archive, if 4.3's proposal is accepted; otherwise unchanged |
| SwRS LIFE-177 (Open as Text) | proposed | amend: statement, scenario and verification no longer say the text editor is recorded as opened by Studio; add "the text editor stays" (never replaced), with or without the association |
| SwRS LIFE-181 (a requested line reaches the page) | proposed | amend to the side preview only (the scenario "a Studio tab opening for a file at line 42" goes; the verification no longer cites the `StudioLineRequests` tests). If nothing testable is left that LIFE-187..191 do not already state, archive it instead and say so in the PR body |
| SwRS LIFE-182 (links inside Studio open in Studio at the line) | proposed | archive |
| SwRS LIFE-183 (Studio put in place of the text tab) | proposed | archive |
| SwRS LIFE-184 (the opening decision, nine rules) | proposed | archive |
| SwRS LIFE-185 (the opening watcher) | proposed | archive |
| SwRS LIFE-186 (a jump is recognised) | proposed | keep; update the "Implementation" file name (4.1) and any sentence that names the watcher |
| SwRS LIFE-187..191 (side preview marker on a jump) | proposed | keep; reword only sentences that name the watcher |
| SwRS LIFE-178..180, 192..194 (the marker in the page) | proposed | keep; reword only scenarios that start from "a Studio tab opened at a line by the watcher" so they start from the side preview |
| SwRS LIFE-001 (activation events) | proposed | check the sentence about "the editor association migration": it now names the reverse migration; `onLanguage:markdown` stays |
| SwRS LIFE-149 (who writes a setting) | proposed | check: `vscodeHost.ts` is still the one writer |
| SwRS LIFE-156 (settings groups) | proposed | amend: five groups, "Opening Files" removed |
| SwRS CORE-001 (`rendering-core`, touched by `e883dfb6`) | - | check; amend only if it names the watcher or the settings |
| StRS LIFE-023 ("A reader opens a Markdown file at a searched line and sees that line marked in Studio") | proposed | amend, cannot be archived: it is the parent of the kept SwRS (177, 178..180, 186..194). New title and statement about what remains: the reader sees the line of a jump marked in the side preview, and gets the raw text on request. Rationale, user need, the Mermaid use case diagram (it names the opening watcher) and the main paths are rewritten: path 1 (Open as Text) and path 5 (side preview jump) stay; paths 2 (migration and settings), 3 (Studio at the searched line) and 4 (links inside Studio) go or are reduced to the reverse migration. A main path cites only in-force SwRS |
| StRS LIFE-001 | proposed | amend the sentence "its only write outside its own settings is the one-time move of a `*.md` editor association to its setting": the write is now the one-time restore of the `*.md` association and the removal of the retired settings |

Owner re-approval: **none is required by the okfreq rule**. No requirement of `lifecycle-sync` is
`approved` (the bundle has 14 approved requirements, none here); StRS LIFE-023 and StRS LIFE-001
are `proposed`. The owner should still read the new title and statement of StRS LIFE-023 in the
PR, because its subject changes (it loses "opens ... in Studio at a searched line"; that use case
comes back with `studio-at-searched-line`). If the Driver finds a requirement with
`req_lifecycle: approved` that must change, they stop and report it; they do not change it.

After the edits: markers `@implements_req` / `@tests_req` follow the code (an in-force SwRS has a
source marker; at most three IDs per block), `just requirements-lint`, `just requirements-update`,
and one dated entry in `requirements/tiers/log.md`.

### 4.8 Documentation

- `docs/user/open-studio.md`, section "Open at a line": remove the first paragraph and the last
  part (the watcher and the two settings). Keep "With the side preview open" and its table.
  Add how to open every Markdown file in Studio: the `workbench.editorAssociations` entry, or
  "Open With... > Configure default editor for '*.md'...". Say that "Open as Text" and "Open
  With... > Text Editor" always give the text. Say that with the association, a jump opens Studio
  at the top of the file.
- `docs/user/settings.md`: remove the group "Opening Files".
- `docs/known-limitations.md`: remove "the opening watcher" from the sentence that lists it, and
  in "## Opening Files" remove the limits of the watcher (the flash of the text tab, the pinned
  tab, "Open With" replaced, the first file opened as text). Keep the limits of the side preview
  marker, "Jumping to the very same line within one second", the diff-side line, and "Open as Text
  on unsaved changes asks to save". Add: with the native association, a jump opens Studio at the
  top, not at the line. If the heading is renamed, update the link
  `../known-limitations.md#opening-files` in `open-studio.md`.
- `.agents/glossary/common.md`: update "Jump" (it says the opening watcher reads it); remove
  "Feature introduction" if the mechanism goes; remove "opening watcher" if it has an entry.
- `CONTRIBUTING.md` and `skills/writing-for-markdown-okf-schema-studio/`: search for "opening
  watcher", `markdownFilesInStudio`, `searchResultsInStudio`; fix what is found. No rendered
  syntax changes, so the writing skill needs no other update.

### 4.9 CHANGELOG and release notes

- `CHANGELOG.md`, `## Unreleased`: one user-facing line appended at the end of the list, in the
  fix PR, in the format of "CHANGELOG line" of `.agents/guidelines/pull-request.guidelines.md`,
  ending with `(CR-<number> raw-text, PR #<number>)`. It must say the three things a user needs:
  the raw text is never replaced by Studio again; the two settings are gone and VS Code's
  `workbench.editorAssociations` opens every Markdown file in Studio; a user who had
  `open.markdownFilesInStudio` on gets the association back automatically.
- Release notes of 1.12.1: `docs/releases-notes/<date>-v1.12.1/release-notes.md` and `tweet.md`,
  on the pattern of the patch release `docs/releases-notes/2026-11-19-v1.9.3/`. By
  `.agents/guidelines/release-process.guidelines.md` (step 3) they go in the **version PR**, which
  is the release CR. This CR's PR body carries the text they need, ready to copy:
  - what was wrong (since 1.11.0) and what is fixed;
  - the two removed settings and their replacement;
  - the automatic restore, and its one visible effect: the Markdown file that is open when 1.12.1
    activates for the first time stays a text editor; the association applies from the next
    opening;
  - what is lost until the next release: with every Markdown file in Studio, a search result opens
    Studio at the top of the file, not at the line (to return with `studio-at-searched-line`).
  If the Chief of Staff wants the notes file in this PR instead, that is a release-process
  question, not a behaviour one.
- Commit: type `fix`, scope `vscode` (settings and opening are the extension's exposition); see
  `.agents/guidelines/git-commit-message.guidelines.md`.

## 5. The reverse migration

### 5.1 Behaviour

At activation (same place as today in `StudioActivation.start()`, before the commands that
depend on nothing of it), for each scope in the order user, then workspace:

1. Read the scope's own value of `markdownOkfSchemaStudio.open.markdownFilesInStudio` with
   `SettingScopes.inspect("markdownOkfSchemaStudio", "open.markdownFilesInStudio")`. Only the value
   set in that scope counts, never the merged value.
2. If it is `true`: write `workbench.editorAssociations` in that same scope with the entry
   `"*.md": "markdown-okf-schema-studio.editor"` added, **then** remove the setting (write
   `undefined`) in that scope. The association is written first, so a failure in the middle never
   leaves the user with neither.
3. In every case, remove from that scope the leftover values of the two retired settings
   (`open.markdownFilesInStudio` when `false`, `open.searchResultsInStudio` whatever its value),
   so `settings.json` shows no unknown key.

No message, no question, no notice (decision 8: "without a question"). A write that fails is
logged in the extension's output channel and nothing is shown; the setting value is then still
there, so the next activation tries again. This is why no "migrated" mark is needed: the setting
value is the mark, and the migration is idempotent.

Also remove the state keys the old code left: `markdownOkfSchemaStudio.migrations.editorAssociation`
(globalState and workspaceState) and, if the mechanism goes,
`markdownOkfSchemaStudio.introductions.openInStudio`.

Workspace-folder scope is not handled, as in the forward migration (`SettingScopes` has `user` and
`workspace` only).

### 5.2 The pure rewrite (`src/core/configuration/editorAssociationMigration.ts`)

A function that takes the current value of `workbench.editorAssociations` in one scope and returns
the value to write, or "nothing to write":

| Current value in the scope | Result |
| --- | --- |
| absent | `{ "*.md": "markdown-okf-schema-studio.editor" }` |
| object without `*.md` | the same object plus the `*.md` entry; other entries and their order kept |
| object with `*.md` → Studio already | nothing to write (the setting is still removed) |
| object with `*.md` → another editor | nothing to write: the user's own choice wins (the setting is still removed). Not grilled: open question 3 |
| legacy array form `[{ viewType, filenamePattern }]` | the array plus `{ viewType: "markdown-okf-schema-studio.editor", filenamePattern: "*.md" }`, unless a `*.md` item exists (same two rules as above) |
| any other shape (not an object, not an array) | nothing to write, logged; the setting is kept so nothing is lost |

Only the pattern `*.md` is written, the same one the forward migration removed.

### 5.3 Cases

| User scope | Workspace scope | Result |
| --- | --- | --- |
| on | not set | association in user settings; setting removed |
| not set | on | association in workspace settings; setting removed |
| on | on | association in both; both removed |
| on | off | association in user settings; both values removed. In that workspace Markdown now opens in Studio where it did not before: VS Code has no "off" value for an association in a narrower scope. Not grilled: open question 3 |
| off or not set | off or not set | no association written; leftover values removed |
| never had the feature (fresh 1.12.1 install) | | nothing written at all |

## 6. Out of scope

- Opening Studio at the searched line under the native association: the P1 CR
  `studio-at-searched-line` (decision 5). Nothing of it is prepared here beyond leaving the page's
  line marker and `requestRevealLine` in place.
- The release itself: version commit, tag, release notes files, announcement thread. A separate
  release CR (decision 6). This CR ends with a fix PR ready to merge.
- Any new rule in the opening decision (for example "never replace an editor the user chose"): the
  mechanism is removed, not repaired.
- Any change to the side preview marker, to the page's line marker, or to what "Open as Text"
  does, beyond removing the watcher's bookkeeping.
- Rewriting the 1.11.0 and 1.12.0 CHANGELOG sections or release notes.
- A migration for the workspace-folder scope.

## 7. Evidence

The gate is `just preflight` (on Windows: the static stage; CI runs the others). The real-window
tests run in the `integration` job, which a pull request does not run: dispatch it on the branch
with `gh workflow run ci.yml --ref <branch> -f heavy=true` and give the run's link in the PR.

### 7.1 Static checks

1. `just check` green: TypeScript, import boundaries, unused exports (no orphan of the removed
   code is left), settings schema in sync with the registry.
2. A search of `src/`, `test/`, `docs/`, `requirements/` (in-force text), `skills/`, `package.json`
   for `openingWatcher`, `openingDecision`, `putStudioInPlace`, `showDocumentInStudio`,
   `navigatesInStudio`, `StudioLineRequests`, `StudioOpenedTextEditors`, `StudioClosedTabs`,
   `searchResultsInStudio` finds nothing; `markdownFilesInStudio` is found only in the reverse
   migration, its tests, its SwRS, the deprecated requirements and the release history.
3. The manifest tests read the shipped `package.json` of the branch (the file as it ships, not a
   fixture): no property `markdownOkfSchemaStudio.open.*`, no group "Opening Files",
   `onLanguage:markdown` still in `activationEvents`, command `openAsText` still declared with its
   `when` clause.
4. `just requirements-lint` green; `just requirements-update` leaves no diff; no in-force
   requirement cites a deprecated one; the log entry is there.

### 7.2 Unit and host tests (each fails on `main` at `2e2efa6`)

- The pure rewrite: one test per row of the table in 5.2.
- The session migration with memory ports: one test per row of 5.3; the order "association first,
  then the setting"; a failing association write leaves the setting in place and shows nothing; a
  second run writes nothing; no notice is ever shown.
- Host (`fakeVscode`): activating with a Markdown text editor active, with `*.md` associated or
  not, closes no tab and runs no `vscode.openWith`; "Open as Text" opens the text at the line in
  the same column, closes the Studio tab, and expects the selection as `"no-mark"`.
- Session: a link, Back and Next call `showDocument` in every case; the side preview still gets
  `requestJumpMarker`.

### 7.3 Real VS Code window (replaces `test/integration/openAtLine.test.ts`)

Host and default matrix. The change depends on a configured value against the shipped default, so
both columns are run. "Stays" means: still the active tab, a text editor, after a wait longer than
the old watcher's delays (2 s is enough).

| Scenario | `*.md` → Studio configured | Shipped default (no association) |
| --- | --- | --- |
| `vscode.openWith(uri, "default")` on a Markdown file (what "Open With... > Text Editor" runs) | text editor, stays; no Studio tab for that file appears | text editor, stays |
| The same on a file already open in Studio ("Reopen Editor With... > Text Editor") | text editor, stays | n/a |
| `vscode.open` with a selection at line 42 (a jump) | no text tab is closed by the extension; the result is VS Code's (Studio tab) | text editor at line 42, stays |
| "Open as Text" from a Studio tab scrolled to a known line | text editor at that line, same column, stays; the Studio tab is closed | same |
| A jump with the side preview open on the file | text editor at the line; the side preview marks the line (`sidePreviewJump.test.ts`, unchanged, green) | same |
| Reverse migration: `open.markdownFilesInStudio: true` in user settings before activation | after activation, user `settings.json` has the `*.md` entry and no `markdownOkfSchemaStudio.open.*` key; no notification was shown; the next `vscode.open` of a Markdown file gives a Studio tab | - |
| Same, value in workspace settings | the same, in the workspace's `.vscode/settings.json` | - |

Two points the real window must prove, because the fakes cannot:

- `showTextDocument` in "Open as Text" gives a text editor when the association is set (it did in
  1.10 to 1.12; the watcher's registry is no longer there to protect it, so it is asserted).
- `WorkspaceConfiguration.update("open.markdownFilesInStudio", undefined, target)` succeeds on a
  key that `package.json` no longer declares. If VS Code refuses it, stop and report: the fallback
  is open question 3.

Hosts: the real-window scenarios run where the `integration` job runs (Linux). The static and
unit evidence runs on Linux and Windows (`just ci-static` on both).

### 7.4 Manual scenario for the owner (five minutes, on the packaged VSIX)

1. In a profile with 1.12.0 and "Open Markdown files in Studio" on, install the 1.12.1 VSIX and
   open a Markdown file. Expected: no message. In the user `settings.json`: the `*.md` entry is in
   `workbench.editorAssociations`, no `markdownOkfSchemaStudio.open.*` key.
2. Click another Markdown file in the Explorer. Expected: a Studio tab.
3. Right-click a Markdown file > "Open With..." > "Text Editor". Expected: the text, and it stays.
4. In a Studio tab, "Open as Text". Expected: the text at the line that was at the top, and it
   stays.
5. Open the side preview on a file, then jump to a line of it from the Search view. Expected: the
   text at that line, and the side preview marks the line.
6. Settings UI, search "Studio": no group "Opening Files".

## 8. Open questions

Points the answers leave open. The Spec-writer does not decide them; the proposal in the spec is
marked as such.

1. **Links followed inside a Studio tab.** With the native association, a link, Back or Next
   followed inside a Studio tab opens the target in Studio at the top of the file: the target line
   is lost (as in 1.10), until `studio-at-searched-line`. The strict removal (the brief lists
   `studioPlacement.ts` for removal, and `showDocumentInStudio` depends on it) gives this. Confirm,
   or ask to keep "links inside Studio open in Studio at the line" (it needs `putStudioInPlace`
   and `StudioLineRequests` kept, and SwRS LIFE-182 and part of LIFE-181, LIFE-183).
2. **The feature introductions mechanism.** It is dead once the feature goes (`showOnce` is never
   called). Proposal: remove it with the palette command "Show Feature Introductions Again" and
   SwRS LIFE-176. The answers do not name this command. Remove, or keep for a later feature?
3. **Edges of the reverse migration**, not grilled:
   - an existing `*.md` entry for another editor: proposal, leave it and still remove the setting;
   - leftover values (`searchResultsInStudio`, an explicit `false`): proposal, remove them;
   - user on and workspace off: the association cannot be turned off for one workspace; proposal,
     accept it and say it in the release notes;
   - if VS Code refuses to remove a value of a key that is no longer declared: fallback, keep the
     two keys declared in `package.json` for one version with a `deprecationMessage` and no effect.
     To decide only if the real window shows the refusal.
4. **Wording of the release**: the feature shipped in 1.11.0, so "as in 1.11" in the brief means
   "as in 1.10". Confirm the release texts say "since 1.11.0".
5. **Release notes file**: by the release process it belongs to the version PR (release CR), and
   this spec puts only the CHANGELOG line and the ready text in the fix PR. Confirm.
