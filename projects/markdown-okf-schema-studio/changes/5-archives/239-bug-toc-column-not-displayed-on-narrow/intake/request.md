# 239 — The TOC shows on a narrow viewport, as a rail that expands

Type: fix · Priority: P1 · Approved by the owner on 2026-11-03 · Worktree
`../markdown-okf-schema-studio-wt-239`, branch `change-requests/239-bug-toc-column-not-displayed-on-narrow`.
Part of a stacked run.

## Intent

From [01-intent.md](../01-intent.md): on a narrow viewport the TOC column is hidden although its
toolbar toggle is on.

![TOC hidden despite the toggle](../evidence/image.png)

## Owner decisions (2026-11-03)

See [02-decisions.md](../02-answers.md):

- With the TOC toggle on and a narrow viewport: a thin rail on the right, one tick per heading, the
  reader's position highlighted.
- Hover or keyboard focus on the rail opens the TOC as an overlay above the text. It closes 300 ms
  after the pointer leaves, or on Escape. A click on a tick goes to that heading.
- Wide viewports keep today's TOC column.
