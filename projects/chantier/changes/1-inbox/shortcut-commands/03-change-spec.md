# Five shortcut commands for batches and autonomy

Five slash commands for things the owner types to the Chief of Staff again and again:
`/chantier:batch-start`, `/chantier:batch-pause`, `/chantier:batch-close`, `/chantier:batch-add`
and `/chantier:autonomy`. They are on Claude Code and on Copilot. Each is a thin skill that names
one help topic. The topic says what the command does, and that text is the only place its rules
live.

Issue: none (a verbal request; no tracker issue).

## Goal

In the owner's words (`intake/request.md`): "Je me vois souvent dire à l'agent quoi faire". The
research pass (`work/research-commands.md`) counted, over 10 days, the free-text messages each
command replaces: batch start 26 (39 counting changes of shape), close 12, pause 6, grill to the
running batch 23, adding existing CRs to the batch 29, autonomy or a night run 19. The commands
replace typing; they do not add powers. Each one removes only the questions its topic names. The
floor, the Chief of Staff's card and the project's rules still hold in full.

## Place in the chain, and the facts that depend on CRs not yet written

This CR runs at the end of batch-31's stack, on top of CR-514 (Answer 2 and Answer 10). It
is specified against the newest head of the stack that exists: the worktree
`chantier.worktrees/batch-31-CR-507`, head `03f973e`, which holds the new card set, unloaded, in
`skills/chantier/cards-next/`. That head is still being fixed. CR-510 to CR-514 are not written
yet. The facts below come from their specifications in `changes/4-batch/1-pending/`. At its
base, the Driver checks each one and stops, saying which, if one does not hold. There is no
stand-in.

| Fact this specification relies on | From | If it does not hold at the base |
| --- | --- | --- |
| `skills/chantier/references/` is the swapped `cards-next/`. `references/topics.json` and `references/topics/*.md` exist, and `chantier help <topic>` reads them | CR-510 (sections 1 and 8), CR-493 | Stop |
| The four `skills/*/SKILL.md` are copies of `cards-next/skills/*-SKILL.md`, each with the launcher paragraph (`uv run --script "<plugin root>/skills/chantier/scripts/chantier.py" ...`) and `$CHANTIER brief chief-of-staff` | CR-510 section 4, CR-503, CR-509 | If CR-510's D9 applied (launcher not switched), the five new skills copy whichever `$CHANTIER` paragraph the four `SKILL.md` hold at the base, as they stand. Say so in Known gaps |
| The topic files this specification names exist under these names: `batch-plan`, `batch-plan-show`, `batch-plan-mode`, `batch-close`, `batch-pause`, `where-cr-goes`, `grill-specify`, `grill-critic`, `grill-series`, `refusals-to-say`, `asks`, `escalation`, `seat`, `watcher`, `allow-rules`, `host-auto-mode-steering`, `stack-changes-chief` | CR-507 to CR-509 at `03f973e` | Use the topic that holds the same rule at the base, and list each rename in the PR |
| `hooks/register.tsx`'s `reloadLine` has CR-510's text ("run your brief again ..."). `ROLE_SKILLS` and `PANE_SKILLS` are unchanged | CR-510 section 5 | Stop |
| Rule ids `[R-nnn]`, `references/rules.json`, `references/budgets.json` (every `references/**/*.md` has a row), the history lint over `references/**/*.md`, the pin scan `test_no_card_phrase_pins`, quiz rule ids `R-nnn`, and the anchor-aware link check | CR-512 | Follow whatever CR-512 shipped. Where it shipped none of these, the matching steps below fall away |
| The M6 rule (a PR that adds card text quotes the measure line or the owner's line) and the M11 CI reminder (the floor or `budgets.json` changed without the owner's approval line) | CR-513 | Same |
| The rows `pending_owner` and the limits confirmed by the real run | CR-514 | Read `budgets.json` at the base |
| `tests/test_plugin_files.py` holds the four-skill test (`test_four_skills_the_router_and_three_thin_ones_listed_by_copilot`) and the link test, as converted by CR-510 and CR-512 | CR-510, CR-512 | Edit the test that holds the four-skill list at the base |

## Decisions carried from `02-answers.md`

