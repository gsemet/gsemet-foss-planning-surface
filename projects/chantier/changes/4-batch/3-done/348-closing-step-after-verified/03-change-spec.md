# Change Specification: a fresh closing step after VERIFIED

## Goal

In batch-24, three CR Drivers (CR-343 at 132k tokens, CR-344 twice) reached the 130,000-token
hand-back limit after the Verifier's `VERIFIED`, while they were still writing the PR description.
Each one needed a fresh Driver to read its state again from the CR's notes. After this change, a
CR Driver that gets `VERIFIED` at the pushed head stops there and hands off. A fresh Driver that
reads only the CR's notes then does the closing work: the PR body, the evidence images, the
description pass, the PR turned ready and `handback ready`.

## Decisions carried from 02-answers.md

- cs-Q1: the hand-off always happens. It is triggered by the first `VERIFIED` that the `verifier`
  at the pushed head records while the closing is still to do. A matrix probe's `VERIFIED` and a
  verdict carried by `ship` do not trigger it.
- cs-Q2: the closing step is a fresh CR Driver started by the existing restart path. No new role.
- cs-Q3: the hand-back is `blocked context: closing: VERIFIED at <sha7>; next: <what is left>`.
  The take-back note is `resume: closing`.
- cs-Q4: the closing Driver reads only the CR's notes (`handoff`, `log`, `pr-body.md`,
  `work/verify.md` and the evidence files that `verify.md` names, plus `pr-template.md` when it
  edits the body). It reads the specification, `investigation.md`, `r<n>.md` and the diff only
  when a step outside the closing comes up.
- cs-Q5: a Driver started with `resume: closing`, or whose `log` already holds a `closing:`
  note, never hands off for the closing again.
- cs-Q6: a closing hand-off does not count toward "driver out of context twice" or "driver ended
  twice". Reports and retros call it "the closing step".
- cs-Q7: the CLI changes only the line that `handback` prints for a `context: closing` reason.
- cs-Q8: the scope is the CR driver only. The context rule, the worker cards and the agent files
  stay as they are.

## What changes

### `skills/chantier/references/driver.md` (the cards hold the contract)

1. **"CR driver", the paragraph of steps (around lines 639-652).** Insert a closing hand-off after
   "then a `verifier` at the pushed head ... (it records its own `verdict`; you run none for it;
   `NOT VERIFIED` is a round)":
   - When that `verifier` replies `VERIFIED`, your prompt's `Note:` is not `resume: closing` and
     `log <cr>` holds no `closing: VERIFIED at` note yet, you stop and hand off. First record one note that holds everything the
     closing needs:
     `$CHANTIER note <cr> "closing: VERIFIED at <sha7>; PR <link>; base <branch>; pr-body.md
     posted at <sha7 or not yet>; evidence: <the files verify.md names>; UNVERIFIED: <claims or
     none>; next: evidence in Deliverables, Test plan boxes, pre-post audit and post, description
     pass, PR ready then `ship <cr> <link>`, `handback ready <link>` with the body's gaps"`. Then run
     `$CHANTIER handback <cr> blocked context: closing: VERIFIED at <sha7>; next: <what is
     left>` and end your run.
   - Before the note, any claim the Verifier could not prove is already marked `UNVERIFIED` or
     narrowed in `pr-body.md`, so the closing Driver does not have to judge it again.
   - Add one sentence: "Besides `context: host asked the hand-back …`, the closing hand-off is the
     only `context:` hand-back that needs no `context:` line at 130,000 or more; it always happens,
     whatever the context size."
2. **"Your means", the Context bullet (lines 124-130).** The sentence "Hand back `blocked
   context:` only when the last `context:` line read 130,000 or more" gets the exception: "...
   or for the closing hand-off of "CR driver" (`context: closing: ...`)". The same bullet's clause
   "a Driver that stops for any other reason names that reason, never `context:`" becomes "...names
   that reason, never `context:` (the closing hand-off of "CR driver" excepted)".
3. **The opening reading rules, the "A Driver started again" bullet (line 48).** Add a sub-bullet
   for `resume: closing`:
   - Run `$CHANTIER handoff <cr>` and `log <cr>`, then read `pr-body.md`, `work/verify.md` and the
     evidence files it names.
   - Read `pr-template.md` before the first body edit.
   - Do not open the specification, `investigation.md`, the `r<n>.md` notes or the diff.
   - Then carry out the "next:" of the closing note, in the same order as the note: the evidence
     in Deliverables and the Test plan boxes (`gh pr edit --body-file`), the pre-post audit and the
     post, the short `verifier` pass on the posted description alone, the PR turned ready when its
     base is the default branch then `ship <cr> <link>`, and `handback ready <link>` with the gaps
     that the body's Known gaps hold.
   - A step outside the closing (a red check, a move, a review item on the code, a `rebase:`
     note) brings back the card's usual rules and reads. A Driver whose `log` holds a `closing:`
     note never hands off for the closing again.
   - Also add one line to the `## Startup core` section (line 1121): a `Note: resume: closing`
     reads only the CR's notes, as the opening reading rules (line 48) list.
