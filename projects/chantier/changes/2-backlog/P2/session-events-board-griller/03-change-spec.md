# Change Specification: the watcher wakes the Chief of Staff on what the user does in the board

No tracker issue: the CR is verbal (the user, 2026-11-17, during batch-23).

**Written again on top of the forge hub** (hub-Q8): CR-358 `surface-forge-hub`, merged on main as
`a7f32370` (feat(watch): one forge hub per surface and machine, and watchers that wake each
session) and `5717626d` (fix(status): print the forge hub and watch lines after the last closed
batch), delivered this item's forge and merge part: `chantier watch`, the hub's forge reads, the
merges recorded by the Chief of Staff with no word from the user, the fold of `board-seen.jsonl`
into `forge-journal.jsonl`. None of the board events is delivered on main: `board/write_api.py`
and `board/config_api.py` write `board-journal.jsonl` only, and the watcher reads
`forge-journal.jsonl` only. This specification replaces the one of 2026-11-17 (its own
`board-events.jsonl`, its `Monitor`-run watch, its `watch.json`): it keeps only the board's events
and puts them in the hub's journal, read by the hub's watcher.

## Goal

The user, 2026-11-17: a running Chief of Staff session hears nothing of what the user does in the
web board until the user says "rescan". An idea added to the inbox, a priority or a stage changed
(Triage, Kanban), a note saved on a CR from the board's editor, an agent or a model changed on the
Configuration page: the Chief of Staff should be told within about 20 s, with no word from the
user, with or without a batch, on the same wake as the forge's merges. On a host where nothing can
wake the session, the events wait in the journal and the Chief of Staff reads them at the user's
next message. One planning surface holds several projects, each with its own Chief of Staff and
one board for all: each Chief of Staff hears only its own project's board writes.

