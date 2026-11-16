# A Foreman's session is named after the Chief of Staff's, with no epoch

## Problem

The user does not want "epoch" in a session's name. batch-06's Foreman, started from a pasted
prompt, is titled "Chantier Foreman batch-06 epoch 1". The card's form, `<your title> - Foreman
[<batch>]`, applies only when the Chief of Staff starts the session itself.

## Change

- A Foreman's session title is `<Chief of Staff's session title> - [Foreman Batch <nn>]`, `<nn>`
  the batch's number on two digits: `[Battlestation] Chantier - [Foreman Batch 06]`.
- The Chief of Staff gives this title to `start_session`, and on Copilot to `create_session`.
- The start prompt carries the full title, and the Foreman sets it on itself as its first act:
  that covers a session the user started and a reused Foreman, whose title names the old batch.
  On Claude with `set_session_title`; on Copilot when the host offers it, else the title stays.
- A later Foreman of the same batch has the same title.

## Out of scope

"Epoch" stays where the user does not read it: the CLI's `--epoch` and the cards' rule on who owns
a batch. No word in a message to the user, a report or a title says it.

## Done when

- `chief-of-staff.md` and `foreman.md` say the above, and no report or title form holds "epoch".
- The change goes where CR-123 leaves the host's lines, if CR-123 is merged first.
- `just scenario` passes.
