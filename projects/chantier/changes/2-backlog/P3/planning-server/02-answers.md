# Answers

## 2026-11-10, the user, during the Beads study

> la regle 'aucune configuration' est pour le projet cible, mais en mode externe on pourrait
> accepter une configuration yaml/json. Par contre les regles de codage doivent rester dans le
> projets AGENTS.md. l'idee c'est que des contributions mineurs externes doivent pouvoir etre
> faite sans chantier, meme si ce serait bien qu'elles se terminent par un rapport dans les
> archives.

- "No setup" is for the target project. The external surface may take a YAML/JSON configuration.
  Coding rules stay in the project's `AGENTS.md`.
- Minor outside contributions can be made without chantier; ideally they end as a report in the
  archives.

On the risks of adopting Beads as the store:

- Installing a binary is not a problem.
- It would be multi-session.
- The CLI would do the persistence and the sync.
- **The upstream churn is the main blocker.**

On what to borrow:

- **Hash IDs:** rejected: "ce serait pas trié et j'ai déjà un slug".
- **Heartbeat/reclaim:** "ça vaudrait le coup".
- **Gates:** they must stay generic: a GitLab MR as well as a GitHub PR; Codex, GitLab Duo or
  Copilot as well as Claude Code.
- **The external planning surface:** "le point le plus important : je touche très vite les
  limites de mettre le plan dans mon projet. Il faut une surface de planification externe, mais
  c'est plus lourd."

> pour moi dans chantier le seul écrivain c'est le chief of staff, même avec des grillers. il
> peut donc être le garant du serveur (qui fait les écritures, push/rebase et sert un serveur de
> tracking des tickets)

> alors je pense qu'il faut 1 chief of staff par project dans un meme depot. met tout dans une
> CR en P3 que l'on continue plus tard

- One Chief of Staff per project, several projects in one surface repository.
- Filed as P3, to continue later.

## 2026-11-10, the user: Markdown browsable on the forge

> pour moi le fait de tout avoir en markdown est primordial je veux pouvoir naviguer dans le
> projet avec la forge, ca peut passer par une branche speciale ou mieux notre projet special.
>
> ces comparaisons sont importantes a mettre dans l'etude sur le CR

- **Everything in Markdown is essential:** the user must be able to browse the plan on the forge.
- **Where on the remote:** a dedicated branch is acceptable; a separate planning project is better.
  A hidden ref, as Beads does now with `refs/dolt/data`, is ruled out because the forge cannot
  show it. So is a database as the store.
- The comparison tables go into the CR's study: `experiments/plan-storage-comparison.md`.

## 2026-11-10, the user: the storage table, corrected

The user rewrote the "chantier, studied" column of the storage table, now in
`experiments/plan-storage-comparison.md`, section 2. What changed against the first draft:

- **Format:** the append-only events are additional Markdown and JSON files. The table no longer
  says the STATUS files are regenerated and never merged.
- **Writes:** the other sessions talk to the Chief of Staff's session.
- **Reads:** the files are directly readable on the forge. Tracking over HTTP/MCP is no longer
  named.
- **Sync delay:** after each write, within 5 minutes at most.
- **Conflicts:** the server raises them to the Chief of Staff for an automated resolution. If two
  sessions have not synced and both try to push, the Chief of Staff resolves to its best guess or
  asks the user. This replaces "no conflict within a project".
