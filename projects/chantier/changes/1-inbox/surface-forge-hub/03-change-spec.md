# Change Specification: one forge hub per surface and machine, and watchers that wake each session

Short name `hub`. Grilled with the user on 2026-11-18 (`02-answers.md`, hub-Q1..Q4, all A, and
the points settled by the Chief of Staff). No tracker issue: the CR is verbal.

## Goal

The Chief of Staff learns on its own, with no word from the user, that a PR of its batch merged
(or that CI turned red on a PR ready to merge), and acts on it: it records a merge that landed on
the default branch, and tells the user the rest. A stack merged in one go gives one wake, not one
per PR. This holds when one planning surface carries several projects (today chantier,
markdown-okf-schema-studio, okf-schema, agentic-planning-surface), each with its own Chief of Staff
session and batches, and when the surface is shared between machines by autosync. CRs added to a
running batch, and new batches, are followed with no relaunch.

The measured cost this removes: one round trip with the user per merge ("I merged #42").

## The design in one paragraph

Each session's Chief of Staff runs `$CHANTIER watch` in the background while its project has a
running batch. Every watcher of a surface on one machine competes for one OS file lock; the one
that holds it is the **hub**: the only process that reads the forge, for every project of the
surface, at most once every 10 s. The hub appends events (a merge the record does not hold, CI
turning red on a PR ready to merge) to each project's local **journal**, `forge-journal.jsonl` in
the planning folder, ignored by git; this journal replaces `board-seen.jsonl`, and the board's
PRs page writes its merge lines there too. Each watcher reads only its project's journal, from its
own cursor, never the forge, and ends once 20 s have passed with no newer event of its project.
Its end wakes the session, which checks, records, relays, and starts the watcher again from the
printed cursor. If the hub's watcher ends or dies, another watcher of the surface takes the lock
within about a second. Machines do not coordinate: the forge is the truth, and `order merged`
already answers `<cr> already merged` to a merge recorded twice.

## Decisions carried from `02-answers.md`

