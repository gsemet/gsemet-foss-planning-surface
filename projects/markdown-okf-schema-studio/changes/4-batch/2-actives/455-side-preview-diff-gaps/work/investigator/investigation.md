# Investigation CR-455: side preview next to a diff

Base `a106fa7b` (worktree batch-07-CR-455). Read only; nothing was run (no dependencies installed, and
real-window suites do not run on this Windows machine, see the evidence plan). Line numbers are of
this base.

## 1. Files and entry points

### 4.1 / 4.2 Real file, command, title button

- `src/host-vscode/activation.ts`
  - `openPreview(uri?)` (l.317-383). Two blocks: (a) l.320-338, a `file:` URI that is not
    `activeTextEditor.document.uri` is opened with `openTextDocument` + `showTextDocument` (the "menu
    argument hazard"); (b) l.339-347, the previewed doc is `activeTextEditor?.document ?? openStudioTabDocument()`,
    refused (`"Open a Markdown file to use Markdown OKF-Schema Studio."`) when `document.path` is undefined
    or not `.md`. `documents.of(...).path` is `uri.fsPath` only for the `file:` scheme
    (`src/host-vscode/documents.ts:30`), so a `git:` or virtual side has `path === undefined`: that is the
    refusal.
  - The seam for the change: before block (a), compute `diffRealFile()` (new, 4.1). When `uri` is
    undefined or equals `toString()` of one of the active diff's two sides, skip block (a) and use
    `await vscode.workspace.openTextDocument(realUri)` as `textDocument` in (b). Any other `file:` URI keeps
    block (a). `openStudioTabDocument` (l.305) is the model: it also reads `tabGroups.activeTabGroup.activeTab.input`.
  - Listener wiring (l.183-189): `onDidChangeActiveTextEditor` -> `manager.events.onActiveEditorChanged(host.editorOf(editor))`;
    `onDidChangeTextEditorVisibleRanges` -> `onVisibleRangesChanged(host.editorOf(event.textEditor))`.
    4.4 needs a new `vscode.window.tabGroups.onDidChangeTabs` listener here (not yet used in this file;
    `openingWatcher.ts:201` already subscribes to it for its own purpose, leave that alone).
- New file in `src/host-vscode/` (suggest `diffRealFile.ts`), pure over `vscode.TabInputTextDiff`
  (`original`, `modified`) with an injected "active side" (the `activeTextEditor` document URI) and
  a file-exists test (`vscode.workspace.fs.stat` or `fs.existsSync`; `openTextDocument` of a missing file throws).
  Rules 1, 2, 3 of the spec map to a small function returning `{ uri, kind: "file" | "stand-in" } | undefined`.
  Eligible side = `scheme === "file"` and `.md` (same test as `isEligibleUri`, `openingWatcher.ts:56`:
  reuse or extract it, do not copy a third time).
  The active tab: `vscode.window.tabGroups.activeTabGroup.activeTab?.input instanceof vscode.TabInputTextDiff`.
- `package.json` l.186-191, `menus["editor/title"][0].when`; mirrored by
  `test/security/package-contract.test.ts:95`. Both change in lockstep.
  `workbench.editors.textDiffEditor` is the VS Code id; confirm the `resource` key in a real window
  (in the replace preview `resource` is the virtual doc).

### 4.4 Following

- `src/session/hostEvents.ts` `onActiveEditorChanged(editor)` (l.445-457): returns when there is no
  editor or its document is not eligible. It takes a `PairedEditor`. The session layer must not import
  `vscode` (layers `core, host-api, page, node-services, session, ..., host-vscode`; import-boundary
  check in `just check`), so the real-file reading must reach it as a `HostDocument` or through a
  host-api port. Smallest: the activation computes the real file of the active diff (4.1 rules 1-2 only,
  no stand-in) and calls `manager.events.onActiveEditorChanged` with a `PairedEditor`/document of that file,
  or a new `onActiveDiffChanged(document: HostDocument | undefined)` that calls the same
  `switchAfterFlush(session, document)`. A `PairedEditor` needs `fsPath`, `firstVisibleLine`,
  `selectionLine`, `revealLine`: for a document-only switch a method taking `HostDocument` is cleaner.
- `src/session/previewManager.ts` `switchAfterFlush` (-> l.612-626, the "Following the active Markdown
  editor." pending state, LIFE-026 marker at l.621) is unchanged.
- No-op rule needed: "a focus move between the two sides of the same diff switches nothing". The
  switch already no-ops when `document.id === session.documentUri`? Not verified: read `switchAfterFlush`
  head (above l.612) and add a same-document guard if it re-renders.
- Trigger set: `onDidChangeActiveTextEditor` (existing) plus `tabGroups.onDidChangeTabs` filtered to
  `changed`/`opened` tabs whose `isActive` and whose input is a `TabInputTextDiff`. Beware double fire
  (both events for one diff opening): the same-document no-op is what makes this safe.

### 4.3 Scroll

- Diff to preview: `host-vscode/vscodeHost.ts` `pairedEditor` (l.325-349): `firstVisibleLine`
  = `editor.visibleRanges[0]?.start.line`; `isLineVisible` = `visibleRanges[0].contains(...)`. Then
  `hostEvents.onVisibleRangesChanged(editor)` (l.468) -> `scrollSync.syncEditorToPreview(editor)`
  (`src/session/features/scrollSync.ts` l.135-180). That function matches
  `preview.documentUri === sourceEditor.document.id`, so a `file:` modified side already matches; a
  `git:` side has a different id and never matches (the "never a non-file side" rule is already true
  for diff-to-preview, nothing to add there). The working-tree stand-in is never an editor, so it never syncs.
- Preview to diff: `scrollSync.revealEditorLine` (l.103-130) picks `host.editors.visible().find(fsPath ===
  stage.activeDocumentPath)`. `PairedEditor.fsPath` doc says it is deliberately the fsPath "also for an
  editor of another scheme (a diff editor)". So a `git:` original side and the replace virtual side
  qualify, and `find` returns the first in `visibleTextEditors` order. Fix: require
  `candidate.document.id === preview.documentUri` (the `file:` URI string) in addition, or expose a
  `scheme`/`isFile` on `PairedEditor` (`src/host-api/textEditors.ts`), then adapt
  `test/host/fakeVscode.ts` `editorFor` and any other `PairedEditor` implementer (grep `PairedEditor`).
  The caret mark (`markEditorSelectionInPreview`, l.283) uses `visibleEditorFor` (match on `document.id`),
  already file-only; `syncEditorToPreview` posts `selectionLine` from the same editor.
  Note `visibleEditorFor` / `notifyPairing` also decide the page's anchor button "paired" state.

## 2. Candidate causes of the diff-side scroll gap (code alone, to confirm in a real window)

Finding: `Ctrl+End` in a text editor moves the page, in the diff's modified side it leaves it at 0, same
`file:` URI. Ranked:

1. **VS Code reports no `onDidChangeTextEditorVisibleRanges` for a diff side, or reports a stale value.**
   Nothing in the host code distinguishes a diff side; the whole path is `event.textEditor`-driven. First
   check: log in `activation.ts` l.188 listener (editor `viewColumn`, `document.uri.scheme`,
   `visibleRanges`) and see whether the event fires at all on Ctrl+End in the diff. If it does not fire,
   decision 7 applies (limitation) unless a polling/other signal exists (none found in the API).
2. **`visibleRanges[0]` with collapsed unchanged regions.** A diff hides unchanged regions by default
   (`diffEditor.hideUnchangedRegions`); the modified editor then has several disjoint ranges. A long
   file with one change and `Ctrl+End` -> `visibleRanges` may be the changed hunk plus the tail, so
   `[0].start.line` stays at the first hunk (line near 0) while the end is a later range. This would give
   "0 px" exactly as in the finding and is cheap to test: assert on the last range, or compare with
   `hideUnchangedRegions` false. Fix candidate: use the range the user is reading (last range that
   intersects the viewport, or the first range after an event that moved it); needs a decision rule and
   a `PairedEditor` change (`firstVisibleLine` is documented "the zero-based first visible line").
3. **Echo guard and anchor owner after the diff's activation.** The activation of the diff triggers the
   switch (or an `openPreview` render) that sets `scroll.anchor`/`lastRevealedSourceLine` and may
   `echoGuard.expect(...)` (via `revealEditorLine` from a `previewReveal` the page sends on render);
   `isEcho` swallows an event whose top is within `[from-1, to+1]` for 500 ms, and
   `revealedLineIsVisible` uses `isLineVisible` -> `visibleRanges[0]`, which in a diff with collapsed regions
   may contain a stale `lastRevealedSourceLine`, wrongly eating events. Less likely with a human-paced
   `Ctrl+End`, and `ownEditUntil` (l.151) is the same family. Check by logging `isEcho` inputs.
4. **Layout-specific:** the finding tried side-by-side only; in inline mode the original side may be
   hosted differently (T1 runs both layouts), and the second candidate differs per layout.
5. **Page side:** `followSourceScroll` (`src/page/features/scrollCore.ts` l.518) ignores the message when
   `scrollPreviewWithEditor` is off; `applyPairing(message.pairedTextEditor !== false)`
   (`anchorMode.ts:88`) could disable the anchor if `visibleEditorFor` (match on `document.id`) found no
   editor. A diff modified side has the same id, so pairing should be true; assert it in T1.

## 3. Smallest change

1. `diffRealFile.ts` (host-vscode) + tests; 2. `openPreview` seam (use real file for no-URI/side-URI);
3. `package.json` + contract test; 4. activation listener for `onDidChangeTabs` + a document-based
   follow entry in `hostEvents` (`onActiveEditorChanged` unchanged for non-diff); 5. `revealEditorLine`
   restricted to the editor whose `document.id` is the preview's `documentUri`; 6. the scroll fix per the
   cause found (or the limitation path); 7. SwRS LIFE-003/026/100/108 text + markers moving with code,
   `requirements-update`, log entry; 8. docs (`docs/known-limitations.md:25`, `docs/user/open-studio.md:19,43`),
   `CHANGELOG.md`, glossary ("diff editor", "real file (of a diff)").

## 4. Tests a Coder edits or adds

- `test/host/lifeReq.requirements.test.ts` (LIFE-003 at l.257/275/306, LIFE-026 at l.365/983, LIFE-100 at l.748):
  add the 4.1 table, openPreview from a diff (no text editor opened: assert `fake.controls.shownTextOptions`
  unchanged and no new `studioTabs`), other-file URI keeps today's path, 4.4 switch, no stand-in switch,
  LIFE-108 reveal aimed at the `file:` side.
- `test/host/fakeVscode.ts` needs work: `tabGroups.activeTabGroup.activeTab` only ever returns the
  custom tab (l.456-464); `TabInputTextDiff(uri, uri)` at l.444 uses the same URI for both sides;
  `editorFor` has no scheme/uri control and `openTab` makes no editor for `kind: "diff"` (l.731). Needs
  a `controls.activateDiffTab({ original, modified, activeSide })` that sets the active tab input, the
  visible editors (one per side, with the chosen `document.uri`s, `git:`/virtual allowed: `FakeTextDocument`
  built from a `Uri` of another scheme; `documents.of(...).path` is then undefined as in VS Code), the
  `activeTextEditor`, and fires `changeTabs`/`changeActiveEditor`. Also `Uri.from({scheme:"git",...})`
  support, check the fake `Uri`.
- `test/host/openingWatcher.test.ts` (diff tab case at l.95) must stay green (CR-445).
- `test/security/package-contract.test.ts:95`.
- Integration: `test/integration/lifecycle.test.ts` (already uses `COMMAND_ID`, `getActivePreviewForTests`,
  `waitFor`) for T3/T4/T5/T6 (non-visual); new `test/integration/diffPreview.test.ts` registered in
  `trusted-suite.ts` (like `openAtLine.test.ts`, imported l.52) and in `test/shared/e2eGroups.ts` (group
  `lifecycle-sync`, the file list is checked) for T1/T2 with real scroll; screenshots via
  `scroll-sync-suite.ts` style (needs `test/shared/captureRegistry.ts` entries, unknown ids throw, and a
  complete suite fails if a registered capture is not taken).
- Requirement files: `requirements/tiers/swrs/lifecycle-sync/SwRS-MDOKFSTUDIO-LIFE-{003,026,100,108}.md`,
  StRS-LIFE-010 if a new SwRS is chosen, `requirements/tiers/log.md`.

## 5. Risks and measured values

- No size or measured value changes (no layout numbers), so no derived-value search applies.
- `PairedEditor.fsPath` doc/behaviour is relied on elsewhere (grep `fsPath` users of `PairedEditor`)
  before narrowing `revealEditorLine`; the LIFE-108 integration (`sourceMapping.test.ts:96,106`) must pass.
- `openPreview` with `uri` = a side of the diff while the tab is a diff: today the modified-side URI
  equals the `activeTextEditor` only when the cursor is in the modified side; the new equality test must
  use the diff tab's `modified`/`original`, not `activeTextEditor`.
- `onDidChangeTabs` + `onDidChangeActiveTextEditor` double fire -> double `switchAfterFlush`; guard on
  same document.
- Replace preview / `git:` sides: `host.editorOf(editor)` for a virtual side builds a `PairedEditor` whose
  document has `path === undefined`; fine, `isDocumentEligible` rejects it (that is why 4.4 needs the tab
  reading).
- Multiple matching tab groups: the diff of the active group only (spec); a side preview in the same group
  as the diff is not possible (the preview locks its group, `manager.lockNewGroup`).
- `Uri.file(modified.fsPath)` for the stand-in: `modified.fsPath` of a `git:` URI is the repo-relative-looking
  absolute path as VS Code gives it; verify in a real window (timeline URIs use `git:`/`file:` with query).
- `hideUnchangedRegions` default and diff layouts depend on VS Code 1.147 behaviour.

## 6. Questions only the user can answer

None found. (The spec's decision 7 already covers a VS Code limit on the scroll.)

## 7. Evidence plan

Kind: user-visible UI and behaviour change in a real VS Code window, plus code/logic tests.

- **Automated, before/after:** integration T1-T6 above (real VS Code, `@vscode/test-electron`), each
  asserting through `getActivePreviewForTests()` (`phase`, `documentUri`, `lastSourceScrollLine`,
  `scrollTop`, `html`) and `vscode.window.tabGroups` (no `TabInputText` added in T3), plus
  `sendPreviewMessageForTests`/`syncActiveEditorForTests` from `extensionApi.ts`. Helpers available:
  `waitFor`, `createFixture`, `closeAllEditors`, `connectWorkbench`, `findCurrentFrame`
  (`test/integration/realInput/harness.ts`); the `previewFrame`/`scrollPane` pattern in
  `scroll-sync-suite.ts` (page scroll via `frame.evaluate(() => window.scrollY)`, source scroll via
  `visibleRanges`, wheel via `page.mouse.wheel` on the Monaco). Diffs are opened with
  `vscode.diff` (as `stockCoexistence.test.ts:136`) and `vscode.commands.executeCommand("workbench.action.compareEditor...")`;
  the replace preview and the git diff (needs `git` in the fixture dir: `git init` + commit + edit, then
  `git.openChange` or `vscode.diff` with a `git:` URI via `git.api`) have no existing helper and must be
  written. Scroll in a diff: `revealRange` on the side editor is not a user scroll; use
  `workbench.action.compareEditor.*` or `page.mouse.wheel` / `cursorBottom` on the focused diff side;
  layouts via `vscode.workspace.getConfiguration("diffEditor").update("renderSideBySide", false)`.
  T4 cannot read the real title menu: assert the `package.json` contribution (`vscode.extensions.getExtension(...).packageJSON`)
  like `stockCoexistence.test.ts:59`, and a real-window screenshot for the visible button.
- **First step for the cause (4.3):** a throwaway test or a temporary log at `activation.ts:188` printing
  `{event fired, scheme, viewColumn, visibleRanges}` while a diff is scrolled in both layouts and with
  `diffEditor.hideUnchangedRegions.enabled` true/false; this separates candidates 1/2/3. Record it in
  the CR `evidence/` as a `.log`.
- **Screenshots for the PR** (title button on a git diff and on the replace preview; `Ctrl+K Shift+V` on the
  replace preview; side preview following a scrolled diff): produced by the real-window suites with
  `RealWindowEvidence.shoot` (`test/integration/evidence.ts`, `page.screenshot` over CDP, viewport set by
  `setViewport(page, {1440, 900})`), entries registered in `test/shared/captureRegistry.ts`, files under
  `E2E_SCREENSHOT_ROOT`. Before/after: take the same capture on `origin/main` (button absent, preview
  at 0 px, refusal message) and on the branch.
- **Cannot be shown here:** this is a Windows machine and the real-window stages (`ci-integration`, e2e,
  `just e2e`) run on Linux and macOS only (AGENTS.md, CONTRIBUTING.md "Windows"; `run-tests.ts`
  defaults `localCodePath` to the macOS app, `STUDIO_VSCODE_EXECUTABLE` can override). So the real-window
  screenshots and T1-T6 run on CI (`gh workflow run ci.yml --ref <branch> -f heavy=true`, artifacts) or on
  a Mac; locally only `just check` (static, host and package-contract tests) runs. The title button visibility on
  VS Code's own menu cannot be asserted through the API; only a screenshot shows it. Whether VS Code
  reports diff-side visible ranges is only observable in a real window.
