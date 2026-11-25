Short name: `context-limits`

# Answer 1 (2026-11-25, the owner, in chat)

Question (Chief of Staff): add `context-limits-of-the-drivers-configurab` to batch-31, at its end after `shortcut-commands`, grilled first?

Answer: "Oui, grille-la" (yes, grill it). The grill starts; the destination is confirmed at "grilled enough?".

# Answer 2, context-limits-Q1 (2026-11-25, the owner)

What "200K" is: A, the hand-back threshold at 200,000 with the agents' context window raised above it (for instance 300,000). Nothing proves the model accepts a larger window: the CR measures it first and comes back to the owner when it is impossible. Facts given with the question: the cards hand back at 130,000 (115,000 before the closing); agents with a 200,000 window were compacted near 162,000 (measured, batch-16 and batch-17).

# Answer 3, context-limits-Q2 (2026-11-25, the owner)

Where the thresholds are set: B, as A (the project's `chantier.yaml` and a command that lists each limit with its value and source) and, in addition, editable on the board's Configuration page, Limits tab (recommended was A, without the board).

# Answer 4, context-limits-Q3 (2026-11-25, the owner)

Incoherent settings: A, warn without blocking, in the list and when a batch opens.

# Answer 5, context-limits-Q4 (2026-11-25, the owner)

What the list holds: C, the context limits only (recommended was every limit). Rounds, slots, budget, lease, heartbeat, watcher wake and `specifying.parallel` are out; this narrows the request's "same list".

# Answer 6, context-limits-Q5 (2026-11-25, the owner)

"Grilled enough?": B, specify for the running batch batch-31 (recommended was the next batch), on this restatement:

- The Drivers' hand-back threshold moves to 200,000 tokens and their agents' context window is raised above it (for instance 300,000). The CR measures first that the model accepts that window; if it cannot, it comes back to the owner.
- The thresholds are set in the project's `chantier.yaml` and on the board (Configuration page, Limits tab).
- A command lists the context limits only, each with its value and source.
- Incoherent settings give a warning, in the list and when a batch opens, without blocking.

Defaults the Chief of Staff took, accepted with the restatement: the closing threshold stays 15,000 under the hand-back one (185,000); it applies to the Drivers (CR, stack, QA, release) and to the context thresholds the Foreman applies, the other agents unchanged; `chantier` prints the thresholds to the Drivers and the cards name no figure.

Open: the exact window, set by the trial. The extra cost of a large context is not measured.

Destination: running batch batch-31, after `shortcut-commands`. Spec critic: yes (it changes the Drivers' contract and the board's Configuration page).
