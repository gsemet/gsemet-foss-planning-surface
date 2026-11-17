# 131 — Code blocks: Shiki highlighting, dark background and line numbers

Type: feat · Priority: P1 · From backlog: `02-backlog/P1/code-block-reading-comfort`

## Intent (user)

See [01-intent.md](../01-intent.md) (moved from the backlog, verbatim).

## Autonomous decisions

- Decided by the main session on 2026-10-27 under the user's instruction "lance 4 CR max en parallèle pour fixer tout ça et finaliser une nouvelle stack PR" (same autonomous mode as the previous run). List these in the PR body under "Autonomous decisions".
- The decisions are in the item (user, 2026-10-27). Adding the `shiki` dependency (JavaScript regex engine, no WASM) is allowed by this CR: `npm install` of that package only, lock file committed.
- Settings: `markdownOkfSchemaStudio.preview.codeBlocks.darkBackground` (default true) and `markdownOkfSchemaStudio.preview.codeBlocks.lineNumbers` (default true), `scope: resource`.
- Placed on top of the stack: largest change.
- Driver 2026-10-27: worktree 131 got its own node_modules (unlinked the shared symlink, cloned the main copy, ran `npm install shiki`) because installing through the symlink would have altered the main checkout and the parallel worktrees.
- Coder: colour classes instead of inline styles; DOM lib added to tsconfig (highlight.js was the only source of DOM types); comments no longer italic (Dark+); diff blocks are padded rounded blocks on the dark background.
