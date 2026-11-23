Short name: `rebase-only`

1. rebase-only-Q1: **What the CLI does with a merge commit in a CR branch.** Not a flat ban. The user's words: "C'est un peu plus compliqué qu'une interdiction. Si le projet cible ne veut pas de rebase auto il faut respecter, mais dans une stack on ne fait jamais de commit de merge." So: the default is rebase only; a project whose own rules want another way is respected (project rules rank above the cards); in a stack, never a merge commit, with no exception. How a project says it, and what `ship` does, is asked in rebase-only-Q4.
2. rebase-only-Q2: **A branch that already holds a merge commit.** A. The Driver removes it itself by a rebase, then a protected force-push of the chantier branch.
3. rebase-only-Q3: **A stack's CR updated on the CR below.** A. Yes, rebase only, on the CR below too.
