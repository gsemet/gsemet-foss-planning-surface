---
type: cr-intent
id: 423-edit-mode-commit-latency
description: "Bug: after 1.9.2, committing a block edit on a large document still takes 0.6-1.9 s and opening a block editor ~0.4-0.7 s; render a commit without debounce and cut the forced layouts of the patch and of the editor open."
generated: {by: "agent:claude-opus-5-5", at: "2026-11-19T16:05:00Z"}
sources: [{id: issue, resource: "https://github.com/gsemet/markdown-okf-schema-studio/issues/423", title: "Edit mode still slow on large documents after 1.9.2: commit round trip and editor open", author: "github:gsemet", last_modified: "2026-11-19"}]
---

# Edit mode: commit round trip and editor open still slow

issue: https://github.com/gsemet/markdown-okf-schema-studio/issues/423

Follow-up of #420 (shipped in 1.9.2). On `08-research-plan-implement.md` of the white paper, in
the author's own environment (145 extensions, 8-folder workspace), committing a block edit takes
1.9 s the first time after opening, then 1.1 s and 0.6 s; opening a block editor takes ~670 ms.
The issue and its comment hold the source-mapped profiles of the webview, the extension host and
the render worker.

## Known

- The build queue waits twice the last render before rendering (`currentDebounceMs`, capped at
  1,000 ms). The first render after opening is slow under load (457 ms), so the first commit waits
  ~1 s before its render starts. A commit from the preview is a final change: it needs no wait.
- The webview spends ~300 ms applying the patch: `tableRowMove.position` runs synchronously from
  `applyEditMode` (~200 ms with its forced style and layout), and seven full-document forced
  recalcs follow each other (`closeBlockEdit`, `scrollCore.measure`/`maxScrollTop`,
  `firstClearance`, `stickyHeadings`, `blockSelectionView`).
- Opening a block editor forces five full recalcs (`beginEditAnchor`, `firstClearance`,
  `syncPaletteSticky`, `resizeTextarea` x2) between writes, one of them the
  `data-sphinx-preview-block-editing` attribute on `documentElement`.
- The host parses the rendered HTML with parse5 three times per commit (`analyze`, `shellOf`, the
  properties table): ~65-85 ms.
- Other extensions share the extension host (markdownlint 70-265 ms, Todo Tree, MPE, GC); today
  they run inside our debounce window.

## Not in scope

- Hover paint cost and VS Code's own `did-mouse-move` sash handler.
- `content-visibility` on top-level blocks.
