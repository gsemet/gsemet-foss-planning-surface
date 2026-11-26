# Board server notifies when a CR arrives by pull on the surface

Short name: `pull-arrival`. Destination: running batch batch-31.

## Goal

The owner runs the surface server by hand on their PC. A CR can reach the chantier project's inbox
or backlog in two ways that this project's Chief of Staff does not see:

- another machine's session files it, its writer pushes it, and this machine's writer pulls it;
- another project's session on this same PC (okf-schema's Chief of Staff, for instance) writes it.

In both cases the owner should not have to look to find it. The board page shows it, and the Chief
of Staff hears of it through one journal line that names the CR and its stage:

- at once through its watcher (Q1);
- after a conflict, once the conflict ends (Q9);
- at the next session start when no watcher ran (Q10).

Writes by chantier's own session and by the board notify nobody (Q8).

## Decisions carried (02-answers.md)

1. Q1, what is seen: the page updates, and one journal line, which the watcher carries to the
   Chief of Staff, names the CR and its stage.
2. Q2, no timer: a pulled arrival is seen after the writer's fetch and integration (merge
   `--ff-only` or rebase), in the writer's existing cycle. There is no new timer, fetch or watch.
3. Q3, stages: only a CR that ends in `1-inbox` or `2-backlog/P<n>` notifies. A CR that ends in
   `3-ready` or `4-batch` notifies nobody: that is the owning Chief of Staff's own doing.
4. Q4, moves: a new CR notifies, and so does a CR whose stage changed between the inbox and the
   backlog.
5. Q6, backlog rows: a move from one backlog row to another (for example `P2` to `P1`) notifies,
   as a move.
6. Q7, back from `3-ready`: a CR that comes back from `3-ready` into the inbox or the backlog
   notifies, and the line says it comes back from `3-ready`. This specification settles the case
   Q7 left to it, in line with Q3: a CR that comes back from `4-batch`, `5-archives` or `6-trash`
   (a restore) notifies nobody, because that is the owning Chief of Staff's own doing.
7. Q8, who notifies nobody: only the writes of chantier's own session and the board's writes.
   Every other write notifies like a pull:
   - a write pulled from the remote;
   - a write by another project's session on this machine, as when a CR is relayed into chantier's
     inbox or backlog;
   - a write through a login profile (`cli.run`) by a session that is not chantier's own.
   This replaces the request's rule "the server's own writes notify nobody".
8. Q9, a pull that ended in a conflict: once the conflict ends, the CRs that the recorded upstream
   brought are told.
9. Q10, while no watcher runs: the session-start read lists the arrivals that no watcher of the
   project has told yet.
10. The critic's findings:
    - the page half of Q1 is proved with the file watch fed, or with a subscription to the
      board's `project` topic, not only by reading the merged files;
    - the tests are named under `skills/chantier/scripts/cli/tests/`;
    - `test_another_machines_commit_is_integrated_before_the_push` is the base of the first check.

## Words

- **CR folder**: a direct subfolder of `changes/1-inbox/`, of `changes/2-backlog/P1/` to
  `changes/2-backlog/P4/`, or of `changes/3-ready/`. Its name is the CR's slug, which identifies
  the CR.
- **Stage**: `1-inbox`, `2-backlog/P<n>` or `3-ready`. A change of backlog row is a change of
  stage.
- **Arrival**: a CR whose stage after the change is `1-inbox` or `2-backlog/P<n>` and differs from
  its stage before. Before the change, the CR either:
  - was in none of the three stages, and was not in `4-batch` (`4-batch/<batch>/{1-pending,2-actives,3-done}/<slug>`),
    `5-archives` or `6-trash` (a folder `<yymmdd-hhmm>-...` whose name ends with `-<slug>`). Then
    it is **new**, with `before: null`; or
  - was in another of the three stages. Then it is **moved**, and `before` is its old folder
    relative to `changes/`. When that folder is in `3-ready`, it is **back from 3-ready**.

  A CR that was in `4-batch`, `5-archives` or `6-trash` before the change is not an arrival
  (decision 6). A change inside a CR folder that stays in its stage is not an arrival.
