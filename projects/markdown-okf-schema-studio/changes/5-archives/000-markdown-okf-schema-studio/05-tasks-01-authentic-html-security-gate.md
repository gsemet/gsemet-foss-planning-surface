# Task 01 Inspector Review

**Verdict: ACCEPTED.** The coder implementation in `d0a543d` was initially `REWORK` because
versioned Sphinx resource URLs were validated as filenames, MyST includes were not staged, and
the hostile-content tests did not cover nested SVG, EOF CSS imports, or whitespace-obscured
refresh metadata. The trusted integration assertions also checked only generic `_static` text,
not surviving stylesheet links or dirty-buffer rendering.

The inspector repaired query/fragment-aware resource resolution, recursive include and stylesheet
handling, nested active SVG removal, metadata normalization, and trusted coverage. The inspector
also removed stale package diagnostics, preserved complete external navigation URLs, and added a
dirty-buffer test that verifies the on-disk fixture remains unchanged.

Independent validation now passes: compile and 11 security/staging unit tests, both isolated
untrusted/trusted extension hosts, the post-sanitization asset probe (9 local CSS and 12 local JS
links retained with zero missing local resources), `just check-justfile`, VSIX packaging, and
default-profile local installation. Task 01 is `GO`; Tasks 02-07 remain blocked until their stated
dependencies are completed.

## Task 01: Authentic HTML and Security Gate

**Depends on**: None

## Important Information

Before coding, Read FIRST -> Load [05-task-00-READBEFORE.md](05-task-00-READBEFORE.md)

## Applicable Guidelines

| Rule | Application |
| ---- | ----------- |
| [Repository constitution](../../../../CONSTITUTION.md) | Keep Sphinx as the sole renderer and use the pinned Node/npm conventions. |
| [Build-system guideline](../../../guidelines/build-system-setup.guideline.md) | Isolate preview output and preserve normal production build behavior. |
| VS Code Workspace Trust | Do not spawn Sphinx, Python, `just`, or a server before trust is granted. |
| Webview security | Use restrictive CSP, nonces, bounded `localResourceRoots`, and explicit URI validation. |
| Stock non-regression | Do not register stock command IDs, Markdown contributions, or a default `.md` editor. |

## Objective

Create the minimal extension development host and prove a `GO` or `NO-GO` for displaying the
currently open Markdown file's MyST/Sphinx HTML in a VS Code Webview, without weakening Workspace
Trust or resource security. A small file with an admonition, math, and a local image is sufficient.

## Files to Modify/Create

- `package.json`
- `package-lock.json`
- `.npmrc`
- `.nvmrc`
- `tsconfig.json`
- `.vscodeignore`
- `.gitignore`
- `.vscode/launch.json` at the white-paper workspace root
- `src/extension.ts`
- `src/security/*`
- `src/preview/*`
- `test/security/*`
- `test/integration/*`
- `docs/feasibility-authentic-html.md`
- `README.md`
- `justfile` for targeted extension development/check recipes only

## Detailed Steps

1. Scaffold a TypeScript VS Code extension with a distinct publisher/name and command namespace,
   unit-test, and isolated extension-host integration-test scripts. Pin Node 24 in the nested
   `.nvmrc`, matching this repository. Give the nested npm package its own `.npmrc`, using the
   Artifactory registry and corporate-network settings in the existing root `.npmrc` and
   [Compendium marketplace .npmrc](../../../../../nestor-compendium/src/marketplace/.npmrc).
   Create and verify its lockfile against that registry; no public npm registry or credentials in
   tracked files. Ensure `artifactory.tls.renault.fr` is reached directly on the Renault network
   or VPN (`NO_PROXY`/`no_proxy`), not through the corporate proxy. Use `fnm exec -- npm` from
   the extension package directory. Provide a workspace-root F5 launch configuration opening this
   book workspace for debugging.
2. Contribute only `Sphinx: Open MyST Preview to Side` for Markdown files in this workspace.
   Do not contribute `markdown.*` IDs, Markdown-It plug-ins, preview scripts/styles, a default
   editor association, or workspace setting changes.
3. Reject the command before any process spawn when `vscode.workspace.isTrusted` is false. Add an
   integration test that instruments process creation and proves the spawn count remains zero.
4. In a trusted isolated extension host, render the active Markdown file through the project's
   MyST/Sphinx HTML configuration into temporary output. Do not call `book-prepare` or require a
   full book build. Stage only inputs necessary for this file; report unavailable references.
