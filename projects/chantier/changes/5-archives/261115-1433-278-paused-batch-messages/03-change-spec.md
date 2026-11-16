# Change Specification: commands name a paused batch and the way out

Short name: `paused-msgs`

## Goal

Two refusals seen in batch-18's real eval runs of 2026-11-15 (audits:
`C:/Users/gaeta/Projets/chantier-eval/real-foreman-2026-11-15.audit.md` and
`real-direct-2026-11-15.audit.md`) send the user the wrong way or nowhere:

1. On a paused batch, `chantier cost --explain` and `chantier cost --by cr` refuse with
   `no running batch: run \`chantier open\` first; no batch closed yet` (both runs). The message
   sends the user to open a new batch, while `--batch <n>` was all that was missing.
2. `chantier board` failed in run 2 with a bare `board not started: [WinError 10048] ...` (the
   port was in use: an earlier board still ran). The refusal names neither the port, nor that a
   board may already run there, nor the way out.

After this CR, a consultation of the only paused batch just works, every other refusal names the
paused batch and `--batch`, and a held port names the port, what holds it when chantier can tell,
and the way out (the running board's URL, or `--port`).

## Decisions carried from `02-answers.md`

- The request's scope stands as written: "Pick the only paused batch when there is one, or name
  it and `--batch` in the refusal" for the batch, and "names the port, that a board may already
  run, and the way out (its URL, or `--port`) where one exists" for the board.
- Planned for the next batch (parallel), before the next release.
- Implementation detail is the agents'.

How "pick" and "name" split (this specification's reading of the request's "or", see the open
question): a command that only reads the batch picks the only paused batch; a command that writes
it (some of which set a paused batch running again, `take` and `order qa`) never picks one
silently and names it in its refusal instead.

## What changes

### 1. Batch resolution: `skills/chantier/scripts/cli/src/chantier/core/batch.py`

`resolve_batch(repo, batch)` today: `--batch`, else `CHANTIER_BATCH`, else the only running batch
(`Repo.open_batches()` in `core/repo.py`, which leaves out `status == "paused"`), else
`no running batch: run \`chantier open\` first` + `last_closed_note(repo)`
(`core/batch_records.py`), else `several running batches (...): pass --batch`.

New behaviour, when neither `--batch` nor `CHANTIER_BATCH` is given and no batch runs:

- **A reading command and exactly one paused batch:** the paused batch is used, as if
  `--batch <name>` had been passed. No extra line: `cost`'s first line already starts with the
  batch's name, and `status`'s batch line already says `(paused, cost to date)`.
- **Any other case with one or more paused batches** (a writing command, or several paused
  batches): refused, naming each paused batch and the flag, and keeping the last-closed note, e.g.
  `no running batch; paused: batch-18: pass \`--batch batch-18\`; last closed: batch-17`
  (several: `paused: batch-17, batch-18: pass \`--batch <name>\``). It no longer says
  `run \`chantier open\` first`.
- **No paused batch:** unchanged (`no running batch: run \`chantier open\` first; ...`).
- Exit codes unchanged (the current `no running batch` code; the scenario expects 2 from
  `status`).
- With a running batch, `--batch`, or `CHANTIER_BATCH`: unchanged.

The reading commands, which opt in (for example a keyword argument such as
`resolve_batch(repo, batch, paused=True)`, plus a `Repo` helper beside `open_batches()` listing
the paused ones; the form is the Driver's):

- `cost`, every form (`--by cr`, `--by driver`, `--explain`, `--summary`):
  `commands/cost/command.py`, `cost()`.
- `status` without `--refresh` and without `--stop-heartbeat`: `commands/batch_status.py`,
  `status()`. With either flag `status` writes, and keeps the naming refusal.

Every other caller of `resolve_batch` (`asks`, `agents` for `stack`/`O-k`, `delivery.py`,
`driver.py`, `orders.py`, `orders_merged.py`, `seat.py`, `closing.py`'s `pause`,
`forge_stack.py`, `forge_stack_gh.py`, `rules.py`) does not opt in and gets the naming refusal.
`close` (`_close_target`) and `find_cr_batch` have their own resolution and do not change.

### 2. Board on a held port: `skills/chantier/scripts/cli/src/chantier/board/command.py`

Today `_bind()` turns any `OSError` into `_not_started(e)`: `board not started: <the OS text>`,
exit 4 (`EXIT_EXTERNAL`). `board()` probes first (`_running` via `address.probe`), and a board of
this folder behind this key already answers `board already running at <URL>` (unchanged).

New: when the bind fails because the address is in use (`errno.EADDRINUSE` on POSIX, Windows'
`WSAEADDRINUSE`/10048), the refusal is one line that names the port and host, says what holds it
as far as the probe can tell, and gives the way out:

- A chantier board behind this key, serving another folder (the probe's `/api/board` dict, a
  `served` that is not this folder): `board not started: port 8765 on 0.0.0.0 is held by a
  chantier board over <its served folder>: open <its URL with the key>, or pass --port <n>
  (0: any free port)`.
- A chantier board behind another key (the probe gets the board's `401` with `NEEDS_KEY` from
  `board/guard.py`; `address.probe` learns to tell this from any other answer): `board not
  started: port 8765 on 0.0.0.0 is held by another chantier board (another project's key; its
  session printed its link): pass --port <n> (0: any free port)`.
- Anything else, or nothing answering the probe: `board not started: port 8765 on 0.0.0.0 is in
  use (a board may already run there, or another program): pass --port <n> (0: any free port)`.
- When the port came from `chantier.yaml`'s `board.port` (no `--port` given), the way out also
  names it: `pass --port <n> (0: any free port) or change board.port in chantier.yaml`.

The line keeps its `board not started: ` prefix, stays one line on stderr with nothing on
stdout, and exit 4: the Chief of Staff's handling in `skills/chantier/references/session-start.md`
("`error: board not started: ...`: one line with the reason, then go on") holds unchanged. Any
other bind failure (a bad address, a port refused by the system) keeps today's message. The probe
reuses the existing 2 s timeout of `address._call`; the board still never blocks a session.

### 3. Docs

- `docs/use-cases.md`, the paragraph "Once a batch is paused, `status` and `cost` without
  `--batch` answer `no running batch`: pass `--batch <name>`.": now `status` and `cost` read the
  only paused batch by themselves; a command that would act on a paused batch without `--batch`
  names it and `--batch <name>`.
- `docs/web-board.md`, "When it stops." bullet: add one sentence: a port held by something else
  stops the start with the port named and the way out (the running board's link when it is
  chantier's behind the same key, else `--port`).

No card changes: no role's judgment changes. No agent file, hook or type changes.

## Out of scope

- Picking a paused batch for a command that writes the batch (it would set a paused batch
  running again, or record into it, without the user naming it).
- Picking among several paused batches.
- Other refusals of the board (`check_planning`, a seat not taken, a bad `--host`/`--port`).
- Changing the default port, or retrying another port by itself (that would be a fallback).
- `close`'s own resolution and its messages.

## Evidence

Tests (`skills/chantier/scripts/cli/tests/`, in-process, parametrized, within the `just test`
budget):

- `resolve_batch` on prepared states (in `test_rail_refusals.py` or `test_cli_units.py`), one
  parametrized test: no batch at all (unchanged text); one paused batch with a reading command
  (returns it); one paused batch with a writing command (refusal names it and
  `--batch batch-NN`, no `chantier open`); two paused batches (both named, `--batch <name>`, for a
  reading command too); one running and one paused (the running one, unchanged).
- `test_board.py`: a socket bound and listening on `127.0.0.1:<port>`, then `chantier board
  --host 127.0.0.1 --port <port>`: exit 4, one stderr line starting `board not started: `, naming
  the port and `--port`. A probe answered with the board's `401`/`NEEDS_KEY` is classified as
  another chantier board (unit test of `address.probe`'s classification).

Scenario (`scenario/run_scenario.py`):

- Section "9. Cost", after the pause, with `CHANTIER_BATCH` unset: `cost --by cr` and `cost
  --explain` without `--batch` exit 0 and give the same first lines as with `--batch`; `status`
  without `--batch` exits 0; one writing command without `--batch` (e.g. `asks`) refuses naming
  the paused batch and `--batch <name>`, and its stderr holds no `chantier open`.
- The check "a port held by another program exits 4 with one `board not started` line"
  (around line 1674) also requires the busy port's number and `--port` in that line.
- The end-of-run check "with no running batch, `status` refuses and names the last closed batch"
  (around line 2784, no paused batch left) holds unchanged.

Gates: `just check` on the Driver's machine; the pipeline's `just scenario (ubuntu-latest)` job
green at the PR's head (the CLI changes). No `just mod` (no `hooks/` or `types/` change). No
screenshot (the CR board pane is not touched).

## Open questions for the user

1. The request says "pick the only paused batch when there is one, or name it and `--batch` in
   the refusal". This specification picks it for the reading commands (`cost`, plain `status`)
   and names it in the refusal for every command that writes the batch (`take`, `order`, `pause`,
   `asks`, ...), so that no command sets a paused batch running again without the user naming it.
   Is that split right, or should the reading commands also only name it (never pick)?
