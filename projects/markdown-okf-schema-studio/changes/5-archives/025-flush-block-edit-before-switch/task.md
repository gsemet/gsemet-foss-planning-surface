# T1 — Flush the open block editor before any document switch

Worktree: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-025 (branch
`fix/flush-block-edit` from origin/main). Work ONLY there; `node_modules`/`.venv` are symlinks to
the main checkout: never delete or stage them. Read `00-request.md` (decisions) and `rules.md`.

## Change

1. Map every path that makes the preview show another document or reload its page: link clicks to
   another file (webview → host message), toolbar Back/Forward (NavigationHistory), the preview
   following the active text editor, panel hide/dispose, window close/reload. Note each in the report.
2. Page side (src/webview/scrollSync.ts and the block/cell/frontmatter editors): before posting a
   navigation message, flush the open editor (pending autosave or not yet autosaved text) with a
   save that closes the editor, then post the navigation. Invalid content is written as typed.
3. Host side (src/extension.ts, message registry src/preview/previewMessages.ts): process the save
   before the navigation and await the WorkspaceEdit before switching document. For switches the
   host starts itself (editor tab follow, Back/Forward triggered on the host), ask the page to flush
   and await its save (with a bounded wait so a dead page cannot block), then switch. readOnly and
   untrusted previews never edit (keep the existing refusals).
4. One undo step per saved edit, as the autosave does today. No change when no editor is open.

## Tests

- Unit tests for any new pure logic (ordering helper, flush decision).
- Real-input integration scenarios (test/integration/realInput.test.ts style), one per trigger:
  type in a block editor, then IMMEDIATELY (< 400 ms, no wait for autosave) follow a link to another
  file / Back cross-doc / switch editor tab; assert the typed text is in the source document and the
  editor is closed. Also a frontmatter editor with invalid YAML, and a table cell.
  They cannot run locally (VS Code windows): write them carefully, compile them, CI runs them.
- Capture a relevant screenshot in one scenario (the source document showing the flushed text, or
  the preview after coming back) through the existing capture helpers, for the PR.

## Docs

CHANGELOG Unreleased bullet (user-facing: typed text is never lost when you follow a link, go Back
or switch tabs right after typing). README only if it documents autosave.

## Gates (foreground, windowless only)

`npx tsc -p .`, `just check`, `just visual`. No integration/e2e/preflight locally.

## Report

`/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/requests/025-flush-block-edit-before-switch/reports/T1-r<round>.md`.
