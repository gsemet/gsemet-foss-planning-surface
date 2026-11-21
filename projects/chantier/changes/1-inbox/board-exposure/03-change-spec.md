# The board stays on this machine unless asked, with a key you can rotate

From the audit of 2026-11-21 (high, confirmed): `chantier board` listens on `0.0.0.0` by default,
in plain HTTP, with a key that never expires, carried in the URL and then in a one-year cookie.
Whoever reads the key on the local network can rewrite a specification and move it to `3-ready`,
which Drivers then run with their push rights. The key is printed at each `chantier board` start,
so it sits in 3 local transcripts today.

## Goal

In the user's words: the board is not exposed to the network unless the user asks; its key can be
revoked; reaching the board from the phone on the local network stays possible, as a conscious
choice.

## Decisions carried (02-answers.md)

1. **Default address (board-exposure-Q1, A).** The board listens on `127.0.0.1` by default. It
   listens on the local network only on the user's ask: `board.host` in `chantier.yaml`, or
   `--host`. When it listens beyond this machine, it says so.
2. **The key's life (board-exposure-Q2, A).** The key stays stable across restarts. A command
   changes it: `chantier board --new-key`, which invalidates the old URL. The key is rotated once
   now (it sits in 3 transcripts). The cookie lasts 30 days instead of a year.
3. **The key in the sessions' output (board-exposure-Q3, B).** The full URL, key included, keeps
   being printed; the protection is the rotation (decision 2).
4. **Grilled enough (board-exposure-Q4, A).** Specified now.

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
  (`playbook/layers.py:load_board`, keys checked by `playbook/config.py:BOARD_KEYS`).
- A board bound to a non-loopback address prints, at its start, the line
  `board: listens on the local network (<host>); the link holds its key: give it to the user only,
  plain HTTP` (`board/command.py:BEYOND`, from `_announce`), and, when it listens on every address,
  the second link `on this machine: http://127.0.0.1:<port>/?k=<key>` (`address.local_url`).

So decision 2's command and its invalidation need no new code; this CR changes the default, the
cookie's life, the "already running" lines, the texts that describe the default, and proves the
rotation in the scenario.

## What changes

### CLI

- `skills/chantier/scripts/cli/src/chantier/board/address.py`: `DEFAULT_HOST` becomes
  `"127.0.0.1"` (port stays 8765). `settings()` keeps its order: the option, else `chantier.yaml`'s
  `board.host`, else the default. `EVERYWHERE`, `reachable`, `local_url` and `_loopback_of` are
  unchanged: they still serve a board configured on `0.0.0.0` or `::`.
- `skills/chantier/scripts/cli/src/chantier/board/key.py`: the cookie's `Max-Age` becomes 30 days
  (`30 * 24 * 3600` = 2592000 s); rename the constant from `YEAR_S` to a name that says what it is
  (for instance `COOKIE_MAX_AGE_S`). `set_cookie` keeps `Path=/; HttpOnly; SameSite=Strict` and
  adds nothing else. A cookie already set with a one-year life holds the old key and stops working
  at the rotation (decision 2).
- `skills/chantier/scripts/cli/src/chantier/board/command.py`:
  - `_announce` is unchanged: on a loopback address it prints the one `board on <URL> over <folder>`
    line; beyond it, the `on this machine:` line when it applies and the `BEYOND` line.
  - The "already running" path of `board()` (the `there` branch) also says so when the board found
    listens beyond this machine: after `board already running at <URL>` and the optional
    `on this machine:` line, it appends the same `BEYOND` text, with the host from the record
    (`run["host"]`) or the configured host that answered, when `is_loopback` is false. The order of
    lines matches `_announce`'s, so the session-start card reads both alike.
  - The `BEYOND` text stays word for word (the scenario and the session-start card match on its
    start `board: listens on the local network (`).
- `skills/chantier/scripts/cli/src/chantier/declare/board.py`:
  - `--host` help: `the address to listen on (default: chantier.yaml's board.host, else
    127.0.0.1, this machine only; 0.0.0.0 or this machine's address on the network opens it to the
    local network)`.
  - `HELP`: `serve the board's API and the web client (or another UI: --ui) on this machine (on the
    local network with --host or board.host), behind a key`.
  - `--new-key` help stays (`replace the board's key: the old link stops working`).
- The full URL with its key keeps being printed by every start, by `board already running at`, and
  in the refusals that name a running board (`_held_by`, `_another_version`): nothing changes there
  (decision 3).

