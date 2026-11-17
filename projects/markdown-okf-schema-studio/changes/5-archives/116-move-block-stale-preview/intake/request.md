# 116 — Move block up/down works instead of reporting a stale preview

Type: fix · Priority: P1 · From backlog: `02-backlog/P1/bug-move-block`

## Intent (user)

When i click to move a block up or down, it does nothing and this message appears:

![image.png](../evidence/image.png)

the e2e should have covered this use case

Expected: no error, and the block is moved 1 up

## Autonomous decisions

- Decided by the main session on 2026-10-26 under the user's instruction "pas de questions, full autonome". List these in the PR body under "Autonomous decisions".
- The error "The preview is out of date. Refresh it and try again." must not appear when the preview is in sync: fix the version check that rejects the move.
- When the preview is really out of date, re-render and retry once automatically before showing any message.
- e2e: move a block up and down in a document with a front matter and headings; the existing e2e missed it, so the test must fail on the current code.
