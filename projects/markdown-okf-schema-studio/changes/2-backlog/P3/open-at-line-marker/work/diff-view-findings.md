# Studio in VS Code's diff views: what happens today

Explored 2026-11-20 by a Griller, on Studio `origin/main` at `dd89211d` (release 1.10.0), in a
real VS Code 1.147.0 window on Windows 11 (Extension Development Host, isolated user data, a
throw-away git repository with `doc.md` committed then changed in the working tree). The window
was driven by Playwright over CDP; the scripts are in `experiments/` (`01-diff-view-*` to `04-diff-view-*`), the
screenshots and the probes' logs in `evidence/diff-view/`.

Two settings were tried:

- **default**: Studio as installed, its custom editor at `"priority": "option"` (opened only by
  "Reopen Editor With..." or the side preview command).
- **assoc**: Studio made the default `.md` editor by the user,
  `"workbench.editorAssociations": {"*.md": "markdown-okf-schema-studio.editor"}`.

## How Studio is registered

- `package.json` `customEditors`: one editor, `markdown-okf-schema-studio.editor`, selector
  `*.md`, priority `option`. No `vscode.diff` call, no diff handling in `src/`.
- `resolvePreviewEditor` (`src/host-vscode/activation.ts:259`) shows "requires a Markdown file"
  for a document without a file path (any non-`file:` scheme, e.g. `git:`); this path was never
  reached in the trials, because VS Code never opened Studio inside a diff.
- The editor title button "Open Preview to Side" shows only when
  `activeEditor == workbench.editors.files.textFileEditor`: not on a diff editor. The palette
  command and `Ctrl+K Shift+V` work there.

## Results

| # | Diff view | default | assoc |
| --- | --- | --- | --- |
| 1 | Git: Open Changes (palette, from a text editor) | text diff | text diff |
| 2 | Source Control view, click the changed file | text diff | text diff |
| 3 | Timeline view, click the commit | text diff | (same command, not re-run) |
| 4 | File: Compare Active File with Saved (unsaved edit typed in a text editor) | text diff | text diff |
| 5 | Same, unsaved edit made inside a Studio editor | text diff | not run |
| 6 | File: Compare Active File With... another `.md` | text diff | text diff |
| 7 | Search and replace: click a match (replace preview) | text diff | text diff |
| 8 | Replace All while a Studio editor shows the file | Studio re-renders with the new text, file saved, no error | same |

So Studio never opens inside a diff, even when it is the user's default `.md` editor: every diff
is VS Code's own text diff, both sides, editable as usual. Nothing crashes, nothing is blank. The
replace preview works as without Studio. Evidence: `default-01`, `default-03`, `assoc-01`,
`assoc-03`, `assoc-09`, `p2-default-04`, `p2-default-09`, `p3-assoc-03`, `p4-default-01`, `p4-default-02`.

### The side preview while a diff is active

- **It stays on the real file.** With the side preview open, opening the git diff or the replace
  preview leaves it on `doc.md`, showing the file's current text (not the "after replacement"
  text of the replace preview) with its usual change bars against HEAD (`default-05`,
  `default-06`).
- **Scroll is not synced from a diff.** Text editor at the end: the preview scrolls to 1512 px.
  Git diff at the end (same document): the preview stays at 0 (`p3-default-01`, `p3-default-02`;
  same in assoc).
- **"Open Preview to Side" from a git diff** opens the preview of the file (works).
- **"Open Preview to Side" from the replace preview** refuses with "Open a Markdown file to use
  Markdown OKF-Schema Studio." The active side is VS Code's virtual "after replacement" document,
  which has no file path (`p2-default-07`).

### From a Studio editor

- The editor's "Open Changes" title button (Git's) opens the text diff (`p2-default-01`).
- The palette command "Git: Open Changes" does nothing at all when a Studio editor is active (no
  diff, no message) (`default-08`). Git reads the active text editor, and a custom editor is none;
  this is VS Code's Git behaviour, not a Studio error.
- "Compare Active File with Saved" from a Studio editor with an unsaved Studio edit opens the
  text diff (`p2-default-04`).

## Not tried

- A rendered diff inside Studio (nothing exists to try).
- Merge editor (conflict resolution), staged changes, multi-file "Open All Changes", the GitHub
  Pull Requests extension's diffs, macOS and Linux.
- The timeline and two-file compare in assoc mode (same VS Code command as the git diff).

## Reading

Nothing is broken: the owner's worry (the replace preview diff) works. The gaps are comfort
gaps of the side preview next to a diff (scroll, the refusal from the replace preview, the hidden
title button) and, as a possible feature, a rendered diff.
