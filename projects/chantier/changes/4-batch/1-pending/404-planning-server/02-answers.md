# Answers

Short name: `planning-server`

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

## 2026-11-20, the user: the specification's questions (spec critic: 12 points, 5 fixed without the user, 7 questions)

1. planning-server-Q7, delivery of the seven parts: "7 CR séparés". One CR per part (A typed
   events, B store, C writer, D leases, E waits, F access, G outside contributions), with their
   dependencies (A and B first, then C, then D to G).
2. planning-server-Q8, what keeps a Driver's lease alive during a long CI or worker wait: "Tâche
   de fond vivante". The lease stays live while a background task recorded for the CR runs (the
   CI watch), as the long gate today.
3. planning-server-Q9, AGENTS.md's measured-cost rule for new CLI tools: "Exception nommée".
   `access`, `wait` and `lease` are built and named as exceptions in AGENTS.md by this work,
   citing the user's 2026-11-20 answer ("tout").
4. planning-server-Q10, thin client: "Oui, ça remplace". Sessions write the surface's files under
   the CLI's locks; only the writer commits, rebases and pushes. The older "the other sessions
   talk to the Chief of Staff's session" and "thin client" are superseded.
5. planning-server-Q11, the code's clone and worktrees under `projects/<name>/`: "Ne jamais les
   ajouter". The writer excludes the paths `checkout.yml` names and blocks on any other nested
   repository.
6. planning-server-Q12, the remote moved while files are not yet committed: "Tout commiter
   d'abord". The writer commits everything pending before it integrates, so any conflict is a
   rebase conflict, raised to the Chief of Staff.
7. planning-server-Q13, the autosync tool's secret scan is lost: "Hooks git seulement". The writer
   runs the user's git hooks (never `--no-verify`); a secret scan goes in a pre-commit hook if the
   user wants one. Nothing more in chantier.
8. planning-server-Q14, Copilot's 5-minute `close` rule: "Baux en attendant". Leases serve until
   `copilot-close-end-event` (P2) lands; then Copilot reads the agent's end and the lease is only
   shown, as on Claude Code.
9. planning-server-Q15, a board the user starts by hand (no seat): "Oui, tu le garantis". It runs
   the writer too; the user guarantees it.
10. planning-server-Q16, a Driver's lease length: "10 min, constante". 10 minutes, renewed every
    3, a constant in the code.
11. planning-server-Q17, the surface's other files (`AGENTS.md`, `scripts/`, `justfile`): "Commit
    à la main". They stay committed by hand, like code; the writer touches only the plan
    (`projects/` and the root `chantier.yaml`).
12. planning-server-Q18, files staged by hand for two cycles: "Se bloquer". The writer blocks
    (`staged`) and tells the Chief of Staff to commit or unstage them.
13. planning-server-Q19, the conformance test runs on one real storage only: "Oui, plus tard".
    The interface stays; the test proves it the day a second backend is built. The dedicated
    branch becomes a CR of its own, later.
14. planning-server-Q20, a live lease on Claude Code: "Non, affiché seulement". The transcripts
    stay the exact source for `close`; the lease is shown beside them.
15. planning-server-Q21, QA orders: "Oui, dans ce travail". The QA driver takes and renews a lease
    as a CR's Driver does.
16. planning-server-Q22, more wait types: "Ajouter `merge`, Sur le backlog aussi". A fourth type,
    `merge` (a review request merged), and a backlog CR may carry a wait too (e.g. the user's
    answer between two grills).
17. planning-server-Q23, GitLab approvals unproved: "À prouver d'abord". GitLab's approval read
    is marked unproved; one read on a real GitLab MR (Free and Premium) before the GitLab half of
    `approval` ships.

Split (Q7): Part C, the writer, stays in this CR (`planning-server`). Parts A, B, D, E, F and G
are filed as inbox items of their own, each naming this CR; the full seven-part specification,
with every answer folded, is kept as `experiments/03-change-spec-all-parts.md` for their
specifications to start from.

## 2026-11-20, the user: forge monitoring and connectors

> Pour le monitoring sur les forge il faudra nécessairement faire du polling mais il faut une
> système pour savoir qui est intéressé. Pour les d'événements sur les issues je penses que je
> ferais un polling extérieur. Il faudra un système de plugin pour facilement rajouter des
> connecteurs

- Monitoring the forge needs polling, necessarily; it needs a way to know who is interested
  (subscriptions), so the poll reads only what someone waits for.
- Events on issues: polled from outside (an external poller), not by chantier's hub.
- A plugin system, to add connectors easily.
- Where it lands (typed waits, the hub, or a CR of its own) is the next question.

planning-server-Q24, where forge monitoring goes (polling with a registry of who is interested,
issues read by an outside poller, a plugin system for connectors): "Un CR à part". A new inbox
item, `forge-connectors`: a connector interface as plugins, the interest registry, and an entry
for an outside poller that writes into the journal. Typed waits depend on it.