4. **"Your end" (around line 508) and line 533-535,** where the `context:` hand-back is listed.
   Name `context: closing: ...` there as the closing hand-off of "CR driver".

### `skills/chantier/references/foreman.md` (direct mode reads the same rules)

5. **The bullet "A hand-back `blocked context: …`" (lines 611-619).**
   - Its opening parenthesis ("the Driver's context reached the threshold, or the host asked its
     hand-back early: its text says which") gains ", or the Driver stopped at its pushed-head
     `VERIFIED` for the closing step (`context: closing: …`)".
   - Add the closing case. A text that starts `context: closing:` goes through the same restart
     path, with the note `resume: closing`: `agents set <cr> - --epoch <n>`, then `take <cr>
     --note "resume: closing" --epoch <n>`, then a new CR Driver, then `agents set <cr> <id>
     --epoch <n>`. No round is counted, no ask is made, and it goes before any queued CR.
   - The counting sentence becomes: "the second-`context:` ask counts only real context ends (no
     `host asked the hand-back` and no `closing:` in the text)".
   - A report or a retro calls a `context: closing:` hand-back "the closing step", never "out of
     context".
6. **"A silent end" (lines 669-672).** "a `context:` hand-back do not" already covers the closing
   hand-off, so the text stays as it is. Check it while editing and leave it.

### The CLI: `skills/chantier/scripts/cli/src/chantier/commands/driver_checks.py`

7. **`handback_blocked`, before the general `context:` branch.** A note whose lowercase form
   starts with `context: closing` returns `[line, f"{cr} verified; the Foreman restarts a fresh
   Driver for the closing step, with no ask to the Chief of Staff"]`. The record does not change
   (`blocked`, `blocked_reason` = the note), and neither do the usage text, the other refusals or
   the eval kit's `HANDBACK_WORDS` (the reason still starts with `context:`).

### Scenario: `scenario/run_scenario.py` (beside the `context:` check, around lines 4239-4258)

8. Add one check, on `two` after the take at lines 4247-4250: `handback two blocked "context:
   closing: VERIFIED at abc1234; next: description pass"`, then `agents set two - --epoch 1`, then
   `take two --note "resume: closing" --epoch 1`. The check expects:
   - the CR is `blocked` with that reason;
   - the output holds "for the closing step";
   - the output holds neither "out of context" nor "asks the Chief of Staff";
   - the take succeeds with the round unchanged.

   Extend the existing card check: `driver.md` holds `resume: closing` and `context: closing:`,
   and `foreman.md` holds `resume: closing`. Each check reads the shipped card files.

No change to `tests/`: the change adds no refusal. No change to `docs/`: no page describes the
Driver's closing steps. No change to `agents/`, `com.github.copilot/agents/` or `evals/kit/`.

## Out of scope

- The stack driver, the QA driver and the release driver.
- The 130,000-token threshold and the "host asked the hand-back" rule.
- The Verifier's, Inspector's and Coder's cards, and the PR template.
- A new role, agent file, CLI command, hand-back word or record field.

## Evidence

- `just check` passes. The Driver also runs `just eval-dry-run` before the first push (the change
  is under the CLI's `src/`).
- `just scenario` passes with the new check (step 8): the `context: closing` line, the take-back
  with `resume: closing` and the round unchanged, and the card strings read from the shipped
  `driver.md` and `foreman.md`.
- A read of the diff shows:
  - `driver.md` names the trigger (the pushed-head `VERIFIED`), the closing note and the
    hand-back, the `resume: closing` reads, the exception to the 130,000 rule and the no-loop rule;
  - `foreman.md` names the `resume: closing` take-back and the counting exclusion.
- No host and default matrix: the hand-off does not depend on the host (it fires on both Claude
  Code and Copilot, whether the context is measured or not) or on a configured value.
