# Change Specification: boot mode by surface, README rework and the board's docs

One CR, one PR, in three parts (the user, 2026-11-12, "Met une CR"): the mode a Chief of Staff's
batches use follows the surface unless forced; the README is reworked; the CR board mod is
documented with the user's screenshots. Sources: `intake/request.md`, `01-intent.md`,
`02-answers.md` (an advisor's answers given in the user's place on the user's word of 2026-11-12,
plus the user's own two answers at its end). No tracker issue.

## Goal, in the user's terms

- `/chantier:chief-of-staff` with no argument: Foreman mode in a local session at the desktop,
  direct mode under Remote Control (and wherever a Foreman cannot start). Two arguments force one:
  `foreman` or `direct`.
- The README says that everything starts with a new session and one boot skill,
  `/chantier:chief-of-staff`, with or without an argument; it opens "Planning modes" on what a CR
  is and "Batch modes" on why batches exist; "Releases" shows how far a project's procedure can go;
  a new section shows the CR board; "What is chantier?" and "Repository layout" move to
  `CONTRIBUTING.md`.
- The CR board mod gets a real docs page, with pictures: what it is, how to open it, how to read it.

## Part 1: the mode by surface

### The rule (decisions of 02-answers.md)

1. **The argument.** Only the invocation's first word counts, and only when it is exactly
   `foreman` or `direct`. Anything else (`init`, `prepare yourself…`, `Run the campaign…`) is the
   user's request and forces nothing. `/chantier:chief-of-staff direct Run the campaign …` is
   `direct` plus a request.
2. **Forced holds for the session.** `foreman` or `direct` holds for every batch of the session
   until the user's word changes it. The user's word ("you are in direct mode", "use a Foreman")
   keeps working with or without an argument, and also holds for the session (today's rule for
   `direct`, extended to `foreman`).
3. **No argument: the mode this surface can run.** Read at the plan of each batch, never frozen at
   the invocation (the known path to a remote Chief of Staff is "start locally, then turn on Remote
   Control", so a session started at the desk and later driven from the phone must plan its next
   batch as direct):
   - **direct** when the conversation carries the host's Remote Control notice
     (`hosts/claude-code.md`, "Surfaces and options"), even if a Foreman could be reused;
   - **direct** on every host that cannot start a Foreman: a terminal, VS Code, and on Copilot a
     session where the session tools do not load. The test is the one the card already has: the
     Foreman-mode preflight's P1 (`$CHANTIER preflight`, host is Claude Desktop or a Copilot agent
     session) and P2 (the host's session tools load: `start_session` on Claude Code;
     `create_session` and `send_message` on Copilot). This reconciles the two answers on Copilot:
     a Copilot host that can start a Foreman session (the SDK host) runs Foreman, one that cannot
     runs direct; how Copilot passes the argument stays **unproved**;
   - **Foreman** otherwise. No notice means local: a missing notice fails safe to Foreman, and
     where no Foreman can start the bullet above applies.
4. **The plan says it, no question.** The plan states the mode and why in one line ("direct: this
   session is under Remote Control", "Foreman: at the desktop", "direct: forced by the argument")
   and, when direct, what that changes (no Foreman session; the Chief of Staff steers the Drivers;
   no grill while the batch runs, backlog work and the spec-writer stay open; new ideas go to the
   inbox). There is no separate yes for the mode: the go is the yes. The user may still change the
   mode before the go by saying so.
5. **A forced `foreman` where no Foreman can start** (Remote Control with no Foreman to reuse, a
   terminal, VS Code) is refused at the plan, with the reason and what the user can do (say
   "direct", or start from the desktop app). Under Remote Control with a Foreman to reuse, it reuses
   it (`hosts/claude-code.md`, "Reusing the last Foreman"). A forced mode is never swapped silently
   (no fallback).
6. **`direct` stays allowed locally**, unchanged (small batches, the `real-direct` eval).
7. **A batch keeps the steering it was opened with.** Going to the phone or coming back changes no
   running or paused batch. "Switching to Foreman mode" stays the user's word, unchanged; a Foreman
   batch never becomes direct. A Foreman batch followed from the phone keeps working through orders.
8. **The introduction** (first turn) says which mode this session would use now, and why, in the
   "Direct or Foreman" bullet.
9. **The router** (`/chantier:chantier`) asks two roles only: the Chief of Staff or a Griller. It
   loads `chief-of-staff` with no argument, and the mode follows the surface.
10. **Unchanged:** a cloud session (no main checkout, stops at the start checks); the CLI (no
    command, no flag, no surface detection: `open --direct` and `preflight --direct` stay the only
    switches, set by the Chief of Staff); no new skill (`foreman` and `direct` are arguments of the
    one entry).

### Files

- `skills/chief-of-staff/SKILL.md`: the description's last sentence and the body's last paragraph
  say: with no argument the session's batches follow the surface (Foreman at the desktop, direct
  under Remote Control or where no Foreman can start); a first word `foreman` or `direct` forces
  one for the session; the user's word changes it; pointer to `chief-of-staff.md`, "Starting a
  batch". The description's "(Foreman mode on Claude Desktop or a Copilot SDK host, direct mode
  anywhere)" stays true and may stay.
