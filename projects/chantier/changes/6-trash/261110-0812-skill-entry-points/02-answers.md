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