| Decision | Where it lands below |
| --- | --- |
| hub-Q1 A: merges, plus CI turning red on a PR ready to merge; review comments are not followed | Journal events (`merged`, `checks-red`); Out of scope |
| hub-Q2 A: after checking it on the forge, a merge that landed on main is recorded with `order merged`, no word from the user; in Foreman mode its line goes to the Foreman as today; a merge into another CR's branch is only reported | Cards, chief-of-staff.md |
| hub-Q3 A: the watcher ends 20 s after the last event of its project; the wait grows while a stack keeps landing | `chantier watch`, its end |
| hub-Q4 A: a new named exception in `AGENTS.md` for the hub (reads the forge, read-only, with the user's own `gh` or `glab`, justified by one round trip with the user per merge); the board's exception is left as it is | AGENTS.md and CONTRIBUTING.md |
| Settled: a red CI on a ready PR is told to the user and, in Foreman mode, relayed to the Foreman; the Chief of Staff records nothing for it | Cards; routing.md |
| Settled: the Chief of Staff starts its watcher while its project has a running batch and again after each wake; with no running batch it starts none | Cards; `watch` refuses with no running batch |
| Settled: the journal is local to the machine and ignored by git; `board-seen.jsonl` folds into it | The journal |
| Settled: a merge recorded twice is harmless (`order merged` answers `already merged`) | No cross-machine coordination |

## What changes

### 1. The journal (`forge-journal.jsonl`)

- **Where.** One file per project, at the root of the planning folder (`repo.changes`):
  `.agents/changes/forge-journal.jsonl` in-project, `projects/<name>/changes/forge-journal.jsonl`
  on a surface. Add `forge-journal.jsonl` to `IGNORED` in
  `skills/chantier/scripts/cli/src/chantier/core/files.py` (so `ensure_gitignore` completes every
  planning folder's `.gitignore`); keep `board-seen.jsonl` in `IGNORED` so an old file stays
  unpublished. In `board/fingerprint.py`, `SINGLE` names `forge-journal.jsonl` instead of
  `board-seen.jsonl`.
- **Shape.** Append-only JSON lines, UTF-8, `\n`. Every line carries `seq` (an integer, 1 for the
  first line of the file, then the last line's `seq` plus one), `t` (`clock.now()`), `by`
  (`"hub"` or `"board"`) and `kind`:
  - `merged`: `batch`, `cr`, `pr`, `into` (the branch), `into_cr` (the CR whose branch it is, or
    null), `merged_at`, and, once the base landed, `landed_with` and `landed_at`: the same fields
    `board/seen.py` writes today.
  - `checks-red`: `batch`, `cr`, `pr`, `head` (the PR head's full commit SHA the forge reports).
- **Writers and their rule of once.** Every append runs under the project's lifecycle lock
  (`lifecycle.stages.changes_lock`), reads the file, assigns `seq`, and skips a line already there:
  a `merged` line once per (batch, CR, landed-or-not), as `seen.signal` does today, whoever wrote
  the first (hub or board); a `checks-red` line once per (batch, CR, head SHA), so a new red head
  after a fix gives a new line and a red head read again gives none. An unreadable line is
  skipped and never rewritten; `seq` continues from the highest readable `seq`.
- **The fold of `board-seen.jsonl`.** The module that owns the journal (new,
  `chantier/hub/journal.py`) replaces `board/seen.py`: its read, its once rule and its `status`
  lines move there, with the file name `forge-journal.jsonl`. The board's PRs page
  (`board/prs.py`, `answer`) appends its `merged` lines through it with `by: "board"`; nothing
  else changes on that page. An existing `board-seen.jsonl` is left where it is, no longer read and
  no longer written: no migration is needed, because the hub's first cycle reads the forge for
  every PR the record does not hold merged and writes those merges again.
- **Never truncated** by chantier. The board's `journal/rescan` empties `board-journal.jsonl`
  only, as today.

### 2. The hub (election and cycle)

- **Lock.** `<git common dir>/chantier/hub.lock`, the git folder of the session's repository
  (`repo.git_dir`: the surface's on a surface, the project's in-project), next to the board's
  `board.json`. Taken with `core.files.try_lock` (msvcrt on Windows, flock on POSIX), never
  waited on: the OS releases it when the holder exits or dies, so no stale-lock cleanup exists.
  This mirrors the surface autosync's `sync.lock` election (`scripts/ai-autosync-git.py`,
  `participate`: try the lock with no wait, lead while holding it, else stand by and try again
  about every second), without its participants' files: no new dependency (the CLI does not take
  `filelock`).
- **Its record.** While it holds the lock, the hub keeps `<git common dir>/chantier/hub.json`
  (atomic `write_json`): `pid`, `version` (the CLI's), `started`, and per project `read_at` (the
  last good read) and `error` (the last failed read's one line, or null). A record whose process is
  not alive since `started` is no record (`procs.alive_since`, as `board/running.py` does). The
  hub removes the record when it releases the lock, only if it still names its own PID.
- **Which projects.** On a surface, every project of `repo.surface_projects(surface_root)`; in
  a repository, its one project. For each, the batch in `4-batch/` when its `batch.json` status is
  `running` (not paused, not closed). The record is read again at every cycle, so a CR added
  mid-batch and a new batch are covered with no relaunch.
- **What it reads.** For a project whose running batch has at least one CR with a PR that the
  record does not hold merged or cancelled: one forge call, `board/forge_read.read` over every PR
  link of that batch (the recorded-merged ones included, to follow a stack's landing), with the
  user's own `gh` or `glab`, read-only (`api graphql`, a query, never a mutation). A project with
  nothing to read costs no call. A project whose links span several repositories gets
  `forge_read`'s refusal as its `error` in `hub.json`.
- **When.** One cycle at most every 10 s (a module constant, the board's `TTL_S`), the first at
  once when a watcher becomes the hub. A forge error (no `gh`, a timeout, a forge error) goes in
  `hub.json` and the cycle goes on with the next project; nothing is written to the journal for
  it.
- **How it judges.** Exactly as the PRs page: factor the row building of `board/prs.py`'s
  `answer` (`row_of`, `landed_with`, `why_not`, `ready_now`, the CR's readiness from
  `board/crs.py`'s `ready_word(...) == READY_TO_MERGE`) into one function that both the page and
  the hub call, so the two never disagree.
  - A row whose `why` is `merged` gives a `merged` event (into a branch, into another CR's branch,
    or landed with it), as the page's signal does today.
  - A row of a CR ready to merge in the record, open on the forge, whose checks are `failing`,
    gives a `checks-red` event with the PR's head SHA.
- **Head SHA.** Add the head commit to the forge query: `headRefOid` in `GITHUB_FIELDS`,
  `diffHeadSha` in `GITLAB_FIELDS`, carried as `head` in `github_state` and `gitlab_state`. The page
  ignores it.
- **What it never does.** No git command, no record write, no message to any agent, no forge
  write, no write outside the projects' journals and its own `hub.lock` and `hub.json`.

### 3. `chantier watch`

- **Command.** `$CHANTIER watch [--after <seq>]` (the global `--project` names the project on a
  surface, as for every command: `chantier --project <p> watch`). New parser module
  `skills/chantier/scripts/cli/src/chantier/declare/watch.py` (scope `NO_BATCH`), registered like
  the others; handler in the new package `chantier/hub/` (for example `hub/watch.py`, with
  `hub/lock.py` for the election and `hub/cycle.py` for the hub's cycle). The help says: "wait in
  the background for the forge events of this project's running batch (merges, CI red on a PR
  ready to merge), read from the local journal; one process per surface and machine reads the
  forge for all".
- **Refusals** (changing nothing):
  - no running batch in the project: exit 2, `watch: no running batch in <project>: nothing to
    watch`;
  - `--after` greater than the journal's highest `seq`: exit 1, `watch: --after <n> is past the
    journal's end (<last>)`.
- **Cursor.** Without `--after`, the cursor is the journal's highest `seq` when the watcher
  starts (0 for no file). With it, events with `seq` greater than `<n>` count, including those
  written while no watcher ran.
- **Loop.** About once a second: if it is not the hub, try the lock (become the hub on success);
  if it is the hub and a cycle is due, run it; then read its own project's journal past the
  cursor. Only its own project's journal is read; a watcher never calls the forge except as the
  hub, and as the hub only through the cycle above.
- **End (hub-Q3).** From the first new event on, the watcher ends once 20 s have passed (a module
  constant) with no newer event, measured on its own monotonic clock from when it saw each event,
  never from the `t` field (two machines' clocks may differ). A stack that keeps landing keeps
  the watcher waiting; a stack merged in one go gives one end. A hub cycle in progress may delay
  the end by at most that cycle. It also ends, with no event, when its project no longer has a
  running batch: `watch: no running batch in <project>; ended`, exit 0.
- **Output at its end** (exit 0), one line per new event, in `seq` order, then the cursor:
  - `merged` lines: the same text as `status` prints (below), from one shared function.
  - `checks-red`: `forge saw checks red: <cr> <pr> at <head, 7 characters>, ready to merge in
    the record; for the Chief of Staff: tell the user, record nothing`.
  - last line: `watch: cursor <seq>; next: chantier watch --after <seq>`.
  The watcher prints every new event of its journal; it does not filter against the record (a
  merge already recorded is answered `already merged` by `order merged`).
  At its start it prints one line, `watch: <project> from cursor <n>` (and `, the hub` when it holds
  the lock), for the host's output.
- **Its end releases the lock** (process exit), and removes `hub.json` when it was the hub.
- **Test seam.** One environment variable read only by the hub package, named in its docstring,
  shortens the 10 s cycle and the 20 s quiet for the scenario (no command-line option, so no agent
  is invited to change the user's 20 s). Unit tests drive the end and the cycle through pure
  functions with an injected clock and the `forge_read.read` seam, never by sleeping.

### 4. `status`

In `skills/chantier/scripts/cli/src/chantier/commands/batch_status.py`:

- `_seen_lines` reads `forge-journal.jsonl` through the journal module; the unreadable-line
  message names that file. It prints the `merged` lines only (never `checks-red`: a red check is
  told by the watcher's end), one per open CR of the batch, the landed line winning, as today.
- The prefix changes from `board saw merged:` to `forge saw merged:` (the hub and the board both
  write the journal); the rest of each line is today's text:
  - `forge saw merged: <cr> <pr> into <branch> at <time>; for the Chief of Staff: order merged <cr>`
  - `forge saw merged: <cr> <pr> into <other cr>'s branch at <time>; for the Chief of Staff: not
    landed, tell the user, record nothing until <other cr> lands`
  - `forge saw merged: <cr> <pr> into <other cr>'s branch at <time>, landed with <other cr> at
    <time>; for the Chief of Staff: order merged <cr>`
- Two new lines while the project has a running batch: `forge hub: PID <n> (chantier <v>), last
  read <time>` (with `; last read failed at <time>: <error>` when that project's `error` is set),
  or `forge hub: none running`; and `watch: chantier watch --after <highest seq>`. They are not
  `STATUS.json` fields (the CR board pane is unchanged).

### 5. Cards

- **`skills/chantier/references/chief-of-staff.md`**
  - Entry points table (line ~31): the trigger cell "a `board saw merged` line in `status`"
    becomes "a `forge saw merged` line in `status` or at a watcher's end"; one new row: "a
    watcher's end (its background task ended)" → read its output and act on each line as below,
    then start it again.
  - Starting a batch: once the batch runs, start `$CHANTIER watch --after <n>` (the `watch:` line
    of `status`) in the background by the host's means (host reference, "Run the watcher"). While
    It runs, after a session start or a reload with a running batch: the same, if no watcher of
    this session runs.
  - While it runs, the paragraph at lines ~1036-1048: the `board saw merged` text becomes `forge
    saw merged`; "the board read" and "the board then writes a second line" become "the hub (or
    the board) read" and "the hub or the board then writes". A new paragraph, **A watcher's end**:
    for each `forge saw merged … order merged <cr>` line, check the merge on the forge first
    (`gh pr view <pr> --json state,baseRefName,mergedAt`, `glab mr view <iid>` on GitLab): merged,
    into the default branch, or for a `landed with` line, its base's PR merged into the default
    branch; then `order merged <cr>` with no word from the user (Foreman mode: send its line to the
    Foreman, as for any order; direct mode: do what it needs yourself); `already merged` is
    harmless. A line the forge does not confirm is not recorded: tell the user what the forge
    shows. A `not landed` line: tell the user where the PR went, record nothing (as today). A
    `forge saw checks red` line: tell the user (the CR, the PR, the head), record nothing; in
    Foreman mode send the Foreman `checks red <cr> <pr> at <head7>`. Then one message to the user
    with what was recorded and told (the report format of the card), and start the watcher again
    with the `--after <seq>` of its last line while `status` shows a running batch; with none,
    start none. A watcher that ends with `no running batch` is not started again. The GitLab fold
    rule keeps its precedence.
  - Never: never start a second watcher in the same session while one runs; never stop
    another session's watcher.
  - Handing the seat over: the old Chief of Staff stops its watcher (the host's stop of a
    background shell); the new one starts its own.
- **`skills/chantier/references/foreman.md`** (line ~683): the `board saw merged` sentence
  becomes `forge saw merged`; the `forge hub:` and `watch:` lines of `status` are the Chief of
  Staff's (do nothing with them; not an undone order). A `checks red <cr> <pr> at <head7>` line
  from the Chief of Staff: see the open question 2 for what the Foreman does; until it is
  answered, the proposal: it records nothing and starts no Driver on it; a live Driver of that CR
  gets it as a `note`.
- **`skills/chantier/references/routing.md`**: in the second "Chief of Staff → Foreman" row, add
  `checks red <cr> <pr> at <head7>` (a red CI on a PR ready to merge, relayed from a watcher; the
  Foreman records nothing for it).
- **`skills/chantier/references/session-start.md`**: after "The board", a short paragraph **The
  watcher**: a Chief of Staff (never a Griller, a Foreman, a Driver or the router before a role)
  whose project has a running batch starts `$CHANTIER watch --after <n>` in the background (host
  reference, "Run the watcher"), with no question to the user (the hub's exception in
  `AGENTS.md` covers its forge reads); a host that cannot run a background command: one line with
  the reason, then go on, no workaround.
- **`skills/chantier/references/hosts/claude-code.md`** (the Claude Code host reference), table
  rows:
  - "Run the watcher": the shell tool (`Bash`, or `PowerShell` on Windows) with
    `run_in_background: true` and `$CHANTIER watch --after <n>`; its end is the background task's
    completion notice, which starts a turn of the idle Chief of Staff session; its output is read
    from the background task. Mark: unproved; trial: a batch's first merge with a watcher running,
    the Chief of Staff's transcript showing the notice, the `forge saw merged` line and the
    `order merged` that followed with no user message between. (A subagent's wake by a background
    shell's end is proved, row "End a subagent's turn"; the main session's is not.)
  - "The watcher when the session ends": whether the host ends a background command when the
    session ends. Unproved; trial as for the board's row. An orphaned watcher costs no forge read
    once its project has no running batch, and ends then.
- **`skills/chantier/references/hosts/copilot.md`**: the same "Run the watcher" row with the
  host's background shell, unproved, with the same trial; if the host cannot run a background
  command or its end does not start a turn, the Chief of Staff starts no watcher and says so in one
  line (no workaround).
- The agent files (`agents/`, `com.github.copilot/agents/`) do not change.

### 6. `AGENTS.md` and `CONTRIBUTING.md`

- **`AGENTS.md`, the "plugin must work with no setup" bullet**: "the CLI needs no network once
  uv's cache holds its packages, except the board's PRs page (below)" becomes "... except the
  board's PRs page and the forge hub (below)"; after "the board keeps its key, and while it serves
  its PID, address and version, in the repository's git folder (`chantier/board.json`)", add "the
  forge hub keeps its lock and, while it runs, its PID, version and last reads there too
  (`chantier/hub.lock`, `chantier/hub.json`)".
- **`AGENTS.md`, "The CLI's scope" bullet**: "Two named exceptions." becomes "Three named
  exceptions."; append the third:

  > Third, the forge hub of `chantier watch`: of the watchers of a planning surface (or a
  > repository) on one machine, the one that holds an OS file lock in the git folder
  > (`chantier/hub.lock`) reads the forge, read-only, with the user's own `gh` or `glab`, on its
  > own (no agent asks it), and needs the network for that: at most once every 10 s, one query per
  > project of the surface whose running batch has a PR the record does not hold merged or
  > cancelled; it appends to that project's `forge-journal.jsonl` (planning folder, never
  > published) one line per merge the record does not hold and per CI turning red on a PR ready to
  > merge, and nothing else; each session's watcher reads only its project's journal, never the
  > forge, and ends 20 s after the last new event, which wakes its session; the hub records
  > nothing in a batch, runs no git and messages no agent. Its measured cost to justify it: one
  > round trip with the user per merge.

- **`AGENTS.md`, the board's bullet**: the board's exception is unchanged in scope (hub-Q4); only
  the file it appends to is renamed by the fold: "it appends one line to `board-seen.jsonl`"
  becomes "it appends one line to `forge-journal.jsonl`".
- **`CONTRIBUTING.md`** (section 2, lines ~84-110): the same three edits, in its own words
  (the git-folder files, the third exception, the file name in the board's exception).
- **Docs**: `docs/web-board.md` ("The signal", line 62): the file name and the `forge saw merged`
  prefix, and one sentence that the hub writes the same lines; `docs/planning-folder.md` (the
  local files, line ~49): add `forge-journal.jsonl`; `scenario/README.md`: the coverage bullets
  below.

## Out of scope

- Review comments (hub-Q1).
- Any coordination between machines; each machine has its own hub and journals.
- A hub that runs without a watcher (a service, the board as hub): set aside in the request.
- Any change to the board's PRs page beyond writing the journal instead of `board-seen.jsonl`
  and reading the shared row function (no new page, no new reads, no new cadence).
- A watcher for a Griller, the Foreman or a Driver.
- The CR-number collision between machines noted in the request (a separate subject).
- `STATUS.json` fields and the CR board pane (`hooks/register.tsx`), `hooks/` and `types/`.
- A version bump (the release does it).

## Evidence

The project's rules (`AGENTS.md`) for a change under the CLI's `src/` and the cards:

1. **Before the first push**, the Driver runs, in the worktree at the rebased head it pushes,
   `just check` (lint, the unit tests within the 30 s margin, release notes) and `just
   eval-dry-run`, and records both outputs.
2. **Before the PR is ready**: the pipeline's `just scenario (ubuntu-latest)` job green at the
   PR's head (a change to the CLI and the cards). On ubuntu the lock is `fcntl.flock`; the
   Windows lock (`msvcrt`) is proved by the unit test run in `just check` on the user's Windows
   machine, and by the local `just scenario` (`chantier gate`) when this CR is on top of its
   batch's stack.
3. No `just mod` (no change to `hooks/` or `types/`), no pane screenshot (no change to the pane or
   to `STATUS.json` fields), no `DESIGN.md` (no change under `board/web/`).

### Unit tests (`skills/chantier/scripts/cli/tests/`, few, parametrized, no sleep)

New `test_forge_hub.py`:

- `test_one_watcher_holds_the_hub_lock_and_the_next_takes_it`: two handles on one `hub.lock`;
  the first wins, the second does not, and gets it once the first is released; `hub.json` names
  the holder's PID and is gone after.
- `test_a_hub_cycle_writes_each_event_once` (parametrized): with `forge_read.read` replaced, on a
  two-project surface (one running batch each, a third project paused): a PR merged into main
  gives one `merged` line, `by: "hub"`, `seq` 1, in its project's journal only; a second cycle
  writes none; a PR merged into another CR's branch gives the not-landed line, then the landed
  line once its base merges; a ready PR failing at head A gives one `checks-red`; the same head
  again none; head B red gives a second; a failing PR not ready to merge gives none; the paused
  project's forge is not read (the seam not called for it); a project with no PR left open costs
  no call; a forge error lands in `hub.json`, not in the journal.
- `test_the_board_and_the_hub_share_the_journal_once`: a board `merged` line for (batch, CR) then
  the hub's cycle on the same merge writes no second line, and the reverse.
- `test_a_watcher_ends_twenty_seconds_after_the_last_event` (parametrized, injected clock):
  events at 0 s end at 20 s; at 0, 15 and 30 s end at 50 s; none never ends while the batch runs;
  the batch no longer running ends with the `no running batch` line.
- `test_watch_refusals`: no running batch, exit 2 and its line; `--after` past the end, exit 1;
  nothing written.
- `test_status_prints_the_journal_merges_the_hub_and_the_cursor`: `forge saw merged` lines (the
  three forms), no `checks-red` line, `forge hub:` both forms, `watch: chantier watch --after
  <n>`.

Updated: `test_board_prs.py` (`SEEN` and the `board saw merged` strings become the journal's file
and `forge saw merged`; the folder check allows `forge-journal.jsonl` only),
`test_board_prs_batches.py` (line ~61: no `forge-journal.jsonl` for a closed batch),
`test_board_forge_read.py` (the `head` field on both forges). `test_scenario_coverage.py` must
pass on the new bullets. A test that asserts a card's or `AGENTS.md`'s text, if one is added,
reads the shipped file from the repository at the head under test, never a prepared copy.

### Scenario (`scenario/run_scenario.py`, the `surface-board` unit)

- Update the `board_prs` case for the file name and the `forge saw merged` prefix (and its
  README bullets at lines ~280-292).
- A new case `forge_hub` in `UNITS["surface-board"]` (raise the unit's budget by its measured
  cost), on a two-project surface with the fake `gh` (`forge_pr`, `forge_calls`), the test seam
  shortening the cycle and the quiet:
  - `chantier watch` for project A and for project B started as background processes; while both
    run, `hub.json` names one PID and each cycle makes one `api graphql` call per project with an
    open PR, never two hubs' worth;
  - A's PR merged into main on the fake forge: A's watcher ends with the `forge saw merged … order
    merged <cr>` line and `watch: cursor 1; next: …`, B's watcher keeps running and takes the
    lock (the next cycle still reads the forge, its PID in `hub.json`);
  - two of A's PRs merged one after the other within the quiet: one end with both lines;
  - a ready PR's checks failing: the `forge saw checks red` line; `status` does not print it;
  - restarted with `--after <n>`: no line replayed; `order merged <cr>` twice: the second answers
    `<cr> already merged`;
  - a merge the board's PRs page reads first: the hub writes no second line and the watcher
    wakes on the board's line;
  - the journal is ignored by git (`git check-ignore`), the record (`batch.json`, `events.jsonl`)
    unchanged by the hub, and no `gh` call but `api graphql` queries.
- `scenario/README.md` Coverage: one bullet per point above with `(unit: surface-board)` and the
  unit tests' names `(test: test_forge_hub.py::…)`.

### Host matrix

The watcher depends on the host's background command and its wake; the times are constants, not
configured (no default-versus-configured cell).

| Cell | Result it must show | Real flow that proves it |
| --- | --- | --- |
| Claude Code, a watcher's end with the session idle | the session takes a turn, records the merge with no user message | first batch after the merge (host row trial); until then the PR's Known gaps names "the main session's wake by a background watcher's end is unproved" |
| Claude Code, session ended with a watcher running | the watcher ends with the host, or ends at the batch's end | host row trial; unproved until then |
| Copilot, a watcher's end | as for Claude Code, or, with no background command or no wake, no watcher and one line | host row trial; unproved |
| Windows lock (msvcrt) / POSIX lock (flock) | one hub, the next watcher takes over | `just check` on Windows, the scenario on ubuntu |

## Open questions for the Chief of Staff

1. **The hub's cadence.** This specification uses 10 s, the board's own limit: about 360 forge
   calls an hour per project with an open PR (four projects at once: about 1440, under GitHub's
   GraphQL budget of 5000 points an hour, shared with the Drivers' `gh` use). Keep 10 s, or
   longer (for example 20 s, the buffer's length)?
2. **What the Foreman does with `checks red <cr> <pr> at <head7>`.** The settled points say the
   Chief of Staff relays it; they do not say what the Foreman does. Proposed: it records nothing
   and starts no Driver on it; a live Driver of that CR gets it as a `note` (its CI wait usually
   saw it already); with no live Driver, nothing until the user asks (the Chief of Staff told
   them). Confirm, or name another action.
3. **A paused batch.** This specification follows running batches only (the settled point), so a
   PR the user merges while the batch is paused is seen at the next `status` or by the board, not
   by a wake. Keep it so?