- **Setup of the surface:** to be defined (no longer "a YAML or JSON config").
- Dolt considered for the Markdown, then set aside for now (the user: "on l'écarte pour
  l'instant").

## 2026-11-10, from planning-repo's grill (Chief of Staff's session)

- `planning-repo` was split into three CRs (its `02-answers.md`, answer 6). The third CR is the
  sync taken over by chantier, and it joins this CR: the surface becomes chantier-sourced
  (answer 3). Chantier does the autosync and the several projects. n Chiefs of Staff on n
  projects of one surface synchronise their pushes and rebases with each other. At worst there
  are about three checkouts of the surface.
- A running batch's state stays local to the steering machine (answer 4).
- No OKF for now (answer 5).
## 2026-11-20, the user: build or reuse Vercel Board (Griller session)

Question 1: does "the plan is Markdown browsable on the forge" stay absolute, now that Board
breaks it as Beads did?

> je differentie la board pour les messages et le stockage des plans. on met tout dans vercel
> board ?

- The user separates two things: a board for messages (coordination between sessions) and the
  storage of the plans.
- The user asked whether everything should go into Vercel Board; the Griller's answer is in the
  next question.

Question 2 (for messages between sessions: keep chantier's journal and borrow Board's ideas, an
optional Board bridge, or Board as the main channel). The user asked first:

> il ne supporte pas gitlab ou jira ?

- The Griller's answer, from the docs and the sibling study: Board syncs with GitHub (pull
  requests and issues into a channel, one way by default), Slack and Linear (both ways), all
  through Vercel Connect. Neither GitLab nor Jira is supported or mentioned; labels and task
  state never sync.

> 1

- **Keep chantier's own messaging and borrow Board's ideas.** No Board dependency, hosted or
  local, for messages or for plans: chantier's journal, surface server and watchers stay the
  channel between sessions.

Question 3: which of Board's ideas this CR takes (leases on tasks; typed waits, or gates; typed
events with a versioned schema; an "explain access" command; the storage behind a minimal
interface with a conformance test).

> tout

- All five go into this CR's scope:
  1. Leases: a session claims a ready CR and renews a short lease; an expired lease frees the CR.
     It replaces the "session file written in the last 5 minutes" heuristic.
  2. Typed waits (gates): a blocked CR records what it waits for (a human answer, an approval, a
     green pipeline), generic across GitHub and GitLab, Claude Code and Copilot.
  3. Typed journal events, `name@N`, a published version never changing.
  4. An "explain access" command: why a session may or may not write, claim or push.
  5. The plan's storage behind a minimal interface with one conformance test that every backend
     (the planning folder, a dedicated branch, a server) passes.

The Griller restated the decision (build, borrow Board's five ideas, no Board dependency) and
asked whether the CR was grilled enough.

> ce n est pas du tout assez etudier il va faloir tout specifier

- Not grilled enough: everything must be specified. The grill goes on, idea by idea, before any
  specification.

Question 4: who syncs the surface with the forge (chantier takes the sync over; the surface's own
autosync tool stays; or both, chantier stepping aside where the surface has an autosync)?

> 1

- **Chantier takes the sync over.** The surface server, elected and guaranteed by the Chief of
  Staff, becomes the one writer: it commits, rebases and pushes within 5 minutes, and raises
  conflicts to the Chief of Staff. The surface's own autosync tool is no longer needed.

Question 5: what happens when no server runs (the Chief of Staff's session closed, the machine
restarted, a Griller alone): writes refused; written locally and pushed at the next start; or any
chantier session may start the server?

> 1

- **Writes are refused** until a Chief of Staff starts the server again: no fallback. A Griller
  alone records nothing.

Question 6: on how many machines at once (one machine in this CR; several, one per project;
several, even on one project)?

> il faut qu un seul watcher-autosync a un moment donne. mais cest inherent au fait d etre sur un
> projet git distribue. n accorde pas trop d importance et rentre dans les details de la spec de
> chaque etat, chaque message. fait un document de specification complet

- One watcher-autosync at a time, for the surface. Several machines is inherent to a distributed
  git project: do not weigh it much; two writers on two machines meet as any two git clones do.
- Go into the specification's details: every state and every message, specified.
- Write a complete specification document.

- The user's word to write the specification counts as "grilled enough" for this pass; the
  specification states every state and message, and its open questions come back to the user.
- Spec critic: yes, it changes who writes and pushes the surface (a shared, irreversible step),
  the CLI's refusals (writes refused with no server), the roles' contracts (leases, waits) and
  several areas at once.
