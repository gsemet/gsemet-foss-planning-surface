# 117 — Insert figure opens the figure editor right away

Type: fix · Priority: P1 · From backlog: `02-backlog/P1/bug-edit-figure`

## Intent (user)

i click on insert figure

i choose an image

the block looks like this:

![image.png](../evidence/image.png)

I would expect to active directly the edit figure modal



![image-1.png](../evidence/image-1.png)

look other editor for similar behavior

## Autonomous decisions

- Decided by the main session on 2026-10-26 under the user's instruction "pas de questions, full autonome". List these in the PR body under "Autonomous decisions".
- After "Insert figure" and the image choice, the figure edit modal opens immediately, focused on the caption field (as other editors do).
- Cancel in that modal keeps the inserted figure with its default values.
