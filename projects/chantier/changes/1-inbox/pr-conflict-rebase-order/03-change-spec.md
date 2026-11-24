# One board per surface, and a watcher that reaches the forge hub

The forge hub stayed idle for batch-31 for six hours while two watchers of the Chief of Staff and a
board page were "subscribed": the merges of CR-477, CR-479 and CR-483 were never journalled. This
change makes sure that a subscribed watcher is in fact subscribed to the server that holds the
forge hub, so the hub reads the forge for a running batch. A watcher that loses that server
subscribes again, or says it is no longer subscribed. `status` tells the cases apart.

Scope (pr-conflict-Q1 A, 2026-11-24): the hub and the watcher only. The detection of PRs left in
conflict by a merge, and the order to rebase them, belong to the separate inbox item
`pr-conflict-detect-and-rebase-order`. Destination (pr-conflict-Q2 A): the running batch batch-31.

Base: `origin/main`. The local main checkout is behind it. `origin/main` already holds CR-476
(the stream watcher, `--stream`, and no 2 h end while a batch is in flight), CR-478
(`serve --restart`, `board/restart.py`) and CR-479 (the Foreman's own watcher,
`hub/watch_reads.py`). Read them there, not in the local checkout.

## The cause, as read on 2026-11-24 at 20:36 UTC (to be proved first, below)

The code path works as designed. `hub/loop.py` `HubLoop.poll` reads only while `observed()` is
true, and `observed()` is `PushLoop.observed` (`board/api/push.py`) of the server process that
holds `hub.lock`: true while that process holds a subscription. `status`'s line
"forge hub: ... idle (no client subscribed)" (`hub/lines.py` `hub_line`) reads the `idle` flag of
the `hub` entry of `server.json`. That entry was true: the process that holds the hub really had
no client.

The clients were connected to another process. Two `chantier serve` processes serve the planning
surface at once:

```
TCP 0.0.0.0:8765    LISTENING  29916   serve --host 0.0.0.0 --seat local_ce68... (started 14:25:02 UTC)
TCP 127.0.0.1:8765  LISTENING  37316   serve --seat local_ce68... --stop-idle   (started 14:25:02 UTC)
TCP 127.0.0.1:8765  ESTABLISHED 37316  <- the watcher (PID 22552, `watch --after 113`), Chrome, Claude desktop
```

- `server.json` names PID 29916 in its `server`, `hub` and `writer` entries. That process holds
  `hub.lock` and `writer.lock`, but no client reaches it: it is idle, which is true.
- PID 37316 is not in `server.json` and holds neither lock. Its `HubLoop` tries `hub.lock` every
  second and never gets it, so it never reads the forge. It does receive every loopback client:
  `Board.link` (`hub/feed.py`) links to `loopback_base(0.0.0.0, 8765)`, which is
  `127.0.0.1:8765`, and Windows gives that connection to the more specific bind. Because it always
  has clients, its `--stop-idle` never fires.
- Both started in the same second, from the same seat: the session's explicit
  `serve --host 0.0.0.0 --seat` and its watcher's detached `serve --seat --stop-idle`
  (`hub/feed.py` `serve_argv`). `board/command.py` `board()` checks for a live server
  (`state.live_entry`, `_answering`), then binds (`board/binding.py`), then writes its `server`
  entry. Nothing makes that check-then-bind-then-write atomic, so both passed the check.
- Windows let the second bind succeed. `binding._open` sets no `SO_REUSEADDR` on Windows, but it
  does not set `SO_EXCLUSIVEADDRUSE` either. Without it, a process of the same user can bind
  `127.0.0.1:8765` while another holds `0.0.0.0:8765`, so the port did not count as "held" and the
  start did not walk to the next free port. macOS (BSD semantics with `SO_REUSEADDR`, which
  `_open` sets there) may allow the same thing. Linux refuses that bind, so there the second
  server walks to 8766 (commit 627bd4d2, "start on the next free port") and is still a second
  server.
- The watcher's link was alive the whole time (ticks every few seconds), so `status` printed
  "watch: this session's watcher runs" next to "forge hub: idle (no client subscribed)". Both
  lines were true, each about a different process.

Ruled out on the same reading: no `gh` process was alive under 29916 (no hung forge read), and
`connectors/run.py` bounds a read at 20 s. The lifecycle lock that `journal.append` takes is
bounded at 30 s (`store/folder.py`).

## What the Driver proves first, before any fix

1. Reproduce the double server in a test that fails on today's code. Start two servers for one
   surface at once, or start the second while the first is past its live-entry check and has not
   yet written its entry. Today both serve. With one on `0.0.0.0` and one on `127.0.0.1`, they
   share the port on Windows, and a loopback client reaches the server that holds no hub.
