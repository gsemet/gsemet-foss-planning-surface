## Summary

Next to a VS Code text diff of a Markdown file (Git changes, Compare with Saved, a two-file compare, the search and replace preview), Studio's side preview was half-working: no title button on the diff, "Open Preview to Side" refused from the replace preview, the side preview did not switch to a diff of another file, and scrolling the diff did not move it. This PR treats the real file of a diff (the file on disk, never a `git:` or virtual side) as the file to preview.

## Deliverables

- The editor title button "Open Preview to Side" shows on a text diff of a `.md` file and opens the real file's preview beside the diff, without opening a text editor.
- From the replace preview, the command, the button and `Ctrl+K Shift+V` preview the real file (the original side) instead of refusing.
- The side preview switches to the real file when a text diff becomes the active editor.
- Scrolling the real file's side of a diff scrolls the side preview, and the preview's reveal targets only the real file's side.

```mermaid
flowchart LR
  tab[active diff tab] --> rf[diffRealFile: real file]
  rf --> op[openPreview]
  rf --> fol[follow active diff]
  rf --> sc[scrollSync: real file side only]
```

Real-file rule (`src/host-vscode/diffRealFile.ts`): both sides `.md` files, the active side; one side only, that side; no `file:` side (staged, timeline), the working-tree file at that path, no scroll sync.

**UNVERIFIED:** screenshots and the real-window tests (title button on a diff, replace preview, scroll in side-by-side and inline layouts) have not run yet.

## Blast radius

Grade: 2. It touches the open-preview command, the active-editor following and the scroll sync, which are shared. Revert restores the previous behaviour.

## Autonomous decisions

- The button test (T4) lives with the new diff integration suite rather than the lifecycle suite.

## Known gaps

- **UNVERIFIED:** the diff-to-preview scroll in a real window (cause of the former 0 px gap unproven); if it proves impossible it becomes a documented limitation.
- Multi-file diff and merge editors are out of scope (no API input class).
- Screenshots not yet captured.

<details>
<summary>Details</summary>

## Changes

- `src/host-vscode/diffRealFile.ts`: new reading of the real file of the active diff.
- `src/host-vscode/activation.ts`: `openPreview` uses it for no URI or a diff side's URI; a tab-change listener follows the active diff.
- `src/session/hostEvents.ts`, `src/session/features/scrollSync.ts`: follow by document; reveal targets only `file:` documents.
- `package.json` `editor/title` clause, and its package contract test.
- Tests: host tests with a diff-capable fake host; real-window suite `test/integration/diffPreview.test.ts`.
- Requirements (four SwRS of lifecycle-sync), docs, changelog, glossary.

## Human decisions

- The file of a diff is its real file; in the replace preview this is the original side, not the virtual modified side.
- On a staged or timeline diff the button previews the working-tree file; there is no scroll following then.
- If the scroll cannot work because of VS Code, the button and command still ship and the scroll becomes a written limitation.
- A diff stays VS Code's text diff.

## Impacts

The button, command, following and scroll work next to text diffs of Markdown files. No other visual change.

## Test plan

- [ ] New or changed tests (they fail on the previous code)
- [ ] Local gates at `<sha7>`
- [ ] Evidence: before at `<sha7>`, after at `<sha7>`
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

- CR-455 side-preview-diff-gaps.

</details>
