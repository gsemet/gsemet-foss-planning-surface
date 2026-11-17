# Task T1 — Change bar for front matter fields

Worktree `../markdown-okf-schema-studio-wt-155`, branch `change-requests/155-frontmatter-diff-line`.
Find how body blocks get their change bar (diff with HEAD) and why the front matter properties
table is skipped; add per-field bars. Tests first (unit on the diff mapping, visual check light and
dark). SwRS: find the diff-gutter requirement; new behaviour → new SwRS `--lifecycle proposed`.
Docs: the user doc page about the diff bars. Screenshots before/after light+dark.
Gates: `just check`; normal CI; heavy CI dispatched.