2. A bind test on the three systems of `just check`: with a socket listening on `0.0.0.0:<p>`,
   `board/binding.py` opening `127.0.0.1:<p>` must count as "port held". Today it succeeds on
   Windows (and possibly macOS), so this test fails there before the fix.
3. Put the evidence above (the listening table, the two command lines, the `server.json` entries
   without keys) in the PR's Known gaps or Deliverables. If the live state differs when the Driver
   looks (for example, someone stopped 37316), quote what was seen and the reproduction test
   instead.

If the proof shows a different or an additional cause (a subscription that a live server holds
but `observed()` does not count, a hub thread that stopped), the Driver says so to the Foreman
before fixing, with the evidence. The fix below targets the cause named above.

## What changes

### One server per planning surface and machine (`board/command.py`, `board/binding.py`)

- Two `chantier serve` starts for one surface on one machine, concurrent or not, never give two
  serving processes. Exactly one serves. The other behaves as a start that finds a board running
  does today: it prints "board already running at <link>" with its lines, registers its `--seat`
  on that board, and exits. A start that finds the surface held by a process that does not answer
  refuses with today's silent-board text.
- The check and the claim are one atomic step, held by an OS lock in the git folder. Prefer an
  existing lock file. If the Driver needs a new file there, AGENTS.md names it in the same PR,
  beside `server.json.lock`, `hub.lock` and `writer.lock`. A process that serves holds the
  surface for its whole life. `serve --restart` (CR-478) keeps working: the old process releases
  the surface when it ends, and the new one takes it.
- "Port held" means held on any address, on every system. A bind on `127.0.0.1:<p>` while
  another socket listens on `0.0.0.0:<p>` (or the reverse) is a held port. With the default port,
  the start walks to the next free one, as the walk already does for any held port. With a named
  port, it refuses with the held-port text. On Windows the board's socket is exclusive
  (`SO_EXCLUSIVEADDRUSE` or what the Driver finds equivalent). On POSIX, the Driver checks that
  `SO_REUSEADDR` does not let a specific bind share a wildcard-bound port (macOS), and closes that
  gap if it does.
- No server serves clients while another process holds the surface's hub, so a loopback client
  can no longer reach a process that never reads the forge. A server that finds the surface held
  by another live server stops (see open question 1 for one that is already running).

### The watcher reaches the server that holds the hub (`hub/watch.py`, `hub/feed.py`)

- A watcher links only to the server that `server.json` records, and it confirms that it is that
  server: the process that answers its link is the recorded `server` PID, which is also the `hub`
  PID. A link that reaches another process does not count as linked. The watcher drops it and
  links again, and if it is still not on the recorded server after `SILENT_S` (20 s), it ends with
  a line that names both PIDs and the remedy (stop the stray server, then start the watcher
  again). The Driver chooses how the server says who it is: its `welcome`, the probe it already
  answers, or the `events` topic.
- After a server restart (`serve --restart`, a crash, an idle stop followed by a new start; a new
  PID, maybe a new port), a running watcher (plain or `--stream`) links again to the newly
  recorded server within a bounded time (at most `SILENT_S` plus `RETRY_S`). It resubscribes from
  its cursor, so no journal line is lost or told twice (the `after:` rule `clients/tui/link.py`
  already keeps). If the seat rule allows it, the watcher starts the server when none runs, as
  today.
- A watcher never says it runs while it receives nothing. While it is not subscribed to the
  recorded server, it either links again within the bound above or ends with its line. It never
  sits for hours on a link to a process that has no hub.
- The Foreman's watcher (CR-479: it starts no server) follows the same linking rule.

### The hub entry and `status` (`hub/state.py`, `hub/cycle.py`, `hub/loop.py`, `hub/lines.py`)

- The `hub` entry of `server.json` says whether a client observes the hub, and the Driver may
  add how many clients do, as it does today with `idle`. A process that does not hold the hub
  never writes that entry (unchanged).
- `status` tells these states apart, one line each, with no contradiction left unexplained:
  - the hub reads: "forge hub: PID n, the surface server, last read <t>" (unchanged);
  - the hub is idle and no watcher of this session runs: "idle (no client subscribed)" (unchanged);
  - this session's watcher runs, but the hub sees no subscriber, or the watcher is linked to
    another process than the hub's: one line that says the watcher is not subscribed to the hub,
    names the PIDs it can name and gives the remedy. `status` never prints
    "watch: this session's watcher runs" and "forge hub: idle" side by side without that line;
  - two live `serve` processes for the surface, if `status` can see them (for example a live
    server that answers the recorded port but is not the recorded PID): one line naming the stray
    one and how to stop it.
