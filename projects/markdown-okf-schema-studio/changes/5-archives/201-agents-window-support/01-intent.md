# Studio in the VS Code Agents window

Type: feat · Priority: P1 · Filed 2026-10-29 by the user (main session) · Spike done, CR not
opened. Next files: [02-decisions.md](02-answers.md), [03-spike-report.md](work/03-spike-report.md),
[04-implementation-plan.md](work/04-implementation-plan.md).

## Problem

Studio works in the main VS Code window, but the Agents window (VS Code 1.144) does not offer it:
"Open With" lists only "Text Editor" and "Markdown Editor". The cause is not a missing Copilot
canvas. The Agents window disables every installed extension that has executable code and has not
declared support for that window (`capabilities.agentsWindow.supported` in `package.json`).

## Intent

- Studio runs in the Agents window without any user setting, through its manifest declaration.
- A Markdown file of the active agent session opens editable, as it does in a workspace folder of
  the main window.
- Switching agent sessions in the Agents window does not close a Studio tab, and does not leave a
  stale read-only page behind.
- The user documentation explains how to open Studio in the Agents window and gives the
  workaround setting for older VS Code builds.

## Out of scope

- A Copilot canvas. Canvases are agent-driven side panels, not file editors (checked during the
  spike).
- Making Studio the default `.md` editor in the Agents window. VS Code owns that choice through
  `workbench.editor.markdownDefaultEditorInAgentsWindow` and `workbench.editorAssociations`.

## Sources

- Agents window configuration, extensions section:
  https://github.com/microsoft/vscode-docs/blob/main/docs/agents/run/agents-window-configuration.md
- Support gate: `src/vs/workbench/services/extensions/common/extensionManifestPropertiesService.ts`
  in microsoft/vscode, and `IExtensionCapabilities.agentsWindow` in
  `src/vs/platform/extensions/common/extensions.ts`.
- Session folder mounting:
  `src/vs/sessions/contrib/workspace/browser/workspaceFolderManagement.ts` in microsoft/vscode.
- Related upstream request: microsoft/vscode#330192 (extensions in the Agents window).
