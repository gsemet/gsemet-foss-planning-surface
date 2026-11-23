# Board server notifies when a CR arrives by pull on the surface

Short name: `pull-arrival`. Destination: running batch batch-31.

## Goal

The owner runs the surface server by hand on their PC. Another Chief of Staff session (okf-schema,
for instance) files a CR in the shared planning surface, and that session's writer pushes it to the
surface's remote. When this machine's writer pulls the surface, the owner should not have to look
to find the new item. A CR that the pull brings new into `1-inbox` or `2-backlog`, or that it moves
between the two, shows on the board page, and the Chief of Staff's watcher wakes its session with
a line that names the CR and its stage (02-answers Q1, Q4).

## Decisions carried (02-answers.md)

1. Q1, what is seen: the page updates, and the server appends one journal line, which the watcher
   carries to the Chief of Staff, naming the CR and its stage.
2. Q2, no timer: the arrival is seen after the writer's fetch and integration (merge
   `--ff-only` or rebase), in the writer's existing cycle. No new timer, fetch or watch.
3. Q3, stages: only `1-inbox` and `2-backlog` notify. A CR that a pull brings into `3-ready` or
   `4-batch` notifies nobody, because one Chief of Staff owns a project and that is its own doing.
4. Q4, moves: a new CR and a CR whose stage changed between inbox and backlog both notify.
5. Rule 5: the server's own writes notify nobody. This covers every write made on this machine:
   the board's writes, the CLI commands' writes, the Griller's writes and the user's commits by
   hand in the surface.

## What changes

### 1. A new published journal type, `arrived@1` (`hub/`)

- `skills/chantier/scripts/cli/src/chantier/hub/schemas_sync.py`: add the model `Arrived1(Payload)`
  next to the writer's other models:
  - `project: str`, the project's name under `projects/`.
  - `folder: str`, the CR's folder now, relative to the project's `changes/`, for example
    `1-inbox/board-server-notifies-when-a-cr-arrives-` or `2-backlog/P2/export-columns`.
  - `stage: str`, either `1-inbox` or `2-backlog/P<n>`.
  - `before: str | None`, the CR's folder before the pull (see 2) when the pull moved it, else
    `None`.
  - `upstream: Sha`, the upstream commit the writer integrated.
- `hub/schemas.py`: import it and add one entry to `PUBLISHED`:
  `"arrived@1": Entry(Arrived1, True, arrived_text, None, <example>)`. It always wakes. It has no
  duplicate key: each line is its own event, like the `sync-*@1` lines. The example is
  `{"project": "demo", "folder": "1-inbox/an-idea", "stage": "1-inbox", "before": None, "upstream": "d" * 40}`.
  - `arrived_text(e)` is the one sentence, defined in `schemas.py` (or in `schemas_sync.py`
    beside the model):
    - when `before` is null: `surface pull brought <folder> (new in <stage>); for the Chief of Staff: tell the user, act on nothing`
    - when `before` is set: `surface pull brought <folder> (moved from <before>); for the Chief of Staff: tell the user, act on nothing`
- `hub/schemas.json`: run `just journal-schemas`, which adds the `arrived@1` entry. Never write
  it by hand.
- `hub/journal.py`'s module docstring and `schemas.py`'s docstring: add `arrived@1` to the list
  of published types and say the writer writes it (source `writer`).
- `status` (`journal.lines`, `journal.writer_lines`) does not list `arrived@1`. The line reaches
  the Chief of Staff through the watcher and the `watch --once` pull path, as `board@1` lines do.
  The `events` topic (`board/api/topics.py`, `_events` and `_told`) and the watcher
  (`hub/watch_lines.told`) already pass on any published type with its text, so they need no
  change. Check this, and change them only if a test shows a gap.

### 2. The writer finds the arrivals of an integration (`writer/`)

In `writer/cycle.py`, `Writer._integrate(look, upstream)` already reads `local = HEAD` and
`theirs = <upstream>` before it merges or rebases. Change it as follows:

- Before the merge or rebase, read `base = git merge-base <local> <theirs>`. Add one read method
  for this to `writer/git_ops.Git`: a read, never a write, run through `Git.read` with the C
  locale like every other read. With `ahead == 0`, `base` is `local`.