5. Load the resulting page into a Webview. Rewrite local output resources through supported Webview
   URIs or a constrained bridge. Preserve theme CSS and any JavaScript, local images, fonts,
   anchors, and links needed by the rendered active file.
6. Apply a restrictive CSP. Allow only required origins and nonce-bearing scripts. Record each CSP
   allowance and the concrete project feature that requires it; reject broad `*`, arbitrary
   `file:`, inline event handlers, and uncontrolled script execution.
7. Centralize resource and navigation validation. Canonicalize paths, resolve symlinks, enforce
   staged output and explicit source asset roots, decode encoded paths before validation, and
   allowlist schemes. Cover raw
   HTML, active SVG, event attributes, `srcset`, CSS `url()`/`@import`, fonts, media, `javascript:`,
   `data:`, `vscode:`, encoded traversal, symlink escape, and unrelated workspace-file probes.
8. Add focused `just` recipes for development, checking, `vscode-sphinx-liveview-build`, and
   `vscode-sphinx-liveview-install`. The build recipe compiles and packages a local VSIX at
   `.artifacts/markdown-okf-schema-studio.vsix`, prints its path,
   and keeps generated artifacts untracked. The install recipe depends on the build recipe and
   uses `code --install-extension <vsix> --force` for the default profile, accepting an explicit
   VS Code profile for non-default installations. If the `code` CLI is unavailable, report the VSIX
   path and the manual Install from VSIX action instead of claiming success. Do not make the
   existing book build depend on these recipes.
9. Document local install/update without marketplace publishing, the VS Code window reload, and
   invoking the MyST command on an open Markdown file in this workspace. Do not claim that source files under
   `src/` auto-activate, that a VSIX installation is workspace-local, or that a recipe can reload
   the already-open VS Code window.
10. Record `GO` only if authentic output and required assets work under the restrictive policy. If
   required Sphinx output cannot be made Webview-safe, record `NO-GO`, document the tested embedded
   browser/server alternative and its scroll limitations, and stop the DAG.

## Acceptance Criteria

- [x] The extension opens only through a distinct MyST command for a Markdown file in this workspace.
- [x] Extension installation and activation do not alter stock Markdown contributions or `.md`
      editor associations.
- [x] An untrusted-workspace integration test proves zero Sphinx, Python, `just`, and server spawns.
- [x] A trusted host test displays real MyST/Sphinx HTML, theme CSS, an admonition, math,
   and a local image from the open file without a book-wide build.
- [x] CSP contains no wildcard source and no uncontrolled inline script or event-handler execution.
- [x] Hostile raw HTML, active SVG, `srcset`, CSS URL/import, font/media, scheme, traversal, encoded
      traversal, and symlink escapes are blocked or safely transformed with clear diagnostics.
- [x] Local resource access is limited to staged output and explicit assets used by the open file;
   unrelated workspace files cannot be fetched.
- [x] `fnm exec -- npm run compile`, unit tests, and isolated extension-host tests pass.
- [x] Nested `.npmrc` routes installs and VSIX packaging dependencies through Renault Artifactory;
   the lockfile contains no public npm registry URLs or credentials, and nested `.nvmrc` pins 24.
- [x] `just vscode-sphinx-liveview-build` creates the documented ignored VSIX without publishing.
- [x] `just vscode-sphinx-liveview-install` installs that VSIX using the available `code` CLI,
   supports an explicit profile, or reports a manual installation path when CLI is unavailable.
- [x] A local VSIX installs without publication; after reloading the current white-paper workspace,
      the MyST command previews the open Markdown file. F5 also opens this workspace for debug.
- [x] `just check-justfile` passes after adding recipes.
- [x] `docs/feasibility-authentic-html.md` records commands, artifacts, policy decisions, and
      an evidence-backed `GO` or `NO-GO`.

## Testing Strategy

Use pure unit tests for URI canonicalization, CSP generation, HTML/resource rewriting, and hostile
inputs. Use an isolated VS Code host for Workspace Trust, command contribution, real Sphinx
process launch, Webview rendering, and stock-contribution non-regression. Capture console/CSP errors
and assert required page artifacts, not only successful process exit.

## Notes

This is a hard feasibility gate. Do not add broad lifecycle, scroll, or fixed-view behavior here.
Tasks 02 and 03 may start only after this task records `GO`.
