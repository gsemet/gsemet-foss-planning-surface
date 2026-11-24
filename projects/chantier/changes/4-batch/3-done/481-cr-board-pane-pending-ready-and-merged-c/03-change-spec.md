# CR board pane: the batch's CRs by state, board links, services, stats

## Goal

The user looks at the CR board pane (the Claude Code mod, `hooks/register.tsx`) and wants to see
the running batch as it is: its CRs by state (pending, working, ready to merge, merged), so that a
batch whose CRs have all merged does not look empty. In the same CR, the pane also shows the web
board's links when a board runs (the pane is the user's, who holds the key), whether the watcher
and the surface server run (with PID and build), and a few figures of the batch.

Two inbox items merged into this one (board-pane-Q1 A): `intake/request.md` and
`intake-2-this-batch-merged.md`. One CR, one PR, one screenshot.

## What the record shows today (read on 2026-11-24, batch-31)

The planning folder's `STATUS.json` (`status/views.py`, `dashboard_view`) is read correctly by the
pane; nothing is lost in the read. What the user misses comes from what the file holds and how the
pane draws it:

- A batch entry's `crs` lists its active CRs only (`status not in ENDED`): batch-31 has
  `crs_total` 18 and 3 rows. Its 15 merged CRs (in `4-batch/3-done/`) appear only in the global
  `merged` list (capped at `PAST_LIMIT`, mixed with every other batch's), in the "Merged (n of
  total)" section, created folded.
- The batch section groups its rows into "Waiting for you" and "In progress" only; it names no
  state group (a `queued` CR of `1-pending/`, a working CR and a ready CR sit in the same table).
- `3-ready` CRs are in `backlog` (priority `3-ready`), in the folded "Backlog" section.

First step for the Driver: run the pane on the real surface at batch-31 and compare it with
`chantier status`, to confirm this reading. A real read failure found there (a project of the
surface not read, an entry dropped) is fixed in this CR and named in the PR.

## What changes

### 1. `STATUS.json` (the planning folder's index): `status/views.py`

Additions only; `schema` stays 3 (the pane reads an older file without them, as it does for
`phase`, `crs_total` and `spent_at`). `types/index.d.ts` declares each new field, optional.

- Each batch entry gains its merged CRs: `merged`, the batch's CRs whose status is `merged`,
  newest merge first, in the `ChantierPast` shape `_done_rows` already builds (`cr`, `title`,
  `state`, `batch`, `pr`, `cost_usd`, `when` = `merged_at`, `path`). All of the batch's merged
  CRs, uncapped, wherever their folder now is (`3-done/`, or `5-archives/` after `close`).
- Each batch entry gains what the figures need that it does not hold yet: `created` (the batch
  record's `created`) and its count of CRs per status over all its CRs, ended ones included
  (`counts`: `queued`, `working`, `ready`, `blocked`, `merged`, `cancelled`, and any other status
  the record holds, by its own name).
- The index gains `services`, a snapshot of this machine's chantier processes for the planning
  surface, taken when the file is written, with its time (`at`):
  - `server`: `null` when no live `server` entry (`hub/state.py`, `live_entry`), else its `pid`,
    `version`, `source`, `started`, `host`, `port`, and the links without any key: the address
    the user can reach (`board/address.py`, `url(host, port)` with no key) and its `127.0.0.1`
    form when it differs (`local_url`). The `other_build` / `other_version` clause, when the
    server runs another build or version than the writing CLI, as one string (`build_note`), else
    `null`.
  - `hub`: `null` or its `pid`, `version`, `started`, `idle`.
  - `writer`: `null` or its `pid`, `state` and `text`.
  - `watchers`: the session keys that hold a watcher lock of this project now
    (`hub/lock.py`, `watchers`).
  - No key, private or public, ever: the keys stay in `server.json` (AGENTS.md: the surface
    server keeps its two keys in the git folder). A test asserts that the written `STATUS.json`
    holds neither key of the `server.json` it was written beside.
- `STATUS.md` (`status/markdown.py`) and the web board's API (`board/state.py` picks its fields
  from the view one by one) are unchanged.

### 2. The pane: `hooks/register.tsx`

Sections and their default fold (board-pane-Q2 A): the running batch open, the rest folded.

- **The batch section** (open while the batch is not paused, as today) shows its CRs by state, each
  state named: pending (`queued`), working (and blocked), ready to merge (a `ready` CR, its
  `readiness` as today: ready locally, PR in draft, ready to merge), and merged (the batch's new
  `merged` list, with its PR links and costs). An empty state says so in one dim line or is left
  out; a batch whose CRs have all merged shows its merged CRs, never an empty batch. "Waiting for
  you" stays: its count is the header's, and the user acts on it. The exact layout (one table
  with a state column or one table per state, the merged group's own fold) is the Driver's,
  within this: every state of the running batch is visible with the batch section open, with no
  other fold to open.
- **The batch's figures** (board-pane-Q5 A), inside the batch section, from the batch entry
  alone, these three and no other: the CRs per state out of `crs_total` (merged, cancelled
  included), the time since the batch started (`created`), and the spend per merged CR when the
  batch is priced. The cost, budget and spend age stay on the title
  line as today.