- `skills/chantier/SKILL.md`: the description ("the Chief of Staff (with a Foreman, or in direct
  mode) or a Griller") and the first bullet ask two roles, Chief of Staff or Griller, and load
  `chief-of-staff` with no argument or `griller`. Remove "(with the argument `direct` for the
  second)".
- `skills/chantier/references/chief-of-staff.md`:
  - the table row "a batch, …": "the mode comes from the session" becomes "the mode: forced by the
    argument or the user's word, else the surface (Starting a batch)";
  - "Starting a batch", step 1: the mode is settled before the preflight. Forced `direct`, or no
    argument under the Remote Control notice: `$CHANTIER preflight --direct` (P2 left out, as
    today). Otherwise the Foreman-mode preflight runs; with no forced mode, a failure of P1 or P2
    alone makes the mode direct and `preflight --direct` then runs and is the batch's preflight;
    with `foreman` forced, that failure is the refusal of rule 5. Any other failure stops as today;
  - step 2: replace the paragraph from "The steering mode is the session's" to "Wait for the user's
    yes." with rules 1 to 5 above, in the card's style. Drop "propose direct mode … Wait for the
    user's yes": the plan says the mode and why in one line and the go is the yes;
  - "Switching to Foreman mode": unchanged.
- `skills/chantier/references/session-start.md`:
  - section 4, the "Direct or Foreman" bullet: add one line, which mode this session would use now
    and why (forced, Remote Control, a host that cannot start a Foreman, or the desktop), and that
    `foreman`, `direct` or the user's word changes it. Leave the rest of the bullet as it is (see
    Out of scope);
  - section 2's table and the remote line of section 4: unchanged unless a word contradicts the
    two-role router.
- `skills/chantier/references/init.md`, the "Steering" bullet: "Direct mode is used where the host
  cannot start a Foreman session or for a small batch; the plan names it and the user's go approves
  it" becomes: used where the session is under Remote Control or the host cannot start a Foreman
  session, or when the user forces it (`direct`, or says so); the plan names it and why, the go
  approves it.
