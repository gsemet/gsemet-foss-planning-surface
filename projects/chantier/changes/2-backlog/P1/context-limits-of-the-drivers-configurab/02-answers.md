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

# Answer 7, context-limits-Q6 (2026-11-25, the owner)

Asked: what to deliver if a Driver's window cannot be raised. Answer: "arrete on fera ca plus tard" (stop, we will do this later). The Chief of Staff reads it as: the whole CR is left aside. It does not join batch-31. Replaces the destination of Answer 6 and the "yes" of Answer 1.

context-limits-Q7 (release and QA Drivers) and context-limits-Q8 (when a threshold change applies) got no answer: still open, to ask again when the CR is taken up.

State of the specification: written, critic run once (8 findings), the 6 fixes applied; findings 1 (Q6) and 3 (Q7) and open question 1 (Q8) are not folded.

Destination: none for now, left aside by the owner. No `order add` without a new word from the owner.

# Decision 8 (2026-11-25, the owner, in chat)

"tu vas te concentrer sur livrer les CR 507 a 514 sur le rework. tu vas annuler les specs de tous les autres mais eviement pas perdre les reponses que j avais donnee en interview. Avec le rework en cours il faudra refaire la specification de tout, et on fera ca dans un batch 32."

The specification is to be written again after the rework, from these answers, for batch-32.

Destination: none for now; to specify again for batch-32.

The cancelled specification is kept for reference in `work/spec-before-rework.md`.

# Decision 9 (2026-11-25, the owner, in chat)

Asked (Chief of Staff): "Je passe en ready les 10 CR à respécifier, pour batch-32 ?" Answer: "Oui, les 10".

Not automatable: the request is not its specification. The Chief of Staff told the owner that the specification stays to be written before the launch: write it from these answers before any batch takes this CR; context-limits-Q6, Q7 and Q8 stay open.

Destination: next batch (3-ready), batch-32. Replaces the earlier destination.

# Answer 10, context-limits-Q9 (2026-11-27, the owner, in chat)

Asked (Chief of Staff), after the owner saw a Driver of batch-32 hand back for its context: take this CR up again now, for batch-32 (recommended), or later?

Answer, verbatim: "context-limits-of-the-drivers-configurab => laisse les drivers s'autocompacter, cette limite c'est pour tuer un driver qui n'a pas d'autocompact, donc il faudrait plutot le mettre a 500K. c'est vraiment pour éviter des driver qui monte au million de context sans control. il faudra bien expliquer que c'est pour les cas ou le autocompact est mal configuré. Il doit y avoir un settings qui permette de placer un autocompact autour de 400K par defaut (remonte par rapport a 200K, c'est trop peu), et que ce soit configurable par l'utilisateur.

doncil y a 2 chose: config autocompact qui depend du harnais, certains ne permettant pas cet autocompact, et de l'autre le max context pour tuer le driver quand il depasse 500K (pareil, configurable). laisse ca en P1"

What it asks, two separate settings:

- Autocompact: the Drivers are left to compact themselves. A setting places the autocompact around 400,000 tokens by default (200,000 is too low), configurable by the user. It depends on the host; some hosts do not allow it.
- Maximum context: the Driver's context limit is a safety net that ends a Driver passing it, default 500,000 tokens, configurable by the user. It exists so that no Driver climbs to a million tokens with no control. The text must say clearly that it is for a missing or badly configured autocompact.

Replaces: the 200,000 hand-back threshold and the window "for instance 300,000" of Answers 2 and 6.

Not named by the owner, so Answers 3 to 5 stand (settings in `chantier.yaml` and on the board's Limits tab, warn without blocking, a list of the context limits only).

Open, for the next grill or the specification:

- the closing hand-off at 115,000 tokens, not named;
- who ends a Driver past the maximum: itself (today's hand-back) or the steering session;
- context-limits-Q7 (release and QA Drivers) and context-limits-Q8 (when a threshold change applies);
- not measured: whether the agents' model and host accept a window of 400,000;
- not proved: that a compacted Driver reads its rules again (the host row `reload-after-compact` says the plugin's mod leaves a subagent's compaction alone).

Measured in batch-32 on 2026-11-27, from the Driver and worker transcripts: CR-515's Driver handed back at about 133,000 tokens and CR-522's closing hand-off came at about 116,000, neither having compacted; workers compacted between about 166,000 and 175,000 and went on.

Destination: backlog, P1 ("laisse ca en P1"); not batch-32. Replaces the destination of Decision 9.
