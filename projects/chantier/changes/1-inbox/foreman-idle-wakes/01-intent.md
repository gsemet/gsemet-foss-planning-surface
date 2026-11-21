# The Foreman's idle wakes: measure a turn's cost, then cut them

From the batch-29 retro (kept point 1): orchestration was 52 % of the batch's $243.5, and the Foreman alone cost $59.7 (25 %, 292 wakes, 184k tokens of context on average), as much as all CR Drivers, much of it on heartbeats, relays and re-reads while nothing changes.

Intent: measure what one Foreman turn reads and costs by kind of wake, then cut the wakes that find nothing new, so the Foreman's share of a batch drops with no event missed.