- After an integration that succeeds (no conflict), compute the arrivals. The working tree is
  never used for this: it holds this machine's uncommitted writes. Only git's trees are read, at
  `base` and at `theirs`, through a new read method of `Git` (for example
  `git ls-tree -r -d --name-only <rev> -- <paths>` filtered by depth, or
  `git diff --name-only -z <base> <theirs> -- <paths>` and then the trees of the folders it
  names; the Driver picks the cheaper one). For each project of `self.projects`, with its
  `changes` folder relative to the surface root:
  - The CR folders at `theirs`: the direct subfolders of `changes/1-inbox/` (stage `1-inbox`), and
    those of `changes/2-backlog/P1/` through `changes/2-backlog/P4/` (stage `2-backlog/P<n>`).
  - The CR folders at `base`: the same, plus the direct subfolders of `changes/3-ready/` (stage
    `3-ready`).
  - A CR is identified by its folder name (the slug).
  - There is an arrival when a slug's stage at `theirs` is `1-inbox` or `2-backlog/P<n>`, and at
    `base` the slug is either absent from those three places (`before: None`), or in another one of
    the two notifying stages, or in `3-ready` (`before` is its folder at `base`).
  - A slug whose stage at `base` and at `theirs` is the same, or whose only change is its backlog
    row (`2-backlog/P2` to `2-backlog/P1`), is not an arrival. See open question 1.
  - A slug that is in `3-ready` or `4-batch` at `theirs` is never an arrival (Q3).
- Each arrival gives one `arrived@1` event, queued with `self._tell(event, [the project's Repo])`.
  The line goes to the project that holds the CR, whether or not it has a seat, because it is that
  project's news. `_flush` appends it at the cycle's end, through `journal.append(repo, [event],
  "writer")`, the one append function, outside the lifecycle locks, as for the `sync-*@1` lines.
  The audience stays `["project"]`.
- A conflict (`_conflict`), a failed integration or an offline fetch gives no `arrived@1` line.
  The next cycle that integrates the same upstream sees the same arrivals, because `base` has not
  moved: none is lost and none is told twice.
- Rule 5 holds by construction. Every write made on this machine (the board's, a command's, the
  Griller's, or a commit by hand) is in `local` and so at or below `base`. Only commits that exist
  in `theirs` and not in `local` can give a line. A local write of the same CR that was already
  pushed is an ancestor of `base`, and gives none either.
- An integration that the Chief of Staff makes by hand after a conflict (`_conflict_over`) is
  not seen by the writer as an integration. Its arrivals are not told (out of scope, below).
- Keep the cost small. The arrival reads run only when an integration ran (`HEAD..upstream` was
  non-empty). They are at most one or two git reads per integration, never one per project per
  cycle when nothing came in.

### 3. The board page

Q1 is already met: the surface server watches the planning files (`board/watch_files.py`:
system notifications, or a check every 5 s) and publishes 1 s after the last change. A merge or
rebase by the writer changes those files like any other write. Nothing on the page changes: no new
toast and no new panel. The evidence (below) checks that the arrived CR shows in the project's
read after the cycle.

### 4. The Chief of Staff's card (`skills/chantier/references/chief-of-staff.md`)

In "The watcher":
- In the sentence "It prints the project's forge events ... the issue events an outside poller
  writes (`tracker saw`)", add: what a pull of the surface brought into the inbox or the backlog
  (`surface pull brought`).
- In "*A watcher's end:*", next to the `tracker saw` rule, add: a `surface pull brought ...` line
  (another session's CR, new in the inbox or the backlog or moved between them): one line to the
  user that names the CR's folder and its stage, no tool call, no action, nothing written (not
  even a destination).
- In "*The pull path:*", in "Tell its `board wrote`, `tracker saw` and role `config@1` lines as
  above", add `surface pull brought`.

The agent files (`agents/`, `com.github.copilot/agents/`) do not change.

### 5. Project rules and docs

- `AGENTS.md`, which names what the writer appends:
  - In the long server bullet, "its writer's commits of the planning surface's published paths
    (below) and its journal lines (`sync-*@1`)" becomes "(`sync-*@1`, `arrived@1`)".
  - In the writer's paragraph, "appends `sync-*@1` lines to the journal" becomes "appends
    `sync-*@1` lines, and one `arrived@1` line per CR that an integration of the upstream brings
    new into a project's `1-inbox` or `2-backlog` or moves between them, to the journal".
  - No other rule changes. The writer's git commands stay the ones named: `merge-base` and
    `ls-tree`/`diff` are reads.
- `docs/planning-folder.md`:
  - In the `type` row of the field table, and in the sentence "Every line written today is for
    `["project"]`: ...", add `arrived@1` by the writer.
  - In the type table, add the row `| arrived@1 | the writer, after it integrates the upstream: a CR new in 1-inbox or 2-backlog, or moved between them | yes |`.
- `skills/chantier/references/concepts.md`, line 164 ("the journal's `sync-*` lines say"): add
  one clause saying that a CR another machine brings into the inbox or the backlog is told by an
  `arrived@1` line.
- `scenario/README.md`, in the "the surface's writer" step: add the `arrived@1` check (Evidence,
  below).

## Out of scope

- A timer, a fetch or a file watch of its own for arrivals (Q2).
- Notifying `3-ready`, `4-batch`, the archives or the trash (Q3).
- A new toast, banner or panel on the board page.
- A line in `status` for `arrived@1`.
- The arrivals in an integration that the Chief of Staff makes by hand after a writer conflict.
- An in-project planning folder: it has no writer and no remote pull.
- Routing to a role, CR or session other than the project audience.

## Evidence

All tests call the CLI's code in-process. They stay few, parametrized and fast (`just test`
budget).

