# Side preview next to a diff: scroll, replace preview, title button

When a VS Code text diff of a `.md` file is the active editor, Studio treats the real file of that
diff as the file to preview. The side preview switches to it by itself, Studio's editor title button
shows on the diff and opens the side preview of the real file, "Open Preview to Side" run from the
search and replace preview opens the real file's preview instead of refusing, and the side preview
and the diff scroll together as they do with a text editor.

Origin: verbal (owner), split off from CR-445 open-at-line-marker (decision 17, diff-view Q2 to Q4).
No tracker issue. Code base: `origin/main` at `5a84db8b` (release 1.11.0). Decisions come from
`02-answers.md`: the owner's answers dg-Q1 to dg-Q5 (final) and the points the Chief of Staff
settled from the spec critic. Facts come from the CR-445 exploration
`4-batch/3-done/445-open-at-line-marker/work/diff-view-findings.md` (VS Code 1.147.0, Windows 11,
at 1.10.0; the code it names is unchanged on these points at 1.11.0).

## 1. Goal, in the user's terms

- I look at the Git changes of `doc.md` (Open Changes, Source Control, Compare with Saved, a
  two-file compare): Studio's "Open Preview to Side" button is in the editor title, as on a text
  editor, and it opens the preview of `doc.md` beside the diff. The diff stays where it is.
- With the side preview open, I bring a diff of another file to the front: the side preview switches
  to that file, as it does for a text editor.
- I preview a search and replace (I clicked a match with a replace text typed): "Open Preview to
  Side" (button, palette or `Ctrl+K Shift+V`) opens the preview of the real `doc.md`, not a refusal.
- I scroll the diff: the preview scrolls with it. I scroll or click the preview: the diff follows,
  under the same settings as a text editor.
- On a staged-changes or timeline diff, the button opens the preview of the file in my working tree.

## 2. Facts at 1.11.0

- **Title button.** `package.json` `menus.editor/title` shows `openPreview` only when
  `resourceExtname == .md && activeEditor == workbench.editors.files.textFileEditor`; the same
  clause is pinned by `test/security/package-contract.test.ts:95`. A diff editor (VS Code's text
  diff editor, id `workbench.editors.textDiffEditor`, also used by the replace preview) does not
  match, so the button is hidden there. The palette entry (`resourceExtname == .md`) and the
  keybinding (`editorTextFocus && resourceExtname == .md`) already work in a diff.
- **Which file the command previews.** `StudioActivation.openPreview`
  (`src/host-vscode/activation.ts`, SwRS-MDOKFSTUDIO-LIFE-003) previews
  `vscode.window.activeTextEditor?.document` (or the Studio Open With tab's document). A document
  without a file path (`isDocumentEligible`, `src/session/sessionDocuments.ts`: `path` defined and
  extension `.md`) gets "Open a Markdown file to use Markdown OKF-Schema Studio."
  - In a git diff with the cursor in the modified side, the active text editor is the working-tree
    file: the preview opens (finding: "works").
  - In the replace preview, the active side is VS Code's virtual "after replacement" document (not a
    `file:` URI): refusal (finding `p2-default-07`). In VS Code, the replace preview's **original
    (left) side is the real file** and its modified (right) side is the virtual document.
  - Not observed but read from the code: with the cursor in a git diff's original side (`git:` URI),
    the command refuses the same way.
- **Menu argument hazard.** When a menu passes a `file:` URI that is not the active text editor's
  document, `openPreview` first opens that file in a **text editor** (in another column when a side
  preview exists). A title button click on a git diff passes the modified side's URI; with the
  cursor in the original side, this path would open a text editor of the file next to the diff. The
  change must not do that (4.2).
