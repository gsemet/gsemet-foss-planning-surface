# 109 — Front-matter table keeps keys on one line

Type: fix · Priority: P1 · From backlog: `02-backlog/P1/bug-squized-frontmatter`

## Intent (user)

Image only. In the front-matter properties table the key column is so narrow that keys wrap letter by letter ("na/me", "des/cri/pti/on", "me/tad/ata"). Expected: the key column wide enough for its keys.

![image.png](../evidence/image.png)

## Autonomous decisions

- Decided by the main session on 2026-10-26 under the user's instruction "pas de questions, full autonome". List these in the PR body under "Autonomous decisions".
- The key column never wraps inside a word: `white-space: nowrap` and a width fitted to the longest key, capped at 40% of the table; longer keys ellipsize with the full key as tooltip.
- The value column takes the remaining width and wraps normally.
