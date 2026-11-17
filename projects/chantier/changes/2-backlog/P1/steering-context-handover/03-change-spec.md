# Change Specification: a costed study of handing a long batch's steering to a fresh session

No issue (origin: verbal, from the retro of batch-22, 2026-11-17, kept by the retro critic; record:
`5-archives/batches/batch-22.md`). Priority P1, the user's word. The CR has no `01-intent.md`; its
inputs are `intake/request.md` and `02-answers.md`.

## Goal

The steering session of a long batch carries a large context on every wake, and that context is
paid again at each wake. In batch-22 the Chief of Staff, steering in direct mode, cost $15.99 (26%
of $61.78) over 61 wakes, with a context of 180,750 tokens on average and 266,181 at its peak, and
3 compactions since the batch opened. Other batches show the same: batch-21 187,068 on average
over 9 wakes (56% of its spend), batch-19 133,476 over 16 wakes, and in the Foreman batches
batch-17 189,870 over 312 wakes and batch-18 166,848 over 226 wakes.

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
`hooks/`, `types/`, `scenario/`, `tests/`, `docs/` or the CLI, no branch, no commit there, no PR
(`handover-Q3`).

- **The study**: one Markdown document, in English, at the root of the CR's folder:
  `steering-handover-study.md` (a name that does not start with `report` or `summary`, as
  `concepts.md`, "Starting an agent", asks).
