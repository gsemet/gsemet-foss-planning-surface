# Implementer rules (every task, every round)

- Repo /Users/az02065/Projects/DevTools/markdown-okf-schema-studio, branch dev/gsemet. Re-read the
  current code: the brief's line numbers are hints only (many tasks changed scrollSync.ts).
- Do not commit, push, stash, or change branches. Do not run `just dev`, `just update`, `npm ci`,
  `npm install`, `uv sync`, `fnm install`, pip, or anything that installs or downloads (no network).
- Only touch files the task needs. Never touch `.agents/changes/` except to write your report.
- README.md and CHANGELOG.md hold the USER'S OWN uncommitted edits (CHANGELOG: the T22 link bullet
  wrapped in `<!-- TODO: read back); ... -->`). README.md holds ("Linked-File Annotations" heading level, the
  reworded sentence under it, a `<!-- TODO: add frontmatter example here -->` line). Never revert,
  reformat or rewrite them; DO add your own lines (README feature list, CHANGELOG bullet) without
  touching theirs.
- New webview→host messages go through the registry in src/preview/previewMessages.ts; handlers
  that write files or edit documents refuse readOnly and untrusted previews themselves.
- Style through the stylesheet or CSSOM only, never inline `style=`. Keep the page shell identical
  across renders (runtime UI is built by the page script).
- Shortcuts: Cmd on macOS, Ctrl elsewhere (`isApplePlatform()` in editActions.ts), match `key` before
  `code`. Palette controls cancel mousedown; the T22 blur relaxation keeps focus moves inside the
  editor frame from saving. Opening/closing UI above the text box keeps the text in place
  (shared palette scroll-shift helper; residual ≤ 2 px).
- Never widen or weaken an existing test (width, tolerance, count) to make it pass. If an existing
  test fails, fix the product, or explain why the test is wrong and how you kept its intent. Write
  new tests first and record their failure on the unchanged code when practical.
- Before each VS Code test run check nothing else runs: `ps aux | grep -E "run-tests|extensionDevelopmentPath"`.
  Run the gates in the FOREGROUND, wait for them, and leave nothing running (check ps at the end).
  If a keyboard-injection suite or a scroll scenario fails only on a timing timeout, re-run it once
  and report both results; every other failure must be fixed.
- Report `reports/<Txx>-r<round>.md`: files changed/added (exact paths), what you did, tests added
  and whether they failed before, existing assertions changed and why, gate results (counts),
  deviations, open points, manual checks for the user, screenshot paths for UI changes.
  Reply with a 5-line summary.

## Update 2026-10-21 (U27)

The user's former uncommitted README/CHANGELOG edits are committed (88ce48c). The tree is clean
at task start; README/CHANGELOG diffs must contain only the task's lines. Gate levels: when the
screen is locked use TL / FL (keyboard and undo suites skipped: checkboxToggle, realInput,
labelRename, blockMove) and record them pending-unlock.
