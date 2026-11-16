# Answers: multi-session-chief-of-staff

Grilled with the user on 2026-11-09 (Battlestation session), in French; recorded in English.

## 1. The second role and what it is for

- The role is called **Griller**, not Planner.
- A Griller refines, reorders and rearranges the inbox and the backlog (file, triage, grill,
  answers, specification). It may also prepare work for the Chief of Staff.
- Griller sessions are normally **short**: started for a few items, they end quickly.
- The **Chief of Staff always has the last word** on launching and arranging batches.
- In direct mode the Chief of Staff steers the Drivers itself, so its role and the Foreman's
  are partly merged; that does not change the rule above.
- Motivation: working with **no nested sessions** is simpler in remote.

## 2. How a session takes its role

- `/chantier` in an environment with **no other active session**: the session answers that it
  is the Chief of Staff (the user's word: "chef de chantier") and renames itself. No question.
- `/chantier` in a **second session**: the same opening, ending with one message, in the
  user's language: "a Chief of Staff is already active at <link to that session>; I become a
  Griller: I will not follow the batches actively, but I can help refine the backlog's ideas."
- Difficulties the user names, to be solved by the CR:
  - telling the sessions really active from those that have stopped;
  - offering the user options, but not complex ones;
  - extensible to other coding agents, e.g. Copilot.

## 3. Telling an active session from a stopped one

- The seat is a small file in `.agents/changes/`, kept by the CLI: the session id, the
  environment, the title and the link. No activity date is taken as proof of life (a Chief of
  Staff may sit idle for hours and still be alive).
- The **host** says whether the seat's session is alive (on Claude Code, the session list and
  its states); how is written in `references/hosts/<host>.md`, which keeps it extensible to
  Copilot and others.
- When the host cannot tell, or the seat's session looks stopped, the new session never takes
  the seat by itself: one line, "the Chief of Staff at <link> looks stopped; shall I take its
  place?".
- The Griller's opening message ends with one option only: say "become chief of staff" to
  take over.
- The user's caution: keep it **simple and flexible**.

## 4. Handing the seat over while a batch runs

- Encode only the **rules**; the models judge the rest well. No step-by-step procedure.
- A running Driver cannot be stopped or moved to another session.
- If the user agrees, the old Chief of Staff finishes the running work itself (or through its
  Foreman). Once every Driver has finished (its PR may still be open, not yet merged or
  archived), the old Chief of Staff tells the new one: "your turn, you are the Chief of Staff".
- Like the transfer of controls in aviation, the new one acknowledges explicitly, e.g. "I have
  the batch". The seat moves only on that acknowledgement.

## 5. Two sessions on one CR

- **No claim, no lock.** The user may work in several Grillers at once, or in a session
  isolated from everything, just to refine one point.
- What matters is that every session always works **from the CR folder's files** (re-read them
  before acting, write each answer there at once), so another session's work is never lost.
- What a Griller never does stays as before: no batch, no order, no steering, no close, no
  merge (answer 1: the Chief of Staff has the last word on batches).

## 6. How the Chief of Staff learns what the Grillers did

- Through the files only: no dedicated journal, no routine messages between sessions (the
  host limits them, and a Griller may be isolated).
- The Chief of Staff re-reads the backlog's folders when it needs to: before proposing a
  batch, on "status?", or when the user says a Griller has finished.
- One optional message: a Griller that sees an active Chief of Staff session may send it one
  line when a CR becomes ready to run (its specification written): "<CR> ready, spec written".

## 7. Session titles

- Format `[env] Project [role]`:
  - `[env]`: the machine's name (`Battlestation`, `Mac`), `Remote` for a cloud session;
  - `Project`: the repository's name, capitalised (`Chantier`);
  - role: `Chief of Staff` or `Griller`.
- A session renames itself as soon as its role is set, and again when it changes (hand-over).
- A Griller may add its subject once known: `[Battlestation] Chantier [Griller] landing-page`.
- Foreman: `[env] Project [Foreman - Batch 06]` (replaces the current rule "Chief of Staff
  title + ` - [Foreman Batch 06]`").
- Chief of Staff steering a direct batch: `[env] Project [Chief of Staff - Batch 06 - Direct]`;
  back to `[env] Project [Chief of Staff]` once the batch is closed.
- A host that cannot rename a session: nothing is done, no workaround.

## 8. The guided remote set-up

- With answers 2 and 3, the last two steps of the user's flow become automatic: the first
  session is the Chief of Staff, the fork becomes a Griller by itself.
- The flow is written in `references/hosts/claude-code.md` and, short, as a how-to in the docs
  ("A Chief of Staff and Grillers in remote").
- The Chief of Staff offers it in one line when relevant (end of the first-turn introduction in
  a remote session; the user asks to grill while a direct batch runs): "to grill in parallel,
  fork this session; the fork becomes a Griller".
- It never does what is the user's: the fork, auto mode, no worktree. It explains them.
- To prove during implementation: a fork inherits the conversation and could believe it is the
  Chief of Staff. Rule: a session re-reads the seat at each `/chantier` and after a fork; the
  host decides. The user's condition: **only if the host makes it possible**; otherwise record
  what is not possible in the host reference, no workaround.

## Cross-reference from `skill-entry-points` (2026-11-10)

The user renamed the Planner role **Griller**, with its own skill `/chantier:griller`; the Chief
of Staff's skill is `/chantier:chief-of-staff` (direct mode by the user's word or its `direct`
argument). See `2-backlog/P1/skill-entry-points/02-answers.md`, Q1.

