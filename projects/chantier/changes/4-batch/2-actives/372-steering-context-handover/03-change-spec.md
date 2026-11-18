# Change Specification: a costed study of handing a long batch's steering to a fresh session

No issue (origin: verbal, from the retro of batch-22, 2026-11-17, kept by the retro critic; record:
`5-archives/batches/batch-22.md`). Priority P1, the user's word. The CR has no `01-intent.md`; its
inputs are `intake/request.md` and `02-answers.md`.

Brought up to date on 2026-11-18 with chantier's main at v0.13.0 and after (the forge hub and the
watcher, the switch of a Foreman batch to direct mode, the Driver's closing hand-off, the reload
after a compaction, the cost receipt recorded at a batch's close, CR-367 and CR-368). No decision
of `02-answers.md` changed.

## Goal

The steering session of a long batch carries a large context on every wake, and that context is
paid again at each wake. In batch-22 the Chief of Staff, steering in direct mode, cost $15.99 (26%
of $61.78) over 61 wakes, with a context of 180,750 tokens on average and 266,181 at its peak, and
3 compactions since the batch opened. Other batches show the same: batch-21 187,068 on average
over 9 wakes (56% of its spend), batch-19 133,476 over 16 wakes; in the Foreman batches batch-17
189,870 over 312 wakes, batch-18 166,848 over 226 wakes, batch-23 176,158 over 75 wakes, batch-24
178,467 over 167 wakes, batch-26 212,653 over 28 wakes and batch-27 172,831 over 52 wakes ($12.67,
48% of $26.40). Every peak since batch-22 sits between 261,128 and 266,614 tokens, where the host
compacts.

The user wants to know, with figures, whether handing a long batch's steering to a fresh session
would pay, at what threshold, and what that fresh session must read to take over. This CR delivers
**a study only** (`handover-Q1`): no behaviour, no card, no CLI change, and **no PR**
(`handover-Q3`). The study covers both kinds of steering session: the Chief of Staff steering a
direct batch and the Foreman of a Foreman batch (`handover-Q4`). The mechanism, if the study
recommends one, comes in a later batch as its own CR.

## Decisions carried from `02-answers.md`

- `handover-Q1` (2026-11-17): a costed study, not the threshold mechanism. Its contents: the
  steering share by batch, the threshold options (context, wakes, or none), what a fresh session
  reads to take over, the risks, and a recommendation. The mechanism comes in a later batch.
- `handover-Q2` (2026-11-17): when the mechanism comes, the steering session **offers** the
  hand-over and waits for the user's answer; it never hands over on its own. The study takes this
  as given: it does not weigh an automatic hand-over, and every option it costs includes the
  user's yes (and the wait for it) as a step.
- `handover-Q3` (2026-11-17): the study lives in the CR's folder in the planning surface: the
  study document in the folder itself, its scripts and data in the folder's `experiments/`. The CR
  delivers no PR: nothing changes in the chantier repository.
- `handover-Q4` (2026-11-17): the study covers both the Chief of Staff steering in direct mode and
  the Foreman of a Foreman batch.
- Spec critic: "no, it delivers a study, no behaviour" (no spec critic run is asked for this CR).

## What changes

All of it in the CR's folder in the planning surface
(`projects/chantier/changes/<the CR's current place>/steering-context-handover/`), and nothing
in the chantier repository: no file under `skills/`, `agents/`, `com.github.copilot/agents/`,
`hooks/`, `types/`, `scenario/`, `tests/`, `docs/`, `config/` or the CLI, no branch, no commit
there, no PR (`handover-Q3`).

- **The study**: one Markdown document, in English, at the root of the CR's folder:
  `steering-handover-study.md` (a name that does not start with `report` or `summary`, as
  `concepts.md`, "Starting an agent", asks).
