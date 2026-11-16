# The Foreman stops waking when nothing can move

The Foreman ends its heartbeat, never its session: an idle session still receives an order, as it
does today. The CLI does not change.

## The heartbeat

On Claude it goes from `55m` to `30m`, in `foreman.md` and the table of `README.md`. Copilot's
`/every 4m` stays.

## When it ends

In `foreman.md`, the Foreman ends the `/loop` (`ScheduleWakeup` with `stop: true`):

- right after `land`;
- on a wake where no Driver of any kind has run since the last wake, and no order is undone:
  every Driver has ended, ready or blocked, for 30 minutes at least. A stack or a batch blocked
  and not finished is such a stop: the batch stays open, and the user wakes the Foreman. Its asks
  are recorded, so it sends no further line.

While any Driver runs (CR, stack, QA or release) the heartbeat goes on: its silence is still the
Foreman's to catch.

## A Driver's wait has an end

A long PR keeps its Driver alive, through CI and the fixes it brings: that is what holds the
Foreman. So each Driver must end. Rounds, the budget and the single re-run of an infrastructure
failure already bound the fixes. What nothing bounds yet is a wait: a CI that never ends, answered
by a `pong` at every ping.

In `driver.md`, section CI: with no result after 3 hours on one head, the Driver stops waiting and
ends with `handback <cr> blocked infra: CI still running after 3 hours`. A project whose rules
give a longer CI gives its own limit. In `foreman.md`: a `pong` proves a Driver is alive, not that
it moves; a Driver with no new round, head or note for 3 hours gets `stop`.

## When it starts again

An order's line or a `ping` starts a turn. If the turn leaves a Driver running, it arms the
heartbeat again.

On Copilot the Foreman cannot end `/every`. The Chief of Staff tells the user to delete it, as it
does at landing, and arms it again with the next order.

## Reading a silent Foreman

- In `chief-of-staff.md`, "Recovery": a stale heartbeat says something only while a CR is
  `working`. With none, the Foreman has stopped waking, as it should.
- The board already alerts only while a CR is `working`, but `SILENT_MINUTES` in
  `hooks/register.tsx` is 20, below the heartbeat, so a healthy Foreman shows as silent between
  two wakes. It goes to 40, and its test follows.

## Done when

- `just check` and `just scenario` pass, and `grep -rn "55" README.md skills/chantier/references`
  names no heartbeat.
