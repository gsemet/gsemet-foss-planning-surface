# Side preview next to a diff: scroll, replace preview, title button

When a VS Code diff of a `.md` file is the active editor, Studio treats the real file of that diff
as the file to preview: its editor title button shows on the diff and opens the side preview of the
real file, "Open Preview to Side" run from the search and replace preview opens the real file's
preview instead of refusing, and the side preview follows the scroll of the diff.

Origin: verbal (owner), split off from CR-445 open-at-line-marker (decision 17, diff-view Q2 to Q4).
No tracker issue. Code base: `origin/main` at `5a84db8b` (release 1.11.0). Decisions come from
`02-answers.md` (dg-Q1, owner's answer "Le vrai fichier", final). Facts come from the CR-445
exploration `4-batch/3-done/445-open-at-line-marker/work/diff-view-findings.md` (VS Code 1.147.0,
Windows 11, at 1.10.0; the code it names is unchanged on these points at 1.11.0).

## 1. Goal, in the user's terms

- I look at the Git changes of `doc.md` (Open Changes, Source Control, Compare with Saved, a
  two-file compare): Studio's "Open Preview to Side" button is in the editor title, as on a text
  editor, and it opens the preview of `doc.md` beside the diff. The diff stays where it is.
- I preview a search and replace (I clicked a match with a replace text typed): "Open Preview to
  Side" (button, palette or `Ctrl+K Shift+V`) opens the preview of the real `doc.md`, not a refusal.
- With the side preview open, I scroll the diff: the preview scrolls with it, as it does for a text
  editor of the same file.

## 2. Facts at 1.11.0

- **Title button.** `package.json` `menus.editor/title` shows `openPreview` only when
  `resourceExtname == .md && activeEditor == workbench.editors.files.textFileEditor`; the same
  clause is pinned by `test/security/package-contract.test.ts:95`. A diff editor (VS Code's text
  diff editor, id `workbench.editors.textDiffEditor`, also used by the replace preview) does not
  match, so the button is hidden there. The palette entry (`resourceExtname == .md`) and the
  keybinding (`editorTextFocus && resourceExtname == .md`) already work in a diff.
- **Which file the command previews.** `StudioActivation.openPreview`
  (`src/host-vscode/activation.ts`, SwRS-MDOKFSTUDIO-LIFE-003, CORE-043) previews
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
  SwRS-MDOKFSTUDIO-LIFE-026) switches the side preview only to an eligible document; a `git:` side
  or the virtual replace document is not eligible, so the side preview keeps the real file (finding:
  "It stays on the real file", `default-05`, `default-06`). This stays as is.
- **Scroll.** `vscode.window.onDidChangeTextEditorVisibleRanges` →
  `HostEvents.onVisibleRangesChanged` → `ScrollSyncController.syncEditorToPreview`
  (`src/session/features/scrollSync.ts`, SwRS-MDOKFSTUDIO-LIFE-100) moves every preview whose
  `documentUri` equals the scrolled editor's document id. In the finding (`p3-default-01`, `-02`),
  `Ctrl+End` in a text editor scrolled the preview to 1512 px, `Ctrl+End` in the git diff's modified
  side left it at 0, although that side's document is the same `file:` URI. **The cause is not
  known**: it was not investigated (candidates: VS Code does not report the visible ranges of a diff
  side, or reports them differently; the echo guard or the anchor of the switch that the diff's
  activation triggered; the `visibleRanges[0]` reading in `pairedEditor`,
  `src/host-vscode/vscodeHost.ts`, with collapsed unchanged regions). The coder finds it first (4.3).
- The diff tab is already recognised in one place: `tabKindOf` in
  `src/host-vscode/openingWatcher.ts` maps `vscode.TabInputTextDiff` to `"diff"` (CR-445, which
  keeps diffs out of Studio). `TabInputTextDiff` carries `original` and `modified` URIs.

## 3. Decisions carried

| # | Decision | Source | Where |
| --- | --- | --- | --- |
| 1 | The file of a diff is **the real file**: the side preview previews it, never a virtual or `git:` side | dg-Q1, owner | 4.1 |
| 2 | Studio's editor title button shows on a diff editor of a `.md` file and opens the real file's preview (the modified side) | dg-Q1, owner | 4.2 |
| 3 | "Open Preview to Side" from the search and replace preview opens the real file's preview instead of refusing | dg-Q1, owner | 4.1, 4.2 |
| 4 | The side preview follows the diff editor's scroll | dg-Q1, owner | 4.3 |
| 5 | The diff stays VS Code's text diff (CR-445 decision 11 unchanged) | CR-445 | 5 |
| 6 | Once final and ready, the CR joins the running batch-07 | owner, 2026-11-21 | (planning) |