### Cards (both hosts read the same cards; no agent file changes)

- `skills/chantier/references/chief-of-staff.md`, the intent row "board on my phone", "where is the
  board?" (line 47): the default is this machine only. Replace "on the user's word, to keep the
  board on this machine only, `board.host: 127.0.0.1` in `chantier.yaml`" with: on the user's word,
  to reach it from the phone or another device on the local network, `board.host: 0.0.0.0` (or this
  machine's address on that network) in `chantier.yaml`, or `--host` for one start, then the board
  started again (stop the running one by the host's means, then `$CHANTIER board --seat <id>`).
  Add to the same row, or as its own row, "a new board key", "the board's link leaked": on the
  user's word, `$CHANTIER board --seat <id> --new-key`; the old link and the open pages stop
  working; give the user the new link.
- Same card, the tips' "board on my phone" example (around line 1470): the same inversion (on the
  user's word, `board.host` opens the board to the local network).
- `skills/chantier/references/session-start.md`, **The board** (around lines 70-90): the board
  listens on this machine only unless `board.host` or `--host` says otherwise; a phone reaches it
  only after the user asked for it. The `board already running at <URL>` bullet also names the
  `board: listens on the local network ...` line, which now may follow it.
- `skills/chantier/references/hosts/claude-code.md`, the row "The remote board (`chantier board`)"
  (line 685): "yes, from any device on the local network, through the link, once `board.host` (or
  `--host`) opens it to the local network". `hosts/copilot.md` holds no such row: unchanged.

### Docs

- `docs/web-board.md`:
  - The intro (line 4): "for this machine, and for any device on your network when you open it to
    the network".
  - **The link**: the second line `on this machine:` is printed "when the board listens on every
    address (`board.host: 0.0.0.0`)", not "(the default)". Say the cookie lasts 30 days, and that
    `chantier board --new-key` replaces the key while the board runs: the old link, the cookies and
    the open pages stop working at once.
  - **The local network**: by default the board listens on `127.0.0.1`, this machine only. To reach
    it from the phone, set `board.host` (or pass `--host`); the board then prints
    `board: listens on the local network (<host>) ...`. Plain HTTP: keep it off networks you do not
    trust; the Windows firewall prompt appears at the first start on a network address only.
  - **Keeping it on the machine** becomes **Opening it to the local network**, with the example
    `host: 0.0.0.0   # the local network; default 127.0.0.1, this machine only`.
- `docs/boards.md` line 3: "served by `chantier board` on this machine, or to any device on the
  local network when you open it".
- `docs/agents-and-models.md` line 101: unchanged (it names the keys, not the default).
- `CONTRIBUTING.md` line 99 and `AGENTS.md`'s board bullet ("for the user on this machine and the
  local network") stay true (the local network is still served, on the user's ask): unchanged.
- The web client (`clients/web/`) is not touched: its `DESIGN.md` needs no change. The Costs page's
  "Copy as image" already works on `127.0.0.1`.

### Rollout (no code)

- **The rotation now (decision 2).** The key is rotated once with `board --new-key`, by the Chief of
  Staff on the user's word, and the user gets the new link. Timing: see open question 1.
- **The phone today.** The surface (`gsemet-foss-planning-surface`) has no `chantier.yaml` at its
  root nor in `projects/chantier/`. Once this CR is merged and the board restarted on the new
  version, the board listens on `127.0.0.1` and the phone loses it. The phone's access comes back
  only with `board.host` set (or `--host` at each start), and only on the user's word, by the Chief
  of Staff. Where and how: open question 2.

## Out of scope

- TLS, and the cookie's `Secure` flag: the board stays plain HTTP (a `Secure` cookie is not sent
  over plain HTTP from a phone, which would break the LAN case). The audit names the missing
  `Secure`; the answers did not take it up: open question 3.
- Hiding or shortening the key in the printed lines and in the transcripts (decision 3, B).
- An expiry of the key itself, or any automatic rotation: the key is stable until `--new-key`.
- The board's Configuration page and `config.put`: they edit the limits and the roles only, not
  `board.host` (AGENTS.md); unchanged.
- Cleaning the 3 transcripts that hold the current key: the rotation makes them harmless.

## Host and default matrix (CLI only; the agent host plays no part)

- No `--host`, no `board.host`: listens on `127.0.0.1`; prints one line `board on
  http://127.0.0.1:<port>/?k=<key> over ...`; no `on this machine:` line, no `board: listens on the
  local network` line.
