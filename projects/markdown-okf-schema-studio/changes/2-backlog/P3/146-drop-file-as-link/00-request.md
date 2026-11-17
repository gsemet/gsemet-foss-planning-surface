# 146 — Dropping a file from the Explorer inserts a link

Type: feat · Priority: P1 · From backlog: `02-backlog/P1/drop-file-as-link`

## Intent (user)

See [01-intent.md](01-intent.md) (moved from the backlog, verbatim).

## Autonomous decisions

- Decided by the main session on 2026-10-27 under the user's instruction "rajoute tout ça dans les requêtes à faire dans une stack … livre-moi tout ça sur la stack en cours, dans des nouvelles PR; s'il y a des changements impactants tu peux t'organiser pour optimiser les livraisons". List these in the PR body under "Autonomous decisions".
- Wiki links are not part of the extension (the user removed that item): a dropped `.md` file always gives a relative Markdown link.

## Why parked (2026-10-28)

- Parked by the owner; PR https://github.com/gsemet/markdown-okf-schema-studio/pull/154 is a draft
  (branch `change-requests/146-drop-file-as-link`, worktree `../markdown-okf-schema-studio-wt-146`,
  both kept).
- The heavy integration failure (image drop inserts after the first gap, run
  https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40656099555) was never
  re-diagnosed. Since then `test/integration/dropFiles.test.ts` restores edit mode at the end.
- To resume: rebase on `origin/main` (after the 4-row toolbar PR #167), re-run heavy CI, diagnose.
