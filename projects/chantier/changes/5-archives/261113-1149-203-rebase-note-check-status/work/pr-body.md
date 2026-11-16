## Summary

The session that steers a batch, in either of its two modes, could send the agent running a CR a
`rebase:` note just after that agent had handed the CR back ready. That agent, by its card,
refuses to start work on a note that carries no `taken back:`, so one exchange was lost and the
rebase was delayed. Now the steering session reads the CR's state just before it sends any note
that carries work, and takes a ready or blocked CR back instead of messaging it.

## Deliverables

The rule, written once in the steering card and inherited by the direct mode's card:

| State shown by a plain `status` read just before the note | Path |
| --- | --- |
| `ready` or `blocked` | no message: `take <cr> --note "<the note>"` and the existing take-back path |
| `working` | the note message to the agent, as before |

- The read is a plain `status`: no `--refresh`, no `--epoch`, so it is not a wake and records no
  heartbeat.
- It covers every note that carries work (a `rebase:` first of all, an order note, an answer).
- No second, shorter path for a rebase on a ready CR; no CLI change.
- The rule for the agent running the CR is unchanged: a note with no `taken back:` after its
  hand-back is still passed up. That is the net for a hand-back landing between the read and the
  message, a window of seconds that costs one exchange and loses no work.

## Blast radius

Grade: **1**. Two cards change, no code; a plain `git revert` restores the previous behaviour.

## Autonomous decisions

- The Series sub-bullet's back-reference to the rule is worded in the card's own style (the
  specification gave the Parallel wording only in general terms).

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/foreman.md`: the "Orders are the user's word" bullet carries the
  rule; the Parallel and Series `order merged` sub-bullets point back to it; the "taken back from
  `ready`" bullet says its `status` read may be the same one.
- `skills/chantier/references/chief-of-staff.md`: one bullet under "Steering a batch yourself"
  makes the inheritance visible.

## Impacts

No visual change. Steering sessions read the cards at their next start.

## Test plan

- [x] No behaviour change in code; the CLI and the card of the agent running a CR are untouched
- [x] Local gates at `901c916`: `just check` pass; `just scenario` carried from `3caa3fa`: patch unchanged; the long gate runs once at the top of the stack, PR 152
- [x] Review: approved at `d178c7e` (reviewed uncommitted, committed as `3caa3fa`; carried to `901c916`: patch unchanged by the restack)
- [x] Verified at `901c916`
- [x] CI green at `901c916`

## Internal references

- CR-203 the-steering-session-reads-status-before-a-note-that-carries-work (real-direct run 1,
  finding 8)

</details>