- `skills/chantier/references/hosts/claude-code.md`:
  - "Tools", the skills row: `/chantier:chief-of-staff [foreman|direct]`; the argument's handling
    (first word only) stays **unproved** until a session shows it (the `real-direct` eval already
    passes `direct` first: if its report proves the argument was read, mark it so with its date);
  - "Classes of session": one sentence under the table: with no argument the Chief of Staff's
    batches are direct in the Remote Control row and on any entry where the Foreman-mode P1 fails
    (terminal, VS Code), Foreman in the "Desktop, typed" row (`chief-of-staff.md`, "Starting a
    batch");
  - "Surfaces and options": say that the notice now also sets the mode of a batch planned with no
    argument. Add the mark: whether the notice appears on a turn typed at the desktop in a session
    connected to Remote Control (the setting "Connect new sessions to Remote Control") is
    **unproved**; trial: in such a session, type one turn at the desktop and one from the phone,
    and record which carries the notice. Until then the rule holds as written and a forced
    `foreman` is the user's way;
  - "For you", "A Chief of Staff and Grillers in remote", step 2: "In remote, reuse this session,
    in direct mode" becomes: in remote, reuse this session; with no argument its next batch is
    direct by itself.
- `skills/chantier/references/hosts/copilot.md`, "Tools", the skills row: "how Copilot passes the
  argument `foreman` or `direct`, or the argument `reload`, is not known (unproved)". Add in
  "Surfaces and options": with no Remote Control signal known on Copilot, the no-argument mode
  follows P1 and P2 only (rule 3), unproved.
- `agents/`, `com.github.copilot/agents/`, `hooks/`, `types/`, the CLI: no change.

## Part 2: the README and CONTRIBUTING

### README.md, top to bottom (the user's order, open question 2)

1. **The bullets.** Keep them. The "Direct or Foreman" bullet says the mode follows where you are
   (Foreman at the desktop, direct from the phone under Remote Control, or in a terminal or VS
   Code), and `foreman` or `direct` forces one. Keep its two other points (a CR added while the
   batch runs waits for a slot; Foreman mode leaves the Chief of Staff free to grill).
2. **How Chantier works** (keep the heading). Opens with: everything starts with a new session and
   one boot skill, `/chantier:chief-of-staff`, with or without an argument; with none, the mode
   follows the surface; `foreman` or `direct` forces one. Then the three diagrams as today. The
   Foreman paragraph names `/chantier:chief-of-staff` at the desktop, or `… foreman`; the direct
   paragraph names `/chantier:chief-of-staff` under Remote Control, in a terminal or VS Code, or
   `… direct`. Under the direct paragraph: the picture `docs/direct-mode-session.png` (alt text
   saying a direct batch: the Chief of Staff's transcript, its Drivers and a Verifier in the
   Background tasks, the CR board), a one-line caption that the Drivers run straight from the
   current session, and the line: while the batch runs, the Chief of Staff in direct mode declines
   to grill new requests and points you to a separate Griller session (`/chantier:griller`). Keep
   "The difference that matters most" paragraph.
3. **Planning modes** (keep the heading: `docs/planning-folder.md` links `#batch-modes`, keep the
   anchors stable). Opens with the user's text, its content and order in the README's plain
   English: Chantier works on Change Requests, a folder of Markdown files describing what you want.
   It starts from an intent, written by hand or taken from a Jira, GitHub or GitLab issue, and the
   Chief of Staff helps you turn it into a Change Specification. Then "Chantier plans in one of two
   places, the planning folder:" and the rest of the section unchanged.
4. **Batch modes** (keep the heading). Opens with the user's why, in plain English: Chantier is
   meant to work a set of changes and deliver them in coordination. Most of the time you plan a set
   of CRs ahead and build a batch: for instance you grill during the day and chantier implements
   the whole batch on its own overnight, up to a ready-to-merge PR/MR stack. Then "A batch has one
   of three modes. …" and the rest unchanged.
5. **Change Requests Lifecycle** and **Detailed lifecycle**: unchanged.
6. **Releases**: keep the first paragraph's facts and the `release-driver.svg` picture. Add: a
   release procedure ranges from a simple package publish (PyPI, npm) to a long procedure, and the
   Release Driver and the Chief of Staff follow the project's own. Example, written as one
   project's own procedure that the Release Driver follows with the tools its session has, each
   irreversible step on your approval (never a claim that chantier ships a publisher): a project
   that publishes to GitHub Pages and to a marketplace creates the release and its notes, puts them
   up for review, follows the release pipeline, waits for the marketplace to publish (about ten
   minutes on the VS Code marketplace, an order of size), publishes the release notes and the
   announcement thread on X/Twitter, then holds a retro that improves the procedure, which stays
   written and maintained in the project.
7. **The CR board** (new section): two or three lines on what it is (a read-only pane of Claude
   Code over the planning folder, opened by `/chantier-board` or by loading the Chief of Staff),
   the picture `docs/board-mod-batch.png`, and a link to [`docs/boards.md`](docs/boards.md).
8. **Install**: the entries paragraph says `/chief-of-staff` makes the session the Chief of Staff,
   its mode following the surface (`/chief-of-staff foreman` or `/chief-of-staff direct` to force
   one), and `/chantier` asks Chief of Staff or Griller. Rest unchanged.
9. **Use**: the row "run the P1s, …": "a Foreman starts on your go, or the Chief of Staff steers in
   direct mode, as the plan says (the surface, or your `foreman` / `direct`)". Rest unchanged.
10. **More**: the Boards line stays; **Develop**: unchanged.
11. **Removed**: "What is Chantier?" and "Repository layout". Nothing of them is copied back: the
    new "Planning modes" opening and the tutorial link cover the CR's files, the grill and the
    spec-writer. The README keeps two pictures only (`board-mod-batch.png`, `direct-mode-session.png`)
    besides the diagrams. This reverses CR-195's "What is Chantier? stays in the README", on the
    user's later word.

### CONTRIBUTING.md

Under "How the project is built", as `###` subsections: "What is chantier?" first (before "chantier
is four things"), "Repository layout" after the "no fallback" paragraph. Moved as they are, with
their links fixed for the new place: `[series or a stack](#batch-modes)` becomes
`[series or a stack](README.md#batch-modes)`; check every other link resolves from the root. One
sentence is brought in line with Part 1, else the moved text would contradict it: item 3's "(proposed
when the host cannot start a Foreman session, or the batch is small)" says instead that direct mode
is used under Remote Control, where the host cannot start a Foreman session, or when you force it.
The layout's `docs/` line may add "screenshots".

## Part 3: the board's docs

### Screenshots

Copy, byte for byte, from `intake/screenshots/` to `docs/` beside the diagrams, keeping their names:
`board-mod-batch.png`, `board-mod-batch-prs-light.png`, `board-mod-waiting-light.png`,
`board-mod-merged-light.png`, `board-mod-batch-done.png`, `direct-mode-session.png`,
`status-report-done.png`. The intake is never edited. `direct-mode-session.png` is published whole,
as sent (it shows the public eval sandbox's name, the context use and the model; nothing private).

### docs/boards.md, enriched

The same page (the README's "More" list and the cards already link it); the remote board keeps its
section. "The CR board (Claude Code)" becomes:

- **What it is:** a Claude Code mod (early access) that shows a read-only pane over the planning
  folder's `STATUS.json` (one section per project in a surface): the live batches, the backlog (and
  `3-ready`), the merged and trashed CRs. Nothing of it on Copilot; not shown in a Remote Control
  view (keep the issue link). It writes nothing and runs no process but `git rev-parse`.
- **How to open it:** `/chantier-board` shows or hides it; loading the `chantier` or
  `chief-of-staff` skill opens it too (not `griller`).
- **How to read it**, from the screenshots: the header line (`5 live · 0 waiting for you · read 0s
  ago`); each batch line (its id, cost / budget, a gauge), its unread asks, its slots (`Slots 3/3,
  0 free`); "Waiting for you" and "In progress" with the columns CR, Subject, State (state, step and
  round: `working Round 1/3`, `working CI 2/3`, `ready Notify 1/3`, `queued`), PR, Cost; then
  Backlog, Merged (n of m), Trashed (n of m). Press a CR for its sheet and its documents. It
  refreshes every 15 seconds while open.
- **A batch in pictures**, in this order, each with one line: `board-mod-batch.png` (just opened:
  three CRs working round 1/3, two queued, no PR, no cost), `board-mod-batch-prs-light.png` (three
  CRs in CI with PRs #1 to #3 and their costs, $0.57 of $20), `board-mod-waiting-light.png` ("3
  waiting for you": two CRs ready, and one unread ask), `board-mod-merged-light.png` ("Merged (2 of
  2)" open), `board-mod-batch-done.png` (0 live, $9.22 of $20, "Merged (5 of 5)" with each CR's PR
  and cost).
- **Two facts the pictures raise**, said so they do not read as bugs: the header's "waiting for
  you" counts the unread asks as well as the table's rows (`board-mod-merged-light.png`: "1 waiting
  for you" beside "Nothing waits for you"); the batch's cost is priced when the steering session
  refreshes the status, not live ($0.57 over three pictures while the CRs moved on, then $9.22 once
  the batch was done).
- Keep the last paragraph (the mod's guard of a worker's writes) as it is.

This CR documents the pane as it is at its merge. It does not wait for `board-refresh-button`, nor
the reverse (no `depends.json`): the second to merge rebases its lines of `docs/boards.md`.

### status-report-done.png

Not in the README. It goes in `docs/tutorial-claude-code.md`, section 6 "Follow and steer" (after
the table, captioned as what "status?" or `/chantier:status` gives once a batch is done: the CR
table with result, PR, rounds and cost, the notes, the cost by role with the orchestration share,
the spend outside the batch, the cost notes), and in `docs/costs.md` (after its second paragraph,
as an example of the report's cost tables).

## Part 4: the other docs, the diagrams and the evals

Every place that says the plan "proposes direct mode" or that `direct` is the only way to direct
mode says the new rule instead (no argument: the surface; `foreman` / `direct` force one):

- `docs/use-cases.md`: the paragraph under the configuration table (lines 24-27); "A Chief of Staff
  and Grillers in remote" step 2 ("In remote, reuse that session: with no argument, its next batch
  is direct"); "When chantier says no" (with no argument, direct mode is used where a Foreman
  cannot start; a forced `foreman` there is refused with the reason).
- `docs/use-cases-direct.md`, the paragraph at lines 10-12; `docs/use-cases-foreman.md`, the
  paragraph at lines 10-14 (no argument at the desktop, or `/chantier:chief-of-staff foreman`).
- `docs/hosts.md`, lines 12-13 and 16-17.
- `docs/tutorial-claude-code.md`: "You need" (line 9-10), section 3's note on the entry (line 68:
  with no argument the mode follows where you are; `foreman` or `direct` after it forces one),
  section 5 (the plan names who steers and why; drop "or the batch is small"), "If something goes
  wrong" (the terminal or VS Code: direct mode is used there with no argument; a forced `foreman`
  is refused with the reason).
