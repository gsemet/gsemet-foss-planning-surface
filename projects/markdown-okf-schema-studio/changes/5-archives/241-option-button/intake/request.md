# 241 — Toggle option button, and Enter continues an option list

Type: feat · Priority: P1 · Approved by the owner on 2026-11-03 · Worktree
`../markdown-okf-schema-studio-wt-241`, branch `change-requests/241-option-button`.
Part of a stacked run.

## Intent

From [01-intent.md](../01-intent.md): option lists `- ( )` have no toolbar button, and Enter does not
prefill the next option.

![Missing toggle and prefill](../evidence/image.png)

## Owner decisions (2026-11-03)

See [02-decisions.md](../02-answers.md):

- A "Toggle option" toolbar button next to "Toggle checkbox": it turns the selected lines into an
  option list `- ( ) `, and back.
- In the block editor, Enter at the end of an option item starts the next line with `- ( ) `. Enter
  on an empty option item ends the list, as for task lists.
- The audit of every syntax in the slash menu and toolbar is a separate backlog item
  (`syntax-coverage-audit`), not this CR.