- `board.host: 0.0.0.0` in `chantier.yaml`, no option: listens on every address; the link on this
  machine's network address, then `on this machine: http://127.0.0.1:<port>/?k=...`, then the
  `board: listens on the local network (0.0.0.0) ...` line.
- `board.host: 127.0.0.1` set explicitly: same as the default.
- `--host 0.0.0.0` with `board.host: 127.0.0.1`: the option wins; the three lines of the network
  case.
- `--host <this machine's LAN address>`: the link on that address and the `board: listens on the
  local network (<address>)` line; no `on this machine:` line (it is not an every-address bind).
- A second `board --seat <id>` while a network board runs: `board already running at <URL>`, the
  `on this machine:` line when it applies, then the `board: listens on the local network` line.
- Windows, Linux, macOS: the same; the Windows firewall prompt comes only with a non-loopback bind.

## Evidence

### Tests (`skills/chantier/scripts/cli/tests/`, in-process, few and parametrized)

- `test_playbook_layers.py::test_the_light_readers_see_the_board_and_long_gate_keys_of_any_layer`:
  its assertion `settings(repo, None, None) == ("0.0.0.0", PORT)` becomes `("127.0.0.1", PORT)`
  (a `board.port` alone keeps the default host).
- One parametrized test on `address.settings` (or an existing one extended): no option and no
  config gives `("127.0.0.1", 8765)`; `board.host: 0.0.0.0` gives `0.0.0.0`; `--host 0.0.0.0`
  wins over `board.host: 127.0.0.1`. It reads `DEFAULT_HOST` through `settings`, from the code as
  it ships.
- The cookie: `keys.set_cookie("k")` holds `Max-Age=2592000` and still `HttpOnly` and
  `SameSite=Strict`; and the `?k=` exchange's `303` (`guard.exchange`) carries that header, through
  the routes, as `test_server_api.py` already calls them.
- The "already running" lines: with a recorded board on `0.0.0.0` that answers (the probe
  monkeypatched as `test_board_running.py` does), `board --seat s` prints `board already running
  at`, then `on this machine:`, then the line starting `board: listens on the local network
  (0.0.0.0)`; with a recorded board on `127.0.0.1`, the one line only.
- The existing `--new-key` tests (`test_board_running.py::test_new_key_keeps_the_running_record_and_
  the_exit_removes_only_its_own`, `test_server_api_ws.py`'s key change closing a socket) stay
  green, unchanged.
- `just test` stays within its time budget (AGENTS.md).

### Scenario (`scenario/run_scenario.py`, the board steps near step 10)

- New check: `board --port 0` with no `--host` and no `chantier.yaml` prints a first line
  starting `board on http://127.0.0.1:` whose link opens (`Link(head).ok`), and the board's
  recorded host in `server.json` is `127.0.0.1`.
- Step 10 (`--host 0.0.0.0`) stays as it is: the network case still prints its warning line.
- New check, the revocation: with a board running, a second `chantier board --new-key` prints
  `board already running at <URL>` with a key different from the first; the first link's `?k=`
  gets `401`, the new link's gets the `303` with `Set-Cookie` holding `Max-Age=2592000`.
- `scenario/README.md` lists the new checks where it lists the board's.

### Gates

- `just check` and `just eval-dry-run` in the worktree (a change under the CLI's `src/`), and the
  pipeline's `just scenario (ubuntu-latest)` green at the PR's head (a change to the CLI and the
  cards). No `hooks/` or `types/` change, so no `just mod`.

## Open questions for the user

1. **When to rotate.** `--new-key` already exists today: rotate at once, with the current version
   (the phone keeps working, with a new link), or at the first board start of the merged version
   (the board must be restarted then anyway)?
2. **The phone after the merge.** The surface holds no `chantier.yaml`. To keep the phone, which
   do you want: `board.host: 0.0.0.0` in the surface's root `chantier.yaml` (pushed by the writer:
   every machine that runs a board on this surface then opens it to its local network), the same in
   `projects/chantier/chantier.yaml` (also pushed), or no file and the Chief of Staff passing
   `--host 0.0.0.0` on your word at each session's start? Or this machine's LAN address rather than
   `0.0.0.0`?
3. **The cookie's `Secure` flag**, named by the audit: leave it out (the board stays plain HTTP,
   and a `Secure` cookie would not reach a phone over plain HTTP), as this spec says, or file it as
   its own inbox item with TLS?