- **Following the active editor.** `HostEvents.onActiveEditorChanged` (`src/session/hostEvents.ts`,
  SwRS-MDOKFSTUDIO-LIFE-026) switches the side preview to the active text editor's document when it
  is eligible, and otherwise leaves it as it is. A git diff opened with the cursor in its modified
  side (the working-tree file) therefore already switches it. The replace preview's active side,
  and a `git:` side, are not eligible: the side preview keeps the file it showed (finding: "It stays
  on the real file", `default-05`, `default-06`, where it already showed that file). A diff of
  another file whose active side is not eligible does not switch it today. This CR changes that
  (4.4, decision 6).
- **Scroll, diff to preview.** `vscode.window.onDidChangeTextEditorVisibleRanges` →
  `HostEvents.onVisibleRangesChanged` → `ScrollSyncController.syncEditorToPreview`
  (`src/session/features/scrollSync.ts`, SwRS-MDOKFSTUDIO-LIFE-100) moves every preview whose
  `documentUri` equals the scrolled editor's document id. In the finding (`p3-default-01`, `-02`),
  `Ctrl+End` in a text editor scrolled the preview to 1512 px, while `Ctrl+End` in the git diff's
  modified side left it at 0, although that side's document is the same `file:` URI. **The cause is
  not known** because nobody investigated it. Candidates: VS Code does not report a diff side's
  visible ranges, or reports them differently; the echo guard, or the anchor of the switch that the
  diff's activation triggered; or the `visibleRanges[0]` reading in `pairedEditor`
  (`src/host-vscode/vscodeHost.ts`) when unchanged regions are collapsed. The finding tried only the
  side-by-side layout, never the inline one.
- **Scroll, preview to diff.** `ScrollSyncController.revealEditorLine` (SwRS-MDOKFSTUDIO-LIFE-108)
  picks the visible editor whose `fsPath` equals the preview's active document path. A `git:` side
  or the replace preview's virtual side can share that `fsPath`, so the reveal may land on a side
  that is not the real file. Nobody has observed what it does today.
- The diff tab is already recognised in one place: `tabKindOf` in
  `src/host-vscode/openingWatcher.ts` maps `vscode.TabInputTextDiff` to `"diff"` (CR-445, which
  keeps diffs out of Studio). `TabInputTextDiff` carries `original` and `modified` URIs. The
  multi-file diff and merge editors have no input class in the API (`openingWatcher.ts:47`).

## 3. Decisions carried

| # | Decision | Source | Where |
| --- | --- | --- | --- |
| 1 | The file of a diff is **the real file**: the side preview previews it, never a virtual or `git:` side | dg-Q1, owner | 4.1 |
| 2 | Studio's editor title button shows on a diff editor of a `.md` file and opens the real file's preview | dg-Q1, owner | 4.2 |
| 3 | "Open Preview to Side" from the search and replace preview opens the real file's preview instead of refusing; the replace preview previews the real file (left side) | dg-Q1, owner; Chief of Staff | 4.1, 4.2 |
| 4 | The side preview follows the diff editor's scroll | dg-Q1, owner | 4.3 |
| 5 | A diff with no real file (staged, timeline): the button opens the preview of the working-tree file at that path, no scroll following; refusal only when no such file exists | dg-Q2, owner | 4.1, 4.3 |
| 6 | When a text diff with a real file becomes the active editor, the side preview switches to that real file by itself, for every text diff | dg-Q4, owner | 4.4 |
| 7 | If the diff-to-preview scroll proves impossible because of VS Code, the button and the command ship; the scroll becomes a written known limitation plus a new inbox item | dg-Q5, owner | 4.3, 4.6 |
| 8 | Preview to diff (scroll editor with preview, reveal on click) and the caret-line mark behave as with a text editor, under the existing settings, aimed at the real file's side; today's behaviour observed first | Chief of Staff | 4.3 |
| 9 | Compare of two real `.md` files: the preview shows the side with the cursor, as today; the other side still moves a preview of its own file (LIFE-100) | Chief of Staff | 4.1, 4.3 |
| 10 | Multi-file diff and merge editors out of scope (no input class in the API); a follow-up inbox item | Chief of Staff | 5 |
| 11 | A search click with a replace text that opens the replace preview marks the real file's line in the side preview, when the jump is detectable on a diff side: specified in side-preview-jump-marker, stacked after this CR | dg-Q3, owner | 7 |
| 12 | The diff stays VS Code's text diff (CR-445 decision 11 unchanged) | CR-445 | 5 |
| 13 | Once final and ready, the CR joins the running batch-07 | owner, 2026-11-21 | (planning) |

Reading note on decision 3: dg-Q1 says "the real file (the modified side)". That holds for a git
diff, Compare with Saved and a two-file compare. In the replace preview the modified side is the
virtual document, and the real file is the original side. The principle "the real file" wins, as
the Chief of Staff confirmed. The PR body says so for the owner's review.

## 4. The change

### 4.1 The real file of the active diff

A new host-side reading in `src/host-vscode/`, the layer that reads VS Code tabs. When the active tab
of the active group is a `vscode.TabInputTextDiff`, the **real file** of that diff is the first that
applies:

1. when both sides are eligible files (`file:` scheme, extension `.md`): the **active side**, the one
   holding the cursor (a two-file compare; decision 9). With no active side known, the modified side;
2. when one side only is an eligible file: that side. This is the modified side for a git diff and
   Compare with Saved, and the original side for the replace preview;
3. when no side is a `file:` URI (for example a `git:` against `git:` staged or timeline diff): the
   working-tree file at the modified side's path (`Uri.file(modified.fsPath)`), when that file
   exists and is `.md`. This is a **working-tree stand-in**: its lines may differ from the diff's,
   so no scroll is synced with it (4.3). With no such file: none.

The coder checks in a real window which URIs the staged-changes and timeline diffs use. That they
are `git:` against `git:` is not proven. Rule 3 applies only to sides that are not `file:` URIs.

`openPreview` uses this reading **only when** the command gets no URI (palette, keybinding), or gets
a URI equal to one of the active diff's two sides (the title button). In those cases it previews the
diff's real file, opening it with `vscode.workspace.openTextDocument` and never showing it in a text
editor, whichever side holds the cursor. With no real file it shows today's refusal message. Any
other `file:` URI (the Explorer context menu, a URI of another file) keeps today's path unchanged,
even while a diff is active. Outside a diff nothing changes.

### 4.2 The editor title button on a diff

- `package.json` `menus.editor/title`, the `openPreview` entry: the `when` clause also matches the
  text diff editor, for example
  `resourceExtname == .md && (activeEditor == workbench.editors.files.textFileEditor || activeEditor == workbench.editors.textDiffEditor)`.
  In a diff, `resource` is the modified side's URI. In the replace preview it is the virtual
  document, whose path still ends in `.md`, so the button shows there too. The coder checks the
  exact context keys in a real VS Code window.
- `test/security/package-contract.test.ts`: the pinned clause follows.
- The button passes a URI of one of the diff's sides, so by 4.1 `openPreview` previews the diff's
  real file and **opens no text editor**. The diff stays the active editor of its group, and the side
  preview opens beside it (or is revealed and switched), as it does from a text editor.

### 4.3 Scroll between the diff and the side preview

- **Investigate first.** The coder reproduces the finding in an integration test: side preview open,
  a git diff or Compare with Saved of the same long file, scroll the real file's side to the end,
  read the page's scroll. Do it in both diff layouts, **side by side and inline**
  (`diffEditor.renderSideBySide: false`), and find the cause (section 2). Before changing anything,
  also observe and record what today's preview-to-diff reveal does (LIFE-108).
- **Diff to preview** (decision 4). When a diff side showing a real file (rule 1 or 2 of 4.1)
  scrolls, every preview of that file follows the first visible line of that side, under the same
  rules as LIFE-100: the anchor is owned by the editor, the line sits at the reading line, nothing
  echoes back, and the anchor mode is respected. In both layouts the two sides of a VS Code diff
  scroll together, so in the replace preview (real file on the left) scrolling moves the preview. In
  a two-file compare each `.md` side still moves the previews of its own file. A side that is not a
  `file:` document (`git:`, the virtual replace document) never moves a preview. The working-tree
  stand-in of rule 3 never syncs a scroll in either direction.
- **Preview to diff** (decision 8). Scroll editor with preview, the reveal on a block click, and the
  editor caret-line mark behave as with a text editor, under the existing settings. The reveal
  (`revealEditorLine`, today matched on `fsPath`) and the caret mark target **the real file's side
  only**, never a `git:` or virtual side that shares the path.
- **If the diff-to-preview scroll proves impossible** because of VS Code (decision 7), for example
  because VS Code reports no visible ranges for diff sides: the button, the command and the
  following of 4.4 ship anyway. The coder records the evidence (the API gap, the trial) in the PR.
  The limitation is written in the docs (4.6), and the coder files a new inbox item for the scroll.
  The preview-to-diff direction ships if it works on its own.
- The preview shows the real file's current text (not the "after replacement" text), as today.

### 4.4 The side preview follows a diff

When a text diff becomes the active editor, and it has a real file by rule 1 or 2 of 4.1, the side
preview that follows the active editor switches to that real file (decision 6). This covers every
text diff, including the replace preview and a diff whose cursor sits in a `git:` side. It uses the
same switch and the same "Preview pending / Following the active Markdown editor." state as LIFE-026.
A diff with only a working-tree stand-in (rule 3) does not switch the side preview by itself,
because dg-Q2 covers only the button. A focus move between the two sides of the same diff switches
nothing. In a two-file compare, moving the cursor from one side to the other switches to that side's
file, as today. The trigger is the active tab change (`tabGroups.onDidChangeTabs`) as well as
`onDidChangeActiveTextEditor`, since the active text editor of a diff may be a non-eligible side.

### 4.5 Requirements (okfreq)

Per `requirements/guidelines/project.guidelines.md` ("During a change"), scope `lifecycle-sync`:

- SwRS-MDOKFSTUDIO-LIFE-003 (Open Preview to Side): the command's source also covers the active text
  diff's real file (4.1) when the command gets no URI or a URI of one of its sides. The button is
  offered on a diff of a `.md` file, no text editor opens from a diff, and the working-tree stand-in
  applies with refusal only when that file is missing.
- SwRS-MDOKFSTUDIO-LIFE-026 (follow the active editor): **changes**. A text diff with a real file
  that becomes active switches the side preview to its real file (4.4).
- SwRS-MDOKFSTUDIO-LIFE-100 (scroll editor to preview): extended to the real file's side of a diff
  editor, in both layouts, never for a non-`file:` side or the working-tree stand-in. Or a new SwRS
  deriving from StRS-MDOKFSTUDIO-LIFE-010, if the requirements guideline prefers.
- SwRS-MDOKFSTUDIO-LIFE-108 (preview reveals the source line): the reveal targets the real file's
  side of a diff, never a side that only shares its path.
- Markers move with the code. Then `just requirements-update`, and a dated entry in
  `requirements/tiers/log.md`.

### 4.6 Docs and changelog

- `docs/known-limitations.md:25` ("live comparison against another document or native
  source/version diff editor integration"): say that the side preview works next to VS Code's text
  diffs (button, command, following, scroll), while there is still no rendered diff. If the scroll
  ships as a limitation (decision 7), it is written here.
- `docs/user/open-studio.md:19` (book icon / Open Preview to Side): the button also shows on a text
  diff of a Markdown file and previews the real file (working tree, or the original file of the
  replace preview).
- `docs/user/open-studio.md:43` ("A diff stays a text diff."): add that the side preview follows a
  diff of its file.
- `CHANGELOG.md`, `## Unreleased`: one line in the user's terms (button on diffs, Open Preview to
  Side from the replace preview, the side preview following and scrolling with a diff).
- No rendered syntax changes, so the writing skill stays as it is. Glossary: add "diff editor" and
  "real file (of a diff)" to `.agents/glossary/common.md` if they are missing.

## 5. Out of scope

- Studio inside a diff, a rendered diff (CR-445 decision 11: diffs stay VS Code's text diffs).
- The multi-file diff editor ("Open All Changes", Source Control's multi-diff) and the merge editor:
  they have no input class in the API (decision 10). **Follow-up**: an inbox item for them, filed by
  the Chief of Staff or the coder.
- The GitHub Pull Requests extension's diffs: nobody explored them. They are covered only if they
  are text diffs with a `file:` side.
- Git's own behaviour from a Studio editor ("Git: Open Changes" does nothing there): that is VS
  Code's Git, not Studio.
- The target-line marker on a jump into a diff: side-preview-jump-marker (section 7).

## 6. Tests and acceptance

- **Unit / host tests** (`test/host/`):
  - the real-file choice of 4.1: git diff gives the modified side; replace preview gives the original
    side; two `.md` files give the active side; `git:` against `git:` gives the working-tree file
    when it exists and none when it does not;
  - `openPreview` from a diff, with no URI or a URI of one of its sides, opens no text editor and
    previews the real file whichever side is active;
  - `openPreview` with a `file:` URI of **another** file while a diff is active keeps today's path
    (it opens that file in a text editor, then previews it);
  - the diff activation switch of 4.4, and no switch for a working-tree stand-in;
  - the reveal of LIFE-108 aimed at the real file's side, not at a `git:` side with the same
    `fsPath`.
- **Package contract**: the new `editor/title` clause.
- **Integration** (real VS Code, `test/integration/`, lifecycle and scroll-sync suites):
  - T1: git diff (or Compare with Saved) of a long `.md`, side preview open, scroll the real file's
    side to the end: the preview scrolls (today 0 px). Run it in the side-by-side **and** inline
    layouts.
  - T2: replace preview of a `.md` match, run "Open Preview to Side" from the palette and with
    `Ctrl+K Shift+V`: the side preview shows the real file, with no information message. Scroll the
    replace preview: the preview follows. Run it in both layouts.
  - T3: cursor in a git diff's original side, run the command: the preview of the working-tree file,
    with no text editor tab added.
  - T4: the title button is visible on a diff editor of a `.md` file, and hidden on a diff of a
    non-`.md` file (checked through the menu contribution if the real menu cannot be read).
  - T5: side preview on `a.md`, bring a diff of `b.md` to the front (the replace preview, or a git
    diff with the cursor in its `git:` side): the side preview switches to `b.md`.
  - T6: a staged-changes diff: the command previews the working-tree file, and scrolling the diff
    does not move the preview.
- **Real-window evidence** (screenshots for the PR body, `pull-request.guidelines.md`): the title
  button on a git diff and on the replace preview; `Ctrl+K Shift+V` on the replace preview opening
  the real file's preview; the side preview following a scrolled diff.
- Acceptance: the behaviours of section 1 in a real VS Code window; CR-445's diff tests still pass
  (no diff is pulled into Studio); `just preflight` passes. If decision 7 applies, the scroll
  limitation is written and its inbox item filed.

## 7. Overlap with CR side-preview-jump-marker

The sibling CR (the side preview shows CR-445's target-line marker when a jump opens its file at a
line) touches the same code:

- `src/session/features/scrollSync.ts` (`syncEditorToPreview`, `revealEditorLine`,
  `requestRevealLine`, `postPendingRevealLine`): the jump marker posts a reveal line to the side
  preview, while this CR changes which editor scrolls it and which side a reveal targets;
- `src/session/hostEvents.ts` (`onActiveEditorChanged`, `onVisibleRangesChanged`) and the side
  preview's following of the active editor (4.4);
- `src/host-vscode/openingWatcher.ts` (jump detection, `tabKindOf` "diff");
- SwRS-MDOKFSTUDIO-LIFE-026, LIFE-100, LIFE-108 and the scroll-sync integration suite.

The jump-marker CR **stacks after this CR** (`stacked-prs.guidelines.md`). Owner dg-Q3 says that a
search click with a replace text, which opens the replace preview, marks the real file's line in the
side preview when the jump is detectable on a diff side. That needs this CR's real-file reading
(4.1). The marker is specified in side-preview-jump-marker, not here. This CR exposes the real-file
reading so that the jump-marker CR can reuse it.

## 8. Open questions for the owner

None. The owner (dg-Q1 to dg-Q5) and the Chief of Staff closed every question of the first version.