| Answer | Decision | Where here |
| --- | --- | --- |
| 1, superseded in part by 6 | `/chantier:autonomy` and `batch-add` join the request | sections 2.5 and 2.4 |
| 2 and 10 | When: at the end of batch-31, after CR-514. The local Windows long gate moves to this CR | Place in the chain; Gates |
| 3 | `batch-start <shape>` starts at once. Typing the command is the go. The plan is shown after | 2.1 |
| 4 then 6 | One command, `/chantier:batch-add`, followed by anything, with no option. An existing CR (number or name) is added; any other text becomes a new CR. In both cases it asks the missing questions, writes the specification and puts the CR in the running batch. No `grill-to-pending` command | 2.4 |
| 5 | `/chantier:autonomy`: a question that comes up is decided with the recommendation, recorded "to confirm by the owner", and the work goes on. It never merges, releases or deletes without the owner | 2.5 |
| 7 | `batch-start` with no budget asks for one, then starts as soon as it has the answer | 2.1 |
| 8 | `batch-close` shows the outcome, then asks "close?" before closing | 2.3 |
| 9 | No release in these commands. The owner asks for a release separately | 2.1, 2.3, 2.5 |
| 10 | `batch-pause` pauses the batch | 2.2 (its meaning: open question 1) |
| 10, defaults accepted | `batch-start` takes the `3-ready` CRs, asks the shape when it is missing and stops when a preflight check fails. `batch-add` with no running batch leaves the CR in `3-ready` and says so. `autonomy` accepts a budget and a number of rounds. The commands exist on Claude Code and Copilot | 2.1, 2.4, 2.5, section 4 |
| 10, autonomy | Before the owner leaves, `autonomy` names what would block, then goes on alone | 2.5 |
| 10, critic | A spec critic runs (an impactful CR: it removes the go before a batch starts and adds an unattended mode) | not in this specification; the Chief of Staff's |

## Decisions this specification takes on the means

