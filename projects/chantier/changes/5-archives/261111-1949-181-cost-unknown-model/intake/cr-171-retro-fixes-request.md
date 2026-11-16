# The retro's fixes after CR-171, in one CR

Batch-09 retro, 2026-11-11, the pause after CR-171. The user picked these three points to file
before `close`. They are filed as one CR, as the user asked for the previous retro ("Une seule
CR").

## 1. The hook's tests run somewhere

Moved on 2026-11-11 to `worker-write-guard-redesign` (the user, second grill: a `just mod`
recipe, run by the agent itself before a hook change merges). This item keeps points 2 and 3.

- CR-171's `hooks/register.test.tsx` was never run.
  - The `claude` CLI is not on the Windows machine's PATH, and CI does not run
    `claude plugin test`.
  - The Chief of Staff checked the event shapes against the engine's types by hand: `agent.spawn`
    resolves at start, and `tool.call` carries `tool`, `input` and `agentId`.
- Fix to grill: CI runs `claude plugin validate .` and `claude plugin test .`, or CONTRIBUTING.md
  says where they must run before a hook change merges.

## 2. A Driver reads its team with `handoff`, not `round`

- The CR-171 Driver ran `round 3` (note "x") only to read the `team:` lines, which spent one of
  its three rounds.
- Fix to grill: `driver.md` says the Driver reads the `team:` lines with `handoff`, which counts
  nothing; `round` is only for starting a round.

## 3. `cost` labels the steering session's own subagents plainly

- After CR-171, the pause report shows the subagents that belong to no CR as `Driver
  chief-of-staff with its workers: $26.54 (424 calls)`. They are not a Driver.
- Fix to grill: the line reads as the steering session's own subagents (CR-171's
  specification, part 4: "Chief of Staff's own subagents", or the Foreman's), never "Driver".
