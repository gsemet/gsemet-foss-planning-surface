# The CLI wakes the Chief of Staff on board and forge events

## Goal

The user, 2026-11-17: a running Chief of Staff session hears nothing until its next `status`. A
priority changed in the board, an idea added, a note saved on a CR, a model changed on the
Configuration page, a PR merged on the forge: the session should be told when it happens, on
Claude Code by a line that wakes it, and on a host where nothing can wake a session, at the user's
next message or the next `status`, as today. One planning-surface checkout holds several projects,
each with its own Chief of Staff and one board for all: each Chief of Staff hears only its own
project, and two Chiefs of Staff never record each other's merges.

The Griller started from the board is the separate CR `1-inbox/board-griller`, which waits for
this one (events-Q8). This CR only keeps that CR possible (see "What this leaves open for
`board-griller`").

## Decisions carried (from `02-answers.md`)

| Answer | Decision | Where below |
|---|---|---|
| events-Q1 | The Chief of Staff runs `chantier watch` with Claude Code's `Monitor`; one printed line wakes the session. The board writes its events to `board-events.jsonl`, which the watch reads; the watch also reads the forge (about every 60 s) and reports a merge it sees | A, B, C |
| events-Q2 | Wake on: a priority or stage changed (Triage, Kanban), an item added to the inbox, a comment or note on a CR, a merge seen on the forge, a Configuration change (agent or model). Grouped over about 30 s into one wake-up. No wake for opening a page or for text being typed. What it does not list (labels, groups, ungroup, next batch) does not wake and rides along with the next wake-up (settled after the spec critic) | A, B |
| events-Q3 | Where nothing can wake the session, events wait in the file, the Chief of Staff reads and summarises them at the user's next message or the next `status`, and says at the session's start that this host does not wake it. This is today's pull path, not a look-alike tool | C, D, E |
| events-Q5 | Woken, the Chief of Staff acts alone on merges only: checks the merge on the forge, records it (`order merged`), tells the Foreman, without waiting for the user's "merged". Any other event: one line to the user, no action | D |
| events-Q6 | The watch runs for the whole session, with or without a batch: started at the session's start, started again at the next turn if it stopped or expired, ended with the session. The forge is read only while a PR of the batch is open. This widens AGENTS.md's forge rule | B, F |
| events-Q8 | Two CRs: this one (watch, events file, wake-up, forge, fallback); `board-griller` holds the Griller | Out of scope |
| events-Q9 | A board of another chantier version: the watch and `status` read the board's version in `board.json` (CR-323's record) and say once "the board is chantier <v>: its writes do not reach me; restart it". The watch keeps reading the forge, so merges are still seen | B, C, D |
| events-Q10 | A `Monitor` rule for `chantier watch` joins P10's "Every batch" row, added on the user's yes like P10's other rules, unproved until a trial. A start the host still refuses (auto mode's classifier): the session runs the pull path and says so once | D, E |
| events-Q11 | `status` prints `no watch runs for project <name>` whenever no watch of that project is alive (its PID in `watch.json`); the Chief of Staff then starts it again. This covers a `Monitor` that expires | C, D |
| events-Q12 | Copilot: the CR names a trial to find the tool that wakes a Copilot session; until it is proved, Copilot runs the pull path (`watch --once` at each user message), said once at the session's start | D, E |
| Grilled enough | The spec checks whether a `Monitor` expires and which tool wakes a Copilot session: settled by events-Q11 and events-Q12, with the trials of E | E |
| Several projects on one surface | Each event names its project; a Chief of Staff's watch wakes it only for its own project's events and reads the forge only for its own project's repository; two Chiefs of Staff on one surface never record each other's merges | A, B, D |

## What changes

All paths are in chantier's repository; `cli/` is `skills/chantier/scripts/cli/`, and
`chantier/` is `cli/src/chantier/`.

