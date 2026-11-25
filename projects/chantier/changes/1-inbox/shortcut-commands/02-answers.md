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
