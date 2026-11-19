# bug: the watcher says a native forge stack's merges did not land

Seen at batch-28's end (2026-11-19, 09:30Z). The user merged GitHub forge stack #355 up to #354
in one go: all 14 PRs were merged, and all 18 commits landed on `main` (checked with
`git log 7ee43d0d..origin/main`).

The watcher (`chantier watch --after 12`) printed, for every PR but the bottom one (#335):

    forge saw merged: CR-370 .../pull/342 into CR-369's branch ...; for the Chief of Staff:
    not landed, tell the user, record nothing until CR-369 lands

GitHub reports each stacked PR as merged into the branch below it, while a native stack merge
lands the whole stack on `main`. Following the line would have held 13 merges unrecorded.

Change: when a PR of a native forge stack is merged into a branch below it, and the stack's
bottom PR is merged into main in the same merge (or its commits are on main), the watcher says
`order merged <cr>` as for the bottom one. A test on a prepared forge journal covers it.