**On top of CR-323** (`4-batch/1-pending/323-two-sessions-one-machine`, in batch-23), which edits
some of the same places: rebase on it and keep both texts. The shared places are named where they
come: `AGENTS.md` (first bullet), `skills/chantier/references/session-start.md` ("The board"),
`skills/chantier/references/chief-of-staff.md`, `docs/web-board.md` ("The link"),
`docs/planning-modes.md` ("Two sessions on one surface"), `chantier/commands/batch_status.py`
(`status()`, CR-323's "other batches" line), and the scenario's `external_surface` unit. This CR
also reads CR-323's `running` record in `board.json` (events-Q9).

### A. The events file: `board-events.jsonl`, per project, local

**Where.** At the root of the project's planning folder (`repo.changes`):
`<surface>/projects/<name>/changes/board-events.jsonl` on a planning surface,
`.agents/changes/board-events.jsonl` in-project. One file per project, so a project's events are
never in another's file, whichever session or board wrote them. Local, never published: added to
`IGNORED` in `chantier/core/files.py` (the planning folder's own `.gitignore`, which
`ensure_gitignore` completes), like `board-journal.jsonl`.

**It replaces `board-seen.jsonl`.** The merge signal of CR-303 becomes one kind of event in
`board-events.jsonl`; `board-seen.jsonl` is no longer written or read. `chantier/board/seen.py`
is removed; its read and its once-per-(batch, CR) merge signal move to a new module
`chantier/events/store.py`, which the board, the watch and `status` share. `board-seen.jsonl`
stays in `IGNORED` so a file left by an older version is never published; a merge noted only
there is not lost, as the forge still shows it merged and the record does not: the next forge
read (the board's PRs page or the watch) writes it again as an event. `chantier/board/fingerprint.py`,
`SINGLE`: `board-seen.jsonl` becomes `board-events.jsonl`.

`board-journal.jsonl` stays as it is (the board's journal dialog and its "rescan"): the events
file is written in the same call that writes a journal line, not instead of it.

**One line per event**, a JSON object, UTF-8, appended whole under the lifecycle lock
(`changes_lock`, as `journal._append` does):

```json
{"t":"2026-11-17T10:00:00Z","project":"chantier","source":"board","kind":"move","wakes":true,"items":["foo"],"text":"foo: priority P2 → P1"}
{"t":"2026-11-17T10:01:00Z","project":"chantier","source":"watch","kind":"merged","wakes":true,"batch":"batch-24","cr":"CR-330","pr":"https://github.com/gsemet/chantier/pull/412","into":"main","into_cr":null,"merged_at":"2026-11-17T10:00:40Z","text":"..."}
```

- `project` is the project's id as the board names it (`board/projects.py`, `project_name`):
  the folder's name under `projects/`, else the repository folder's.
- `source`: who wrote the line, `board` or `watch` in this CR. `events/store.py` is the one
  writer's entry; a later CR may add a writer and a `source` value through it.
- `text`: the words the watch prints for this event (for a board write, the journal's words).
- `wakes`: whether the event wakes the session alone. The watch prints the `text` of any kind
  and any source, and wakes on `wakes`, so a new kind or a new source needs no change to the
  watch.

**The board's writes** (`chantier/board/write_api.py`, `_answer`; `chantier/board/config_api.py`,
`_put`): each journal line written there also appends one event, same kind, items and words. The
kinds and whether each wakes (events-Q2):

| Kind | Board action | Wakes |
|---|---|---|
| `new` | an idea added to the inbox | yes |
| `move` | a priority or a stage changed (Triage, Kanban), one item or a group | yes |
| `edit` | a CR's file saved from the board's editor: the board's only way today to leave a comment or a note on a CR; nothing is written while the text is being typed | yes |
| `config` | a role's agent or model changed on the Configuration page (not a dry run) | yes |
| `label`, `group`, `ungroup`, `next-batch` | not in events-Q2's list | no: written, and carried in the next wake-up's line and in `watch --once` |

A refused write writes no event (it writes no journal line today). The journal's `rescan` is not
an event. Opening or reading a page writes nothing.

**The board's PRs page** (`chantier/board/prs.py`, `answer`): a fresh forge read that finds a PR
merged that the record does not hold appends a `merged` event (`source: board`) through
`events/store.py`, once per batch and CR across both sources: a merge the watch already wrote is
not written again, and the reverse. The fields are those of `board-seen.jsonl` today (`batch`,
`cr`, `pr`, `into`, `into_cr`, `merged_at`). Its `text`:

- into the default branch: `merged on the forge: <cr> <pr> into <branch> at <time>; for the Chief of Staff: check it, then order merged <cr>`;
- into another CR's branch: `merged on the forge: <cr> <pr> into <other cr>'s branch at <time>; not landed: tell the user, record nothing until <other cr> lands`.

The page's own row text (`MERGED_NOT_RECORDED`) is unchanged.

### B. `chantier watch`

A new command, declared in `chantier/declare/watch.py` (registered in `cli.py`'s list, `NO_BATCH`:
it reads the project's open batch itself when there is one), run by
`chantier/events/watch.py`. It takes the root `--project` like every command, so on a surface it
serves the one project `$CHANTIER` names.

```
chantier watch [--seat SESSION] [--once] [--group SECONDS] [--forge-every SECONDS]
```

- `--seat SESSION`: the Chief of Staff session it is for. The watch starts only when the
  project's `seat.json` names that session (else `error: watch not started: the seat names
  <other>, not <SESSION>`, exit 2, `EXIT_PRECONDITION`), and it stops when the seat no longer
  names it, checked every 10 s (as the board's `SEAT_CHECK_S`), with one last line `chantier
  watch, project <name>: stopped, the seat names <other> now`, exit 0. So a watch the host leaves
  running after its session ended still stops once another session takes the seat.
- `--group` (default 30) and `--forge-every` (default 60): the grouping window and the forge
  read's interval, in seconds; the scenario shortens them. Values below 1 are refused (exit 1,
  `EXIT_USAGE`).
- `--once`: the pull path (C).

The watch never reads its standard input: a `Monitor` or a background shell may give it a null
one, and its end is not a stop.

**What the running watch does.**

1. **One watch per project.** It keeps its process and its place in `watch.json` at the planning
   folder's root (local, added to `IGNORED`): `{"schema": 1, "read": <whole lines of
   board-events.jsonl already printed>, "forge_read_at": <UTC> | null, "running": {"pid",
   "started", "session"} | null}`, written whole (`write_json`). A record counts as running only
   when its process lives and is the one recorded (`procs.alive_since(pid, started,
   unreadable=True)`, as CR-323 does for the board).
   - A live watch for the same session: the new one prints `chantier watch, project <name>:
     already running (PID <pid>)` and exits 0.
   - A live watch for another session: the new one waits up to 15 s for it to stop by the seat
     rule; if it still runs, `error: watch not started: a watch for project <name> (PID <pid>,
     session <id>) still runs: stop it (<stop command>), then run watch again`, exit 4
     (`EXIT_EXTERNAL`). The stop command is the platform's (`taskkill /PID <pid> /T /F` on
     Windows, `kill <pid>` elsewhere); the CLI only prints it and never stops a process.
   - It stops on the seat rule, on Ctrl-C, or by the host's stop of its background command (a
     process ended hard leaves its `running` record, which the liveness check above treats as
     none). On a stop it handles, it clears `running` when it still names its own PID.
2. **The events.** It polls the size of `board-events.jsonl` every 2 s (no file-notification
   library). New whole lines after `read` whose `project` is its own are taken; a line of another
   project (none is expected in a project's own file) or an unreadable line is skipped and
   counted, never printed as an event. On the first new line with `wakes: true` it waits
   `--group` seconds, then prints **one line** for everything new (waking or not), then advances
   `read`. Lines that do not wake wait for the next waking one. A file cut shorter than `read`
   (the user removed it) resets `read` to its current end, with no line.
   At its start, lines already waiting after `read` are taken the same way: what came while no
   watch ran is said at once.
3. **The forge.** Only while the project's open batch (running or paused) has a CR with a PR that
   the record does not hold merged or cancelled and the last read did not show merged or closed:
   at most once every `--forge-every` seconds (`forge_read_at`), one call through the board's own
   reader (`chantier/board/forge_read.py`, `read`: one `gh api graphql` or `glab api graphql`
   query, read-only, the user's own login), for that project's PRs only, so for that project's
   repository only. A merge the record does not hold is appended as a `merged` event
   (`source: watch`) through `events/store.py`, then printed by step 2. With no open batch or no
   open PR, nothing is read. A failed read prints `chantier watch, project <name>: forge not read:
   <the forge's one line>` once per distinct error, then retries at the same interval with no
   line until it succeeds or the error changes.
4. **The board's version (events-Q9).** At its start and at each seat check, it reads the board's
   `running` record in `board.json` (`<git common dir>/chantier/board.json`, `board/key.py`,
   `key_path`; the record is CR-323's: `pid`, `started`, `version`). When that record is live
   (`procs.alive_since`) and its `version` is not this CLI's `__version__`, it prints once per
   board (per recorded PID): `chantier watch, project <name>: the board is chantier <v>: its
   writes do not reach me; restart it`. The forge read of step 3 goes on, so merges are still
   seen. No live record: nothing is said (a board too old to write the record, or no board).
5. **The printed line**, one per wake-up, flushed at once, UTF-8:
   `chantier events, project <name>: <text>; <text>; ...` in the order written. A `merged`
   event's text is never cut; any other kind's text is cut to 160 characters. The line holds all
   the events of the group, so `Monitor` gets one line per group whatever it does with several
   lines printed together.

It writes nothing else: no batch record, no STATUS file, no git, no forge write, no message.

### C. The pull path: `watch --once` and `status`

**`chantier watch --once`** reads the forge once under the same conditions and interval as step 3
(so at most once per `--forge-every` seconds across calls, through `forge_read_at`), checks the
board's version as step 4 (the line printed each time it holds), then prints the one line of step
5 for every line waiting after `read` (waking or not), advances `read`, and exits 0. Nothing
waiting: it prints nothing more. While a live watch runs for the project: `chantier watch,
project <name>: a watch runs (PID <pid>); its lines come by themselves`, exit 0, and nothing
advances. `--once` takes no `--seat` and starts no process.

**`chantier status`** (`chantier/commands/batch_status.py`, `status()`; on top of CR-323's "other
batches" line, which stays where CR-323 puts it; these lines come after it):

- `_seen_lines` reads the `merged` events of `board-events.jsonl` instead of `board-seen.jsonl`,
  with the same rule (this batch, a CR not merged or cancelled in the record, once per CR, an
  unreadable line named), whatever their source, and whatever `read` says: a merge prints until
  it is recorded. The line's head becomes `forge shows merged:` (was `board saw merged:`), the rest
  unchanged: `forge shows merged: <cr> <pr> into <branch> at <time>; for the Chief of Staff: order
  merged <cr>`, and the `into <other cr>'s branch` form as today.
- events-Q11: whenever no watch of the project is alive (no live `running` in `watch.json`):
  `no watch runs for project <name>`, followed, when lines wait after `read`, by `; board events
  waiting: <n> since <time of the first>`, and always by `; for the Chief of Staff: start it, or
  watch --once on a host that does not wake you`.
- events-Q9: when the board's `running` record is live and of another version: `the board is
  chantier <v>, this is chantier <w>: its writes do not reach the watch; for the Chief of Staff:
  tell the user once to restart it`.
- `status` never advances `read`: the Foreman's heartbeat (`status --refresh`) prints the same
  lines and must not take the Chief of Staff's events.
- These lines are printed only; `STATUS.md`, `STATUS.json` and the CR board pane do not change
  (no pane screenshot is due).

### D. The cards: what the Chief of Staff does

- `skills/chantier/references/session-start.md` (on top of CR-323's edit of "The board"), a
  paragraph "**The watch**" right after "The board": the Chief of Staff (never a Griller, a
  Foreman, a Driver or the router) starts `$CHANTIER watch --seat <own session id>` at its first
  turn, with or without a batch, by the host's means (the host's reference, "Run the watch"); it
  does not ask first (it opens no port and only reads the forge). On a surface it keeps the
  `--project` that `$CHANTIER` holds. A start that prints `already running` is fine. On a host
  whose reference records no way for a background line to wake the session (Copilot today,
  events-Q12), or when the host refuses the start (its exact text, rule 7; events-Q10), it starts
  nothing and says once, in the user's language: "This host does not wake me: what you do in the
  board and the merges on the forge reach me at your next message or at the next `status`." A
  reload starts nothing (unchanged), but see "Woken by the watch" for a watch that stopped.
- `skills/chantier/references/chief-of-staff.md` (on top of CR-323's edits of the same card):
  - The routes table, row of line 30: `a board saw merged line in status` becomes `a forge
    shows merged line in status or in a chantier events line`.
  - The merge paragraph (around line 1025): `A board saw merged: <cr> … line in status` becomes
    `A merged on the forge: <cr> … text (a chantier events line, or a forge shows merged line in
    status)`; same rule: a merge the user made, recorded like any merge.
  - A new section "**Woken by the watch**" (events-Q5, events-Q6, events-Q9, events-Q11, several
    projects):
    - A `chantier events, project <name>:` line whose project is not this session's: nothing
      (never expected; never act on another project's line).
    - A `merged on the forge` text into the default branch: check it on the forge (`gh pr view
      <pr> --json state,mergedAt,baseRefName`, or `glab mr view <iid>`); when the forge confirms,
      `$CHANTIER order merged <cr>` and, in Foreman mode, send its line to the Foreman, as for the
      user's "merged"; in direct mode, what follows a merge as today. Then one line to the user.
      No wait for the user's word. When the forge does not confirm, record nothing and say so in
      one line. The `into <other cr>'s branch` form: record nothing, tell the user where it went
      (unchanged rule).
    - Every other event: one line to the user that says it (a few words per event), and no
      action, no tool call.
    - `forge not read: …`: one line to the user, no action.
    - `the board is chantier <v>: …` (from the watch or `status`): say it once to the user, with
      the restart; never stop or restart the board yourself (CR-323's rule).
    - `stopped, the seat names …`: this session no longer holds the seat; the line of
      `session-start.md` for a moved seat applies.
    - `no watch runs for project <name>` in `status`, or the host saying the background command
      ended: on a host that wakes the session, start the watch again at this turn as at the
      session's start (events-Q6, events-Q11); on one that does not, run `watch --once`.
    - The cost: each wake-up is a turn the user pays; grouping keeps one per ~30 s at most.
  - On a host that does not wake the session (events-Q3, events-Q12): at each turn the user's
    message starts, run `$CHANTIER watch --once` first and say what it prints, in one line per
    event as above (merges handled as above).
  - "The project" (P10's question): the `Monitor` rule of the watch is among the rules P10 may
    name and the Chief of Staff adds on the user's yes (events-Q10); say that auto mode drops it,
    so there the classifier still decides.
- `skills/chantier/references/foreman.md`, line 619: `A board saw merged line` becomes `A forge
  shows merged line`, and the `no watch runs` and `the board is chantier` lines are the Chief of
  Staff's too: do nothing with them, send nothing.
- Keep these edits outside the cards' "Startup core" sections (the startup manifest's 12288 limit).

### E. The hosts and P10

- **P10, the `Monitor` rule (events-Q10).** `chantier/commands/permissions.py`: the "Every batch"
  capability gains the watch's start, as a `Monitor` tool use whose command is the watch, in each
  mode: dev `uv run --no-sync --project /checkout chantier watch --seat <id>`, rule
  `Monitor(uv run --no-sync --project * chantier * watch *)`; plugin `uvx --from /plugin chantier
  --skill /plugin/skills/chantier watch --seat <id>`, rule `Monitor(uvx --from * chantier *
  watch *)`. It is checked like the `SendMessage` bare tool, outside the Bash/PowerShell pair.
  `_counts_as_allow` today ignores every `Monitor` rule (auto mode drops it): a matching
  `Monitor(...)` rule now counts for this sample, and P10's line for it says that auto mode drops
  it and the classifier decides there. `RECOMMENDED_ALLOW` and the pasteable block follow, and
  the test that compares them.
- `skills/chantier/references/hosts/claude-code.md`:
  - "Allow rules" table and the pasteable block: the two `Monitor(...)` rules, chantier's use
    (the Chief of Staff's watch), the risk (any monitor whose command matches), mark
    **unproved**: the rule form for `Monitor` is not documented here. Trial: set the rule outside
    auto mode, start the watch, see no prompt; then in auto mode, see what the classifier does.
  - "Capabilities and their commands", row "Every batch": the watch's command and its rule.
  - "What not to add": it says auto mode drops every `Monitor` rule; add that the watch's rule is
    recommended all the same (it helps outside auto mode), and a refusal is reported (rule 7) and
    leaves the session on the pull path (D).
  - Tools table, two rows after "The board when the session ends":
    - "Run the watch (the Chief of Staff)": the `Monitor` tool with the command `$CHANTIER watch
      --seat <id>`; each line it prints arrives in the session and starts a turn; stopped with
      the host's stop of a monitor. Mark: **unproved**. Trial: a Chief of Staff starts it, the
      user moves an item in the board, and within about 40 s the session starts a turn with the
      `chantier events` line; record whether a timeout or a persistent mode is set, and the date.
    - "The watch when it expires or the session ends": whether a `Monitor` ends after a time,
      whether the host tells the session, and whether it ends with the session: **unproved**.
      What does not depend on it: `status` says `no watch runs` and the Chief of Staff starts it
      again (events-Q11); the seat stops a watch left behind. Trial: start it, leave the session
      idle past the tool's limit (if any), see whether a notice arrives and whether `status`
      then prints `no watch runs`; end the session, take the seat from another, and see the old
      watch's `running` gone within 15 s.
- `skills/chantier/references/hosts/copilot.md`, Tools table, one row "Run the watch (the Chief
  of Staff)" (events-Q12): no tool is recorded whose output wakes a Copilot session (the
  background shell of "Run the board" is not known to start a turn): the Chief of Staff does not
  start the watch and takes the pull path (D), and says so at the session's start. Mark:
  **unproved**. Trial: a Copilot Chief of Staff starts `$CHANTIER watch --seat <id>` in the
  host's background shell, the user moves an item in the board, and the session either starts a
  turn with the line (record the tool and the date; the row then says to start the watch, as on
  Claude Code) or does not (record that, and the pull path stays).

### F. AGENTS.md, CONTRIBUTING.md, docs, scenario

**AGENTS.md** (chantier's own), on top of CR-323, which edits the same first bullet (the board's
`board.json` wording): rebase and keep both.

1. First bullet, the network clause: "the CLI needs no network once uv's cache holds its packages,
   except the board's PRs page (below)" becomes "the CLI needs no network once uv's cache holds
   its packages, except the board's PRs page and `chantier watch` (below)".
2. The CLI's scope bullet, from "and a second, from the same page:" to "messages no agent;"
   becomes:

   > and a second: each write it makes (the backlog, the configuration), and each PR its forge
   > read finds merged that the record does not hold, appends one line to the project's
   > `board-events.jsonl` (planning folder, never published), which `chantier watch` and `status`
   > read for the Chief of Staff; the board itself records nothing and messages no agent;

3. A new bullet right after it:

   > - A second named exception: `chantier watch`, which the Chief of Staff runs for its whole
   >   session (on Claude Code with the `Monitor` tool), for one project. It prints one line per
   >   group of new lines of that project's `board-events.jsonl`, gathered over about 30 s, and
   >   reads the forge, read-only, with the user's own `gh` or `glab`, at most once every 60 s by
   >   default and only while a PR of the project's open batch is open, needing the network for
   >   that; a merge it finds that the record does not hold it appends to `board-events.jsonl`,
   >   and it keeps its place and its process in `watch.json` (planning folder, never published).
   >   It records nothing in a batch, commits nothing, messages no agent and knows no role; it
   >   stops when the project's seat no longer names the session it was started for.

**CONTRIBUTING.md**, the CLI paragraph (around line 103) that mirrors the same rule: the same
changes, in its wording.

**docs/web-board.md** (on top of CR-323's edit of "The link"), PRs section: "The signal" and "The
signal is read only when a `status` runs" are rewritten for `board-events.jsonl`, the `forge shows
merged` line and the watch. A new short section "Events" after "The link": every board write and
every merge seen is one line of the project's `board-events.jsonl`, local; a running Chief of
Staff on Claude Code hears it within about 30 s; on another host at the next message or `status`;
a board of another version than the session's CLI is named, and its writes do not reach the
watch.

**docs/planning-modes.md**: a paragraph "The watch, one per project" next to CR-323's "Two
sessions on one surface": each Chief of Staff's watch hears only its own project's events and
forge; what wakes the session; the pull path on a host that does not wake it.

## What this leaves open for `board-griller`

`board-griller`'s direction (its `01-intent.md`, "Direction", the user, 2026-11-17) is a Griller
started headless (`claude -p`, `copilot -p`) or a Griller session in a remote worktree, which
may message the Chief of Staff and carry files. Such a Griller is neither the board nor the
watch. The events file and the watch do not prevent it: a later CR may add a writer and a
`source` value through `events/store.py` (a kind, its `text`, its `wakes`), and the watch prints
its lines unchanged (B, step 5). Nothing here starts a Griller or carries its files.

## Out of scope

- The Griller started from the board, how it is started, and what it may say to the Chief of
  Staff (CR `board-griller`).
- A comment or discussion feature in the board: today a note is a file saved from its editor.
- A prompt hook, an MCP channel server, or the plugin's mod (`hooks/register.tsx`) as a wake path:
  not chosen (events-Q1). No `hooks/` or `types/` change.
- The Foreman, the Griller and the Drivers: they never run the watch.
- A machine-wide event bus or any message between the sessions of two projects.
- Folding `board-journal.jsonl` into `board-events.jsonl`.
- Stopping or restarting a board of another version: the user's (CR-323).
- `STATUS.md`, `STATUS.json` and the CR board pane.

## Evidence

**Tests** (`cli/tests/`, in-process, few and parametrized; `just test` within its budget):

- `test_board_prs.py`: the existing `board-seen.jsonl` checks move to `board-events.jsonl` (one
  `merged` event, once; the folder unchanged but that file), and one more case: a merge already
  written by the watch is not written again by the page.
- One parametrized test of the board's write routes and `config` put: each kind writes one event
  with `project`, `source: board` and the `wakes` of the table; a refused write and a dry run write
  none.
- One parametrized test of `events/store.py` and `watch --once` (the forge read replaced by the
  seam `forge_read.read`): nothing waiting prints nothing; one move prints one `chantier events,
  project <name>:` line and a second `--once` prints nothing; a non-waking line is carried with
  the next; a line of another project and an unreadable line are skipped; a file cut short resets
  `read`; a long `merged` text is printed whole and a long `move` text is cut to 160 characters;
  no open PR asks the forge nothing; two calls within `--forge-every` ask it once; a live
  `running` record makes `--once` print `a watch runs` and advance nothing; a live board record
  of another version prints the `the board is chantier <v>` line.
- `status`: the `forge shows merged` line from a `merged` event of either source; `no watch runs
  for project <name>` with no live watch (with and without waiting events) and not with one; the
  other-version board line; `read` unchanged after `status`.
- The watch's start decision (seat names another session; live watch same session; live watch
  of another session that does not stop, with `alive_since` monkeypatched and no process
  signalled).
- P10 (the existing permissions tests): the watch's `Monitor` sample is reported missing with no
  rule and covered by the recommended `Monitor(...)` rule; `RECOMMENDED_ALLOW` equals the block
  of `hosts/claude-code.md`.

**Scenario** (`scenario/run_scenario.py`, `scenario/README.md`; `test_scenario_coverage.py`
checks each bullet names a unit):

- unit surface-board (the PRs page block): `kept()`, `untouched()` and `seen_entries()` read
  `board-events.jsonl`; the merge the board saw is one `merged` event, once, ignored by git
  (`git check-ignore`); `status` and the Foreman's heartbeat form print the `forge shows merged`
  line, the orders unchanged; after `order merged` it no longer prints.
- The same unit: a board move through the API, then `status` prints `no watch runs for project
  <name>; board events waiting: 1 ...`, then `watch --once` prints one line naming the project
  and the move, then `status` prints `no watch runs` with no waiting count.
- `external_surface` (on top of CR-323's checks there; two projects `demo` and `other`): a board
  write on `other` is in `projects/other/changes/board-events.jsonl` only, and `watch --once
  --project demo` prints nothing for it; a merge of `demo`'s PR on the fake forge is not read by
  `watch --once --project other` (other's batch has no such PR).
- The running watch: `watch --seat <the seat's session> --group 1 --forge-every 1` started as a
  child process with a null standard input; a board move prints one line within 5 s; while it
  runs, `status` prints no `no watch runs` line; the fake forge marks a PR merged and one line
  with `merged on the forge` and `order merged <cr>` comes within 5 s, written once in the file;
  a second `watch --seat <same>` prints `already running` and exits 0; the seat moved with `seat`
  to another session makes the watch print its `stopped` line and exit 0 within 15 s;
  `watch.json`'s `running` is then empty.
- Windows: the child process starts, prints UTF-8 lines and stops on the seat with no signal
  sent by the scenario.

**Gates**: `just check` on Linux, macOS and Windows; this CR changes the CLI and the cards, so
the pipeline's `just scenario (ubuntu-latest)` job is green at the PR's head, and `just scenario`
passes locally (`chantier gate`) at its head when it is the top of its batch's stack. No `hooks/`
or `types/` change: no `just mod`. No change to what the pane draws: no screenshot. On top of
CR-323: rebase on it and keep both texts in `AGENTS.md`, `session-start.md` ("The board"),
`chief-of-staff.md`, `docs/web-board.md` ("The link"), `docs/planning-modes.md`,
`commands/batch_status.py` (`status()`) and the scenario's `external_surface` unit.

**After merge, on the hosts** (not a gate of the PR): the trials of E (the `Monitor` rule, the
watch's start and wake-up, its lifetime on Claude Code, the Copilot wake-up), recorded in the host
references with their dates.

## Open questions

None: the user answered events-Q9 to events-Q12 after the spec critic. The trials of E stay
trials, run after merge.
