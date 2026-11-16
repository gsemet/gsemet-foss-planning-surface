# Change Specification: the Chief of Staff keeps its rules, through compaction

## Goal

After a context compaction, the Chief of Staff keeps only a summary of chantier's cards and acts
against rules it no longer sees. On 2026-11-10, steering batch-09 in direct mode, it grilled while
its batch ran, and it offered the user, on Remote Control, options they could not take (Foreman
mode, a command to run in a terminal, a local URL).

This CR makes three changes, on Claude Code only, with the place for Copilot's ready:

1. **What the steering session may do while its batch runs** is written as the user said it:
   backlog work and the spec-writer yes, grill and touching the batch no.
2. **The rules come back after a compaction:** by hand ("chantier reload") and automatically (the
   plugin's mod, at every compaction), with no new CLI gate.
3. **The options the Chief of Staff offers fit where the user is:** a checklist by environment,
   each option with its reason.

The fix lives in chantier itself (the cards, the skills and the mod), so that it works for every
user: it never relies on an agent's private memory or on this user's setup.

## Decisions carried from `02-answers.md`

| # | Decision | Where it lands below |
| --- | --- | --- |
| D1 | While a batch runs, in either steering mode, all work on the backlog's files is allowed: file, add, triage (directly or on a Griller's request), reorganise, merge items, drop | Area 1 |
| D2 | While a batch runs, touching the running batch is not allowed: no CR joins it, nothing is started (as part of that work) | Area 1 |
| D3 | The card's line that forbids triage while steering is stricter than this and changes | Area 1 |
| D4 | The steering session does not grill while its batch runs ("Pas de grille") | Area 1 |
| D5 | The steering session may start the spec-writer on a CR already grilled (for example by a Griller), on the user's word ("spec writer oui") | Area 1 |
| D6 | The fix lives in chantier (cards, skill, CLI), for every user and every host; not in an agent's memory or this user's setup | Goal; all areas |
| D7 | Manual reload: "chantier reload", in plain text or through the skill | Area 2 |
| D8 | Automatic reload: on Claude Code, the plugin's mod reloads the cards at every compaction, manual or automatic, without relying on the model noticing it | Area 2 |
| D9 | No new CLI gate: the CLI keeps refusing only what touches the batch; the gate asked in `intake/no-grill-while-steering-request.md` is replaced by the reload | Area 2; Out of scope |
| D10 | After an automatic reload, the next answer starts with one line saying chantier's rules were reloaded | Area 2 |
| D11 | Signal first: when the host says where the user is (phone on Remote Control, desktop app, terminal), the Chief of Staff offers only what the user can do from there | Area 3 |
| D12 | When the host says nothing, it offers every option that fits, each with its condition ("from the machine", "from the phone") | Area 3 |
| D13 | A checklist by environment gives each option, where it can be done from, and why | Area 3 |
| D14 | Claude Code only; Copilot is another CR | Area 4; Out of scope |
| D15 | Shared cards hold what holds on every host (the rules of D1 to D5, what a reload reads and does, the general rule for options); the host's reference holds what is the host's (how the automatic reload is triggered, the surfaces and the signal, each option's condition there); `hosts/copilot.md` gets the same sections marked "not done yet" with the reason | Areas 1 to 4 |
| D16 | `add-several-while-paused` is its own P1 CR again; this CR keeps three topics | Out of scope |

## What changes, area by area

All paths are relative to the repository root, `C:/Users/gaeta/Projets/chantier`. Read the files
as they are on `main` when you start (PRs 95 to 97 changed the cards, the tree and the CLI on
2026-11-10).

### Area 1: what the steering session may do while its batch runs

The rule binds the **steering session** of a running batch: the Chief of Staff in direct mode. In
Foreman mode the Foreman steers and the Chief of Staff is not the steering session: it keeps what
it may do today (grill, triage, the spec-writer), and D1, D2 hold for it too. A *paused* batch is
not running: everything below lifts at the pause, as today.

**`skills/chantier/references/chief-of-staff.md`**

- Section "Steering a batch yourself", bullet **"What you accept while you steer"**: rewrite it.
  It says, in this order:
  - Accepted, as today: "status?" and "what did it cost?"; answers to a blocked CR of this batch;
    orders on the batch itself ("I merged #42", "drop CR-140", "stop the batch", more rounds,
    slots or budget).
  - **Backlog work, accepted:** any work on the backlog's files: file (`file`), triage
    (`triage`, on the user's word as always, directly or on a Griller's request), reorganise,
    merge items, drop (`abandon`, on the user's explicit word), record answers and decisions in a
    CR's `02-answers.md` (the "Record at once" rule still holds). `triage --ready` moves a CR to
    `3-ready`; it does not join the running batch.
  - **The spec-writer, accepted:** on the user's word that a CR already grilled (by a Griller, or
    before the batch) is grilled enough, start it as "Backlog and grill" says.
  - **Not while the batch runs:** grill a CR (ask its questions, write its `01-intent.md` from a
    discussion with the user); touch the running batch from backlog work: no CR joins it (the CLI
    already refuses `order add` and `order qa` on a running direct batch), nothing starts that the
    user did not order on the batch.
  - Any other request is noted word for word and handed back when the batch completes; an idea is
    filed in the inbox at once (`file`, no grill). A request to grill keeps its one line: "to
    grill in parallel, fork this session; the fork becomes a Griller" (the fork is the user's
    step; explain it, never do it).
  - Remove "no triage" and "no discussion" from the current sentence "You hold no grill, no triage,
    no demo and no discussion until the batch completes." Keep "no grill". The demo: see Open
    question 1; until it is answered, keep "no demo" as written today.
