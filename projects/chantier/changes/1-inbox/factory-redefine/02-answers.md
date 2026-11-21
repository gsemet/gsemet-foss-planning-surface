Short name: `factory`

# Answers

1. factory-Q1 (2026-11-21): **What "factory" means.** It is not a batch mode. The user's words: "En fait c'est pas un mode du batch. C'est un mode du planning avant. En mode normal, on grille et quand c'est prêt par défaut on prépare le prochain batch. Il y a juste l'option en plus d'envoyer directement au batch en cours s'il y a un batch en cours. C'est donc pas un mode spécial, c'est juste que quand une CR est suffisamment grillée, au moment de lancer le spec writer il faut demander si c'est à rajouter au batch en cours (donc vers pending) ou pour le prochain (ready)." In English: no special mode; when a CR is grilled enough, at the spec-writer's start, the user is asked whether it joins the running batch (`4-batch/1-pending/`) or the next one (`3-ready`); by default it prepares the next batch.
2. factory-Q2 (2026-11-21): **The go.** A. Placing a CR in `1-pending` is the go, in every mode: a Driver takes it when a slot frees.
3. factory-Q3 (2026-11-21): **Where the user chooses.** A. On the board (the backlog page's last column split in two, always) and in the grill (the "grilled enough?" question offers both).
4. factory-Q4 (2026-11-21): **With no open batch.** The CR goes to `3-ready` ("S'il n'y a pas de batch ouvert la CR va en ready.").
5. factory-Q5 (2026-11-21): **A batch's last CR.** A. The batch pauses, then the retro and the close offer, as an ordinary batch; until the user's close, it stays the running batch, and a CR placed in `1-pending` starts it again.
6. factory-Q6 (2026-11-21): **The old commands.** A. `open --factory` and `order factory on/off` are removed; old records with `factory: on` stay readable.
7. factory-Q7 (2026-11-21): **When the CR reaches `1-pending`.** A. When its specification is final (after the critic, when it runs); until then it waits in its folder, marked for the running batch.
8. factory-Q8 (2026-11-21): **Grilled enough.** A. Yes, specify now.
Spec critic: yes, it changes the grill's rules, the board, the CLI (removed commands) and how a CR joins a batch.
