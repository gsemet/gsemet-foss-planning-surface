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
**a study only** (`handover-Q1`): no behaviour, no card, no CLI change. The mechanism, if the study
recommends one, comes in a later batch as its own CR.

## Decisions carried from `02-answers.md`

- `handover-Q1` (2026-11-17): a costed study, not the threshold mechanism. Its contents: the
  steering share by batch, the threshold options (context, wakes, or none), what a fresh session
  reads to take over, the risks, and a recommendation. The mechanism comes in a later batch.
- `handover-Q2` (2026-11-17): when the mechanism comes, the steering session **offers** the
  hand-over and waits for the user's answer; it never hands over on its own. The study takes this
  as given: it does not weigh an automatic hand-over, and every option it costs includes the
  user's yes (and the wait for it) as a step.
- Spec critic: "no, it delivers a study, no behaviour" (no spec critic run is asked for this CR).

## What changes

One new Markdown document, the study, written in English (repository text is in English). Its
place is open question 1 below; nothing else in the repository changes: no file under
`skills/`, `agents/`, `com.github.copilot/agents/`, `hooks/`, `types/`, `scenario/`, `tests/` or
the CLI. Scripts the Driver writes to compute the figures go in the CR's `experiments/` folder
(`concepts.md`, "A CR's folder holds its work"), never in the scratchpad, with a numbered name
(`01-steering-wakes.py`, ...); none is added to the repository.

### What the study holds

1. **The steering share by batch.** A table, one row per batch from batch-17 to batch-22 that has
   a record (`5-archives/batches/batch-NN.md`, and `batch-NN.json` where the `.md` is missing, as
   for batch-20): the batch, its mode and steering (direct or Foreman), its total cost, the
   steering row's cost and share, the wakes, the context on average and at its peak, the
   compactions since the batch opened, and the Chief of Staff's own "steering the batch (outside
   the budget)" line in Foreman batches. Each figure names its source (the record's line). A
   figure the records do not hold is written "not recorded", never estimated silently.
2. **Where the steering cost goes.** From the steering session's transcripts, where they are still
   on this machine (Claude Code's project transcripts under `~/.claude/projects/`, read-only,
   parsed as `skills/chantier/scripts/cli/src/chantier/costs/transcripts.py` parses them: a wake is
   what `_wakes` counts, the context of a call is the sum of its input, cache-write and cache-read
   tokens): the context at each wake over the batch's life, the cost per wake against the context,
   the share of cache reads in that cost, and where the compactions fell. At least batch-22's
   steering session is studied this way; others where their transcript exists. A batch whose
   transcript is gone says so. `chantier cost` does not read a closed batch (`unknown batch`), so
   the archived records and the transcripts are the only sources.
3. **What a fresh session costs to start.** The context a fresh steering session holds after it
   has read what it must read to take over (item 5), measured on a real fresh session's transcript
   if one exists (a session's first wakes after `seat take`, or a Chief of Staff session's start),
   else computed from the sizes of the files it reads, with the method said. Plus the one-time cost
   of the hand-over itself: the cache write of the new context, the old session's last turn, the
   messages between the two.
4. **The threshold options, costed.** For each option, replayed on the batches of item 1 and the
   transcripts of item 2, the steering cost it would have given against the cost actually paid,
   with the method and its assumptions stated:
   - a **context** threshold (for example the steering context passing 150,000 tokens at a
     wake; the study tries a few values and says which pays best);
   - a **wakes** threshold (a number of wakes since the session started steering);
   - **none** (today's behaviour, with compaction as the only relief), as the baseline.

   Every option includes the user's yes (`handover-Q2`): the offer, the wait for the answer, and
   what happens to the steering while it waits (the loop's wakes go on in the old session). The
   study says how a delayed or refused yes changes the saving.
5. **What a fresh session reads to take over.** Built from what exists today, naming each file and
   command: the seat (`$CHANTIER seat`, `seat take --over`), the claim of the next epoch (`foreman
   set`, `foreman transcript`, as `chief-of-staff.md`, "Steering a batch yourself", says), `$CHANTIER
   rules` and the rule files it lists, the batch's state (`$CHANTIER status`, `asks`, the STATUS
   files, `brief.md`), the cards the startup manifest (`skills/chantier/references/startup-manifest.json`)
   loads for the role, and the decisions not yet written that only the old session's context holds.
   The study compares this with the existing "Handing the seat over" section of
   `chief-of-staff.md` (which waits for every running Driver to finish before the new session
   takes the batch) and with the reload after compaction (`session-start.md`, section 5), and says
   what the existing hand-over lacks for a hand-over in the middle of a running batch (running
   Drivers that keep the old session as their `Steering:` line, the heartbeat, the Foreman's
   `[chief-of-staff→foreman] chief-of-staff <session id>` in a Foreman batch, the board that stops
   when the seat moves).
6. **The risks.** At least: work lost because it lived only in the old session's context; Drivers
   whose hand-backs reach the old session; the wait for the user's yes on a long, unattended batch;
   two sessions steering at once; the cost attribution of two steering sessions in one batch (the
   cost code already sums one `main` row per steering session, `commands/cost/breakdown.py`,
   `cost_summary` and `_wakes`); hosts other than Claude Code (the Copilot host reference says
   whether a session can be started or reached; what is unproved stays unproved).
7. **A recommendation.** One option (or none), its threshold value, what the later mechanism CR
   would change (cards, CLI command or message, the board if any), and the expected saving per
   long batch with its uncertainty. The recommendation offers the hand-over on the user's yes
   (`handover-Q2`). It is a proposal for the later CR, not a decision.

## Out of scope

- Any mechanism: no threshold check, no offer message, no change to the seat, the heartbeat,
  `status`, the cost code, a card or an agent file. That is the later batch's CR.
- An automatic hand-over without the user's yes (`handover-Q2`).
- Reducing the steering context by other means (shorter cards, fewer wakes, a different compaction
  window), except as a comparison line in the study if the figures show it plainly.
- The Drivers' own context (Driver compaction is covered by `driver.md`).

## Evidence

- The study exists at its place (open question 1) and holds the seven parts above, each with its
  figures and their sources; every figure from a record matches the record's line.
- The scripts that produced the figures are in the CR's `experiments/`, each runnable again with
  the command written at its top.
- `just check` passes. The change touches neither the CLI, the cards nor the scenario, so per
  `AGENTS.md` it needs no `just scenario` run before its PR; it touches neither `hooks/` nor
  `types/`, so no `just mod`.

## Open questions

1. **Where the study lives.** In the repository, in the CR's PR (for example
   `docs/steering-handover-study.md`), or only in the CR's folder in the planning surface
   (`experiments/01-steering-handover-study.md`), with the CR then delivering no PR? The answers do
   not say.
2. **Which steering sessions the study covers.** Only the Chief of Staff steering in direct mode
   (the retro's figures), or also the Foreman of a Foreman batch (batch-17: 312 wakes, 189,870 on
   average; batch-18: 226 wakes, 166,848 on average), whose hand-over would follow the same
   threshold logic but a different procedure? The request speaks of "a long batch's steering",
   which covers both; the answers do not settle it.
