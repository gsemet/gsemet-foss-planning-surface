# Boot mode by surface, README rework and the board's docs

## The request

One change request, in three parts (the user, 2026-11-12; first filed "after the v0.9.0 release",
then moved before it by the user):

1. **Mode by surface.** `/chantier:chief-of-staff` with no argument means Foreman mode in a local
   session and direct mode under Remote Control. Two arguments force one: `foreman` or `direct`.
2. **README rework.** One boot skill named in "How chantier works"; a new opening for "Planning
   modes" (what a CR is, from an intent to a Change Specification) and for "Batch modes" (why
   batches: plan a set of CRs, grill by day, let the batch run overnight up to a ready-to-merge
   stack); a "Releases" section that says a release procedure goes from one package publish to a
   long procedure, with the example of a project publishing to GitHub Pages and a marketplace;
   "What is chantier?" and "Repository layout" leave the README for `CONTRIBUTING.md`.
3. **The board mod, documented.** A short README section with one screenshot
   (`board-mod-batch.png`) and a link to a richer docs page that says what the mod is, how it
   works and how to open it, illustrated with the screenshots of `intake/screenshots/`. Direct
   mode is illustrated with `direct-mode-session.png`, and the docs say that a Chief of Staff
   steering a direct batch declines to grill and points to a Griller session.

## The problem

- **The mode is a thing to know before starting.** Today the user picks the mode at the entry:
  no argument is Foreman mode, `direct` is direct mode
  (`skills/chief-of-staff/SKILL.md`, `chief-of-staff.md` "Starting a batch", step 2). Under
  Remote Control a Foreman cannot be started (`hosts/claude-code.md`, "Classes of session":
  `start_session` is refused), so the no-argument entry leads to a plan that proposes direct mode
  and waits for a yes. The surface already tells which mode can run; the user should not have to.
- **The README explains chantier twice and late.** "What is chantier?" repeats, after six diagram
  sections, what the top bullets and the diagrams say, and "Repository layout" is a contributor's
  matter. "Planning modes" and "Batch modes" open on the mechanism, not on what a CR is or why a
  batch exists. "Releases" is two lines and does not say how far a project's procedure can go.
- **The board mod is nearly invisible.** `docs/boards.md` holds one dense paragraph and no
  picture; the README only links it under "More". Nothing shows what the pane looks like, what
  its header counts, or when its cost moves.

## Where it shows

- The entries: `skills/chief-of-staff/SKILL.md` (description, last paragraph),
  `skills/chantier/SKILL.md` (the router asks three roles: Chief of Staff, Chief of Staff in
  direct mode, Griller), `.github/plugin/plugin.json` (descriptions).
- The cards: `session-start.md` (the table of section 2, the introduction's "Direct or Foreman"
  bullet, the remote line), `chief-of-staff.md` (the row "a batch", "Starting a batch" step 2,
  "Switching to Foreman mode"), `hosts/claude-code.md` ("Classes of session", "Surfaces and
  options", "A Chief of Staff and Grillers in remote"), `hosts/copilot.md` (how the argument is
  passed is unproved there).
- The docs: `README.md`, `docs/hosts.md`, `docs/use-cases*.md`, `docs/tutorial-claude-code.md`,
  `docs/boards.md`, the two simple diagrams and their `-texts.md`
  (`how-chantier-works-simple-foreman`, `-direct`: each names its entry), `CONTRIBUTING.md`.
- The eval runbooks (`evals/*/RUNBOOK.md`) start a session with the entry; `real-direct` already
  passes `direct`.

## What would fix it