## 9. Reconciling with `skill-entry-points` (2026-11-10)

Question: a session starts while a Chief of Staff is active; answers 2, 3 and 8 against
`skill-entry-points` Q2 (two Chiefs of Staff: warn, block until the user chooses).

> B oui sauf s'il y a un batch actif il faut demander à l'utilisateur s'il est sûr de faire le
> "handover" à la nouvelle session ou s'il veut juste griller des CR

- `/chantier:chief-of-staff` (or `/chantier:chantier`) in a second session, with a Chief of Staff
  active and **no batch active**: the session becomes a Griller by itself, as in answer 2.
- **With a batch active**: the new session asks the user whether they are sure they want the
  hand-over to this session (answer 4's rules then apply) or only want to grill CRs.
- `/chantier:griller`: a Griller, no question.
- The block of `skill-entry-points` Q2 holds only when the user's word makes a second session
  Chief of Staff ("tu es le chief of staff"): warn, block until the user chooses the one that
  takes the batch.
- Answer 8 holds: the fork becomes a Griller by itself (or asks, if a batch is active).

## 10. A Griller in a worktree (2026-11-10)

> On va juste rajouter un point sur les sessions griller dans multi-session: le griller peut
> travailler sur un worktree, mais dans ce cas, il ne fera pas de PR/MR mais il enverra ces
> fichiers de spec, plan, artifact,… à la session chief of staff

- A Griller may work in a worktree (a linked worktree of the project, as a remote or app
  session often starts).
- In that case it opens no PR or MR for its work: the planning files it produced (answers,
  specification, plan, artifacts, …) are sent to the Chief of Staff's session, which places them
  in `.agents/changes/` of the main checkout.
- This refines answer 6 ("through the files only"): a Griller on the main checkout writes the
  CR folder directly; a Griller in a worktree hands its files to the Chief of Staff instead.
  How the files travel (message, paths) is the host's; written in `references/hosts/<host>.md`.

## Go (2026-11-10)

> Aller fait les spec et lance le batch que tu laisseras ouverts à la fin

- Grilled enough. Specs by the spec-writer, then one batch, direct mode, in series:`multi-session-chief-of-staff` then `skill-entry-points`. At the end the batch is paused, not closed.
- Blocked the same day: preflight P6 and P7 failed (this session runs in the linked worktree `epic-lamport-b88c2f`; its hook also refuses writes in the main checkout's `.agents/changes/`).



---

# Merged from skill-entry-points (2026-11-10)

The user merged skill-entry-points into this CR: one CR, one specification. Its file follows as it was.

# Answers: skill entry points

Grill with the user, 2026-11-10, in French; recorded in English.

## Q1. The role from the skill invoked, or from the user's word?

> 1. Nom des skills: Chief-of-staff et griller (pas planner). Le mode direct se fait en verbal ou
> en faisant /chantier:chief-of-staff direct)

- Two skills: `/chantier:chief-of-staff` and `/chantier:griller`. This replaces the request's
  `chief-of-staff-with-foreman` / `chief-of-staff-direct` pair.
- The role the P1 `multi-session-chief-of-staff` calls **Planner** is named **Griller**.
- Direct mode is not a skill of its own: the user says it ("tu es en mode direct"), or invokes
  `/chantier:chief-of-staff direct` (the skill's argument). Without it, Foreman mode.

## Q2. Changing role on the user's word

> Tout est possible mais il faut prévenir l'utilisateur quand 2 chief of staff est actif et tout
> bloqué tant que l'un n'est pas choisi comme le chief of staff actif pour "prendre le batch"

- The skill invoked gives the starting role; the user's word changes it at any time, both ways
  (Griller to Chief of Staff, Chief of Staff to Griller).
- When two sessions are Chief of Staff at once, the user is warned, and everything is blocked
  until the user chooses which one is the active Chief of Staff, the one that "takes the batch".

## Q3. The old `/chantier:chantier`

> B

Then corrected:

> C plutôt
> J'ai demandé c à la précédente question

- `/chantier:chantier` stays, as a router: it asks the user which role they want (Chief of Staff,
  with or without direct mode, or Griller), then loads that skill. No alias, no removal.

## Q4. Where the shared content lives

> 4. Dans le skill commun "chantier"

- The cards, the CLI and the assets stay in the common skill `skills/chantier/` (its `SKILL.md`
  is the router of Q3). `skills/chief-of-staff/SKILL.md` and `skills/griller/SKILL.md` are thin
  and point at `skills/chantier/`'s cards and CLI; `$CHANTIER`, the tests and the docs keep their
  paths.

## Q5. Foreman mode asked where no Foreman can start

> A il proposé et il explique pourquoi et ce qui change clairement

- `/chantier:chief-of-staff` without `direct`, on a host that cannot start a Foreman: at the plan,
  the Chief of Staff proposes direct mode, says why, and says clearly what changes (no Foreman
  session; it steers the Drivers itself; no grill, triage or discussion while the batch runs;
  new ideas go to the inbox). It waits for the user's yes.

## Q6. Copilot

> Pareil valide je testerais plus tard

- Same three skills, same names, on both hosts: `.github/plugin/plugin.json` declares
  `skills/chantier` (router), `skills/chief-of-staff` and `skills/griller`. The user tests Copilot
  later; what is not proved there is marked unproved in the host reference.

## Grilled enough

The user, 2026-11-10, after the full restatement: "Parfait." The spec-writer runs once both CRs of the batch are grilled.

## Q7. Reconciled with `multi-session-chief-of-staff` (2026-11-10)

A second session started as Chief of Staff becomes a Griller by itself when no batch is active;
with a batch active it asks the user: hand-over or only grilling. The Q2 block holds only when the
user's word makes a second session Chief of Staff. See that CR's `02-answers.md`, answer 9.

## Go (2026-11-10)

> Aller fait les spec et lance le batch que tu laisseras ouverts à la fin

- Grilled enough. Specs by the spec-writer, then one batch, direct mode, in series:`multi-session-chief-of-staff` then `skill-entry-points`. At the end the batch is paused, not closed.
- Blocked the same day: preflight P6 and P7 failed (this session runs in the linked worktree `epic-lamport-b88c2f`; its hook also refuses writes in the main checkout's `.agents/changes/`).


## Q8. Fail at start, not at the go (2026-11-10)

> Pourquoi tu me la pas dit il fallait failer tout de suite en griller ou cos

- At its start, `/chantier:chief-of-staff` and `/chantier:griller` (and the router) check what
  would block the work later, the session in a linked worktree first (preflight P6, P7, and a
  host that refuses writes in the main checkout's `.agents/changes/`), and say it at once, in the
  first message: what fails and what the user does (a session on the main checkout).
- A Chief of Staff there cannot steer a batch; a Griller cannot write in `.agents/changes/`. Not
  discovered at the go.

## Q9. Claude Code remote sessions start in a worktree (2026-11-10)

> J'ai l'impression que dans Claude code quand on démarre une session remote on est tjs sur un
> worktree. Tu peux passer sur main sans perte ? Si c est le cas pour la prochaine, encode dans
> l'une des CR cette spécificité de Claude code de telle manière que tu proposes, les prochaines
> fois de passer sur main pour faire la planification.

- Claude Code specific, written in `references/hosts/claude-code.md`: a remote session (and an
  app session by default) often starts in a linked worktree (`.claude/worktrees/<name>`).
- With Q8: at start, the Chief of Staff or the Griller sees it and proposes to move the session
  to the main checkout for planning, with the host's means (Claude Desktop:
  `mcp__ccd_directory__change_directory` to the repository's root, which the user approves). It
  first checks nothing is lost: the worktree is clean and its branch has no commit beyond the
  default branch; otherwise it says what would be left behind and asks.
- Refused on 2026-11-10 in the Battlestation session (a clean worktree, no commit):
  `change_directory` answered that a session in an isolated worktree cannot be moved. So the
  proposal is a step of the user's: open a new session on the main checkout, without worktree;
  the files hold the state, nothing is lost. Whether a remote session can start without a
  worktree is to prove; the host reference says what is and is not possible.
- Once a planning surface exists (P1 `planning-repo`), "main" means the surface's checkout on
  its default branch, not the project's.


## Merge (2026-11-10)

> Je pense que tu peux merger les CR multi et skill entry points. Tue les 2 spec et fait en qu'un CR.

- One CR now: multi-session-chief-of-staff carries skill-entry-points (its request in `intake/request-skill-entry-points.md`, its intent and answers appended above). One specification, one PR.
- The two spec-writers started earlier were stopped before writing anything.
- The skill-entry-points folder goes to `5-trash/` (abandon), its content kept here.

## Diagrams moved out (2026-11-10)

- The docs SVG diagrams (`docs/*.svg`, the README's images) move to a separate CR, `diagrams-modes-griller`, filed on the user's request the same day; it runs after this CR. This CR keeps the prose docs it needs. The spec-writer was told.

## The specification's open questions (2026-11-10)

- **Q1:** a paused batch counts as active for answer 9's hand-over question (the user chose this over the recommended running-only): the question is asked whenever a batch is not closed.
- **Q2:** confirmed: `/chantier:chief-of-staff` never asks the role; the router asks unless a live Chief of Staff holds the seat.
- **Q3:** no CLI refusal of `open`, `order`, `close` from a session not in the seat; the Griller's card forbids them (simple and flexible). (Recommended.)
- **Q6:** a Griller may `abandon` an item, on the user's explicit word only. (Recommended.)
- **Q4** (the CR board for `griller`) and **Q5** (`[env]` from the hostname): implementation detail, not asked (the user's rule of the same day: such detail is the agents'); the spec's recommendations stand: no board for `griller`, `[env]` from the hostname.
