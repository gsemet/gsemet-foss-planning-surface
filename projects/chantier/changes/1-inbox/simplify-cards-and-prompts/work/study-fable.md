# Study: a complete rewrite of the card mechanism

Fable study for `simplify-cards-and-prompts`, 2026-11-24, on chantier 0.15.1 (`3c29dd7c`).
Read-only: no card, wrapper or code was changed; no writing `chantier` command was run.

## 1. Summary (one page)

**The cards are 808 KB (about 200,000 tokens). What a role really reads is far above its declared
boot, and most of it is procedure the CLI already knows.**

Measured on 1,829 transcripts of the last 4 days (every project on this machine that runs
chantier), card bytes read per run, and the target:

| Role | Runs | Read today (mean) | Target per run | Cut |
| --- | --- | --- | --- | --- |
| Chief of Staff (session) | 2 | 343 KB (~86k tokens) | 40 KB | -88 % |
| Foreman (batch) | 3 | 157 KB (~39k tokens) | 25 KB | -84 % |
| Griller (session) | 8 | 81 KB | 12 KB | -85 % |
| Stack driver | 35 | 58 KB | 15 KB | -74 % |
| CR driver | 277 | 46 KB (~11.5k tokens) | 12 KB | -74 % |
| Release driver | 16 | 30 KB | 10 KB | -67 % |
| Verifier | 341 | 18 KB | 4 KB | -78 % |
| Inspector | 338 | 11 KB | 3 KB | -73 % |
| Other workers | 668 | 4 to 12 KB | 2 to 3 KB | -50 % |

Over the 4 days the roles ingested about 38 MB of card text (about 9.5 million tokens, before
cache re-reads). The CR driver alone is 34 % of it and the Verifier 16 %: the volume is in the
Drivers and the checkers, not in the Chief of Staff's card. The target brings the 38 MB to about
9 MB.

**The design in 10 lines:**

1. A card is a contract of at most 2 KB (workers), 4 KB (Drivers, Foreman) or 6 KB (Chief of
   Staff, Griller): goal, what you own, at most 5 role nevers, how you end, your reply format.
2. One shared floor of at most 1.2 KB holds the rules that protect the user and the repository;
   the CLI adds it to every prompt, so no card restates it and no contributor can leave it out.
3. The CLI writes the whole prompt (`chantier brief <role> <cr>`): card, floor, facts, host row.
   A role boots with zero `Read` call, and the parent copies one block.
4. Procedure leaves the cards. Every state-changing command ends with `next:` lines, and
   `chantier next` prints what is due now for the caller, from the record.
5. Rare cases become help topics of at most 1.5 KB (`chantier help <topic>`). A refusal and a
   state line name their topic, so a role reads a case only when it meets it.
6. The watcher and `status` print a `state:` line and a delta, not the whole batch at each wake.
7. Messages between agents go through the board (`chantier msg`, `chantier inbox`), not through
   host tables of who can reach whom.
8. The "never" rules a machine can check become refusals: in the CLI, and in the Claude Code hook
   that already guards writes.
9. Trial marks, dates and incident stories go to a proof log nobody loads; the CLI prints one
   word of it (`proved`, `untested`) with the host row it gives.
10. A test holds every card under its byte budget, so a retro fix lands as code, a `next:` line or
    a help topic, never as card text.

No behaviour is dropped by this design alone: a rule moves to a new home, and section 5 gives the
method that proves each move.

## 2. Measures

### 2.1 Sizes

