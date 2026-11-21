# The board stays on this machine unless asked, with a key you can rotate

From the audit of 2026-11-21 (high, confirmed): `chantier board` listens on `0.0.0.0` by default,
in plain HTTP, with a key that never expires, carried in the URL and then in a one-year cookie.
Whoever reads the key on the local network can rewrite a specification and move it to `3-ready`,
which Drivers then run with their push rights. The key was printed at each `chantier board` start,
so it sat in 3 local transcripts (rotated on 2026-11-21, see Rollout).

## Goal

In the user's words: the board is not exposed to the network unless the user asks; its key can be
revoked; reaching the board from the phone on the local network stays possible, as a conscious
choice, and keeps working when the machine's address changes ("Met l'ip dynamiquement").

## Decisions carried (02-answers.md)

1. **Default address (board-exposure-Q1, A).** The board listens on `127.0.0.1` by default. It
   listens on the local network only on the user's ask: a setting in `chantier.yaml`, or `--host`.
   When it listens beyond this machine, it says so.
2. **The key's life (board-exposure-Q2, A).** The key stays stable across restarts. A command
   changes it: `chantier board --new-key`, which invalidates the old URL. The key is rotated once
   (it sat in 3 transcripts): done, see Rollout. The cookie lasts 30 days instead of a year.
3. **The key in the sessions' output (board-exposure-Q3, B).** The full URL, key included, keeps
   being printed; the protection is the rotation (decision 2).
4. **Grilled enough (board-exposure-Q4, A).** Specified.
5. **When to rotate (board-exposure-Q5, A).** Now, on the current version: the Chief of Staff
   stopped the board, started it again with `--new-key` and gave the user the new link. Recorded
   in Rollout as done; it is not part of this CR's work.
6. **The network setting holds no fixed address (board-exposure-Q6).** The user's words: "Met l'ip
   dynamiquement". The `chantier.yaml` setting that opens the board to the network names no
   address: at each start, the board finds this machine's local network address and names it in
   its link (decision 12 says where it listens). So a shared `chantier.yaml` never breaks another machine's board, and a DHCP change is
   followed at the next start. Opening stays the user's choice (decision 1). A fixed address only
   with `--host`, for one start.
7. **Where the board says it is open to the network (board-exposure-Q7, A).** In its start lines,
   which the Chief of Staff passes on; the web client does not change.
8. **The cookie's `Secure` flag (board-exposure-Q8, A).** Out of this CR, and no inbox item for
   now (see Out of scope).
9. **Grilled enough (board-exposure-Q9, A).** The spec revised from Q5 to Q8 and the critic's
   fixes 4 and 5, then checked again by the critic for Q6; destination the next batch (`3-ready`).
10. **The network setting's form and place (board-exposure-Q10, A).** A word under the existing
    key: `board.host: network`. A fixed address in `chantier.yaml` is refused by the config check,
    with a message pointing to `--host`. For this surface, it goes in
    `projects/chantier/chantier.yaml`, for the chantier project only.
11. **No network at start (board-exposure-Q11, A).** With `board.host: network` and no local
    network address found at start, the board starts on `127.0.0.1` and says plainly it is not
    open to the network: `board: no local network address found; on this machine only`. A restart
    opens it once the network is back.
12. **Where the board listens with `board.host: network` (board-exposure-Q12, A).** On every
    address (`0.0.0.0`). The main link names the address found at this start, and the
    `on this machine: http://127.0.0.1:<port>/?k=<key>` link is kept, so the Costs page's "Copy as
    image" works on this machine and a VPN does not hide the local network. Nothing fixed sits in
    `chantier.yaml`. Decision 11 is unchanged: with no address found, the board binds `127.0.0.1`
    and prints `NO_NETWORK`.
13. **The phone after the merge (board-exposure-Q13, A).** When it restarts the board on the
    merged version, the Chief of Staff writes `board.host: network` in
    `projects/chantier/chantier.yaml`; Q6 and Q10 count as the user's word (see Rollout).

## What exists already (read, not to rebuild)

- `--new-key` exists (`declare/board.py`, `board/command.py` passes `args.new_key` to
  `board/key.py:load_or_create`). It writes a new key into `<git common dir>/chantier/server.json`
  and keeps the `server` and `hub` entries.