1. `tests/test_writer_cycle.py` uses the existing rig (`writer_rig.Rig`: a real surface, a real
   bare origin, a second clone `r.other`). Extend `test_another_machines_commit_is_integrated_before_the_push`
   or add one parametrized test. Each case pushes from `r.other` and then drives cycles, and the
   project's journal lines (`r.lines()` / `r.types()`) are checked:
   - a new `1-inbox/<slug>/01-intent.md` gives exactly one `arrived@1` line, with
     `folder == "1-inbox/<slug>"`, `stage == "1-inbox"`, `before is None`, `upstream` equal to the
     origin's head, and `source == "writer"`;
   - a new `2-backlog/P2/<slug>/` gives one line with stage `2-backlog/P2`;
   - a CR moved by the other clone from `1-inbox/<slug>` to `2-backlog/P1/<slug>` gives one line
     with `before == "1-inbox/<slug>"`;
   - a CR moved from `3-ready/<slug>` to `2-backlog/P3/<slug>` gives one line with
     `before == "3-ready/<slug>"`;
   - a CR moved into `3-ready/` or `4-batch/`, and a CR moved only from `2-backlog/P2` to
     `2-backlog/P1`, give no line;
   - an edit of a file inside an inbox CR that already exists gives no line.
2. In the same file, rule 5: a CR filed on this machine (`r.write(...)` in `r.root`) and pushed by
   the writer gives no `arrived@1` line, in the cycle that pushes it or in any later cycle. This
   holds also when the same cycle integrates a commit of the other clone that brings another CR,
   which gives exactly one line, for that other CR.
3. In the same file, the conflict case. In `test_a_conflict_aborts_the_rebase_tells_it_and_ends_when_integrated`,
   or in a sibling test, the other clone's conflicting commit also adds a new inbox CR. The
   conflict cycle gives no `arrived@1` line.
4. One check that a second cycle over the same, already integrated upstream adds no second line.
5. `tests/test_event_types.py` passes with the new entry. It reads the shipped
   `hub/schemas.json` from the repository at the head under test, and `PUBLISHED["arrived@1"]`'s
   example validates. `just journal-schemas` reports nothing more to add.
6. One check of the sentence through the watcher's path, in `tests/test_watch_events.py`, or
   parametrized into an existing test of `watch_lines.told` or of the `events` topic's `_told`:
   an `arrived@1` line is told as `surface pull brought <folder> (new in <stage>); ...` or
   `(moved from <before>)`, and it wakes (`journal.waking` is True).
7. The page: after the integrating cycle of check 1, the board's read of the project (the state
   that `board/reads.state_of` serves for the `project` topic, or the backlog listing that feeds
   it) lists the arrived CR in its stage. This needs no page change. It proves Q1's page half
   with the existing file watch.
8. `scenario/run_scenario.py`, in the surface-writer step near line 10800 ("a commit pushed from
   a second clone of the surface is integrated"): the second clone's commit also adds
   `projects/<project>/changes/1-inbox/<slug>/01-intent.md`, and a new `check(...)` asserts that
   the project's events (the step's `events()` helper) hold one `arrived@1` line naming that
   folder. Mirror it in `scenario/README.md`. The long gate `just scenario (ubuntu-latest)` is
   green at the PR's head.
9. `just check` passes, and `just eval-dry-run` passes, because the change is under the CLI's
   `src/`.

There is no host or default matrix: the behaviour does not depend on the host or on a configured
value. The CR adds or changes no CI job.

## Open questions (for the user, through the Chief of Staff)

1. A CR that a pull moves only from one backlog row to another (for example `2-backlog/P2` to
   `2-backlog/P1`): notify or not? The answers say "between inbox and backlog". This
   specification reads that as no line for a change of priority alone. The board's own
   priority moves do wake (`board@1` action `move`).
2. A CR that a pull brings back from `3-ready` into the inbox or the backlog: notify (this
   specification's reading, with `before: 3-ready/<slug>`), or not, because under Q3 it is the
   owning Chief of Staff's own doing? A CR coming back from `4-batch`, the archives or the trash
   would show as `new` (`before: null`), because those places are not read at `base`.