| File | Size | Read by |
| --- | --- | --- |
| `chief-of-staff.md` | 206 KB | Chief of Staff |
| `driver.md` | 135 KB | the four Drivers |
| `hosts/claude-code.md` | 109 KB | steering sessions, Drivers (parts) |
| `foreman.md` | 85 KB | Foreman, direct-mode Chief of Staff |
| `concepts.md` | 74 KB | steering sessions, Drivers (parts) |
| `hosts/copilot.md` | 19 KB | steering sessions |
| `status-layout.md`, `pr-template.md`, `foreman-stack.md` | 17 KB each | by action |
| `verifier.md` | 15 KB | Verifier |
| `session-start.md` + `session-start-chief-of-staff.md` | 13 + 11 KB | Chief of Staff, Griller |
| `griller.md`, `init.md` | 11 + 10 KB | Griller |
| 9 other worker cards | 3 to 6 KB each | one worker each |
| 4 `SKILL.md` | 4 KB each, 3 KB of it the same `$CHANTIER` paragraph | loaded by the host |
| 15 wrappers | 1.0 to 1.5 KB each | loaded by the host |

Largest sections: "While it runs" (67 KB) and "Backlog and grill" (40 KB) of
`chief-of-staff.md`; "Your means" (52 KB) of `foreman.md`; "Words" (45 KB) of `concepts.md`;
"Configuration" (45 KB, of which "Allow rules" 26 KB) of `hosts/claude-code.md`; "Stack driver"
(31.5 KB) of `driver.md`.

### 2.2 Declared reading against real reading

"Declared" follows `startup-manifest.json` (`startup_sections`, then `actions`) and the cards'
"read X with your card" pointers. "Measured" is the sum of the `Read` results (and shell reads)
of card files in a transcript, each tool result counted once.

