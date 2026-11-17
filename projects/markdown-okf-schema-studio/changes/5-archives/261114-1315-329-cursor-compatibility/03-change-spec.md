# Change Specification: Cursor, VSCodium and Windsurf compatibility

Type: docs (report closed with checks; no code change). Priority P1, batch-04.
Sources: `01-intent.md` (split from CR-322), `02-answers.md` (2026-11-14). Code read at `main`
`5a61b0c9` (version 1.9.1). Public pages read on 2026-11-14.

## Goal

Close every open point of the report that does not need Cursor installed, and tell users which
editors are expected to run Studio and where they install it from. No gap was found, so nothing
in `src/` or `package.json` changes.

## Facts checked for this specification

### Engine versions of the forks

| Editor | Current build | VS Code engine it reports | Source | Meets `^1.95.0` |
| --- | --- | --- | --- | --- |
| VS Code | 1.146.0 | 1.146.0 | `update.code.visualstudio.com/api/releases/stable` | ✅ |
| VSCodium | 1.143.17232 (2026-10-28) | 1.143 (VSCodium tags follow the VS Code version) | GitHub releases API, `VSCodium/vscodium` | ✅ |
| Cursor | 3.30.14 (stable download API) | 1.128.0 for Cursor 3.24 to 3.29; 1.105.1 for Cursor 2.x | About-box text in Cursor forum bug reports, 2026-11-04 to 2026-11-13 | ✅ |
| Windsurf | 3.12.59 | 1.141.2 ("The editor now uses VS Code 1.141.2", 3.12.x entries) | `windsurf.com/changelog` | ✅ |

> [!NOTE]
> Cursor publishes no engine number in its changelog. The 1.128.0 value comes from the
> "VSCode Version" line that users paste from the About box into forum reports. The newest
> Cursor build (3.30.14) was not checked, but its engine can only be the same or newer.

Every current build of the three forks is well above 1.95. Only very old builds would be refused:
Windsurf before its "Merged changes from VS Code 1.97.0" release (1.6.x) and Cursor 0.x.

### The code uses nothing newer than VS Code 1.95

- The lock file resolves `@types/vscode` to 1.140.0, so `just check` accepts any API up to 1.140.
  To find out whether the code relies on that, `src/` was type-checked against
  `@types/vscode@1.95.0` (the same `tsconfig.json` with `src/**/*.ts` only, TypeScript 7.0.2):
  **0 errors**. The control run against 1.140.0 also has 0 errors.
- The built-in commands it runs (`setContext`, `type`, `vscode.open`,
  `workbench.action.lockEditorGroup`, `workbench.action.unlockEditorGroup`,
  `workbench.actions.view.problems`) all existed long before 1.95.
- The manifest has no `enabledApiProposals`, no `extensionKind`, no `browser`, no
  `extensionDependencies` and no `extensionPack` (confirms `01-intent.md`).

### `capabilities.agentsWindow` is ignored outside VS Code

- VS Code's manifest validator (`src/vs/platform/extensions/common/extensionValidator.ts`,
  `validateExtensionManifest`, read at tag 1.105.1, the engine of Cursor 2.x) checks `engines`,
  `main` and `browser`, but never reads `capabilities`. At 1.105.1, `IExtensionCapabilities` has
  no `agentsWindow` key, so an older engine does not read the key at all.
- Open VSX accepted the 1.9.1 manifest with the key: `open-vsx.org/api/GaetanSemet/markdown-okf-schema-studio`
  returns version 1.9.1, `engines.vscode` `^1.95.0`, published 2026-11-14.
- Deduced from the source, not run: no fork was started.

### What stays unproven

The webview behaviour (custom editor, preview panel, panel restore) in a fork. Only a smoke test
in an installed fork proves it (open question 2).

## Decisions (Chief of Staff, no user impact)

1. **No code or manifest change.** `engines.vscode` stays `^1.95.0` unless the owner says
   otherwise (open question 1). SwRS-MDOKFSTUDIO-LIFE-001 and its test stay as they are.
2. **User docs name the editors, not their version numbers.** Fork version numbers go stale every
   few weeks, so the docs give the minimum engine (VS Code 1.95) and the editors, and the numbers
   stay in this spec.
3. **The Agents window section says it is VS Code only.** Cursor, VSCodium and Windsurf have no
   Agents window. The `agentsWindow` declaration does nothing there and causes no error.
4. **No requirement change.** No SwRS covers fork compatibility, and this change adds no behaviour.
   The writing skill does not change (no rendered syntax changes).

## What changes

### 1. `docs/user/open-studio.md`, section "Install and Open Studio"

After the two install paragraphs, add a short paragraph (the wording is up to the coder):

- Studio needs VS Code 1.95 or later, or an editor built on it.
- Expected to work in VSCodium, Cursor and Windsurf, installed from Open VSX. Their current
  builds are based on newer VS Code versions.
- The wording follows open question 2: "expected to work" until a smoke test is done, "tested in
  <editor>" after it.

### 2. `docs/user/open-studio.md`, section "In the Agents window"

Add one sentence at the top: the Agents window is a VS Code feature; other editors have no Agents
window, and Studio works there in the normal editor.

### 3. `README.md`, section "Install"

Apply the same change in one sentence: name Windsurf next to VSCodium and Cursor, and give the
minimum (VS Code 1.95 or an editor built on it). Keep the Marketplace and Open VSX links as they
are.

## Acceptance checks

1. `docs/user/open-studio.md` and `README.md` name VSCodium, Cursor and Windsurf, say they install
   from Open VSX, and give VS Code 1.95 as the minimum. Neither file gives a fork version number.
2. The "In the Agents window" section says the Agents window is VS Code only.
3. `git diff --stat origin/main` lists only `README.md`, `docs/user/open-studio.md` and this CR's
   files. Nothing changes under `src/`, `test/`, `requirements/` or in `package.json`.
4. `just preflight` passes.

## Out of scope, follow-up candidate

The engine floor is not protected: `@types/vscode` resolves to 1.140.0 while `engines.vscode`
says 1.95, so a future change could use a newer API and break VS Code 1.95 to 1.139 users without
any check failing. A `just check` step that type-checks `src/` against `@types/vscode` at the engine
floor (the check run for this spec) would close it. That is a backlog item for the Chief of Staff
to file, not part of this change.

## Open questions (owner, user impact)

1. **Lower `engines.vscode` below 1.95?** Recommended: **no, keep `^1.95.0`.** Every current
   build of VS Code, VSCodium, Cursor and Windsurf is at 1.105 or later, so a lower floor lets no
   current user in, and nothing below 1.95 is tested.
2. **Smoke test in a real fork?** It means downloading and installing Cursor (or VSCodium) on this
   machine, then opening a document, editing a block and opening the preview to the side.
   Recommended: **Cursor, done by the owner, after merge**: it is the editor the owner asked
   about, its editor runs without signing in, and it installs from the same Open VSX build users
   get. VSCodium is the fallback if Cursor will not install. Until then the
   docs say "expected to work". If the owner declines, the docs keep "expected to work" and the
   report closes with the webview point unproven.
