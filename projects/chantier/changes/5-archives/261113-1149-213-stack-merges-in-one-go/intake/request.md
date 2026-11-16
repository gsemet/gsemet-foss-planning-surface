Stack mode means a stack the user merges in one go. Batch-15: the stack driver left every PR above the bottom one as a draft, to be merged bottom-up with a restack after each merge, so the user saw 15 drafts and no stack. Fix the stack driver's card, the Foreman's and the Chief of Staff's checks, the docs and the SVGs so that 'stack ready' means mergeable in one action, with the release commit last on main.

## 2026-11-13, the user's words to the Chief of Staff

- "Le mode 'pile mergeable d'un coup' c'est le mode 'stack'."
- "Je veux une stack prête à merger d'un coup. Je t'ai donné un objectif clair et ça devrait être
  dans les instructions du stack driver et toi tu devrais le vérifier. Tu as aussi le foreman."
- "Je ne veux pas que tu crées de mémoire, je veux que tu encodes les bonnes instructions dans
  Chantier et ses skills."
- "Quand une stack est demandée tu peux recommander d'installer l'extension, si c'est refusé tu
  peux te rabattre sur une commande de ton CLI qui va faire la même chose avec l'API."

Restated:

- A stack on GitHub is a native stack (stacked pull requests, generally available 2026-10-06):
  the PRs grouped bottom to top, merged in one action from the top PR. A chain of PRs based on
  each other is not a stack.
- When the user asks for a stack, the Chief of Staff recommends installing the `gh stack`
  extension (github/gh-stack). If the user declines, the stack is made by a new `$CHANTIER`
  command that calls the REST API (`POST /repos/{owner}/{repo}/stacks` with `pull_requests[]`,
  bottom to top). This is the user's named choice, not a silent fallback.
- The stack driver creates the stack once every PR is ready; the Foreman and the Chief of Staff
  verify it on the forge (`GET .../stacks/{number}`: open, every PR in order, none a draft, the
  release PR on top) before they call it ready.
- Batch-15 measured the cost of doing it without the command: a whole morning of the user's
  back and forth, the stack made by hand with `gh api` (stack #155).
- Open for the grill: GitLab's equivalent; whether the preflight checks for the extension.

## 2026-11-13, later: into batch-15, and a new use case

- "Je veux que tu fasses cette modification dans le batch en cours en l'insérant juste avant la
  PR de release en mettant à jour bien sûr la release notes. Mets cette PR de release en draft
  pour empêcher son merge. Je veux que tu encodes ce use case 'insertion d'un commit sur une
  stack prête', en disant bien de mettre en draft le ou les PR qui seront au-dessus."

Restated:

- This CR joins batch-15 (`order add`), its PR inserted in stack #155 just below the release PR
  154, which the Chief of Staff has put back to draft (done 2026-11-13). The release CR-212
  updates its release notes to name this change.
- New use case, encoded in the cards (stack driver, Foreman, Chief of Staff), the docs and the
  SVGs: **inserting a change into a ready stack.** Before anything else, every PR that will sit
  above the inserted one goes back to draft, so the user cannot merge the stack while it is
  being changed. The new PR is inserted at the place named, the PRs above are restacked on it,
  the stack is updated on the forge (re-created if the forge cannot insert), every PR is
  verified again, and only then do the PRs above go back to ready. The release PR, when there
  is one, stays on top and updates its release notes.
- Scope of this CR, decided: the native stack (extension recommended, `$CHANTIER` command over
  the REST API when the user declines it, GitHub only; GitLab is a later CR), the definition of
  a ready stack (mergeable in one action, none a draft, release on top, verified on the forge by
  the Foreman and the Chief of Staff), and the insertion use case. The preflight check for the
  extension goes with `forge-permissions-at-start` (P1).

## 2026-11-13, later: agents refused for a missing first line

- "Ça fait plusieurs fois que ça arrive : que faut-il faire pour que l'invocation se passe bien
  à chaque fois ? Rajoute-le dans cette CR."
- What happened: the Chief of Staff started the spec-writer with a prompt that began "Your
  card: …". The agent answered "I run inside a chantier batch only." and did nothing; the same
  happened when the corrected line came by SendMessage to the stopped agent. Only a new start
  whose prompt began with `chantier spec-writer` worked. The rule exists
  (`chief-of-staff.md` l. 139-144: copy the first line `$CHANTIER playbook` prints;
  `concepts.md` l. 244-260), but a session that has compacted its context no longer has it,
  and nothing it sees when it starts an agent reminds it.
- Restated, in this CR's scope: every chantier agent can be started right the first time from
  what the parent sees at that moment.
  - Each agent's `description` (the text the host shows next to the agent type when the parent
    starts it, on both hosts) ends with the first line its prompt must start with, e.g.
    "Prompt starts with: `chantier spec-writer for the Chief of Staff, in the project <root>.`".
  - The refusal names the expected first line, and says that a new start is needed (a message
    to the refused agent does not restart it).
  - The Chief of Staff's card puts the rule among its hard rules, and the steps that start an
    agent (spec-writer, demo-explorer, Foreman's Drivers) say "copy the first line" where they
    start it.
