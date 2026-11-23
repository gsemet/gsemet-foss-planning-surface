Short name: `rebase-only`

1. rebase-only-Q1: **What the CLI does with a merge commit in a CR branch.** Not a flat ban. The user's words: "C'est un peu plus compliqué qu'une interdiction. Si le projet cible ne veut pas de rebase auto il faut respecter, mais dans une stack on ne fait jamais de commit de merge." So: the default is rebase only; a project whose own rules want another way is respected (project rules rank above the cards); in a stack, never a merge commit, with no exception. How a project says it, and what `ship` does, is asked in rebase-only-Q4.
2. rebase-only-Q2: **A branch that already holds a merge commit.** A. The Driver removes it itself by a rebase, then a protected force-push of the chantier branch.
3. rebase-only-Q3: **A stack's CR updated on the CR below.** A. Yes, rebase only, on the CR below too.
4. rebase-only-Q4: **How a project asks for another method.** Simplified, no project key for now. The user's words: "Pour l'instant on va simplifier: dans le PR que livre Chantier, jamais de merge commit, si ça arrive on rebase." So: in the PRs chantier delivers there is never a merge commit, with no project exception; when one appears, the branch is rebased. This replaces the exception part of Q1.
5. rebase-only-Q5: **The CLI's check.** A. `ship` refuses a branch that holds a merge commit and says to rebase.
6. rebase-only-Q6: **Grilled enough.** A. Specify, for the running batch batch-31 (4-batch/1-pending/).

Destination: running batch batch-31.
Spec critic: yes, default model (it changes a CLI refusal and the roles' cards).
