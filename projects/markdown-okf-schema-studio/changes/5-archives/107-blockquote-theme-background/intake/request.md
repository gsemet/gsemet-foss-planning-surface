# 107 — Blockquotes get a theme-tinted background

Type: fix · Priority: P1 · From backlog: `02-backlog/P1/bug-background-quote`

## Intent (user)

Look how quote block is rendered, especially the background

![image-1.png](../evidence/image-1.png)

this:

> toto
>
> tata

Should be rendered in cream background (on cream theme). Adapt on other theme.

## Autonomous decisions

- Decided by the main session on 2026-10-26 under the user's instruction "pas de questions, full autonome". List these in the PR body under "Autonomous decisions".
- Cream theme: blockquotes get a cream background a step darker than the page, with the existing left rule.
- Every other theme gets the equivalent tint from its own tokens (one CSS variable per theme), checked in light and dark.
- Before/after screenshots of the cream theme and one dark theme in the PR.
