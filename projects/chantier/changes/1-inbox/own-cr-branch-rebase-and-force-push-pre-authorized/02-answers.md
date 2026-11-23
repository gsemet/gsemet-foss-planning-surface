Short name: `own-branch-push`

1. own-branch-push-Q1: **Branches covered.** B. Any `chantier/*` branch (not only the running batch's `chantier/<batch>/*`); never the default branch, never a protected branch, never a plain `--force`.
2. own-branch-push-Q2: **The durable grant.** A. Local `git rebase` and `git push --force-with-lease origin chantier/*`, named by preflight's P10 and added on the user's yes, once per machine.
3. own-branch-push-Q3: **The Chief of Staff's answer.** A. For a `chantier/<batch>/*` branch the Chief of Staff answers the Foreman itself; only a push to a protected or non-chantier branch goes to the user. (Q1 widened the covered set to `chantier/*`; the answer applies to it.)
4. own-branch-push-Q4: **The Driver's brief.** A. The brief names the action and its scope.
5. own-branch-push-Q5: **Grilled enough.** A. Specify, for the running batch batch-31.

Destination: running batch batch-31.
Spec critic: yes, default model (it changes what a role may do and a permission grant).
6. own-branch-push-Q6: **A host refusal that remains.** A. Today's single question to the user, and the push goes on their yes.
7. own-branch-push-Q7: **A `chantier/*` branch that `handoff` ties to no CR of the batch.** A. A hard refusal with no question to the user, as today.
8. own-branch-push-Q8: **A refused rebase.** A. The steering session runs the same rebase in the Driver's worktree (`git -C <worktree> rebase <base>`), under the same check as a push (the branch tied by `handoff`); on a conflict it hands the work back to a new Driver; the user is asked only if the host refuses the steering session too.
9. own-branch-push-Q9: **A force push of a non-`chantier/*` branch or the default branch.** A. Nothing is pushed; the user is told, as information, which branch was asked and by which CR; a yes does not push it (today's guard stays). This replaces the part of Q3 that sent such a push "to the user" for a push on a yes.
10. own-branch-push-Q10: **Width of the rebase allow rules.** A. Narrow forms that name the base: `git -C * rebase origin/*`, `git -C * rebase --onto chantier/* *`, `git -C * rebase --continue`, `git -C * rebase --abort` (and the plain forms); the cards forbid `--exec`/`-x`; the risk column names what remains.
Critic's other findings, applied without a question: the effect on the classifier is marked unproved with a trial named, and the Driver's line is worded "chantier's normal flow, pre-authorized by the playbook" (no user, no date); CR-465 is the base to rebase onto and its rebase forms are checked against the chosen rules; the two passages that still say "asked only when the host refuses you too" (`chief-of-staff.md` direct mode, the start alert in `hosts/claude-code.md`) are updated and name the rebase; the GitLab protected-branch rejection text is marked unproved.
