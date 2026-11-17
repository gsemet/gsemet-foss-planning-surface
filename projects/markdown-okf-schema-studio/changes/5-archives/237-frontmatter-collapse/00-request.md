# 237 — Collapse and expand the frontmatter properties table

Type: feat · Priority: P1 · Approved by the owner on 2026-11-03 · Worktree
`../markdown-okf-schema-studio-wt-237`, branch `change-requests/237-frontmatter-collapse`.

## Intent

From [01-intent.md](01-intent.md): a button next to the "Frontmatter properties" title collapses
and expands the table.

![Where the button goes](image.png)

## Owner decisions (2026-11-03)

- The button sits in the frontmatter header, next to "Frontmatter properties", with the same icon
  and behaviour as the Description column collapse.
- The state holds while the document stays open: a re-render or an edit keeps the table collapsed.
- On a reload or when a document is opened, the frontmatter is always shown again (unlike the
  Description column, which keeps its setting).

## Owner decision (2026-11-03, after round 1)

- The frontmatter toggle uses a down-pointing arrow (▼ when expanded, collapsing the table
  vertically) instead of the Description column's left-pointing triangle. The Description column
  keeps its own icon.
