# Own CR branches: rebase and force-with-lease are pre-authorized

Short name: `own-branch-push`. Owner's words of 2026-11-23, relayed from markdown-okf-schema-studio (batch-09, stack mode).

The rebase of a CR's own branch and its push with `--force-with-lease` (any `chantier/*` branch, never the default branch, never a protected branch, never a plain `--force`) is the normal flow of a stack and must not reach the owner, in any new session. Three parts: (1) a durable grant, once per machine: preflight's P10 names the rules for the local `git rebase` and `git push --force-with-lease origin chantier/*` and the Chief of Staff adds them on the user's yes; (2) the Chief of Staff's card: it answers a Foreman's refusal of such a push itself, and only a push to a protected or non-chantier branch goes to the user; (3) the Driver's brief names the action and its scope, so the host's classifier sees it is in scope. Forge-neutral (GitHub and GitLab).

Why: the stack driver's rebase and force-with-lease were denied by the host's auto-mode classifier; the question climbed Driver, Foreman, Chief of Staff, owner, and the batch waited on it.