- A running board reads the key again when that file changes (`board/key.py:KeyFile`), so a
  `board --new-key` run while a board serves takes effect at once: the old link and old cookies get
  `401` (`guard.NEEDS_KEY`), and the push loop closes every WebSocket still holding the old key with
  `4401` (`board/api/push.py:_close_stale_keys`). The second `board` process then finds the running
  board with the new key (`_recorded`) and prints `board already running at <new URL>`.
- `board.host` and `board.port` are read from the merged `chantier.yaml` layers
  (`playbook/layers.py:load_board`, keys checked by `playbook/config.py:BOARD_KEYS` and the
  `board` checks around `config.py:273-285`).
- `board/address.py:_default_route_address()` already finds this machine's address on the network
  of its default route (a UDP `connect` that sends nothing), and returns `127.0.0.1` when the
  machine has no network. Today only `reachable()` uses it, for the link of an every-address bind
  (`url()` calls `reachable()`), so a `0.0.0.0` bind already prints its link on the found address.
- A board bound to a non-loopback address prints, at its start, the line
  `board: listens on the local network (<host>); the link holds its key: give it to the user only,
  plain HTTP` (`board/command.py:BEYOND`, from `_announce`), and, when it listens on every address,
  the second link `on this machine: http://127.0.0.1:<port>/?k=<key>` (`address.local_url`).

So decision 2's command and its invalidation need no new code, and an every-address bind already
prints the link and the lines decision 12 asks for; this CR changes the default, adds
`board.host: network` (an every-address bind when an address is found at this start, `127.0.0.1`
and the `NO_NETWORK` line when none is), the cookie's life, the "already
running" lines, the texts that describe the default, and proves the rotation in the scenario.

## What changes

### CLI

- `skills/chantier/scripts/cli/src/chantier/board/address.py`:
  - `DEFAULT_HOST` becomes `"127.0.0.1"` (port stays 8765).
  - `settings()` keeps its order: the option, else `chantier.yaml`'s `board.host`, else the
    default. When `chantier.yaml`'s `board.host` is `network` (decision 10), it calls
    `_default_route_address()` at this start: when that call finds a non-loopback address, it
    returns the bind host `0.0.0.0`, every address (decision 12); when it finds none (it gives
    `127.0.0.1`), it returns `127.0.0.1` and the board's start says so (decision 11, see
    `command.py` below). `settings()` lets its caller tell that case apart (for instance a third
    returned value), so the `NO_NETWORK` line is printed only for `network` without an address,
    never for the default nor for `--host 127.0.0.1`.
  - The bind host `0.0.0.0` is what `server.json` records (`state.write_server`), as for a
    `--host 0.0.0.0` start; no found address is stored anywhere, so each start finds it again.
  - `--host` keeps taking any address, `0.0.0.0` and `::` included, for this one start.
  - `EVERYWHERE`, `reachable`, `url`, `local_url`, `_loopback_of` and `loopback_base` are
    unchanged: with `network` and an address found, the board is a `0.0.0.0` bind, so `url()`
    names the found address in the main link (through `reachable()`), `local_url()` gives the
    `127.0.0.1` link, and this machine's own clients reach the board on `127.0.0.1`
    (`_loopback_of`).
- `skills/chantier/scripts/cli/src/chantier/playbook/config.py`: `BOARD_KEYS` stays
  `("host", "port")`. In `_board` (lines 270-291), the `host` key accepts the one word `network`
  and refuses any other value, every address included (`127.0.0.1` and `0.0.0.0` too), and also
  an empty value, a value with whitespace or a non-scalar one, all with the same message pointing
  to `--host`, for instance `board: "host" is network (this machine's local network address,
  found at each start); a fixed address goes in --host, for one start` (decisions 6 and 10). So
  the shared "one address with no whitespace" branch (lines 280-284) no longer applies to `host`;
  the `port` branch, its whitespace check and its "integer from 1 to 65535" message stay as they
  are. A reset (`is_reset`) of `host` keeps working. `board` and `validate` report the refusal
  like the other `board` problems.
