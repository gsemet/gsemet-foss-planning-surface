Short name: `rebase-only`

1. rebase-only-Q1: **What the CLI does with a merge commit in a CR branch.** Not a flat ban. The user's words: "C'est un peu plus compliqué qu'une interdiction. Si le projet cible ne veut pas de rebase auto il faut respecter, mais dans une stack on ne fait jamais de commit de merge." So: the default is rebase only; a project whose own rules want another way is respected (project rules rank above the cards); in a stack, never a merge commit, with no exception. How a project says it, and what `ship` does, is asked in rebase-only-Q4.
2. rebase-only-Q2: **A branch that already holds a merge commit.** A. The Driver removes it itself by a rebase, then a protected force-push of the chantier branch.
3. rebase-only-Q3: **A stack's CR updated on the CR below.** A. Yes, rebase only, on the CR below too.
4. rebase-only-Q4: **How a project asks for another method.** Simplified, no project key for now. The user's words: "Pour l'instant on va simplifier: dans le PR que livre Chantier, jamais de merge commit, si ça arrive on rebase." So: in the PRs chantier delivers there is never a merge commit, with no project exception; when one appears, the branch is rebased. This replaces the exception part of Q1.
5. rebase-only-Q5: **The CLI's check.** A. `ship` refuses a branch that holds a merge commit and says to rebase.
6. rebase-only-Q6: **Grilled enough.** A. Specify, for the running batch batch-31 (4-batch/1-pending/).

Destination: running batch batch-31.
Spec critic: yes, default model (it changes a CLI refusal and the roles' cards).
7. rebase-only-Q7: **A GitLab fold.** A. The folded CR's Driver rebases its branch onto its base, which linearizes the fold, then pushes with `--force-with-lease`, ships and judges again; the `folded:` procedure in `driver.md` says so.
8. rebase-only-Q8: **The forge's rebase action.** A. The agents' means is the local rebase plus `--force-with-lease`; the forge's rebase action is allowed but marked unproved, with a trial named, and its commands are not stated as fact.
Critic's other findings, applied without a question: the new check runs `git rev-list --merges` with `check=True` (a git failure is the unreadable-base refusal, `_merges` is not reused as it stands); the unit test adds the fallback lower bound and the unreadable-base cases; the scenario line goes in the `ship` item of `scenario/README.md` (near line 109).
