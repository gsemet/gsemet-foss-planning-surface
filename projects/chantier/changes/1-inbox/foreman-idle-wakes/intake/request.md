# The Foreman's idle wakes: measure a turn's cost, then cut them

In batch-29 orchestration was 52 % of the $243.5 spent: the Foreman alone cost $59.7 (25 %, 983 calls, 292 wakes, context 184k tokens on average, 267k at peak), as much as all CR Drivers together, after 36 % in batch-28 and 48 % in batch-27. Much of it is heartbeats, relays and re-reads while nothing changes.

Wanted (the user's choice, 2026-11-21, "measure then cut"):
1. Measure what one Foreman turn reads and costs, by kind of wake (heartbeat with no event, Driver message, watcher event, the Chief of Staff's order), from the batch's transcripts.
2. Cut the idle wakes: a Foreman wakes on an event (a Driver's message, the watcher's journal line, an order), not on a timer that finds nothing; and a turn that finds nothing new reads as little as it can.

Done when: the measure is in the PR, and a batch's Foreman share drops measurably (target to set in the spec) with no missed event.

Source: batch-29 retro, kept point 1 (retro critic kept it).
