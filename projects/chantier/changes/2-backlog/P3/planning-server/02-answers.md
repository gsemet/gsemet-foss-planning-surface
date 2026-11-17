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