The measured cost it removes: one round trip with the user per board session ("rescan", "I
updated the priorities", the `chief-of-staff.md` entry row for it), and a Chief of Staff that
plans on a stale backlog when the user forgets it.

## Decisions carried (from `02-answers.md`)

| Answer | Decision | Where below |
|---|---|---|
| events-Q1, as re-scoped by hub-Q8 | The board's writes go into the hub's journal and wake the session through the hub's watcher (its background end), not a `Monitor` | 1, 2 |
| events-Q2 | Wake on: a priority or stage changed (Triage, Kanban), an item added to the inbox, a note on a CR (a file saved from the board's editor), a Configuration change (agent or model). Grouped into one wake. No wake for opening a page or text being typed. Labels, groups, ungroup and next batch do not wake and ride along with the next wake (settled after the spec critic) | 1, 2 |
| events-Q3 | Where nothing wakes the session: the events wait in the journal; the Chief of Staff reads and summarises them at the user's next message, and says once at the session's start that this host does not wake it; today's pull path, no look-alike tool | 2 (`--once`), 4 |
| events-Q5 | Woken, the Chief of Staff acts alone on merges only (the hub's rule, unchanged); a board event: one line to the user, no action | 4 |
| events-Q6 | The watcher runs for the whole session, with or without a batch; the forge is read only while a PR of a running batch is open (the hub's rule, unchanged) | 2, 4, 5 |
| events-Q8 | Two CRs: this one holds the events; the Griller started from the board is `2-backlog/P3/board-griller` | Out of scope |
| events-Q9 | A board of another chantier version is named, once, by the watcher and by `status`, with "restart it"; the forge is still read, merges still seen | 2, 3, 4 |
| events-Q10, as re-scoped by hub-Q8 | No `Monitor`, so no `Monitor` rule: the watcher is a shell command already covered by P10's `chantier *` rules | Settled in `02-answers.md` |
| events-Q11, as re-scoped by hub-Q8 | A `Monitor` that expires no longer exists; the hub's `watch:` line of `status` and the start again after each end stay | Open question 1 |
| events-Q12 | Copilot: a watcher's wake is unproved there; until it is, the Chief of Staff also runs the pull path (`watch --once`) at each user message, said once at the session's start | 4, 5 |
| Several projects on one surface | Each board write lands in its own project's journal only; a watcher reads only its project's journal | 1, Evidence |
| hub-Q8 | Same journal (`forge-journal.jsonl`), same `watch` | 1, 2 |
| hub-Q9 | The user's yes once per session before the watcher starts; now asked at every Chief of Staff session's start (events-Q6), the question naming the board's writes too | 4 |

## What changes

All paths are in chantier's repository; `cli/` is `skills/chantier/scripts/cli/`, and
`chantier/` is `cli/src/chantier/`. Keep every card edit outside the cards' "Startup core"
sections (the startup manifest's limit).

### 1. The journal: board lines in `forge-journal.jsonl`

`chantier/hub/journal.py` (the journal's one module) gains a third kind, `board`, next to `merged`
and `checks-red`. Its docstring and the package docstring of `chantier/hub/__init__.py` say the
board's writes are its third writer's lines.

- **Shape.** `{"seq", "t", "by": "board", "kind": "board", "action", "items", "text", "wakes"}`:
  `action` is the board journal's kind (`new`, `move`, `edit`, `config`, `label`, `group`,
  `ungroup`, `next-batch`), `items` and `text` the same slugs and words as the
  `board-journal.jsonl` line written in the same call, `wakes` a boolean from the table below.
- **Never deduplicated.** `_key` gives no key for a `board` line: `append` writes each one (two
  identical moves are two writes). Today `_key` treats every kind other than `checks-red` as a
  merge: a `board` line must not fall into that branch.
- **Which actions wake** (events-Q2):

  | `action` | Board write | `wakes` |
  |---|---|---|
  | `new` | an idea added to the inbox | true |
  | `move` | a priority or a stage changed, one item or a group | true |
  | `edit` | a CR's file saved from the board's editor (the board's way to leave a note) | true |
  | `config` | a role's agent, model or escalation changed on the Configuration page, not a dry run | true |
  | `label`, `group`, `ungroup`, `next-batch` | not in events-Q2's list | false |

- **Its text** (`event_text`, the one function the watcher's output uses): `board wrote
  (<action>): <text>; for the Chief of Staff: tell the user, act on nothing`. A `merged` or
  `checks-red` line keeps its text. `lines()` (the `status` lines) still lists `merged` lines only:
  a board line is never printed by `status`.
- **The writers.** `chantier/board/write_api.py`, `_answer`: when it writes a
  `board-journal.jsonl` line, it also appends one `board` line through `hub.journal.append(repo,
  [...], "board")`, same kind, slugs and words. `chantier/board/config_api.py`, `_put`: the same
  when it writes its `config` journal line (never for a dry run). A refused write writes none (it
  writes no journal line today); `rescan` writes none; reading or opening a page writes nothing.
  The project is the route's own (`project.repo`), so a write on project `other` lands in
  `projects/other/changes/forge-journal.jsonl` only.
- `board-journal.jsonl`, its dialog and its `rescan` are unchanged: the journal line is written in
  addition, not instead.

### 2. `chantier watch`

`chantier/declare/watch.py` and `chantier/hub/watch.py`.

```
chantier watch --seat SESSION [--after SEQ]
chantier watch --once --after SEQ
```

- **`--seat SESSION`** (new, required without `--once`): the Chief of Staff session it is for.
  Refused, writing nothing, when the project's `seat.json` (`core/seat.py`, `read_seat`) does not
  name it: `watch: the seat of <project> names <other or no session>, not <SESSION>`, exit 2
  (`EXIT_PRECONDITION`).
- **No batch needed** (events-Q6). The refusal `watch: no running batch in <project>: nothing to
  watch` and the end `watch: no running batch in <project>; ended` are removed: the watcher runs
  with a running, paused or no batch. The hub's cycle is unchanged (`hub/cycle.py`: running
  batches with a PR the record does not hold merged or cancelled; nothing else is read), so a
  watcher with no running batch reads the forge for no project of its own.
- **Its end.**
  - From the first new line with a waking kind (`merged`, `checks-red`, or `board` with `wakes:
    true`), it ends once `quiet_s()` (20 s) has passed with no newer waking line, as today. A
    `board` line with `wakes: false` neither starts nor extends that wait; it is carried and
    printed at the next end.
  - It also ends when the project's `seat.json` no longer names its session, checked about every
    10 s (the board's `SEAT_CHECK_S`): its new lines, then `watch: the seat of <project> names
    <other or no session> now; ended`, exit 0. This is what stops a watcher left behind by a
    session that ended, once another session takes the seat.
  - The last line otherwise stays `watch: cursor <seq>; next: chantier watch --after <seq>`; the
    next start passes `--seat` too.
- **Start line** (events-Q9): `watch: <project> from cursor <n>` with `, the hub` or `; hub is
  chantier <v>` as today, then `; board is chantier <v>: its writes do not reach this watcher,
  restart it` when the board's running record (`board/running.py`, `live(key_path(repo))`) is live
  and its `version` is not this CLI's `__version__`. No live record: nothing said. The watcher
  goes on either way.
- **`--once`** (the pull path, events-Q3 and events-Q12): prints, for every journal line whose
  `seq` is above `--after` (waking or not), its `event_text`, then `watch: cursor <seq>; next:
  chantier watch --after <seq>` (the cursor unchanged when nothing is new), and exits 0. It takes
  no lock, is never the hub, reads no forge, needs no seat and no batch, and starts no process.
  `--once` without `--after`, or with `--seat`: exit 1 (`EXIT_USAGE`). `--after` past the
  journal's end: today's refusal, in both forms.
- The help text names the board's writes next to the forge events.

### 3. `status`

`chantier/commands/batch_status.py`:

- `_watch_lines`: the `watch: chantier watch --after <highest seq>` line prints for a paused batch
  too (the watcher runs whatever the batch); the `forge hub:` line stays for a running batch only.
- events-Q9: a new line, whatever the batch's status, when the board's running record is live and
  of another version: `board: chantier <v> serves this surface, this is chantier <w>: its writes do
  not reach the watcher; for the Chief of Staff: tell the user once to restart it`.
- No board event is printed by `status` (it is the Foreman's heartbeat too, and the Chief of
  Staff's cursor is its own). `STATUS.md`, `STATUS.json` and the CR board pane do not change.

### 4. The cards

- **`skills/chantier/references/session-start.md`, "The watcher"** (line 97): a Chief of Staff
  asks at its session's start, whatever the batch, after `seat take` (no longer "whose project has
  a running batch"); the question also says the watcher tells it, within about 20 s, what the user
  does in the board. The command becomes `$CHANTIER watch --seat <own session id> --after <n>`
  (`<n>` from `status`'s `watch:` line, or the journal's end when `status` has no batch: omit
  `--after`). On a host whose reference says a watcher's end does not wake the session, or is not
  proved to (Copilot today, events-Q12), say once, in the user's language: "This host may not wake
  me: what you do in the board reaches me at your next message." A no: unchanged for the forge;
  see open question 2 for the board's writes.
- **`skills/chantier/references/chief-of-staff.md`**
  - "The watcher" (line 1220): it prints the forge events and the board's writes; it ends 20 s
    after the last waking one, or when the seat moves. *When it starts*: with the session's yes, at
    the session's start or a reload when no watcher of this session runs, and after each end with
    the `--after <seq>` of its last line; with or without a batch (events-Q6). "A watcher that ends
    with `no running batch` is not started again" becomes "A watcher that ends with `the seat …
    names <other> now` is not started again: the seat moved". *A watcher's end*: a `board wrote`
    line: one line to the user that says it (a few words per event), no tool call, no action
    (events-Q5); the merge and `checks red` rules unchanged. The `board:` version line of `status`
    and the start line's `board is chantier <v>`: say it once to the user with the restart; never
    stop or restart the board yourself.
  - The pull path (events-Q3, events-Q12): when no watcher can wake this session (its host's
    reference), run `$CHANTIER watch --once --after <n>` at the start of each turn the user's
    message opens, say its `board wrote` lines as above and act on its merge lines as at a
    watcher's end, and keep its last line's cursor. A line whose `seq` was already told is not
    told again.
  - Entry row "rescan" (line 46): add "with a watcher running, the board's writes already came at
    its end; read the backlog again only when the user asks".
  - Handing the seat over (line 1683): the old watcher also ends by itself once the seat moves.
- **`skills/chantier/references/foreman.md`** (line 772): the `board:` version line of `status` is
  the Chief of Staff's too: do nothing with it, send nothing.
- **`skills/chantier/references/concepts.md`**, rule 8 (line 685): "and stops itself" becomes
  "and stops itself (at its end, or when the seat moves)".
- **`skills/chantier/references/hosts/claude-code.md`**: "Run the watcher" row: the command with
  `--seat <id>`, and its trial also a board move with no batch running and the session's turn
  that follows (unproved until then). "The watcher when the session ends": "An orphaned watcher
  ends once its project has no running batch" becomes "… ends once the project's seat names
  another session".
- **`skills/chantier/references/hosts/copilot.md`**, "Run the watcher": the command with `--seat
  <id>`; until the trial is recorded, the Chief of Staff also runs the pull path at each user
  message (events-Q12).
- The agent files (`agents/`, `com.github.copilot/agents/`) do not change.

### 5. `AGENTS.md`, `CONTRIBUTING.md`, docs

- **`AGENTS.md`**, the CLI's scope bullet:
  - The board's exception, after "which `status` prints for the Chief of Staff to record at its
    next `status`;": add "and each write it makes to the backlog or the configuration (not a dry
    run) also appends one line to that project's `forge-journal.jsonl`, which the Chief of Staff's
    watcher reads;".
  - The third exception: "each session's watcher reads only its project's journal, never the
    forge, and ends 20 s after the last new event, which wakes its session;" becomes "each
    session's watcher, run for the Chief of Staff's whole session, reads only its project's
    journal (the hub's lines and the board's writes), never the forge, and ends 20 s after the
    last new event that wakes, which wakes its session, or when the project's seat names another
    session;"; "one round trip with the user per merge." becomes "one round trip with the user per
    merge and per board session ("rescan").".
- **`CONTRIBUTING.md`** (lines 96-120): the same two edits, in its own words.
- **`docs/web-board.md`**: line 84 ("The board does not talk to the Chief of Staff: tell it
  'rescan'…") and line 162: a Chief of Staff whose watcher runs hears each write within about 20 s;
  "rescan" stays for one that runs none. The board's page and its texts do not change (nothing
  under `board/web/`).
- **`docs/planning-folder.md`** (line 49): `forge-journal.jsonl` also holds the board's writes.

## Out of scope

- The Griller started from the board, how it starts and what it says to the Chief of Staff
  (`2-backlog/P3/board-griller`). A later writer may add a `by` value and a kind through
  `hub/journal.py`; nothing here starts a Griller.
- Anything the hub delivered (forge reads, merges, `checks red`, the lock, its cadence).
- A comment feature in the board: a note is a file saved from its editor.
- A prompt hook, an MCP channel, a `Monitor`, or the plugin's mod as a wake path; no `hooks/` or
  `types/` change.
- Folding `board-journal.jsonl` into `forge-journal.jsonl`; any change to the board's page.
- A watcher for a Griller, a Foreman or a Driver; any message between two projects' sessions.
- Stopping or restarting a board of another version (the user's).
- `STATUS.md`, `STATUS.json`, the CR board pane; a version bump.

## Evidence

**Gates.** A change under the CLI's `src/` and the cards: before the first push, `just check` and
`just eval-dry-run` in the worktree at the rebased head; before the PR is ready, the pipeline's
`just scenario (ubuntu-latest)` job green at the PR's head, and the local `just scenario`
(`chantier gate`) when this CR is the top of its batch. No `just mod`, no pane screenshot, no
`DESIGN.md` (nothing under `board/web/`).

**Unit tests** (`cli/tests/`, in-process, few, parametrized, no sleep):

- `test_board.py`: one parametrized test over the write routes (`new`, `move`, `edit`, `label`,
  `group`, `ungroup`, `next-batch`): each success appends one `board` line to the project's
  `forge-journal.jsonl` with `by: board`, its `action`, `items`, `text` equal to the
  `board-journal.jsonl` line's, and the `wakes` of the table; a refused write and `rescan` append
  none; on a two-project surface the line lands in the written project's journal only.
- `test_board_config.py`: a saved change appends one `config` line with `wakes: true`; a dry run
  none.
- `test_forge_hub.py`:
  - `test_a_watcher_ends_twenty_seconds_after_the_last_event` gains cases (injected clock): a
    waking board line at 0 s ends at 20 s; a non-waking one alone never ends, and is printed at
    the end a later waking one causes; the batch paused or closed does not end it.
  - `test_watch_refusals`: no `--seat`; a seat that names another session or none; `--once`
    without `--after` or with `--seat`; nothing written. The no-running-batch refusal is gone.
  - New: the seat moved ends the watcher with its line; `--once` prints the lines above
    `--after` and the cursor line, with no `hub.json` written and the `forge_read.read` seam not
    called; the start line and `status` name a live board of another version, and not one of this
    version or a dead record.
  - `test_the_board_and_the_hub_share_the_journal_once` still holds with `board` lines between
    (they shift `seq`, never block a `merged` line).
- `status`: the `watch:` line for a paused batch, the `board:` version line, no `board wrote` line.

**Scenario** (`scenario/run_scenario.py`, unit `surface-board`, `scenario/README.md` bullets with
their unit; `test_scenario_coverage.py` passes):

- `board_writes`: a move through the API leaves one `board` line in `forge-journal.jsonl`
  (`git check-ignore` holds), and a refused move none.
- `forge_hub`: watchers start with `--seat`; the check that ends `watch: no running batch in demo;
  ended` (line 1903) becomes: demo's batch paused, demo's watcher keeps running; a board move on
  demo then ends it with its `board wrote (move)` line within the quiet; a board write on project
  `other` does not end demo's watcher; `seat take` by another session ends a running watcher with
  its seat line; `watch --once --after <n>` prints the same lines and the cursor.
- Windows: the same unit on the user's machine at the local gate.

**Host matrix** (the wake depends on the host; the times are constants, nothing configured):

| Cell | Result it must show | Proof |
|---|---|---|
| Claude Code, the user's yes, a board move with the session idle, no batch running | the session takes a turn within about 20 s and says the move in one line | the "Run the watcher" row's trial; until then the PR's Known gaps names "the main session's wake by a background watcher's end is unproved" |
| Claude Code, the session ended, another session takes the seat | the old watcher ends with the seat line | scenario (`seat take`), and the host row's trial |
| Copilot | `watch --once` at each user message says the board's writes; the watcher's own wake unproved | the Copilot row's trial |
| The user's no | as open question 2 decides | the same first session after the merge |

**After merge, on the hosts** (not a gate): the trials of the two host rows, recorded with dates.

## Open questions

1. **events-Q11's `no watch runs for project <name>` line.** It answered a `Monitor` that expires;
   the hub's watcher is a background command whose end always comes back to the session, which
   starts it again, and `status` already prints `forge hub:` and `watch:`. Options: (A) drop the
   line: no per-watcher record, nothing new in `status`; (B) each watcher records its PID per
   project in the git folder and `status` prints `no watcher runs for project <name>` when none is
   alive. Recommendation: A (the hub's design has no case where the watcher stops unseen; B adds a
   record for it). This specification is written on A.
2. **The board's writes after the user's no to the watcher.** hub-Q9's no starts nothing, and
   merges go back to the user's word. Options: (A) the pull path anyway: `watch --once` at each
   user message (no background process, no forge read, one short call per message); (B) nothing:
   the user's "rescan" as today. Recommendation: A (events-Q3's fallback; the no was to a process
   that runs on and reads the forge, and `--once` does neither). This specification is written on
   A in its cards (section 4, "The pull path": "when no watcher can wake this session" includes a
   session whose user said no).
