# 056 — refactor-host-neutral-core

From backlog `P1/refactoring-study` (moved here: `00-intent.md`, `01-analysis.md`,
`02-multi-host.md`). The spec is `01-analysis.md` sections 4–5 (phases 0–8, definition of done)
plus the decisions D1–D6 and M1–M8 in both analysis files. The analysis is dated 2026-10-21:
re-measure before each step (since then `extension.ts` grew to 5 830 lines, `scrollSync.ts` to
5 668, and the runtime script and CSS are now served as bundled files, `src/webview/previewRuntimeEntry.ts`,
though still built from strings via `toString()`).

## Decisions (user grill, 2026-10-23)

1. **Go now**, without the okfreq requirements layer (overrides the 2026-10-22 order; okfreq stays
   parked). The safety net is the existing campaign (unit, 320 visual scenarios, real VS Code
   integration) plus step S1.
2. **One PR for the whole refactor, 5–8 commits.** Work in steps, one commit per step, each step
   with its own coder + reviewer cycle (max 3 rounds per step). The driver commits each approved
   step. Steps (merge phases if it keeps the commit count ≤ 8):
   - **S1 Safety net** (phase 0): focused tests for timer/race ordering, page-side message
     validation, `toString()`-sensitive code, before moving code.
   - **S2 Protocol** (phase 1): one typed, transport-agnostic protocol for both directions
     (discriminated unions, co-located validators, typed routers on each side), legacy messages in
     the registry, `isPreviewSyncMessage` retired, core revision counter instead of VS Code
     document versions.
   - **S3 Ports** (phase 2): host-api interfaces of `02-multi-host.md` §3.2 (DocumentStore,
     FileSystem async, Settings, WorkspaceInfo, HostUi, VcsInfo, Diagnostics, Watcher,
     ProcessRunner, AssetResolver, Navigation, capabilities) with a VS Code adapter; edit
     operations as pure core functions returning text edits.
   - **S4 Host extraction** (phase 3): feature controllers, `PreviewSession`, `PreviewManager` on
     ports only; module-level globals and `ActivePreview` god object removed; `*ForTests` hooks
     reduced.
   - **S5 Page bundle and split** (phases 4 + 6): page runtime as a typed esbuild bundle with normal
     imports and a `HostTransport` (no more `Function.prototype.toString()` injection), boot
     context as JSON, feature modules on a page bus; neutral theme token layer mapped to
     `--vscode-*`. CSP stays strict (D2/M8: change script loading only if security improves with
     no visible effect).
   - **S6 Layout and boundaries** (phase 5): `src/core`, `src/host-api`, `src/page`,
     `src/node-services`, `src/host-vscode`; **dependency-cruiser** (allowed new dev dependency,
     install it in this CR) enforcing core ↛ vscode/DOM/Node built-ins, page ↛ host; run by
     `just check`. **File size ratchet** in `just check`: 800 lines for `src/`, 1 500 for tests;
     files already above are listed with their current size and may only shrink.
   - **S7 Registries** (phase 7): palette actions, MyST directives, settings (one table that also
     generates the `package.json` configuration schema, categories and order unchanged).
   - **S8 Internals and tests** (phase 8): `mystRenderer.ts` as named passes with a dispatch table,
     `okfFrontmatter.ts` split parse/validate/serialize, CSS as `.css` files, remaining test
     splits including `test/visual/capture.py`. The big files (`extension.ts`, `scrollSync.ts`,
     `previewStyles.ts`) end under the ratchet ceiling.
3. **Definition of done, every step**: `just check` + `just visual` green; **no visible behaviour
   change** (visual baselines unchanged, real-input tests unchanged); TSDoc on every exported
   symbol of the core, the service interfaces and the protocol (D6); tests of the touched area
   reorganised to mirror the new modules (D4); boundary lint passing once it exists. Never weaken
   a test to make a move pass.
4. **Real VS Code**: local `npm run test:integration` under the window lock at the end of S2, S4,
   S5 and the last step; one manual heavy CI run (`-f heavy=true`) before ready.
5. **Freeze of `src/`** during this CR: no other CR touches `src/`; docs, CI, dependency and
   backlog CRs may run in parallel.
6. Branch `changes-requests/056-refactor-host-neutral-core`, no assets branch (no visible change).
   Open the PR as **draft after S1**, push after each approved step, mark ready after the last
   step with `checks` green and the heavy run. Rebase on `origin/main` before each push.
7. Opus everywhere. PR for an external reader (what moved where, why, what stays identical for
   users); "Autonomous decisions" section; commits `Assisted-by: Claude:Opus-5.5`.
8. Not in scope: any new host (host-node, pywebview, Tauri, canvas, MCP App, JetBrains), the M5
   undo/save design, behaviour changes, PERF-10, STAB-05.
9. **At the end** (PR ready): run `just install-vsix` from the worktree so the user can test the
   refactored extension in their own VS Code; say so in the final report.
