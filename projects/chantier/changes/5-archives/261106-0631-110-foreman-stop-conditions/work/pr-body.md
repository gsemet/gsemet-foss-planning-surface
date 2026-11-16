The Foreman now ends its heartbeat when nothing can move, and never its session: an idle session still receives an order. The CLI does not change.

## What changes

- **The heartbeat:** on Claude it goes from `55m` to `30m`, in `foreman.md` and the table of `README.md`. Copilot's `/every 4m` stays.
- **When it ends:** the Foreman ends the `/loop` (`ScheduleWakeup` with `stop: true`) right after `land`, and on a wake where no Driver of any kind has run since the last wake and no order is undone. A stack or a batch blocked and not finished is such a stop: the batch stays open and the user wakes the Foreman.
- **When it starts again:** an order's line or a `ping` starts a turn; a turn that leaves a Driver running arms the heartbeat again. On Copilot the Foreman cannot end `/every`: the Chief of Staff tells the user to delete it and arms it again with the next order.
- **A Driver's wait has an end:** with no CI result after 3 hours on one head, a Driver ends with `handback <cr> blocked infra: CI still running after 3 hours`; a project whose rules give a longer CI gives its own limit. In `foreman.md`, a `pong` proves a Driver is alive, not that it moves: no new round, head or note for 3 hours gets `stop`.
- **Reading a silent Foreman:** in `chief-of-staff.md`, "Recovery", a stale heartbeat says something only while a CR is `working`. `SILENT_MINUTES` in `hooks/register.tsx` goes from 20 to 40, above the heartbeat, and its test follows.

## Checks

- `just check` (26 tests, Windows) and `just scenario` pass at this head.
- `grep -rn "55" README.md skills/chantier/references` names no heartbeat.

## Not proven yet

- `hooks/register.test.tsx` was not run: `just check` does not run it, as it needs the host. Its change was reviewed by reading only.
- The new stop was not tried with real agents; the `claude-smoke` campaign covers a change to a role or the flow.
