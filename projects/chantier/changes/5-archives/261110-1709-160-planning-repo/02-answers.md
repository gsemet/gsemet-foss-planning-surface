# Answers (grill of 2026-11-07)

- **The surface declares its projects; a project does not declare its surface.** The model is the
  user's repository https://github.com/gsemet/agentic-planning-surface: `projects/<name>/changes/`
  holds the chantier tree (`1-inbox` … `5-trash`, without archives), the project's clone is in
  `projects/<name>/.repo/` by default, or elsewhere by configuration (a relative path), and its
  worktrees go in `projects/<name>/.worktrees/` (gitignored there). The Chief of Staff's session
  runs in the surface.
- **Syncing the surface:** the surface's own rules win. If its `AGENTS.md` says how it syncs
  (that repository runs a git autosync), chantier follows it; otherwise the Chief of Staff
  commits and pushes the surface after each step that changes it (file, grill, open, merge
  recorded, close).
- **Archives, cleaned:** an archive keeps the specification, the CR's story, a summary of what
  the PR delivers and the implementation report; it drops the working files.
- **Archives arrive in the CR's own PR:** the Driver adds the CR's cleaned archive to its PR
  before the hand-back, so it merges with the code, in the project's repository (for example
  `.agents/changes/archives`), in the same format.
- **A fully supported mode** (earlier word): every command, card, agent and host works on an
  external surface as in-project; `just scenario` covers it.
- 2026-11-07, the user: not in batch-08; it waits for later ("Playbook-config et
  external-surface le seront plus tard"). The user calls it "external-surface".
- Still open: the configuration key's name and place in the surface's `AGENTS.md`; whether
  "archives in the PR" also applies in-project mode (the archive folder is separate in both
  modes); one batch at a time per project or per surface; migration of an existing tree.

## 2026-11-10: the planning surface, always on main

> Prépare aussi le terrain pour un mode qui doit être aussi en P2 ou P1 qui est la surface de
> planification agentique, toute la partie planification spec grill sera déplacé dans un projet
> git donné, lui aussi tjs sur main.

- Confirms this CR (P1) as that mode: the whole planning part (file, triage, grill, answers,
  specification) moves to one given git repository, the surface.
- The surface is always worked on its default branch (main), never in a worktree: the Chief of
  Staff and the Griller run there. Only the project's code gets worktrees
  (`projects/<name>/.worktrees/`).
- Ground prepared by `skill-entry-points` (Q8, Q9): the start-of-session check that proposes to
  move a session from a worktree to main; with a surface, main is the surface's checkout.
- Not grilled yet; the open points above remain.

## 2026-11-10: the surface renamed, with example projects

> attention la surface de plannification a ete renommée en https://github.com/gsemet/gsemet-foss-planning-surface
> et mis plusieurs projets vides dedans pour voir la structure.

- The surface is now https://github.com/gsemet/gsemet-foss-planning-surface (the old
  `agentic-planning-surface` URL above is stale). `agentic-planning-surface` is now one of its
  projects (a CLI, "maybe merged to Chantier soon").
- Structure seen there by the Chief of Staff (2026-11-10), to check in the grill against the
  answers above: `projects/<name>/project.md` (remote, default branch, rules), a `checkout.yml`
  giving the clone and the worktrees as relative paths (chantier: `repo: ../../../chantier/`,
  `worktrees: ../../../chantier.worktrees/`, outside the surface, not `.repo/` and `.worktrees/`),
  and `changes/1-inbox, 2-backlog, 3-stash, 4-batches, 5-archives, 6-trash` (a new `3-stash`, and
  archives kept). The `agentic-planning-surface` project still has the older
  `1-inbox … 3-batches, 4-archive, 5-trash`.
- 2026-11-10, grill of `diagrams-modes-griller`: the README does not mention the external
  surface yet ("Ne pas en parler"). This CR adds it to the README, the docs and the introduction
  when it ships: the planning area is either in the project (`.agents/changes/`) or external.
