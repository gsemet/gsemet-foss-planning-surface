# Change Specification: a planning surface stays in sync through its own autosync

## Goal

The user's request (option A, their pick): chantier does not own an autosync; the planning surface
does, and chantier uses it. Today, with an external planning surface, the Chief of Staff commits and
pushes the surface by hand after each step and at each hand-back. That costs turns, is easy to
forget, and leaves the surface behind while the Foreman, a Griller and the Chief of Staff all write
in it. A surface such as the user's `gsemet-foss-planning-surface` ships its own autosync
(`scripts/ai-autosync-git.py`, `.agents/guidelines/autosync.guidelines.md`).

At the end of this CR:

- The Chief of Staff, the Foreman and a Griller join the surface's autosync group at session start.
  While the group is enabled, no session commits or pushes the surface by hand.
- A `blocked:` group is the Chief of Staff's to fix. When upstream moved, it integrates and
  restarts the group, and never force-pushes. When an approval is needed, the user gives it, never
  an agent.
- The CLI checks the group, read-only: `preflight` warns, and `status` shows one line.
- The board server joins the group while it runs, so its own backlog writes are committed and pushed
  even with no agent session open.
- The board shows the autosync as a pill with a panel, as in the prototype. The user approves an
  incident there and starts or stops the group.

This is CR 5 of the five split from `visualization-backend` (the user: "Oui, ces 5 CRs"). The user
on the code: "juste assure toi que le code soit hyper propre avec de beau standard et modularité
pour facilite la maintenance".

## Decisions carried from the grill

