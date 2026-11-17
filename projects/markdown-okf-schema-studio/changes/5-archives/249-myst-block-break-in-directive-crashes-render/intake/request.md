# 249 — A +++ line inside a container no longer crashes the MyST render

Type: fix · Priority: P2 · Approved by the owner on 2026-11-03 · Worktree
`../markdown-okf-schema-studio-wt-249`, branch `change-requests/249-myst-block-break-in-directive-crashes-render`.
Part of the stacked run of 2026-11-03 (afternoon), before release 1.3.0.

## Intent

See [01-intent.md](../01-intent.md)

## Owner decisions (2026-11-03)

- Inside any container (MyST directive `:::`, quote, list item, alert), a `+++` line renders as text, as GitHub does inside an alert. Only a root-level `+++` stays a block break.
