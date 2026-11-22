# Diagnosis: surface-board check "an `events` subscription gets that line, with its `seq`" (CI run 44964890886)

Reproduction: `uv run python scenario/run_scenario.py --unit surface-board --forge github` (about 300-450 s; not run here, per the brief). Flaky by timing; not reproduced locally.

## Cause (a test-side race; read from the code, not reproduced)

scenario/run_scenario.py, board_api, lines 1740-1754:

    ws.send(sub events "e")        ; frame_of(ws, "result", id == "e")
    ws.send(call backlog.move "m") ; moved = frame_of(ws, "result", id == "m")
    ...
    said = frame_of(ws, "event", sub == "e" and data.lines)   # 15 s

`frame_of` (line 1669) reads the socket and DISCARDS every frame that is not the one asked for. While `moved` waits for the `result` of `m`, any `event` of sub `e` that arrives before that result is thrown away. The later `frame_of(... "event" sub e ...)` then waits 15 s for a NEW rev and gets None (the `events` rev is the last seq: it does not move again) -> `said is None`, the check fails. The failure line `str(said)` would read `None`.

The server gives no ordering between a call's `result` and another subscription's `event`:
- `backlog.move` runs `write_api._answer`, which appends the `board@1` line to `forge-journal.jsonl` BEFORE the call returns (write_api.py lines 85-86). After that: the body is built, then `ws._run` does `ctx.seats.gone()` (file reads, ws.py 179-183), then the executor hands back to the asyncio loop, then `conn.post(result)` (ws.py 198-203).
- The push thread (`PushLoop.poll`, every 1 s in the scenario, `CHANTIER_API_TEST_TIMES=1:...`; also woken by the file watch) reads the `events` topic (`topics._events`, which reads the journal by size/mtime, not gated by the file watch) and sinks the event with `Connection.post` straight from its own thread (`Gate.sink` is open since `e`'s `result`). So when a push pass lands between the journal append and the `result` post, the `event` frame is queued before the `m` result.
- The only ordering the server guarantees is a sub's `result` before its first `event` (the Gate). Nothing for a different call.

Why only on CI: the window (append -> result post) is a few ms on a quiet machine, but the push pass reads the `project` topic first on the same pass (heavy: state read), and the runner is slower and loaded (unit ran 308 s with 2-core contention), so the GIL and executor hand-offs stretch the window and a 1 s push pass lands in it. The same unit passed on Windows (449.8 s) and in earlier runs: consistent with a low-probability race.

Other checks on the same path were ruled out by reading:
- inotify vs check mode: the `events` topic does not depend on the file watch (settle only wakes the push earlier); both modes give the same event.
- first-event wait: 15 s is far above the 1 s look; settle rule (1 s quiet / 5 s most) is irrelevant to `events`.
- subscribe/cursor: `e` is subscribed before the move and `cursor = last_seq` at subscription; the journal cache is keyed on (size, mtime_ns), size always changes on an append.
- another journal line (hub `merged@1`/`checks-red`, deduped by key; board's writer): the earlier check `len(lines) == before + 1` passed, so no extra line in the window up to the move's result. A later extra line (the hub cycles at 20 s while observed) would make `said.lines[-1].seq != lines[-1].seq`; possible but much less likely than the discard (the hub dedups, one line per event). It cannot be excluded without the transcript.

## Place and smallest fix (recommended, not applied)

scenario/run_scenario.py, lines 1741-1751: stop discarding frames between the call and the event. Smallest change: make the wait for `m`'s result keep the `event` frames of sub `e` it passes over, and look at them first for the line, e.g. a `frames` list filled by a local reader used for both waits (read until both `result m` and an `e` event with `lines` have come, either order, 15 s). The check text and assertions stay the same.

Server code needs no change: the protocol does not promise an order between a call's result and another sub's event.

Alternative (weaker): subscribe `e` with `args.after = <seq before the move>` after the move; deterministic, but no longer tests the push of a line to a live subscription.
