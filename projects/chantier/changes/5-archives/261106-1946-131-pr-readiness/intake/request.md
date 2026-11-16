# A PR or MR says on the forge when it is not ready to merge

The user, after merging PR 57 into CR-123's branch instead of main (the same accident as PR 55):
"il faudrait que tu mettes les PR en draft tant qu'elles sont pas mergeable par exemple. Encode ca
dans les instructions sur github ou gitlab. Attention, les regles du projets peuvent donner des
instructions autres, comme mettre des labels etc. ne supute rien, mais trouve une maniere de
m'indiquer quand les PR et MR ne sont pas prete a etre mergé sur Github ou Gitlab"

What is asked:

- On GitHub and GitLab, the user sees on the forge itself when a PR or MR must not be merged yet.
  Draft is the user's example, not the only way.
- The project's rules rank first: a project may ask for a label or something else. Assume nothing;
  read them.

Known today:

- `skills/chantier/references/driver.md` line 31 opens the PR with `gh pr create` or
  `glab mr create` and says nothing of a draft; no card mentions a draft PR.
- PR 55 and PR 57 were both green and mergeable, with a base that was another CR's branch. A forge
  says nothing against that merge, so CI and `mergeable` do not cover the case.

To settle in the grill:

- What "not ready" means: a base other than main, red CI, a CR not yet handed back, others.
- Who turns a PR ready, and when: the Driver, the stack's driver, or the Foreman; after a lower PR
  merges, a PR's base changes and it may turn ready.
- A forge or plan without drafts, and what a project rule replaces.
- Whether the Chief of Staff's report says it too.
