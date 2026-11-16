# The cost report says who spent what, and explains it

## Problem

The pricing is right (batch-06: $49.285 over 1232 calls, recomputed from the raw transcripts), but the
report is not:

- The Chief of Staff groups `cost --by role` by hand into orchestration, implementation and review. It
  drifted from the card: $41.47 of orchestration instead of $19.07.
- The card's groups mislead anyway: 84% of its "implementation" is Drivers, and a user's own Driver or
  reviewer falls in it.
- `_cost_summary` calls a Driver an agent that started one, so 7 Drivers with no worker count as
  workers ($3.42), and a QA or release driver, which has no Agent tool, always does.
- `_cost_summary` prints "Driver cr-driver $28.26" with its workers next to "Drivers $18.97" without.
- Nothing tells the user why the figures are what they are: it took a subagent of 136k tokens.

## Change

**Who is who, from the record.** In `commands.py`: the Foreman is the main agent, a Driver an agent with
no parent, a worker an agent with a parent. No role name is added to the CLI: a user's own Driver gets
its line under the type the host gives it. Check this on Copilot's transcripts; where the parent links
are missing, the report says `not measured`.

**One breakdown, computed.** `cost` prints one line for the Foreman, one per Driver type and one per
worker type, each with its own calls and dollars only, and they add up to the total as printed.
`_cost_summary` uses it, and names its "with workers" figures as such, so that two figures for one word
no longer sit side by side.

**The report shows it as printed.** In `chief-of-staff.md`, Cost: the cost table is those lines, in that
order, with the Chief of Staff's session apart. The words orchestration, implementation and review as
groups go, and the Chief of Staff adds or regroups nothing. The same holds for the Progress and
Completion reports and for the README.

**The figures explained.** `cost --explain` prints, for each line of the breakdown, what the report needs
to explain it, all measured: the number of agents, the calls, the model, the shares of cost in cache
reads, cache writes and output, the calls made after the cache expired, and how many Drivers restarted
on a CR that already had one. It ends with what the figures do not count (compaction calls). In the
card: the Chief of Staff gives this explanation, in a few plain lines from that output, in the
Completion report and when the user asks; a Driver's line covers its own rebases, gates and file writes,
and the card says so. It starts no subagent for it.

## Out of scope

Rates and pricing stay as they are. Lowering the spend, the Drivers' model (`drivers-sonnet`) and pricing
compaction calls are other changes.

## Done when

- On a fixture with a Foreman, a Driver with workers, a Driver with none and a root agent of an unknown
  type, `cost` shows each on its own line, and the lines add up to the total as printed.
- `cost --explain` prints the measures above on that fixture.
- `cost --by cr` still adds up to the Drivers and workers.
- The card, the README and the scenario say the same thing; no report groups by hand.
- `just check` and `just scenario` pass.