- **Chantier's own session**: the session that holds the project's seat, that is, the CLI run's
  `hub/autostart.session_key()` equals the seat's transcript, kept the same way. This is
  `autostart.holds_seat(read_seat(repo).transcript)`. With no seat, no session is chantier's own.
  A Foreman's or a Driver's session is not the seat's, so its `file` or `triage` notifies, and
  the line then tells the Chief of Staff of a write in its own batch's project. That is harmless:
  the line acts on nothing.

## What changes

### 1. A new published journal type, `arrived@1` (`hub/`)

- `skills/chantier/scripts/cli/src/chantier/hub/schemas_sync.py`: add the model `Arrived1(Payload)`
  with these fields:
  - `project: str`, the project's name;
  - `folder: str`, the CR's folder now, relative to `changes/`, for example `1-inbox/<slug>` or
    `2-backlog/P2/<slug>`;
  - `stage: str`, `1-inbox` or `2-backlog/P<n>`;
  - `before: str | None`, the old folder for a move, `null` for a new CR;
  - `via: str`, `pull` (the writer integrated it from the remote) or `session` (a CLI command
    on this machine wrote it);
  - `upstream: Sha | None`, the upstream commit for `via: pull`, `null` for `via: session`.
- `hub/schemas.py`: import the model and add one entry to `PUBLISHED`:
  `"arrived@1": Entry(Arrived1, True, arrived_text, None, <example>)`.
  - It always wakes.
  - It has no duplicate key: each line is its own event, like the `sync-*@1` lines.
  - The example is
    `{"project": "demo", "folder": "1-inbox/an-idea", "stage": "1-inbox", "before": None, "via": "pull", "upstream": "d" * 40}`.
- `arrived_text(e)`, the one sentence, is built from three parts:
  - `<who>`: `surface pull brought` for `via: pull`, `another session wrote` for `via: session`;
  - `<what>`:
    - `new in <stage>` when `before` is null;
    - `back from 3-ready` when `before` starts with `3-ready/`;
    - `moved from <before>` otherwise (a backlog row change included);
  - the sentence: `<who> <folder> (<what>); for the Chief of Staff: tell the user, act on nothing`.
- `hub/schemas.json`: run `just journal-schemas`, which adds the `arrived@1` entry. Never write
  it by hand.
- The docstrings of `hub/journal.py` and `hub/schemas.py`: add `arrived@1` to the published
  types. It is written by the writer (`source: writer`, `via: pull`) and by the `file` and
  `triage` commands (`source: cli`, `via: session`).
- One function computes arrivals for both writers. It is pure: it takes two maps of slug to stage
  plus the set of slugs held in `4-batch`, `5-archives` or `6-trash` before the change, and gives
  the arrivals. Put it, for example, in a new `hub/arrivals.py` or in `lifecycle/stages.py`; the
  Driver chooses. The writer (2) and the commands (3) both call it.
- The `events` topic (`board/api/topics.py`, `_events` and `_told`) and the watcher
  (`hub/watch_lines.told`) already pass on any published type with its text. They change only for
  the told mark (5).

### 2. The writer tells pulled arrivals (`writer/`)

In `writer/cycle.py`, `Writer._integrate(look, upstream)` already reads `local` (HEAD) and
`theirs` (the upstream) before it merges or rebases.

- Before the merge or rebase, read `base`, the merge-base of `local` and `theirs`, through a new
  read method of `writer/git_ops.Git`. It is a read, run through `Git.read` in the C locale like
  every other read. With `ahead == 0`, `base` is `local`.
- After an integration that succeeds (no conflict), read the stages from git's trees, never from
  the working tree, which holds this machine's uncommitted writes:
  - at `base`: each project's CR folders, plus the slugs it holds in `4-batch`, `5-archives` and
    `6-trash`;
  - at `theirs`: each project's CR folders.
  For each project of `self.projects`, use its `changes` folder relative to the surface root. Read
  through one new read method of `Git`: `git ls-tree` on the stage folders, one or a few calls per
  revision, not one per project per cycle when nothing came in. Then call the arrivals function.