- The two simple diagrams and their texts, the entry line only: `how-chantier-works-simple-foreman.svg`
  and `-texts.md` show the desktop entry with no argument or `foreman` (for example
  `/chantier:chief-of-staff · desk or foreman`); `how-chantier-works-simple-direct.svg` and
  `-texts.md` show no argument under Remote Control or `direct` (for example
  `/chantier:chief-of-staff · remote or direct`). The SVG line must fit its 440-pixel box; the
  `-texts.md` and the SVG say the same. No other diagram changes (`how-chantier-works.svg` keeps
  `/chantier:chief-of-staff · direct`, still true).
- `evals/real-foreman/RUNBOOK.md` and `evals/full/RUNBOOK.md`: the start line becomes
  `/chantier:chief-of-staff foreman Run the chantier eval campaign …`, so an eval never depends on
  whether Remote Control happens to be on. `evals/real-direct/RUNBOOK.md` keeps `direct`.
- `.github/plugin/plugin.json`: its description names no mode; no change needed.

## Out of scope

- The CLI: no command, no flag, no surface detection.
- A new skill.
- A batch's steering once open; "Switching to Foreman mode" unchanged.
- The board's code (`hooks/`): the Refresh button is `board-refresh-button`.
- New diagrams; any diagram change beyond the entry line of the two simple ones.
- The remote board (`chantier board`) and the cost's freshness itself (`status-spend-age`, P3).
- The gap between `session-start.md`'s introduction ("in direct mode a CR joins only once every
  other CR is handled and the batch is paused"), `use-cases-direct.md` and the tutorial on one side
  and the README on the other ("queued and taken when a slot frees"): noticed, not this CR's; its
  sentences are left as they are.