- **Backlog** (folded): unchanged rows, `3-ready` first as today; its fold label says how many
  are in `3-ready` so a ready CR is visible folded (for example `Backlog (54, 2 ready)`).
- **Merged** of all batches and **Trashed**: unchanged, folded.
- **Services** (new, folded): the surface server (running or not, PID, version, build when
  `build_note` says another one, address), the hub, the writer's state, and the watcher (running
  for this session, for another session, or not running; the pane knows its own session id,
  `readSessionId`), with the snapshot's age from `services.at` ("as of N min ago"), since the pane
  cannot tell a live process itself. The fold's label carries the one-word state of the server and
  of this session's watcher, so it is read folded.
- **The web board's links** (board-pane-Q4 C), in the Services section, only when
  `services.server` is not null: both links, each named, the private one (reads and acts, the
  `key`) and the public read-only one (the `read_key`). The pane reads both keys from the git
  folder's `chantier/server.json` (the git common dir it already finds with `git rev-parse`; a
  file read, no new process), appends `?k=<key>` to each address of `services.server`, and draws
  them as links. Nothing it reads there is written anywhere. When `server.json` cannot be read or
  holds no key, the links are drawn without a key and one line says so; a file with no
  `read_key` gives no read-only link, as `read_only_lines` does.
- The pane still writes nothing and runs no process but `git rev-parse`; the header comment and
  CONTRIBUTING.md's "A mod" paragraph say it now also reads `server.json` for the board's key.

### 3. Docs

- `CONTRIBUTING.md`, "A mod": the pane reads `STATUS.json` and, for the board's link, the git
  folder's `chantier/server.json`.
- The CR board's user doc, wherever the pane is described in `docs/` (the Driver finds it), says
  the sections and their default folds.
- A release note per the project's release-notes rule.

## Decisions carried from `02-answers.md`

- board-pane-Q1 A: one CR for both inbox items; the batch's states first, then links, services
  and stats, in this CR; one screenshot.
- board-pane-Q2 A: the running batch open (its CRs by state), the rest folded (Backlog with
  `3-ready`, Merged of all batches). Services is part of "the rest": folded.
- board-pane-Q3 A: destination, the running batch batch-31.
- board-pane-Q4 C: the pane shows both links, the public read-only one and the private one; the
  PR's screenshot hides the private one.
- board-pane-Q5 A: the batch's figures are the CRs per state out of the total, the time since
  the batch started and the spend per merged CR.

## Out of scope

- The web board (`clients/web/`), `chantier live` (`clients/tui/`), `STATUS.md` and the server's
  API: no change.
- Any new process in the pane (no PID probe, no port probe, no network read): liveness comes from
  the CLI's snapshot in `STATUS.json`.
- A key in `STATUS.json`, `STATUS.md` or any file of the planning folder.
- Starting or stopping the board or the watcher from the pane (the pane stays read-only).
- Copilot: it has no pane.

## Evidence

- Python tests (`skills/chantier/scripts/cli/tests/`, in-process, few and parametrized): on a
  prepared batch with CRs queued, working, ready, merged (in `3-done/`) and cancelled, the
  written `STATUS.json` holds the batch's `merged` (all of them, newest first), `created` and
  `counts`; on a prepared `server.json` with a live entry and a watcher lock held, `services`
  names them with links and no key, and the file holds neither key's text; with no server,
  `services.server` is `null`.
- Pane tests (`hooks/register.test.tsx`): with an index of a batch whose active `crs` is empty and
  whose `merged` holds CRs, the open batch section shows the merged CRs and no empty-batch line;
  each state group appears with the batch section open and no other fold turned; Backlog,
  Merged and Services are folded by default; the Services fold shows the server's state and the
  watcher's for this session; with a `server.json` holding both keys, a private link carrying
  `?k=<key>` and a read-only link carrying `?k=<read_key>`, each named; with no `read_key`, the
  private link alone; with no readable file, links without a key and the one line; the figures
  line shows the three figures of board-pane-Q5; an index of the older shape (no
  `merged`, `counts`, `services`) draws as today.
- `just check` passes; `just mod` passes (a change to `hooks/` and `types/`, AGENTS.md), run by
  the Driver itself before the PR; `just eval-dry-run` (a change under the CLI's `src/`).
- The long gate `scenario` (a change to the CLI) green at the PR's head; the local Windows run as
  AGENTS.md assigns it by the batch's shape.
- The PR's Deliverables carry one screenshot of the pane from a real Claude Code session running
  the PR's head (`claude --plugin-dir <worktree>`), captioned with the head's SHA (seven
  characters), showing the running batch's CRs by state with its merged CRs. Until it is there,
  the PR's Known gaps names it ("no screenshot of the pane from a real session"). The screenshot
  hides the private link (board-pane-Q4): the Services fold closed, or the private link's key
  masked in the image; the read-only link may show.

## Open questions

None: board-pane-Q4 and board-pane-Q5 closed the two of the first draft.
