# SC21: New card: the Foreman, with its topics

Child 21 of 28 of the program `simplify-cards-and-prompts`. These rank above this specification,
in this order: the program's `03-change-spec.md`, its `02-answers.md` (answers 17 to 22) and its
`work/study-*.md`. Short ids such as F5, Q4 and Q6 are the program's findings and questions, as the
Chief of Staff settled them in answer 22. The owner confirms answer 22 when they wake.

Child 19's specification (`4-batch/1-pending/505-sc19-cards-workers/03-change-spec.md`) sets the
method for all the card children: where the files live, the budgets, the inventory and the proof.
This file follows it. Where this file seems to differ from it, child 19 wins.

## Goal

Write the Foreman's card of the target card set, and the Foreman's help topics, in
`skills/chantier/cards-next/`, a folder nothing loads.

Today the Foreman reads `references/foreman.md` (36,927 bytes at `origin/main` 8a960d34) and eight
`foreman-*.md` pieces (69,203 bytes). Its start reading is declared at 91 KB and was measured at
144 KB (study-fable-v2). The target is a card of 4 KB, plus the floor and the host rows that
`brief` adds. Every rare case moves to a topic, a `next:` line, a refusal, `judge`'s wording or
`--help`.

The card section "The user's boundaries" (12.1 KB, `foreman.md:59-184`) is not cut blindly. Each
of its rules is sorted under F5:
- a rule that protects the user or the repository lives in the floor, in this card, or in a named
  CLI refusal, and never in a topic alone;
- the rest becomes topics.

Section 4 gives the split, rule by rule.

## Place in the chain

- **Base: child 20's branch** (`sc20-cards-drivers`), the batch's stack top when this child joins
  (F16). The Driver rebases on it before the first push.
