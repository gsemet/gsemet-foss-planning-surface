# 108 — Dropdown admonitions show their open/closed state

Type: fix · Priority: P1 · From backlog: `02-backlog/P1/bug-dropdown-state`

## Intent (user)

Dropdown:

:::{note} Title
:class: dropdown

Content
:::

This does not show the state (collapsed or expanded)

![image.png](image.png)

Expected => show a > or V icon to the right

## Autonomous decisions

- Decided by the main session on 2026-10-26 under the user's instruction "pas de questions, full autonome". List these in the PR body under "Autonomous decisions".
- A chevron at the right of the title: `>` (pointing right) when collapsed, `v` when expanded, rotating on toggle.
- Default state follows MyST: `:class: dropdown` starts collapsed, `dropdown-open` (if supported) starts expanded.
- Applies to every admonition kind that supports `dropdown`, all themes.
