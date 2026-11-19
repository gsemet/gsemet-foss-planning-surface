# Change Specification: the watcher wakes the Chief of Staff on what the user does in the board

No tracker issue: the CR is verbal (the user, 2026-11-17, during batch-23).

**Stacks on two CRs** (`depends.json`), and rebases on their text whichever lands first:

- CR-375 `watcher-autostart` (`4-batch/1-pending/375-the-watcher-starts-on-its-own-with-a-run`):
  the per-session watcher lock (`chantier/watch-<project>/<session>.lock`, the session key from
  `own_transcript(detect_host())`), the helpers `watch_command(repo, n)` and
  `not_running_line(...)`, the `watch: not running: …` line at the end of `open`, `take`, `order
  qa`, the switch to direct mode and `status`, and the watcher's end line `watch: <batch> still
  running: …`.
- `config-spec-writers-slots` (`1-inbox/spec-writers-and-slots-set-from-the-boar`): the `config`
  line of `forge-journal.jsonl` (`by: "board"`, `kind: "config"`, `key`, `old`, `new`, `batch`),
  its `event_text`, its `status` lines and the Chief of Staff's acts for `batch.slots` and
  `specifying.parallel`.

The forge and merge part of this item was delivered by CR-358 `surface-forge-hub` (`a7f32370`,
`5717626d`): `chantier watch`, the hub's forge reads, merges recorded with no word from the user.
On main the board writes `board-journal.jsonl` only and the watcher reads `forge-journal.jsonl`
only, so no board write reaches a session. This specification keeps only the board's writes, puts
them in the hub's journal, and lets the watcher run with or without a batch.

## Goal

The user, 2026-11-17: a running Chief of Staff session hears nothing of what the user does in the
web board until the user says "rescan". An idea added to the inbox, a priority or a stage changed
(Triage, Kanban), a note saved on a CR from the board's editor, an agent, a model or an escalation
changed on the Configuration page: the Chief of Staff should be told within about 20 s, with no
word from the user, with or without a batch, on the same wake as the forge's merges. On a host
where nothing can wake the session, or after the user's no to the watcher, the events wait in the
journal and the Chief of Staff reads them at the user's next message. One planning surface holds
several projects, each with its own Chief of Staff and one board for all: each Chief of Staff
hears only its own project's board writes.

The measured cost it removes: one round trip with the user per board session ("rescan", "I
updated the priorities", the `chief-of-staff.md` entry row for it), and a Chief of Staff that
plans on a stale backlog when the user forgets it.

## Decisions carried (from `02-answers.md`)

| Answer | Decision | Where below |
|---|---|---|
| events-Q1, as re-scoped by hub-Q8 | The board's writes go into the hub's journal and wake the session through the hub's watcher (its background end), not a `Monitor` | 1, 2 |
| events-Q2 | Wake on: a priority or stage changed, an item added to the inbox, a note on a CR (a file saved from the board's editor), a Configuration change. Grouped into one wake (the watcher's 20 s quiet). No wake for opening a page or text being typed. Labels, groups, ungroup and next batch do not wake and ride along with the next wake | 1, 2 |
| events-Q3 | Where nothing wakes the session: the events wait in the journal; the Chief of Staff reads them at the user's next message, and says once at the session's start that this host does not wake it; today's pull path, no look-alike tool | 2 (`--once`), 4 |
| events-Q5, widened by the spec critic's settlement | Woken, the Chief of Staff acts alone on merges (the hub's rule) and on a `config` line of the config CR's two keys (`batch.slots`: `order slots --note <n>`; `specifying.parallel`: the spec-writer limit), as that CR says. Any other `config` line (agent, model, escalation) and every `board` line: one line to the user, no action | 1, 4 |
| events-Q6 (settled again 2026-11-18) | The watcher runs for the whole session, with or without a batch, running or paused; the forge is read only while a PR of a running batch is open (the hub's rule, unchanged) | 2, 3, 4 |
| events-Q8 | Two CRs: this one holds the events; the Griller started from the board is `2-backlog/P3/board-griller` | Out of scope |
| events-Q9 | A board of another chantier version is named, once, by the watcher's start line and by `status`, with "restart it"; the forge is still read, merges still seen | 2, 3, 4 |
| events-Q10, as re-scoped by hub-Q8 | No `Monitor`, so no `Monitor` rule: the watcher is a shell command already covered by P10's `chantier *` rules; nothing changes in `permissions.py` | Settled in `02-answers.md` |
| events-Q11, settled (former open question 1, answer A) | No `no watch runs for project <name>` line and no per-watcher PID record of this CR: `status`'s `forge hub:` line and CR-375's `watch:` lines (this session's watcher, another session's, or `watch: not running`) cover it | 3 |
| events-Q12 | Copilot: a watcher's wake is unproved there; until it is, the Chief of Staff also runs the pull path (`watch --once`) at each user message, said once at the session's start | 2, 4 |
| Pull path after a no (former open question 2, answer A) | After the user's no to the watcher, the Chief of Staff runs the pull path `watch --once` at each user message (no background process, no forge read) | 2, 4 |
| Several projects on one surface | Each board write lands in its own project's journal only; a watcher reads only its project's journal | 1, Evidence |
| hub-Q8 | Same journal (`forge-journal.jsonl`), same `watch` | 1, 2 |
| hub-Q9 | The user's yes once per session before the watcher starts; now asked at every Chief of Staff session's start (events-Q6), the question naming the board's writes too | 4 |
| One kind of line per configuration change (Chief of Staff, 2026-11-18; spec critic, answer A) | A Configuration save writes the config CR's `config` line (key, old, new), for every key: the two limits and each role's `agent`, `model` and `escalation`; never a second kind | 1 |
| On top of CR-375 (spec critic, answer A) | No `--seat` flag: the watcher's session is CR-375's key from the environment; the seat end compares it with `seat.json`; CR-375's `watch: not running` and `still running` lines print whatever the batch's status; the `no running batch` end and refusal are removed; the command is always taken from a printed line | 2, 3, 4 |
| Orphaned watcher (spec critic, answer A) | An ended session's watcher may run until another session takes the seat, until the Claude Code trial says whether the host ends it; the PR's Known gaps names it and the host row records the trial | 2, 4, Evidence |

## What changes

All paths are in chantier's repository; `cli/` is `skills/chantier/scripts/cli/`, and
`chantier/` is `cli/src/chantier/`. Keep every card edit outside the cards' "Startup core"
sections, and leave `skills/chief-of-staff/SKILL.md` as CR-375 leaves it: the startup reading
budget (12,544) is not touched.

### 1. The journal: what the board writes in `forge-journal.jsonl`

`chantier/hub/journal.py` is the journal's one module. Its docstring and the package docstring of
`chantier/hub/__init__.py` say the board writes two kinds of line there, both `by: "board"`:

- `merged`, from its PRs page (as today, unchanged);
- its write lines: `board` (a backlog write, new here) and `config` (a Configuration save, the
  config CR's line, here extended to every key).

`by` says who wrote a line, never what it is: every reader dispatches on `kind`.

- **`_key` keyed on `kind`.** `checks-red` and `merged` keep today's keys, and the `merged` key
  applies to `kind == "merged"` only (today every kind other than `checks-red` falls into the merge
  branch). A `board` or `config` line gets a key no other line shares, so `append` writes each one
  (two identical moves, or two saves of the same value, are two lines). The config CR's own dedup
  key, if it lands first, is replaced by this rule.
- **The `board` line.** `{"seq", "t", "by": "board", "kind": "board", "action", "items", "text",
  "wakes"}`: `action` is the board journal's kind (`new`, `move`, `edit`, `label`, `group`,
  `ungroup`, `next-batch`), `items` and `text` the slugs and words of the `board-journal.jsonl`
  line written in the same call, `wakes` a boolean from this table (events-Q2):

  | `action` | Board write | `wakes` |
  |---|---|---|
  | `new` | an idea added to the inbox | true |
  | `move` | a priority or a stage changed, one item or a group | true |
  | `edit` | a CR's file saved from the board's editor (the board's way to leave a note) | true |
  | `label`, `group`, `ungroup`, `next-batch` | not in events-Q2's list | false |

  A Configuration save is never a `board` line: it is a `config` line.
- **The `config` line, for every key.** The config CR's shape, unchanged (that CR writes it for its two limit keys only, one line per changed key; this CR adds the role keys): `{"seq", "t", "by":
  "board", "kind": "config", "key", "old", "new", "batch"}`, `old` and `new` the effective values
  before and after the save (all layers), `batch` the running or paused batch at the save, or
  `null`. `key` is the dotted path the save changed:
  - the config CR's two keys, `batch.slots` and `specifying.parallel`;
  - a role's key, `hosts.<host>.roles.<role>.<agent|model|escalation>`, its values the
    `effective` of `config_view`'s row (`playbook/edit.py`) before and after (for `escalation`,
    the value `escalation.row` names as applying). `null` when nothing applies.

  Every `config` line wakes.
- **Text** (`event_text`, the one function the watcher's output uses):
  - `board`: `board wrote (<action>): <text>; for the Chief of Staff: tell the user, act on
    nothing`.
  - `config` of the two keys: the config CR's texts, unchanged.
  - `config` of a role's key: `config changed on the board: <key> <old> -> <new>; applies at the
    next batch; for the Chief of Staff: tell the user, act on nothing` (`inherited` for a `null`).
  - `merged` and `checks-red`: unchanged.
- **`lines()`** (the `status` lines): the `merged` lines and the config CR's `batch.slots` line,
  as that CR says; never a `board` line, never a `config` line of `specifying.parallel` or of a role's key.
- **The writers.**
  - `chantier/board/write_api.py`, `_answer`: when it writes its `board-journal.jsonl` line
    (something was written), it also appends one `board` line through `hub.journal.append(repo,
    [...], "board")`, same kind, slugs and words. A refused write writes none; `rescan` writes
    none; reading or opening a page writes nothing.
  - `chantier/board/config_api.py`, `_put`, on a real save (never a dry run): one `config` line
    per key whose effective value the save changed, through the same function the config CR adds
    for its two keys; a key left at its effective value writes none. A save of one change (the
    Models tab's agent, model or escalation of one role, or one limit) is one line. The board
    journal's `config` line and the response lines stay (`applies at the next batch` for a role's
    key; the config CR's lines for its two).
  - The project is the route's own (`project.repo`): a write on project `other` lands in
    `projects/other/changes/forge-journal.jsonl` only.
- `board-journal.jsonl`, its dialog and its `rescan` are unchanged: the journal line is written in
  addition, not instead.

### 2. `chantier watch`

`chantier/declare/watch.py` and `chantier/hub/watch.py`, as CR-375 leaves them.

```
chantier watch [--after SEQ]
chantier watch --once --after SEQ
```

- **No `--seat` flag.** The watcher's session is CR-375's key (`own_transcript(detect_host())`,
  kept to `[A-Za-z0-9-]`, else `none`), read from its own environment, the key its lock already
  carries.
- **No batch needed** (events-Q6). The refusal `watch: no running batch in <project>: nothing to
  watch` and the end `watch: no running batch in <project>; ended` (`Watch.lines`, reason
  `no-batch`) are removed: the watcher runs with a running, paused or no batch. The hub's cycle is
  unchanged (`hub/cycle.py`: running batches with a PR the record does not hold merged or
  cancelled), so with no running batch it reads the forge for no project of its own.
- **Its ends.**
  - *Events.* From the first new line that wakes (`merged`, `checks-red`, `config`, or `board`
    with `wakes: true`), it ends once `quiet_s()` (20 s) has passed with no newer waking line, as
    today. A `board` line with `wakes: false` neither starts nor extends that wait; it is carried
    and printed at the next end. The end's last line is CR-375's `watch: <name> still running: for
    the Chief of Staff, start again in the background now: <watch_command(repo, n)>`, printed
    whatever the batch's status: `<name>` is the project's running or paused batch, else
    `<project> (no batch)`.
  - *The seat moved.* About every 10 s (the board's `SEAT_CHECK_S`, `board/seats.py`; reuse the
    constant), the watcher reads `seat.json` (`core/seat.py`, `read_seat`). When the seat records
    a `transcript` that, kept to `[A-Za-z0-9-]` as CR-375 keeps its key, is not the watcher's own
    key, the watcher prints its new lines, then `watch: the seat of <project> is another session's
    now; ended`, and exits 0, with no restart line. No seat, a seat with no `transcript`, or a
    watcher whose key is `none`: no seat end (nothing to compare). This is what stops a watcher
    left behind by an ended session, once another session takes the seat.
- **Start line** (events-Q9): `watch: <project> from cursor <n>` with `, the hub` or `; hub is
  chantier <v>` as today, then `; board is chantier <v>: its writes do not reach this watcher,
  restart it` when the board's running record (`board/running.py`, `live(key_path(repo))`) is live
  and its `version` is not this CLI's `__version__`. No live record: nothing said. The watcher goes
  on either way.
- **`--once`** (the pull path: events-Q3, events-Q12, and after the user's no): prints, for every
  journal line whose `seq` is above `--after` (waking or not), its `event_text`, then `watch:
  cursor <seq>; next, at the user's next message: <cli_command(repo)> watch --once --after <seq>`
  (the cursor unchanged when nothing is new), and exits 0. It takes no lock (neither the hub's nor
  CR-375's watcher lock, so it never counts as a running watcher), is never the hub, reads no
  forge, needs no seat and no batch, and starts no process. `--once` without `--after`: exit 1
  (`EXIT_USAGE`). `--after` past the journal's end: today's refusal, in both forms.
- **The printed pull command.** So that the pull path's first command is also printed, never
  built: CR-375's `watch: not running: for the Chief of Staff, start in the background: <command>`
  gains a second clause, `; after the user's no, at each user message: <cli_command(repo)> watch
  --once --after <n>` (same `n`); and `status`'s line for a running watcher of this session
  (CR-375's kept `watch: chantier watch --after <n>`) becomes `watch: this session's watcher runs;
  pull path: <cli_command(repo)> watch --once --after <n>`, so the Copilot pull path (events-Q12)
  has its command while its watcher runs. Both from one helper next to `watch_command`.
- The help text names the board's writes next to the forge events, and the seat end.

### 3. Where the `watch: not running` line prints, and `status`

CR-375's `not_running_line` no longer takes the batch's status: it returns its line whenever no
watcher of this session runs (events-Q6), `[]` when one does.

- CR-375's outputs keep it, now whatever the batch's status: `open` (a batch born paused
  included), the `take` or `order qa` that sets a paused batch running, the switch to direct mode,
  and `status` of a running or paused batch.
- New, so a session with no batch gets the printed command: `seat take` and `seat` (`get`)
  (`commands/seat.py`, `_take`, `_get`) end with the line when the seat's `transcript`, kept as
  CR-375 keeps its key, is this CLI run's own key (the seat is this session's). A seat of another
  session, or none: no line (a Griller reading the seat sees none).
- `status` (`chantier/commands/batch_status.py`, `_watch_lines`, as CR-375 leaves it): the
  `forge hub:` line stays for a running batch only; the lines for this session's watcher (the
  `pull path` line above), another session's watcher, or none (the `watch: not running` line last)
  print for a paused batch too. With no batch running or paused, `status` refuses as today; the
  line then comes from `seat`.
- events-Q9: a new line, whatever the batch's status, when the board's running record is live and
  of another version: `board: chantier <v> serves this surface, this is chantier <w>: its writes do
  not reach the watcher; for the Chief of Staff: tell the user once to restart it`.
- No `board` line, and no `config` line but the config CR's `batch.slots` one, is printed by `status` (it is the
  Foreman's heartbeat too). `STATUS.md`, `STATUS.json` and the CR board pane do not change.

### 4. The cards

Every command the cards name for the watcher or the pull path is "the printed command" (CR-375's
sentence, word for word: run the printed command as is: no flag added); no card builds a command
or states an `--after` rule.

- **`skills/chantier/references/session-start.md`, "The watcher"** (~line 97, as CR-375 leaves
  it): a Chief of Staff asks at its session's start whatever the batch, on the `watch: not
  running` line of `seat take` (or of any output later); the question also says the watcher tells
  it, within about 20 s, what the user does in the board. A yes: start it by the host's means; run
  the printed command as is: no flag added. A no: no process for the session, merges go back to
  the user's word, and the pull path (the line's `after the user's no` command) runs at each user
  message. On a host whose reference says a watcher's end does not wake the session, or is not
  proved to (Copilot today, events-Q12), say once, in the user's language: "This host may not wake
  me: what you do in the board reaches me at your next message."
- **`skills/chantier/references/chief-of-staff.md`**
  - "The watcher" (~line 1220, as CR-375 leaves it): it prints the forge events and the board's
    writes; it ends 20 s after the last one that wakes, or when the seat is another session's. *When
    it starts*: whatever the batch, running, paused or none (events-Q6); its end's `still running`
    line names the restart. Remove "A watcher that ends with `no running batch` is not started
    again" and "a paused batch prints no line" (CR-375's text); add "A watcher that ends with `the
    seat of <project> is another session's now` is not started again: the seat moved". *A
    watcher's end*: a `board wrote` line, or a `config changed on the board` line of a role's key:
    one line to the user that says it (a few words per event), no tool call, no action
    (events-Q5); a `config` line of `batch.slots` or `specifying.parallel`: as the config CR
    says; the merge and `checks red` rules unchanged. The `board:` version line of `status` and
    the start line's `board is chantier <v>`: say it once to the user with the restart; never stop
    or restart the board yourself.
  - The pull path (events-Q3, events-Q12, the user's no): when no watcher can wake this session
    (its host's reference, or the user's no), run the printed `watch --once` command at the start
    of each turn the user's message opens (from the `watch: not running` line, `status`'s `pull
    path` line, or the last `--once` output's `next` line); tell its `board wrote` and role
    `config` lines as above and act on its merge and two-key `config` lines as at a watcher's end.
    A line whose `seq` was already told is not told again.
  - Entry row "rescan" (~line 46): add "with a watcher or the pull path running, the board's
    writes already came; read the backlog again only when the user asks".
  - Handing the seat over (~line 1683): the old watcher ends by itself once the new session takes
    the seat.
- **`skills/chantier/references/foreman.md`** (~line 772): the `board:` version line and the
  `pull path` line of `status` are the Chief of Staff's: do nothing with them, send nothing.
- **`skills/chantier/references/concepts.md`**, rule 8 (~line 685): "and stops itself" becomes
  "and stops itself (at its end, or when the seat is another session's)".
- **`skills/chantier/references/hosts/claude-code.md`**:
  - "Run the watcher": the command the `watch: not running` or `still running` line prints (as
    CR-375 says); its trial also covers a board move with no batch running and the session's turn
    that follows (unproved until then).
  - "The watcher when the session ends": "An orphaned watcher ends once its project has no running
    batch" becomes "An orphaned watcher ends once the project's seat is another session's; until
    the trial says whether the host ends it with the session, one may run until then (accepted)";
    the trial, when run, records its date and result in this row.
- **`skills/chantier/references/hosts/copilot.md`**, "Run the watcher": until the trial is
  recorded, the Chief of Staff also runs the pull path at each user message (events-Q12), from the
  printed command.
- The agent files (`agents/`, `com.github.copilot/agents/`) and `skills/chief-of-staff/SKILL.md`
  do not change.

### 5. `AGENTS.md`, `CONTRIBUTING.md`, docs

- **`AGENTS.md`**, the CLI's scope bullet:
  - The board's exception, after the config CR's text on its `config` line: the `config` line is
    written for each key the board saves (the two limits, and each role's agent, model and
    escalation), and "each write it makes to the backlog also appends one `board` line to that
    project's `forge-journal.jsonl`, which the Chief of Staff's watcher reads;".
  - The third exception: "each session's watcher reads only its project's journal, never the
    forge, and ends 20 s after the last new event, which wakes its session;" becomes "each
    session's watcher, run for the Chief of Staff's whole session, with or without a batch, reads
    only its project's journal (the hub's lines and the board's), never the forge, and ends 20 s
    after the last new event that wakes, which wakes its session, or when the project's seat is
    another session's;"; "one round trip with the user per merge." becomes "one round trip with
    the user per merge and per board session ("rescan").".
- **`CONTRIBUTING.md`** (~lines 96-120): the same edits, in its own words.
- **`docs/web-board.md`**: ~line 84 ("The board does not talk to the Chief of Staff: tell it
  'rescan'…") and ~line 162: a Chief of Staff whose watcher or pull path runs hears each write;
  "rescan" stays for one that runs neither. The board's page and its texts do not change (nothing
  under `board/web/` beyond the config CR's).
- **`docs/planning-folder.md`** (~line 49): `forge-journal.jsonl` also holds the board's writes.

## Out of scope

- The Griller started from the board, how it starts and what it says to the Chief of Staff
  (`2-backlog/P3/board-griller`). A later writer may add a kind through `hub/journal.py`; nothing
  here starts a Griller.
- Anything the hub delivered (forge reads, merges, `checks red`, the lock, its cadence).
- What the config CR delivers for its two keys (the Limits tab, `order slots --note <n>`, the spec-writer
  limit), beyond widening its `config` line to every key.
- A comment feature in the board: a note is a file saved from its editor.
- A prompt hook, an MCP channel, a `Monitor`, or the plugin's mod as a wake path; no `hooks/` or
  `types/` change.
- Folding `board-journal.jsonl` into `forge-journal.jsonl`; any change to the board's page.
- A watcher for a Griller, a Foreman or a Driver; any message between two projects' sessions.
- Stopping an orphaned watcher by other means than the seat end (a PID record, a kill); stopping
  or restarting a board of another version (the user's).
- The startup reading budget and `skills/chief-of-staff/SKILL.md`; `STATUS.md`, `STATUS.json`, the
  CR board pane; a version bump.

## Evidence

**Gates.** A change under the CLI's `src/` and the cards: before the first push, `just check` and
`just eval-dry-run` in the worktree at the rebased head; before the PR is ready, the pipeline's
`just scenario (ubuntu-latest)` job green at the PR's head, and the local `just scenario`
(`chantier gate`) when this CR is the top of its batch. No `just mod`, no pane screenshot, no
`DESIGN.md` (nothing under `board/web/`).

**Known gaps** the PR names until the trials run: "the main session's wake by a background
watcher's end is unproved" and "an ended session's watcher may run until another session takes
the seat (the Claude Code trial says whether the host ends it)".

**Unit tests** (`cli/tests/`, in-process, few, parametrized, no sleep; `just test` within its
budget):

- `test_board.py`: one parametrized test over the write routes (`new`, `move`, `edit`, `label`,
  `group`, `ungroup`, `next-batch`): each success appends one `board` line to the project's
  `forge-journal.jsonl` with `by: "board"`, its `action`, `items` and `text` equal to the
  `board-journal.jsonl` line's, and the table's `wakes`; two identical moves append two lines; a
  refused write and `rescan` append none; on a two-project surface the line lands in the written
  project's journal only.
- `test_board_config.py`, parametrized over a role's `agent` change, a role's `model` change,
  `batch.slots` and `specifying.parallel`: a real save of one change appends exactly one line of
  the config CR's shape (`by: "board"`, `kind: "config"`, `key` the dotted path, `old` and `new`
  the effective values, `batch`); a second identical save appends a second line; a dry run
  appends none.
- `test_forge_hub.py`:
  - `_key`: a `merged` line by the board and one by the hub share a key (one written); `board` and
    `config` lines are never deduplicated; a `board` line never blocks a `merged` line
    (`test_the_board_and_the_hub_share_the_journal_once` still holds with `board` lines between).
  - `event_text` of a `board` line and of a role's `config` line; `lines()` holds neither.
  - `test_a_watcher_ends_twenty_seconds_after_the_last_event` gains cases (injected clock): a
    waking `board` line at 0 s ends at 20 s; a non-waking one alone never ends, and is printed at
    the end a later waking one causes; a role's `config` line ends it; with the batch paused, or
    none, it still ends on events, and its last line is the `still running` line with the batch's
    name, or `<project> (no batch)`.
  - The seat end: `seat.json` recording another session's `transcript` ends the watcher with its
    seat line and no restart line; a seat of its own session, a seat with no `transcript`, no
    seat, or a watcher keyed `none`: no seat end.
  - `test_watch_refusals`: the no-running-batch refusal is gone; `--once` without `--after`:
    exit 1; nothing written.
  - `--once`: prints the lines above `--after` (waking or not) and the cursor line with the
    printed `next` command; no `hub.json` written, the `forge_read.read` seam not called, no
    watcher lock taken (CR-375's `watchers` stays `[]` while it runs).
  - The start line and `status` name a live board of another version, and not one of this
    version or a dead record.
- The printed lines (CR-375's parametrized output test, extended): the `watch: not running` line,
  with its `after the user's no` clause, ends `open` of a batch born paused and `status` of a
  paused batch; it ends `seat take` and `seat` when the seat is this session's (session set
  through the host's environment variable) and no watcher of this session runs, and is absent
  for another session's seat; `status` with this session's watcher holds the `pull path` line;
  no `board wrote` line in `status`.

**Scenario** (`scenario/run_scenario.py`, unit `surface-board`, `scenario/README.md` bullets with
their unit; `test_scenario_coverage.py` passes):

- `board_writes`: a move through the API leaves one `board` line in `forge-journal.jsonl`
  (`git check-ignore` holds), and a refused move none; a model change through the Configuration
  PUT leaves one `config` line.
- `forge_hub`: the check that ends `watch: no running batch in demo; ended` (~line 1903) becomes:
  demo's batch paused, demo's watcher keeps running; a board move on demo then ends it with its
  `board wrote (move)` line within the quiet and the `still running` line; a board write on
  project `other` does not end demo's watcher; `seat take` by another session (another
  `CLAUDE_CODE_SESSION_ID` in its environment) ends a running watcher with its seat line; the
  printed `watch --once --after <n>` command prints the same lines and the cursor line.
- Windows: the same unit on the user's machine at the local gate.

**Host matrix** (the wake depends on the host; the times are constants, nothing configured):

| Cell | Result it must show | Proof |
|---|---|---|
| Claude Code, the user's yes, a board move with the session idle, no batch running | the session takes a turn within about 20 s and says the move in one line | the "Run the watcher" row's trial; until then the PR's Known gaps names it |
| Claude Code, the session ended, another session takes the seat | the old watcher ends with the seat line | scenario (`seat take`); whether the host ends it earlier: the "watcher when the session ends" row's trial, recorded there; until then Known gaps |
| Copilot | the printed `watch --once` at each user message says the board's writes; the watcher's own wake unproved | the Copilot row's trial |
| Any host, the user's no | no process; the printed `watch --once` at each user message says the board's writes and the merges | unit tests of `--once`; the first session after the merge |

**After merge, on the hosts** (not a gate): the trials of the host rows, recorded with dates in
`hosts/claude-code.md` and `hosts/copilot.md`.

## Open questions

None for behaviour. One for the Chief of Staff to confirm, a means rather than a behaviour: with
no batch, the printed command comes from `seat take` and `seat` (section 3), since `status`
refuses with no batch; and the pull path's first command is printed by a second clause of CR-375's
`watch: not running` line and by `status`'s `pull path` line (section 2), so that no card builds a
command.