- **Its scripts and data**: in the CR's `experiments/` folder (`concepts.md`, "A CR's folder holds
  its work"), created only once there is a first file, never in the scratchpad, each with a
  numbered name (`01-steering-wakes.py`, `02-...`), each runnable again with the command written at
  its top. A data file a script writes (a CSV or JSON of wakes) goes there too, with a numbered
  name. Raw transcripts are never copied there (they hold the sessions' full text, and personal
  data stays out of a CR's folder); the scripts read them in place, read-only, and the data files
  hold figures only (times, token counts, costs, record ids), no message text.

### The sources

- **The batch records** in `5-archives/batches/`: `batch-NN.md` (the "Cost" section's lines) and
  `batch-NN.json`. From batch-23 on, `batch-NN.json` also holds the `cost_receipt` recorded at the
  close (its `steering` entry: label, dollars, calls, wakes, average context; its `split`; its
  `outside` steering and grill figures); the study reads those and checks they match the `.md`.
  The archived records hold no transcript ids (`foreman_transcripts`, `foreman_claims` and
  `chief_transcripts` live only in a running batch's `4-batch/batch.json`).
- **The transcripts**: Claude Code's project transcripts under `~/.claude/projects/`, read-only,
  in both the chantier repository's folder and the planning surface's folder (sessions have
  steered from the surface since the move to the external planning surface). A steering session's
  transcript is found by the batch's time window and its claim commands (`foreman set ... --epoch
  <n>`, `foreman transcript ...`) in it. They are parsed as
  `skills/chantier/scripts/cli/src/chantier/costs/transcripts.py` parses them: a wake is what its
  `_wakes` counts (a user record that is not only tool results), and the context of a call is the
  sum of its input, 5-minute cache-write, 1-hour cache-write and cache-read tokens (the first four
  usage figures, as `peak_context` and `wake_context` sum them). The figures of a batch are summed
  as `commands/cost/breakdown.py` does (`wake_figures`, `_wakes`, `cost_summary`: one `main` row
  per steering session).
- `$CHANTIER cost` does not read a closed batch (it answers `error: unknown batch batch-22`, exit
  2, checked 2026-11-18): the archived records and the transcripts are the only sources for a
  closed batch.

### What the study holds

Each part treats the two kinds of steering session (`handover-Q4`): the **Chief of Staff steering a
direct batch** and the **Foreman of a Foreman batch**, side by side where the figures allow, and
says where their procedures differ.

1. **The steering share by batch.** A table, one row per batch from batch-17 to the last batch
   closed when the study is written (batch-27 on 2026-11-18) that has a record
   (`5-archives/batches/batch-NN.md`, and `batch-NN.json` where the `.md` is missing, as for
   batch-20, a Copilot direct batch whose record still says `running` and holds no cost): the
   batch, its mode (direct or Foreman, and stack or parallel), its total cost, the steering row's
   cost and share (the Chief of Staff's in a direct batch, the Foreman's in a Foreman batch, as
   the record labels it), the wakes, the context on average and at its peak, the compactions since
   the batch opened, and, in a Foreman batch, the Chief of Staff's own "steering the batch (outside
   the budget)" line as a second row. A batch whose steering row joins two sessions (batch-25:
   "Chief of Staff, steering the batch and Foreman", 14 wakes, $3.98) is shown as recorded, and the
   study says, from its record and transcripts, how its steering moved between the two sessions.
   Each figure names its source (the record's line, or the `cost_receipt` key). A figure the
   records do not hold is written "not recorded", never estimated silently.
2. **Where the steering cost goes.** From the steering sessions' transcripts, where they are still
   on this machine: the context at each wake over the batch's life, the cost per wake against the
   context, the share of cache reads and of cache writes in that cost, the calls made after the
   cache expired (the cost code's rule, `EXPIRY_NOTE` in `breakdown.py`: 5 minutes after a
   5-minute write, 1 hour after a 1-hour one; the host's reference measured a session's writes as
   1-hour and a subagent's as 5-minute, 2026-11-17), and where the compactions fell. It sorts the
   wakes by cause, as far as the transcript tells them: the heartbeat (the batch's steering wake,
   30 minutes by default, `timing:` in `config/chantier.defaults.yml`), a Driver's line or
   hand-back, a leftover background task of an ended Driver (batch-24's retro counts 75 such
   Foreman wakes), the end of the Chief of Staff's watcher (`$CHANTIER watch`, in direct mode), an
   order or the user's turn. At least batch-22's steering session (direct) and one Foreman
   session among batch-17, batch-18, batch-23 and batch-24 are studied this way, plus one batch
   closed after the watcher shipped (batch-26 or later) when its transcript exists; others where
   their transcript exists. A batch whose transcript is gone says so.
3. **What a fresh session costs to start.** For each kind of steering session, the context a fresh
   one holds after it has read what it must read to take over (item 5), measured on real fresh
   sessions' transcripts where they exist: a Foreman's first wakes after its `foreman set --epoch
   <n>` claim (every Foreman batch from batch-23 to batch-27 starts one), the Chief of Staff's first
   wakes after the claim of a switch to direct mode, and a Chief of Staff session's first wakes
   after `seat take`; else computed from the sizes of the files it reads, with the method said.
   Plus the one-time cost of the hand-over itself: the cache write of the new context, the old
   session's last turn, the messages between the two, and the restart of the Drivers it brings
   (item 5).
4. **The threshold options, costed.** For each option, replayed on the batches of item 1 and the
   transcripts of item 2, the steering cost it would have given against the cost actually paid,
   with the method and its assumptions stated:
   - a **context** threshold (for example the steering context passing 150,000 tokens at a
     wake; the study tries a few values and says which pays best, and compares them with the
     Driver's own threshold of 130,000 tokens, `driver.md`, "Your means", and with the host's
     compaction point near 162,000 to 170,000 tokens, `hosts/claude-code.md`, "Compacting");
   - a **wakes** threshold (a number of wakes since the session started steering), with the wakes
     counted as item 2 sorts them, and said whether the count should leave out the wakes no
     steering needed (a leftover task's);
   - **none** (today's behaviour, with compaction and the automatic reload as the only relief),
     as the baseline.

   The study says whether the best threshold differs between a direct batch's Chief of Staff and a
   Foreman (their wake rates differ: batch-17's Foreman woke 312 times, batch-24's 167). Every
   option includes the user's yes (`handover-Q2`): the offer, the wait for the answer, and what
   happens to the steering while it waits (the loop's wakes go on in the old session). In a Foreman
   batch the study says how the offer reaches the user (the Foreman has no conversation with the
   user: through the Chief of Staff, as its other escalations do, an `asks` line). It says how a
   delayed or refused yes changes the saving.
5. **What a fresh session reads to take over.** Built from what exists today at chantier's main,
   naming each file and command, for each kind:
   - **Chief of Staff, direct batch:** the seat (`$CHANTIER seat`, `seat take --over`), the claim
     of the next epoch (`foreman set`, `foreman transcript`, as `chief-of-staff.md`, "Steering a
     batch yourself", says), `$CHANTIER rules` and the rule files it lists, the batch's state
     (`$CHANTIER status`, `asks`, the STATUS files, `brief.md`), the cards the startup manifest
     (`skills/chantier/references/startup-manifest.json`) loads for the role, the heartbeat it
     arms, and the watcher it starts again (`$CHANTIER watch --after <n>`, from the `watch:` line
     of `status`; the user's yes for the watcher holds once per session, `session-start.md`, "The
     watcher", so a fresh session asks it again).
   - **Foreman:** the claim of the next epoch (`foreman.md`: `foreman set <session id> --epoch
     <n>`, then `foreman transcript`), its brief, the same rules and batch state, the Foreman's
     cards from the startup manifest, the heartbeat, and the restart of every `working` CR, the
     recorded stack driver and every open QA order that the new epoch brings (`foreman.md`, "After
     an app restart, at a new epoch" and "The restart path"; `chief-of-staff.md`, "Recovery").
   - For both: the decisions not yet written that only the old session's context holds.

   The study compares this with the procedures that already move steering or context today, and
   says what each lacks for a hand-over in the middle of a running batch:
   - **"Switching to direct mode"** (`chief-of-staff.md`, steps 1 to 9) and **"Switching to
     Foreman mode"**: the closest existing procedure, a steering move with CRs in flight. Its
     pre-check of `chief_transcript`, its ping of the Foreman, its `[chief-of-staff→foreman]
     switch to direct mode` and `switched to direct mode <batch>: stopped …` lines, its check that
     each old Driver ended (`close --batch <batch>` without `--yes`), its claim of the next epoch,
     and its restart of the stopped Drivers by the restart path (`resume: switch to direct
     mode`). The study says which steps a same-kind hand-over (Chief of Staff to Chief of Staff,
     Foreman to Foreman) would reuse as they are, and what the user's yes (`handover-Q2`) adds.
   - **"Handing the seat over"** (`chief-of-staff.md`), which waits for every running Driver to
     finish before the new session takes the batch, and has the old session stop its watcher and
     the new one start its own.
   - **The new Foreman after an app restart** (`chief-of-staff.md`, "Recovery").
   - **The reload after a compaction** (`session-start.md`, section 5, and
     `hosts/claude-code.md`, "Reload after a compaction": the mod's message after every compaction
     of a role session, which makes it call its skill again with `reload`).
   - **The Driver's own context hand-back** (`driver.md`, "Your means": `handback <cr> blocked
     context: …` at 130,000 tokens, and the CR driver's closing hand-off `context: closing:
     VERIFIED at <sha7>; next: …`; `foreman.md`, "A hand-back `blocked context: …`"): the same idea
     one level down, already in use, whose figures (the fresh Driver's start cost against the old
     one's context) the study may quote as a comparison.

   What each lacks, at least: running Drivers are background children of the steering session and
   die with it (`foreman.md`); Drivers whose `Steering:` line names the old session; the heartbeat;
   the Foreman's `[chief-of-staff→foreman] chief-of-staff <session id>` in a Foreman batch; the
   board, which stops when the seat moves; the watcher, which belongs to its session.
6. **The risks.** At least: work lost because it lived only in the old session's context; Drivers
   that die with the old session, or whose hand-backs reach it; the restart cost of those Drivers
   (their own fresh context, added to the hand-over's cost); the wait for the user's yes on a long,
   unattended batch; two sessions steering at once (the epoch makes the CLI refuse the stale one,
   exit 3, but a Driver of the old one may still run); a forge event missed between the old
   watcher's stop and the new one's start (the forge hub keeps the journal, `forge-journal.jsonl`,
   and `watch --after <n>` reads from a sequence number: the study says whether that closes the
   gap); the cost attribution of two steering sessions in one batch (the cost code sums one `main`
   row per steering session, `commands/cost/breakdown.py`, `cost_summary` and `wake_figures`, and
   batch-25's record shows the joined label); hosts other than Claude Code (the Copilot host
   reference says whether a session can be started, reached or stopped; what is unproved stays
   unproved, and so does the new Foreman from a remote client, unproved in
   `hosts/claude-code.md`, and the stop of a session from the phone under Remote Control,
   unproved in `chief-of-staff.md`'s switch).
7. **A recommendation.** For each kind of steering session, one option (or none), its threshold
   value, what the later mechanism CR would change (cards, CLI command or message, the board if
   any; whether it can reuse the switch's steps), and the expected saving per long batch with its
   uncertainty. The recommendation offers the hand-over on the user's yes (`handover-Q2`). It is a
   proposal for the later CR, not a decision.

## Out of scope

- Any mechanism: no threshold check, no offer message, no change to the seat, the heartbeat, the
  watcher, `status`, the cost code, a card or an agent file. That is the later batch's CR.
- Any change in the chantier repository, and any PR (`handover-Q3`).
- An automatic hand-over without the user's yes (`handover-Q2`).
- Reducing the steering context by other means (shorter cards, fewer wakes, a different compaction
  window, a longer steering wake), except as a comparison line in the study if the figures show it
  plainly.
- The Drivers' own context (Driver compaction and the Driver's context hand-back are covered by
  `driver.md`), except the restart cost a hand-over brings them (item 6) and the comparison of
  item 5.

## Evidence

- `steering-handover-study.md` exists at the root of the CR's folder and holds the seven parts
  above, each treating the Chief of Staff in direct mode and the Foreman, each with its figures and
  their sources; every figure from a record matches the record's line (or its `cost_receipt` key).
- The scripts that produced the figures are in the CR's `experiments/`, each runnable again with
  the command written at its top, and running one again gives the figures the study quotes. No
  file there holds a transcript's message text.
- `git -C <the chantier checkout> status` shows nothing from this CR: nothing changes in the
  repository, so no `just check`, no `just scenario`, no `just eval-dry-run` and no `just mod` is
  needed (`AGENTS.md`).

No host and default matrix: the study changes nothing that depends on a host or a configured
value; it reports the host of each batch it reads.

## Open questions

None. The Chief of Staff settled the last one (2026-11-17): the CR does not enter a batch (it has no
PR, and `handback ready` needs one). A Chief of Staff study subagent writes the study into this CR's
folder (`concepts.md`, "Starting an agent"; `chief-of-staff.md`, "Subagents and the demo"). The
folder stays in the backlog until the user has read the study; the user then says whether it is
archived or becomes the input of a later CR for the mechanism.
