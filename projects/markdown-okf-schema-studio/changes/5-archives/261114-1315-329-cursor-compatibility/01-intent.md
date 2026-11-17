# Cursor compatibility report

Type: report (no fix). Split from CR-322 "publish to Open VSX" (its `01-intent.md`).

## Owner's words

> Then check what would be necessary to be compatible with Cursor

## What was checked (code at `origin/main`, branch of CR-322)

- `engines.vscode` is `^1.95.0` in `package.json`.
- No `enabledApiProposals`, no `extensionKind`, no `browser` entry, no `extensionDependencies`.
- A custom text editor: `registerCustomEditorProvider` (`src/host-vscode/activation.ts`), view type
  `markdown-okf-schema-studio.editor`, priority `option`.
- A webview panel with a serializer: `createWebviewPanel` and `registerWebviewPanelSerializer`
  (`src/host-vscode/activation.ts`). Standard APIs, but webview behaviour in Cursor is unproven.
- `capabilities.agentsWindow.supported: true` is VS Code specific; presumably ignored elsewhere (to
  confirm).

## What stays open

- Compare `engines.vscode` (`^1.95.0`) with the VS Code engine version that Cursor, VSCodium and
  Windsurf report (each editor's About box or release notes): not checked.
- Install the Open VSX build in Cursor and run a smoke test: open a document, edit a block, open the
  preview to the side. Nobody can prove it without Cursor installed.
- Confirm that `agentsWindow` is ignored without error outside VS Code.

No gap is proven; no fix is proposed.
