## Summary

Two Drivers of a past batch ended near 90k tokens, one with a `blocked context:` hand-back the figure did not support and one with no hand-back at all. The Driver card's 150,000-token threshold also sits only about 12k below where agents were measured to compact. This PR sets the threshold from that measure, tells a Driver never to end its turn to wait for a child, and caps the Inspector's JSON reply, which reached 9,343 characters.

## Deliverables

The measure (transcripts of the batch-16 and batch-17 steering session; the last prompt is the sum `costs.agent_context` makes):

| Driver run | Calls | Last prompt | How it ended |
| --- | --- | --- | --- |
| CR-215 Driver | 14 | 92,125 | resumed a worker by message, then called the host's hand-back with no `$CHANTIER handback` |
| CR-216 Driver | 12 | 91,771 | ended its turn to wait for a worker; the host asked for its hand-back; it handed back `blocked context:` at 91,159 |

First compaction of agents set to `autoCompactWindow: 200000` (three Coders): after a last prompt of 161,951, 164,772 and 166,684 tokens. The CLI's `context:` line was checked against a transcript (44,582 both) and needs no change.

Before and after, in the Driver card's Context bullet:

| | Before | After |
| --- | --- | --- |
| Threshold | 150,000 (three quarters of 200,000) | 130,000 (about 32k below the first measured compaction) |
| `blocked context:` | at the threshold | only when the last `context:` line read 130,000 or more; another stop names its own reason |
| Waiting for a child | not said | never end the turn for it; the CI watch is the one wait |
| Host asks for the hand-back early | not said | note, then `blocked context: host asked the hand-back at <n> tokens: ...`, then the host's hand-back |

The Inspector's reply is capped: 300 characters an item, five `minor` items, 3,000 characters in all.

## Blast radius

Grade: 1. Cards only, no code; a plain `git revert` restores the previous text.

## Autonomous decisions

None.

## Known gaps

- The 130,000 threshold is not yet seen working in a real batch: it is proved only when a Driver of a later batch hands back `context:` at or past 130,000 with no compaction before it.
- The ten-line cap on the Coders' and Verifier's replies, which the measure shows is not kept (93 to 105 lines, 69 lines), is left out of this PR on purpose.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/driver.md`: the Context bullet (threshold, when `context:` is the reason, no turn end to wait for a child, the host-asked hand-back).
- `skills/chantier/references/worker.md`: "Inspector" gains the reply cap.
- `skills/chantier/references/hosts/claude-code.md`: "Compacting" carries the measured compaction point; the capabilities table gains the fact that a subagent that ends its turn with nothing in the background is asked for its hand-back at once.

## Impacts

No visual change. A Driver hands back earlier and for the right cause; Inspector replies are shorter.

## Test plan

- [x] No behaviour change: cards only
- [x] Local gates at `05b6375`: just check, long gate (github 695/695, gitlab 676/676)
- [x] Evidence: the diff is the before and after
- [x] Review: approved at `8d9efdb`, carried unchanged to `05b6375` (rebase only, patch unchanged)
- [x] Verified at `05b6375`
- [x] CI green at `05b6375`

## Internal references

- CR-236 driver-context-budget; depends on CR-230 worker-reply-contract (merged; this PR is based on main).

</details>