- Each arrival gives one `arrived@1` event (`via: pull`, `upstream: theirs`). It is queued with
  `self._tell(event, [the project's Repo])`. It goes to the project that holds the CR, whether or
  not that project has a seat. `_flush` appends it at the cycle's end through
  `journal.append(repo, [event], "writer")`, outside the lifecycle locks, with the audience
  `["project"]`.
- Q8 holds by construction. A write made on this machine is in `local`, so it is at or below
  `base`, and the writer never tells it. Another project's session's local write is told by the
  command that made it (3), not by the writer. Only commits that exist in `theirs` and not in
  `local` give a `via: pull` line.
- The cost: these reads run only when an integration ran (`HEAD..upstream` was not empty).
- **Q9, the conflict's end.** `Writer._conflict` already records
  `conflict = {"upstream": theirs, "local": local, "files": ...}` and gives no `arrived@1` line.
  When `_run` finds `_conflict_over()` true, and before it clears `r["conflict"]`:
  - compute the arrivals between `merge-base(conflict.local, conflict.upstream)` and
    `conflict.upstream`, in the same way;
  - keep only those whose folder HEAD's tree also holds, so that a CR the Chief of Staff's
    resolution removed or moved away is not told;
  - tell each with `via: pull` and `upstream: conflict.upstream`.
  The next ordinary integration's `base` is at or above `conflict.upstream`, so nothing is told
  twice.
- An offline fetch or a failed integration tells nothing. The next integration of the same
  upstream finds the same arrivals, because `base` has not moved.

### 3. The commands tell another session's writes (`commands/intake.py`)

The board's backlog writes call `lifecycle.backlog` directly (`board/write_api.py`) and never
pass through these commands, so the board is never told (Q8).

- `file_cr` (the `file` command): after the CR is filed in `1-inbox`, when the run is not
  chantier's own session, append one `arrived@1` (`via: session`, `before: null`,
  `upstream: null`, `stage: 1-inbox`) through `journal.append(repo, [event], "cli")`.
- `triage` (moves between the inbox, the backlog rows and `3-ready`; not `--running-batch`, which
  changes no stage): when the move is an arrival by the definition above and the run is not
  chantier's own session, append one `arrived@1` (`via: session`, `before` the old folder). A move
  to `3-ready` gives no line.
- `restore` gives no line (decision 6). `abandon` gives none either, because it ends in the trash.
- A command run through a login profile (`cli.run`) carries the client's session variables
  (`board/cli_run.child_env`), so the same test applies to it.
- A CR folder that a session creates or moves by hand, without the CLI, is not told by a command.
  When it is committed by this machine's writer, it is a local write and gives no pull line. The
  cards already file and triage through the CLI.

### 4. The board page

Q1's page half needs no new code. The server watches the planning files
(`board/watch_files.py`, with system notifications or a check every 5 s) and publishes 1 s after
the last change. A merge or rebase by the writer, or a command's write, changes those files like
any other write. There is no new toast and no new panel. The evidence proves this with the file
watch fed.

### 5. The told mark and the session-start listing (Q10)

- A new local file, `arrivals-told.json`, at the root of the planning folder (`changes/`): it holds
  `{"seq": <n>}`, the highest `seq` of an `arrived@1` line already told.
  - Add it to the ignore list in `core/files.py`, next to `forge-journal.jsonl`, so it is never
    published and the writer never commits it.
  - Write it under the project's lifecycle lock (`changes_lock`). The new value is the larger of
    the file's value and the one given, so the mark never goes back.
- Who moves the mark:
  - the watcher (`hub/watch.py`), when it prints its lines at its end, to the highest `seq` of an
    `arrived@1` line among them;
  - `watch --once` (`once`), the same, for the lines it prints;
  - the listing below, for the lines it lists.
- The listing: one function, for example `journal.arrival_lines(entries, told)` in
  `hub/journal.py`, gives `arrived_text(e)` for each `arrived@1` line whose `seq` is above the mark,
  in `seq` order.
  - At most 10 lines, then `and <k> more arrivals: <cli> watch --once --after <seq of the 10th>`.
  - A line of a refused payload or of no published type is skipped, as in `journal.lines`.
