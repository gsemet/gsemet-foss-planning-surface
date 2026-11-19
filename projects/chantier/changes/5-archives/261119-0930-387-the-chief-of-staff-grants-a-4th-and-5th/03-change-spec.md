# Change Specification: the Chief of Staff grants a 4th and 5th round when the batch caused the red

## Goal

In the user's words (2026-11-19): "tu as le droit dans ces cas-là de donner un 4e et un 5e tour,
il faut que tu l'encodes." When a CR's rounds ran out on a red that the batch itself caused (a
restack, a rebase onto another CR's branch, a CR merged or moved below it), not on the CR's own
work failing to converge, the Chief of Staff grants the next round itself, up to two, and says so
to the user; the batch no longer waits on the user for a trivial fix. Every other grant of rounds
stays the user's word.

The case behind it: batch-28's CR-383 used its 3 rounds; after the Chief of Staff's restack (A-19)
moved CR-375 under it, `just scenario` went red on two surface-board checks that still expected
the watcher's old last line. The Chief of Staff's `order rounds CR-383 --note 4` was held by the
Foreman, because the cards say the round limit is the user's.

## The rule (the rounds exception)

- **When.** A CR handed back `blocked rounds:` whose last round failed on a red the batch caused:
  the red appeared after an event the CR's own work did not make, namely a restack or rebase of
  the CR onto another CR's branch ordered by the Chief of Staff, the Foreman or a stack driver, or
  a CR merged or moved below it. The Chief of Staff judges it from the hand-back, `log <cr>` and
  the Debugger's `diagnosis.md` when there is one. In doubt, it is the user's word. (02-answers 5)
- **How far.** The cap is read from the batch's own `settings.max_rounds` (the batch record, or the
  project's configuration), never from the CR's limit that `status` shows (`r<k>/<limit>`), which
  rises with each grant. Each exception grant sets the CR's limit to its current limit + 1, one
  round at a time and each on its own cause, never above `max_rounds` + 2. With the default 3: the
  4th round, then the 5th. A CR whose limit is already at `max_rounds` + 2 or above gets no
  exception grant. (02-answers 3, 4, 12)
- **The orders.** Two orders, both sent to the Foreman in one message:
  `$CHANTIER order rounds <cr> --note <current limit + 1>` and
  `$CHANTIER order note <cr> --note "rounds exception: <the event>; <the failing check>"`.
  The note carries the reason: `order rounds` takes a number only. (02-answers 1)
- **The user.** Told in the same message that reports the blocked CR, with no wait for a word:
  `CR-<n>: round <k> granted under the rounds exception: <cause>`. The user may still drop the CR
  or set another limit with their own `order rounds`. (02-answers 6)
- **The Foreman.** It takes every `order rounds`, as today ("Orders are the user's word"); there is
  no hold rule and no check of the cap: the Chief of Staff alone answers for using the exception
  rightly. The `rounds exception:` note changes only the take: with the note on the CR, the next
  Driver is taken with `take <cr> --note "rounds exception: <cause>"` and no escalation (the Coder
  stays on the batch's model); without it, `escalate: rounds` as today. The Foreman reads the note
  in `status`'s order list (`O-<k> note <cr> rounds exception: ...`) or, in full, in the CR's notes
  (`handoff <cr>`, `log <cr>`), and marks the note's order done only after that `take`.
  (02-answers 7, 11, 14)
- **Blocked twice.** A `blocked rounds:` hand-back covered by the rounds exception does not count
  toward "blocked twice", and a CR that already holds an `escalated:` note can still get the
  exception. (02-answers 10)
- **Everything else is unchanged.** Any other `blocked rounds:` hand-back, and any round past
  `max_rounds` + 2, is the user's word as today.
- **Direct mode.** The Chief of Staff applies the same rule and the same take itself.

## What changes, file by file

Under `C:/Users/gaeta/Projets/chantier/`. Keep each edit short; use the name "the rounds
exception" everywhere so the places read as one rule.

### `skills/chantier/references/chief-of-staff.md`

1. The steering code block (around line 967): the comment of
   `$CHANTIER order rounds CR-102 --note 5      # on the user's word` becomes
   `# on the user's word, or under the rounds exception (below)`.
2. After the steering paragraphs (next to "A Driver's question", around line 987), a short
   paragraph **"The rounds exception"** stating the rule above: when; the cap from the batch's
   `settings.max_rounds`, never the CR's shown limit, + 1 per grant, never above `max_rounds` + 2;
   the two orders sent together; the line to the user in the same message; the Foreman's take with
   `rounds exception:` and no escalation; that you alone answer for it; everything else the user's.
3. Table row G (around line 1486), column "What the user can do now": append "A red the batch
   caused (a restack, a rebase onto another CR, a CR merged or moved below) is the rounds
   exception: you grant the next round yourself, up to the batch's `max_rounds` + 2, and say so
   (Steering)." The other columns stay; the quoted CLI message stays as the CLI prints it.
4. "Steering a batch yourself", bullet **Escalation** (around line 1500): in direct mode you apply
   the rounds exception yourself; its take carries `rounds exception:` and does not escalate.

### `skills/chantier/references/concepts.md`

1. "Slots, budget, rounds" (around lines 300-301): "three per CR unless the user grants more"
   becomes "three per CR unless the user grants more, or the Chief of Staff under the rounds
   exception ([chief-of-staff](chief-of-staff.md), Steering)".
2. The escalation table, first row (around line 606), middle column: "the round limit stays the
   user's (`order rounds`): escalation never grants a round" becomes "the round limit stays the
   user's (`order rounds`), except the rounds exception (the Chief of Staff grants up to two more
   when the batch caused the red): escalation never grants a round". Third column: after "once the
   user grants more rounds", add "(a grant whose CR holds a `rounds exception:` note is taken with
   that note and does not escalate)".
3. The "blocked twice" row (around line 607), first column: after the list of what counts, add "a
   `rounds:` hand-back covered by the rounds exception never counts".

### `skills/chantier/references/foreman.md`

1. "Orders are the user's word" (around line 164) stays: every `order rounds` is taken. Next to the
   take-back text there, one sentence: after an `order rounds`, when the CR holds a note starting
   `rounds exception:` (in `status`'s order list, or in full in `handoff <cr>` / `log <cr>`), take
   it with `take <cr> --note "rounds exception: <cause>"`, with no escalation, and mark that note's
   order done only after the `take`; without such a note, `escalate: rounds` as today.
2. The Escalation bullet of Your means (around lines 227-234): after "the user's grant of more
   rounds after `blocked rounds:` (`escalate: rounds`)", add "(not a grant under the rounds
   exception, which keeps the batch's model)"; and in the blocked-twice route, "a `rounds:`
   hand-back covered by the rounds exception does not count, and a CR with an `escalated:` note can
   still get the exception".

### `evals/SCORECARD.md`

Row C4: "the batch's or the one the user granted" becomes "the batch's, the one the user granted,
or the one the Chief of Staff granted under the rounds exception".

### Not changed

- The CLI: no refusal is added and `order rounds` keeps its whole-number note
  (`skills/chantier/scripts/cli/src/chantier/commands/orders_apply.py`). The CLI knows no role and
  cannot tell the Chief of Staff's order from the user's; a cap at 5 would refuse the user's own
  larger grants. The rail's message in `rails.py` ("round limit <n> reached; hand back blocked,
  only the user grants more (`order rounds`)") stays: the Driver who reads it still hands back
  blocked. (02-answers 2)
- The agent bodies (`agents/`, `com.github.copilot/agents/`) and `docs/`: none carries the
  round-limit wording. `driver.md`: a Driver still hands back `blocked rounds:` and works the round
  the take gives it. (02-answers 9)

## Out of scope

- Any CLI change (a reason field on `order rounds`, a cap, a new order kind).
- Changing who grants rounds in any other case, or the default `max_rounds`.
- The cost or board display of rounds.

## Evidence

- `just check` passes in the worktree (no CLI or eval-kit change: no `just eval-dry-run` owed).
- The pipeline's `just scenario (ubuntu-latest)` job is green at the PR's head (a change to the
  cards owes it, AGENTS.md).
- A read of the shipped files at the head shows: "rounds exception" in `chief-of-staff.md`,
  `concepts.md`, `foreman.md` and `evals/SCORECARD.md`; the cap stated the same way (the batch's
  `settings.max_rounds`, + 1 per grant, never above `max_rounds` + 2); `order note <cr> --note
  "rounds exception: ..."` named in `chief-of-staff.md`, and the take with that note and no
  escalation in `foreman.md`; no hold rule for the Foreman; the blocked-twice exclusion in both
  `concepts.md` and `foreman.md`. A search for `unless the user grants more`, `stays the user's`,
  `the one the user granted`, and `on the user's word` beside `order rounds` (concepts.md ~301 and
  ~606, chief-of-staff.md ~967 and row G, SCORECARD C4) finds none left without the exception.
- No new test: the change adds no refusal; the tests check refusals and structure.

No host or default matrix: the rule reads the batch's `max_rounds` the same way on both hosts and
with a shipped or configured value.

## Open questions

None: points 1-9 were settled by the spec-writer, 10-14 by the Chief of Staff (`02-answers.md`);
point 11 replaces point 8.
