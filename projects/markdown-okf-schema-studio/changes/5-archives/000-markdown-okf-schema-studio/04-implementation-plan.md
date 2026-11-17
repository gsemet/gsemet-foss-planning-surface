# VS Code Sphinx/MyST Live View: Implementation Plan

## Scope

Implement an opt-in, read-only VS Code preview of the currently open Markdown file in this
workspace. The preview must render its MyST syntax through the project's Sphinx HTML configuration,
update from the active unsaved buffer, and provide stable two-way block/line navigation. The stock
Markdown editor, preview, commands, settings, plug-ins, and diff workflow remain unchanged.

The first release includes one side preview following the active Markdown editor. Fixed-file and
multi-panel modes, a stock-preview clone, and the later Obsidian-like edit mode are outside this plan.
The extension must be locally packageable and usable in the current white-paper VS Code window
after VSIX installation and reload; it does not need marketplace publication or its own repository.

## Governing Inputs

- [Approved implementation specification](03-spec.md)
- [Stock preview research inventory (historical)](02-stock-livepreview-spec.md)
- [Original broader proposal (superseded scope)](01-plan.md)
- [Repository constitution](../../../../CONSTITUTION.md)
- [Build-system guideline](../../../guidelines/build-system-setup.guideline.md)
- [Documentation guideline](../../../guidelines/documentation.guideline.md)

## Delivery Strategy

The first three tasks are feasibility gates. They prove the risks that could invalidate the product
before broad integration begins. Tasks 04-07 must not proceed unless Tasks 01-03 record `GO` with
reproducible evidence.

1. Prove authentic Sphinx HTML of the open file can run in a VS Code Webview under Workspace Trust,
   restrictive CSP, bounded resource roots, and hostile-resource tests. Provide a debug launch
   and a local VSIX install path for use in this workspace's current VS Code window.
2. Prove a versioned snapshot of the active unsaved file renders without writing to the worktree
  or invoking the source-writing `book-prepare` recipe.
3. Prove Sphinx nodes retain real source lines for the active document, with stable two-way
  block/line synchronization.
4. Test actual rendered output for representative MyST syntax in a single open file, plus clear
  diagnostics when a referenced input is unavailable.
5. Integrate a side preview that follows the active Markdown editor, refreshes on edits, and
  preserves correct identity, status, and navigation.
6. Complete scrolling, basic interaction, accessibility, and stock-preview non-regression.
7. Verify the extension installed in the current VS Code window, record hard-gate evidence, and
  document its scope and limitations. No full P01-P24 parity claim is required.

## Dependency DAG

```text
01 Active-file HTML, CSP, and trust gate
├── 02 Active dirty snapshot gate
└── 03 Active-file source-position and scroll gate
    02 + 03 ──> 04 MyST rendering fixture
        └──> 05 Active preview integration
          └──> 06 Interaction and accessibility
            └──> 07 Release evidence
```

Task 02 and Task 03 may run in parallel after Task 01. All later tasks are ordered because they
exercise the same preview lifecycle and acceptance matrix.

## Tasks

| Task | Purpose | Depends on | Gate |
| ------ | ------- | ---------- | ---- |
| [01](05-tasks-01-authentic-html-security-gate.md) | Scaffold and prove active-file Sphinx HTML, trust, CSP, and resource safety | None | Hard `GO`/`NO-GO` |
| [02](05-tasks-02-dirty-snapshot-build-gate.md) | Render an active unsaved buffer outside the worktree | 01 | Hard `GO`/`NO-GO` |
| [03](05-tasks-03-source-mapping-scroll-gate.md) | Prove active-file source positions and two-way block/line sync | 01 | Hard `GO`/`NO-GO` |
| [04](05-tasks-04-sphinx-feature-contract.md) | Check actual MyST output and missing-input diagnostics | 02, 03 | Rendering gate |
| [05](05-tasks-05-preview-lifecycle-integration.md) | Follow the active file, handle edits, status, navigation, and restoration | 02, 03, 04 | Product integration |
| [06](05-tasks-06-interaction-parity.md) | Complete interaction, accessibility, and stock non-regression | 05 | Behavior gate |
| [07](05-tasks-07-release-evidence.md) | Verify current-window use, security, and focused validation | 06 | Release gate |