- **Relied on, below in the stack.** If any of these is missing at the base, the Driver stops and
  says so. There is no stand-in.
  - child 1: `chantier push` (the Drivers' push);
  - child 6: `just quiz <role> --cards <folder>`, its cases and its baseline of the old cards;
  - child 7: the topic format, `chantier help`, and the topic names the CLI prints;
  - child 8: the host rows;
  - child 10: `chantier brief foreman --cards <folder>`, and `cards-next/floor.md`, which child 19
    copies;
  - child 12: `next --epoch N`, and the `next:` lines;
  - child 13: `msg steering` and `inbox`;
  - child 14: `judge <cr>`;
  - child 15: `chantier conflicts <cr>`;
  - child 16: `retro draft`;
  - child 18: `roles.yaml`, whose `card` field for `foreman` is `foreman.md`. So
    `brief foreman --cards skills/chantier/cards-next` reads `cards-next/foreman.md` directly, and
    no staging folder is needed (unlike child 20's Drivers);
  - child 19: `cards-next/`, its `floor.md`, the first `cards-next/topics.json`, and the method;
  - child 20: the Driver side of the shared topics `lease` and `refused-push`, to which this child
    adds the steering side.
- **Next:** child 22 (the Chief of Staff and the Griller) builds on this branch. In direct mode the
  Chief of Staff steers with this card (answer 13). Child 22 writes the differences (topic
  `direct`) and the Chief of Staff's side of the refused-push route.
- **Later:** child 23 writes the shared cards this card links to (`concepts.md`, `routing.md`,
  `pr-template.md`, the final `topics.json` and `floor.md`). Child 24 swaps the set in. Child 25
  reviews every removed rule from this child's inventory.
- **Merge:** under the program's merge rule (answers 14 and 22: F2, F11, Q8).
  - The merge waits for the owner. Nothing merges while the owner sleeps.
  - Children 19 to 28 merge as one unit, in order, in one sitting, with no session started in
    between, and only after child 28's campaign has passed.

## Decisions carried

| Source | Decision | Where here |
| --- | --- | --- |
| Answer 1 | Smallest card, no behaviour lost. The roles and the Foreman's duties do not change | sections 2 to 4 |
| Answer 3 (Q6) | No stumbling on the common path; free stumbling on rare cases | common path in the card, rare cases in topics |
| Answer 4 (Q7) | Only `anomaly` and `blocked` wake the Foreman. A note waits for its next wake | card, "Messages" |
| Answer 8 (Q5b) | A refused push or rebase of a batch's `chantier/*` branch: the Chief of Staff runs it alone and tells the user in the report | topic `refused-push`, steering reading; card never 3 |
| Answer 10 (Q10) | A rare incident rule with no CLI trigger becomes a topic for one release, with `review_by` | section 3 |
| Answer 11 (Q11) | `next` is advice on the choice of CR and the wording. The safety steps are refusals. The CLI words the ask and the Foreman adds at most one sentence | card, "You own" and "The CLI" |
| Answer 12 (Q12) | No steering role comes from outside | the Foreman card stays chantier's own |
| Answer 13 (Q15) | In direct mode the Chief of Staff gets this card and the Foreman's tools | card intro; topics serve `foreman` and `chief-of-staff` |
| Answers 14, 17; F2 | One card set, written beside the old one, nothing loaded until the swap | `cards-next/` only |
| Answer 15 (Q14) | A card is one short file, a rule lives in one place, a piece is loaded at its moment | no rule written twice; the floor is not restated |
| Answer 16 (Q13); M3 | No date, batch, CR id, model, token count, "proved", "unproved" or trial story in a card | all files; the GitLab marks of today's text are listed, not copied (section 5) |
| F3, Q6 | The refused-push route stays for good. The steering session keeps the plain `git push --force-with-lease` | topic `refused-push`, steering reading |
| F4 | Quiz pass rule: no case scores 0 of 3 that the old cards passed. Spend cap printed first | Acceptance evidence 4 |
| F5 | A protecting rule lives only in the floor, the card or a refusal. The cap on nevers gives way before it | section 4 |
| F6, F11 | Handed back validated, with the Known gap "real run not done (child 28)" and a typed merge wait on child 28 | Handback |
| F17 | An unproved behaviour keeps the one word "unproved" in a topic, never a trial story | topics |
| F20 | State the seconds added to `just test` | Acceptance evidence 7 |
| Q4 | A card or topic above its target goes in Known gaps with its size. Only the owner raises a target | Acceptance evidence 2 |
| Program, child 21 | Scope: Foreman card and topics; `foreman-stack.md` becomes the `stack` topics, and a stack batch adds one line through `brief`; chat obeys only "stop" and "hold"; "The user's boundaries" sorted under F5; acceptance adds the split list | the whole specification |
| Child 19 | Files in `cards-next/`, topics in `cards-next/topics/`, `topics.json` in child 7's format, 1 KB = 1,000 LF bytes, topic 1,500 bytes, inventory in `<CR folder>/evidence/cards-inventory-<family>.md`, no test added, no quiz case added | sections 1, 3, 5; evidence |
| `02-answers.md` of this CR | Specified from the program. No separate critic. Destination: running batch batch-31 | this specification as written |

## What changes

Paths are from the repository root. `src/` is `skills/chantier/scripts/cli/src/chantier/`. Sizes
are LF bytes, read from git (`git show HEAD:<path> | wc -c`). "Today" means `origin/main` 8a960d34.
The Driver re-measures at its base, and the PR gives the base's figures.

### 1. The files this child adds or extends

| Path | Use | Budget |
| --- | --- | --- |
| `skills/chantier/cards-next/foreman.md` | the Foreman's card (new) | 4,000 |
| `skills/chantier/cards-next/topics/<name>.md` | the Foreman's topics (new, section 3) | 1,500 each |
| `skills/chantier/cards-next/topics.json` | child 19's file: this child adds its rows, and adds a reading and two roles to the shared rows `lease` and `refused-push` | none |

UTF-8 with no BOM, LF endings. No other file changes. No file of child 19 or 20 is edited, except
the two shared rows of `topics.json`, which gain the steering readings.

### 2. The card, `cards-next/foreman.md`

Child 19's shape, in this order and nothing more: title, goal, what the role owns, its nevers, how
it ends, its reply format, and one "Rare cases" line naming the topics.

What it leaves out, because it reaches the Foreman another way:
- the brief's facts (child 10): the CLI with `--batch`, the repository, the batch, the epoch, the
  team, the timing lines, the Needs line, and "the project's rules rank above the card; run
  `$CHANTIER rules` first";
- the floor's ten rules: never merge without the user's word, rebase only and
  `--force-with-lease` on the CR's own branch, no fallback, a CLI that cannot run is a stop, never
  discard a worktree's work, an irreversible release action waits for the user, only the user
  starts work, no image showing the username or the home folder, report a refusal verbatim,
  never stop a process by name or pattern;
- the host rows (child 8): starting, messaging and stopping a Driver, the heartbeat wake, ending
  a turn, compacting, the write guard;
- the `--epoch` list (`foreman.md`, "Exactly these commands carry `--epoch`"): each command
  refuses a wrong use (exit 2). Only "exit 3: stop at once" stays, as a never;
- the step order that `next --epoch` gives (child 12).

The content. The Driver words it, within budget:

- **Intro.** You steer one batch for the Chief of Staff, until it is paused. The CLI holds the
  limits, words the asks and refuses what is unsafe. You hold the judgement. In direct mode the
  Chief of Staff steers with this card (`help direct`, child 22).
- **Goal.** Every CR of the batch merged or cancelled, with the fewest questions to the user that
  still leave every decision that is theirs to them.
- **Start.**
  - Set the session title your prompt gives.
  - `git rev-parse --git-dir --git-common-dir`. If the two differ, take no CR, claim no epoch,
    send `$CHANTIER asks "blocked <batch> this session is in a worktree (<path>); start the
    Foreman on the main checkout"`, and stop. See open question 1.
  - `foreman set <session id> --epoch <n>`, then `foreman transcript <uuid> --epoch <n>`. A
    refusal or an empty variable is a stop.
  - Rules and `status`, then `[foreman→chief-of-staff] ready <batch>`.
  - A batch starts from its state alone, never from what you remember of an earlier one.
  - After a compaction, reread your brief, and in a stack batch the topic its `shape:` line names.
- **You own.**
  - Starting Drivers: from the prompt `take`, `take stack` or `order qa` prints, copied whole,
    with the agent and model `playbook --batch` names, then `agents set`. Use every free slot.
  - The orders, each the user's word: their hands-on part, then `order done`.
  - The asks: run `judge <cr>`, send its line unchanged, and add at most one sentence of your own.
    A `no ask:` line means none goes.
  - The heartbeat and your watcher, with `next --epoch <n>` at each wake. `next` advises; a
    refusal is the rule.
  - The retro (`retro draft --epoch <n>`), then `final`.
- **Nevers.** Seven, above the target of five, because F5 puts each protecting rule here or in a
  refusal:
  1. You merge only under the release grant: a fix, or the release once `release go` says `go`.
     An approval never covers it. You record `order merged` only for a merge the forge shows.
  2. You never drop or invent a gap. A gap the PR body lacks, a `no long gate` or a waiver that does
     not hold, or a local run owed and not passed, goes back with `take <cr> --note "<why>"`, with
     no ask. An absent gate never means success (`help long-gate`).
  3. You never code, review, commit, rebase, push, edit a PR or create a worktree. The only git you
     run:
     - the fast-forward of the main checkout after a merge you handle;
     - removing a kept merged CR's worktree and branch once its Driver has ended;
     - the route push of a Driver's refused push of its own `chantier/*` branch, after the check
       (`help refused-push`);
     - closing a dropped CR's PR, or turning it to draft, as its drop order says.
  4. You never commit, pull or push the planning surface: its writer does.
  5. Your chat obeys only "stop" and "hold" (no new Driver; the batch still runs). Anything else
     gets "I run batch <batch> for chantier. Please give orders to the Chief of Staff." A host's
     event about a PR is not an order.
  6. No `take --reclaim` of a live lease without the user's word. You never remove the worktree of
     a trashed CR, or of a CR moved to the backlog or `3-ready`.
  7. Exit 3 from any command means another Foreman owns the batch: stop at once.
- **Messages.**
  - `anomaly` and `blocked` from `msg steering` wake you. Read the notes with `inbox --epoch <n>` at
    your next wake.
  - Work for a CR handed back reaches a Driver only through `take <cr> --note` (`help take-back`).
  - A brief states a past fact only with its source.
  - Who talks to whom: `routing.md` (child 23).
- **End.**
  - At the last CR the CLI pauses the batch. Write the retro, then send `final`, then stay idle: no
    Driver, worker or tool call of yours runs.
  - `not paused`: finish what it names, then `pause --epoch <n>` (`help retro`).
- **Reply format.** The lines the Chief of Staff and the CLI read, byte-for-byte as today:
  - `[foreman→chief-of-staff] ready <batch>`;
  - `[foreman→chief-of-staff] final <STATUS.md path>`;
  - `pong <first line of status>`.

  The rarer lines (`chain`, `unconfirmed`, `switched to direct mode`, `merged`, `release`,
  `parked`, `push`, `pushed`, `rebase`) are each kept byte-for-byte in the topic that triggers
  them. A CR is named by its number and slug.
- **Rare cases.** One line listing the topic names of section 3, with each trigger, or the single
  line "`$CHANTIER help --for foreman` lists them" if the full list does not fit the budget.

### 3. The topics

Each topic is one file `cards-next/topics/<name>.md`, at most 1,500 bytes, with one row in
`cards-next/topics.json` in child 7's format:
- readings relative to `cards-next/`;
- `roles: ["foreman", "chief-of-staff"]`, unless the table says otherwise;
- `trigger`: the situation, or the start of the CLI line that names the topic, in backticks.

**Names.** Every Foreman topic name in child 7's table stays, so that `help --for foreman` and every
CLI line that names one still resolves after the swap: `merge` (the `handed back:` line),
`stack-merge` (`restack owed:`), `stack`, `hold`, `lost-driver`, `conflict-check`, `release`,
`retro`, `sync`, `lease` and `refused-push`. A source too big for 1,500 bytes is split into new
names, and the old name stays as the row whose `readings` list the parts (child 20's rule). The
Driver may merge or split topics within the budgets, and records the final list in the PR.

| Topic | Source today | Holds |
| --- | --- | --- |
| `merge` | `foreman-merge.md`, "An order merged, by mode" | the handed-back ask path, `order merged` by mode, the `merged` line |
| `take-back` | `foreman-merge.md`, "A CR taken back from ready"; `foreman.md:116-139` | work reaches a Driver only by `take --note`; a plain `status` before a work note; `ready`/`blocked` against `working`; `blocked` with waits and `wait clear` |
| `main-checkout` | `foreman-merge.md`, "The main checkout after a merge" | the fast-forward, from the clone with a planning surface; ties to `sync` |
| `sync` | child 7's row (`sync-checkout.md`) | kept as child 7 set it, or pointed at `main-checkout` when child 23 rewrites `sync-checkout.md` |
| `merge-under-grant` | `foreman-merge.md`, "Merging on GitHub"; `foreman.md:139-146` | the fix and release merge under the grant, after `release go`, then `order merged`, then the fast-forward |
| `long-gate` | `foreman.md:75-117` | the `--no-gate` check against the rules; exemption by changed files; a pipeline job as the long gate; rules silent (`question … no long gate written down`); waivers checked against the order (`order waive`); `gate <cr> --first` |
| `local-gate` | `foreman.md:89-128` | the local run: the stack's top, a parallel or series CR that owes it, `deliver by <time>`, `judge --local-gate` |
| `orders` | `foreman.md:155-163` | orders pending and applied; `order done`; the rounds exception; `cancel` to the recorded destination; an `evidence:` order note; a cancelled dependency |
| `drop` | `foreman.md:170-178` | close the PR (`close its PR`) or turn it to draft (`turn its PR to draft`), no comment, no `--delete-branch` |
| `cleanup` | `foreman.md:178-184` | `kept:` and `not removed:` lines; `git worktree remove`, `git branch -D` once the Driver has ended |
| `chain` | `foreman.md`, means, chaining a queued CR | when chaining costs less than rebasing; the `chain` line |
| `qa-order` | `foreman.md`, means, `order qa` | the order's slot and folder, starting the QA driver |
| `escalation` | `foreman.md`, means, Escalation; `concepts.md#Escalation` | the two routes, blocked twice, `rounds:` |
| `lost-driver` | `foreman-lost-driver.md` (11,440, split) | a Driver lost, silent, ended with no hand-back, stopped from outside or waking; a new epoch; `blocked context:` and `context: closing:`; the `ping` and `record` lines |
| `hold` | `foreman-hold.md`, "A held CR" | `order hold`, `order unhold`, the `stop` line |
| `park` | `foreman-hold.md`, "Parking a CR on an outside wait" | park at once; the `parked` line |
| `mode-switch` | `foreman-hold.md`, "A mode switch" | an `order mode` switch |
| `conflict-check` | `foreman-conflict.md` | the early check in a parallel batch, now by `chantier conflicts <cr> --epoch <n>` (child 15). The Foreman's own `git merge-tree` is gone |
| `release` | `foreman-release.md` | a release CR in the batch; it waits while a CR is held or parked |
| `retro` | `foreman-pause.md`; `foreman.md:20-48` | the CLI's pause; `not paused`; the retro section and its tags (`retro draft`); idle after `final`; a paused batch with no CR; an order that adds work |
| `wakes` | `foreman.md`, means: heartbeat, watcher, `forge saw`, `checks red`, ending the heartbeat, short turns | what wakes you, what to do on each line, the `board:` and `pull path` lines left to the Chief of Staff |
| `handover` | `foreman.md:357-369` | a seat hand-over (`seat`), the switch to direct mode and its `switched` line |
| `writer-off` | `foreman.md`, means, the `writer:` line | a writer stopped or failing: tell the Chief of Staff, never commit the surface |
| `stack` | `foreman-stack.md`, preamble and "The stack's asks" | the stack's shape and asks; a CR's readiness goes through the stack; `--outside-stack` only with an order carrying the user's word |
| `stack-grows` | `foreman-stack.md`, "The stack grows" | a CR joining the stack |
| `stack-run` | `foreman-stack.md`, "The stack driver" | starting and steering the stack driver; the `[foreman→stack] note` line |
| `stack-checks` | `foreman-stack.md`, "The five checks" | the five checks read back from the stack driver's hand-back |
| `stack-merge` | `foreman-stack.md`, "After a merge" | the restack owed after a merge |
| `refused-push` (shared) | child 20's row; add `topics/refused-push-steering.md` from `foreman-refused.md`, "A Driver's refused force push" | add roles `foreman`, `chief-of-staff`. The check (the branch matches `chantier/*`, is not the default branch, matches `handoff`'s branch), the judgement, the route form `git push --force-with-lease=<branch>:<expected> …`, one command per branch, the `push` and `pushed` lines, the ladder up to the Chief of Staff (answer 8) |
| `refused-rebase` | `foreman-refused.md`, "A Driver's refused rebase" | the same ladder for a rebase, the `rebase` line. It may be a second steering reading of `refused-push` if it fits |
| `lease` (shared) | child 20's row; add `topics/lease-steering.md` | add roles `foreman`, `chief-of-staff`: a stale lease (`next`'s item), `take --reclaim` only on the user's word |

**`review_by`.** Set to the next minor version after the base's version in
`.claude-plugin/plugin.json` (`"0.16.0"` if the base is still 0.15.x, child 19's rule). It goes on
every topic that only holds rare incident rules with no CLI trigger. Expected:
`writer-off`, `mode-switch`, `handover`, and the parts of `lost-driver` about a Driver stopped from
outside. The PR lists which rows carry it and why.

**No protecting rule in a topic alone (F5).** A topic may repeat the command form of a never, but
never the never itself. When the Driver is unsure whether a rule protects the user or the
repository, it treats it as protecting and keeps it in the card (child 19's rule).

### 4. "The user's boundaries", split rule by rule (F5)

Each sentence group of `foreman.md:59-184` is given one home. "Protecting" means the rule protects
the user or the repository. A protecting rule's home is the floor, the card or a refusal. A topic
may only add the steps around it.

| # | Rule today | Protecting | Home |
| --- | --- | --- | --- |
| B1a | Never merge without the user's word; the readiness words `ready-to-merge`, `pr-in-draft`, `ready-locally`; a draft is never called mergeable | yes | floor 1; `judge` words it (child 14, `ready_word`); card never 1 |
| B1b | An ask's icon is the CR's state at the ask | no | `judge` carries no icon (child 14): the rule disappears |
| B1c | A stack CR's readiness reaches the user through the stack | yes | refusal: `check_shape` / `shape_refusal` (`src/rails_release.py`) refuses a per-CR ready ask in a stack that is not alone; `judge` prints `no ask:` with the stack's pairs; steps in `stack` |
| B1d | A draft's text and a `gaps: …` tail stay in the ask as the Driver wrote them | yes | `judge` copies them verbatim (child 14); card never 2 |
| B1e | Relay a note that an image showing the username or home folder was replaced, or a screenshot not uploaded | yes | floor 8; `judge` copies the hand-back's gaps; the card's "send its line unchanged". If `judge` does not carry such a note, it goes in Known gaps for child 25 |
| B1f | Invent no gap, drop none; a gap the body lacks is a take-back with no ask | yes | card never 2; the steps in `take-back` |
| B1g | An order note `evidence: <path>` becomes `take <cr> --note "evidence: <path>"` | no | `orders` |
| B1h | The `--no-gate` check against the rules (exemption, changed files, pipeline job green at head) | yes | card never 2; the steps in `long-gate` |
| B1i | The stack's top handed back `--no-gate` while the rules ask a local run goes back | yes | card never 2; `local-gate` |
| B1j | A parallel or series CR owing the local run goes back when not passed | yes | card never 2; `local-gate`; `judge --local-gate` adds the clause |
| B1k | `deliver by <time>`: the ask goes with `not run` or `failed` | no | `local-gate`; `judge --local-gate` |
| B1l | Rules declaring a long gate that covers the CR: take back | yes | card never 2; `long-gate` |
| B1m | Rules silent on a long gate: `question … no long gate written down`; an absent gate never means success | yes | card never 2 (the last clause verbatim); `long-gate` |
| B1n | A waiver holds only with the recorded order; a waiver does not waive the local run unless it names the gate | yes | card never 2; `long-gate` and `local-gate` |
| B1o | A release PR is merged only under the grant, after `release go` says `go`; an approval never covers it | yes | floor 6; card never 1; refusal `release go` (`src/rails_release.py`); steps in `merge-under-grant` |
| B1p | A fix is merged only under the grant, with the local run passed when owed, then `order merged`, then the fast-forward | yes | card never 1; refusal `check_granted_fix` (no grant, cap on fixes); steps in `merge-under-grant` and `main-checkout` |
| B2 | The batch's limits are the CLI's; a refusal is a fact; the slots stay as opened unless `order slots` | yes | refusals `check_slot`, `check_budget`, `check_round` (`src/rails.py`); floor 9 |
| B2b | A spent budget, a round limit, a question, an approval, an infrastructure failure: one ask, once | no | `judge` and `next` (child 12's `due:` items); `escalation` |
| B3 | A refusal not understood: `access <cr> --epoch <n>` | no | the refusals name the next command (child 3, M9); the card says nothing |
| B4 | The rounds exception | no | `orders` |
| B5a | Orders are the user's word; `pause` waits for them all | yes | refusal: `pause` waits for orders not done; card "You own" |
| B5b | `cancel` moves to the recorded destination; you never choose one; a refused `cancel` goes up as an ask | yes | refusal: `cancel <cr>: no destination recorded; …` (`src/commands/release.py:137`); `orders` |
| B5c | Work on a CR handed back reaches a Driver only through `take --note`; a plain `status` first | yes (a message to a Driver that handed back can be lost) | card "Messages"; `take-back` |
| B5d | Blocked with typed waits: `wait clear`, then take back | no | `take-back`; `next` names the wait |
| B6 | The chat obeys only "stop", "hold" and the user's line allowing a refused action | yes | card never 5, with "stop" and "hold" only (child scope). The third case is dropped: a refused command goes to the Chief of Staff (answer 8) |
| B7a | Never code, review, commit, rebase, push, edit a PR, create a worktree | yes | card never 3 |
| B7b | Close or draft a dropped CR's PR | yes (the named exception) | card never 3 lists it; steps in `drop` |
| B7c | Kept worktrees: remove once the Driver has ended; a trashed or moved CR's worktree stays | yes | card never 6 (no removal of a trashed or moved CR's worktree); steps in `cleanup` |
| B7d | The fast-forward is the only move of the main checkout | yes | card never 3; steps in `main-checkout` |
| B7e | The early conflict check by `git merge-tree` only | yes (it moves no ref) | the git leaves the Foreman: `chantier conflicts` runs it (child 15); `conflict-check` |
| B7f | The push of a Driver's refused force push, and the rebase | yes | card never 3 names it; the check in `refused-push` (steering reading) |

Outside "The user's boundaries", these protecting rules of `foreman.md` also stay in the card:
the worktree check at the start, the epoch claim, `--reclaim` only on the user's word, never
commit the planning surface, and exit 3.

### 5. The rest of `foreman.md` and the pieces

The inventory (section 6) has a row per sentence. At the section level:

| Source | Home |
| --- | --- |
| `foreman.md:1-18` (start, compaction) | card "Start"; brief facts; host rows |
| `foreman.md:20-48` (goal, pause, retro, `final`) | card "Goal" and "End"; `retro` (the tags and the line form; `retro draft` gives the frame) |
| `foreman.md:50-57` (orders that add work, a batch born paused, an `add` CR as the go) | `retro` and `orders`; `next` gives the next CR |
| `foreman.md:186-202` (the moments) | gone: each moment is now a topic named by its trigger |
| `foreman.md:204-393` (your means) | card "You own" (`take`, the asks, the heartbeat); topics `wakes`, `chain`, `qa-order`, `escalation`, `handover`, `writer-off`; `--help` of each command |
| the `--epoch` list | refusals (exit 2), with exit 3 in the card |
| "Keep each turn short …", background tasks | host rows `end-turn-background`, `stop-own-background-task`; `wakes` |
| the eight `foreman-*.md` pieces | the topics of section 3, by section |
| GitLab forms marked "unproved" today (`glab ci status`, `glab mr update --draft`) | kept as the command form in the topic, with the one word "unproved" (F17); the trial history goes to no card (M3) |
| "the Copilot host's path is unproved" | the host rows (child 8) say it per host; not in a topic |

### 6. The inventory (seed of child 25)

Child 19's format, at `<CR folder>/evidence/cards-inventory-foreman.md`, in the planning folder,
linked from the PR:
- **Sources:** `references/foreman.md` and the eight pieces `foreman-stack.md`, `foreman-merge.md`,
  `foreman-hold.md`, `foreman-lost-driver.md`, `foreman-conflict.md`, `foreman-release.md`,
  `foreman-refused.md`, `foreman-pause.md`, at this child's base. `chief-of-staff-direct.md` and
  `chief-of-staff-steering.md` are child 22's.
- **One row per rule sentence**, with child 19's columns: `id` (`FM-nnn`, a draft id), `role`,
  `trigger`, `behaviour`, `source` (`file:line`), `kind` (a to f), `new home`, `check`.
- The table of section 4 is copied in as the B rows, with their final homes.
- `check` names a quiz case where one exists, or "child 25" where a case is needed. The Driver
  marks these candidates for child 25: the chat obeys only stop and hold; a note does not wake;
  `judge` then send, no merge; the `--no-gate` check; a release not merged without the grant; a
  refused push of a branch that is not `chantier/*`; a session in a worktree; `next` against a
  refusal.
- **Two lists at the end:** every protecting row with its home (a card, the floor or a refusal),
  and every `inferable` row (none of them protecting).

### 7. The stack batch's line, handed to child 24

The program says a stack batch adds one line through `brief`. This child may not edit the CLI. It
fixes the line's text, and child 24 makes `brief foreman` (and `status --refresh`) print it:

```
shape: stack: read `$CHANTIER help stack` now and after each compaction
```

Child 24 must change `src/stack_shape.py`'s `shape_line()` anyway, because it prints
`rules: {skill_dir}/references/foreman-stack.md (reread after a compaction)`, a path the swap
removes (F18). The PR's Internal references name this hand-over, together with the tests that read
the old Foreman cards and that child 24 converts: `test_came_back.py`, `test_stack_shape.py`,
`test_reload_rules.py`, `test_role_cards_split.py`, `test_startup_manifest.py`,
`test_stack_chain_cards.py`, `test_rebase_rules.py`, `test_release_tag.py` and `moved_rules.tsv`.

### 8. Kept unloaded

As child 19, section 5: no file outside `skills/chantier/cards-next/` names `cards-next/` as a
path to read. No change to `roles.yaml`, the wrappers, `src/`, `hooks/`, `references/`,
`startup-manifest.json`, any test or any version. `help` reads only `references/topics.json` until
child 24.

## Out of scope (must not)

- Any edit to `references/`, `src/`, `hooks/`, `types/`, the wrappers, a `SKILL.md`,
  `roles.yaml`, `startup-manifest.json`, a test, AGENTS.md or a version.
- The CLI change that prints the stack line (child 24), and any other CLI change.
- The Chief of Staff's card, its `direct` topic and its side of the refused-push route (child 22).
- `concepts.md`, `routing.md`, the templates, the final `topics.json` and the final `floor.md`
  (child 23). This card links to them by their target names.
- New quiz cases or any change under `evals/` (child 25).
- Removing an old file (child 24).
- Changing what the Foreman is responsible for (answer 1).
- Raising a budget (Q4).

## Acceptance evidence

Each item is in the PR, or under `<CR folder>/evidence/`, from the pushed head.

1. **The files.** The PR lists the files added under `skills/chantier/cards-next/`, and quotes
   `git diff --stat <base>..HEAD`, showing changes under that folder only.
2. **Bytes against the budgets.** One row per file: bytes read from git at head, the target,
   "within" or "over by N". The card is at most 4,000 and each topic at most 1,500. Any file over
   its target goes in Known gaps with its size (Q4).
3. **Brief bytes.**
   - The old: `$CHANTIER brief foreman`.
   - The new: `$CHANTIER brief foreman --cards <worktree>/skills/chantier/cards-next`, on each host
     that child 10's `brief` selects.
   - Both exit 0. The table sets them beside the old start reading: 91 KB declared and 144 KB
     measured.
4. **Quiz under F4.** `just quiz foreman --cards skills/chantier/cards-next --against <child 6's
   baseline for foreman> --model <the model child 6 names for the session roles>`.
   - The plan line is printed first, under the default `--max-usd 10`.
   - Pass: no case scores 0 of 3 that the old cards passed.
   - A failing case brings its rule back into the card (within budget, else Known gaps), and the
     case runs again.
   - If the Driver cannot start the headless host CLI (unproved, child 6), it hands back with the
     files written and the command, and the Chief of Staff runs it. Until then, a Known gap names
     it.
5. **Links.** Every relative link and every `help <topic>` name in the new files resolves inside
   `cards-next/`, or is a forward link to a file a later child writes (`concepts.md`, `routing.md`,
   `pr-template.md`, child 23; topic `direct`, child 22), listed by name. No link points into
   `references/`.
6. **`topics.json`.** It loads with child 7's `load_topics(path)` pointed at it. Every reading
   exists, every role is in `roles.yaml`, every `review_by` matches `X.Y.Z`, and every name of
   child 7's Foreman rows is present.
7. **`just test`: 0 seconds added.** No test is added or changed. The Driver records the
   `just test` time at the base and at head, on the same machine.
8. **The split of "The user's boundaries".** Section 4's table, with the final homes, in the PR
   and in the inventory. Every protecting row's home is the floor, the card or a refusal, quoted
   with its file and line, or the refusal's message start.
9. **The inventory.** Complete as child 19, item 6. The Driver states how it walked the sources.
   No empty `new home`. No protecting row is `inferable`. The reply lines are byte-for-byte as
   today.
10. **Unloaded.** `git grep -n "cards-next" HEAD -- . ':(exclude)skills/chantier/cards-next'` is
    quoted. Each line it shows is a `--cards` argument in usage text or a doc.
11. **Gates.**
    - `just check` at the rebased head, before the first push.
    - The long gate `just scenario (ubuntu-latest)` green at the PR's head (a card change owes it).
    - The local `chantier gate <cr> scenario` only if this CR is the stack's top.
    - `just eval-dry-run` and `just mod` are not owed (no change under `src/`, `evals/kit/`,
      `hooks/` or `types/`).

## Handback

- Handed back validated (F6), with the Known gaps "real run not done (child 28)", every file over
  its target with its size, and "do not merge: merges with children 19 to 28 as one unit, after
  child 28's campaign".
- The typed merge wait `$CHANTIER wait <cr> merge <child 28's PR>` is recorded once child 28's PR
  exists. Until then, the Known gap above says it.
- The PR's Internal references name the hand-over items for child 24 (section 7).

## Risk

- Low on the running product: nothing loads the new files until child 24.
- The cut is deep (about 106 KB of card and pieces down to about 4 KB of card plus topics). A rule
  cut without a home shows only at child 24's swap and child 28's run. The quiz and the inventory
  are the guards before them.
- Seven nevers and the start check may not fit in 4,000 bytes. A card over its target goes in
  Known gaps (Q4); a protecting rule is never moved to a topic to fit.
- The long gate is owed. No AGENTS.md change. No `just mod`.

## AGENTS.md change

None.

## Open questions

1. sc21-Q1 (behaviour, risk): **The worktree override.** Today a Foreman started in a worktree
   stops, unless the user's own words in its chat allow it for that batch. The new chat obeys only
   "stop" and "hold", so the override would go. Should the override be dropped (the user starts the
   Foreman on the main checkout, or the Chief of Staff steers in direct mode), or should it stay as
   a third chat word? Default if unanswered: dropped, and the change is named in the PR for
   child 25.