- **The mode is read from the surface when it is not forced.** With no argument, the session's
  batches are Foreman batches when the user is at the machine and direct batches when the host
  signals Remote Control (its notice in the conversation, `hosts/claude-code.md`, "Surfaces and
  options"). `foreman` and `direct` force one; the user's word ("you are in direct mode") still
  changes it. A forced `foreman` where no Foreman can start is refused with the reason, as today.
  The known path to a remote Chief of Staff is "start locally, then turn on Remote Control"
  (`hosts/claude-code.md`), so the surface is read when the mode matters, at the plan, not frozen
  at the invocation.
- **The README**, top to bottom: the bullets; "How chantier works" opening on "a new session and
  one boot skill, `/chantier:chief-of-staff`, with or without an argument"; "Planning modes" and
  "Batch modes" with the user's openings; the two lifecycle sections unchanged; "Releases" with
  the range of procedures and the GitHub Pages plus marketplace example, ending on the retro that
  improves the procedure the project keeps; a board section with one screenshot and the link;
  then Install, Use, More, Develop. "What is chantier?" and "Repository layout" go to
  `CONTRIBUTING.md` (this reverses CR-195's "What is Chantier? stays in the README").
- **The board's docs page**: what the mod is (a read-only pane of Claude Code over the planning
  folder's `STATUS.json`), how to open it (`/chantier-board`, or loading the `chantier` or
  `chief-of-staff` skill), how to read it, with the screenshots in the order of a batch
  (just opened, PRs and costs, waiting for you, merged, done). Two facts the screenshots raise are
  said: the header's "waiting for you" counts unread asks as well as the table's rows; the
  batch's cost is priced when the steering session refreshes the status, not live ($0.57 over
  three screenshots, then $9.22 once done). `status-report-done.png` illustrates what "status" or
  `/chantier:status` gives.
- The screenshots are copied from `intake/screenshots/` to `docs/`; the intake is never edited.

## What the screenshots show (seven, all read)

- `board-mod-batch.png` (dark): batch-01 just opened, 3 CRs working round 1/3, 2 queued, no PR,
  no cost. The README's one picture.
- `board-mod-batch-prs-light.png`: $0.57 of $20, three CRs in CI with PRs #1 to #3 and costs.
- `board-mod-waiting-light.png`: "3 waiting for you": 1 unread ask and 2 CRs ready (Notify).
- `board-mod-merged-light.png`: "1 waiting for you" beside "Nothing waits for you" (the unread
  ask), "Merged (2 of 2)" open.
- `board-mod-batch-done.png`: 0 live, $9.22 of $20, "Merged (5 of 5)", the batch folded.
- `direct-mode-session.png`: the whole desktop window of a direct batch: the Chief of Staff's
  transcript, the Background tasks pane with three Drivers and a Verifier run from this session,
  the CR board, the session title `[Battlestation] … [Chief of Staff - Batch 01 - Direct]`, the
  Remote Control switch on. It also shows the eval sandbox's repository name, the context usage
  and the model of the session.
- `status-report-done.png`: the answer to "status" once the batch is done: the CR table, the
  notes, the cost by role, the orchestration share, the spend outside the batch, the cost notes.

## Out of scope

- The CLI: no command, no flag, no detection of the surface (the CLI knows no role and no host
  signal); `open --direct` and `preflight --direct` stay as they are.
- A new skill: `foreman` and `direct` are arguments of the one entry, not skills.
- A batch's steering once open: a batch does not change mode because the user changes surface;
  "Switching to Foreman mode" stays the user's word, and a Foreman batch still does not become
  direct.
- The board's code (`hooks/`): the Refresh button is `board-refresh-button`. This CR documents the
  pane as it is at its merge.
- New diagrams: only the entry named in the two simple diagrams and their texts changes.
- The remote board (`chantier board`), the cost's freshness itself (`status-spend-age`, P3).
- The pre-existing gap between the introduction in `session-start.md` ("in direct mode a CR joins
  only once every other CR is handled and the batch is paused") and the README ("a CR added
  while the batch runs is queued and taken when a slot frees"): noticed here, not this CR's.

## Gates

The cards and the skills change: `just check` and `just scenario` before the PR. No change under
`hooks/` or `types/`: `just mod` does not apply.