Reading of decision 2 for the replace preview: the owner wrote "the real file (the modified side)",
and also that the replace preview opens "the real file's preview". In a git diff, Compare with
Saved and a two-file compare, the modified side is the real file. In the replace preview the
modified side is the virtual document and the real file is the original side. This spec follows the
principle "the real file" (decision 1), so in the replace preview it takes the original side. The
PR body says so for the owner's review.

## 4. The change

### 4.1 The real file of the active diff

A new host-side reading, in `src/host-vscode/` (the layer that reads VS Code tabs): when the active
tab of the active group is a `vscode.TabInputTextDiff`, the **real file** of that diff is:

1. its modified side, when that URI is an eligible file (`file:` scheme, extension `.md`);
2. otherwise its original side, when that URI is an eligible file (the replace preview);
3. otherwise none (both sides virtual, for example `git:` against `git:`; see open question Q2).

`openPreview` uses it: when the active tab is a text diff, the document to preview is the diff's
real file (opened with `vscode.workspace.openTextDocument`, never shown in a text editor), whatever
side holds the cursor. When the diff has no real file, the command behaves as today (the active text
editor's document, else the refusal message). Outside a diff nothing changes.

### 4.2 The editor title button on a diff

- `package.json` `menus.editor/title`, the `openPreview` entry: the `when` clause also matches the
  text diff editor, for example
  `resourceExtname == .md && (activeEditor == workbench.editors.files.textFileEditor || activeEditor == workbench.editors.textDiffEditor)`.
  `resource` in a diff is the modified side's URI; in the replace preview it is the virtual
  document, whose path still ends in `.md`, so the button shows there too. The exact context keys
  are checked in a real VS Code window by the coder.
- `test/security/package-contract.test.ts`: the pinned clause follows.
- The URI the button passes is not used to open a text editor when a text diff is the active tab:
  `openPreview` previews the diff's real file (4.1) and **opens no text editor**; the diff stays the
  active editor of its group and the side preview opens (or is revealed and switched) beside it, as
  from a text editor.
- The button stays hidden on the multi-file diff editor and the merge editor until Q3 is answered.

### 4.3 Scroll from a diff

- The coder first reproduces the finding in an integration test (side preview open, a git diff or
  Compare with Saved of the same long file, scroll its modified side to the end, read the page's
  scroll) and finds the cause (section 2, Scroll).
- Required behaviour: when a diff editor whose real file (4.1) is the side preview's document
  scrolls, the side preview follows the first visible line of the **real file's side**, with the
  same rules as LIFE-100 (anchor owned by the editor, reading line, no echo back, the anchor mode
  respected). The two sides of a VS Code diff scroll together, so in the replace preview (real file
  on the left) scrolling either side moves the preview.
- A side that is not the real file (a `git:` or virtual document) never moves a preview by itself.
- The preview shows the real file's current text (not the "after replacement" text), as today.

### 4.4 Requirements (okfreq)

Per `requirements/guidelines/project.guidelines.md` ("During a change"), scope `lifecycle-sync`:

- SwRS-MDOKFSTUDIO-LIFE-003 (Open Preview to Side): the source of the command also covers the
  active text diff (its real file, 4.1), the button offered on a diff of a `.md` file, and no text
  editor opened from a diff.
- SwRS-MDOKFSTUDIO-LIFE-100 (scroll editor to preview): extended to the real file's side of a diff
  editor, or a new SwRS deriving from StRS-MDOKFSTUDIO-LIFE-010, as the requirements guideline
  prefers.
- SwRS-MDOKFSTUDIO-LIFE-026 (follow the active editor): checked, probably unchanged (a diff side
  that is not the real file leaves the preview unchanged); if the coder makes the diff's activation
  switch the side preview to its real file, the SwRS says so.
- Markers move with the code; `just requirements-update` and a dated entry in
  `requirements/tiers/log.md`.

### 4.5 Docs

The user documentation that describes the side preview, its title button or the scroll sync
mentions diff editors (a line, not a section). No rendered syntax changes: the writing skill is not
touched. Glossary: add "diff editor" and "real file (of a diff)" to `.agents/glossary/common.md` if
absent.

## 5. Out of scope

- Studio inside a diff, a rendered diff (CR-445 decision 11: diffs stay VS Code's text diffs).
- The multi-file diff editor ("Open All Changes"), the merge editor, the GitHub Pull Requests
  extension's diffs: not explored; see Q3.
- Git's own behaviour from a Studio editor ("Git: Open Changes" does nothing there): VS Code's Git,
  not Studio.
- macOS and Linux behaviour beyond what CI covers.

## 6. Tests and acceptance

- **Unit / host tests** (`test/host/`): the real-file choice of 4.1 for the four cases (git diff:
  modified; replace preview: original; two `.md` files: modified; no file side: none), and
  `openPreview` from a diff opens no text editor and previews the real file whatever side is
  active.
- **Package contract**: the new `editor/title` clause.
- **Integration** (real VS Code, `test/integration/`, lifecycle and scroll-sync suites):
  - T1: git diff (or Compare with Saved) of a long `.md`, side preview open, scroll the modified side
    to the end: the preview scrolls (today 0 px).
  - T2: replace preview of a `.md` match, run "Open Preview to Side": the side preview shows the real
    file, no information message.
  - T3: cursor in a git diff's original side, run the command: the preview of the working-tree file,
    no text editor tab added.
  - T4: the title button is visible on a diff editor of a `.md` file, hidden on a diff of a non-`.md`
    file (checked through the menu contribution if the real menu cannot be read).
- **Visual / evidence**: a screenshot of the title button on a git diff and of the side preview
  following a scrolled diff, for the PR body (`pull-request.guidelines.md`).
- Acceptance: the three behaviours of section 1 in a real VS Code window; CR-445's diff tests still
  pass (no diff pulled into Studio); `just preflight` passes.

## 7. Overlap with CR side-preview-jump-marker

The sibling CR (being specified now: the side preview shows CR-445's target-line marker when a text
editor of its file is opened at a line by a jump) touches the same code:

- `src/session/features/scrollSync.ts` (`syncEditorToPreview`, `requestRevealLine`,
  `postPendingRevealLine`): the jump marker posts a reveal line to the side preview, this CR changes
  which editor scrolls it. Both edit the anchor handling of the side preview.
- `src/session/hostEvents.ts` (`onActiveEditorChanged`, `onVisibleRangesChanged`) and the side
  preview's following of the active editor.
- `src/host-vscode/openingWatcher.ts` (jump detection, `tabKindOf` "diff"): the jump CR likely
  reads jumps there; this CR may reuse its diff recognition.
- SwRS-MDOKFSTUDIO-LIFE-026 and LIFE-100, and the scroll-sync integration suite.

Recommendation: stack the two PRs (`stacked-prs.guidelines.md`) rather than run them on parallel
branches from `main`, and settle Q4 in both specs the same way.

## 8. Open questions for the owner

- **Q1, scroll from the preview to the diff.** With a text editor, scrolling or clicking the side
  preview also moves the editor (scroll editor with preview, reveal), and the editor's caret line is
  marked in the preview. The owner asked for diff → preview only. Should the preview also scroll the
  diff and should the diff's caret line be marked in the preview, as for a text editor?
- **Q2, diff with no real file.** Staged changes (`git:` HEAD against `git:` index) and a timeline
  commit diff (two `git:` versions) have no `file:` side, yet the button would show (the resource
  ends in `.md`). Should the button open the preview of the working-tree file of that path, stay
  hidden, or show the current refusal?
- **Q3, other diff editors.** Should the button and the scroll also work in the multi-file diff
  editor ("Open All Changes", Source Control's multi-diff) and in the merge editor? This spec leaves
  them as today.
- **Q4, jump into a diff (shared with side-preview-jump-marker).** A jump can open a diff (clicking a
  search match with a replace text opens the replace preview at that line). Should the side preview
  then show the target-line marker on that line of the real file, as for a jump into a text editor?
- **Q5, replace preview side (reading of decision 2, section 3).** Confirm that in the replace
  preview "the real file" wins over "the modified side": Studio previews the original (left) side,
  the real file, not the virtual "after replacement" document.
