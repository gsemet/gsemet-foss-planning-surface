## Summary

Opening a Markdown file outside a trusted workspace (or in Restricted Mode) showed no way to enter
edit mode and no explanation. The Edit (pencil) button was silently hidden. It now stays visible,
greyed out and disabled, and its tooltip says why: "Editing is unavailable: this file is not in a
trusted workspace" (or "... not in a folder opened in the VS Code workspace" when the file has no
folder). Clicking it does nothing.

## Deliverables

Before (button missing, no hint) and after (greyed button with reason), in a real Restricted Mode
window, cream and dark themes. 

| Before | After |
| --- | --- |
| ![before](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/603e2eafe3448f4ddcefa355f77bb6362e4229c0/before-cream.png) | ![after](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/603e2eafe3448f4ddcefa355f77bb6362e4229c0/after-cream.png) |
| ![before](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/603e2eafe3448f4ddcefa355f77bb6362e4229c0/before-dark.png) | ![after](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/603e2eafe3448f4ddcefa355f77bb6362e4229c0/after-dark.png) |

- The Edit button is the only toolbar control hidden because of trust; it is the only one changed.
- Reason text comes from one new module, `src/core/edits/readOnlyReasons.ts`, used by the toolbar
  and the page runtime.
- Requirements (trust, toolbar, block editing, lifecycle) and the changelog are updated; tests that
  asserted the button was absent now assert it is present and disabled.

## Changes

- `src/core/edits/readOnlyReasons.ts` (new), toolbar and page runtime use it.
- Requirements text and changelog; tests updated.

## Impacts

The toolbar always has 13 buttons; a read-only preview now shows a disabled Edit button.

## Blast radius

1 of 3: one control, only in read-only previews.

## Autonomous decisions

- Only the Edit button needed the change; the Diff toggle and other trust-dependent items were left
  alone after checking the code.
- Tooltip wording has two variants depending on the reason (untrusted vs. no workspace folder).
- `okfreq update-coverage` was not run (the installed version reorders many files); the new file was
  added to the trust requirement's `implemented_in_files` by hand. Run `just requirements-update`
  with a current `okfreq`.

## Test plan

New and changed unit, page-runtime and visual scenarios fail on the old code. Visual groups
toolbar-navigation and trust-security: 43/43. `just check` passes except `requirements-lint`, which
fails locally because the installed `okfreq` lacks `--check-links` (environment issue).

## Internal references

CR 126 (backlog item bug-edit-button-hidden-untrusted).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