- Section "Starting a batch", step 2: the sentence "no grill, triage or discussion while the batch
  runs; new ideas go to the inbox" becomes "no grill while the batch runs (backlog work and the
  spec-writer stay open); new ideas go to the inbox".
- Section "Entry points", the row "to file, triage or refine an item": add that while a direct
  batch runs, file and triage stay open and the grill waits for the pause (point to "Steering a
  batch yourself").
- Section "Backlog and grill": the sentence on the spec-writer already says "at any time, a batch
  running or not": keep it.

**Other texts that state the old, stricter rule** (change only the stricter part; "no grill"
stays true):

- `skills/chantier/references/init.md`, "Steering" (about line 44): "hold no grill or discussion
  until the batch completes" becomes "hold no grill until the batch completes (filing, triage and
  the spec-writer stay open)".
- `docs/use-cases-direct.md`, "No grill in the same session" (about lines 24 to 39): the list of
  what the Chief of Staff answers gains the backlog work and the spec-writer of a CR already
  grilled; "Any other request is noted…" and the Griller paragraph stay.
- Unchanged, already true: `skills/chantier/references/session-start.md` ("I hold no grill while
  it runs"), `README.md` (about line 111), `docs/tutorial-claude-code.md` (about line 135), the
  docs diagrams and their `-texts.md` ("no grill while the batch runs").

### Area 2: the reload, manual and automatic

**What a reload reads and does** (shared, every host). Add a section **"5. Reload"** to
`skills/chantier/references/session-start.md` (read by the router, the Chief of Staff and the
Griller):

- **Trigger:** the user says "chantier reload" (plain text, any language around it), or invokes
  the router skill with the argument `reload` (the host's form is in its reference), or the host
  puts the automatic reload's line in the conversation after a compaction (Area 2, host part).
- **What it reads again, whole:** `concepts.md`, `session-start.md`, the card of the session's
  role (`chief-of-staff.md`, or `griller.md`: see Open question 2), the host's reference, and
  `report.md`; while this session steers a direct batch (the seat names this session and the
  active batch's steering is `direct`, from `$CHANTIER status`), also `foreman.md`.
- **What it does:** re-read the seat (as at any skill invocation; a seat that names another
  session makes this session a Griller, as section 2 says). The role is the one the session
  already holds: no role question, no introduction (section 4 is skipped), no first-turn
  preflight report, no title change unless the seat changed the role.
- **What it touches:** nothing in the batch: no order, no epoch claim, no `take`, no heartbeat
  armed or stopped, no Driver started or messaged. Reads only (`$CHANTIER seat`, `$CHANTIER
  status`).
- **What it says:** one short line, in the user's language, that chantier's rules are reloaded;
  then, if a batch is active, the current status in `report.md`'s Progress shape (`status
  --refresh` with no epoch first, as `report.md` says). After an **automatic** reload, that line
  opens the next answer (D10), before whatever answers the user's message.
- A session that holds no chantier role yet (the router never ran, no seat names it, it is not a
  Griller): a reload is the router's start, as with no argument.

**The skills.**

- `skills/chantier/SKILL.md` (the router):
  - `description`: add that it is also used when the user says "chantier reload". The skill
    descriptions stay in the context through a compaction: this is what makes the plain-text
    phrase work when the cards are gone.
  - Body: a line before the seat bullets: with the argument `reload`, or on the words "chantier
    reload", follow `session-start.md` section "5. Reload" and do nothing else of this file (ask
    no role).
- `skills/chief-of-staff/SKILL.md` and `skills/griller/SKILL.md`: one line each: "chantier reload"
  follows `session-start.md`, "Reload". (They already read `session-start.md`.)
- `skills/status/SKILL.md`: unchanged (it reads only `report.md`).

**The automatic reload on Claude Code** (host part).

`hooks/register.tsx` (the mod) gains a hook on the engine's `session.compact` event (it exists in
the engine: `trigger` `manual` or `auto`, `agentId`, optional `instructions`, a result of
`{ messages, … }` or `{ skip }`; confirm the exact contract in the engine's
`claude-code/index.d.ts`, as `CONTRIBUTING.md` says, before writing it):

- It acts only on the main loop's compaction (no `agentId`: a Driver's or worker's own compaction
  is untouched) of a session that loaded a chantier role skill. The mod already sees each
  `skill.prompt`: record there, in a session atom (`atom(...)`, as `site`, `feed`, `pages`), that
  this session loaded `chantier`, `chief-of-staff` (and `griller`, per Open question 2). `status`
  does not count.
- Both triggers: `manual` (`/compact`) and `auto`.
- It never vetoes (`skip`) a compaction, and changes nothing else of it.
- **The reload must be in the conversation after the compaction by the hook's own act, not left to
  the summarizer or to the model's noticing (D8).** The way: call `next(e)`, then add to the
  `messages` it returns one message that is the automatic reload's line, for example:
  `chantier reload (automatic, after a compaction): follow session-start.md, "5. Reload"; start
  your next answer with one line saying chantier's rules were reloaded.` The model then runs the
  same procedure as the manual reload, through the router skill. Adding a matching line to the
  summarizer's `instructions` before `next(e)` is allowed on top, never instead.
- If the engine's contract gives the hook no way to put that line in the compacted conversation,
  the CR is blocked: hand back with the engine's exact text (no fallback, no look-alike).
- The mod's existing rules hold: it writes nothing on disk and runs no process but `git
  rev-parse`. The CR board's behaviour is unchanged.
- `hooks/register.test.tsx`: tests in the file's style (`world(on)`, the engine's own `on`):
  1. after `$.skill.prompt({ skill: 'chantier:chief-of-staff', … })`, a `session.compact` with
     trigger `auto` returns messages whose last one carries the reload line; the same with
     trigger `manual`;
  2. a session that loaded no chantier skill (or only `status`): the compaction's messages are
     unchanged;
  3. a compaction with an `agentId`: unchanged;
  4. the hook never returns `skip`.
- `types/index.d.ts`: extend only if the new atom's value needs a type there.

**The host references.**

- `skills/chantier/references/hosts/claude-code.md`:
  - Tools table, row "The skills": add `/chantier:chantier reload` (the router with the argument
    `reload`), mark documented (the skills page), and "unproved until a reload runs" for the
    argument's handling; trial: type it after a `/compact`, see the one line and no introduction.
  - New section **"Reload after a compaction"** (next to "Compacting"): the mod's `session.compact`
    hook adds the reload line after every compaction, manual or automatic, of a session that
    loaded `chantier` or `chief-of-staff`; what it does not touch (a subagent's compaction). Mark
    it **unproved** until seen: the trial is a Chief of Staff session, `/compact`, then the next
    answer opens with the reload line and the cards are read (tool calls visible). Say also that
    the mod is Claude Code's only (as `CONTRIBUTING.md` says), so the automatic reload exists only
    where the plugin's mod loads.
  - Section "Compacting": the line to copy that the Chief of Staff gives with the compact
    command (chief-of-staff.md, "Compacting") no longer needs to say "reload the cards"; nothing
    else changes there.
- `skills/chantier/references/hosts/copilot.md`: see Area 4.

**No CLI change.** `rails.py`, `commands.py` and the other CLI files are untouched: the CLI keeps
refusing only what touches the batch (D9).

### Area 3: the options offered, by environment

**The general rule** (shared). Add a section **"Offering options"** to
`skills/chantier/references/chief-of-staff.md` (after "While it runs", before "Steering a batch
yourself"):

- Before offering the user an option, check where they can take it from: the phone on Remote
  Control, the desktop app, a terminal. Where the user is comes only from the host's signal, as
  the host's reference describes it; never guessed.
- **The host signals where the user is:** offer only what the user can do from there. When no
  option fits, say so, and why; never offer one they cannot take.
- **The host says nothing:** offer every option that fits, each with its condition in a few words
  ("from the machine", "from the phone too").
- Something the Chief of Staff can do itself (run a command, send a file) is done, or it says it
  cannot and why; it is not handed to a user who has no shell.
- The checklist, generic (what an option needs, and why); each host's reference gives the
  condition on that host:

  | Option | It needs | Why |
  | --- | --- | --- |
  | Switch to Foreman mode | a Foreman session the user can see and steer, or one to reuse | the Foreman is a separate session |
  | "Run this command in a terminal" | a shell on the machine | otherwise the Chief of Staff runs it, or says it cannot and why |
  | Open a local URL or a file path | the machine | send the file or a forge link instead |
  | A host command that opens a terminal dialog | a terminal | the app and a remote view have no such panel; use the app's own UI |
  | Restart the app, reload the plugins, open a file in an editor | the machine | |
  | Review renders, review and merge a PR | the forge, from any device | never refused |
  | A host feature (a scheduled wake, start a session, a monitor) | the host to have it in this session | no fallback: say it is missing, offer no look-alike |
  | Work in the main checkout | no eval running, a session on the main checkout | the project's rules (an eval leaves the main checkout untouched); fail fast |

- Pointers: the Tips bullet of "While it runs" and the "For you" block follow this section.
- `skills/chantier/references/report.md`, "Tips": add that a tip never names what the user cannot
  take from where they are (the host's signal), next to "never a command the host refuses in this
  session". (`/chantier:status` reads only `report.md`: the sentence must stand alone there.)

**The Claude Code part.** Add a section **"Surfaces and options"** to
`skills/chantier/references/hosts/claude-code.md` (after "Classes of session"):

- The surfaces: the phone (or another device) on Remote Control; the desktop app typed at the
  keyboard; a terminal (CLI).
- How the host signals the surface: the desktop app adds a Remote Control notice to the
  conversation when the user works through Remote Control (proved 2026-11-10, Battlestation: said
  at each turn's end that day). A terminal gives no signal, and no signal is said when the user is
  at the desktop app's keyboard: the absence of the notice does not prove the user is at the
  machine (the session's class row "no Remote Control notice" says "desktop, typed", which this
  section qualifies). Mark the rest unproved.
- The table, one row per option of the shared checklist, one column per surface, each cell "yes",
  "no" or the condition, and the reason. From the intake draft and the cards:
  - Switch to Foreman mode: desktop typed yes; Remote Control only by reusing a Foreman (as
    "Switching to Foreman mode" says), else no; terminal no (preflight P1 fails).
  - Run in a terminal: desktop and terminal yes; Remote Control no.
  - Open `localhost` or a path: desktop and terminal yes; Remote Control no (send the file, or a
    forge link).
  - `/permissions`, `/config`: terminal yes; desktop app and Remote Control no (the app's own
    settings UI).
  - Restart the app, `/reload-plugins`, open in an editor: desktop yes (terminal: restart the CLI);
    Remote Control no.
  - `/chantier-board`: desktop and terminal; the pane does not show in a Remote Control view
    (`README.md`, the CR board).
  - Review renders, merge a PR: every surface.
  - A host feature (scheduled wake, start a session, a monitor): where the host has it;
    `start_session` is refused on Remote Control (the classes table).
  - Work in the main checkout: not during an eval, not from a worktree session (the classes table).
  Mark each row proved, documented or unproved as the file's other sections do; a row taken from
  the intake draft with no dated trial is unproved, except where the classes table already proves
  it.

### Area 4: the place for Copilot

`skills/chantier/references/hosts/copilot.md` gets the same sections, with the same titles, each
saying **"Not done yet"** and the reason, so the later Copilot CR fills them and moves nothing:

- **"Reload after a compaction":** not done yet: this CR covers Claude Code only (the user's
  choice, 2026-11-10); Copilot has no mod (its manifest names no hooks) and its own way to react to
  a compaction is not known. Until then the manual reload ("chantier reload") is the only one, and
  the Chief of Staff names no compacting command (the "Compacting" section holds).
- **"Surfaces and options":** not done yet: how Copilot signals where the user is is not known;
  until then the Chief of Staff offers every option, each with its condition (the shared rule's
  "the host says nothing" case).
- Tools table, row "The skills": how Copilot passes the argument `reload` is not known (unproved),
  as for `direct`.

### Area 5: the contributor and user docs

- `CONTRIBUTING.md`, "How the project is built", point 4 (the mod): it hooks `skill.prompt`,
  `session.compact` (the automatic reload), the `/chantier-board` command and the `cr-board` pane;
  it still writes nothing and runs no process but `git rev-parse`.
- `README.md`:
  - the "Use" table: a row "chantier reload" (`/chantier:chantier reload`): the session reads
    chantier's rules again, typically after a compaction; on Claude Code the plugin also does it by
    itself at every compaction;
  - the tree line `hooks/, types/ ← Claude Code only: the CR board mod and its contract`: add "and
    the reload after a compaction".
- No version change (the release does it), no change to `agents/` or `com.github.copilot/agents/`
  (no role's body changes), no change to the docs diagrams.

## Out of scope

- **Any CLI change**, and in particular the CLI gate asked in
  `intake/no-grill-while-steering-request.md` (refusing grill steps from the steering session):
  replaced by the reload (D9).
- **Copilot's own behaviour** (its automatic reload, its surface signal, its option conditions):
  another CR, which only fills the sections of Area 4 (D14).
- **Adding several CRs to a paused batch** (`add-several-while-paused`): its own P1 CR, with its
  grill (D16). Its intake files stay here as history; nothing of them is implemented here,
  including the text of the "a running direct batch is strict" refusal.
- The Foreman's own options and reload: the Foreman does not talk to the user; not asked.
- Drivers' and workers' compactions: untouched by the hook.

## Evidence

Run at the pushed head, with their output kept in the PR's evidence:

1. `just check` (structure tests), green on Linux, macOS and Windows in CI. In particular
   `test_each_host_has_its_reference_and_the_cards_hold_no_host_tool` stays green: the shared cards
   (`chief-of-staff.md`, `session-start.md`, `report.md`, `concepts.md`, `griller.md`) name no host
   tool or command (`/compact`, `/chantier:…` slash forms and `/permissions` live in
   `hosts/claude-code.md` only); `test_skill_and_references_links_resolve` stays green for every new
   link; `test_four_skills_the_router_and_three_thin_ones_listed_by_copilot` stays green.
2. `just scenario` (the cards changed): green.
3. The mod, with the session's own `claude` binary (`CONTRIBUTING.md`, "Daily work"):
   - `claude plugin validate .`: no new error (the two known warnings only);
   - `claude plugin test .`: the four new tests of Area 2 and every existing test pass;
   - `tsc -p <folder>` as `CONTRIBUTING.md` describes: no error.
4. A text check, shown with its output: `rg -n "no triage|no discussion|grill, triage or discussion|grill or discussion" skills docs README.md`
   finds nothing.
5. A live trial cannot run before the merge: the plugin loads from the main checkout, not from a
   worktree (`AGENTS.md`). The PR says so, and the marks of Area 2 stay unproved. After the merge,
   on the user's word: `/chantier:chief-of-staff`, then `/compact`; the next answer opens with the
   reload line and the cards are read; then "chantier reload" in plain text does the same with no
   introduction. The result, dated, turns those marks to proved in a later change.

## Open questions

1. **The demo while the steering session's batch runs.** The answers name grill (no), backlog work
   (yes) and the spec-writer (yes); the intent removes "no triage" and "no discussion" but says
   nothing of the demo. Keep "no demo" while a direct batch runs (recommended: the demo guides the
   user through the batch's own stack, which is touching the batch), or allow it?
2. **The Griller.** The CR is about the Chief of Staff. Does the reload cover a Griller session
   too: the manual "chantier reload" reading `griller.md`, and the automatic reload after a
   Griller's compaction? Recommended: yes for both (same rules lost, same fix, no cost), which this
   specification already writes as an option in Area 2.
