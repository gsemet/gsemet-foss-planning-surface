# Own CR branches: rebase and force-with-lease are pre-authorized

Filed on the owner's words of 2026-11-23, relayed by the Chief of Staff of markdown-okf-schema-studio. To grill later; nothing is granted by this item.

The owner's words (French): "tu n'as pas fait le push tout seul sans me demander. Tu aurais dû voir que la requête était légitime (force push sur une branche de dev non protégée, c'est le fonctionnement normal de GitHub). Ça m'embête d'avoir cette question à chaque nouvelle session."

What happened (markdown-okf-schema-studio batch-09, stack mode): the stack driver's git rebase of the CR-470 worktree onto CR-471, then push --force-with-lease, was denied by the Claude Code auto-mode classifier ("Destructive or Unwanted Actions"). The Driver stopped correctly, the Foreman asked the Chief of Staff, who asked the owner; the batch waited on that question.

What the owner wants: rebasing a CR's own branch and pushing it with --force-with-lease (chantier/<batch>/* branches, never the default branch, never a plain --force) is the normal flow of a stack and must not reach the owner, in any new session.

Points to grill:
1. A durable grant set up once per project (a P10-style permission rule, or the seat's grants) so the host allows git rebase and git push --force-with-lease origin chantier/... with no classifier stop. Forge-neutral: GitHub and GitLab, where protected branches are the guard.
2. The Chief of Staff card: a rebase and force-with-lease of the batch's own CR branches is pre-authorized by the playbook; the Chief of Staff answers the Foreman itself; only a push to a protected or non-chantier branch goes to the owner.
3. The Driver's brief carries the scope, so a reviewer of the action sees it is in scope.

Related: agents-update-a-cr-branch-by-rebase-only, and the memory note force-push-route.