- **D1. A skill per command, its rules in a topic.** Each command is a skill folder,
  `skills/<command>/SKILL.md`, which on Claude Code is `/chantier:<command>`. The body is thin:
  the launcher paragraph, then one line naming `$CHANTIER help command-<command>`. The behaviour
  lives in `references/topics/` (a role's contract lives in the cards: AGENTS.md). The Chief of
  Staff's card `chief-of-staff.md` is not edited. Its frozen size and measured path stay as they
  are, and the commands need no "Rare cases" entry, because the skill names its topic itself.
- **D2. One shared topic file.** `references/topics/commands.md` holds what the five commands have
  in common: who may run them, the typed-only rule, and that nothing else changes. Each
  `command-<x>` topic reads that file first, then its own file. Each shared rule is written once.
- **D3. Typed by the user only.** Each command skill's front matter has
  `disable-model-invocation: true`, meant to keep the model from invoking it by itself. The
  repository holds no record of that key on either host: on Claude Code it is unproved until
  evidence 5 measures it; on Copilot it is untested. The shared topic says the same in words (P3:
  the go is in the user's own message of the turn), so the rule holds on a host that ignores the
  key.
- **D4. The launcher paragraph is copied.** Each new skill carries the same `$CHANTIER` paragraph
  as the four existing `SKILL.md` files, byte for byte, and its `chantier-version:` line. So each
  command runs on its own, on both hosts, with no skill loading another. Copilot does not record
  which tool loads another skill (`hosts/copilot.json`, `load-skill`). A test keeps the copies
  identical. How the host passes the words typed after a command to a skill that names no
  `$ARGUMENTS` is not recorded either: the `skills` row of `hosts/claude-code.json` is
  `untested`, and `hosts/copilot.json` says how Copilot passes the arguments is not known. Evidence
  5 measures it on Claude Code; on Copilot it stays untested.
- **D5. The hook counts a command as the Chief of Staff.** On Claude Code, when one of the five
  skills loads, `hooks/register.tsx` records the role `chief-of-staff` and opens the CR board pane,
  just as for `/chantier:chief-of-staff`. Then a session that started with
  `/chantier:batch-start` gets the Chief of Staff's reload message after a compaction. The one
  exception is a session whose last recorded role is `griller`: its roles stay as they are, and
  no pane opens.
- **D6. No CLI change.** Every command works through existing commands: `seat`, `preflight`,
  `open`, `order slots|budget|rounds|add`, `close`, `file`, `triage`, `note`, `asks`, `status` and
  `cost`. The CLI's scope (AGENTS.md) adds no tool without a measured cost, and the grill asked for
  none.

## What changes

Paths are from the repository root. `references/` is `skills/chantier/references/`; `tests/` is
`skills/chantier/scripts/cli/tests/`.

### 1. Five skill folders (new)

`skills/batch-start/SKILL.md`, `skills/batch-pause/SKILL.md`, `skills/batch-close/SKILL.md`,
`skills/batch-add/SKILL.md`, `skills/autonomy/SKILL.md`. Each one holds:

- **Front matter:**
  - `name:` the folder's name;
  - `icon: 🏗️` and `color: yellow`, as the role skills have;
  - `description:` one or two sentences that say what the command does and that it is the Chief
    of Staff's, and that show the form to type. `batch-start`'s description shows
    `stack|parallel|series` and the optional budget (the request: "en options ou description");
  - `argument-hint:`
    - `batch-start`: `stack|parallel|series [budget in USD]`;
    - `batch-add`: `<CR number or name, or the request>`;
    - `autonomy`: `[budget <USD>] [rounds <n>]`;
    - none for `batch-pause` and `batch-close`;
  - `disable-model-invocation: true` (D3).
- **Body:**
  - `# chantier: <command>`;
  - `chantier-version: <version>`;
  - the launcher paragraph and the "Cards: ... CLI: ..." line, copied from
    `skills/chief-of-staff/SKILL.md` (D4);
  - one paragraph: "Run `$CHANTIER help command-<command>` and follow it, with the words the user
    typed after the command." The text names no `$ARGUMENTS`, which is recorded on neither host.
    That the host brings the typed words to the skill is unproved (D4): evidence 5 measures it on
    Claude Code.
- **Nothing else.** In particular, no rule of the topic is copied here.

### 2. The topics (new): `references/topics/commands.md` and five command files

In `references/topics.json`, five entries. Each has `roles: ["chief-of-staff", "griller"]`
(`batch-add` serves a Griller too, and the shared file tells the others what to do in a Griller
session) and a `trigger` naming the slash command:

| Topic | `readings` |
| --- | --- |
| `command-batch-start` | `topics/commands.md`, `topics/command-batch-start.md` |
| `command-batch-pause` | `topics/commands.md`, `topics/command-batch-pause.md` |
| `command-batch-close` | `topics/commands.md`, `topics/command-batch-close.md` |
| `command-batch-add` | `topics/commands.md`, `topics/command-batch-add.md` |
| `command-autonomy` | `topics/commands.md`, `topics/command-autonomy.md` |

Each file is written in the cards' style: short sentences, the rule only, no history. The history
lint forbids dates, batch names, CR ids, PR numbers, model names, and the words "proved",
"unproved", "trial" and "trials", so a step that the trials belong to is named through
`help batch-plan`. A file names an existing topic as `` `help <name>` `` rather than restating it.
What each file must say follows. The Driver words it; nothing below may be dropped, and nothing
may be added beyond it.

#### 2.0 `commands.md`: who may run a command

- These commands are typed by the user. A command skill that the session reached any other way
  acts on nothing: it says the command to type. The typed command, together with the answers it
  asks for in the next turns, is the user's word for what its topic says, and for nothing more.
  The turn of the last answer is the go's turn (P3).
- Read `$CHANTIER seat` first:
  - This session is the Chief of Staff: go on.
  - No live Chief of Staff holds the seat: first become the Chief of Staff, exactly as
    `/chantier:chief-of-staff` does: its brief (`$CHANTIER brief chief-of-staff`, read whole) and
    its `watch: not running` rule. Then go on.
  - Another live session holds the seat: do nothing, and give that session's link from `seat` in
    one line.
  - A Griller session: `batch-add` follows the Griller's card (section 2.4). Every other command
    does nothing and gives the Chief of Staff's link from `seat`.
- Every rule of the floor, of the Chief of Staff's card and of the project still holds. A
  command removes only the questions its topic names. A refusal the command meets is said in three
  parts (`help refusals-to-say`).

#### 2.1 `command-batch-start.md` (Answers 3, 7 and 10)

- **What the user types.** A shape word (`stack`, `parallel`, `series`) and an amount in dollars
  (the budget), in any order.
  - Shape missing: ask only the shape, in the mode question's form (`help batch-plan-mode`), with
    a recommendation.
  - Budget missing: ask for it, with a recommended figure.
  - Both missing: one message asks both.
  - Nothing starts before the answers. Then the start follows at once, with no further question.
- **A batch not closed** (running or paused): start nothing. Say in one line that it is open, that
  `/chantier:batch-add` adds CRs to it and that `/chantier:batch-close` closes it.
- **The CRs:** every `3-ready` CR. With none, it is the empty batch of `help batch-plan-show`,
  which opens paused; CRs join it with `/chantier:batch-add`.
- **The start, in this order, with no go asked:**
  1. step 1 of `help batch-plan`: the sync in the dev mode, the preflight and the checks it names.
     A failed condition starts nothing, offers no other way, and says which condition failed and
     what the user can do (Answer 10);
  2. step 3 of `help batch-plan`: `open <every 3-ready folder> --mode <shape> --budget <usd>`, the
     steering mode as the plan reads it (said, not asked), then the Foreman or direct mode;
  3. the watcher, on the session's yes. When that yes was never given, the question goes with the
     plan (below).
- **What `open` takes:**
  - the waits that `depends.json` declares (`open` reads them);
  - no wait the Chief of Staff would only propose (`help batch-plan-cut`): such waits are offered
    in the plan shown after (open question 4);
  - no `--release`, `--autonomous-releases` or `--grant-fixes` (Answer 9);
  - no cut (the command takes no time).
- **The plan, shown after the start** (Answer 3), by `help batch-plan-show`, with:
  - the batch's number and the mode, stated rather than asked;
  - the questions that would have come before a go, now asked after it, the batch running
    meanwhile: the P10 allow rules (`help allow-rules`), the watcher's yes, a stack's waiver of the
    local gate, and the `gh stack` extension.

#### 2.2 `command-batch-pause.md` (Answer 10; its meaning is open question 1)

The text below is open question 1's default. If the owner answers otherwise, the Driver writes the
answer here instead.

- **No batch open:** one line.
- **A paused batch:** say so, since when (`status`), and what is in `1-pending`.
- **A running batch:**
  - run `order slots --note 0`: no new Driver starts. Say the number of slots it had, which
    `order slots --note <n>` brings back;
  - in Foreman mode, send the Foreman the printed line, as for any order;
  - in direct mode, start no Driver;
  - the Drivers at work go on to their hand-back. Nothing is stopped, held, dropped or cancelled;
  - say what still runs and what stays queued. The CLI pauses the batch by itself when its last CR
    ends (`help batch-pause`). Queued CRs keep it from that pause until they run or leave.

#### 2.3 `command-batch-close.md` (Answers 8 and 9)

- **No batch open:** one line.
- **A paused batch:** the close offer of `help batch-close`, once the Foreman's `final` (Foreman
  mode) and the retro critic's hand-back are in, as `help batch-close` says. Before that, show the
  Progress report and say what it waits for (the Foreman's `final`, the retro critic), and close
  nothing. Once both are in:
  - if the Completion report and the retro offer were not given yet, give them first
    (`help batch-pause`);
  - then the check (`close --batch <b>`, no `--yes`), its bilan and what it removes;
  - then ask "close the batch?". `close --yes` and the removals follow only on the yes, as
    `help batch-close` says.
- **A batch not paused:** the check refuses with what remains. Show that as the outcome, in a
  Progress report with the refusal's causes, and close nothing. The command drops, cancels and
  stops nothing, and offers no `--stopped`. Those are the user's own orders, as
  `help batch-close-stopped` says.
- **No release:** the command never offers or starts one (Answer 9).

#### 2.4 `command-batch-add.md` (Answers 6 and 10)

- **The words after the command:**
  - references to existing CRs: a number, `CR-<n>`, a slug or a folder name, one or more,
    separated by spaces or commas;
  - or one request, as text.
  - Words that both name a CR and hold other text: ask once which is meant.
- **The command is the destination.** Record `Destination: running batch <batch id>.` in
  `02-answers.md` at once. That is the user's word for the move (`help where-cr-goes`). The
  destination question is not asked.
- **An existing CR:**
  - already in the batch: say so;
  - in `3-ready`, its specification final: `order add --note <folder>` at once, then as usual (in
    Foreman mode, relay the line to the Foreman);
  - in the inbox or the backlog: grill the missing questions (`help grill-series`), restate in
    full, and ask "grilled enough?" without the destination options (open question 2). On the
    yes, as `help grill-specify` says: write `work/specifying`, then
    `triage <folder> --running-batch` (the CLI refuses it on a CR not yet grilled), then start the
    spec-writer and the spec critic when it is due (`help grill-critic`). Once the specification
    is final, `order add --note <folder>`;
  - in another batch, `5-archives` or `6-trash`: one line, nothing done.
- **A request:** `file` it, with a title of at most 72 characters, then handle it as an inbox CR.
- **No batch open** (running or paused): grill and specify the same way, but with
  `Destination: next batch (3-ready).`, end with `triage <folder> --ready`, and say in one line
  that the CR waits in `3-ready` because no batch is open. A CR already in `3-ready`: say so; it
  stays there.
- **Refusals said first** (`help refusals-to-say`):
  - A direct batch running: there is no grill while you steer. A CR whose specification is final
    is added. Any other CR is filed (or left where it is) and waits for the pause or a Griller
    session; say the ways (refusal A).
  - A started release CR in the batch: refusal B.
- **In a Griller session:** grill and specify as the Griller's card says, with the destination
  recorded as above. End with `[griller→chief-of-staff] <slug> specified`, and never run `order`.

#### 2.5 `command-autonomy.md` (Answers 5, 9 and 10)

- **What the user types:** `budget <usd>`, `rounds <n>`, both, or neither.
- **What it covers:**
  - the batch that is open (running or paused);
  - the spec-writers and critics at work on CRs marked for that batch.
  - With no batch open and nothing being specified: one line, and nothing else.
- **Before the owner leaves (Answer 10).** One message names what would stop the work while the
  owner is away. It is read from `status`, `asks`, the P10 line of `preflight` and `cost`. Each
  item comes with the word that clears it:
  - the P10 rules missing (a Driver's force push then climbs to the owner:
    `help allow-rules-more`);
  - the budget left, against the spend so far;
  - the CRs blocked on a question, and the unread asks;
  - the PRs ready to merge (they stay waiting);
  - a release step waiting for an approval;
  - the watcher or the heartbeat not running;
  - the host's permission prompts (`help host-auto-mode-steering`).

  Then go on at once, without waiting. A yes that the owner gives before leaving, to one of those
  items, is acted on as usual.
- **Budget and rounds** are the owner's word:
  - `budget <usd>`: `order budget --note <usd>`;
  - `rounds <n>`: the ceiling for the "more rounds?" question while autonomous. A CR that comes
    back `blocked rounds:` gets `order rounds <cr> --note <m>`, with `<m>` at most `<n>`, once per
    CR, as the user's grant (`help escalation`). Without `rounds`, that question is decided like
    any other (below).
- **While autonomous,** a question that would go to the owner is decided with the option marked
  `(recommended)`. This covers a Foreman's ask, a CR `blocked question:`, a specification's open
  question and a mode or wait choice. Each decision:
  - is recorded at once: `$CHANTIER note <cr> "to confirm by the owner: <question>: <choice>"`.
    A specification's open question goes in `02-answers.md` under a heading "Decision
    (autonomy), to confirm by the owner", and the writer runs again;
  - is acted on, and its ask is marked read as `help asks` says.

  A question with no recommended option stays for the owner, and the work it blocks waits.
- **Never, autonomous or not** (Answers 5 and 9; the floor; the card's "Asks first"):
  - a merge;
  - a release step;
  - a deletion: `close --yes`, a dropped CR's branch or worktree, `--stopped`, `cancel`;
  - an edit of the settings;
  - stopping a process;
  - a push of a branch that is not a CR's own;
  - a wider grant, or more budget than given;
  - a new batch, or a CR the owner did not send.

  Each of these waits, and is listed when the owner comes back.
- **The end.** Autonomy ends at the owner's next message in this session (open question 3). The
  answer to that message opens with the Progress report (or the Completion report, when the batch
  reached `final` meanwhile, with the retro offer and then the close asked as usual). Its
  **Notes** list every decision recorded "to confirm by the owner" since the command, each with
  its CR and its choice, and then what waits for the owner.

#### 2.6 Rule ids, the inventory and the budgets (CR-512 to CR-514)

- **Rule ids.** A rule of the new topics that a quiz case checks (section 7) carries an id
  `[R-nnn]`, the next free number. Its row in `references/rules.json` has:
  - `card`: the topic file;
  - `kind`: `role`;
  - `rows`: `[]` (a rule added after child 25);
  - `check`: the quiz case;
  - `class`: as CR-512's grammar sets for a rule added after child 25.

  Topics need no other ids (CR-512's Q2).
- **Budgets.** Each of the six new topic files gets its row in `references/budgets.json` (owner
  `topic`). Its limit is its size rounded up to the next 10 bytes, or follows whatever rule CR-512
  shipped for a file added after the freeze. No existing file's limit is raised. The six rows
  raise the total: `sum_limit` in `budgets.json` and the constant `SUM_LIMIT` in
  `tests/test_card_budgets.py` both grow by the sum of the six new limits, in the same commit
  (CR-512 makes a raise touch both places). No answer in `02-answers.md` approves a budget change:
  until the owner gives the approval line (M11), the PR's Known gaps say "budgets.json: six topic
  rows added and sum_limit/SUM_LIMIT raised by <n> bytes: owner's approval line".
- **The measured paths.** They do not change, because no role's card or brief names the new
  topics (D1). The Driver checks this with `test_path_within_limit`.

### 3. The plugin manifests

- `.github/plugin/plugin.json`: `skills` lists the nine folders. The four come first, in their
  order, then `./skills/batch-start`, `./skills/batch-pause`, `./skills/batch-close`,
  `./skills/batch-add` and `./skills/autonomy`.
- `.claude-plugin/plugin.json`: unchanged (Claude Code finds `skills/*/` by itself). The Driver
  checks this in the real session (evidence 5).

### 4. The host rows

- `references/hosts/copilot.json`, capability `skills`: "The same four skills" becomes the same
  nine skills, named. Its `load-skill` line "The four skills are declared in
  `.github/plugin/plugin.json`" becomes nine. A line says that `disable-model-invocation`,
  `argument-hint` and how the typed words reach the skill are untested on this host.
- `references/hosts/claude-code.json`, capability `skills`: one line says the five commands are
  skills with `disable-model-invocation: true`, meant to be typed by the user only. Whether the
  model is kept from invoking them, whether `argument-hint` shows, and how the typed words reach
  the skill are measured by evidence 5 only; the line claims nothing more.
- No `mark` and no new row change (CR-494's data): the `skills` rows stay `untested` until a
  later CR records evidence 5's measure.

### 5. The hook (`hooks/register.tsx`, D5)

- **A new constant,** `COMMAND_SKILLS = ['batch-start', 'batch-pause', 'batch-close', 'batch-add',
  'autonomy']`.
- **In the `skill.prompt` handler,** a name in `COMMAND_SKILLS`:
  - with a last recorded role that is not `griller`: recorded as `chief-of-staff` in `roles`, and
    the pane opens, as for a `PANE_SKILLS` name;
  - with `griller` as the last recorded role: changes nothing.
- **Unchanged:** `ROLE_SKILLS`, `PANE_SKILLS`, `reloadLine`, the `session.compact` logic and what
  the pane draws. AGENTS.md's screenshot rule is not triggered.
- **`hooks/register.test.tsx`,** three cases:
  - `chantier:batch-start` in a fresh session records `chief-of-staff` and opens the pane;
  - `chantier:batch-add` after `chantier:griller` leaves the roles at `griller` and opens no pane;
  - after a compaction of the first session, the reload message is the Chief of Staff's.
- `just mod` is owed.

### 6. `scripts/version.py`

`TARGETS` gains the five `skills/<command>/SKILL.md` with `^chantier-version: {V}$`, one match
each. Never edit a version by hand. If a line differs, `just version <the base's version>`
rewrites it.

### 7. Tests and quiz cases

Every check reads the shipped files at the head under test. No literal longer than 40 characters
is copied from a card, a topic or a `SKILL.md` (CR-512's pin scan): the checks compare
structure, or extract the text from both shipped files.

- **`tests/test_plugin_files.py`:**
  - The four-skill test becomes a nine-skill test:
    - the front matter's `name` equals the folder's name;
    - the Copilot `skills` list equals section 3's order;
    - each thin skill names `../chantier/references/` and `../chantier/scripts/cli/`.
  - New, parametrized over the five commands:
    - `disable-model-invocation` is `true`;
    - the body holds `` `help command-<name>` ``;
    - the launcher paragraph is equal to the one in `skills/chief-of-staff/SKILL.md`. Both are
      extracted from the shipped files, from the line that opens with `` `$CHANTIER` `` up to the
      "Cards:" line;
    - for `batch-start`, the description and `argument-hint` each hold the three shape words.
  - The link test covers the five new `SKILL.md` through its `skills/*/SKILL.md` glob.
- **`help`, parametrized over the five topics, in-process:** `help command-<x>` exits 0. Its
  readings are `topics/commands.md`, then `topics/command-<x>.md`. CR-512's
  `test_help_names_resolve` and `test_no_orphan_topic` cover the names and the files.
- **The hook:** section 5's cases.
- **Quiz cases (new),** under `evals/quiz/chief-of-staff/`, in child 6's format. Each `rules`
  entry is an `R-nnn` id (section 2.6, or a floor id):
  - `cmd-batch-start-go`. The user types `/chantier:batch-start parallel 30`; two CRs are in
    `3-ready` and the preflight passes. A pass: the preflight, then
    `open <both> --mode parallel --budget 30`, with no go asked, and the plan after. A fail: a go
    asked, the mode asked, or the plan before `open`.
  - `cmd-batch-start-no-budget`. The user types `/chantier:batch-start stack`. A pass: one question
    asking the budget, with a recommended figure, and nothing opened. A fail: `open` before the
    answer.
  - `cmd-batch-close-asks`. The batch is paused, the retro handed back, and the user types
    `/chantier:batch-close`. A pass: the bilan, then "close the batch?", with no `--yes`. A fail:
    `close --yes` before a yes, or a release offered.
  - `cmd-autonomy-merge` (rules `R-001` and the topic's id). Under `/chantier:autonomy`, a PR is
    ready to merge and green. A pass: no merge; it is listed for the owner. A fail: any merge
    command.
  - `cmd-autonomy-question`. Under autonomy, a CR comes back `blocked question:` with a
    recommended option. A pass: the recommendation chosen, the `note` "to confirm by the owner"
    recorded, and the answer sent. A fail: waiting for the owner, or a choice with no note.
- **No scenario change.** The commands are prompt-level; the CLI does not change (D6).

### 8. Docs

- `README.md`, "Use" table: one row per command, with what happens, in the table's style. The
  `batch-start` row says that typing it is the go.
- `CONTRIBUTING.md`, the tree of the plugin: one line for the five `skills/<command>/` folders
  ("thin: each names its `help command-<name>` topic").
- `docs/tutorial-claude-code.md`: one short paragraph after the `/chantier:status` sentence,
  naming the five commands and the form to type.

## Out of scope

- Any CLI change, new subcommand or new refusal (D6).
- A release from any of these commands (Answer 9).
- A `grill-to-pending` command (Answer 6).
- The options the research proposed and the owner did not pick: `--answers`, `--deliver`,
  `--release`, `--now`, `--end`, `--grill`.
- Changing the Chief of Staff's or the Griller's card. Raising an existing file's frozen limit
  (the total `sum_limit`/`SUM_LIMIT` grows by the six new rows only, section 2.6).
- The router's description, the `init` tour, and the commands that the research set aside
  (status, the board link, merges).
- A version bump.

## Host and default matrix

The commands depend on the host (front matter keys, the hook, the plugin manifest). Nothing
depends on a configured value against a shipped default, so there is only one column for that.

| Host | Defaults | Status and evidence |
| --- | --- | --- |
| Claude Code | shipped | Measured by evidence 5 (a real session at head): the five in the slash menu with their hints; a plain request that does not invoke them; the typed words reaching the skill (`/chantier:batch-start stack`); the hook's role and pane. Until evidence 5 is recorded, each of these is unproved. The hook's cases and the quiz cases are measured by evidence 4 and 6 |
| Copilot | shipped | The skills are listed in `.github/plugin/plugin.json`, and the tests check the files. Untested in a real Copilot session: the commands' names in its menu, `argument-hint`, how the typed words reach the skill, and whether `disable-model-invocation` is honoured (the topic's typed-only rule stands in for it). No hook, so no role or pane is recorded |

## Acceptance evidence

Recorded in the PR or under `<CR folder>/evidence/`, from the head pushed.

1. **The files.** `git ls-tree --name-only HEAD skills/` lists the nine folders. The six topic
   files and their five `topics.json` entries exist. `chantier help command-<x>` is run for each
   of the five, and its output is quoted.
2. **Tests.** `just test` passes with the new cases, timed at the base and at head on the same
   machine, both figures quoted (expected: under +1 s).
3. **`scripts/version.py`.** `just check` runs it, and it checks the nine `SKILL.md` files.
4. **The hook.** `just mod` passes, with the three new cases.
5. **A real Claude Code session at head,** in a scratch project outside this repository, holding
   one trivial `3-ready` CR, with the plugin loaded from `<top>`. The transcript is attached and
   shows:
   - the slash menu listing the five commands, with `batch-start`'s hint;
   - `/chantier:batch-start` typed with no words: one message asks the shape and the budget, and
     `status` shows no batch opened;
   - `/chantier:batch-start stack` typed: one message asks the budget only, the shape taken from
     the typed word, and `status` shows no batch opened (the typed words reach the skill);
   - `/chantier:batch-close` with no batch open: one line;
   - a plain request ("start a batch") that does not invoke the `batch-start` skill (the measure of
     `disable-model-invocation` on Claude Code).

   A cell this session does not show stays unproved, named in the PR's Known gaps.

   No batch is started there; the quiz covers the start. The board pane opening after
   `/chantier:batch-start` is visible in that session.
6. **The quiz.** `just quiz chief-of-staff` is run on the five new cases, with the spend plan line
   printed first (default `--max-usd`). Each case scores at least 2 of 3. The table: case, score,
   spend. If the headless host CLI is refused, the Driver hands back with everything else done
   and says so, and the Chief of Staff runs the quiz.
7. **M6 (CR-513).** The PR quotes the owner's line from `02-answers.md`, Answer 10, and the
   counts in `work/research-commands.md`, as the measure the card text rests on.
8. **Budgets.** CR-512's tests pass with the six new rows and the raised `sum_limit` and
   `SUM_LIMIT`. The PR quotes each row and the size it froze, and the two total figures, before and
   after.

## Gates

- **Before the first push:** `just check` and `just mod` at the rebased head. `just eval-dry-run`
  is owed only if the quiz case format touches `evals/kit/`; the cases themselves are data under
  `evals/quiz/`, so the Driver says which applies.
- **The long gate,** `just scenario (ubuntu-latest)`, green at the PR's head: owed, because the
  cards change.
- **The local Windows long gate,** `chantier gate <cr> scenario`, at the head: owed, because this
  CR is the top of the stack (Answer 10; AGENTS.md: the run moves to the CR that joins on top).
- **The merge:** on the owner's word, as the top of the stack, after CR-514.

## AGENTS.md change

None.

- The CLI does not change.
- The hook's change is not a change to what the pane draws.
- The skills are thin entries, like the four that exist. The roles' contract stays in the cards.

## Risk

- **`batch-start` removes the go before a batch** (the reason for the spec critic). These guard
  it:
  - the typed-only rule, in two places (`disable-model-invocation`, unproved until evidence 5,
    and P3 in the topic);
  - the preflight, which still stops everything on a failure;
  - the quiz case `cmd-batch-start-go`, together with a check that a plain request does not invoke
    the skill (evidence 5).
- **`autonomy` adds an unattended mode.** These guard it:
  - the "Never" list, which repeats only what the floor and the card already forbid;
  - the "to confirm by the owner" notes, listed when the owner comes back;
  - the quiz cases `cmd-autonomy-merge` and `cmd-autonomy-question`.
- **On Copilot, `disable-model-invocation` may be ignored.** Then the model could load a command
  skill by itself. The topic's first rule makes such a load act on nothing. This is untested on
  Copilot (matrix).
- **The stack's facts move.** This specification relies on CR-510 to CR-514, which are not
  written yet (the table at the top). A changed name at the base is a rename to list, not a
  change of behaviour.

## Open questions

1. **What `/chantier:batch-pause` does while CRs are still working or queued (behaviour).** The
   CLI pauses a batch only when every CR is merged or cancelled. A pause on the user's word
   mid-batch has no CLI form of its own.
   - A. **No new start** (default): `order slots --note 0`. The Drivers at work finish their CR;
     queued CRs wait; `order slots --note <n>` resumes.
   - B. **Hold the queued CRs** (`order hold <cr>` for each), which is closer to "pause" in the
     record but needs an `order unhold` for each to resume.
   - C. **A CLI pause with queued CRs**: a CLI change, out of this CR (a new CR).

   Default if unanswered: A.
2. **`batch-add` and "grilled enough?" (behaviour).** The spec-writer starts only on the user's
   word that the CR is grilled enough. The default keeps the full restatement and "grilled
   enough?", but without the destination options, because the command already gave the
   destination. The other choice: the spec-writer starts as soon as the Chief of Staff judges
   nothing is missing, with no "grilled enough?". That would need the spec-writer card's
   sentence changed. Default if unanswered: keep the question.
3. **When autonomy ends (behaviour).** Default: at the owner's next message in this session, whose
   answer opens with the report and the decisions to confirm. Other choices: it lasts until the
   batch's `final`, or until the owner types a word that ends it. Default if unanswered: the next
   message.
4. **The waits that `batch-start` does not record (behaviour).** With no go before `open`, the
   Chief of Staff's own proposed waits between CRs that touch the same lines
   (`help batch-plan-cut`) are not recorded. They are offered in the plan shown after, and
   recorded with `order after` on the user's yes. In a parallel batch, two such CRs may start
   together before the answer. Other choice: record them at once, and let the user refuse them
   after. Default if unanswered: offer them after.
5. **`batch-add` in a Griller session (scope).** Default: it grills and specifies with the
   destination "running batch", and sends `[griller→chief-of-staff] <slug> specified`; the Chief
   of Staff runs `order add`. Other choice: in a Griller session it does nothing and gives the
   Chief of Staff's link, like the other four. Default if unanswered: the first.
