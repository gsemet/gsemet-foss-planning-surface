# The steering session reads the rules after its claim

## Goal

In direct mode, the Chief of Staff steering a batch reads the project's rules right after it
claims the batch's epoch, every batch, as a Foreman does at its start: it runs `$CHANTIER rules`
and reads the rule files that command lists. The command is the anchor the eval audit reads
(J14); the files are the substance.

Source: real-direct run 1 (2026-11-12, PR 137, audit J14, finding 6 of
`evals/results/real-direct-2026-11-12-run1.md`): the Chief of Staff ran `$CHANTIER rules` at the
start of its session, before `open`, and not again after its claim, so the audit (which reads the
steering transcript from the claim on) failed J14. The real-foreman run of the same day
(`evals/results/real-foreman-2026-11-12.md`, finding 5) showed the weaker form of the same gap: a
`rules` run with no rule file read, which meets the rail in name only.

## Decisions carried from 02-answers.md

1. **Command and files.** Right after the claim, every batch: run `$CHANTIER rules`, and read again
   the rule files it lists. The command itself runs every time; only the re-read of a file is
   skipped, and only for a file this session has read both since this batch's `open` and since
   its last compaction (a full re-read minutes after a reading done for this batch pays tokens
   for nothing). A reading before this batch's `open` is not this batch's: it never exempts a
   file.
2. **Every batch**, not only a session's first: a session can steer several batches, and the
   project's rules change between them (a merged CR often edits `AGENTS.md`).
3. **The audit is not relaxed**: J14 keeps anchoring on the claim; a `rules` run before the claim
   does not count.
4. **Every claim**, a resumed steering session too: a new session that claims a later epoch of the
   same batch (a resume, a seat hand-over in direct mode) runs the command and reads the files; it
   knows nothing of what the first session read.
5. **The Foreman's card changes only if its wording on reading the rule files is weaker than the
   new line**; the two cards must ask the same thing of a steering session. Checked: it is not
   weaker and, with the skip bounded as in decision 1, it asks the same thing (see "Foreman card"
   below), so `foreman.md` does not change.
6. **No CLI enforcement**: no new refusal (the CLI knows no role; a refusal needs a measured cost,
   per `AGENTS.md`; one audited slip in one run is a card fix).
7. **Nothing new for the user**: one more command and at most a few file reads per batch in the
   steering session. No output, default or habit changes.
8. **Gates**: `just check` and `just scenario` (a change to a card, per `AGENTS.md`).

## What changes

### `skills/chantier/references/chief-of-staff.md`, section "Steering a batch yourself"

In the bullet **"Your epoch."**, right after the claim sentence ("Claim it as a Foreman does:
`$CHANTIER foreman set <your session id> --epoch <n>` (`1` for a new batch), then `$CHANTIER
foreman transcript <your transcript id> --epoch <n>`."), add the rules step, so that it sits in
the claim itself and every place that says "claims ... as in Steering a batch yourself" carries
it. Suggested wording (the Driver may tune the words, not the content):

> Right after each claim, every batch you steer, a resumed or taken-over one too: run
> `$CHANTIER rules` and read the rule files it lists, as a Foreman does at its start. A reading
> before this batch's `open` is not this batch's; skip only the re-read of a file this session
> has read since this batch's `open` and since its last compaction. The command runs every time,
> after the claim, whatever ran before it.

Then the existing text of the bullet ("Carry `--epoch <n>` on exactly these commands...")
continues unchanged. `rules` does not carry `--epoch` (it is not in that list, and stays out of it).

Nothing else in the card changes:

- "The project" ("At the start of each session, `$CHANTIER rules` ...") stays: it is the session's
  start, the new line is the batch's.
- "Handing the seat over" already says the new session of a direct batch "claims the next epoch
  as in Steering a batch yourself"; with the step inside "Your epoch", it covers decision 4 with no
  edit there.

### Foreman card (`skills/chantier/references/foreman.md`): no change

Its opening paragraph already asks the same: at the start of every batch, in a reused session
too, and again after a compaction, "read the cards and the rule files `$CHANTIER rules` lists
again, not only the command's output. An earlier reading is not this batch's."; and its claim
bullet says "Then the brief and the rules" right after `foreman set` / `foreman transcript`. With
the skip bounded to this batch and the last compaction (decision 1), the new line and the
Foreman's card ask the same thing of a steering session, so per decision 5 it stays as it is.

### Agent files, CLI, audit: no change

- `agents/` and `com.github.copilot/agents/`: the contract lives in the card.
- The CLI (`skills/chantier/scripts/cli/`): no refusal, no new output.
- The eval kit (`evals/kit/audit.py`, the J14 check `RULES_COMMAND` read from the claim on) and
  `evals/SCORECARD.md`: unchanged.

## Out of scope

- The audit and J14 (the item `audit-direct-false-fails` does not touch J14 either).
- The Foreman's card (see above).
- The agent files on both hosts.
- A CLI refusal such as `take` refused until `rules` ran.
- The audit's blind spot for `Invoke-Expression "$c rules"` (real-foreman finding 5): another item.

## Evidence

- `just check` passes (Linux, macOS and Windows in CI).
- `just scenario` passes (both forges).
- The diff touches only `skills/chantier/references/chief-of-staff.md`, within the "Your epoch."
  bullet of "Steering a batch yourself"; quote the new sentence in the PR description.
- A read of the two cards side by side, recorded in the CR's `work/` notes: the new line and
  `foreman.md`'s opening paragraph and claim bullet ask the same of a steering session (the
  command after the claim, the listed files read for this batch, an earlier reading not this
  batch's), with no contradiction.
- Done when, in full: the next real-direct eval's audit passes J14 with `rules` run after the
  claim. That run is the user's eval, outside this CR's PR; the PR's evidence is the card and the
  gates above.
