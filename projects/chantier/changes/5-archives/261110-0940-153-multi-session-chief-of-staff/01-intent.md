# Intent: several chantier sessions, one Chief of Staff

Intake: `intake/request.md` (two merged items: the Mac CR's request, summarised, and the
user's words of 2026-11-08, in French). Analysed against v0.8.0.

## The request

The user opens several sessions on the same repository and runs `/chantier` in each. The
sessions see each other and, under the user's supervision, agree that exactly one of them is
the active **Chief of Staff** at any time. Every other session is a **Planner**: it takes items
from the inbox or the backlog, grills them with the user, completes their specifications and
changes their priorities. The Chief of Staff is notified of what the Planners do, but only it
opens and runs batches, either through a Foreman or by steering them itself (direct mode). The
user expects the usual set-up to be one Chief of Staff in direct mode with one or more Planners.

Added on 2026-11-08:

- **Roles assigned by the user's word:** "tu es le chief of staff" in one session, "tu es un
  planner" in another. This is in tension with a seat claimed automatically at `/chantier`.
- **Session titles:** once a session has its role, it renames itself `[env] Project [role]`,
  e.g. `[Battlestation] Chantier [Chief of Staff]`, `[Battlestation] Chantier [Planner]`.
- **A guided remote set-up** chantier helps the user through:
  1. start a remote session, with no worktree and with the tools allowed in auto mode;
  2. run `/chantier`;
  3. after the boot, fork the session;
  4. say "tu es le chief of staff" in one;
  5. say "tu es un planner" in the other.

Target: Claude Code first. Host-specific mechanics go in the host's reference
(`references/hosts/claude-code.md`), not in the role cards.

## What v0.8.0 already has

- **Direct mode** (`open --direct`, `preflight --direct`, "Steering a batch yourself"): the Chief
  of Staff claims the batch's steering seat (`foreman set <own session id>`) and runs the
  Drivers itself. While it steers, it holds no grill, triage or discussion. The batch-lifecycle
  doc already says "grill in another session of yours". That other session is what this CR
  makes a role.
- **One batch at a time:** `open` exits 2 while a batch is not closed.
- **The batch's steering seat:** a stale one exits 3.
- **`work/specifying`** marks a CR whose `spec-writer` is running.
- **Host references** (`hosts/claude-code.md`, `hosts/copilot.md`) with proved / documented /
  unproved marks.
- **Session renaming** works on Claude Code (this session renamed itself on 2026-11-08).

## What is missing

- **A Planner role:** the backlog-and-grill part of the Chief of Staff card (file, triage,
  grill, `02-answers.md`, spec-writer), with no `open`, no `order`, no steering, no `close`.
- **A Chief of Staff seat outside any batch:** who is the Chief of Staff of the repository right
  now, so a second `/chantier` session knows it is a Planner. The batch's seat only covers a
  batch that is already open.
- **Role assignment and titles:** how a session learns its role (the user's word, the seat) and
  renames itself `[env] Project [role]`; what `[env]` is.
- **The guided remote set-up:** where chantier offers it (first turn, `init`, on demand) and
  what it can do itself versus what the user does (fork, auto mode, no worktree).
- **Seeing the other sessions:** finding them and reaching them with a message (a host
  mechanism, to prove on Claude Code and to record in the host reference).
- **Notifying the Chief of Staff** of the Planners' changes (filed, triaged, specified, ready to
  run) without using up the host's limit on messages between sessions.
- **No two sessions on one CR:** two Planners, or a Planner and the Chief of Staff, must not
  grill or specify the same CR at once.
- **Hand-over:** the seat moves from one session to another on the user's word, including while
  a direct batch runs (its Drivers belong to the steering session) and with a Foreman.

Likely touches: `SKILL.md` (the role a session takes at start), `references/chief-of-staff.md`,
a new `references/planner.md`, `references/hosts/claude-code.md`, `concepts.md`, `routing.md`,
the CLI (seat, CR claim, a backlog journal: `rails.py` for the refusals), README and docs
diagrams, the scenario, `tests/test_structure.py`.


---

# Merged from skill-entry-points (2026-11-10)

The user merged skill-entry-points into this CR: one CR, one specification. Its file follows as it was.

# Intent: two skill entry points, the steering mode chosen at invocation

Intake: `intake/request.md` (the user's words of 2026-11-10, in French). Analysed against v0.8.0.

## The request

The plugin's one entry point, `/chantier:chantier`, becomes two:
`/chantier:chief-of-staff-with-foreman` and `/chantier:chief-of-staff-direct`. The skill the user
invokes says how the session's batches are steered. The two share everything they can: one may
call the other, and no text is duplicated. A small CR.

## Today (v0.8.0)

- One skill folder, `skills/chantier/`: `SKILL.md` (introduction, entry points, hard rules), the
  cards in `references/`, the CLI in `scripts/cli/`, the assets. `$CHANTIER` is computed from that
  folder's path.
- The mode is picked when a batch starts: `chief-of-staff.md`, Starting a batch, step 2 proposes
  direct mode (host cannot start a Foreman, or few CRs); `preflight --direct`, `open --direct`.
- The name `/chantier:chantier` appears in `plugin.json`, `marketplace.json`, the docs, the init
  tour and the release notes.

## Batch

To run with the P1 `multi-session-chief-of-staff` in one new batch, in series (user's word,
2026-11-10). Both touch `SKILL.md` and the role a session takes at start.
