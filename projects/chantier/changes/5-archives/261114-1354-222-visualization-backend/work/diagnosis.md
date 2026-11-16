# CR-222 CI failure: `ConnectionRefusedError: [Errno 111]` on ubuntu-latest

## Cause

`chantier board` prints its start line when its socket is only **bound**, not **listening**.

`skills/chantier/scripts/cli/src/chantier/board/command.py`:
- `_bind` (l.42-53) does `socket()`, `setsockopt`, `bind()` and returns. No `listen()`.
- `board()` (l.102-104) then prints `board on <link> ...` with `flush=True`.
- `_run` (l.56-71) builds the Starlette app, then `box[0].run(sockets=[sock])`. uvicorn starts an
  asyncio loop and only then calls `loop.create_server(sock=sock)`, which is the first `listen()`.

Between the printed line and that `listen()` there is the import and setup of uvicorn and starlette,
which takes from tens of ms to seconds on a cold CI runner. A TCP connect to a bound socket that does
not listen is refused at once on Linux (ECONNREFUSED, errno 111).

The scenario treats the start line as "ready" and requests right away, at these sites in
`scenario/run_scenario.py`:
- l.1321-1325: `second = board(...)`, `second.line()`, then `jget(port, ...)` at once. No delay. This is
  the likeliest failing step, after the first board was stopped.
- l.1355-1357: `timed.line()`, then `jget(tlink.port, ...)` at once.
- l.5608-5612: the surface board, `bp.line()`, then `jget(...)` at once.

The first board (l.1162-1176) is protected only by the `first.line(1.5)` wait that follows the line,
which gives the server 1.5 s to start. That is luck, not a guarantee.

An uncaught exception in `check` bodies ends the scenario. That is why the log shows a single FAIL
"scenario ran to the end" and 676 of 677 checks (the local run has 719; the rest never ran).

## Why Windows passes

On Windows, `connect()` to a bound but not listening port is retried by the TCP stack for about 2 s
before it reports WSAECONNREFUSED (10061). The server is up within that window, so the race is hidden.

Proof, run on this Windows machine (no WSL or docker here, so Linux is shown by reasoning plus the
known semantics of Linux TCP):

```python
s = socket.socket(); s.bind(("127.0.0.1", 0))
socket.create_connection(("127.0.0.1", s.getsockname()[1]), timeout=10)
# -> ConnectionRefusedError 10061 after 2.06 s  (Windows retries the SYN)
# On Linux the same call returns ECONNREFUSED in under a millisecond: no SYN retry for a
# closed (non-LISTEN) port, the kernel answers with an RST.
```

So the scenario's immediate request after the start line, which succeeds on Windows because of the
2 s retry, gets Errno 111 on Linux whenever uvicorn needs more than a few ms to reach `listen()`.

I did not need the other suspects: seat watch (a daemon thread started after `arm`, not involved in
the socket), `0.0.0.0` binding (the l.1349 step makes no request, only reads lines), and port 0
parsing (the regex and `sock.getsockname()[1]` are correct, and failures with a bad port would give
a failed `check`, not an exception).

## Fix (for a Coder)

One line in `skills/chantier/scripts/cli/src/chantier/board/command.py`, in `_bind`, inside the
`try`, right after `sock.bind((host, port))` (l.49):

```python
        sock.bind((host, port))
        sock.listen(socket.SOMAXCONN)
```

Update the docstring ("bound and listening before anything is printed"). Why this is right:
- A listening socket queues connections in the kernel backlog, so a request sent right after the
  start line waits until uvicorn accepts, instead of being refused.
- uvicorn calls `listen(backlog)` again through `loop.create_server(sock=sock)`: harmless, it only
  changes the backlog.
- The "port held by another program" path is unchanged: `bind` still fails first, and `listen` is
  never reached.
- The "board already running" probe (`_running`, l.74-77) runs before `_bind`, so it is not
  affected.

Nothing else in the CLI changes. The scenario needs no change, and must not get a retry loop
(a workaround).

## Check after the fix

`just scenario` on Linux (CI), and `just check`. If a Linux box is wanted locally: start the board
under `python -X importtime` or add `time.sleep(2)` before `box[0].run(...)` in `_run` temporarily; on
Linux it then fails at once with 111 without the fix and passes with it. On Windows the same delay
(`sleep(5)`) reproduces it too, since it exceeds the 2 s retry window.
