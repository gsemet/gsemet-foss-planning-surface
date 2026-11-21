Short name: `factory`

# Answers

1. factory-Q1 (2026-11-21): **What "factory" means.** It is not a batch mode. The user's words: "En fait c'est pas un mode du batch. C'est un mode du planning avant. En mode normal, on grille et quand c'est prêt par défaut on prépare le prochain batch. Il y a juste l'option en plus d'envoyer directement au batch en cours s'il y a un batch en cours. C'est donc pas un mode spécial, c'est juste que quand une CR est suffisamment grillée, au moment de lancer le spec writer il faut demander si c'est à rajouter au batch en cours (donc vers pending) ou pour le prochain (ready)." In English: no special mode; when a CR is grilled enough, at the spec-writer's start, the user is asked whether it joins the running batch (`4-batch/1-pending/`) or the next one (`3-ready`); by default it prepares the next batch.
2. factory-Q2 (2026-11-21): **The go.** A. Placing a CR in `1-pending` is the go, in every mode: a Driver takes it when a slot frees.
3. factory-Q3 (2026-11-21): **Where the user chooses.** A. On the board (the backlog page's last column split in two, always) and in the grill (the "grilled enough?" question offers both).
4. factory-Q4 (2026-11-21): **With no open batch.** The CR goes to `3-ready` ("S'il n'y a pas de batch ouvert la CR va en ready.").
