# CR 026 — change bar spacing, TOC accent corners, commit guidelines move (2026-10-22)

Original intent: `01-intent.md` (backlog P3/bug-changed-files-too-close) + user request: move
`.github/guidelines/git-commit-allowed-scopes.md` and `git-commit-message.guidelines.md` to
`.agents/guidelines/` (update AGENTS.md) in the same PR, in an isolated worktree.

## Decisions (user, 2026-10-22)

- Change bar (incoming-change mark, `[data-sphinx-preview-changed]`, previewStyles.ts ~2508): draw
  it in the left margin ~12px from the text; the text must not move ("nothing moves").
- Rounded corners: ONLY left accent borders with rounded corners are unwanted ("typique de l'IA").
  Buttons and text boxes keep their rounding. Scan result (orchestrator, computed styles on the 79
  visual pages + source): the only case is the TOC current item
  (`nav[data-sphinx-preview-toc] li[data-sphinx-preview-toc-current] > button`, inset 3px bar +
  4px radius from `li button`). Inline code (no accent bar) stays as is.
- "Alignment on several text is not perfect": ignore.
- Guidelines move: update `guidelines.lock.json` target paths (and guidelines.yml if relevant) so
  `guidelines update` writes to `.agents/guidelines`.

## Decision update (user, 2026-10-22, supersedes the "~12px from the text" rule)

Screenshots: `change-bar-rounded-in-code.png`, `change-bar-target-column.png` (red line = target).

- The change bar on a code block (and any block with border-radius) is drawn with rounded ends
  because the inset shadow follows the block's radius: the bar must have square ends everywhere.
- ALL change bars sit in ONE column, aligned as close as possible to the page's left margin (the
  red line), whatever the block's indentation (list items, nested blocks, code blocks, headings
  all get their bar at the same x). The text never moves. The bar spans the block's full height.
