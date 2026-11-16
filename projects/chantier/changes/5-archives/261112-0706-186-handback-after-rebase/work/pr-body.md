**Eval run: do not merge.** The maintainer decides what happens to this PR.

## Summary

A CR handed back as ready and later sent back to its Driver (for a rebase or a fix) could not be handed back again: `handback` refused it with "no Driver to hand it back", and nothing steered the steering session towards `take <cr> --note`. This PR makes the refusals name the way out, refuses a hand-back whose worktree head `ship` did not record, and tells the steering session to resume the Driver that handed the CR back.

## Deliverables

Three CLI messages, before and after:

| Command | Before | After |
|---|---|---|
| `handback` on a ready or blocked CR | `<cr> is ready: no Driver to hand it back` | `<CR> is ready: no Driver holds it until the steering session takes it back (take <CR> --note "<why>"), then hand back again` |
| `handback ready` after a commit with no `ship` | the head cause mixed with the gate and verdict causes | one refusal alone: `the worktree's head <short> is not the head ship recorded (<recorded>): ship <CR> <pr> again, then the long gate and a verdict VERIFIED at the new head` |
| `order note` on a ready or blocked CR | `noted on <cr>: ...` | the same, plus `<CR> is <status>: no Driver works on it until the Foreman takes it back (take <CR> --note "<why>")` |

Card choices: work on a ready or blocked CR reaches a Driver only through `take --note` (reopens to `working`, no round); the Foreman resumes the Driver that handed a ready CR back, and starts a new one only if it does not answer; a Driver resumed by a `taken back:` note goes on as from a prompt's `Note:`.

## Blast radius

Grade: **1**. Three CLI messages and a head check on `handback ready`, plus card text; a plain `git revert` restores the previous behaviour.

## Autonomous decisions

- The head check replaces the existing mixed head cause line in `handback ready`, instead of adding a second check, to keep one refusal per cause.
- Cards say "by the host's means" rather than naming `SendMessage` or `write_agent`, as the structure test forbids host tools in the cards.
- ship stores the full SHA at this base, not 7 characters: the head check compares by prefix and the refusal prints the recorded head as stored.

<details>
<summary>Details</summary>

## Changes

- `commands.py`: `handback` refusal for ready or blocked; standalone prefix-compared head check; `order note` extra line.
- `foreman.md`, `driver.md`: the `take` route, the resume of the Driver, the new hand-back refusals.
- `scenario/run_scenario.py`: `handback_proofs` proves the refusals, the `take`, the head check and the second hand-back.

## Human decisions

- A ready CR sent back is reopened by `take <cr> --note`; it counts no round.
- The Driver passes both gates again at the new head, then hands back ready again.
- The Driver that handed the CR back is resumed; a new one only when it does not answer. Ready only: a blocked CR keeps a new Driver.

## Impacts

No visual change. Refusal texts of `handback` and `order note` change.

## Test plan

- [x] `just check` at 718c9ed (gate and CI on three systems)
- [x] `just scenario` at 718c9ed (gate and CI)
- [x] Verifier at 718c9ed: VERIFIED. The Driver resume is card behaviour, **UNVERIFIED** until an eval run shows it.

## Internal references

CR-186 "A ready CR sent back to its Driver can be handed back again", batch-12.

</details>