- Where it is printed:
  - `seat`, the read every session start makes (`session-start.md`), with or without a batch
    (`commands/seat.py`, beside `writer_lines`);
  - `status` (`commands/batch_status.py`, in its journal lines).
  In both, it is printed only when no watcher of the project runs: `hub/lock.watchers(git_dir,
  project)` is empty. After printing, the command moves the mark. A running watcher tells the
  lines itself at its end, so they are never told twice.
- `status`'s docstring "Nothing is written" changes: the told mark is now its one write.

### 6. The Chief of Staff's card (`skills/chantier/references/chief-of-staff.md`)

- In "The watcher":
  - In "It prints the project's forge events ... the issue events an outside poller writes
    (`tracker saw`)", add: the CRs that another machine or another session brought into the inbox
    or the backlog (`surface pull brought`, `another session wrote`).
  - In "*A watcher's end:*", next to the `tracker saw` rule, add: a `surface pull brought ...` or
    `another session wrote ...` line gets one line to the user that names the CR's folder and its
    stage (new, moved, or back from `3-ready`). No tool call, no action, nothing written: not even
    a destination.
  - In "*The pull path:*", in "Tell its `board wrote`, `tracker saw` and role `config@1` lines as
    above", add the two arrival lines.
- `skills/chantier/references/session-start.md`, where it reads `seat`: the same lines, listed
  there when no watcher ran, are told to the user in the session's first report, in one line
  each, with no action.

The agent files (`agents/`, `com.github.copilot/agents/`) do not change.

### 7. Project rules and docs

- `AGENTS.md`:
  - In the long server bullet, "its writer's commits of the planning surface's published paths
    (below) and its journal lines (`sync-*@1`)" becomes "(`sync-*@1`, `arrived@1`)".
  - In the writer's paragraph, "appends `sync-*@1` lines to the journal" becomes "appends
    `sync-*@1` lines, and one `arrived@1` line per CR that an integration of the upstream brings
    new into a project's `1-inbox` or `2-backlog` or moves there, to the journal".
  - The writer's git commands stay the ones named: `merge-base` and `ls-tree` are reads.
  - `arrivals-told.json` is in the planning folder, where chantier already writes, so no rule
    changes for it.
- `docs/planning-folder.md`:
  - Add `arrived@1` to the `type` row and to the sentence "Every line written today is for
    `["project"]`: ...": by the writer and by `file` and `triage`.
  - Add the row `| arrived@1 | the writer after it integrates the upstream (via pull, and at a conflict's end), file and triage run by a session that is not the seat's (via session) | yes |`.
  - Add `arrivals-told.json` to the list of the local files that are never published (line 54).
- `skills/chantier/references/concepts.md`, near line 164: one clause saying that a CR another
  machine or another session brings into the inbox or the backlog is told by an `arrived@1` line.
- `scenario/README.md`, in "the surface's writer" step: the arrival check (Evidence 9).

## Out of scope

- A timer, a fetch or a file watch of its own for arrivals (Q2).
- Lines for CRs that end in `3-ready`, `4-batch`, the archives or the trash (Q3), and for
  restores (decision 6).
- A new toast, banner or panel on the board page.
- A CR folder created or moved by hand, without the CLI, by a session of this machine.
- A conflict whose writer was stopped before it ended: the conflict record is held in memory and
  lost with it, so its arrivals are not told.
- An in-project planning folder for the pull lines: it has no writer. Its `file` and `triage`
  lines (3) and the listing (5) still apply.
- Routing to a role, CR or session other than the project audience.

## Evidence

All tests are under `skills/chantier/scripts/cli/tests/` and call the code in-process. Keep them
few, parametrized and fast (the `just test` budget).