## Cross-Task Invariants

- The extension lives under `` and owns its TypeScript, package,
  tests, Webview assets, and release evidence.
- The nested package pins Node 24 and uses its own `.npmrc` for Renault Artifactory, matching
  the repository and Compendium marketplace conventions. The lockfile must not resolve from the
  public npm registry or contain credentials.
- The source does not auto-activate from `src/`: local VSIX installation in the current VS Code
  profile and window reload are required for current-window use. No marketplace publishing is needed.
- `just vscode-sphinx-liveview-build` packages the ignored local VSIX under
  `.artifacts/`; `just vscode-sphinx-liveview-install` builds and
  installs it through the `code` CLI (default or explicitly selected profile), or reports the
  manual Install from VSIX path if unavailable.
- Sphinx remains the only renderer. A failure produces diagnostics and stale last-good output,
  never a Markdown-It fallback or silently degraded HTML.
- Preview builds use the HTML builder and real [Sphinx configuration](../../../../sphinx/conf.py)
  for the open file. PDF, RevealJS, Confluence, and whole-book output are outside scope.
- Preview work never runs `just book-prepare`. That recipe writes `_nav.md`, `_toc_table.md`, and
  `index_latex.md` under `book/chapters/` via
  [generate-toctree.py](../../../../scripts/generate-toctree.py).
- Snapshot the active unsaved file; include an external input only if it is referenced by that file.
  The newest document version wins; stale results are discarded.
- No Sphinx, `just`, Python, or local server process starts in an untrusted workspace.
- Local resources and navigation remain workspace-bound, scheme-allowlisted, traversal-safe, and
  symlink-safe. CSP stays restrictive and scripts use nonces where scripts are unavoidable.
- Generated fragments without real source positions are non-navigable. No mapping is invented.
- The stock preview remains unchanged before and after installation. The extension contributes no
  stock command ID, Markdown-It plug-in, preview script/style, or default `.md` association.
- Native rendered diff stays in the stock preview; MyST diff is outside this release.
- Optional rendered-block editing is a later release and is not part of any task in this DAG.

## Validation Commands

Tasks 01 and 07 define targeted `just` recipes for extension development and checking. Until those
recipes exist, run package scripts from `` after Task 01 creates
its `package.json`.

For direct use in the current VS Code window, Task 01 also defines these workspace-root recipes:

```bash
just vscode-sphinx-liveview-build
just vscode-sphinx-liveview-install
```

Reload the VS Code window after installation; the recipe does not reload an open editor session.

```bash
cd markdown-okf-schema-studio
fnm exec -- npm ci
fnm exec -- npm run compile
fnm exec -- npm test
fnm exec -- npm run test:integration
```

When shared Sphinx configuration, hooks, toctree generation, or book output changes, also run:

```bash
just check-justfile
just book-check
just preflight
```

Task 07 must record commands actually run and their results. A command is not considered evidence
merely because it appears in this plan.

## Definition of Done

- Tasks 01-03 each contain reproducible `GO` evidence; otherwise work stops with the failed gate
  documented.
- The preview renders MyST syntax from the active unsaved file without changing the worktree;
  missing referenced inputs are diagnosed rather than triggering book-wide generation.
- The active-file side view follows editor changes and survives failures, links, themes, and reloads.
- The locally installed extension works on a real chapter in the current white-paper VS Code
  workspace after reload; Extension Development Host testing alone does not satisfy this check.
- Two-way source mapping stays stable at block/line granularity and never fabricates positions.
- All hard safety gates pass, including Workspace Trust and hostile-resource coverage.
- Applicable preview interactions have recorded evidence; unrelated P01-P24 features are not gates.
- The native Markdown preview and unrelated Markdown files are unchanged.
- Focused extension checks pass, and repository checks pass wherever shared build surfaces changed.
- Release notes state that fixed-file mode, edit mode, and native MyST diff are not provided.
