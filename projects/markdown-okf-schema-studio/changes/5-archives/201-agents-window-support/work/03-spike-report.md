# Spike report: Studio in the Agents window

Date: 2026-10-29 · Host: VS Code 1.144.0 (macOS arm64), launched with `--agents` and isolated
user data, extensions, shared, agents-data and agents-extensions directories · Studio: VSIX built
by `just package` from `main` 95598afa (local build of 2026-10-29).

## How to replay

Everything is in [spike/](../experiments/spike):

- `spike.mjs <variant> '<settings-json>' <devPath...>` starts an isolated Agents window with CDP.
  Env: `INSTALL_VSIX=<vsix>` installs a VSIX first, `KILL=1` stops VS Code after collection,
  `AGENTS=0` opens a normal window, `PROBE_SCENARIO=folders` runs the folder scenario.
- `probe/` is a small extension that declares Agents window support. It records what an extension
  sees (`workspaceFolders`, the Studio extension state, tabs) and opens `ws/sample.md` with
  `vscode.openWith(..., "markdown-okf-schema-studio.editor")`.
- `inspect.mjs <port> [expr]` evaluates inside the Studio page through the webview `iframe` CDP
  target (`#active-frame.contentDocument`), as in the QA harness.
- `phases.sh <run-dir> <port>` drives the folder scenario and inspects the Edit button at each
  phase.
- `patch_vsix.py` (`uv run --no-project`) adds `capabilities.agentsWindow.supported: true` to a
  VSIX.

Results are in `spike/runs/<variant>/` (probe JSON, screenshots).

## Results

### Extension enablement

| Variant | Studio installed as | Settings | Studio in the Agents window | `openWith` result |
| --- | --- | --- | --- | --- |
| v1 | `--extensionDevelopmentPath` | none | enabled (development extensions skip the gate) | Studio tab |
| v2 | VSIX | none | **absent**, the user's symptom | built-in text editor |
| v3 | VSIX | `extensions.supportAgentsWindow: { "GaetanSemet.markdown-okf-schema-studio": true }` | enabled | Studio tab |
| v4 | VSIX + manifest declaration | `extensions.experimental.enableAgentsWindowCapability: true` | enabled | Studio tab |
| v5 | VSIX + manifest declaration | none | enabled | Studio tab |

Conclusions:

- The manifest declaration alone is enough on 1.144 (v5). The upstream source on `main` reads the
  declaration of a third-party extension only when `enableAgentsWindowCapability` is set; on 1.144
  it works without it. Keep the v3 setting in the docs as the workaround.
- A test with `--extensionDevelopmentPath` cannot reproduce the bug (v1). Any automated check of
  the gate must install a VSIX.
- Rendering, the toolbar, themes and the Open With picker work in the Agents window editor panel
  ([spike/agents-window-studio.png](../experiments/spike/agents-window-studio.png)).

### What an extension sees

- `vscode.workspace.workspaceFolders` is `[]` with no active agent session. The workspace is a
  synthetic `agent-sessions.code-workspace` (`folders: []` on disk, also in the user's real
  profile).
- When a session becomes active, the Agents window mounts its working directory with
  `updateFolders`/`addFolders`. On a session switch it replaces or removes the folders
  (`workspaceFolderManagement.ts`). Untrusted folders are never mounted.
- `workspace.isTrusted` is `true`.

### Folder lifecycle (v6, manifest declaration, no setting)

The probe repeats what `workspaceFolderManagement.ts` does with `updateWorkspaceFolders`:

| Phase | Folders | Studio page |
| --- | --- | --- |
| 1. `sample.md` opened, no session folder | `[]` | read-only: "Editing is unavailable: this file is not in a folder opened in the VS Code workspace" (expected) |
| 2. Session worktree mounted | `[ws]` | **still read-only** (gap 1) |
| 3. `second.md` opened after the mount | `[ws]` | editable ("Edit mode" enabled) |
| 4. Worktree removed (session switch) | `[]` | **the `second.md` tab is closed** (gap 2); `sample.md` stays read-only |

### Gaps in the code

- **Gap 1, mount does not promote.** `HostEvents.onFoldersChanged` (`src/session/hostEvents.ts`)
  only starts stem watchers for added folders. `PreviewManager.refreshTrust`
  (`src/session/previewManager.ts`) already promotes a read-only preview whose document is now in
  a trusted folder, but it runs only on `onDidGrantWorkspaceTrust`.
- **Gap 2, unmount closes the tab.** `onFoldersChanged` calls `disposeSession(session, true)` for
  every session whose folder was removed (SwRS-MDOKFSTUDIO-LIFE-143). In the Agents window, every
  session switch removes the folder.
- **Minor.** The Anchor button is disabled ("No text editor shows this file") because the Agents
  window rarely shows a text editor beside Studio. Expected behaviour, no change planned.

## Limits of the spike

- No real agent session: the isolated profile has no GitHub sign-in, so the session mount was
  simulated with `updateWorkspaceFolders`. The simulation calls the same workspace editing path
  as `workspaceFolderManagement.ts`.
- Remote or cloud session folders (non-`file` URIs) were not tested. Studio reads paths with
  `fsPath`, so such sessions stay out of scope.