## 2026-11-20, the user: the spec critic's second pass (12 points, 8 fixed without the user, 4 questions)

1. planning-server-Q25, a failed git step of the writer (a refusing hook, an IDE's `index.lock`,
   a stash): "Réessayer, dire au 2e". It retries at every cycle and appends `sync-blocked@1` only
   when the same failure comes back on two cycles in a row, as `staged`; the episode ends at the
   first cycle that completes its git steps.
2. planning-server-Q26, who pushes hand commits of the surface's other files: "il faut que tu me
   donnes un exemple plus precis et illustre". Not answered yet: asked again with an illustrated
   example.
3. planning-server-Q27, an older board with no writer still serving after the upgrade: "Nommer le
   vieux board". The refusal and the `writer: not running` line name the running board's version,
   PID and stop command; the Chief of Staff asks the user to stop it.
4. planning-server-Q28, the writer off during a batch: "Un ask, puis attendre". The Foreman sends
   one `writer off` ask per episode and holds its takes until the `writer:` line comes back.
5. planning-server-Q26, asked again with an illustrated example (a hand commit H of the surface's
   `AGENTS.md`, then the writer's commit W on top, both pushed at once): "redefini moi tout. c est
   quoi l ecrivain ?". Not answered yet: the Griller redefines the writer and its terms from the
   start, then asks again.

## 2026-11-20, the user: the writer is chantier's Board; the UI goes out of the server

> oui il y a qu un seul ecrivain pour la surface. Et cette ecrivain est celui qui maintient l'etat
> et expose le server. C'est donc bien l'equivalent de Vercel Board. Neamoins chantier board
> expose aussi la UI et je pense que il faut le sortir pour que tout passe en websocket ou HTTP
> (cas degradé derriere un proxy par exemple). Ca me permettra de faire plusieurs UI ou app
> android ou ios native par exemple

- One writer for the surface. The writer is the one that keeps the state and exposes the server:
  chantier's equivalent of Vercel Board.
- `chantier board` also serves the UI today; the UI should go out of it, so that everything goes
  through a WebSocket, or HTTP as the degraded case (behind a proxy, for instance).
- Goal: several UIs, or native Android or iOS apps.
- Q26 (who pushes hand commits) is read as "one writer pushes everything" (option A), to confirm.

planning-server-Q26, confirmed: "Oui, A". The writer pushes every local commit of the branch, hand
commits of the surface's other files included; nobody pulls or pushes the surface by hand while a
writer runs; the cards and docs say so; P13 warns on a surface rule that names a hand push.

planning-server-Q29, where the API/UI split goes: "Un CR à part". A new inbox item, `server-api`:
the server exposes an API over a WebSocket, with HTTP as the degraded case behind a proxy; the web
UI becomes one client among others (other UIs, native Android or iOS apps). It comes after
`planning-server`; until then the writer keeps the board's current HTTP API.

planning-server-Q30, hand edits left in `git stash list` when git cannot put them back after an
integration: "Oui, au 1er cycle". An exception to Q25's two-cycle rule: one `sync-blocked@1` at
once, `git-error`, the stash's name in `text`; the Chief of Staff tells the user where the edits
are.

Approval of the writer's specification, asked by the Griller:

> voit avec le CoS qui est en train de specifier et planifier tout cq

- Not approved here: the user hands the specification over to the Chief of Staff, who is
  specifying and planning all of it. The Griller tells the Chief of Staff where it stands.

## 2026-11-20, the user: a coherent split, docs and SVGs included

> normalement tout est en inbox, il faut juste que tu verifies bien que le spec writer ait bien
> compris pour livrer a la fin un redecoupage coherent, incluant la doc et les svg

- The split must end coherent: each part carries the docs and the SVG diagrams (with their
  `-texts.md` sources) its change makes false, in the same CR as the behaviour.
- The Griller's review found: Part C named three docs and no SVG (`planning-modes.svg` shows the
  autosync); A, B, F named none; D gave a search, not a list; E's "gates" collides with the fast
  and long gates; the parts table missed `forge-connectors` and `server-api`. A spec-writer run
  fixes them, with a docs map (file → parts).

## 2026-11-20, the user: the writer's specification approved

The Chief of Staff asked whether the writer pushes everything and nobody pushes the surface by
hand any more (the autosync tool, the hand-commit procedure and its secret scan go; the surface's
other files stay committed by hand, the writer pushing those commits; with no surface server, the
CLI refuses every write to the surface).

> Oui, j'approuve

- `03-change-spec.md` (Part C) is approved. It stays in the backlog until Parts A
  (`typed-journal-events`) and B (`plan-store-interface`) are specified; the three go to
  `3-ready` on the user's word.