- `serve`'s start line and the watcher's start line say "board already running" when they join
  a running board, as today. They never report a server they started if that server did not take
  the surface.

### AGENTS.md

The PR rewrites AGENTS.md's long sentences on the surface server, the forge hub and the watcher
so that they say what is now true. Shorter sentences are fine, but no named exception,
permission, file or network use is dropped or widened. In particular:

- the surface server: one serving process per planning surface and machine. A second start joins
  the running one or refuses, and never serves. "Port held" covers any address. Keep the
  "next free port" rule (remote-cli-Q17);
- the forge hub: it reads while a client is subscribed to the server that holds it. Add the
  watcher-lock signal only if open question 2 is answered B;
- each session's watcher: it subscribes to the recorded server's `events` topic, confirms that
  this is the server that holds the hub, links again after a restart, and ends with a line when it
  cannot. Keep CR-476's end rules;
- any new lock file in the git folder, named in the list of what chantier writes there.

### Cards

If a card tells the Chief of Staff to start the board and the watcher together (the double start
seen here), the Driver adjusts it so the two starts no longer race. The CLI's single-server rule
must hold anyway, whatever a card says. Change a role's agent files on both hosts together only if
an agent file names this; the card is where the contract lives.

## Host and default matrix (evidence: one line per cell)

- Windows, `board.host: network` (`0.0.0.0`), then a second start on loopback: a second server
  today (the observed case). After the fix, one server, and the second start joins it.
- Windows, both loopback: today the second bind fails and the start walks to 8766, so a second
  server. After the fix, one server.
- Windows, `--host 0.0.0.0` with a named port, and another program holding `127.0.0.1` on that
  port: refused as held.
- Linux, any `board.host`: today a second server on 8766. After the fix, one server.
- macOS, `board.host: network` then loopback: proved by `just check`'s macOS run of the bind
  test (step 2). After the fix, held.
- `--forge-always` (a host that cannot run the watcher): the hub reads with or without a client
  (unchanged). The single-server rule holds.
- Shipped default port (8765, walk on) versus a configured `board.port` (refuse when held): both
  count a port held on any address.

## Evidence

- Tests (`tests/`, in-process, few and parametrized, inside the `just test` budget):
  - the bind test of step 2, on the shipped `board/binding.py`, run by `just check` on Linux,
    macOS and Windows;
  - the double start of step 1: one serving process, the second start prints
    "board already running" and exits;
  - the watcher, its `Board` replaced by a fake: a link answered by a process other than the
    recorded server is not counted as linked, and the watcher relinks or ends with its line; a
    recorded server whose PID changes (restart) gets the watcher's new subscription within the
    bound, from its cursor;
  - `status` (`hub/lines.py`): the line for "watcher runs, hub sees no subscriber" on a prepared
    `server.json` and watcher lock; the unchanged lines for the reading and the idle hub.
- Scenario (`just scenario`), one step: start the board and, at the same moment, a watcher that
  would spawn one. Then assert one serving process for the surface, the watcher subscribed to it,
  the `hub` entry not idle, and a merge of the scenario's PR journalled and told by the watcher.
  Then `serve --restart`, and assert the same watcher subscribed to the new process and the next
  event told once.
- The live evidence of step 3 in the PR.
- `just check`, `just eval-dry-run` (a change under the CLI's `src/`), and the long gate
  `scenario` as AGENTS.md asks for this batch's shape.

## Out of scope

- Detecting PRs in conflict after a merge and ordering their rebase
  (`pr-conflict-detect-and-rebase-order`).
- The watcher's end rules of CR-476 (the 2 h end while no batch is in flight), unchanged.
- The hub's read cadence (20 s), the forge connectors and what the hub journals.
- Stopping the stray server that runs now (PID 37316). That is an operation for the Chief of
  Staff or the user (stop it, and the loopback clients reach PID 29916), not part of the change.

## Open questions

1. A stray server that is already running when the fixed build arrives, or one that appears
   anyway: should a server that finds the surface held by another live server, or finds itself
   not the recorded one, stop by itself? Or does the fix only prevent new duplicates, with
   `status` and the watcher naming any stray one for the user to stop? Recommended: it stops by
   itself after its writer's last cycle, since it serves nothing true.
2. The signal the hub reads on: A) the subscription stays the only signal. Once the watcher is
   sure to reach the hub's server, a watcher that runs is a subscriber. B) also read the forge
   while the seat holder's watcher lock (`chantier/watch-<project>/<session>.lock`) is held, even
   with no subscription. B is what the intent first asked for, but it makes the hub read the
   watcher locks and changes AGENTS.md's hub rule. Recommended: A, given the cause found.
