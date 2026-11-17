# 110 — Readable comment threads and a configurable author name

Type: fix · Priority: P1 · From backlog: `02-backlog/P1/bug-comment-thread-readability`

## Intent (user)

# Readability of the comment thread

look:

![image.png](image.png)

not easy to read (gray on creme background). Review on all themes.

Also, where the name comes from ? => allow setting it through a settings, overwritable in Workspace or project in vscode.

## Autonomous decisions

- Decided by the main session on 2026-10-26 under the user's instruction "pas de questions, full autonome". List these in the PR body under "Autonomous decisions".
- Comment text, author and date reach WCAG AA contrast (4.5:1 for text) on every theme; audited theme by theme with a contrast test.
- New setting for the comment author name, `scope: resource` so it can be set per user, workspace or folder. Default: keep the current source (document it in the setting description and in the docs).
- Name the setting after the existing settings prefix in package.json.
