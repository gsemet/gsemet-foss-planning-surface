# Intent: `/chantier:chantier init`, a guided tour for a newcomer

The user wants a way to start chantier in a project for someone who knows nothing of it:
`/chantier:chantier init` prepares the project's stage folders and gives a didactic tour of how
the project will work with chantier from now on (the concepts, the words, the mechanics),
adapted to that project, then proposes what to improve so that chantier works well there.

Why: chantier works well only when the project's harness (gates, CI, merge rules, written in
`AGENTS.md`) is in order, and today a newcomer gets ten lines of introduction and nothing that
explains the CR's life, the roles or what they alone decide.

Scope as grilled (see `02-answers.md`): a new card and a one-line entry point, a CLI command
that only creates the five empty stage folders, an HTML template in the plugin. No other CLI
change, no change to the repository's rules for now.