- **Its scripts and data**: in the CR's `experiments/` folder (`concepts.md`, "A CR's folder holds
  its work"), created only once there is a first file, never in the scratchpad, each with a
  numbered name (`01-steering-wakes.py`, `02-...`), each runnable again with the command written at
  its top. A data file a script writes (a CSV or JSON of wakes) goes there too, with a numbered
  name. Raw transcripts are never copied there (they hold the sessions' full text); the scripts
  read them in place, read-only.

### What the study holds

Each part treats the two kinds of steering session (`handover-Q4`): the **Chief of Staff steering a
direct batch** and the **Foreman of a Foreman batch**, side by side where the figures allow, and
says where their procedures differ.

1. **The steering share by batch.** A table, one row per batch from batch-17 to batch-22 that has
   a record (`5-archives/batches/batch-NN.md`, and `batch-NN.json` where the `.md` is missing, as
   for batch-20): the batch, its mode (direct or Foreman), its total cost, the steering row's cost
   and share (the Chief of Staff's in a direct batch, the Foreman's in a Foreman batch), the wakes,
   the context on average and at its peak, the compactions since the batch opened, and, in a
   Foreman batch, the Chief of Staff's own "steering the batch (outside the budget)" line as a
   second row. Each figure names its source (the record's line). A figure the records do not hold
   is written "not recorded", never estimated silently.
2. **Where the steering cost goes.** From the steering sessions' transcripts, where they are still
   on this machine (Claude Code's project transcripts under `~/.claude/projects/`, read-only,
   parsed as `skills/chantier/scripts/cli/src/chantier/costs/transcripts.py` parses them: a wake is
   what `_wakes` counts, the context of a call is the sum of its input, cache-write and cache-read
   tokens): the context at each wake over the batch's life, the cost per wake against the context,
   the share of cache reads in that cost, and where the compactions fell. At least batch-22's
   steering session (direct) and one Foreman batch's Foreman session (batch-17 or batch-18) are
   studied this way; others where their transcript exists. A batch whose transcript is gone says
   so. `chantier cost` does not read a closed batch (`unknown batch`), so the archived records and
   the transcripts are the only sources.
3. **What a fresh session costs to start.** For each kind of steering session, the context a fresh
   one holds after it has read what it must read to take over (item 5), measured on a real fresh
   session's transcript if one exists (a Chief of Staff session's first wakes after `seat take`, a
   Foreman's first wakes after its `foreman set --epoch <n>` claim), else computed from the sizes
   of the files it reads, with the method said. Plus the one-time cost of the hand-over itself: the
   cache write of the new context, the old session's last turn, the messages between the two.
4. **The threshold options, costed.** For each option, replayed on the batches of item 1 and the
   transcripts of item 2, the steering cost it would have given against the cost actually paid,
   with the method and its assumptions stated:
   - a **context** threshold (for example the steering context passing 150,000 tokens at a
     wake; the study tries a few values and says which pays best);
   - a **wakes** threshold (a number of wakes since the session started steering);
   - **none** (today's behaviour, with compaction as the only relief), as the baseline.

   The study says whether the best threshold differs between a direct batch's Chief of Staff and a
   Foreman (their wake rates differ: batch-17's Foreman woke 312 times). Every option includes the
   user's yes (`handover-Q2`): the offer, the wait for the answer, and what happens to the steering
   while it waits (the loop's wakes go on in the old session). In a Foreman batch the study says
   how the offer reaches the user (the Foreman has no conversation with the user: through the Chief
   of Staff, as its other escalations do). It says how a delayed or refused yes changes the saving.
5. **What a fresh session reads to take over.** Built from what exists today, naming each file and
   command, for each kind:
   - **Chief of Staff, direct batch:** the seat (`$CHANTIER seat`, `seat take --over`), the claim
     of the next epoch (`foreman set`, `foreman transcript`, as `chief-of-staff.md`, "Steering a
     batch yourself", says), `$CHANTIER rules` and the rule files it lists, the batch's state
     (`$CHANTIER status`, `asks`, the STATUS files, `brief.md`), the cards the startup manifest
     (`skills/chantier/references/startup-manifest.json`) loads for the role.
   - **Foreman:** the claim of the next epoch (`foreman.md`: `foreman set <session id> --epoch
     <n>`, then `foreman transcript`), its brief, the same rules and batch state, the Foreman's
     cards from the startup manifest, and the restart of every `working` CR that the new epoch
     brings (`foreman.md`, "After an app restart, at a new epoch"; `chief-of-staff.md`,
     "Recovery": the restart path `agents set <cr> - --epoch <n>`, `handoff`, `take <cr> --note
     "resume: <cause>" --epoch <n>`, a new Driver).
   - For both: the decisions not yet written that only the old session's context holds.

   The study compares this with the existing "Handing the seat over" section of
   `chief-of-staff.md` (which waits for every running Driver to finish before the new session
   takes the batch), with the new Foreman after an app restart (`chief-of-staff.md`, "Recovery"),
   and with the reload after compaction (`session-start.md`, section 5), and says what each lacks
   for a hand-over in the middle of a running batch: running Drivers are background children of the
   steering session and die with it (`foreman.md`), Drivers whose `Steering:` line names the old
   session, the heartbeat, the Foreman's `[chief-of-staff→foreman] chief-of-staff <session id>` in
   a Foreman batch, the board that stops when the seat moves.
6. **The risks.** At least: work lost because it lived only in the old session's context; Drivers
   that die with the old session, or whose hand-backs reach it; the restart cost of those Drivers
   (their own fresh context, added to the hand-over's cost); the wait for the user's yes on a long,
   unattended batch; two sessions steering at once; the cost attribution of two steering sessions
   in one batch (the cost code already sums one `main` row per steering session,
   `commands/cost/breakdown.py`, `cost_summary` and `_wakes`); hosts other than Claude Code (the
   Copilot host reference says whether a session can be started or reached; what is unproved stays
   unproved, and so does the new Foreman from a remote client, unproved in
   `hosts/claude-code.md`).
7. **A recommendation.** For each kind of steering session, one option (or none), its threshold
   value, what the later mechanism CR would change (cards, CLI command or message, the board if
   any), and the expected saving per long batch with its uncertainty. The recommendation offers the
   hand-over on the user's yes (`handover-Q2`). It is a proposal for the later CR, not a decision.

## Out of scope

- Any mechanism: no threshold check, no offer message, no change to the seat, the heartbeat,
  `status`, the cost code, a card or an agent file. That is the later batch's CR.
- Any change in the chantier repository, and any PR (`handover-Q3`).
- An automatic hand-over without the user's yes (`handover-Q2`).
- Reducing the steering context by other means (shorter cards, fewer wakes, a different compaction
  window), except as a comparison line in the study if the figures show it plainly.
- The Drivers' own context (Driver compaction is covered by `driver.md`), except the restart cost a
  hand-over brings them (item 6).

## Evidence

- `steering-handover-study.md` exists at the root of the CR's folder and holds the seven parts
  above, each treating the Chief of Staff in direct mode and the Foreman, each with its figures and
  their sources; every figure from a record matches the record's line.
- The scripts that produced the figures are in the CR's `experiments/`, each runnable again with
  the command written at its top, and running one again gives the figures the study quotes.
- `git -C <the chantier checkout> status` shows nothing from this CR: nothing changes in the
  repository, so no `just check`, no `just scenario` and no `just mod` is needed (`AGENTS.md`).

## Open questions

None. The Chief of Staff settled the last one (2026-11-17): the CR does not enter a batch (it has no
PR, and `handback ready` needs one). A Chief of Staff study subagent writes the study into this CR's
folder (`concepts.md`, "Starting an agent"), alongside the batch. The folder stays in the backlog
until the user has read the study; the user then says whether it is archived or becomes the input of
a later CR for the mechanism.
