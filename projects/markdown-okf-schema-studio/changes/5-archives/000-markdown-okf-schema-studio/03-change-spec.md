# VS Code Sphinx/MyST Live View: Implementation Specification

Status: specification, not an implementation or a claim of tested parity.
Source documents: [evaluation and plan](work/01-plan.md) and
[stock-preview behavioral specification](work/02-stock-livepreview-spec.md).

## Goal and Boundary

Provide an opt-in, read-only VS Code preview of the currently open Markdown file in
this workspace. Render its MyST syntax from the unsaved editor buffer, update while
typing, and synchronize source and preview in both directions. Preserve the stock Markdown
editor and preview for every Markdown file, including their commands, shortcuts,
extensions, settings, and rendered-diff workflow. Do not register the new view as the
default `.md` editor or replace the built-in renderer.

The active document is the unit of preview, not the whole book. Do not require a
book-wide build, bibliography regeneration, release metadata, generated navigation,
or synchronization of other dirty documents merely to display the current file.
Resolve a referenced file or asset only when the open document actually uses it;
report unavailable dependencies in the preview without modifying repository files.

The first release needs one side preview following the active Markdown editor and
updating as that editor changes. It must not take over the stock preview or editor.
No third-party Markdown-It syntax contribution is required in the MyST view;
third-party contributions must continue to work in the stock preview. Fixed-file
views, multi-panel management, and later rendered-block editing are not first-release
requirements.

Use this project's MyST/Sphinx HTML configuration for the active file, so syntax
actually present in it renders as Sphinx would render it. A file with a citation or
include may need its referenced input; a file without one must not require
bibliography or include processing. PDF, RevealJS, Confluence, and book-wide
publication output are outside this preview. Do not silently substitute another
renderer when Sphinx fails; show a useful error instead.

## Live Document Contract

- Render the newest in-memory `TextDocument` version without requiring a save and
  without saving or modifying the user's buffer. Resolve local references when used
  by that document; do not require an overlay of every dirty workspace document.
- Stage the active file and any inputs it actually needs outside the worktree.
  Do not invoke the source-writing `book-prepare` recipe or modify generated book
  files. Keep preview output separate from production build outputs.
- Rebuild on edits to the active buffer and its referenced assets or inputs.
  Debounce edits, discard obsolete builds, and reject stale versions before display.
- Show pending status while building. On failure, show actionable diagnostics and
  retain the last successful result visibly marked stale; never present another
  document's output as current. Recover on the next valid edit or explicit refresh.
- Map visible blocks back to the active source where Sphinx preserves a real line.
  For included content, use its actual origin when available. Generated fragments
  with no valid source position must not navigate to fabricated locations.

## Interaction and Parity Contract

The stock behavior inventory P01-P24 in
[02-stock-livepreview-spec.md](work/02-stock-livepreview-spec.md) informs interaction
tests, not a mandate to reproduce every stock command or editor mode. Verify that
installing and using the MyST view does not change the built-in preview.

Support editor-to-preview and preview-to-editor scrolling at stable block/line
granularity for the active document. Pixel precision is unnecessary. Avoid loops,
wrong-editor targeting, and drift. Provide ordinary preview links, find, selectable
text, theme support, and keyboard access; do not take on a full stock-preview clone.

Keep any MyST-specific settings independent of stock settings. The new command
must not alter unrelated Markdown files or installed Markdown-It plugins.

Native rendered diff remains in the stock preview; a MyST diff view is out of scope.

Do not advertise full P01-P24 parity. Record limitations relevant to this smaller
preview instead of treating unrelated stock features as release blockers.

## Safety and Release Gates

The following are non-negotiable for any release, including a limited one:

1. Real MyST/Sphinx HTML for the currently open file, with clear diagnostics when
  a directive or referenced input cannot be rendered.
2. Live unsaved-buffer rendering with correct latest-version behavior and no writes
  to the user's source document or generated book files.
3. Stable bidirectional block/line source mapping for the active Markdown file,
  with no feedback loops or invented locations for unmappable fragments.
4. Workspace Trust enforcement before starting Sphinx, `just`, Python, or a local
   server. Executable Sphinx configuration and extensions never run untrusted.
5. Restricted preview resources and navigation: bound local roots, safe URI schemes,
   guarded relative paths and symlinks, restrictive CSP, and explicit handling of
   raw HTML, active SVG, event attributes, `srcset`, CSS URLs/imports, fonts, media,
   and hostile or encoded resource paths. Unsafe content must not gain execution
   or arbitrary file access through the preview.

Prove those gates on an ordinary file containing MyST syntax, an unsaved edit,
and a long document in a trusted VS Code window. Check that switching editors
changes the active preview and that a failure retains visibly stale last-good
content. Test trust and hostile-resource cases. Confirm the stock preview remains
unchanged with the extension installed. Do not require `book-serve-multipage` or
other book-wide build recipes as preview prerequisites.

Run focused extension tests and build checks. If Sphinx configuration, hooks, or
book output change, also run `just book-check` and `just preflight`. The existing
book build and publishing workflow must not depend on the VS Code extension.

If a hard gate cannot be met, do not ship the preview as specified. A peripheral
P-item failure may ship as a clearly disclosed limitation without a full-parity
claim; it must not be misreported as a passing acceptance test.

## Later Editing Phase

After the read-only preview, a separate opt-in Obsidian-like mode may render
inactive blocks while exposing the active line as editable Markdown source.
The `TextDocument` remains authoritative; preserve Markdown bytes and VS Code's
undo, save, and multi-view behavior. This phase does not change the default
Markdown editor and is not a first-release gate. Before implementing it, specify
caret/source mapping, IME, paste/drop, undo, synchronization, and accessibility
as a separate interaction contract.

## Decision Record

| Interview decision | Resolution |
| --- | --- |
| Q1 | Treat native rendered-diff Stable API limits as current, subject to a feasibility spike. |
| Q2 | Require stable two-way block/line scroll sync, not pixel precision. |
| Q3 | Defer editing mode until after the read-only preview. |
| Q4 | Use stock preview behavior as guidance, not a full parity gate for this narrowed scope. |
| Q5, Q9 | Require no third-party Markdown-It syntax in the first MyST release. |
| Q6 | Later editor: rendered blocks with the active line shown as Markdown source. |
| Q8 | Keep stock rendered diff; do not build a MyST diff view. |
| Q11 | Superseded by the active-file-only first release; fixed-file mode is deferred. |
| Q12 | Use independent MyST settings with stock-like defaults. |
| Q13, Q15, Q16 | Retain safety, source integrity, real Sphinx, active dirty-buffer rendering, and two-way mapping as hard gates. |

The active-file focus above supersedes earlier book-wide and stock-clone goals.
Runtime feasibility remains to be established, not assumed from this document.
