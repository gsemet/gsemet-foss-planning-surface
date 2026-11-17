# READ BEFORE: VS Code Sphinx/MyST Live View

## Product Boundary

Build an opt-in, read-only VS Code preview of the currently open Markdown file in this workspace.
Render MyST syntax in its unsaved buffer using the repository's Sphinx HTML configuration.
Do not replace or modify VS Code's stock Markdown editor or preview.

The first release includes:

- a side preview following the active Markdown file;
- live unsaved-buffer rendering, build diagnostics, and navigation;
- stable editor-to-preview and preview-to-editor block/line synchronization;
- actual Sphinx HTML output for MyST syntax in the active file.

The Obsidian-like edit mode is a later release. Do not implement it in this task set. Native MyST
rendered diff remains in the stock preview. Fixed-file and multi-panel modes, book-wide builds,
and full P01-P24 parity are not first-release requirements.

This extension is developed in this repository for direct use in the current white-paper workspace.
Source under `src/` does not auto-load in VS Code: provide a locally installable VSIX and document
installation/reload in the current window. Installing a VSIX affects the selected VS Code profile,
not just this workspace; keep commands opt-in and limited to this workspace. Marketplace
publishing and extraction to a standalone project are outside this task set.
The workspace-root `just vscode-sphinx-liveview-build` and `just vscode-sphinx-liveview-install`
recipes produce and install the ignored VSIX under `.artifacts/`.
The install recipe supports an explicit profile when the active window is not using the default.
If `code` is unavailable, show the path for manual Install from VSIX instead; the user reloads
the open window after installing.

## Non-Negotiable Gates

1. Use authentic MyST/Sphinx HTML for the open file. Never silently fall back to Markdown-It.
2. Render the active dirty `TextDocument` without saving or modifying user source. Diagnose
  unavailable references; do not regenerate bibliography or navigation for an unrelated file.
3. Keep staged active source, doctrees, and output outside the worktree and production `_build/`.
4. Never invoke `just book-prepare` from preview code. It writes `_nav.md`, `_toc_table.md`, and
   `index_latex.md` under `book/chapters/`.
5. Never start Sphinx, `just`, Python, or a server unless `vscode.workspace.isTrusted` is true.
6. Enforce restrictive CSP, bounded local resource roots, scheme allowlists, traversal and symlink
  checks, and handling of raw HTML, active SVG, event attributes, `srcset`, CSS URLs/imports,
   fonts, media, hostile schemes, and encoded paths.
7. Preserve real source file/line origins in the active file. Included and generated fragments
  without a trustworthy location are non-navigable.
8. Stop after a failed feasibility gate. Do not continue by weakening a hard requirement.

## Repository Facts

- Extension root: ``.
- Sphinx config: [sphinx/conf.py](../../../../sphinx/conf.py).
- Preview input: the currently open Markdown file in this workspace, not the entire chapter tree.
- Current HTML command:
  `uv run sphinx-build -W --keep-going -b html -c sphinx/ book/chapters/ _build/html/`.
- Current live server: `just book-serve-multipage`; it depends on source-writing `book-prepare` and
  therefore must not be called by preview code.
- Toctree generator: [scripts/generate-toctree.py](../../../../scripts/generate-toctree.py). Its
  default behavior must remain unchanged for normal book builds.
- Local Sphinx extensions: `src/sphinx_animation/` and `src/sphinx_figure_layout/`.
- Existing Sphinx test pattern: `src/sphinx_animation/tests/` with fixtures under `tests/fixtures/`.
- Node is pinned by `.nvmrc`; repository npm commands use `fnm exec -- npm`.
- The nested extension package must pin Node 24 in its own `.nvmrc` and carry its own `.npmrc`.
  Mirror the repository's Renault Artifactory registry and the working corporate npm settings in
  the Compendium marketplace; never rely on the public npm registry or commit credentials.
- Full repository gates are `just book-check` and `just preflight`; `just check-justfile` validates
  justfile formatting.

## Rendering Surface

Exercise representative MyST syntax in the currently open file: directives, admonitions, math,
links, figures, and syntax that relies on the project's Sphinx configuration. A citation or include
may load its referenced input if present; neither requires a book-wide regeneration pipeline.
Sphinx may load configured extensions, but only features the active file uses need preview tests.

## Stock Preview Contract

Use [02-stock-livepreview-spec.md](02-stock-livepreview-spec.md) for interaction ideas, not as a
release matrix. Stock preview and rendered diff remain unchanged. Safety, source integrity,
authentic Sphinx output, live active-buffer rendering, and two-way mapping are hard gates.

## Required Engineering Practices

- Read [CONSTITUTION.md](../../../../CONSTITUTION.md) before changes.
- Follow [build-system-setup.guideline.md](../../../guidelines/build-system-setup.guideline.md) for
  shared build surfaces and
  [documentation.guideline.md](../../../guidelines/documentation.guideline.md)
  for Markdown.
- Use `apply_patch` for manual edits.
- Do not modify generated chapter files, derived book assets, sacred SVGs, or production output.
- Add focused tests with each behavior change. Keep normal book builds independent of the extension.
- Copy upstream code only when necessary and preserve its MIT notice and attribution.
- Do not implement beyond the current task's files and objective.

## Task Completion Protocol

1. Run the focused checks named by the task.
2. If shared Sphinx/build behavior changed, run `just check-justfile`, `just book-check`, and
   `just preflight` as required by the task.
3. Record concrete evidence and unresolved limitations in the task's designated report or tests.
4. Update [06-implementation-status.md](06-implementation-status.md) for only the completed task.
5. Do not start a dependent task after `NO-GO`, failed hard gate, or missing required evidence.
