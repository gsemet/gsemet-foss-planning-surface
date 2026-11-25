Short name: `shortcuts`

# Answer 1 (2026-11-25, the owner, in chat)

Question: which of the two commands the research proposed (`work/research-commands.md`) join the request: both, `autonomy` only, or none?

Answer: "Les deux" (both). The request now also holds `/chantier:autonomy` and `batch-add`. The Chief of Staff's proposal in that question, to merge `batch-add` and grill-to-pending into one command with a `--grill` option, was part of the "both" choice: to confirm in the grill.

# Answer 2, shortcuts-Q1 (2026-11-25, the owner)

When: B, at the end of batch-31, after CR-514 (recommended was the next batch).

# Answer 3, shortcuts-Q2 (2026-11-25, the owner)

`/chantier:batch-start <shape>`: B, it starts at once. Typing the command is the go; the plan is shown after (recommended was to wait for the go).

# Answer 4, shortcuts-Q3 (2026-11-25, the owner)

Merging grill-to-pending and batch-add: no option taken. "j ai du mal a comprendre, trouve un fonctionnement simple et efficace" (hard to follow; find a simple and efficient way). Re-asked as shortcuts-Q5.

# Answer 5, shortcuts-Q4 (2026-11-25, the owner)

`/chantier:autonomy`, a question that comes up: A, decide it with the recommendation, record it "to confirm by the owner", and go on. It never merges, releases or deletes without the owner.

# Answer 6, shortcuts-Q5 (2026-11-25, the owner)

A: one command, `/chantier:batch-add`, followed by anything, with no option. An existing CR (number or name) is added; any other text becomes a new CR. In both cases it asks the missing questions, writes the specification and puts the CR in the running batch. There is no `grill-to-pending` command. Replaces the "Open" part of Answer 1.

# Answer 7, shortcuts-Q6 (2026-11-25, the owner)

`batch-start` typed with no budget: A, it asks for the budget, then starts as soon as it has the answer.

# Answer 8, shortcuts-Q7 (2026-11-25, the owner)

`/chantier:batch-close`: A, it shows the outcome and asks "close?" before closing.

# Answer 9, shortcuts-Q8 (2026-11-25, the owner)

Release: B, none in these commands; the owner asks for a release apart (recommended was `batch-close --release`).

# Answer 10, shortcuts-Q9 (2026-11-25, the owner)

"Assez grillé" (grilled enough), on this restatement:

- `/chantier:batch-start stack|parallel|series`: starts at once, no go, the plan shown after; with no budget it asks for one first.
- `/chantier:batch-pause`: pauses the batch.
- `/chantier:batch-close`: shows the outcome, then asks "close?"; no release.
- `/chantier:batch-add <CR or request>`: adds an existing CR or files the request, asks the missing questions, writes the specification, puts the CR in the running batch; no `grill-to-pending`.
- `/chantier:autonomy`: names before the owner leaves what would block, then goes on alone; questions are decided with the recommendation and recorded "to confirm by the owner"; never a merge, release or deletion without the owner.

Defaults the Chief of Staff took, accepted with the restatement: `batch-start` takes the `3-ready` CRs, asks the shape when it is missing, and stops when a preflight check fails; `batch-add` with no running batch leaves the CR in `3-ready` and says so; `autonomy` accepts a budget and a number of rounds; the commands exist on Claude Code and Copilot.

When: at the end of batch-31, after CR-514; the local Windows long gate then moves to it.

Destination: running batch batch-31. (From Answers 2 and 10: specified, then added with `order add` and chained after CR-514.) Spec critic: yes (the Chief of Staff judges the CR impactful: it removes the go before a batch starts and adds an unattended mode).

# Answer 11, shortcuts-Q10 (2026-11-25, the owner)

Split: B, two CRs: this one keeps the four batch commands (`batch-start`, `batch-pause`, `batch-close`, `batch-add`) and the shared base; `/chantier:autonomy` becomes its own CR, after this one (recommended was three CRs).

# Answer 12, shortcuts-Q11 (2026-11-25, the owner)

`/chantier:batch-pause`: no option taken. "je ne comprend pas. c est simple, quand un batch touche, batch-pause met en pause, quand le batch est en pause il ne fait rien. pour reprendre on fait un batch-start qui resume le batch paused". Read by the Chief of Staff ("touche" as "tourne"): on a running batch, `batch-pause` pauses it; a paused batch does nothing; `/chantier:batch-start` resumes a paused batch. Replaces open question 1 of the specification, and its rule that `batch-start` starts nothing on a paused batch. Still open: what the Drivers at work do at the pause (asked next).

# Answer 13, shortcuts-Q12 (2026-11-25, the owner)

`/chantier:batch-add P1` (or `ready`, `inbox`): B, list the folder's CRs and ask which, once (recommended was to add the whole folder).

# Answer 14, shortcuts-Q13 (2026-11-25, the owner)

The commands and the board pane: A, record the Chief of Staff role, open no pane.

# Answer 15, shortcuts-Q14 (2026-11-25, the owner)

At the pause, the work already running: A, it finishes, nothing else starts. Settles the open point of Answer 12.

# Answer 16, shortcuts-Q15 (2026-11-25, the owner)

`batch-start` with a missing Claude Code permission rule: A, ask before starting, in one question with the budget when it is missing, then start.

# Answer 17, shortcuts-Q16 (2026-11-25, the owner)

`batch-add`: A, it asks "grilled enough?" before the specification is written (no destination options, the command gave it). Settles open question 2 of the specification.

# Answer 18, shortcuts-Q17 (2026-11-25, the owner)

Waits between CRs that change the same lines, with `batch-start`: A, proposed after the start, recorded on the owner's yes. Settles open question 4 of the specification.

# Answer 19, shortcuts-Q18 (2026-11-25, the owner)

`batch-add` typed in a Griller session: A, the Griller grills and specifies the CR, and the Chief of Staff adds it to the batch. Settles open question 5 of the specification.

# Decision 20 (2026-11-25, the owner, in chat)

"tu vas te concentrer sur livrer les CR 507 a 514 sur le rework. tu vas annuler les specs de tous les autres mais eviement pas perdre les reponses que j avais donnee en interview. Avec le rework en cours il faudra refaire la specification de tout, et on fera ca dans un batch 32."

This CR does not join batch-31. Its specification is to be written again after the rework, from these answers, for batch-32. The rewrite under way for Answers 11 to 19 was stopped.

Destination: none for now; to specify again for batch-32. Replaces the earlier destination.
