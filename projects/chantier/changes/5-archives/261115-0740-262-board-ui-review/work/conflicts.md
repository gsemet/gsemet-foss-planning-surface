# Conflicts: CR-262 rebased onto CR-255's branch (head c5e2498)

Rebase stopped at 93a67aa (1 of 2); 63a6138 applied without conflict.

## docs/web-board.md, Kanban paragraph
Choice: this CR's seven-column paragraph (Inbox, Backlog, Grill, 3-ready, In progress, Handed back, Done; priority tag and filter), plus CR-261's sentence on a working CR's step, "waits for the user" and the "next to start" tag, inserted before "A click opens the folder."

## kanban-cards.js, imports and helpers
HEAD (CR-261) had `import { nextTag, stateColor, stateTag, tag }` plus local `count`/`files`; this CR moved `files` to ui/item-card.js. Choice: import `nextTag, stateColor, stateTag` (no `tag`, now unused here), drop the local helpers; CR-261's `nextTag(c)` in the CR card is kept.

## Note
My first `git rebase --continue` committed the docs file with its markers still in (my edit missed on CRLF). Fixed in a follow-up commit, "fix(docs): web-board kanban paragraph keeps both ...". No markers remain (git grep).

## Fast gate
`just check` in the worktree: passed (ruff format/check, mypy, uv lock --check, biome, pytest 134 passed, release-notes check).
