## Summary

Dragging a file from the VS Code Explorer onto the preview in edit mode now inserts a reference to
it at the drop position: a relative Markdown link for a Markdown file (its first heading as the
link text, the file name when it has none) and an image for a picture. Before, the drop did
nothing. While the files are over the page, the nearest insertion point shows a drop marker.

## Deliverables

- **Drop marker**: a 4 px line in the focus colour on the insertion point nearest to the pointer.
- **Link**: `[Getting started](The%20Guide.md)`; spaces and parentheses in the path are
  percent-encoded, `[`, `]` and `\` in the text are escaped, the path is relative to the edited
  document.
- **Image**: `![logo](../img/logo.png)`; several files give several references in one new block.
- One undo step, refused like a block paste (read-only preview, open block editor, stale page).
- Only `file:` addresses inside a workspace folder are used; anything else is ignored.
- README, user guide (`docs/user/editing.md`) and changelog describe the feature.

The "before" captures show the same page with the same drag: no marker, no change. The "after"
captures are headless Chromium captures of the real page bundle with the mock host (the link and
image captures render the document the host writes), cream and dark.

| Step | After (cream) | After (dark) |
| --- | --- | --- |
| Drop marker | ![](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/8936b33510101fe56afcf3c1779abf869401c8f6/after-cream-1-marker.png) | ![](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/8936b33510101fe56afcf3c1779abf869401c8f6/after-dark-1-marker.png) |
| Resulting link | ![](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/8936b33510101fe56afcf3c1779abf869401c8f6/after-cream-2-link.png) | ![](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/8936b33510101fe56afcf3c1779abf869401c8f6/after-dark-2-link.png) |
| Resulting image | ![](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/8936b33510101fe56afcf3c1779abf869401c8f6/after-cream-3-image.png) | ![](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/8936b33510101fe56afcf3c1779abf869401c8f6/after-dark-3-image.png) |

| Step | Before (cream) | Before (dark) |
| --- | --- | --- |
| Drop marker | ![](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/8936b33510101fe56afcf3c1779abf869401c8f6/before-cream-1-marker.png) | ![](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/8936b33510101fe56afcf3c1779abf869401c8f6/before-dark-1-marker.png) |
| Resulting link | ![](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/8936b33510101fe56afcf3c1779abf869401c8f6/before-cream-2-link.png) | ![](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/8936b33510101fe56afcf3c1779abf869401c8f6/before-dark-2-link.png) |
| Resulting image | ![](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/8936b33510101fe56afcf3c1779abf869401c8f6/before-cream-3-image.png) | ![](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/8936b33510101fe56afcf3c1779abf869401c8f6/before-dark-3-image.png) |

## Changes

New `src/core/mapping/dropReferences.ts` (reference building), `src/page/modules/dropFiles.ts`
(drag data, nearest bar), `src/page/features/fileDrop.ts` (marker and message); a new page-to-host
message `previewDropFiles` with its validator; a host handler in
`src/session/features/sourceEdits.ts` that reuses the block paste planner and answer.

## Tests

- 12 new unit and session tests (`test/core/mapping/dropReferences.test.ts`,
  `test/page/modules/dropFiles.test.ts`, `test/page/runtimeFileDrop.test.ts`,
  `test/session/dropFiles.requirements.test.ts`); the new files fail on the previous code (the
  modules, message and handler do not exist).
- `just check` passes: type check, boundaries, limits, unit 2880/2880, contracts, security 66/66,
  Python 45, requirements validation (1031, 0 errors). The `update-coverage --check` step reports
  drift in three files (StRS MYST-005, SwRS DIAG-097, SwRS PALETTE-003) that exists on the base
  branch and is not caused by this change; those files were left untouched.
- **Real-window drop scenario: pending.** `test/integration/dropFiles.test.ts` (scenario
  `drop-files`, cream and dark) is written and wired into the trusted real-window suite, but the
  author's macOS session was locked, so it has not run. It is proven by the heavy CI real-window
  job (on-demand); real VS Code window screenshots will follow. The captures above are headless.

### Requirements traceability

| ID | Source | Tests |
| --- | --- | --- |
| SwRS-MDOKFSTUDIO-PALETTE-004 (new; derives from StRS PALETTE-001 and PALETTE-018) | `src/core/protocol/pageToHost.ts`, `src/page/features/fileDrop.ts`, `src/session/features/sourceEdits.ts`, `src/core/mapping/dropReferences.ts`, `src/page/modules/dropFiles.ts` | `test/core/mapping/dropReferences.test.ts`, `test/page/modules/dropFiles.test.ts`, `test/page/runtimeFileDrop.test.ts`, `test/session/dropFiles.requirements.test.ts`, `test/integration/dropFiles.test.ts` |

StRS PALETTE-001 and PALETTE-018 gain a `derived_by` entry (generated).

## Autonomous decisions

- Wiki links are not part of the extension: a dropped `.md` file always gives a relative Markdown
  link, never a `[[wiki]]` link.
- In a real VS Code window, the webview only receives an Explorer drop while **Shift** is held
 . This is documented in the user guide and the
  changelog; the synthetic drag of the tests cannot show it, so it is not yet verified in a real
  Explorer drag.
- Nothing happens while a block editor is open: its text box keeps the browser's own drop.
- The first 64 KiB of a Markdown file are read to find its first heading; a file without heading
  uses its name.

## Impacts

Edit-mode preview gains a drop target; the page-to-host protocol gains one message (handler count
41 to 42). No setting, no change to saved documents unless a drop happens.

## Blast radius

2 (preview page runtime and the host edit path; shared block paste planner reused, not changed).

## Internal references

CR 146, backlog item `drop-file-as-link`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