The grill is `visualization-backend/02-answers.md` (its "Autosync merged in", "Autosync and
access, answered", "Split into CRs" and "Technology" sections), with the design of option A in
`visualization-backend/intake/02-surface-autosync.md`.

| Decision | Where this spec carries it |
| --- | --- |
| Option A: chantier owns no autosync and uses the surface's own | "What chantier reads", "Cards" |
| The Chief of Staff, the Foreman and a Griller join the group at session start. Drivers do not join. A Griller in a surface worktree joins nothing | "Cards" |
| While the group is enabled, no session commits or pushes the surface by hand | "Cards", chief-of-staff.md |
| A `blocked:` group is the Chief of Staff's. When upstream moved, it integrates (no change discarded, never a force push), then `start . --enable-only`. The Foreman that meets one tells the Chief of Staff | "Cards" |
| Approvals (staged changes, a found secret) are the user's, never an agent's. They are given from the board's "approve" button, which the user clicks | "Cards", "Board server", "Board interface" |
| The CLI checks, read-only and with no git write: preflight warns when the surface names an autosync but its group has no live participant or is `blocked:`. Status shows one line from `.git/ai-autosync/status.json` and `control.json` | "CLI" |
| "start autosync" / "stop autosync" in the chat: the Chief of Staff runs the surface's own commands | "Cards" |
| The board server joins the group while it runs | "Board server" |
| Option A stays beside the server, and the board adds an autosync mode (state, leader, participants, start and stop) | "Board server", "Board interface" |
| Upstream moved: the board shows the block and its reason. The user asks the Chief of Staff, who integrates and restarts. There is no restart button | "Board interface" (no start button while blocked; the server refuses it too) |
| No autosync (a surface without one, or `.agents/changes/` in the project itself): the board shows nothing, and today's rule (the Chief of Staff commits by hand) stays | "What chantier reads" (detection), "Board interface", chief-of-staff.md |
| The pill sits at the foot of the sidebar, and on the phone a dot beside the project picker. Green is active, grey stopped, red blocked (with its reason), orange waiting for an approval. It shows the time of the last push. A click opens a small panel with the leader, the participants, start or stop, and each incident with its "approve" button. No autosync, no pill | "Board interface" |
| The git-write rule: the board's server is the named exception in `AGENTS.md`. It runs the surface's own autosync and does not commit itself. The rest of the CLI keeps no git write | "AGENTS.md" |
| "The same thing at the end": the spec names the views and `v6-xx` screenshots it reproduces, the PR shows them beside the prototype's, and a final QA compares on PC and phone | "The reference", "QA against the prototype" |
| Out of scope: an autosync of the code repository, and porting the autosync into the CLI | "Out of scope" |
| Python dependencies through PEP 723, the measured code targets of `python-inline-deps`, hand-written HTML, CSS and JS with native ES modules and one module per view, no bundler, very clean modular code | "Code standards" |
| This CR needs the server (`visualization-backend`), and its display needs `board-read-views` | "Order" |

## The reference: the same thing at the end

The prototype lives in the `visualization-backend` CR folder (today
`.agents/changes/2-backlog/P2/visualization-backend/`; the folder moves with its stage):

- `prototype/index.html`, served with its `data.js`. The autosync part is `asPaint()` and the
  `AS`/`ASL` objects (around lines 1075–1098). Its styles are `.asy`, `.adot`, `.apop`, `.aw`,
  `.aa`, `.asyd` and `.asph` (around lines 118–134). Its markup is `#asy`/`#apop` at the sidebar's
  foot and `#asy2`/`#apop2` in the phone's top bar (around lines 400–407).
- `evidence/prototype/v6-20-autosync-approval-pc.png`: PC, the panel open on the "à approuver"
  state, with one incident and its "Approuver" button.
- `evidence/prototype/v6-21-autosync-blocked-phone.jpg`: phone, the dot beside the project picker
  and the panel open on the "bloqué" state, with its red reason box.

This CR reproduces exactly these two views: **the autosync pill and its panel**, in its four states,
on PC and on the phone. Nothing else of the prototype is this CR's. The sidebar, the phone's top
bar and the project picker belong to `board-read-views`, which this CR plugs into.

What the prototype shows, and what this CR delivers:

| Element | Prototype | Delivered |
| --- | --- | --- |
| Pill (PC) | at the sidebar's foot: a coloured dot, "Autosync <state>" in bold, a one-line subtitle, a chevron | same |
| Dot (phone) | a 34x33 button beside the project picker, holding only the dot, titled "Autosync <state>" | same |
| Colours | active `#23805a`, stopped `#8b909c`, blocked `#c03552`, approval `#b86e0c` | same, as CSS custom properties |
| Subtitle | active: "poussé il y a N s / N min"; blocked: "le Chief of Staff doit intégrer"; approval: "N incident à approuver"; stopped: "commits manuels" | same, from real data |
| Panel | the header (dot and state); for blocked, a red box "<reason>. Demande au Chief of Staff d'intégrer puis de relancer."; a list of Leader, Participants and Dernier push; for approval, one amber box per incident, "Incident <id> : <message>", with "Approuver"; the actions "Démarrer" (stopped) or "Arrêter" (active, approval), and none while blocked | same, from real data |
| "Simuler" row | four buttons to switch the state | **not delivered**: a prototype aid (open point 5) |
| Panel placement | PC: above the pill, 300 px wide; phone: fixed, 12 px from the sides, 58 px from the top | same |
| Closing | a click outside closes it | same, plus Escape, and `aria-expanded` on the button |

The words are the prototype's (French). If `board-read-views` sets the board's language another way,
these strings follow its rule (open point 6).

## What chantier reads from the surface's autosync

These facts were read from the surface's `scripts/ai-autosync-git.py` (version 1.0.0) and its
guidelines. That repository is never changed by this CR.

- **Its state folder:** `<git dir of the surface's checkout>/ai-autosync/` (the script's
  `repository()`: `git rev-parse --absolute-git-dir`). It holds:
  - `control.json`: `enabled` (absent means true; only `false` disables), `local_only`, `reason`
    (`"started by user"`, `"stopped by user"`, or `"blocked: <message>"`), `updated_at`
    (epoch seconds), and `updated_by_pid`.
  - `status.json`: `state`, which is one of `synced`, `pending`, `waiting`, `offline`,
    `action_required` or `approval_required`. Also `message`, `updated_at`, and, for an
    approval, `incident` (`staged-<20 hex>` or `secrets-<20 hex>`). After a cycle it also
    holds `branch`, `head` and `committed`.
  - `watcher.json`: the leader's `pid` and `local_only`, while a leader runs.
  - `participants/<pid>.json`: `pid`, `harness`, `owner_pid`, `session_id`, `role` (`leader`,
    `follower` or `idle`) and `since`. A file whose `pid` is dead is stale. The tool's own
    `participants()` deletes it; **chantier only skips it and never deletes it**.
  - `approvals.json` and `sync.lock`, which chantier does not read.
- **The leader blocks the group** (`set_control(enabled=False, reason="blocked: …")`) after any
  cycle that returns 1: `action_required` (upstream moved, conflicts, LFS or Gitleaks failure) or
  `approval_required`. An approval therefore leaves a `blocked:` control **and** a status
  `approval_required` with its `incident`.
- **`approve . <incident>`** only records the approval of the incident that `status.json` names now.
  The group stays disabled until `start . --enable-only` (the guidelines: "obtain any required
  approval, then run `start . --enable-only`").
- **Its commands** run from the surface's root with `uv run scripts/ai-autosync-git.py <action> .`:
  `status`, `join --owner-pid <pid> [--harness <h>] [--session-id <id>]`,
  `start [--enable-only] [--local-only]`, `stop`, `sync`, and `approve <incident>`.
- **The harness:** `--harness auto` picks Copilot from `COPILOT_AGENT_SESSION_ID` (then the
  participant follows the chat's `inuse` lock), and Claude Code from `CLAUDECODE=1` (owner process
  only). Claude Code's `session_id` is `null` unless `--session-id` is passed. This was seen in
  the user's surface on 2026-11-13: a `claude-code` participant with `"session_id": null`.

**When a surface "names an autosync"** (the detection, one function): the planning folder is
external (`repo.external`), the surface's instruction file (`surface_instructions(repo)`) contains
the text `.agents/guidelines/autosync.guidelines.md` (the line the tool's `init` writes), and
`<surface>/scripts/ai-autosync-git.py` exists. An in-project planning folder never has one (the
answers: "No autosync … `.agents/changes/` in the project itself"). A surface that names the
guidelines but lacks the script is reported by preflight (below) and treated as having no autosync
everywhere else.

**The four states** (one pure function, used by the CLI and the board alike):

| State | When | Pill |
| --- | --- | --- |
| `approval` | `status.state == "approval_required"` and `status.incident` is set | orange |
| `blocked` | `control.enabled` is false and `control.reason` starts with `blocked:`, and not `approval` | red, with the reason (the text after `blocked: `) |
| `stopped` | `control.enabled` is false otherwise | grey |
| `active` | `control.enabled` is not false | green |

There are two more facts beside the state: **the live participants** (the participant files whose
`pid` is alive) and **the leader** (`watcher.json`'s `pid` when alive, named through its participant
file). **The last push** is the `updated_at` of `status.json` when its state is `synced` (open
point 3). The board remembers the last such time it saw while it runs; the CLI shows it only while
the state is `synced`. A state folder that does not exist yet means "no group yet".

## What changes

### 1. CLI, read-only: `autosync/` (new package, layer 2 of `python-inline-deps`)

This CR builds on the layout of `python-inline-deps` (`core/`, the layer-2 domain modules,
`commands/`, `board/`). If that CR's names moved in review, the Driver follows them, keeping the
layering below. A new package `skills/chantier/scripts/cli/src/chantier/autosync/`:

| Module | Responsibility (one each, in its docstring) |
| --- | --- |
| `autosync/site.py` | `find_site(repo) -> AutosyncSite \| None`: the detection above. `AutosyncSite` is a frozen dataclass with `surface`, `script`, `guidelines`, `state_dir` and `script_missing`. It imports `core/repo.py` and `plugin_files.surface_instructions`. |
| `autosync/records.py` | pydantic models `Control`, `SyncStatus` and `Participant` (`extra="allow"`, defaults as the tool reads them: `enabled` true when absent). `read_group(state_dir) -> GroupFiles` reads the JSON files and **never writes or deletes**. An unreadable file is reported as a fact (`unreadable: <name>`), never guessed. |
| `autosync/view.py` | `AutosyncView` (frozen dataclass: `state`, `reason`, `incident`, `incident_message`, `leader`, `participants`, `last_push`, `local_only`, `no_group`) and `classify(files, alive) -> AutosyncView`, a pure function. `alive` is injected (`procs.alive`), so the function has no I/O. `name_participant(p, names) -> str` names a participant (see "Board server"). |
| `autosync/lines.py` | `preflight_check(site, view) -> Check` and `status_line(view) -> str`: the texts below, and nothing else. |

Imports go `autosync/` → `core/` and `procs.py` (same layer), never upward. No subprocess, no git
call: everything is file reading plus a PID check.

**`preflight`** (`commands/preflight.py`) gets one new check, **P13**. It is warn-only (it never
fails a preflight) and runs only when `find_site` finds a site (external, autosync named). The
lines:

- `P13 ok   the surface's autosync is active: leader <name>, <k> participant(s)`
- `P13 ok   the surface's autosync is stopped (<reason>): commit the surface by hand`
- `P13 warn the surface names an autosync but scripts/ai-autosync-git.py is missing: no autosync until it is there`
- `P13 warn the surface's autosync has no group yet: join it (.agents/guidelines/autosync.guidelines.md)`
- `P13 warn the surface's autosync is active but has no live participant: join it (.agents/guidelines/autosync.guidelines.md)`
- `P13 warn the surface's autosync is blocked: <reason, 120 chars at most>: the Chief of Staff integrates, then start . --enable-only`
- `P13 warn the surface's autosync waits for the user's approval of incident <id>: <message, 120 chars at most>`

P13 joins the configuration checks that session-start does **not** report at session start (the
session joins right after). It is read at the batch's preflight like the others.

**`status`** (`commands/batch_status.py`): when a site is found, the line right after the batch's
first line:

- `autosync active, leader <name>, <k> participant(s), synced <HH:MM>` (`synced …` only while the
  state is `synced`; `, local only` when `local_only`)
- `autosync active, no live participant: join it`
- `autosync stopped (<reason>): commit the surface by hand`
- `autosync blocked: <reason, 70 chars at most>: the Chief of Staff integrates, then start . --enable-only`
- `autosync waits for the user's approval: incident <id>: <message, 70 chars at most>`
- `autosync: no group yet`

With no running batch, `status` fails as today (open point 4). No line appears with no site.
`STATUS.json` and `STATUS.md` do not change, so the CR board pane does not change and the
screenshot rule of `AGENTS.md` does not apply.

### 2. Board server: joins the group, serves the state, runs the user's three actions

This builds on the server that `visualization-backend` (board-server) delivers: its routes, its
URL secret, its write protection and its live refresh. Two new modules in its `board/` package:

| Module | Responsibility |
| --- | --- |
| `board/autosync_tool.py` | The **only** code of the plugin that starts the surface's autosync. `spawn_join(site, owner_pid)` starts a detached process; `run_action(site, action, *args) -> ToolResult` runs one command synchronously, with a 30 s timeout, from the surface's root, and returns its exit code and last output line. The argv is built from a fixed table (`start`: `start . --enable-only`; `stop`: `stop .`; `approve`: `approve . <incident>`). There is no shell and no free text in an argv. |
| `board/autosync_api.py` | The routes below and the JSON shape. It reads through `autosync/` and acts through `autosync_tool.py`. |

**Joining.** When the server starts serving (not on a reuse, "board already running"), and only if
`find_site` finds a site, it runs, detached and once:

`uv run scripts/ai-autosync-git.py join . --owner-pid <the server's own pid> --harness generic --session-id chantier-board`

- `--harness generic` makes the participant follow the server's process only. Without it, a server
  started from a Copilot chat would leave the group when that chat closes, while the server still
  serves.
- The participant leaves on its own within about a second once the server's process ends (the
  tool's owner-PID check). The server needs no stop code.
- Detached means `start_new_session=True` on POSIX, and `CREATE_NEW_PROCESS_GROUP |
  DETACHED_PROCESS` on Windows. Its stdin, stdout and stderr go to `DEVNULL` (open point 7).
- One line among the server's first lines: `board: joined the surface's autosync (participant pid
  <n>)`, or `board: autosync not joined: <reason>`. The server keeps serving either way: the board
  never blocks a session.

**Naming a participant** (`autosync/view.name_participant`), in this order:

1. `owner_pid` equal to the server's pid: "board (ce serveur)".
2. `session_id` equal to the seat's session (`seat.json`) of any project the server serves:
   "chief-of-staff".
3. `session_id` equal to the `foreman` session of a running batch of those projects: "foreman".
4. Another `session_id`: "session <its first 8 characters>" (a Griller or another session).
5. No `session_id`: "<harness> pid <pid>".

**API** (inside the server's URL secret and write protection, like every board route):

- `GET /api/autosync` returns `{"present": false}` with no site. Otherwise it returns `{"present":
  true, "state", "reason", "incident": {"id", "message"} | null, "leader", "participants": [{"name",
  "role"}], "last_push" (ISO 8601 or null), "local_only", "no_group"}`. The same object goes into
  the server's live-refresh payload, so the pill changes without a reload.
- `POST /api/autosync/start`: allowed only in the `stopped` state. Otherwise it returns 409 with
  "bloqué : le Chief of Staff intègre puis relance" (blocked), or the current state's word. It runs
  `start . --enable-only`.
- `POST /api/autosync/stop`: allowed in `active` and `approval`. It runs `stop .`.
- `POST /api/autosync/approve` with `{"incident": "<id>"}`: allowed only when the state is
  `approval` and the id is the incident shown now (otherwise 409). It runs `approve . <id>`, then,
  on success, `start . --enable-only`, which is the guidelines' step after an approval (open point
  2). It is the user's click; no agent calls this route (the cards say so).
- Each POST returns the new `GET` object and the tool's last output line. A non-zero exit is
  returned as 502 with that line, which the panel shows.

### 3. Board interface: the pill and its panel

One ES module per view (Technology): `board/static/js/views/autosync.js` and its stylesheet
`board/static/css/autosync.css`. The folders follow `board-read-views`' layout.

- `autosync.js` exports `mountAutosync({sidebarFoot, phoneBar, store, api})`. It renders the pill
  into the sidebar's foot, the dot beside the project picker in the phone bar, and one shared panel.
  It subscribes to the store's autosync object (from the live refresh) and re-renders on change.
  The "poussé il y a …" age ticks every 5 s on the client, only while the state is `active` and the
  panel is closed (as the prototype's `setInterval`).
- `present: false` renders nothing, and the pill's slot takes no room. In a multi-project surface,
  the pill shows on every project and on "Tous les projets", since the group is the surface's, not a
  project's.
- Small pure functions: `label(state)`, `subtitle(view, now)`, `panelHtml(view)` (escaped text
  only) and `actions(view)`. Event wiring sits apart from rendering. No inline script or style
  attribute; the colours are classes (`.adot.active` …), so the server's CSP holds.
- The buttons call `api.post('/api/autosync/…')`. While a call runs, the button is disabled. Its
  error line shows inside the panel, under the actions.
- Accessibility: the pill and the dot are `<button aria-haspopup="dialog" aria-expanded>`. The panel
  closes on Escape and on a click outside. The dot's `title` and `aria-label` are "Autosync
  <state>". The contrast meets the visual rules of the grill (WCAG AA, no text under 11 px for a
  badge and 12 px elsewhere).

### 4. Cards (host-neutral references; no agent file changes)

- **`concepts.md`, "Planning surface":** add: "A surface may ship its own autosync (its rules name
  it; chantier recognises `scripts/ai-autosync-git.py` with
  `.agents/guidelines/autosync.guidelines.md`). chantier owns none: the Chief of Staff, the Foreman
  and a Griller in the surface's checkout join its group at session start, with `--session-id
  <their session id>`, and follow its guidelines. Drivers, and a Griller in a surface worktree,
  never join. While the group is enabled, no session commits or pushes the surface by hand. The
  board's server joins it too while it runs (`AGENTS.md`'s named exception)."
- **`session-start.md`, section 2:** after the role is set (the Chief of Staff right after `seat
  take` and the board; a Griller once it is a Griller), and only in a surface whose rules name an
  autosync, run the surface's `status`, then join as its guidelines say, adding `--session-id <own
  session id>`, once per session. Do not join when `status` already lists a participant with this
  session's id. A reload joins nothing, like the board. A blocked or approval state met there: the
  Chief of Staff handles it (its card), and a Griller says it in one line and goes on. Add to "The
  board" list the line `board: autosync not joined: <reason>`, which is one line to the user, like a
  board that did not start.
- **`chief-of-staff.md`, "With a planning surface":** it keeps "the surface's own rules win for its
  sync". It adds:
  - With an autosync enabled: commit or push nothing by hand. `uv run scripts/ai-autosync-git.py
    sync .` publishes at once when a step needs it.
  - Stopped by the user, or no autosync: today's rule (by hand, explicit paths, a plain push, a
    rebase on a rejected push, never a force push).
  - **Blocked** (the `status` line, P13, the Foreman's ask, the board, or the user): the reason
    says what. When upstream moved, integrate as the surface's rules say (chantier's own: a rebase,
    no change discarded, never a force push), then `start . --enable-only`. When something else
    blocks it (LFS, Gitleaks, a conflict), repair what is the session's own, else tell the user the
    reason and wait.
  - **Approval:** show the user the incident (its id and message). Only the user approves, from the
    board's "Approuver" (give the board's URL) or in their own terminal. The Chief of Staff never
    runs `approve`, even on the user's word in the chat (open point 1).
  - Add an entry-point row: `"start autosync", "stop autosync"` → the surface's own `start .
    --enable-only` (and a join if this session is not a member) / `stop .` → "With a planning
    surface".
- **`foreman.md`:** at the start of a batch it steers in a surface whose rules name an autosync, the
  Foreman joins as session-start says, after its title. When a `status` read shows `autosync blocked`
  or `autosync waits for the user's approval`, it sends one ask to the Chief of Staff (`$CHANTIER asks
  "autosync <state>: <reason>"`), once per block, and does nothing else about it.
- **`griller.md`, "In a planning surface":** add "join the surface's autosync as
  [session-start](session-start.md) says". Its "In a worktree" line (joins nothing) stays.
- **`docs/planning-modes.md`:** lines 42–44 and the "Grillers" section get the same account in the
  user's terms. Add a short "The surface's autosync" section: who joins, the four states, who fixes
  a block, that approvals are the user's in the board, and that the board's server joins while it
  runs.

The cards are host-neutral: Claude Code and Copilot read the same text, and `agents/` and
`com.github.copilot/agents/` do not change.

### 5. `AGENTS.md`

`visualization-backend` (board-server) carries the named git exception for the server (its intent:
"the server is the named git exception"). This CR checks that the merged text says the server "runs
the surface's own autosync (it joins its group and runs its start, stop and approve on the user's
click); it never commits itself; the rest of the CLI keeps no git write". It adds that sentence
there only if board-server's wording lacks it (open point 8). Nothing else in `AGENTS.md` changes.

## Code standards

- **Python:** the targets of `python-inline-deps`, enforced by `just check` (`just lint`): files at
  most 400 lines, functions at most 50 lines, complexity at most 10, at most 5 arguments, nesting at
  most 3, ruff with `E W F I B UP SIM C90 PL RUF`, `mypy --strict`, no import cycle, and no import
  inside a function except the declared lazy ones. Each new module states its one responsibility in
  its docstring. The JSON files are read through pydantic models, never as `dict[str, Any]`
  passed around. `classify` and `name_participant` are pure. The subprocess code lives in one
  module.
- **No new dependency:** `procs.alive` (psutil, from `python-inline-deps`) checks a PID; `pydantic`
  is already there.
- **JS and CSS:** the targets and linter that the board CRs set (`python-inline-deps` leaves them
  to them). One ES module, no framework, no bundler, no global, and functions small enough to read
  at a glance.
- **Portability:** paths through `pathlib`, UTF-8 reads, and the detached start for both POSIX and
  Windows (above).

## Order

`depends.json` holds `{"after": ["visualization-backend"]}`. The pill needs `board-read-views`'
sidebar foot, phone bar and project picker, and one CR is one PR. So this CR runs after both, and
`board-read-views` should join `depends.json` (open point 9; this spec does not edit it).
`python-inline-deps` comes before through `visualization-backend`.

## Out of scope

- An autosync of the project's code repository (the clone and its worktrees).
- Porting the autosync into the CLI, or a CLI command that wraps it. Only the board server starts
  the tool, and only `join`, `start`, `stop` and `approve`.
- Any other autosync tool than `scripts/ai-autosync-git.py` with its guidelines.
- A restart button for a blocked group. The board's "approve" for a non-current incident.
- Messages from the board to the Chief of Staff (the queue is a later step, per the grill).
- `STATUS.json`, `STATUS.md`, the CR board pane (`hooks/register.tsx`) and `types/`, so no `just
  mod`. `.github/workflows/ci.yml` does not change.
- The board's other views, its picker and its language: `board-read-views`. The docs' screenshots:
  `board-docs-screenshots`.

## Evidence

The Verifier keeps each item in `work/verifier/evidence/`, and the PR body quotes them.

- **E1. `just check`** passes on the Windows machine, then in CI on Linux, macOS and Windows, with
  the lint targets (0 ruff findings, 0 mypy errors for the new modules).
- **E2. `just scenario`** passes on both forges (the CLI and the cards change). New steps, in the
  scenario's external-surface setup:
  - Detection: no line without the guidelines' mention. P13 `missing` without the script.
  - The state folder, written by the scenario under the scratch surface's `.git/ai-autosync/`, with
    one participant whose pid is a live child process of the scenario, and one dead one. Each of
    `active` (with and without a live participant), `stopped`, `blocked` and `approval`, plus no
    state folder, gives the exact P13 line and `status` line above. The dead participant's file is
    still there afterwards (read-only proof).
  - The board: the scratch surface gets a fake `scripts/ai-autosync-git.py` (`scenario/fake_autosync.py`,
    no dependency) that appends its argv to a file and writes the state files a real tool would. The
    steps check that the server's start spawns `join . --owner-pid <server pid> --harness generic
    --session-id chantier-board`, and that `GET /api/autosync` matches each state. `POST start` is
    refused while `blocked` (409) and runs `start . --enable-only` while `stopped`. `POST approve`
    with a stale id gets 409, and with the current id runs `approve . <id>` then `start .
    --enable-only`. A server in an in-project folder returns `{"present": false}` and spawns
    nothing.
- **E3. The real tool, end to end**, in a scratch folder outside this repository and outside the
  user's surface. The steps:
  1. Make a bare repository as `origin`, clone it as a surface, and copy the user's
     `scripts/ai-autosync-git.py` (read only from there) and run its `init`. Add `projects/demo/`
     (`checkout.yml` and `changes/`).
  2. Start `chantier board --project demo` and show the join line. A `triage` from the board's API
     is committed and pushed by the server's participant, with no agent session open: the bare
     repository's log shows the autosync commit.
  3. Get `blocked` by pushing to `origin` from a second clone, `approval` by staging a file by hand,
     and `stopped` by the board's "Arrêter".
  4. Approve from the board; the group returns to `active` and the staged change is pushed.
  5. Stop the server; within 2 s its participant file is gone.

  Gitleaks and Git LFS must be installed: a missing one stops the step with its message, with no
  workaround.
- **E4. The cards, walked through** in the same scratch surface. A Chief of Staff session and a
  Griller session join, `status` lists their names ("chief-of-staff", "session …"), and a
  `blocked` group is integrated and restarted by the Chief of Staff with no force push (the reflog
  of `origin` shows no forced update). Not proved: a real Foreman (no batch in the scratch surface).
  The PR's Known gaps names it.

## QA against the prototype (PC and phone)

The rule of the split: the PR shows its views beside the prototype's, and a final QA compares them.

- Open the prototype (`prototype/index.html` in the `visualization-backend` folder) and the board of
  E3 at **PC 1400x860** and **phone 375x812**. Use the same browser automation for both (a scratch
  uv script with Playwright, outside the repository and not committed, or the host's browser tool).
  Check that the board has no console error.
- Pairs, each prototype state set with its "Simuler" row:

  | # | Size | State | Panel | Prototype reference |
  | --- | --- | --- | --- | --- |
  | 1 | PC | active | closed | live prototype |
  | 2 | PC | approval | open | `v6-20-autosync-approval-pc.png` |
  | 3 | PC | blocked | open | live prototype |
  | 4 | PC | stopped | open | live prototype |
  | 5 | phone | blocked | open | `v6-21-autosync-blocked-phone.jpg` |
  | 6 | phone | active | closed (the dot) | live prototype |
  | 7 | phone | approval | open | live prototype |
  | 8 | PC and phone | an in-project folder | no pill, no dot | the answer "No autosync, no pill" |

- The PR body holds a table: pair, prototype image, board image, differences. The expected
  differences are real data instead of simulated data, and no "Simuler" row. Any other difference
  is fixed, or named in Known gaps with its reason.
- The whole-board final QA, across the five CRs, is the Chief of Staff's order once all are merged
  (the user's pick). This CR's eight pairs are its part of it.

## CI

No job changes. The `check` job runs `just check` on `ubuntu-latest`, `macos-15-intel` and
`windows-latest`, and the `scenario` job runs on `ubuntu-latest`. Those runners have no Gitleaks,
no Git LFS setup, no `claude` binary, and no real surface. That is why E2 uses the fake tool and E3
runs on the dev machine only. Only the first CI run can prove the detached join under Linux and
macOS (E2's spawn check) and the new lint on three systems.

## Open points (defaults taken, for the Chief of Staff to confirm with the user)

1. **Approval by the Chief of Staff on the user's word in the chat.** The default is never: the
   user clicks "Approuver" in the board or runs the command themselves, as the answer says ("the
   user clicks it, never an agent"). The alternative lets the Chief of Staff run `approve` when the
   user names the incident in the chat.
2. **Restart after an approval.** The tool leaves the group disabled after `approve`. The default
   has the board's "Approuver" run `approve` and then `start . --enable-only`, as the guidelines'
   next step, matching the prototype (the pill turns green). The alternative leaves the restart to
   the Chief of Staff, as for a block.
3. **"Dernier push".** The tool records no push time. The default shows the `updated_at` of the
   last `synced` status, which the leader rewrites at each cycle (every 30 s when idle), so it
   reads "last time found in sync". The alternative reads the remote-tracking ref's reflog in
   `.git/logs/`.
4. **`status` with no running batch.** The default keeps today's failure ("no running batch"), and
   the state is then read from preflight P13 or the board. The alternative prints the autosync line
   alone.
5. **The prototype's "Simuler" row** is a prototype aid and is not delivered. The QA sets the
   prototype's state with it.
6. **The words' language.** The default uses the prototype's French strings, unless
   `board-read-views` sets another rule for the board's language.
7. **The join's output.** The default sends it to `DEVNULL`; the tool's state files say what it
   does. The alternative is a `board-autosync.log` in the planning folder (ignored by `*.log`).
8. **`AGENTS.md`'s exception text.** The default leaves it to board-server and adds the autosync
   sentence here only if it is missing.
9. **`depends.json`.** The default is that the Chief of Staff adds `board-read-views` to this CR's
   `after`, since the pill needs its frame and one CR is one PR.
10. **Joining with a session id.** The default has the cards add `--session-id <own session id>` to
    the surface's join, so the board can name "chief-of-staff" and "foreman". The surface's
    guidelines do not ask for it, but the tool accepts it for every harness. A Griller is shown as
    "session <id>", because no record names a Griller.
11. **The host PID on a PowerShell host.** The surface's guidelines read it with `echo $PPID`
    (bash). The default adds nothing to the cards and follows the guidelines. A host reference may
    later give the PowerShell form if a session cannot find it.
12. **"Each incident".** The tool holds one pending incident at a time, in `status.json`. The panel
    shows that one, so "each incident" is at most one.

## Decisions after the specification (they replace the open points they name)

Asked by the Chief of Staff, 2026-11-13 (in French, recorded in English).

- **The page's language: both.** English by default and French, from one word file per language, built so that more translations can be added later. The prototype's French labels are the French file. Where an open point above says English only or French only, this answer replaces it.
- The other open points stay at the specification's defaults.
