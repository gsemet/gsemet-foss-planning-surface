# The board shows a CR's subject without the "Change Specification:" lead

The user, 2026-11-20: "Dans la board, dans les items de la colonne Subject, je vois que chaque item
commence par "Change Specification: ". ca prend de la place pour rien".

Every CR's title on the board (the PRs page, the home page's PR list, the batch's PR cards) starts
with "Change Specification: ", which takes room and says nothing: every CR has one.

Cause seen: when a CR joins a batch, the record takes its title from the specification's first
heading as written (`# Change Specification: <subject>`), lead included; batch.json, STATUS.json
and STATUS.md carry it, and so do the CR's branch name and the closed batch records. The board
strips the lead in some views (the backlog and the batch's CR list, case-sensitively) and not in
others (the PRs page and the batch's PR list).

Wanted: the CR's subject, plain, everywhere it reaches the user; fixed at the root, where the
record takes the title, with the board's display strip kept as a guard for records already
written.
