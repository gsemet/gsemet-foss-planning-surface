# Change Specification: multi-session-chief-of-staff

Several chantier sessions on one repository: one Chief of Staff, Grillers beside it, and the
skills that start each role.

Sources: `intake/request.md` (the Mac CR and the user's words of 2026-11-08),
`intake/request-skill-entry-points.md` (the user's words of 2026-11-10), `01-intent.md` and
`02-answers.md` (both CRs, the second appended under "Merged from skill-entry-points"). Base:
v0.8.0 (`d670e24`). Where an answer was refined later, the later one rules: answer 9 and Q7
reconcile the two grills; answer 10 (a Griller in a worktree) refines answer 6; Q3 (the router
asks) refines answer 2 for `/chantier:chantier` only (D25). The specification's open questions were
answered on 2026-11-10 (`02-answers.md`, last section): D24 to D29.

## Goal

In the user's terms: open several sessions on the same repository and run chantier in each. The
first is the **Chief of Staff** ("chef de chantier"); every other is a **Griller** that refines,
reorders and specifies the inbox and the backlog with the user, with no nested sessions, which is
simpler in remote. Only the Chief of Staff launches and arranges batches: it always has the last
word. Each session says its role at once and renames itself `[env] Project [role]`. The user
picks the role by the skill they invoke (`/chantier:chief-of-staff`, with `direct` for direct
mode, or `/chantier:griller`), or by their word at any time; `/chantier:chantier` stays as a
router that asks. A session that would be blocked later (a linked worktree) says so in its first
message, not at the go. Keep it **simple and flexible**: rules, not procedures; the models judge
the rest.

## Words (new, into `concepts.md`)

- **Griller:** a session that keeps the inbox and the backlog with the user (file, triage, grill,
  answers, specification) and may prepare work for the Chief of Staff. It opens no batch, sends
  no order, steers nothing, closes nothing, merges nothing. Usually short: started for a few
  items, it ends quickly.
- **The Chief of Staff's seat:** a small file kept by the CLI, `.agents/changes/seat.json`, that
  names the repository's Chief of Staff session: its session id, its transcript id, the
  environment, the title and the link. It records no date: no activity date is ever taken as
  proof of life. The host says whether the seat's session is alive.
- **Session title:** `[env] Project [role]` (Area 2, "Titles").

## Decisions carried from `02-answers.md`

| # | Decision | Answer | Where |
| --- | --- | --- | --- |
| D1 | The second role is **Griller** (not Planner); it refines, reorders and rearranges inbox and backlog, may prepare work for the Chief of Staff; short sessions; the Chief of Staff has the last word on launching and arranging batches; in direct mode too; motivation: no nested sessions in remote | 1, Q1 | Areas 2, 3, 4 |
| D2 | `/chantier:chief-of-staff` with no other active session: the session says it is the Chief of Staff and renames itself, no question | 2, 9 | Area 2 |
| D3 | Same skill in a second session, a Chief of Staff active and **no batch active**: the same opening, ending with one message in the user's language: "a Chief of Staff is already active at <link>; I become a Griller: I will not follow the batches actively, but I can help refine the backlog's ideas", then one option only: say "become chief of staff" to take over | 2, 3, 9 | Area 2 |
| D4 | Same, **with a batch active**: the session asks whether the user is sure they want the hand-over to this session (D8's rules then apply) or only want to grill CRs | 9, Q7 | Area 2 |
| D5 | `/chantier:griller`: a Griller, no question | 9, Q1 | Areas 1, 2 |
| D6 | The seat: a small CLI-kept file in `.agents/changes/` (session id, environment, title, link); no date as proof of life; the host says whether the seat's session is alive (`references/hosts/<host>.md`), extensible to Copilot and others | 3 | Areas 2, 7, 8, 9 |
| D7 | The host cannot tell, or the seat's session looks stopped: never take the seat alone; one line, "the Chief of Staff at <link> looks stopped; shall I take its place?" | 3 | Area 2 |
| D8 | Hand-over: encode only the rules. A running Driver is never stopped nor moved to another session. On the user's agreement, the old Chief of Staff finishes the running work itself (or through its Foreman); once every Driver has finished (its PR may still be open), it tells the new one "your turn, you are the Chief of Staff"; the new one acknowledges explicitly ("I have the batch"); the seat moves only on that acknowledgement | 4 | Areas 4, 5, 6, 9 |
| D9 | No claim, no lock on a CR: several Grillers, or an isolated session, may work at once. Every session works from the CR folder's files: re-read them before acting, write each answer there at once | 5 | Areas 3, 4 |
| D10 | The Chief of Staff learns what the Grillers did through the files only: no journal, no routine messages. It re-reads the backlog's folders before proposing a batch, on "status?", or when the user says a Griller has finished. One optional line: a Griller that sees an active Chief of Staff may send it "<CR> ready, spec written" when a specification is written | 6 | Areas 3, 4, 6 |
| D11 | A Griller may work in a linked worktree: then it opens no PR or MR; it sends its planning files (answers, specification, plan, artifacts, …) to the Chief of Staff's session, which places them in `.agents/changes/` of the main checkout. On the main checkout a Griller writes the CR folder directly. How the files travel is the host's | 10 | Areas 3, 4, 7 |
| D12 | Titles: `[env] Project [role]`; `[env]` the machine's name (`Battlestation`, `Mac`), `Remote` for a cloud session; `Project` the repository's name, capitalised; role `Chief of Staff` or `Griller`. Renamed as soon as the role is set and again when it changes. A Griller may add its subject: `[Battlestation] Chantier [Griller] landing-page`. Foreman: `[env] Project [Foreman - Batch 06]` (replaces "Chief of Staff title + ` - [Foreman Batch 06]`"). A Chief of Staff steering a direct batch: `[env] Project [Chief of Staff - Batch 06 - Direct]`, back to `[env] Project [Chief of Staff]` once the batch is closed. A host that cannot rename: nothing, no workaround | 7 | Areas 2, 4, 7 |
| D13 | The guided remote set-up: the first session is the Chief of Staff, the fork becomes a Griller by itself (or asks, with a batch active). Written in `hosts/claude-code.md` and, short, as a how-to in the docs, "A Chief of Staff and Grillers in remote". The Chief of Staff offers it in one line when relevant (end of the first-turn introduction in a remote session; the user asks to grill while a direct batch runs): "to grill in parallel, fork this session; the fork becomes a Griller". It never does the user's part (the fork, auto mode, no worktree): it explains them | 8, 9 | Areas 2, 4, 7, 11 |
| D14 | A fork inherits the conversation: a session re-reads the seat at each skill invocation and after a fork; the host decides. Only if the host makes it possible; else the host reference records what is not possible, no workaround | 8 | Areas 2, 7 |
| D15 | Two skills, `/chantier:chief-of-staff` and `/chantier:griller` (replacing the request's `chief-of-staff-with-foreman` / `chief-of-staff-direct`). Direct mode is no skill: the user says it ("tu es en mode direct") or invokes `/chantier:chief-of-staff direct`; without it, Foreman mode | Q1 | Areas 1, 4 |
| D16 | The skill invoked gives the starting role; the user's word changes it at any time, both ways. When the user's word makes a second session Chief of Staff ("tu es le chief of staff") while one is active: warn, and block everything until the user chooses which one is the active Chief of Staff, the one that "takes the batch" | Q2, 9 | Area 2 |
| D17 | `/chantier:chantier` stays, as a router: it asks which role (Chief of Staff, with or without direct mode, or Griller), then loads that skill. No alias, no removal | Q3 | Area 1 |
| D18 | Shared content stays in the common skill `skills/chantier/` (cards, CLI, assets; its `SKILL.md` is the router). `skills/chief-of-staff/SKILL.md` and `skills/griller/SKILL.md` are thin and point at `skills/chantier/`'s cards and CLI; `$CHANTIER`, the tests and the docs keep their paths. No duplicated text | Q4 | Area 1 |
| D19 | `/chantier:chief-of-staff` without `direct` on a host that cannot start a Foreman: at the plan, propose direct mode, say why, and say clearly what changes (no Foreman session; it steers the Drivers itself; no grill, triage or discussion while the batch runs; new ideas go to the inbox); wait for the user's yes | Q5 | Area 4 |
| D20 | Copilot: the same three skills, same names; `.github/plugin/plugin.json` declares `skills/chantier`, `skills/chief-of-staff`, `skills/griller`; what is not proved there is marked unproved | Q6 | Areas 1, 8 |
| D21 | Fail at start: the three skills check at once what would block the work later, the linked worktree first (preflight P6, P7, and a host that refuses writes in the main checkout's `.agents/changes/`), and say it in the first message: what fails and what the user does. A Chief of Staff there cannot steer a batch; a Griller cannot write in `.agents/changes/` (it may still work there per D11) | Q8, 10 | Area 2 |
| D22 | Claude Code: a remote session (and an app session by default) often starts in a linked worktree (`.claude/worktrees/<name>`). At start, propose moving to the main checkout for planning, after checking nothing is lost (worktree clean, its branch no commit beyond the default branch; otherwise say what would be left behind and ask). `change_directory` was refused for an isolated worktree (2026-11-10), so the move is the user's step: open a new session on the main checkout, without worktree; the files hold the state. Whether a remote session can start without a worktree is to prove. Once a planning surface exists (P1 `planning-repo`), "main" means the surface's checkout on its default branch | Q9 | Areas 2, 7 |
| D23 | One CR, one specification, one PR (the merge of 2026-11-10) | Merge | this file |
| D24 | "A batch active" in D3, D4 and answer 9 means a batch that is not closed, running or paused: the hand-over question is asked whenever a batch is not closed (the user's choice over running-only) | spec Q1 | Areas 2, 4 |
| D25 | `/chantier:chief-of-staff` never asks the role; the router `/chantier:chantier` asks unless a live Chief of Staff holds the seat, and then behaves as `/chantier:chief-of-staff` | spec Q2 | Areas 1, 2 |
| D26 | No CLI refusal of `open`, `order` or `close` from a session not in the seat; the Griller's card forbids them (simple and flexible) | spec Q3 | Areas 3, 9 |
| D27 | The CR board opens for `chantier` and `chief-of-staff`, not for `griller` | spec Q4 | Areas 1, 10 |
| D28 | `[env]` is read from the machine's host name (its first label); a user's word renames it for the session only | spec Q5 | Area 2 |
| D29 | A Griller may `abandon` an inbox or backlog item, on the user's explicit word only | spec Q6 | Area 3 |

## Area 1: the skills and the manifests

### `skills/chantier/SKILL.md`: the router

Keep the frontmatter keys (`name: chantier`, `icon`, `color`) and the line
`chantier-version: 0.8.0` (`scripts/version.py` and `commands._skill_version` read it there).
Rewrite the `description` to say it is the entry that asks which role, and that
`/chantier:chief-of-staff` and `/chantier:griller` start a role directly. The body:

- The `$CHANTIER` paragraph as today (this folder's `scripts/cli/chantier.py`; nothing to
  install; everything goes to `.agents/changes/`).
- "Read [concepts](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/concepts.md) and [session-start](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/session-start.md)
  now", then the router's own rule: follow `session-start.md`'s start checks and seat reading;
  with no live Chief of Staff in the seat, ask the user in one question which role they want:
  Chief of Staff (Foreman mode), Chief of Staff in direct mode, or Griller; then load that skill
  (`chief-of-staff`, with the argument `direct` for the second, or `griller`) by the host's means
  and follow it. With a live Chief of Staff in the seat, behave as `/chantier:chief-of-staff`
  (D3, D4: answer 9 names `/chantier:chantier` beside it).
- Nothing else: the first-turn introduction, the entry-points table and the hard rules move out
  (below), so no text lives in two places.

### `skills/chief-of-staff/SKILL.md` (new)

Frontmatter: `name: chief-of-staff`, the same `icon` and `color`, and a `description` taken from
today's `skills/chantier/SKILL.md` description (when the user addresses chantier or its Chief of
Staff, files, runs, steers or reports on CRs and batches, changes the team's agents), plus: the
argument `direct` makes this session's batches direct. A line `chantier-version: 0.8.0`. Body,
short:

- `$CHANTIER` means `uv run --script "<the chantier skill's folder>/scripts/cli/chantier.py"`,
  where that folder is the absolute path of `../chantier` from this file's folder (the common
  skill; D18).
- You are the **Chief of Staff**. Read `../chantier/references/concepts.md`,
  `../chantier/references/session-start.md` and `../chantier/references/chief-of-staff.md` now
  (relative links, so the link test resolves them). If the invocation's argument is `direct`, or
  the user says so, your batches are direct (`chief-of-staff.md`, Starting a batch).

### `skills/griller/SKILL.md` (new)

Same shape: `name: griller`, a `description` (refine, reorder and specify the inbox and the
backlog beside an active Chief of Staff; never batches), `chantier-version: 0.8.0`, the same
`$CHANTIER` line, then: you are a **Griller**; read `concepts.md`, `session-start.md` and
`griller.md` of `../chantier/references/`.

### Where today's `skills/chantier/SKILL.md` body goes

- "First turn: introduce chantier" → `references/session-start.md` (Area 2), updated.
- "Entry points" (the table) and "Hard rules" → `references/chief-of-staff.md`, two new sections
  at the top, before `## The project`, text unchanged except: the row "a batch, run the P1s" says
  the mode comes from the session (Area 4); the sentence "The Foreman, the Drivers and the workers
  get their own instructions in their prompts; you never read theirs, except the Foreman's when
  you steer a batch yourself in direct mode" goes with them. "Who talks to whom:
  [routing](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/routing.md)" too.

### Manifests and tooling

- `.github/plugin/plugin.json`: `"skills": ["./skills/chantier", "./skills/chief-of-staff",
  "./skills/griller"]` (D20). `test_manifests_agree` already checks each has a `SKILL.md`.
- `.claude-plugin/plugin.json`: unchanged; Claude Code finds every `skills/<name>/SKILL.md`
  itself and names them `/chantier:<name>`. The Driver confirms it in the docs
  (<https://code.claude.com/docs/en/plugins-reference>, skills) and marks it in
  `hosts/claude-code.md` (documented, with the link).
- `scripts/version.py`: add `skills/chief-of-staff/SKILL.md` and `skills/griller/SKILL.md` to
  `TARGETS` with the pattern `^chantier-version: {V}$`, count 1. The new files are created at
  `0.8.0`; no version is bumped (`just version` is the release's).
- `hooks/register.tsx`, `skill.prompt`: the board opens when the skill loaded is `chantier`; it
  must also open for `chief-of-staff`, not for `griller` (D27). Update
  `hooks/register.test.tsx` to match, and README "The CR board" sentence "Loading the `chantier`
  skill opens it too".

## Area 2: `skills/chantier/references/session-start.md` (new)

Read by the router, the Chief of Staff and the Griller at the start of a session and at each
skill invocation. Host-neutral (no tool of `HOST_TOOLS`; the host's means are in
`hosts/<host>.md`). Sections:

### 1. Start checks, first

Before the role, once per invocation: `$CHANTIER preflight --direct` (it prints P6 and P7 on
any host entry point). On a P6 or P7 failure, or a host its reference says refuses writes in the
main checkout's `.agents/changes/` from this session, the first message says, before anything
else (D21, D22):

- what fails, in one line;
- what it means for this role: a Chief of Staff here cannot steer a batch (preflight will fail at
  the go); a Griller cannot write in `.agents/changes/`, but may work here and send its files to
  the Chief of Staff (`griller.md`, "In a worktree");
- what the user does: open a new session on the main checkout, without worktree, nothing is lost
  since the files hold the state. Before proposing it, check nothing would be left behind: `git
  status --porcelain` is empty and `git rev-list --count <default branch>..HEAD` is 0; else name
  what would be left (the uncommitted files, the commits) and ask. Where the host's reference
  names a way to move this session and marks it proved, offer that; Claude Code's is refused for
  an isolated worktree (its reference).
- Once a planning surface exists (P1 `planning-repo`), "the main checkout" means the surface's
  checkout on its default branch.

The other preflight lines are a batch's and are not reported here, except what the
`claude-code-config` CR adds to the first message (P5, P9, P10), which goes in the same message.

### 2. The seat and the role

`$CHANTIER seat` prints the seat (Area 9). Then, by the skill invoked:

| Invoked | Seat | Role and message |
| --- | --- | --- |
| `chief-of-staff` | none, or this session's own | Chief of Staff: `seat take`, rename, the introduction; no question (D2) |
| `chief-of-staff` | another session, alive (the host says so), **no batch active** | Griller: the introduction ending with D3's message and its one option, "become chief of staff" |
| `chief-of-staff` | another session, alive, **a batch active** | ask once: the hand-over to this session (`chief-of-staff.md`, "Handing the seat over") or only grilling CRs (D4) |
| `chief-of-staff` | another session the host cannot tell, or that looks stopped | one line: "the Chief of Staff at <link> looks stopped; shall I take its place?"; on yes `seat take --over <id>`; never alone (D7) |
| `griller` | any | Griller, no question (D5) |
| `chantier` (router) | none, or a session that looks stopped | ask the role (Area 1); a Chief of Staff chosen over a stopped seat asks D7's line too |
| `chantier` (router) | another session, alive | as `chief-of-staff` (answer 9) |

"A batch active": a batch that is not closed, running or paused (D24). "Alive": the host's
reference says how to tell (D6).

**The user's word changes the role at any time, both ways** (D16):

- "become chief of staff" / "tu es le chief of staff" in a Griller: with the seat free or
  stopped, take it (`seat take`, `--over` the stopped one). With a live Chief of Staff in the
  seat: warn that two sessions would be Chief of Staff, and do no Chief of Staff work (no plan,
  no `open`, no `order`, no steering, no `close`) until the user chooses the one that takes the
  batch. Chosen here: with a batch active, the hand-over rules apply; with none, `seat take
  --over <id>`, and the old session, at its next seat reading, is a Griller. Chosen there: this
  session stays a Griller.
- "become a griller" in the Chief of Staff: with a batch running, the hand-over rules apply
  first (its Drivers are its own); then `seat leave`, rename.

**Re-read the seat** at each skill invocation, after a fork when the host tells the session it is
one (D14), and before each Chief of Staff act on a batch (the plan, `open`, an `order`, `close`,
starting or steering a batch). A seat that names another session makes this session a Griller:
it says so in one line and renames itself. What the host lets a fork know is in its reference;
where it lets it know nothing, the reference says so and nothing else is tried.

### 3. Titles

As soon as the role is set and whenever it changes, the session renames itself by the host's
means (its reference); a host that cannot rename: nothing, no workaround (D12).

- `[env] Project [role]`: `[env]` the machine's name (`Battlestation`, `Mac`), `Remote` in a cloud
  session (the host's reference says how to tell); `Project` the repository's folder name,
  capitalised (`Chantier`); role `Chief of Staff` or `Griller`. The machine's name is the first
  label of its host name (`hostname`); a user's word renames it for the session only (D28).
- A Griller may add its subject once known: `[Battlestation] Chantier [Griller] landing-page`.
- A Chief of Staff steering a direct batch: `[env] Project [Chief of Staff - Batch 06 - Direct]`
  from `open --direct` (or from the hand-over) until the batch is closed, then `[env] Project
  [Chief of Staff]`.
- A Foreman: `[env] Project [Foreman - Batch 06]`, given in its prompt (`chief-of-staff.md`).
- The title given to `seat take --title` is the session's current title; take the seat again
  (same session, no `--over`) when it changes.

### 4. First turn: introduce chantier

Today's "First turn" text of `SKILL.md`, moved here, with these changes:

- Once per session, in the user's language, about ten lines, then answer the request; skipped if
  the user knows chantier or asks `init` first; "new here? say init for a guided tour" when there
  is no `.agents/changes/`. Start-check failures (section 1) come before it.
- The list gains **Griller**: "another session of yours that grills and specifies the backlog
  beside the Chief of Staff; it never runs batches". **Chief of Staff (me)** says "the only
  session that opens and runs batches" when the session is the Chief of Staff.
- A Griller gives the same introduction, ending with D3's message.
- A Chief of Staff in a remote session (Remote Control or cloud, per the host's reference) ends it
  with D13's line: "to grill in parallel, fork this session; the fork becomes a Griller".

## Area 3: `skills/chantier/references/griller.md` (new card)

Host-neutral. Content:

- **Who you are.** A Griller: you keep the inbox and the backlog with the user beside the Chief of
  Staff, who has the last word on batches. Usually short. Talk with the user in their language;
  repository text in English. Read your host's reference with this card.
- **What you do**, as `chief-of-staff.md`'s "Backlog and grill" says (point to it; do not copy
  it): `$CHANTIER file`, `triage`, write `01-intent.md`, record every answer in `02-answers.md` at
  once, the restatement before "grilled enough?", `depends.json` when a CR needs another's
  result, and on the user's word the `spec-writer` (`work/specifying`, the prompt of
  `concepts.md`, the review against `02-answers.md`, its open questions to the user). You may
  prepare work for the Chief of Staff: a proposed grouping or order of prepared CRs, written in
  your reply or in the CRs' `02-answers.md` as the user's words, never a batch. `abandon`
  an inbox or backlog item, on the user's explicit word only (D29).
- **From the files** (D9): no claim, no lock. Re-read a CR's folder before each act on it; write
  each answer there at once; another session may have written since your last read.
- **Never:** open, pause or close a batch; `order`; start or message a Driver or a Foreman; steer;
  merge; `seat take` without the user's word (session-start). A request for any of these: say it
  is the Chief of Staff's, with its link from the seat.
- **Telling the Chief of Staff** (D10): nothing routine. When a CR's specification is written and
  the seat names a live session, you may send it one line, `[griller→chief-of-staff] <CR> ready,
  spec written`, by the host's means; a refused send is reported, never sent another way.
- **In a worktree** (D11): you open no PR or MR and commit nothing. You read the CR folders of the
  main checkout; you write your files (answers, intent, specification, plan, artifacts) in your
  worktree, under the same relative path they would have in the main checkout
  (`.agents/changes/<stage>/<slug>/<file>`). When a piece is done, send the Chief of Staff's
  session one line naming the absolute paths, `[griller→chief-of-staff] files for <slug>: <path>,
  …`, by the host's means (its reference). With no live Chief of Staff, tell the user where the
  files are; the next Chief of Staff places them on the user's word.
- **Your cost** is in no batch.

## Area 4: `skills/chantier/references/chief-of-staff.md`

(`claude-code-config` edits `## The project` and Starting a batch step 1; this CR does not touch
those two places beyond what is listed here.)

- **Top:** the two sections moved from `SKILL.md` (Area 1) and one line: read
  `session-start.md`; your seat and title are there.
- **Opening paragraph:** you are the only session that opens and runs batches; Grillers may work
  beside you (`griller.md`).
- **Backlog and grill:** add (D10) "Grillers write the CR folders too: re-read the backlog's
  folders before proposing a batch, on "status?", and when the user says a Griller has finished;
  re-read a CR's folder before each act on it (D9)". Add (D11) "Files from a Griller in a
  worktree (`files for <slug>: <paths>`): read them, place them in the CR folder of the main
  checkout as received (a new item through `$CHANTIER file @<its request>` first), tell the user,
  and review a specification as one from the `spec-writer`". The spec-writer sentence: the
  Chief of Staff or a Griller starts it.
- **Starting a batch, step 2** (D15, D19): replace the direct-mode proposal ("when the host cannot
  start a Foreman session … or when the batch has few CRs") by: the mode is the session's: direct
  when the skill was invoked with `direct` or the user said so, else Foreman. In Foreman mode on a
  host that cannot start a Foreman session (a terminal or IDE host, a Remote Control session with
  no Foreman to reuse), propose direct mode in the plan, say why, and say clearly what changes: no
  Foreman session; you steer the Drivers yourself; no grill, triage or discussion while the batch
  runs; new ideas go to the inbox. Wait for the user's yes. Before the plan, re-read the seat
  (session-start).
- **Step 4, the Foreman's title** (D12): `<title>` is `[env] Project [Foreman - Batch <nn>]`, e.g.
  `[Battlestation] Chantier [Foreman - Batch 06]`; a later Foreman of the same batch has the same
  title. Remove "`<your title> - [Foreman Batch <nn>]`".
- **Steering a batch yourself:** at `open --direct`, rename yourself `[env] Project [Chief of
  Staff - Batch <nn> - Direct]`; after `close --yes`, back to `[env] Project [Chief of Staff]`.
  "What you accept while you steer": a request to grill gets D13's line ("to grill in parallel,
  fork this session; the fork becomes a Griller") besides being noted.
- **New section "Handing the seat over"** (D8), rules only:
  - The seat moves only on the user's word, and only on the new session's explicit
    acknowledgement.
  - A running Driver is never stopped nor moved to another session. On the user's agreement the
    old Chief of Staff finishes the running work itself, or through its Foreman: it starts no new
    Driver (`order slots --note 0` while CRs are queued). Once every Driver has finished (a PR may
    still be open, not merged or archived), it sends the new session `[chief-of-staff→chief-of-staff]
    your turn, you are the Chief of Staff`.
  - The new one answers `I have the batch`, then `$CHANTIER seat take <own id> --over <old id>
    …`. A direct batch: it claims the next epoch as in Steering a batch yourself (`foreman set`,
    `foreman transcript`), and gives the slots back if a hold was set. A Foreman batch: it sends
    the Foreman `chief-of-staff <own session id>` (routing).
  - The old one becomes a Griller (or ends), and renames itself.
  - With no batch active, the hand-over is the seat alone: `seat take --over` on the user's word.
- **Never:** add "take the seat, or act as Chief of Staff while the seat names another live
  session, without the user's word".

## Area 5: `skills/chantier/references/foreman.md`

One rule in the part about the Chief of Staff's lines: on `[chief-of-staff→foreman]
chief-of-staff <session id>`, check `$CHANTIER seat` names that session; then send your lines to
it from then on. Otherwise ignore it and ask (`asks`) the Chief of Staff of your prompt. The
title paragraph is unchanged (the title comes from the prompt).

## Area 6: `concepts.md`, `routing.md`, `spec-writer.md`, `init.md`

- `concepts.md` (`claude-code-config` edits rule 8 and adds rule 9; this CR edits only Words and
  Starting an agent): the three words above; **Steering session** gains "the Chief of Staff
  session is the one the seat names"; Starting an agent: the Spec-writer is started by the Chief
  of Staff or a Griller, its first line `chantier spec-writer for the Chief of Staff, in the
  project <root>.` unchanged (a Griller writes the same line).
- `routing.md`: new rows: `Chief of Staff → Chief of Staff (hand-over)`: `your turn, you are the
  Chief of Staff`; back: `I have the batch`; `Chief of Staff → Foreman`: also `chief-of-staff
  <session id>`; `Griller → Chief of Staff`: `<CR> ready, spec written` (optional),
  `files for <slug>: <paths>` (a Griller in a worktree). A sentence: Grillers send nothing
  else, to no Foreman and no Driver; the user talks with the Chief of Staff and with Grillers,
  about the backlog only in a Griller.
- `spec-writer.md`: "The Chief of Staff starts you" → "The Chief of Staff or a Griller starts
  you". The agent files `agents/spec-writer.md` and `com.github.copilot/agents/chantier-spec-writer.agent.md`
  are unchanged.
- `init.md`, step 5.3 glossary: add "Griller". (`claude-code-config` edits steps 1 and 5.1.)

## Area 7: `skills/chantier/references/hosts/claude-code.md`

### Sections this CR owns (the `claude-code-config` CR edits the same file)

`claude-code-config` owns `## Configuration` (new, after `## Heartbeat`), `## Compacting`, and
`### Allow rules to add` (new, last subsection of `## The "For you" block`). This CR owns only:

1. `## Tools`: new rows and the edit of the row "Set the Foreman's own title, first";
2. `## Classes of session`: the remote and app worktree facts (rows and paragraph);
3. a new section **`## Sessions of one repository`**, inserted after `## Reusing the last Foreman`
   and before `## The "For you" block`;
4. two new "For you" subsections, **`### A session on the main checkout`** and **`### A Chief of
   Staff and Grillers in remote`**, inserted after `### A closed Foreman session` and before
   `### \`/compact\``.

It does not touch the introduction, `## Heartbeat`, `## Compacting`, `## Configuration`, `## A
Foreman in a worktree asks`, `## Reusing the last Foreman` or the other subsections. Whichever CR
merges second rebases and keeps the other's text as it is.

Every new line carries a mark (proved with where and when; documented with the link; unproved
with its trial).

### `## Tools`

- "Set the Foreman's own title, first" becomes "Set a session's own title (the Chief of Staff, a
  Griller, the Foreman)": `set_session_title`; **proved** for a Chief of Staff's own session,
  2026-11-08 (Battlestation, a session renamed itself); the Foreman's case stays unproved, with its
  trial.
- New rows: "The skills" (`/chantier:chantier`, `/chantier:chief-of-staff [direct]`,
  `/chantier:griller`; a plugin's `skills/<name>/` is `/<plugin>:<name>`: documented, link);
  "Load another skill" (the router; the host's Skill tool: unproved until the router runs);
  "List the sessions and their state; is the seat's session alive" (the session tools the
  Driver finds in the `mcp__ccd_session__` set: the exact tool and the states, unproved; trial:
  two sessions on one repository, one stopped, list both and record the states); "Message another
  session of the user (hand-over, a Griller's line)" (`SendMessage` to its session id: proved for
  the Chief of Staff's session; between two sessions of the user, unproved; trial: a Griller's
  `ready` line); "A session's link" (what `get_session` gives to put in the seat: unproved until
  recorded). The limit on messages applies to these lines.

### `## Classes of session`

- New row "Remote or app session": often starts in a linked worktree `.claude/worktrees/<name>`
  (proved 2026-11-10, Battlestation, session `epic-lamport-b88c2f`: preflight P6 and P7 failed and
  the hook refused writes in the main checkout's `.agents/changes/`).
- New paragraph: `mcp__ccd_directory__change_directory` to the repository's root was refused for
  a session in an isolated worktree, even clean with no commit (proved 2026-11-10, same session).
  So moving to the main checkout is the user's step: a new session on the main checkout, without
  worktree ("For you" below). Whether a remote session can start without a worktree: unproved;
  trial: start one with Worktree off and run `git rev-parse --git-dir --git-common-dir`.
- How to tell a cloud session (for `Remote` in the title) and a Remote Control session (for the
  remote offer): the existing rows; mark the cloud row's test as the same trial.

### `## Sessions of one repository`

- The seat: liveness is asked of the host (the Tools row), never read from a date. Where the host
  cannot tell, the session asks the user (D7).
- A fork: what it inherits (the conversation), whether it gets its own session id and transcript
  id (`$CLAUDE_CODE_SESSION_ID`), and whether anything tells it it is a fork: unproved; trial:
  fork a Chief of Staff session, compare `get_session("self")` and the variable with the seat. If
  the fork has its own id, comparing it with the seat at its next turn makes it a Griller; if not,
  record that a fork cannot be told apart and that the user says "you are a griller" in it.
- A Griller in a worktree sends its files by `SendMessage` to the seat's session, naming the
  absolute paths; the Chief of Staff on the main checkout reads them under
  `.claude/worktrees/<name>/` (unproved; trial: one file sent and placed).
- The two-Chiefs case and the hand-over lines travel by `SendMessage` like the rest.

### `### A session on the main checkout` ("For you")

Cost: a fresh context; the files hold the state, nothing is lost once the start check found the
worktree clean with no commit. Where: the Claude Desktop app (or the remote client). Do: a new
session on the repository's folder, Worktree off (the labels the Driver records from the desktop
docs, documented, link). Paste: `/chantier:chief-of-staff` or `/chantier:griller`. You should
see: the session's introduction with no start-check failure. Unproved until followed once.

### `### A Chief of Staff and Grillers in remote` ("For you")

The guided flow (D13), unproved until followed once by hand:

1. Start a remote session with no worktree and the tools allowed in auto mode (the user's own
   steps; chantier explains them, never does them).
2. Run `/chantier:chief-of-staff` (or `/chantier:chantier`): it becomes the Chief of Staff.
3. After the boot, fork the session (the label on screen, recorded by the trial): the fork
   becomes a Griller by itself, or asks with a batch active.
4. Each renames itself; the user grills in the fork.

What is not possible on the host (a fork that cannot be told apart, a remote session that cannot
start without a worktree) is written here as found, with no workaround.

## Area 8: `skills/chantier/references/hosts/copilot.md`

Add to `## Tools` (all **unproved**): the three skills, same names (`skills/chantier`,
`skills/chief-of-staff`, `skills/griller`), and how Copilot passes the argument `direct`;
setting a session's own title (as for the Foreman: when the host offers a way, else nothing);
listing sessions and telling the seat's session alive: not known, so the seat's session always
"looks stopped" to a new session and D7's line is asked; messaging another session:
`send_message` to its link, unproved; a Griller in a worktree: unproved. The user tests Copilot
later (D20).

## Area 9: the CLI

No dependency, portable, UTF-8; output within ten lines. `rails.py` holds the refusals.

### `seat` (new command, `commands.py` and `cli.py`)

`cmd("seat", commands.seat, "the repository's Chief of Staff session: show, take or leave the
seat", batch=False)` with `action` in `get` (default), `take`, `leave`, an optional `session`,
and `--env`, `--title`, `--link`, `--over`.

- File: `<repo.changes>/seat.json`, written under `changes_lock`, plain JSON:
  `{"session": …, "transcript": …, "env": …, "title": …, "link": …}`. The transcript is read from
  the environment as `open` does (`COPILOT_AGENT_SESSION_ID` on Copilot, else
  `CLAUDE_CODE_SESSION_ID`); `null` when unknown. No date field.
- `seat` / `seat get`: `seat none`, or `seat <session> env <env> title "<title>" link <link>`
  and a second line `transcript <id or unknown>`. Exit 0.
- `seat take <session> --env <env> --title "<title>" --link <link> [--over <session>]`:
  - free, or held by the same session: write; print `seat <session>`.
  - held by another session and `--over` is absent or names someone else: exit 2, `the seat is
    held by <session> (<link>): take it over only on the user's word, with --over <session>`.
  - when a batch is not closed and the transcript is known and differs from the batch's
    `chief_transcript`: under the batch lock, set `chief_transcript` to it, append it to a new
    list `chief_transcripts` (created as `[<the old chief_transcript>]` when absent), log the event
    `chief` with the transcript; print a second line `<batch>: Chief of Staff transcript <id>`.
- `seat leave <session>`: clears the file when it names that session; else exit 2 `the seat is
  held by <other>`; `seat none` already: exit 0, `seat none`.
- The CLI knows no role: the command records a session and refuses a silent take-over; who may
  take it is the cards'. No other command reads the seat: `open`, `order` and `close` are not
  refused from a session not in the seat (D26).

### The batch's Chief of Staff transcripts

- `open`: write `chief_transcripts: [chief]` (empty list when `chief` is none).
- `foreman transcript` (the switch at `commands.py` ~577): a direct batch stays direct when the
  claimed transcript is the current `chief_transcript` (unchanged rule, now fed by `seat take`
  after a hand-over); it still switches to `foreman` for any other transcript.
- Cost (`_cost_rows`, `_window`): a steering window is the Chief of Staff's when its transcript is
  in `chief_transcripts` (fallback `[chief_transcript]` for an old batch); each such window is
  priced from its claim, as today. `_chief_line`: the `Chief of Staff:` line sums the sessions of
  `chief_transcripts`, each with its two figures as today, the steering windows left out; one
  `not measured` makes the line `not measured`.
- `rails.py` close check (line 45): every transcript of `chief_transcripts` is a Chief of Staff
  session: its own file is skipped and its subagents checked, as today for the one.
- `status`, `STATUS.md`, the board: unchanged.

## Area 10: tests and scenario

- `skills/chantier/scripts/cli/tests/test_structure.py` (few, fast):
  - `test_skill_and_references_links_resolve`: also every `skills/*/SKILL.md`.
  - `test_each_host_has_its_reference_and_the_cards_hold_no_host_tool`: the card list gains
    `griller` and `session-start`.
  - One new test: the three skill folders exist, each `SKILL.md`'s frontmatter `name` is its
    folder's, the thin two link `../chantier/references/` and `../chantier/scripts/cli/`, and
    `.github/plugin/plugin.json` lists all three.
  - One new test: `seat` in a fresh repository: `seat none`; `take` writes only
    `.agents/changes/seat.json` with no date field; a second session's `take` exits 2; `--over`
    passes; `leave` by a non-holder exits 2.
- `scenario/run_scenario.py`, the direct-mode part: open a direct batch with the seat taken by
  transcript A; a second session (transcript B) refused `seat take`, then `seat take --over`
  records B as the batch's `chief_transcript`; B claims the next epoch (`foreman set`, `foreman
  transcript B`): the steering stays direct; the old epoch is refused (exit 3); `pause` and
  `close` price two Chief of Staff sessions and are not blocked by either's own file. Update
  `scenario/README.md`'s list.
- `hooks/register.test.tsx`: the board opens on `chief-of-staff`, not on `griller` (D27).

## Area 11: docs

- `README.md`: the install paragraph ("type `/chantier` (on Claude Code, `/chantier:chantier`)")
  names the three entries: `/chantier:chief-of-staff` (add `direct` for direct mode),
  `/chantier:griller`, and `/chantier:chantier`, which asks; the Use table gains "become chief of
  staff", "you are a griller"; the repository layout shows `skills/chief-of-staff/`,
  `skills/griller/` (thin) and the new references; the CR board sentence (Area 1).
- `CONTRIBUTING.md`, "How the project is built" item 1: the router and the two thin skills;
  `griller.md` and `session-start.md` among the references.
- `docs/tutorial-claude-code.md` section 3: `/chantier:chief-of-staff prepare yourself to work on
  this project` and `/chantier:chief-of-staff init`; one sentence on `direct` and on Grillers.
- `docs/use-cases.md`: new section **"A Chief of Staff and Grillers in remote"**, short: the four
  steps of Area 7, the titles, the one-line offer, the hand-over in two sentences, a link to
  `hosts/claude-code.md`.
- `docs/use-cases-direct.md`: replace "To grill meanwhile, open another session yourself … a
  Chief of Staff grills …" by a Griller; the opening paragraph: direct mode is chosen by
  `/chantier:chief-of-staff direct` or your word, and proposed only where no Foreman can start.
- `docs/use-cases-foreman.md`: the same choice of mode, one sentence.
- The SVG diagrams (`docs/*.svg`, the README's images) and their text companions
  (`docs/*-texts.md`, e.g. `batch-lifecycle-texts.md`, "grill in another session of yours") are
  not edited here: see Out of scope.
- Old release notes (`docs/release-notes/2026-11-07-v0.8.0/`) are history: unchanged.

## Out of scope

- No lock or claim on a CR; no backlog journal; no routine messages between sessions (D9, D10).
- No step-by-step hand-over procedure (D8); no way to move a running Driver.
- chantier never forks a session, sets auto mode or creates a session without worktree for the
  user (D13); no way around a host refusal (D14, D22).
- Copilot trials (D20): marked unproved only.
- The configuration and allow rules, P5/P9/P10 at start: `claude-code-config`.
- The planning surface (`planning-repo`): only the forward note of D22.
- No version bump; no change to the agent files' bodies.
- No CLI rail on the seat (D26).
- The SVG diagrams (`docs/*.svg`, the README's images) and their `docs/*-texts.md` companions:
  the CR `diagrams-modes-griller`, which runs after this one, draws the Griller and the two
  steering modes in every SVG. This CR changes the prose docs only (cards, host references,
  README, CONTRIBUTING, tutorial, use cases, the how-to).

## Evidence

- `just check` passes on Linux, macOS and Windows (structure tests above, links, no host tool in
  the cards, the version targets).
- `just scenario` passes on both forges, with the seat and hand-over checks.
- At the pushed head, in a temporary repository: `$CHANTIER seat`, `seat take`, a refused second
  take (exit 2), `--over`, `leave`; the outputs kept in `evidence/`.
- A reader check of `02-answers.md` against this CR's diff: each D1–D29 lands where the table says.
- Host trials (sessions, fork, liveness, rename, messages between sessions, the remote flow) need
  the user's hands: the PR lists them as not proved, and the host reference keeps them unproved
  until run.