- The card's line to a user who asks to grill during a direct batch ("fork this session; the fork
  becomes a Griller"): unchanged; the README's "a separate Griller session (`/chantier:griller`)"
  says the same in the user's terms.
- No version bump (`just version` is the release's).

## Evidence

Gates (`AGENTS.md`, answered): `just check` and `just scenario`, both passing at the pushed head,
their output in the PR. Not `just mod`: nothing under `hooks/` or `types/`.

Checks, each a command run at the pushed head with its output:

1. `just check`: among others, `test_skill_and_references_links_resolve` resolves every link and
   image of the README, the docs and the cards, so the seven PNGs exist under `docs/`.
2. `just scenario` passes (the cards change; the CLI does not).
3. The screenshots are copies: the SHA-256 of each `docs/<name>.png` equals that of
   `intake/screenshots/<name>.png` (for example `Get-FileHash` or `sha256sum` on both).
4. No old wording left: a search of `README.md`, `CONTRIBUTING.md`, `docs/*.md` (release notes
   excluded), `skills/` and `evals/*/RUNBOOK.md` for "proposes direct", "propose direct",
   "proposed when", "or the batch is small" and "Chief of Staff in direct mode, or a Griller" finds
   nothing.
5. The README holds no "What is Chantier?" nor "Repository layout" heading; `CONTRIBUTING.md` holds
   both under "How the project is built", and each of their relative links resolves from the root
   (checked by hand or a one-off script: `CONTRIBUTING.md` is outside the link test).
6. The README's headings, in order: How Chantier works, Planning modes, Batch modes, Change
   Requests Lifecycle, Detailed lifecycle, Releases, The CR board, Install, Use, More, Develop; the
   anchors `#batch-modes` and `#change-requests-lifecycle` still resolve.
7. `evals/real-foreman/RUNBOOK.md` and `evals/full/RUNBOOK.md` start with
   `/chantier:chief-of-staff foreman `; `evals/real-direct/RUNBOOK.md` with
   `/chantier:chief-of-staff direct `.
8. The two simple SVGs open in a browser with the new entry line inside its box (a rendered PNG in
   the CR's `evidence/`), and each `-texts.md` matches its SVG.

The behaviour (the mode at the plan) is a card change no scenario step drives (the scenario has no
model). Its proof is the next real session; the Verifier reads the changed cards against rules 1-10
above and reports any rule not carried.

## Open questions

None. The two questions with user impact were answered by the user on 2026-11-12 ("proposition
validee", "boot-mode-by-surface : ok").
