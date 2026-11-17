# 147 — Changed blocks can show a side-by-side diff with the last commit

Type: feat · Priority: P1 · From backlog: `02-backlog/P1/rich-diff-side-by-side`

## Intent (user)

See [01-intent.md](01-intent.md) (moved from the backlog, verbatim).

## Autonomous decisions

- Decided by the main session on 2026-10-27 under the user's instruction "rajoute tout ça dans les requêtes à faire dans une stack … livre-moi tout ça sur la stack en cours, dans des nouvelles PR; s'il y a des changements impactants tu peux t'organiser pour optimiser les livraisons". List these in the PR body under "Autonomous decisions".
- Largest change, on top of the stack.
- The user's answer about the mode was cut off ("que en mode …"): assumed read mode only (the toggle is disabled in edit mode). Listed as an open question in the PR body.

## Why parked (2026-10-28)

- Parked by the owner; PR https://github.com/gsemet/markdown-okf-schema-studio/pull/155 is a draft
  (branch `change-requests/147-rich-diff-side-by-side`, worktree `../markdown-okf-schema-studio-wt-147`,
  both kept).
- Visual check `myst/v32-conf-warning-banner-narrow-dark-460` fails ("the banner stays clear of
  the floating toolbar").
- Once PR https://github.com/gsemet/markdown-okf-schema-studio/pull/167 merges (floating toolbar in
  4 rows), the Side-by-side button moves into the new row 4 (fold, diff, comment).

## Follow-up after the five-row toolbar (2026-10-28)

When PR #167 (five-row floating toolbar) merges: move this CR's Side-by-side button into row 5,
the comparison row ("section collapse, diff, comment": Fold all sections, Diff, Comments), then
rebase draft #155 and update its toolbar requirements, docs and screenshots accordingly.