- `skills/chantier/scripts/cli/src/chantier/board/key.py`: the cookie's `Max-Age` becomes 30 days
  (`30 * 24 * 3600` = 2592000 s); rename the constant from `YEAR_S` to a name that says what it is
  (for instance `COOKIE_MAX_AGE_S`). `set_cookie` keeps `Path=/; HttpOnly; SameSite=Strict` and
  adds nothing else. A cookie set with a one-year life before the rotation holds the old key and
  already stopped working (decision 5).
- `skills/chantier/scripts/cli/src/chantier/board/command.py`:
  - `_announce` is unchanged: on a loopback address it prints the one `board on <URL> over <folder>`
    line; beyond it, the `on this machine:` line when it applies and the `BEYOND` line. With
    `board.host: network` and an address found, the start prints, as a `--host 0.0.0.0` start
    does: `board on http://<the address found at this start>:<port>/?k=<key> over <folder>`, then
    `on this machine: http://127.0.0.1:<port>/?k=<key>`, then
    `board: listens on the local network (0.0.0.0); the link holds its key: give it to the user
    only, plain HTTP` (the `BEYOND` text names the bind host, as today).
  - New constant `NO_NETWORK = "board: no local network address found; on this machine only"`,
    word for word (decision 11). With `board.host: network` and no address found, the start prints
    the one `board on http://127.0.0.1:<port>/?k=<key> over <folder>` line, then `NO_NETWORK`, and
    no `BEYOND` line. Nothing retries while the board runs: the next start opens it once the
    network is back.
  - The "already running" path of `board()` (the `there` branch) also says so when the board found
    listens beyond this machine: after `board already running at <URL>` and the optional
    `on this machine:` line, it appends the same `BEYOND` text, with the host of the board found
    (`there[0]`: the record's `run["host"]`, or the configured host that answered), when
    `is_loopback` is false. The order of lines matches `_announce`'s, so the session-start card
    reads both alike.
  - The `BEYOND` text stays word for word (the scenario and the session-start card match on its
    start `board: listens on the local network (`). These start lines are the only place the board
    says it is open to the network, or that it could not be (decision 7).
- `skills/chantier/scripts/cli/src/chantier/declare/board.py`:
  - `--host` help: `the address to listen on, for this start (default: chantier.yaml's
    board.host: network, this machine's local network address found at each start, else
    127.0.0.1, this machine only; 0.0.0.0 or an address of this machine on the network opens it to
    the local network)`.
  - `HELP`: `serve the board's API and the web client (or another UI: --ui) on this machine (on the
    local network with --host or chantier.yaml's board.host: network), behind a key`.
  - `--new-key` help stays (`replace the board's key: the old link stops working`).
- The full URL with its key keeps being printed by every start, by `board already running at`, and
  in the refusals that name a running board (`_held_by`, `_another_version`): nothing changes there
  (decision 3).

### Cards (both hosts read the same cards; no agent file changes)

- `skills/chantier/references/chief-of-staff.md`, the intent row "board on my phone", "where is the
  board?" (line 47): the default is this machine only. Replace "on the user's word, to keep the
  board on this machine only, `board.host: 127.0.0.1` in `chantier.yaml`" with: on the user's word,
  to reach it from the phone or another device on the local network, `board.host: network` in
  `chantier.yaml` (the board finds this machine's address at each start), or `--host` for one
  start, then the board started again (stop the running one by the host's means, then
  `$CHANTIER board --seat <id>`); pass on the `board: listens on the local network` line, or the
  `board: no local network address found; on this machine only` line (then: start it again once
  the network is back). Add to the same row, or as its own row, "a new board key", "the board's
  link leaked": on the user's word, `$CHANTIER board --seat <id> --new-key`; the old link and the
  open pages stop working; give the user the new link.
- Same card, the tips' "board on my phone" example (lines 1469-1470): the same inversion (on the
  user's word, `board.host: network` opens the board to the local network).
- `skills/chantier/references/session-start.md`, **The board** (around lines 70-90): the board
  listens on this machine only unless `board.host: network` or `--host` says otherwise; a phone
  reaches it only after the user asked for it. The `board already running at <URL>` bullet also
  names the `board: listens on the local network ...` line, which now may follow it, and the
  Chief of Staff passes that line on. A start with `network` and no network prints
  `board: no local network address found; on this machine only`, which the Chief of Staff passes
  on too.
- `skills/chantier/references/hosts/claude-code.md`, the row "The remote board (`chantier board`)"
  (line 685): "yes, from any device on the local network, through the link, once
  `board.host: network` (or `--host`) opens it to the local network". `hosts/copilot.md` holds no
  such row: unchanged.

### Docs

- `README.md` lines 231-232, **The CR board**: "On any device" becomes: on this machine by default,
  and on the phone or any device of the local network once you open it to the network;
  "it lets you triage the backlog from your phone" keeps, conditioned on that opening.
- `docs/web-board.md`:
  - The intro (line 4): "for this machine, and for any device on your network when you open it to
    the network".
  - Line 8: "To start it, keep it on the machine and stop it" becomes "To start it, open it to the
    local network and stop it".
  - **The link**: the second line `on this machine:` is printed "when the board listens on every
    address (`board.host: network`, or `--host 0.0.0.0`)", not "(the default)". Say the cookie lasts 30 days, and that
    `chantier board --new-key` replaces the key while the board runs: the old link, the cookies and
    the open pages stop working at once.
  - **The local network**: by default the board listens on `127.0.0.1`, this machine only. To reach
    it from the phone, set `board.host: network` in `chantier.yaml`: the board listens on every
    address, finds this machine's local network address at each start and names it in its link,
    and keeps the `on this machine:` link for this machine (a shared `chantier.yaml` suits every
    machine, a new address from DHCP is taken at the next start, and a VPN does not hide the local
    network); or pass
    `--host <address>` for one start (a fixed address in `chantier.yaml` is refused). The board
    then prints `board: listens on the local network (...) ...`. With no network at start,
    it listens on this machine only and prints `board: no local network address found; on this
    machine only`; start it again once the network is back. Plain HTTP: keep it off networks you
    do not trust; the Windows firewall prompt appears at the first start on a network address
    only.
  - **Keeping it on the machine** becomes **Opening it to the local network**, with the example
    `host: network   # this machine's local network address, found at each start; default: this
    machine only` under `board:`.
- `docs/boards.md` line 3: "served by `chantier board` on this machine, or to any device on the
  local network when you open it".
- `docs/agents-and-models.md` line 101: unchanged (it names the keys, `host` and `port`, not the
  default; the keys do not change).
- `CONTRIBUTING.md` line 99 and `AGENTS.md`'s board bullet ("for the user on this machine and the
  local network") stay true (the local network is still served, on the user's ask): unchanged.
- The web client (`clients/web/`) is not touched (decision 7): its `DESIGN.md` needs no change.
  The Costs page's "Copy as image" works on this machine in every case: by default the board is on
  `127.0.0.1`; with `board.host: network` (or `--host 0.0.0.0`) it listens on every address and
  prints the `on this machine: http://127.0.0.1:...` link, which is also where the button's
  tooltip sends a page opened on the network address (decision 12). Only a `--host` on one LAN
  address leaves no `127.0.0.1` link, as today.
- **Overlap with `2-backlog/P3/docs-sphinx-rtd`.** That CR moves `docs/web-board.md` to
  `reference/web-board.md` and adds a section "On a phone". That section must say that the phone
  first needs the board opened to the network (`board.host: network` or `--host`). Whichever of
  the two CRs merges second rebases onto the other's `web-board.md` (moved or edited) and carries
  this CR's texts into it. No `depends.json` entry: a shared file is not a dependency.

### Rollout (no code)

- **The rotation (decision 5): done on 2026-11-21**, with the current version: the Chief of Staff
  stopped the board, started it again with `board --new-key` and gave the user the new link. The
  key in the 3 transcripts no longer opens the board. Not part of this CR.
- **The phone after the merge (decision 13).** The surface (`gsemet-foss-planning-surface`) has
  no `chantier.yaml` at its root nor in `projects/chantier/`. When it restarts the board on the
  merged version, the Chief of Staff writes `board.host: network` in
  `projects/chantier/chantier.yaml` (decision 10, the chantier project only), with no further
  question: Q6 and Q10 count as the user's word. The board then keeps the phone, on the address
  found at that start. Because the setting names no address, the file pushed by the surface's
  writer works on every machine; it opens each machine's board that reads it to its own local
  network, which the user chose knowingly. This is a step of the rollout, not of the CR's code.

## Out of scope

- TLS, and the cookie's `Secure` flag (decision 8): the board stays plain HTTP, and a `Secure`
  cookie is not sent over plain HTTP, so it would not reach a phone on a local network address and
  would break the case this CR keeps. No inbox item for now.
- Hiding or shortening the key in the printed lines and in the transcripts (decision 3, B).
- An expiry of the key itself, or any automatic rotation: the key is stable until `--new-key`.
- Following an address change, or the network coming back, while the board runs: the address is
  found at each start (decisions 6, 11 and 12); a board started before the change keeps its bind
  and the link it printed until it is started again.
- Telling the user in the web client that the board is open to the network (decision 7).
- The board's Configuration page and `config.put`: they edit the limits and the roles only, not
  the board's address (AGENTS.md); unchanged.
- Cleaning the 3 transcripts that held the old key: the rotation made them harmless.
- The rotation itself: done (decision 5).

## Host and default matrix (CLI only; the agent host plays no part)

- No `--host`, no `board.host`: listens on `127.0.0.1`; prints one line `board on
  http://127.0.0.1:<port>/?k=<key> over ...`; no `on this machine:` line, no `board: listens on the
  local network` line, no `board: no local network address found` line.
- `board.host: network` in `chantier.yaml`, no option, the machine on a network: listens on every
  address (`0.0.0.0`); the link on the address `_default_route_address()` finds at this start,
  then `on this machine: http://127.0.0.1:<port>/?k=<key>`, then the
  `board: listens on the local network (0.0.0.0) ...` line. `server.json` records `0.0.0.0`.
- The same setting, the machine's address changed since the last start: the link on the new
  address, same lines.
- The same setting, the machine with no network (no default route): listens on `127.0.0.1`;
  prints the one `board on http://127.0.0.1:<port>/?k=<key> over ...` line, then
  `board: no local network address found; on this machine only`; no `BEYOND` line. A restart with
  the network back gives the case above.
- `--host 0.0.0.0` with `board.host: network` or none: the option wins; the same three lines as
  `board.host: network` with an address found.
- `--host 127.0.0.1` with `board.host: network`: the option wins; the one-line loopback case.
- `--host <this machine's LAN address>`: the link on that address and the `board: listens on the
  local network (<address>)` line; no `on this machine:` line.
- Any `board.host` other than `network` in `chantier.yaml` (`127.0.0.1`, `0.0.0.0`, a LAN
  address, an empty value, a value with whitespace): refused, by `board` and `validate`, with the
  message pointing to `--host`.
- A second `board --seat <id>` while a `board.host: network` board runs: `board already running at
  <URL on the found address>`, `on this machine: http://127.0.0.1:...`, then the
  `board: listens on the local network (0.0.0.0)` line.
- Windows, Linux, macOS: the same; the Windows firewall prompt comes only with a non-loopback bind.

## Evidence

### Tests (`skills/chantier/scripts/cli/tests/`, in-process, few and parametrized)

- `test_playbook_layers.py::test_the_light_readers_see_the_board_and_long_gate_keys_of_any_layer`:
  its only change is the assertion at line 221, `settings(repo, None, None) == ("0.0.0.0", PORT)`,
  which becomes `("127.0.0.1", PORT)` (a `board.port` alone keeps the default host).
- One parametrized test on `address.settings` (or an existing one extended), reading
  `DEFAULT_HOST` through `settings`, from the code as it ships: no option and no config gives
  `("127.0.0.1", 8765)`; `board.host: network` with `_default_route_address` monkeypatched to a
  LAN address gives the bind host `0.0.0.0`, and `url()` on it names that address (monkeypatched
  to two different addresses in two calls, proving the address is found at each start, not
  stored); `board.host: network` with `_default_route_address` monkeypatched to return
  `127.0.0.1` gives `127.0.0.1` and the no-network case; `--host 0.0.0.0` wins over
  `board.host: network`; `--host 127.0.0.1` wins over it too, and is not the no-network case.
- The config check, parametrized: `board.host: 127.0.0.1`, `0.0.0.0`, a LAN address, an empty
  value and a value with whitespace are each refused with the same message pointing to `--host`
  (prepared `chantier.yaml` files, refusal cases), paired with `board.host: network` accepted; a
  `board.port: "8 8"` keeps the port's own message.
- The start lines with `board.host: network` and an address found (`_default_route_address`
  monkeypatched to a LAN address, the bind on `0.0.0.0` with port 0): the link on that address,
  then `on this machine: http://127.0.0.1:`, then the line starting
  `board: listens on the local network (0.0.0.0)`; no `NO_NETWORK` line.
- The start lines with no network: `board` with `board.host: network` and
  `_default_route_address` monkeypatched to `127.0.0.1` prints the `board on http://127.0.0.1:`
  line, then exactly `board: no local network address found; on this machine only`, and no line
  starting `board: listens on the local network`; the default (no `board.host`) prints no
  `NO_NETWORK` line.
- The cookie: `keys.set_cookie("k")` holds `Max-Age=2592000` and still `HttpOnly` and
  `SameSite=Strict`; and the `?k=` exchange's `303` (`guard.exchange`) carries that header, through
  the routes, as `test_server_api.py` already calls them.
- The "already running" lines: with a recorded board on `0.0.0.0` that answers (the probe
  monkeypatched as `test_board_running.py` does), `board --seat s` prints `board already running
  at`, then `on this machine:`, then the line starting `board: listens on the local network
  (0.0.0.0)`; with a recorded board on a LAN address, the first and the last line; with a recorded
  board on `127.0.0.1`, the one line only.
- The existing `--new-key` tests (`test_board_running.py::test_new_key_keeps_the_running_record_and_
  the_exit_removes_only_its_own`, `test_server_api_ws.py`'s key change closing a socket) stay
  green, unchanged.
- `just test` stays within its time budget (AGENTS.md).

### Scenario (`scenario/run_scenario.py`, the board steps 10 and 11, from line 3108)

- New check: `board --port 0` with no `--host` and no `chantier.yaml` prints a first line
  starting `board on http://127.0.0.1:` whose link opens (`Link(head).ok`), and the board's
  recorded host in `server.json` is `127.0.0.1`.
- New check: with `board.host: network` in the scenario surface's `chantier.yaml` and `--port 0`,
  it accepts either outcome, as the runner's network decides: (a) the first line's link is on a
  non-loopback address and opens, `server.json` records the host `0.0.0.0`, the next line starts
  `on this machine: http://127.0.0.1:` and its link opens too, and the line after starts
  `board: listens on the local network (`; or (b) the first line's link is on `127.0.0.1` and
  opens, followed by exactly the `NO_NETWORK` line. (The no-network case is proved for certain by
  the tests.)
- Step 11 (`# 11. chantier.yaml`, line 3124): its fixtures stop setting a fixed host, now refused.
  Line 3128 drops the `host:` line (`board:\n  port: {other}\n`; the check that the board starts
  on `http://127.0.0.1:{other}` still holds, from the default host). Line 3152 drops it too (the
  check matches the "both present" line). Lines 3138 and 3148 use `host: network` instead of
  `host: 127.0.0.1`, so the faulty key stays on line 3 and the `chantier.yaml:3: board: ` and
  `chantier.yml:3: board: ` matches still hold. A new check in that step: `board.host: 127.0.0.1`
  in `chantier.yaml` is refused by `playbook` and by `board` (exit 2), with the message pointing
  to `--host`.
- Step 10 (`--host 0.0.0.0`) stays as it is: the network case still prints its warning line.
- New check, the revocation: with a board running, a second `chantier board --new-key` prints
  `board already running at <URL>` with a key different from the first; the first link's `?k=`
  gets `401`, the new link's gets the `303` with `Set-Cookie` holding `Max-Age=2592000`.
- `scenario/README.md` lists the new checks where it lists the board's.

### Gates

- `just check` and `just eval-dry-run` in the worktree (a change under the CLI's `src/`), and the
  pipeline's `just scenario (ubuntu-latest)` green at the PR's head (a change to the CLI and the
  cards). No `hooks/` or `types/` change, so no `just mod`.