1. `test_writer_cycle.py`, built on `test_another_machines_commit_is_integrated_before_the_push`
   (the rig `writer_rig.Rig`: a real surface, a real bare origin, the second clone `r.other`), as
   one parametrized test. Each case pushes from `r.other`, drives the cycles, then reads the
   project's journal lines (`r.lines()`):
   - a new `1-inbox/<slug>/` gives one `arrived@1` with `folder` `1-inbox/<slug>`, `stage`
     `1-inbox`, `before` null, `via` `pull`, `upstream` the origin's head, and `source` `writer`;
   - a new `2-backlog/P2/<slug>/` gives one line, stage `2-backlog/P2`;
   - `1-inbox/<slug>` to `2-backlog/P1/<slug>` gives one line, `before` `1-inbox/<slug>`;
   - `2-backlog/P2/<slug>` to `2-backlog/P1/<slug>` gives one line (Q6);
   - `3-ready/<slug>` to `2-backlog/P3/<slug>` gives one line, whose text says
     `back from 3-ready` (Q7);
   - `6-trash/<stamp>-<slug>` to `1-inbox/<slug>`, and `5-archives/<stamp>-<slug>` to
     `1-inbox/<slug>`, give no line;
   - a move into `3-ready/` or `4-batch/`, and an edit inside an existing inbox CR, give no line.
2. `test_writer_cycle.py`, this machine's writes: a CR written in `r.root` and pushed by the writer
   gives no `via: pull` line, in that cycle or a later one. This holds also when the same cycle
   integrates the other clone's commit with another CR, which gives exactly one line, for that
   other CR.
3. `test_writer_cycle.py`, Q9. Beside `test_a_conflict_aborts_the_rebase_tells_it_and_ends_when_integrated`,
   the other clone's conflicting commit also adds two new inbox CRs:
   - the conflict cycle gives no `arrived@1`;
   - the test's resolution keeps one of the two CRs and removes the other, then the conflict ends;
   - the cycle that sees the end gives exactly one line, for the kept CR, with `upstream` the
     recorded upstream;
   - a later cycle adds none.
4. `test_writer_cycle.py`: a second cycle over the same, already integrated upstream adds no line.
5. `test_triage_moves.py`, parametrized, with the seat set to a transcript and the host's session
   variable (`CLAUDE_CODE_SESSION_ID`) set by `monkeypatch`:
   - `file` and `triage --priority P2` run as another session each give one
     `arrived@1` (`via: session`, `source: cli`, the right `before`);
   - the same commands run as the seat's session give none;
   - `triage --ready` gives none, and `restore` gives none;
   - a board backlog write (`board/write_api`'s new idea and move) gives its `board@1` line and
     no `arrived@1`.
6. `test_event_types.py` passes with the new entry. It reads the shipped `hub/schemas.json` from
   the repository at the head under test. The example of `PUBLISHED["arrived@1"]` validates, and
   `just journal-schemas` reports nothing more to add.
7. `test_watch_events.py`:
   - `watch_lines.told` gives the four sentences (new and moved for `pull`, new for `session`,
     back from `3-ready`), and `journal.waking` is True;
   - after `once` prints an `arrived@1` line, `arrivals-told.json` holds its `seq`;
   - the listing (Q10), for `seat` and `status`:
     - with no watcher lock held, it lists the lines above the mark and moves the mark, and a
       second run lists nothing;
     - with a watcher lock of the project held, it lists nothing and the mark does not move;
     - with 11 lines, it lists 10 and the `and 1 more` line.
8. `test_file_watch.py`, the page half of Q1: after the writer's integration brings a new inbox CR
   (the rig of check 1), the file watch is fed the paths the integration wrote
   (`FileWatchThread.feed`, then `tick` past `QUIET_S`). The project settles, and the board's
   `project` topic then lists the arrived CR in `1-inbox`. Equivalently, a subscription to the
   `project` topic sees its rev move and the item in its value.
9. `scenario/run_scenario.py`, in the surface-writer step near line 10800 ("a commit pushed from
   a second clone of the surface is integrated"): the second clone's commit also adds
   `projects/<project>/changes/1-inbox/<slug>/01-intent.md`. A new `check(...)` asserts that the
   step's `events()` hold one `arrived@1` line naming that folder with `via: pull`. Mirror it in
   `scenario/README.md`. The long gate `just scenario (ubuntu-latest)` is green at the PR's head.
10. `just check` passes, and `just eval-dry-run` passes, because the change is under the CLI's
    `src/`.

There is no host or default matrix: the behaviour does not depend on the host or on a configured
value. The session test reads the host's session id through `own_transcript`, which the tests
set for Claude Code; the Copilot variable is read by the same function and needs no extra cell.
The CR adds or changes no CI job.