| Role | Declared boot | Declared for its common actions | Measured, median / mean |
| --- | --- | --- | --- |
| Chief of Staff | 36 KB (skill, cores, manifest, two session-start files) | `chief-of-staff`: 372 KB; direct mode adds `batch`: +159 KB | 343 / 343 KB (n=2) |
| Foreman | 6 KB (prompt, cores, two startup sections of 84 and 438 bytes) | `batch`: 288 KB (both hosts' cards); stack: +17 KB | 165 / 157 KB (n=3) |
| Griller | 25 KB | `grill`: 11 KB | 56 / 81 KB (n=8) |
| CR driver | 11 KB | 3 action lines: 33.5 KB; plus host "Tools" 20 KB, concepts 7 KB, `pr-template.md` 17 KB | 45 / 46 KB (n=277), max 131 KB |
| Stack driver | 11 KB | 55 KB | 50 / 58 KB (n=35) |
| Release driver | 11 KB | 36 KB, plus `release-template.md` 5.5 KB | 32 / 30 KB (n=16) |
| QA driver | 11 KB | 25 KB | no run in the sample |
| Verifier | 8.6 KB + card 14.8 KB | - | 15 / 18 KB (n=341) |
| Inspector | 8.6 KB + card 6.1 KB | - | 6 / 11 KB (n=338) |
| Coder | 8.6 KB + card 4.7 KB | - | 5 / 9 KB (n=256) |
| Spec-writer | 8.6 KB + card 3.3 KB | - | 7 / 12 KB (n=178) |
| Spec critic | 8.6 KB + card 3.8 KB | - | 6 / 11 KB (n=103) |
| Conflict resolver | 8.6 KB + card 3.9 KB | - | 4 / 6 KB (n=70) |
| Debugger | 8.6 KB + card 3.7 KB | - | 3.8 / 3.8 KB (n=33) |
| Investigator | 8.6 KB + card 3.6 KB | - | 3.7 / 4.3 KB (n=17) |
| Retro critic | 8.6 KB + card 3.0 KB | - | 4.7 / 7.1 KB (n=11) |
| Demo explorer, board-griller | 8.6 KB + 3.5 KB; 2.2 KB + `griller.md` 10.8 KB | - | no run identified |

Three findings from the gap:

- **The startup manifest made the declared boot small and left the real reading whole.** The
  Foreman's two startup sections are 84 and 438 bytes; its first action then lists 288 KB. A test
  holds the boot under 12,544 bytes (`test_startup_manifest.py`) while a Foreman reads 157 KB.
- **Workers ignore the cores, and nothing breaks.** The prompt the CLI prints for a worker names
  only its card and the project's rules. Across 341 Verifier runs, `startup-core.md` and the
  manifest average 12 and 13 bytes per run: they are not read. `concepts.md` ("The prompt",
  line 519) says every prompt names them; the CLI's worker lines do not.
- **A worker starts at about 17,000 tokens before any card** (the host's system prompt and tool
  schemas). chantier does not own that part. For workers the card is 1,000 to 4,000 tokens more,
  so their gain is real but small per run; it counts because there are about 1,350 worker runs in 4 days.

### 2.3 What the CLI already prints

| Output | What it carries today | Size seen |
| --- | --- | --- |
| `take`, `handoff`, `round` | the CR's facts, the notes, a checklist "gates before handback ready" with `[x]` marks, the `team:` lines, the opening lines of every worker role | CR driver: 15 KB over 12 calls per run |
| `take`, `take stack`, `order qa` | the Driver's whole prompt skeleton (`driver_prompt.py`), with the `Rewrites:` rule | 2 to 3 KB |
| `status` | one line per CR, merged ones included; orders; asks; watcher and board lines with the exact command to run | 5.5 KB for batch-31 (22 merged CRs listed at each call) |
| `open`, `pause` end | a `next:` line (3 places in the code) | one line |
| `watch` | one sentence per event; its end lines say who must do what, with the command | one line each |
| `--help` | 47 commands; several helps already state a rule (`asks`, `close`, `gate`) | 9 KB at top level |
| `playbook` | agent, model, timing, limits, first lines of three roles | 2.5 KB |
| refusals | exit 2, 3 or 5 with a sentence (`rails.py`); `access` explains a refusal | one line |

The Foreman's CLI output is 184 KB per batch over 180 calls, more than its cards. The Chief of
Staff's is 173 KB over 172 calls. A `status` that repeats every merged CR at each wake is a large
part of it.

The journal already addresses events (`project`, `role:<name>`, `cr:<id>`, `session:<key>`,
`user`; `watch --for`). I found 11 event types and no command by which one agent writes a
message to another: `chantier msg` below is a proposal on that base.

## 3. What the cards hold, by kind

The split below is an estimate: keyword counts on every paragraph, plus a full read of about
11 % of the text (parts of `foreman.md`, `driver.md`, `concepts.md`, `chief-of-staff.md`, both
host cards, the session-start cards). It is not a sentence-level inventory; section 5 asks for one.

| Kind | Estimate | Share |
| --- | --- | --- |
| (a) rule that protects the user or the repository | 40 KB written, 6 to 8 KB once deduplicated | 5 % |
| (b) rule the model would infer alone | 120 KB | 15 % |
| (c) incident or retro patch: one case, its exception and its wording | 200 KB | 25 % |
| (d) host trial and "unproved" bookkeeping | 110 KB | 14 % |
| (e) state or procedure the CLI or watcher could print just in time | 260 KB | 33 % |
| (f) duplicated or contradictory text | 60 KB | 8 % |

Examples, with their place:

- **(a)** `concepts.md:735` "Never merge without the user's word"; `driver.md:817` "You never
  discard the worktree's work: no `git reset --hard`..."; `startup-core.md:15` "No fallback".
  `concepts.md:710-800` ("Rules", 8.8 KB) is already a floor of ten rules, at the end of a 74 KB
  file, and each card restates parts of it.
- **(b)** `driver.md:99` "`$CHANTIER note <cr> "<one sentence>"` after each step worth knowing";
  `foreman.md:258` "A brief ... states a past fact only with its source".
- **(c)** `foreman.md:83-143`: one bullet of 60 lines on how the wording of an ask changes with
  `--no-gate`, a waiver, a local-run rule, a `deliver by` time and a stack's top. `concepts.md:588`
  "which the probe of 2026-11-10 accepted". `driver.md:116` "the host compacted agents carrying
  200,000 from about 162,000 tokens".
- **(d)** `hosts/claude-code.md:18-66`: the "Tools" table is 20 KB, most of it the "Mark" column
  (one row: "proved 2026-11-20 (the Studio's batch-07 Foreman); with this model: **unproved** until
  seen. Trial: batch-11..."). The file has 54 "unproved" and 47 "proved"; `copilot.md` has 27
  "unproved" in 19 KB. Paragraphs touching a trial word: 64 % of `claude-code.md`, 81 % of
  `copilot.md`.
- **(e)** `foreman.md:274-314`: the early conflict check, 3.5 KB that fix a `git merge-tree`
  command, its exit codes, the note to record and the ask to send. `driver.md:859-880`: the order
  commit, rebase, gate, push, PR, `ship`, CI, verifier, closing note. `session-start-chief-of-staff.md:106-120`
  lists the watcher's lines one by one, each of which already says what to do.
- **(f) duplicated:** the `$CHANTIER` launch paragraph, 3 KB, word for word in the 4 `SKILL.md`.
  "Copied as printed, never retyped" in `concepts.md:491`, `driver.md:85-92`, `foreman.md:230`
  and `chief-of-staff.md` (Hard rules). "(never `$CHANTIER`: a CLI that cannot run is a stop,
  `startup-core.md`)" in `driver.md:75`, `concepts.md:510`, `concepts.md:724` and
  `chief-of-staff.md:57`. The first-line refusal in 15 wrappers and `concepts.md:555-563`.
- **(f) contradictory:** `role-core.md` "At boot read only the cores, your wrapper and the
  manifest's startup sections" against the worker wrappers "Your card ... read it first, before
  any other step". The manifest's `batch` and `chief-of-staff` actions list `hosts/claude-code.md`
  **and** `hosts/copilot.md` for any host, against the cards' "your host's reference". The
  `concepts.md:519` prompt template (cores and manifest) against the worker lines the CLI prints
  (card only).

## 4. The target design

### 4.1 What a role boots on

```text
chantier <role> for <cr> "<title>" of batch <batch>, in the project <root>.   (unchanged first line)
<the card, at most its budget, inline>
<the floor, at most 1.2 KB, inline>
<facts: cli, worktree, folder, spec, PR, rounds, notes>
<host row: how you start a child, how you end, in 2 to 4 lines, only for this host>
Then: `$CHANTIER next` says what is due; `$CHANTIER help <topic>` when a line names one.
```

`chantier brief <role> [<cr>]` prints this block whole. `take`, `round` and `handoff` stop
printing the opening lines of every worker role; a Driver asks `brief coder <cr>` when it starts
a Coder. The text is byte-stable for a role and a version, so the host's prompt cache holds.

The wrapper keeps its frontmatter and the first-line refusal, and loses the reading orders.
`startup-core.md`, `role-core.md`, the two `host-core-*.md` and `startup-manifest.json` go away:
their content is the floor, or the CLI's own behaviour.

### 4.2 Budgets

| Role | Card today | Card budget | Boot today (measured path) | Boot target | Whole run target |
| --- | --- | --- | --- | --- | --- |
| Chief of Staff | 206 KB + skill 4.5 KB | 6 KB | 343 KB | 8 KB | 40 KB |
| Griller | 10.8 KB + skill 4 KB | 4 KB | 81 KB | 6 KB | 12 KB |
| Foreman | 85 KB (+17 KB stack) | 4 KB | 157 KB | 6 KB | 25 KB |
| CR driver | 135 KB shared | 4 KB | 46 KB | 6 KB | 12 KB |
| Stack driver | 135 KB shared | 4 KB | 58 KB | 6 KB | 15 KB |
| Release driver | 135 KB shared | 3 KB | 30 KB | 5 KB | 10 KB |
| QA driver | 135 KB shared | 2 KB | not measured | 4 KB | 5 KB |
| Verifier | 14.8 KB | 3 KB | 18 KB | 4 KB | 4 KB |
| Inspector | 6.1 KB | 2 KB | 11 KB | 3 KB | 3 KB |
| Coder | 4.7 KB | 1.5 KB | 9 KB | 3 KB | 3 KB |
| Investigator, Debugger, Conflict resolver | 3.6 to 3.9 KB | 1.5 KB | 4 to 6 KB | 3 KB | 3 KB |
| Spec-writer, Spec critic, Retro critic, Demo explorer | 3 to 3.8 KB | 1.5 KB | 7 to 12 KB | 3 KB | 3 KB |
| Board-griller | 10.8 KB | 2 KB | not measured | 4 KB | 6 KB |

Boot target = card + floor (1.2 KB) + host row. "Whole run" adds the help topics a usual run
meets (3 for a CR driver, 6 to 8 for a Foreman).

### 4.3 What is fetched just in time, and by what

| Need | Carrier | Today |
| --- | --- | --- |
| What do I do now | `chantier next` and the `next:` lines at the end of each command | the role's section, read ahead |
| A rare case (a refused force push, a lease not confirmed, a worker that fails) | `chantier help <topic>`; the refusal or the state line names the topic | 27 "Means:" sections in `driver.md`, 580 lines of "Your means" in `foreman.md` |
| A command's usage and its limits | `<command> --help` | restated in the cards |
| Where the batch stands | `state:` line of the watcher and of `status`; `status --since <seq>` gives the delta | `status` whole at each wake |
| What a peer says | `chantier inbox`, fed by `chantier msg <to> <kind> <text>` and delivered by the watcher | `[foreman→driver]` conventions and host tables |
| How this host does a thing | the host row in `brief`; `chantier host <capability>` | `hosts/claude-code.md` (109 KB) |
| Why a host behaviour is believed | `docs/proofs/<host>.md`, never loaded | the "Mark" column in the cards |

The owner's wish holds here as a rule of design: a role that stumbles gets a refusal that says
what to run. Example: `refused (exit 3): the lease of CR-481 is live (Driver a1eb, 4 min).
See: chantier help lease`.

### 4.4 What moves into code

| Today in a card | Becomes |
| --- | --- |
| `$CHANTIER` paragraph (3 KB in 4 skills): dev or plugin mode, `uv sync --check`, `sync pending` | a launcher in the plugin (`bin/chantier`) that decides the mode, checks the sync and prints `sync pending: held by ...` itself |
| How an ask is worded from a hand-back (`foreman.md:83-143`) | `chantier judge <cr>`: prints the ask ready to record, or the take-back command with its note; the Foreman still reads the project's rule when the reason quotes one |
| Early conflict check (`foreman.md:274-314`) | `chantier conflicts <cr>`: runs the pairs, records the notes, prints the one ask |
| Order of ship and proof (`driver.md:859-880`), `phase` before each step | `next` after each of `round`, `gate`, `ship`, `verdict`; the commands record their own phase |
| "Check the reply's format" (`driver.md:76-83`) | `chantier reply-check <role> <file>`; `verdict` already does it for the Verifier |
| Retro sources and layout (`foreman.md:30-66`) | `chantier retro draft`: the asks, blocks, refusals, restarts, red gates and cost outliers of the events, as draft points |
| Which host card and which row | `brief` and `host`, from a data file per host (capability, means, mark) |
| "Record the agent id" after each start | the hook records it at `SubagentStart` on Claude Code; `agents set` stays for Copilot |
| Never `git merge`, `gh pr merge`, `git reset --hard`, `git clean`, `git stash`, plain `--force`, `pkill`, `cd` into a CR folder | refusals of the hook that already guards writes (`hooks/register.tsx`), with the rule in the refusal's text; `ship` refuses a branch that holds a merge commit |
| The watcher's lines explained one by one | nothing: each line already says who does what |

A rule that becomes a refusal stays in the floor too, in one line. The refusal is the net; the
floor is why the model does not try.

### 4.5 The Foreman

The Foreman stays the orchestrator and keeps its judgement: which CR goes next, what a Driver
must hear, what goes up. Its card (4 KB) holds its goal, the user's boundaries in 6 lines, its
loop and its end. Its tools:

| Tool | State | What it gives |
| --- | --- | --- |
| `chantier next --epoch <n>` | new | the due list, from the record: `take CR-484 (slot free)`, `O-21 undone: order done after ...`, `CR-481 handed back: judge CR-481`, `nothing due: wait` |
| `state:` line | new, on each watcher line and each `status` | `batch-31 e1 | working 2, ready 1 (asked), queued 1 | slots 1/4 free | due 2 | heartbeat 1 min` |
| `watch --for role:foreman` | changed: the Foreman runs its own watcher | wakes on a hand-back, an order, a message, a red check; the 30-minute heartbeat becomes the fallback |
| `status --since <seq>` | new | only what changed; merged CRs become one count |
| `chantier judge <cr>` | new | the ask or the take-back, see 4.4 |
| `chantier conflicts <cr>` | new | the early conflict check |
| `chantier brief <role> <cr>` | new, replaces the skeleton of `take` | the whole prompt of a Driver |
| `chantier msg`, `chantier inbox` | new | a note to a working Driver, an `anomaly` from a Driver before its end |
| `chantier retro draft` | new | the retro's draft points |
| `chantier help <topic>`, `help --for foreman` | new | the cases; `--for` lists the topics by their trigger |
| `order merged` | changed | fast-forwards the main checkout itself or prints the one command as `next:` |

`foreman-stack.md` becomes the `stack` help topics; a stack batch adds one line to the card
through `brief` ("this batch is a stack: every ask is the stack's").

### 4.6 The proof log

`docs/proofs/claude-code.md` and `docs/proofs/copilot.md` take every mark, date, batch name and
trial. A host data file keeps one word per capability. The CLI prints `(untested)` beside a row
whose mark is not `proved`, and the floor keeps the one sentence "say an untested path is not
tested". `docs/incidents.md` takes the stories behind the patches; a help topic may link to it,
and no role loads it.

### 4.7 A role written by someone outside

```markdown
---
name: security-reviewer
kind: review-step            # worker | review-step | critic | driver
started_by: cr-driver
tools: Bash, Read, Grep, Glob
writes: none                 # none | worktree | cr-folder
reply: verdict-json          # a format the CLI checks
help: [evidence]
---
## Goal
## You own
## Never
## Done when
```

At most 2 KB of body. `chantier roles lint` holds the budget, refuses a date, a batch name or a
trial mark in a card, and checks the reply format exists. `chantier roles build` writes the host
wrappers (`agents/*.md`, `com.github.copilot/agents/*.agent.md`) from the frontmatter, so the 30
wrapper files are generated. A project names its own roles in `chantier.yaml`; the floor and the
write guard apply to them as to chantier's own.

## 5. Proving that no behaviour is lost

**The inventory.** One table, one row per behaviour, extracted from today's cards section by
section (agents in parallel, a critic on each extract):

| id | role | trigger | behaviour required | source `file:line` | kind (a-f) | new home | check |
| --- | --- | --- | --- | --- | --- | --- | --- |

"New home" is one of: card, floor, CLI refusal, `next:` line, help topic, proof log, dropped as
inferred. `evals/SCORECARD.md` seeds it: its 50 rails (21 of the CLI, 29 of judgement) are
already written this way. The owner reviews two lists only: every row of kind (a), and every row
marked "dropped".

**The checks.**

1. A row moved to code has a pytest or a check of `just scenario` (no model, free).
2. A row moved to a `next:` line, a help topic or the floor carries its id in that text; a test
   fails when an id of the inventory has no home.
3. A row left to the model's inference is proved by a **situation quiz**, a new cheap eval with
   no batch: the role's new boot, one situation from the inventory, the question "what do you do
   next", a judge that reads the row. A row may be "dropped as inferred" only when the model the
   playbook gives that role passes it 3 times out of 3 with no card text for it. The same quiz on
   today's cards gives the baseline: the new cards must score at least as well.
4. The existing campaigns run on both card sets (`claude-planted` for the planted failures,
   `real-foreman` and `real-direct` on the sandbox) and the two scorecards are compared line by
   line, with the cost and the count of turns per CR.

**The 10 rules to keep word for word:**

| # | Rule | Place today |
| --- | --- | --- |
| 1 | Never merge without the user's word; the Foreman merges only a release PR or a granted fix after `release go` | `concepts.md:735`, `foreman.md:83`, `chief-of-staff.md:72` |
| 2 | A CR's branch is updated by rebase only; `--force-with-lease` on its own `chantier/*` branch, never the default or a protected branch, never plain `--force` | `concepts.md:740-752`, `driver.md:163`, `driver_prompt.py` (`Rewrites:`) |
| 3 | No fallback: a tool, model, agent or command not available as named is a stop | `startup-core.md:15`, `concepts.md:719`, `chief-of-staff.md:53` |
| 4 | A CLI that cannot run is a stop: no repair, no other source, never "without it" | `startup-core.md:3-13` |
| 5 | Never discard the worktree's work (`reset --hard`, `checkout --`, `restore`, `clean`, a deleted file) | `driver.md:817` |
| 6 | An irreversible release action waits for the user's go; half-done irreversible work stops and says what is out | `driver.md:1474`, `driver.md:1588` |
| 7 | Only the user starts work: no Foreman, no steering, no backlog item without the go in that turn | `chief-of-staff.md:69` |
| 8 | No image shows the user's username or home folder | `driver.md:483` |
| 9 | Refusals are reported with their exact text, never worked around; an absent long gate never means success | `concepts.md:738`, `foreman.md:127` |
| 10 | Never stop a process by name or pattern, never kill a holder for a sync; `close --yes` and the removal of a dropped CR's worktree only on the user's yes in this turn | `driver.md:168`, the skills' `$CHANTIER` paragraph, `chief-of-staff.md:2301` |

Close behind: state changes only through the CLI (`concepts.md:717`); the Foreman's chat obeys
only "stop" and "hold" (`foreman.md:184`); nothing posted on a tracker issue without the user's
approval (`chief-of-staff.md:2304`); an untested host path is said untested
(`hosts/claude-code.md:16`).

## 6. Order of work

| CR | Content | Behaviour change | Risk |
| --- | --- | --- | --- |
| 1. Measure and inventory | the transcript measure as a `just` target; the behaviour inventory; the situation quiz with its baseline on today's cards | none | low; it costs agent time |
| 2. Proof log | marks, dates and trials out of the host cards into `docs/proofs/`; one word kept per row | none | low; about 85 KB less in the host cards |
| 3. Quick cuts | the launcher instead of the `$CHANTIER` paragraph; the manifest lists only the session's host; `status --since`; `handoff` without every role's opening lines | none intended | low to medium: the launcher changes the command the allow rule P10 matches |
| 4. The tools | `next`, `next:` lines, `help <topic>`, `brief`, `judge`, `conflicts`, `retro draft`, `msg` and `inbox`, the `state:` line, refusals that name a topic | additive | medium: a wrong `next:` line misleads every run, so each is tested in the scenario |
| 5. Refusals | the hook's refusals of the "never" commands; `ship` refuses a merge commit | a prose rule becomes a refusal | medium: a false refusal blocks a Driver |
| 6. The rewrite, by family | cards v2 behind a `cards:` key: workers, then the Drivers (CR, release, stack, QA), then the Foreman, then the Chief of Staff and the Griller; each family passes the quiz and one campaign against v1 | the big one | high for the Foreman and the stack driver |
| 7. Roles as data | the role format, `roles lint`, `roles build`, generated wrappers for both hosts, project roles in `chantier.yaml` | none for existing roles | medium on Copilot: its wrappers are untested here |
| 8. Removal | v1 cards, the manifest and the cores deleted after two releases on v2 | none | low |

CR 1 to 3 are the safe wins and may ship before any decision on the rewrite. CR 4 and 5 improve
the tools while the old cards still work, which is also the fallback if the rewrite stalls.

**Plugin and Copilot.** A batch records the card set it opened with, as it records its playbook,
so a running batch never changes cards. An old session meets the new plugin through `reload`,
which becomes one `brief`. Copilot has no hook: its roles keep every "never" in the floor and get
the CLI refusals only; its wrappers are generated in CR 7 and need one `copilot` campaign.

**Rollback.** `cards: v1` in `chantier.yaml` (or an environment variable for one session) brings
the old cards back until CR 8; the tools of CR 4 and the refusals of CR 5 stay, since v1 cards
work with them.

**Risks of the whole.** Stumbling may cost more turns than the reading saved: the count of turns
and the cost per CR are compared in every campaign. Sonnet 5.5 Drivers may infer less than Opus:
the quiz runs on the model of each role. A small card regrows: the budget test and the lint
refuse it.

## 7. Decisions for the owner

1. **May a prose "never" become a refusal?** The hook would refuse `git merge`, `gh pr merge`,
   `git reset --hard` and the like for chantier's agents. Options: refuse; warn only; keep prose.
   Recommendation: refuse on Claude Code, with the rule in the text.
2. **How much stumbling is accepted?** Options: any, while the cost per CR does not rise; at most
   2 refused commands per CR; none on the common path. Recommendation: none on the common path
   (`next` covers it), free stumbling on rare cases.
3. **Is `next` an order or advice?** Recommendation: advice for the choice of the CR and the
   wording; the safety steps are refusals, not advice.
4. **Rare incident patches with no trigger the CLI can detect:** keep each as a help topic
   nobody is led to, or drop it until the case comes back? Recommendation: drop, after the owner
   reads the list.
5. **May a Driver message the Foreman during its run, through the board?** Options: every
   message wakes the Foreman; only `anomaly` and `blocked` wake it and notes wait for its next
   wake; no message before the end, as today. Recommendation: the second.
6. **May the CLI word the asks (`judge`)?** The user would read more uniform asks.
   Recommendation: yes; the Foreman may add one sentence.
7. **Does the user still hear "I have not tested this path"?** Recommendation: yes, from the mark
   the CLI prints; the trial's story leaves the cards.
8. **What may an outside role be?** Options: review steps and critics only; workers that write in
   the worktree too; Drivers too. Recommendation: review steps, critics and workers; never a
   steering role.
9. **One floor for all roles, or a "never" list per role?** Recommendation: one floor of at most
   1.2 KB, plus at most 5 role nevers.
10. **Does direct mode keep the same tools as the Foreman?** Recommendation: yes; the Chief of
    Staff in direct mode gets the Foreman's card through `brief` and uses `next`.
11. **Both card sets for two releases behind `cards:`, or one switch?** Recommendation: both,
    v2 by default once one `real-foreman` and one `claude-planted` run match v1's scorecard.
12. **Is the byte budget a gate?** A retro fix would then land as code, a `next:` line or a help
    topic, never as card text over the budget. Recommendation: yes; it is what keeps the cards
    small after the rewrite.

## 8. What I could not check

- **Small samples:** Chief of Staff n=2, Foreman n=3. 140 main sessions were not classified by
  role (4.5 MB of card reads in them): some are Chief of Staff or Foreman sessions whose first
  message I did not recognise.
- **No run seen:** QA driver, Demo explorer, board-griller, and every Copilot role. The Copilot
  wrappers were not measured.
- **The split by kind** is an estimate (keywords, and 11 % of the text read), not an inventory.
- **Cost in money:** I counted bytes read once per run. The price of the cache re-reads at every
  later turn, and the real saving in dollars, are not computed.
- **The skills' own load** (`SKILL.md`, 4 KB each) is outside the measured reads.
- **Whether a plugin can ship a launcher** the host's allow rule matches as it matches today's
  `uv run` form: a trial settles it.
- **Whether the hook can refuse a shell command by its content for every agent** as it does a
  write: `hooks/register.tsx` judges shell writes today; I did not read it whole.
- **No eval was run**, and no card text was tried on a model: every target size is a design
  budget, not a result.