- 2026-11-10, the user, while CR-156 (`diagrams-modes-griller`) runs in batch-09: "faut qu'on
  enchaine apres ca par le mode extern" — this CR comes next, right after CR-156. It still needs
  its grill (the open points above, and the surface's new structure) and a specification.
  Where to grill it: "Ici, après CR-156" — in the Chief of Staff's session, once CR-156 is
  merged and batch-09 paused (not in a Griller session in parallel).

## 2026-11-10: explain the planning modes; remote; Grillers; outside contributors; the surface's nature

User's words:

> on va en profiter pour bien expliquer les modes planning, ce qui est sur main et sur worktree
> par ce que c'est pas bien expliqué. en remote, on peut pas demarrer de session non-worktree ce
> qui empeche le mode planing de chantier. donc le chief of staff doit forcément être démarer en
> local puis mis en remote. les session nested aussi pose probleme donc en remote on est reduit a
> une config "reuse de session chief of staff" + optionellement worktree jamais mergé de Griller.
> Les Grillers permettent de faire des prototypes, plan, etc, au propre dans le meme dossier de CR
> (les artefacts devront normalement etre transférer au chief of staff et pas mergé). des
> personnes externes peuvent fournir leur CR sur P1, P2,... mais ca devra passer par une PR sur le
> projet agentique.
> Le projet agentique permet d'avoir un espace de travail isolé, multi utilisateur, partagé par git
> mais il doit fonctionner comme un vault obsidian avec git obsidian, push sur master le plus vite
> possible, comme un onedrive par exemple. c'est un espace de travail semi structuré pour une toute
> petite équipe active (2-4p max) travaillant autour d'un meme sujet.

In English, as points for this CR's scope and grill:

- **Explain the planning modes** (docs, README, cards): what runs on main and what runs in a
  worktree. Today it is not explained well.
- **Remote (the user's finding):** a remote session cannot be started outside a worktree, which
  blocks chantier's planning on main. So the Chief of Staff must be started locally, then put in
  remote. Nested sessions are a problem in remote too. In remote, the setup is therefore reduced
  to: reuse the Chief of Staff's session (direct mode), plus, optionally, Griller sessions in
  worktrees that are never merged.
- **Grillers:** they make prototypes, plans and the like, cleanly, in the same CR folder; the
  artefacts are normally transferred to the Chief of Staff, not merged (consistent with the
  multi-session rule: a Griller in a worktree opens no PR and sends its files to the Chief of
  Staff).
- **Outside contributors:** people outside the team may submit their CR to P1, P2, … but only
  through a PR on the planning project (the surface).
- **The surface's nature:** an isolated, multi-user workspace shared through git, which works like
  an Obsidian vault with obsidian-git: push to the default branch as fast as possible, like
  OneDrive. A semi-structured workspace for a very small active team (2 to 4 people at most)
  working around one subject.
- To check at the grill: the remote limits are the user's own finding on the host; the host
  reference (`hosts/claude-code.md`) records them as such, or as unproved where not yet tried.

## Grill of 2026-11-10 (after batch-09 paused)

### Round 1

The Chief of Staff read the surface first (https://github.com/gsemet/gsemet-foss-planning-surface).
Its `AGENTS.md`:

- requires OKF frontmatter, an `index.md` per folder and `just validate` after each edit;
- names CR folders `<issue>-<slug>` with a raw-tracker `intake/`;
- uses the stages `1-inbox`, `2-backlog/P1..P4`, `3-stash`,
  `4-batches/{1-pending,2-actives,3-done}`, `5-archives` and `6-trash`;
- runs a git autosync (`scripts/ai-autosync-git.py`), with one leader per checkout, about every
  10 s.

1. **Tree layout.** The user chose "Chantier adopte la surface": the surface's tree (`3-stash`,
   `4-batches` with three states, `5-archives`, `6-trash`) becomes chantier's tree in both modes,
   in-project and external.
2. **Archives.** The user's words: "les deux, avec le pointeur dans l'archive de la surface qui
   pointe vers la PR de livraison, et le status "CR livré dans la PR ou pas". il faudra penser
   dans la surface a une maniere de configurer si le mainteneur veut livrer aussi dans la PR ou
   pas".
   - Both places get the archive.
   - The surface's archive points to the delivering PR, and says whether the CR's archive was
     delivered in that PR or not.
   - A surface setting says whether a project's maintainer wants the archive delivered in the PR
     as well.
3. **The surface's own rules.** The user's words: "cette surface va "passer source chantier",
   donc tout ce qui est fait aujourdhui par la surface devra etre fait par chantier: l'autosync,
   multiprojet, etc. juste qu'il pourra y avoir n chief of staff lancé sur n projects dans cette
   surface, donc il faut qu'ils se synchronise les push/rebase entre eux. au pire il y aura 3
   checkout de la surface mais c'est peu probable".
   - The surface becomes chantier-sourced. What the surface does today by its own scripts and rules
     is done by chantier: the autosync, the several projects, and the rest.
   - n Chiefs of Staff may run on n projects of one surface. They synchronise their pushes and
     rebases with each other.
   - At worst there are about three checkouts of the surface; that is unlikely.
4. **A running batch's state.** The user chose "Non, local seulement". `batch.json`,
   `events.jsonl` and the STATUS files of a running batch stay on the steering machine and are
   ignored by git. Only the result (the archive, the final state) is pushed to the surface.

### Round 2

5. **OKF.** The user chose "Pas OKF pour l'instant". Chantier takes over the autosync and the
   several projects, but not the OKF format, which is a later subject. The surface drops its OKF
   rules for chantier's folders.
6. **Split.** The user chose "Plusieurs CR". Each CR merges on its own:
   1. the new tree;
   2. the external mode, on the surface's existing autosync;
   3. the sync taken over by chantier between several Chiefs of Staff, which joins
      `planning-server` (P3).
7. **CR folder names.** The user chose "Numéro de CR". Chantier's number stays
   (`156-diagrams-modes-griller`). A tracker issue, when there is one, is a link inside the CR.
8. **Migration.** The user chose "Pas encore". Chantier's own planning stays in-project for now.
   No migration command is in scope.

### Round 3

9. **`3-stash`.** The user chose "Prête à lancer": specified CRs that wait for the next batch.
10. **`4-batches` states.** The user's words: "ce sont les etat des CR dans le batch". So
    `1-pending`, `2-actives` and `3-done` are the states of the CRs inside the batch. The
    Chief of Staff reads it as follows; this reading is to be confirmed in the restatement:
    - the CR folders of the current batch sit directly under the state folder;
    - there is no `batch-<n>` level;
    - the batch's own files stay local (answer 4), and there is one batch at a time per project.
11. **`planning-surface-positioning`.** The user chose "Fusionner ici". Its request is copied into
    `intake/positioning-request.md`, and the original is moved to
    `5-trash/261110-1140-planning-surface-positioning`. What CR-156 did not cover goes into the
    external mode's documentation (CR 2), with the explanation of the planning modes.

### Restatement and closing

- The Chief of Staff restated the whole grill, including its reading of `4-batches` (answer 10).
  The user: "oui c'est presque bon, est ce que tu proposerais un meilleur nom pour 3-stash ? peut
  etre 3-ready".
- **The `3-stash` folder becomes `3-ready`.** The Chief of Staff warned that "ready" already
  names a CR whose PR is ready to merge (`handback ready`), and recommended `3-next`. The user
  chose "3-ready". The specifications must keep the two meanings apart in their wording: the
  `3-ready` folder, and a PR ready to merge.
- The rest of the restatement stands, the reading of `4-batches` included. Grilled enough.
- **Where the three CRs go:**
  1. The new tree is filed as its own P1 item, `changes-tree-v2`.
  2. The external mode is this CR, `planning-repo`. It depends on `changes-tree-v2`.
  3. The sync taken over by chantier is recorded in `planning-server` (P3).

### The specification's open questions (2026-11-10)

1. **Who declares the surface.** The user chose "La surface" (recommended):
   - the surface's `projects/<name>/` is the declaration;
   - the project's `AGENTS.md` may hold an optional pointer line, which the Chief of Staff reads
     and the CLI does not.
2. **A running CR's `work/`.** The user's words: "poussé dans la surface regulierement, archive a
   la fin (attention il faut éviter de tout publier, le rapport et preuves uniquement, pas de log
   detaillés dans l'archive)".
   - The CR's folder is pushed to the surface regularly while it runs. The archive is made at
     the end.
   - Publish only what is needed: the report and the evidence. Detailed logs stay out of the
     archive.
   - This is not answer 4: answer 4 is about the batch's own files (`batch.json`, `events.jsonl`,
     STATUS), which stay local.
3. **The cleaned archive in the PR.** The user chose to keep `evidence/` and `intake/` as well. The
   archive in the PR therefore has:
   - `intake/`, `evidence/`;
   - `01-intent.md`, `02-answers.md`, `03-change-spec.md`;
   - the delivery file and `STATUS.md`.
   - Without `work/` and without detailed logs.
4. **Diagrams.** The user chose "Dans cette CR": the README and docs diagrams show the external
   mode in this CR, and the user reviews their renders in the PR.

Left to the Driver, the recommendation stands:

- the archive setting's place and default: a line in `project.md`, `yes` when absent;
- a Griller in a surface worktree does not join the autosync, and its files go to the Chief of
  Staff;
- archives in the PR stay out of in-project mode in this CR;
- the fallback sync when a surface has no autosync: the Chief of Staff commits and pushes after
  each step.

## The batch folder's name (2026-11-10, review of PR 95)

The user, reviewing `changes-tree-v2` (CR-158): one batch runs at a time, so the folder is
`4-batch`, not `4-batches`: "4-batch alors". Read `4-batch` wherever `4-batches` appears above.
