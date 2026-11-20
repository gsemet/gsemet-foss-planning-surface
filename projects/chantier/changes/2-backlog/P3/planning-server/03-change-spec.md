# Change Specification: the surface's writer, and five ideas borrowed from Vercel Board

Origin: verbal (2026-11-10, Beads study; grilled 2026-11-20). No tracker issue.

## 1. Goal, in the user's terms

The plan lives outside the project, in a planning surface, as Markdown and JSON that anyone can
browse on the forge (GitHub or GitLab). Putting the plan in the project "hits its limits very
fast"; the external surface is the answer, even if heavier. In it:

- **One writer.** One process commits, rebases and pushes the surface: the surface server that a
  Chief of Staff starts and guarantees. Every change reaches the forge within 5 minutes. The
  surface's own autosync tool is no longer needed. A conflict between two clones that did not sync
  is raised to the Chief of Staff, who resolves it to its best guess or asks the user.
- **No writer, no write.** While no surface server runs, the CLI refuses every write to the
  surface, with no fallback. A Griller alone records nothing.
- **Five ideas from Vercel Board, built in chantier, with no Board dependency:** leases on the
  work a Driver holds, typed waits (gates), typed journal events `name@N`, an "explain access"
  command, and the plan's storage behind a minimal interface checked by one conformance test.

Several machines are not weighed: two writers on two machines meet as any two git clones do, and
their conflict follows the conflict path below.

## 2. Natural parts

The CR is large. It splits along its seams, in this order of dependency; each part is a PR of its
own and may be its own CR (open question 1):

| Part | What | Needs |
| --- | --- | --- |
| A. Typed events | the journal's lines become `name@N`, a published schema never changing | none |
| B. Store interface | the plan's published writes go through one interface, with a conformance test | none |
| C. The writer | the surface server commits, rebases and pushes; writes refused with no writer; the surface's autosync support replaced | A, B |
| D. Leases | the Driver's lease on its CR and on the stack; `close` on Copilot reads it | A |
| E. Typed waits | a blocked CR records what it waits for; the hub signals when the forge shows it done | A |
| F. `access` | why a session may or may not write, claim or push | C, D |
| G. Outside contributions | a PR merged without chantier ends as a report in the archives | C |

The rest of this document specifies all seven, part by part.

## 3. Decisions carried from `02-answers.md`

| Decision (date) | Where it lands |
| --- | --- |
| "No setup" is for the target project; the surface may take a YAML/JSON configuration; coding rules stay in the project's `AGENTS.md` (11-10) | §C.1: the writer needs nothing but the surface's clone with an upstream; no new key in the project's repository; §C.12 the surface's setup |
| Minor outside contributions without chantier; ideally a report in the archives (11-10) | Part G |
| Upstream churn rules out Beads as the store; installing a binary is not the problem (11-10) | §9 out of scope |
| Hash IDs rejected: "ce serait pas trié et j'ai déjà un slug" (11-10) | §9 out of scope; leases and waits use the CR's id and small numbers |
| Heartbeat/reclaim "ça vaudrait le coup" (11-10); leases replace the "session file written in the last 5 minutes" heuristic (11-20) | Part D |
| Gates stay generic: GitHub PR and GitLab MR; Claude Code, Codex, GitLab Duo, Copilot (11-10) | Part E: types named by the fact, never by the forge |
| The external surface is the most important point (11-10) | Part C |
| The only writer is the Chief of Staff, who guarantees the server (11-10) | §C.2: the writer runs in the surface server a Chief of Staff starts |
| One Chief of Staff per project, several projects in one surface repository (11-10) | §C.3: one writer per surface and machine serves every project of the surface; seats unchanged |
| Everything in Markdown, browsable on the forge; a separate planning project is better than a dedicated branch; a hidden ref and a database are ruled out (11-10) | §C: the writer pushes the surface's default branch; Part B names the dedicated branch as a backend not built here |
| The storage table (11-10): events as additional Markdown and JSON files; files read directly on the forge; sync within 5 minutes; conflicts raised to the Chief of Staff, best guess or ask the user; setup to be defined; Dolt set aside | §C.5 (the 5-minute bound), §C.7 (conflicts), §C.12 (setup); Dolt in §9 |
| Chantier takes the sync over; n Chiefs of Staff on n projects of one surface synchronise their pushes; about three checkouts at worst (11-10, from planning-repo) | §C.3, §C.7 |
| A running batch's state stays local to the steering machine (11-10, planning-repo answer 4) | §C.4: the writer never stages an ignored file; leases and waits live in `batch.json` |
| No OKF for now (11-10) | §9 |
| Messages and plan storage are two things; no Board dependency, hosted or local; chantier's journal, surface server and watchers stay the channel (11-20, Q1-Q2) | §9; Part A extends the existing journal |
| All five Board ideas go in this CR (11-20, Q3) | Parts A, B, D, E, F |
| Chantier takes the sync over: the surface server, elected and guaranteed by the Chief of Staff, is the one writer; commits, rebases and pushes within 5 minutes; raises conflicts to the Chief of Staff; the surface's own autosync tool is no longer needed (11-20, Q4) | Part C |
| With no server, writes are refused until a Chief of Staff starts it again; no fallback; a Griller alone records nothing (11-20, Q5) | §C.8, §C.11 (cards) |
| One watcher-autosync at a time for the surface; several machines inherent to distributed git, not weighed; specify every state and message (11-20, Q6) | §C.3 (one writer per surface and machine, by an OS lock), §C.7 (two machines meet as clones), every part's states and messages |
| Spec critic: yes (11-20) | not this document's; the Chief of Staff runs it |

Read as superseded: the 11-10 table's "the other sessions talk to the Chief of Staff's session"
and the intent's "thin client, the write sent to the server". The 11-20 grill makes the surface
server the one writer: sessions on the machine write the surface's working tree as today, under
the CLI's locks, and only the writer commits and pushes. Open question 2 asks the user to confirm.

## 4. Words

- **Writer:** the thread of the surface server (`chantier board`) that commits, rebases and pushes
  the planning surface. It exists only in external mode.
- **Published path:** a path of the surface's working tree that git does not ignore, under
  `projects/` or the surface root's `chantier.yaml` / `chantier.yml`. A path the planning
  folder's `.gitignore` lists (`core/files.py`, `IGNORED`) is local, never published.
- **Published write:** a CLI write that creates, changes, moves or deletes a published path.
- **Lease:** a numbered, time-limited hold of a Driver on the unit `take` gave it (a CR, or the
  stack), renewed by the Driver's commands, ended by its hand-back.
- **Wait:** what a blocked CR waits for, typed by the fact: `answer`, `approval`, `pipeline`.
- **Event type:** `name@N`, the name and the published version of a journal line's payload.

---

## Part A. Typed events

### A.1 What changes

The project's journal, `forge-journal.jsonl` (`hub/journal.py`), gets a version 2 line in which
the payload's kind and version are one field, `type`, of the form `name@N`. A published
`name@N` never changes; a change is a new `name@N+1`.

- New module `skills/chantier/scripts/cli/src/chantier/hub/schemas.py`: one pydantic model per
  published type (`model_config = ConfigDict(extra="forbid", frozen=True)`), a `PUBLISHED`
  mapping `"name@N" -> model`, and `validate(type, payload)`.
- New file `skills/chantier/scripts/cli/src/chantier/hub/schemas.json`, shipped: the JSON Schema
  (`model_json_schema()`) of every published type, keyed by `name@N`, sorted, UTF-8, LF. It is the
  published record: a test (A.4) fails when a model's schema differs from its entry.

### A.2 The line, version 2

In this order: `v` (2), `seq`, `t`, `type`, `source`, `audience`, then the payload of its type.
`source` is one of `hub`, `board`, `cli`, `writer` (new). `audience` is as in version 1.

Published types, each `@1`:

| Type | Payload | Written by | Wakes a watcher |
| --- | --- | --- | --- |
| `merged@1` | `batch`, `cr`, `pr`, `into`, `into_cr`, `merged_at`, optional `landed_with`, `landed_at` | hub, board | yes |
| `checks-red@1` | `batch`, `cr`, `pr`, `head` | hub | yes |
| `config@1` | `key`, `old`, `new`, `batch` | board | yes |
| `board@1` | `action`, `items`, `text`, `wakes` | board | when `wakes` |
| `sync-conflict@1` | `upstream` (sha), `local` (sha), `files` (paths relative to the surface root), `projects` | writer | yes |
| `sync-blocked@1` | `reason` (one of C.6's reasons), `text` | writer | yes |
| `sync-late@1` | `since` (time of the oldest change not pushed), `paths` (count), `ahead` (commits) | writer | yes |
| `sync-resumed@1` | `after` (`conflict`, `blocked`, `offline`) | writer | no |
| `lease-expired@1` | `batch`, `cr` (a CR id or `stack`), `lease` (its number), `expired_at` | hub | yes |
| `wait-cleared@1` | `batch`, `cr`, `wait` (its id), `wait_type` (`approval` or `pipeline`), `ref`, `seen_at` | hub | yes |

The first four are the version 1 kinds frozen as they are today; their payloads do not change.

### A.3 Reading and writing

- `journal.append(repo, events, source)` takes events as `{"type": "name@N", "audience"?, ...}`,
  validates each payload against its model, and raises `ValueError` (a code fault) on an unknown
  type, a payload its model refuses, a wrong source or audience. It keeps its lock, its `seq` and
  its duplicate rule; `_key` dispatches on the type's name. Every writer (hub, board, CLI,
  writer) still goes through this one function.
- `journal.read` gives every line an effective `type`: a version 0 or 1 line's `kind` becomes
  `<kind>@1`, its `source` from `source` or `by`, its audience `project` when it has none. A
  version 0 or 1 line is never rewritten.
- A version 2 line whose `type` is not in `PUBLISHED` (a newer chantier wrote it), or whose
  payload its model refuses, counts for `seq`, is listed with the unreadable lines by number, and
  wakes no one. A line with `v` above 2 is as today's newer line.
- `event_text` dispatches on the type's name; the texts of the four existing kinds do not change.
  The texts of the new types are in C.10, D.6 and E.5.
- The module docstring of `hub/journal.py` is rewritten to describe version 2 and the types.

### A.4 Evidence

- `tests/test_event_types.py` (new, in `skills/chantier/scripts/cli/tests/`):
  - reads the shipped `hub/schemas.json` from the repository at the head under test and compares
    it with `model_json_schema()` of every model in `PUBLISHED`: an entry changed or removed fails
    with `published schema <name@N> changed: publish <name@N+1> instead`; a model with no entry
    fails with `schema <name@N> not published in schemas.json`;
  - parametrized over every published type: a valid payload appends one version 2 line with the
    fields in order; a payload with an extra or a missing field raises `ValueError` and writes
    nothing;
  - a prepared journal (a case the shipped file cannot hold) with a version 0 line, a version 1
    line of each kind, a version 2 line of an unknown type and one with a refused payload: `read`
    gives the effective types, the unknown and refused lines are listed by number, and `watch
    --once --after 0` prints only the known lines.
- `tests/test_event_audience.py` and `tests/test_watch_events.py` keep passing with the `type`
  field (their prepared lines updated where they write new lines).

---

## Part B. The plan's storage behind a minimal interface

### B.1 What changes

New package `skills/chantier/scripts/cli/src/chantier/store/`:

- `base.py`: the protocol `PlanStore`, and `Features` (a frozen set of the words below).
  - `root: Path` (the planning folder), `features: frozenset[str]`.
  - `read_text(rel) -> str`, `exists(rel) -> bool`, `listdir(rel) -> list[str]`.
  - `write_text(rel, text)`, `write_json(rel, data)`: atomic, UTF-8 without BOM, LF kept.
  - `move(rel_src, rel_dst)`: a file or a CR folder, across stages; refused when the target exists.
  - `remove(rel)`: a file or an empty folder.
  - `lock()`: the context manager of the planning folder's lifecycle lock (today
    `lifecycle/stages.py`, `changes_lock`).
  - `published(rel) -> bool`: whether the path is published (not matched by the planning folder's
    `.gitignore` patterns, `IGNORED`).
  - `check_publish(rels)`: raises the refusal of C.8 when one of `rels` is published and the store
    cannot publish now; returns otherwise.
  - Features: `publishes` (published paths reach a remote), `local-files` (ignored files kept beside
    the published ones), `refuses-without-publisher` (a published write is refused while the
    publisher is down).
- `folder.py`: `FolderStore(changes)`: the in-project planning folder. Features: `local-files`.
  Publishes nothing, never refuses (in-project mode is unchanged).
- `surface.py`: `SurfaceStore(repo)`: the external planning folder, the same files plus the
  writer's gate. Features: `publishes`, `local-files`, `refuses-without-publisher`.
  `check_publish` reads the live `writer` entry of `server.json` (C.4); with none it refuses.
  This is the "server" backend of the user's list.
- `Repo.store` (in `core/repo.py`): the store of the repository, chosen by `repo.external`.

The dedicated-branch backend (the plan on a branch of the project's repository) is not built in
this CR: the conformance test declares it, and it is skipped with the reason
`dedicated-branch backend not built (planning-server open question 3)`.

Every published write of the CLI goes through `repo.store`: `file`, `triage`, `abandon`,
`restore`, `init`, `open`, `take`, `handback`, `order` (each kind that moves or writes a CR's
folder: `add`, `merged`, `drop`), `cancel`, `close`, `summary set`, `summary label`, `summary
group`, `verdict` when it writes in a CR's folder, the release commands that write the archive,
and the board's backlog writes (`board/write_api.py`, through `lifecycle/backlog.py`) and its
Configuration page's save (`board/config_api.py`, `projects/<name>/chantier.yaml`). Each command
calls `check_publish` with every published path it will touch **before** it changes anything, so a
refused command leaves the folder and the batch's record as they were. Local files (`batch.json`,
`events.jsonl`, STATUS files, locks, the journals, `seat.json`) may keep `core/files.py`'s
functions directly; they are never refused.

### B.2 Evidence

- `tests/test_store_conformance.py` (new): one test body parametrized over the backends
  `folder`, `surface` (with a writer entry live, then with none) and `dedicated-branch` (skipped,
  B.1). A case whose feature the backend declares absent is skipped by feature, never failed:
  - UTF-8 round trip of a text with non-ASCII letters, no BOM written, LF kept;
  - `write_json` then `read_text` gives the same JSON;
  - `move` of a CR folder from `2-backlog/P3/` to `3-ready/` keeps every file's bytes; a move onto
    an existing folder is refused and changes nothing;
  - `lock` is exclusive: a second `lock()` from another thread waits, and times out with the
    lifecycle lock's message;
  - `published` agrees with `IGNORED` for `seat.json`, `4-batch/batch.json`, `work/gates/x.log`
    (local) and `3-ready/x/01-intent.md`, `5-archives/batches/batch-01.json` (published);
  - `refuses-without-publisher`: with no live writer, `check_publish(["3-ready/x/01-intent.md"])`
    raises exit 2 with C.8's text, and `check_publish(["4-batch/batch.json"])` returns.
- `tests/test_surface_writes.py` (new), parametrized over the command table of B.1 on a prepared
  external surface with no writer: each command exits 2 with C.8's refusal, and the planning
  folder's tree fingerprint (every path and its bytes) and `batch.json` are unchanged. The same
  table with a live writer entry: each command succeeds. In-project, no command is refused.

---

## Part C. The writer

### C.1 Where it runs

- In the surface server (`chantier board`), as a daemon thread beside the hub's
  (`board/command.py` starts it as it starts `HubThread`), only when the folder served is an
  external planning surface. An in-project board starts no writer, and the in-project mode runs no
  git write, as today.
- A board started by a Chief of Staff (`board --seat <id>`) and a board started by hand (no
  `--seat`, the "With no agent" path) both run the writer (open question 4).
- New package `skills/chantier/scripts/cli/src/chantier/writer/`: `loop.py` (`WriterLoop.poll(now)`
  and `WriterThread`, the shape of `hub/loop.py`), `cycle.py` (one cycle, C.5), `git_ops.py` (the
  git commands, through `core/git.py`'s `git`), `record.py` (the `writer` entry, C.4), `times.py`
  (C.5's times and the test seam), `lines.py` (C.10's texts).
- The writer needs nothing beyond what the surface has: `git`, the surface's clone on its default
  branch with an upstream, and the network for fetch and push. Git LFS is needed only when the
  surface's `.gitattributes` names LFS files that change; git's own error then blocks the writer
  (C.6, `git-error`).

### C.2 Election and lifetime

- The writer holds an OS lock, `chantier/writer.lock` in the surface's git common folder, taken
  with `core.files.try_lock`, never waited on, released by the OS when the process ends (as
  `hub.lock`). One writer per surface and machine. A watcher never takes it.
- It starts with the server, after the server's own election (`server.json`'s `server` entry);
  a second session's `board --seat` registers on the running server and starts no second writer.
- It stops when the server stops (its seats gone, the user's stop, a signal). Before it lets the
  lock go it runs one **final cycle** (C.5) limited to 30 s: commit what is pending, push when it
  can. What the final cycle does not push stays committed locally and is pushed by the next writer.
- A session's compaction or reload does not stop it (the board survives a compaction). A machine
  restart or the app's close ends it; the next Chief of Staff session starts the server again
  (session start, as today) and the new writer picks up every change left in the working tree.

### C.3 Several projects, several Chiefs of Staff, several machines

- One writer serves every project of the surface on its machine. Each Chief of Staff of a project
  of the surface guarantees it through its seat on the server; the writer stops only with the
  server.
- Commits touch `projects/<name>/` sub-trees; the writer commits all projects' changes of a cycle
  together, the commit message naming the projects (C.5).
- Two machines, each with its writer, meet as two git clones: a push refused because the other
  pushed first is integrated by rebase (C.5), and a rebase conflict goes to the Chief of Staff
  (C.7). Nothing else coordinates them.

### C.4 The record: the `writer` entry of `server.json`

Written by the writer only, through `hub/state.py`'s `modify` (its lock and its atomic replace);
the `hub/state.py` docstring names it. Fields:

- `pid`, `version`, `started` (as the other entries; an entry whose process has not been alive
  since `started` is no entry, `live_entry`).
- `state`: one of `syncing`, `synced`, `pending`, `offline`, `conflict`, `blocked`.
- `reason`: empty, or C.6's reason word; `text`: one line, at most 200 characters (git's message,
  cut).
- `since`: when the state began.
- `pending`: the count of published paths changed and not committed; `pending_since`: the time
  the oldest of them was first seen, or null.
- `ahead`: the count of local commits not pushed; `unpushed_since`: the time of the oldest, or
  null.
- `last_commit`: `{sha, at}` or null; `last_push`: `{sha, at}` or null; `last_fetch`: time or null.
- `conflict`: while `state` is `conflict`, `{upstream, local, files}`, else null.

Readers derive one more state, `off`, when there is no live `writer` entry. `state.py` gets
`WRITER = "writer"` and `write_writer(git_dir, record)`; `remove_entry` removes it at the end.

### C.5 The cycle

Times (constants in `writer/times.py`; the test seam `CHANTIER_WRITER_TEST_TIMES`, read only there,
as `<every>:<quiet>:<max_wait>:<fetch_every>:<late>` in seconds, as `CHANTIER_HUB_TEST_TIMES`):

| Time | Value | Meaning |
| --- | --- | --- |
| `every` | 30 s | a cycle at least this often |
| `quiet` | 10 s | the changes have not moved for this long: commit |
| `max_wait` | 120 s | the oldest change is this old: commit even if it still moves |
| `fetch_every` | 60 s | a fetch at least this often with nothing to push |
| `late` | 300 s | the 5-minute promise: past it, `sync-late@1` |

The bound: a change is committed within `max_wait + every` (150 s) and pushed in the same cycle
when the remote answers, inside the user's 5 minutes.

A cycle also starts at once when `chantier/writer.wake` in the git common folder is newer than the
last cycle's start (the writer looks at its time every second): `sync now` (C.9) and the board's
button touch it.

One cycle, in order; each step's failure goes to the state named, and ends the cycle:

1. **In conflict?** When `state` is `conflict`: if no rebase, merge, cherry-pick or revert is in
   progress, `HEAD` is on the surface's default branch, and the recorded `upstream` is an ancestor
   of `HEAD` (the Chief of Staff integrated, C.7), clear the conflict, append `sync-resumed@1`
   (`after: conflict`) and go on; else do nothing more this cycle (no git command but reads).
2. **Preconditions** (C.6). A failing one: state `blocked` with its reason; `sync-blocked@1` once
   per episode (an episode ends when the cycle passes the preconditions again, which appends
   `sync-resumed@1`, `after: blocked`).
3. **Changes.** `git status --porcelain=v1 -z --untracked-files=all -- projects chantier.yaml
   chantier.yml` (ignored files are never listed). A fingerprint of the list and each path's size
   and mtime tells whether the changes moved since the last cycle. With changes: state `pending`,
   `pending` counted, `pending_since` kept from the first sighting.
4. **Commit**, when there are changes and (`quiet` has passed since they last moved, or
   `pending_since` is older than `max_wait`, or this is the final cycle, or a `sync now` asked):
   under every project's lifecycle lock (`changes_lock`, taken in the projects' sorted order), `git
   add -A -- projects chantier.yaml chantier.yml`, then `git commit -m <message>` with the user's
   own git identity and hooks (never `--no-verify`). The message: first line `chantier: <projects,
   comma-separated>: <n> files`, then a blank line and the paths, at most 20, then `and <k> more`.
5. **Fetch**, when `ahead` > 0, or `fetch_every` has passed since `last_fetch`: `git fetch <remote>
   <branch>` (the branch's upstream). A network failure (C.6's rule): state `offline`.
6. **Integrate**, when the upstream has commits `HEAD` lacks: with `ahead` = 0, `git merge
   --ff-only <upstream>`; else, under the projects' lifecycle locks, `git rebase --autostash
   <upstream>`. A rebase that stops on a conflict: C.7.
7. **Push**, when `ahead` > 0: `git push <remote> HEAD:<branch>`, never forced. Refused as not a
   fast-forward: back to step 5, at most 3 times in the cycle, then `pending` stays and the next
   cycle tries again. A network failure: state `offline`. Done: `last_push`, `ahead` 0.
8. **State.** `synced` when nothing is pending and `ahead` is 0, else `pending`. When the oldest
   change not pushed (`pending_since` or `unpushed_since`) is older than `late`: `sync-late@1`
   once per episode (it ends when everything is pushed).

`offline`: every later cycle retries steps 5 to 7; the first success appends `sync-resumed@1`
(`after: offline`). Commits go on while offline. No line is appended for `offline` itself; only
`sync-late@1` once its 5 minutes pass.

A network failure is a fetch or push whose git message holds one of git's transport failures
(`Could not resolve host`, `unable to access`, `Connection timed out`, `Connection refused`,
`Could not read from remote repository`, `Network is unreachable`); any other failing git command
is `blocked` with `git-error`.

### C.6 Preconditions and blocked reasons

Checked at each cycle's step 2, in this order:

| Reason | When | Way out (C.10) |
| --- | --- | --- |
| `not-a-branch` | `HEAD` is detached, or not on the surface's default branch (`origin/HEAD`, `core/git.py`'s `default_branch`) | check out the default branch |
| `no-upstream` | the branch has no upstream | set it (`git branch -u <remote>/<branch>`) |
| `git-busy` | a rebase, merge, cherry-pick or revert is in progress that is not the writer's own conflict | finish or abort it |
| `staged` | the index holds changes the writer did not stage, seen at two cycles in a row | commit or unstage them by hand |
| `foreign-autosync` | the surface's autosync tool still runs: `<git dir>/ai-autosync/control.json` enabled and a live leader in `watcher.json` (read by the existing `autosync/records.py` and `autosync/reading.py`, which stay for this check only) | stop the tool (`uv run scripts/ai-autosync-git.py stop .`) |
| `git-error` | any other git command of a cycle failed (a hook, LFS, a lock file left by a crash) | read `text`, repair, then `sync now` |

The `staged` rule waits one cycle so that a person staging and committing by hand within seconds
is not blocked.

### C.7 Conflicts

When the rebase of step 6 stops on a conflict:

1. The writer runs `git rebase --abort`: the working tree and the local commits are as before the
   rebase; nothing is lost.
2. State `conflict`, with `conflict.upstream` (the upstream's sha), `conflict.local` (`HEAD`) and
   `conflict.files` (the paths git named as conflicted).
3. It appends `sync-conflict@1` to the journal of each project whose folder holds a conflicted
   path, audience `project`; when no path is under a project's folder, to every project that has
   a seat.
4. From then on, until step 1 of a later cycle sees the integration, it runs no git write: it
   neither commits nor pushes. CLI writes are still allowed; they wait in the working tree.

The Chief of Staff resolves (its card, C.11): in the surface's checkout, `git fetch`, `git rebase
--autostash <upstream>`, each conflicted file resolved to its best guess (both sides' intent kept:
for Markdown, both sides' added text, in time order; for a `summary.json`, the side with the later
`summarized`; for the board's `next-batch.json` or a `chantier.yaml`, the user's) or, when it
cannot tell, the user asked; `git add` each, `git rebase --continue`. It never skips a commit that
holds a change, never force-pushes, never pushes by hand: the writer sees the integration (step 1)
and pushes at its next cycle.

A Chief of Staff on another machine whose writer meets the same conflict resolves on its own
machine the same way; the first push wins and the other integrates at its next fetch.

### C.8 Writes with no writer

- In external mode, `SurfaceStore.check_publish` refuses a published write while there is no live
  `writer` entry (state `off`). Exit 2 (precondition). Text, one line:
  `error: <command>: the surface's writer is not running: nothing written; for the Chief of Staff: start the surface server ($CHANTIER board --seat <session id>)`
- A writer in `pending`, `offline`, `blocked` or `conflict` is running: the write is done and the
  command's output adds one line: `writer: <state>: not pushed yet (<reason or ahead count>)`.
- Local writes (B.1) are never refused: a running batch keeps its record, its rounds, its notes
  and its asks with no writer; what moves a CR's folder (`open`, `take`, `handback`, `order
  merged`, `close`) is refused.
- Writes made outside the CLI (an agent writing `02-answers.md` with its own tool) cannot be
  refused by the CLI; the cards say that a session records nothing with no writer (C.11). Such
  files left in the working tree are committed by the next writer.
- The board's backlog writes and Configuration saves with no writer: impossible, the board is the
  server and runs the writer. A writer that could not start (its lock held by another process on
  the machine) leaves the board serving with the line `board: writer not started: <reason>`, and
  the board's write routes answer 409 with C.8's text.

### C.9 Commands

- `chantier sync` (new, declared in `declare/sync.py`, handler `commands/sync.py`, scope no-batch):
  prints the writer's state line (C.10) and, when `conflict`, one line per conflicted file. In
  project mode: `sync: in-project planning folder: chantier commits nothing`. Exit 0. Reads only.
- `chantier sync now`: touches `chantier/writer.wake` and waits up to 10 s for the next cycle's end
  (the `writer` entry's `since` or `last_push` moving), then prints the state line. With no writer:
  C.8's text, exit 2. In-project: as above, exit 0.
- `status` (`commands/batch_status.py`): in external mode, one `writer:` line right after the
  batch's first line, with a batch or none (it replaces `_autosync_lines`). Also on the Foreman's
  heartbeat form (`status --refresh --epoch`).
- `seat` and `seat take`: in external mode, the `writer:` line after the seat's lines.
- `preflight` P13 becomes the writer's check (C.10), warn-only, external mode only; P13's
  autosync texts go.
- `board`: one more start line in external mode, `writer: <state line>` or `board: writer not
  started: <reason>`.

### C.10 Messages

The `writer:` line, by state (times `HH:MM` local, as `status` prints them):

| State | Line |
| --- | --- |
| `synced` | `writer: synced, pushed HH:MM` (`, never pushed` when `last_push` is null) |
| `pending` | `writer: pending, <n> paths changed since HH:MM, <k> commits to push` |
| `syncing` | `writer: syncing` |
| `offline` | `writer: offline since HH:MM, <k> commits not pushed: retries every 30 s` |
| `conflict` | `writer: conflict with the remote on <files, at most 3, then "and <k> more">: for the Chief of Staff: integrate by rebase in the surface's checkout, resolve each file to your best guess or ask the user; the writer pushes once integrated` |
| `blocked` | `writer: blocked (<reason>): <text>; for the Chief of Staff: <way out of C.6>` |
| `off` | `writer: not running: writes to the surface are refused; for the Chief of Staff: start the surface server ($CHANTIER board --seat <session id>)` |

P13: `P13 ok   the surface's writer runs: <state line without "writer: ">` for `synced`, `pending`,
`syncing`; `P13 warn <the writer: line>` for the others. When the surface's rules still name
`.agents/guidelines/autosync.guidelines.md`, a second warn line: `P13 warn the surface's rules
name its autosync tool: chantier's writer replaces it; remove the mention from the surface's
AGENTS.md`.

Journal texts (`event_text`), for `status` and a watcher's end:

- `sync-conflict@1`: `writer saw a conflict with the remote on <files>; for the Chief of Staff:
  integrate by rebase, resolve to your best guess or ask the user`
- `sync-blocked@1`: `writer blocked (<reason>): <text>; for the Chief of Staff: <way out>`
- `sync-late@1`: `writer late: <n> paths and <k> commits not pushed since HH:MM; for the Chief of
  Staff: read sync, tell the user if it lasts`
- `sync-resumed@1`: `writer resumed after <after>` (it wakes no one; it rides with the next).

`status` prints the journal's writer lines only while their episode lasts (the `writer` entry
still in that state), so a resolved conflict leaves no line.

### C.11 Cards, docs and project rules

Cards (`skills/chantier/references/`), each statement replaced where it is today:

- `concepts.md`, "Planning surface": the autosync paragraph becomes the writer: the surface server
  commits, rebases and pushes the surface within 5 minutes; no session commits or pushes the
  surface by hand; writes refused with no writer; a conflict goes to the Chief of Staff. "Planning
  folder": published versus local paths. New words: lease, wait, event type.
- `chief-of-staff.md`, "With a planning surface": the hand-commit rule and the autosync bullets go;
  in their place: never commit or push the surface by hand; on a `writer:` line or a writer's
  journal line, act as C.10 says (conflict: C.7's resolution; blocked: the way out, else tell the
  user; offline or late: tell the user once per episode); `sync now` when a step must reach the
  forge at once. The table's "start autosync"/"stop autosync" row goes; "rescan" loses "without
  autosync, commit the planning folder by hand".
- `session-start.md`: "The board" explains that the server is also the surface's writer, and that
  a no starts no server, so the session's writes to the surface are refused; "The surface's
  autosync" paragraph goes.
- `griller.md`, "In a planning surface": no join, no commit, no push; read the `writer:` line of
  `$CHANTIER seat` at start; with `writer: not running`, record nothing (no file, no answer, no CLI
  write), say so to the user in one line, and wait for a Chief of Staff to start the server. "In a
  worktree": "you join no autosync" goes.
- `foreman.md`: the autosync join bullet becomes: never commit or push the surface; on a `writer:`
  line in `conflict` or `blocked`, `$CHANTIER asks "writer <state>: <reason>"` once per episode.
- `routing.md` and `startup-manifest.json` only if a text they hold changes (the Driver checks).

Docs: `docs/planning-modes.md` ("The planning surface", "What runs where", "Grillers", "The
surface's autosync" becomes "The surface's writer", "With no agent", "Two sessions on one surface",
"Setting one up"), `docs/web-board.md` (the pill), `docs/boards.md` if it names the autosync,
`README.md` where it names the surface's sync.

Project rules: `AGENTS.md` of chantier changes (the user's merge of the PR is their approval):

- The write list ("chantier writes only in the planning folder ...") adds: the surface server's
  writer commits, rebases and pushes the planning surface's published paths, and keeps
  `chantier/writer.lock` and `chantier/writer.wake` in the git folder.
- "The CLI's scope": a third named exception: the surface server's writer (C.1 to C.7).
- "The CLI has two named git exceptions": becomes three: the writer's `git add`, `commit`,
  `fetch`, `merge --ff-only`, `rebase --autostash`, `rebase --abort` and `push` (never forced),
  in the surface's checkout only; the board's autosync join goes.
- The server's description: "the server runs no git either, but its autosync join" becomes "the
  server runs no git but its writer's".

### C.12 The surface's setup, and what goes

- Setup: unchanged (`projects/<name>/project.md`, `checkout.yml`, `changes/`), plus the surface's
  clone on its default branch with an upstream. No new configuration key.
- Removed from the CLI: `board/autosync_api.py`, `board/autosync_tool.py`, the routes `GET
  /api/autosync` and its actions, the `autosync` key of `GET /api/board` (replaced by `writer`),
  `autosync/lines.py`, `autosync/view.py`'s naming of participants and the board's join; kept:
  `autosync/site.py`, `records.py`, `reading.py` for C.6's `foreign-autosync` only.
- Removed from the scenario: `scenario/fake_autosync.py` and its cases.
- The surface's own `AGENTS.md` and `.agents/guidelines/autosync.guidelines.md` belong to the
  user's surface, not to chantier: the release notes say to remove the autosync rules and the
  "commit by hand" rule there once the release runs, and P13 warns until then.

### C.13 The board

`skills/chantier/scripts/cli/src/chantier/board/web/`: read `DESIGN.md` first and keep it true.

- The autosync pill becomes the writer's pill, by state: `synced` green, `pending` and `syncing`
  blue, `offline` grey, `conflict` and `blocked` red, `off` grey with "writer off". On a phone, a
  dot, as today.
- Its panel: the state line's facts (state, since, last push, pending paths, commits to push, the
  conflict's files or the blocked reason with its way out). One button, **Sync now**, `POST
  /api/writer/sync` (behind the key, as the other write routes), which touches `writer.wake`; no
  Start, Stop or Approve.
- `GET /api/board` carries `writer`: the `writer` entry as read, or `{"state": "off"}`.

### C.14 Evidence

pytest (`skills/chantier/scripts/cli/tests/`, in-process, on a temporary surface with a bare
origin, the writer's `poll(now)` driven with no sleep):

- `test_writer_cycle.py`, parametrized:
  - a new file under `projects/a/changes/1-inbox/x/` is committed after `quiet` and pushed: the
    bare origin's `main` holds it, the message's first line is `chantier: a: 1 files`;
  - a file that keeps changing is committed once `max_wait` passes;
  - an ignored file (`seat.json`, `4-batch/batch.json`, `forge-journal.jsonl`) and a file outside
    `projects/` (`scripts/x.py`) are never committed;
  - the origin moved (a second clone pushed a change to another project): the writer rebases and
    pushes, no conflict, both changes on `main`;
  - the same file changed on both sides: `git rebase --abort` ran (no rebase in progress, local
    commits intact), state `conflict` with the file, one `sync-conflict@1` line in that project's
    journal; no commit while in conflict; after a resolution done in the test (rebase, resolve,
    continue), the next cycle appends `sync-resumed@1` and pushes;
  - each blocked reason of C.6 (detached HEAD, no upstream, a `MERGE_HEAD`, a staged file seen
    twice, a fake `ai-autosync` group enabled with a live leader pid, a failing `pre-commit` hook):
    its state, reason and one `sync-blocked@1` line;
  - offline (the origin's path renamed away, so the push fails with `Could not read from remote
    repository`): state `offline`, commits go on; past `late`, one `sync-late@1`; the origin back:
    pushed and `sync-resumed@1`;
  - the final cycle commits and pushes a pending change on stop;
  - a second `WriterLoop` on the same git folder does not get `writer.lock`.
- `test_writer_lines.py`: every C.10 line, from a prepared `writer` entry per state (a case the
  shipped files cannot hold), and the absence of any `writer:` line in project mode.
- `test_surface_writes.py` (B.2): the refusal of every command with no writer.

Scenario, unit `surface-board` (`scenario/run_scenario.py`, with `CHANTIER_WRITER_TEST_TIMES`
shortened): the board started with `--seat` on the two-project surface prints its `writer:` line;
`file` in project a, then `triage`, reach the bare origin within the shortened bound; `status` and
`seat` print `writer: synced`; a commit pushed from a second clone of the surface is integrated;
a conflicting change made on both sides yields the conflict line in `status` and the journal, and
the scripted Chief of Staff's resolution (fetch, rebase, a resolved file, continue) is pushed by
the writer; the board stopped, `file` is refused with C.8's text and the folder unchanged; the
autosync cases and `fake_autosync.py` are gone. `scenario/README.md`'s Coverage list is updated
(with each case's test name, as `test_scenario_coverage.py` checks).

---

## Part D. Leases

### D.1 What a lease is

- Every `take` (of a CR, or of the stack) starts a lease for that unit: number `n` (1 at the first
  take of the unit, then the last number plus one), `taken` and `expires` = now + `TTL`.
- `TTL` is 10 minutes (a constant in `core/leases.py`, new; open question 5). The Driver renews at
  a third of it.
- The lease is in `batch.json` (local, never published): `CrEntry.lease` and `BatchRecord.stack_lease`,
  each `{n, taken, renewed, expires, ended}` or null (`core/records.py`). A batch opened before
  this version has none; its CRs work as today, with no `--lease`.
- A lease is **live** while `ended` is null and (`expires` is in the future, or a long gate of the
  unit runs: its `.long-gate*.run` record names the CR and its process is alive). Else it is
  **expired** (not ended) or **ended**.

### D.2 Commands

- `take <cr|stack> --epoch <n>`: refuses a unit whose lease is live: exit 3, `<cr> is held: lease
  <n> live until HH:MM:SS; take it again once it expires, or with --reclaim on the user's word`.
  `--reclaim` (new flag) takes it anyway and logs `reclaim` with the old lease's number. The
  existing rules stay (a `--note` for a working, ready or blocked CR; `agents set <cr> -` first
  while an agent is recorded). An expired lease counts as the agent's end for that clearance (the
  Foreman's card). On success, the output's first line gains `, lease <n> until HH:MM:SS`, and the
  Driver's facts (`driver_prompt.py`) carry the line `lease: <n> (pass --lease <n> on round, ship,
  gate, note, phase, handback; renew within 3 min: lease <cr> renew --lease <n>)`.
- `--lease <n>` (new option) on `round`, `ship`, `handback` (required when the unit has a lease)
  and on `gate`, `note`, `phase` (optional). A valid one renews the lease (`renewed`, `expires`).
  - missing on a required command: exit 2, `<command> <cr> needs --lease <n> (the number take
    printed)`; nothing recorded.
  - a number that is not the unit's current one, or the current one ended: exit 3, `claim lost:
    <cr> was taken again (lease <m>) at HH:MM; stop now: nothing recorded`; nothing recorded.
  - the current one, expired and not taken again: accepted and renewed (the Driver was only
    late); the log records `lease-late` with the minutes.
  - a command run by the steering session (`--epoch`) needs no lease.
- `handback <cr> ready|blocked --lease <n>` ends the lease (`ended`).
- `lease <cr|stack>` (new, `declare/driver.py`): `lease <n> of <cr>: live until HH:MM:SS (renewed
  HH:MM:SS)`, `lease <n> of <cr>: expired at HH:MM (<k> min ago)`, `lease <n> of <cr>: ended at
  HH:MM`, or `<cr>: no lease`. `lease <cr> renew --lease <n>`: renews, prints the first form; a
  stale number: the `claim lost` refusal.
- `status`: a working CR whose lease expired gets `, lease expired HH:MM (<k> min ago)` on its
  line. `handoff` prints the lease line.

### D.3 The stack's lease

`take stack` starts `stack_lease`; the stack driver passes `--lease <n>` on its commands that
name `stack` (`forge-stack`, `stack`, `handback stack`), with the same rules.

### D.4 `close` on Copilot

`rails.running` (`rails.py`) on a Copilot batch no longer reads the session files' age:
`COPILOT_QUIET_SECONDS` and the `idle_seconds` call go. Instead:

- each held agent of a CR or of the stack is a cause while that unit's lease is live: `<agent>
  (<cr>) holds lease <n> until HH:MM:SS`; an expired or ended lease is no cause;
- a held agent of a unit with no lease (a batch opened before this version): `<agent> (<cr>): not
  measured (no lease)`, a cause, as `not measured` is today;
- the current Foreman is a cause while its last heartbeat (`status --refresh --epoch`) is younger
  than `TTL`: `Foreman n°<k>: heartbeat <m> min ago (under 10 min)`.

On Claude Code, `close` keeps reading the transcripts' ends (exact); the lease is shown, never a
cause (open question 6). The cards' texts on the 5-minute heuristic (`concepts.md`, the "Batch"
word; `chief-of-staff.md`, "Closing" and the refusal table's row D) say the lease instead.

### D.5 Cards

- `driver.md`: the lease line of its facts; `--lease <n>` on the named commands; while it waits
  (CI, a review, a worker) longer than 3 minutes, `lease <cr> renew --lease <n>` at least every 3
  minutes; `claim lost` means stop at once, record nothing more, tell the Foreman.
- `foreman.md`: `take` refused for a live lease: wait for its expiry, or `--reclaim` on the user's
  word through the Chief of Staff; an expired lease counts as the Driver's end for `agents set <cr>
  -`; the `lease expired` mark of `status` is a Driver presumed gone: check its end by the host's
  means, then take the CR again with `--note "resume: lease expired"`.
- `chief-of-staff.md` (direct mode): the same as the Foreman's.

### D.6 Messages

- `lease-expired@1` (the hub, once per batch, unit and lease number, for running batches only):
  `lease expired: <cr> lease <n> at HH:MM; for the Chief of Staff: tell the steering session (the
  Foreman sees it in status), record nothing`.

### D.7 Evidence

- `tests/test_leases.py`, parametrized, on a prepared batch (the clock frozen through
  `core/clock.py`'s seam): `take` starts lease 1; a second `take` with the lease live is refused
  (exit 3, the text), with `--reclaim` it starts lease 2 and logs `reclaim`; `round`, `ship`,
  `handback` without `--lease` exit 2; with lease 1 after lease 2 started, exit 3 `claim lost` and
  `batch.json` unchanged; an expired current lease is accepted and logs `lease-late`; `handback`
  ends it; `lease <cr>` prints each of its four forms; a live long gate keeps an expired lease live;
  a batch with no lease needs no `--lease`.
- `tests/test_rail_refusals.py`: the Copilot `close` causes of D.4 (a live lease, an expired one,
  no lease, the Foreman's heartbeat) replace the session-file cases.
- `tests/test_forge_hub.py`: one `lease-expired@1` line per expired lease of a running batch,
  never twice.
- Scenario: in unit `parallel`, the scripted Drivers pass `--lease`; one case runs a stale lease
  (`claim lost`); in unit `direct` (or the unit the Driver judges closest), a Copilot-host batch's
  `close` refused while a lease is live and passing once it expired (with the shortened TTL seam
  `CHANTIER_LEASE_TEST_TTL`, read only by `core/leases.py`).

---

## Part E. Typed waits (gates)

### E.1 What a wait is

A blocked CR records what it waits for, typed by the fact, never by the forge or the host:

| Type | Waits for | `ref` |
| --- | --- | --- |
| `answer` | a person's answer (the user, through the Chief of Staff) | the question, one line |
| `approval` | the review request's approval (a GitHub PR's review decision `APPROVED`; a GitLab MR's approvals met) | the PR or MR link |
| `pipeline` | a green pipeline on a head (every required check passed) | the head's sha (and the PR or MR link) |

Recorded in `batch.json` (local): `CrEntry.waits`, a list of `{id, type, ref, since, note,
cleared_at, cleared_by}`; `id` is `w1`, `w2`, ... per CR.

### E.2 Commands

- `handback <cr> blocked --lease <n> --wait <type>[=<ref>] <reason>` (new repeatable option): the
  hand-back adds each wait. `--wait` on a `ready` hand-back: exit 2.
- `wait <cr> add <type> [--ref <ref>] --note "<text>"` (new command, `declare/driver.py`), by the
  Driver (`--lease`) or the steering session (`--epoch`): records a wait without ending the
  Driver. An `approval` or `pipeline` wait with no `--ref`: the CR's recorded PR, and for
  `pipeline` its recorded head; none recorded: exit 2.
- `wait <cr> clear <id> --epoch <n>`: the steering session clears it (on the user's answer, or
  after a `wait-cleared@1` line); prints `<cr> <id> cleared`.
- `wait [<cr>]`: `<cr> waits for: w1 answer since HH:MM: "<ref>"; w2 pipeline on <sha7> since
  HH:MM` or `<cr> waits for nothing`; with no CR, one line per CR of the batch with an open wait.
- `status`: a CR line with open waits gains `, waits: <types>`; `handoff` prints the `wait` line.
- The board's CR card shows the open waits (`board/state.py`, a `waits` field). `STATUS.json`'s
  fields that the CR board pane shows do not change (no pane change, so no screenshot owed).
- A wait changes no rule: `take`, `close` and the slots read the CR's status as today.

### E.3 The hub's part

For each running batch, each open `approval` or `pipeline` wait of a CR with a PR: the hub's cycle
(`hub/cycle.py`, through `board/forge_read.py`) reads, within its existing query budget (one query
per project and cycle), the review decision (GitHub GraphQL `reviewDecision`; GitLab `approved`
of the MR's approvals) and the checks of the `ref` head. When the forge shows the wait met, it
appends `wait-cleared@1` once per batch, CR and wait id. It records nothing in the batch.

### E.4 Cards

`driver.md`: block with `--wait` when the block is a wait of one of the three types. `foreman.md`
and `chief-of-staff.md`: clear a wait on the user's answer or on a `wait-cleared@1` line, then take
the CR back as today (`take --note`). `concepts.md`: the word "wait".

### E.5 Messages

- `wait-cleared@1`: `forge saw <wait_type> met: <cr> <wait> (<ref, sha cut to 7>); for the
  steering session: wait <cr> clear <wait> --epoch <n>, then take it back`.
- `status` shows the `wait-cleared@1` lines of the batch while the wait is open, as it shows the
  `merged` lines.

### E.6 Evidence

- `tests/test_waits.py`, parametrized over the three types: `handback blocked --wait` records them;
  `wait add` with and without `--ref`; `wait clear` by the steering session; a clear without
  `--epoch` exits 2; `wait` prints both forms; a `--wait` on `ready` exits 2.
- `tests/test_forge_hub.py`, with the fake forge world (`forge_world.py`) on GitHub and on GitLab:
  an approval and a green pipeline each give one `wait-cleared@1` line, never twice; a red
  pipeline gives none.
- Scenario, unit `gates` (GitHub) and unit `gitlab`: a Driver blocks with `--wait pipeline`, the
  fake forge turns green, the journal holds `wait-cleared@1`, the scripted Foreman clears and takes
  back.

---

## Part F. `access`: why a session may or may not write, claim or push

### F.1 The command

`chantier access [write|claim|push] [<cr>] [--lease <n>] [--epoch <n>]` (new, `declare/access.py`,
handler `commands/access.py`), read-only, exit 0 whatever the answers. The CLI knows no role: the
answers name the seat, the epoch, the lease and the writer, never a role. With no action, all three
(`claim` and `push` only when a CR is named). First line, the session:

- `session <key>: holds the seat of <project>` / `session <key>: the seat is <other key> (<link>)`
  / `session <key>: no seat recorded` (the key from `hub/autostart.py`'s `session_key`).

`write`:

- in-project: `write: allowed: in-project planning folder, under the lifecycle lock; chantier
  commits nothing`
- external, writer running: `write: allowed: the surface's writer runs (pid <p>, <state>); it
  commits and pushes within 5 min`, and when not `synced`: `; not pushed yet: <reason>`
- external, no writer: `write: refused: the surface's writer is not running; start the surface
  server ($CHANTIER board --seat <session id>)`

`claim <cr>` (the checks of `take`, run read-only, in `take`'s order):

- `claim: allowed: <cr> is <status>; <k> of <s> slots held; dependencies ready; budget left <x>`
- `claim: refused: <the refusal take would print>` (a live lease, no slot, a dependency, the
  budget, an agent recorded, the CR's status), and with no `--epoch` or a stale one: `claim: needs
  the steering session's --epoch (Foreman n°<k>)`.

`push <cr>`:

- the CR's branch: `push: allowed: lease <n> of <cr> is live; push <branch> without force; a
  rewrite uses --force-with-lease (driver.md)` / `push: refused: claim lost (lease <m> is current)`
  / `push: refused: no --lease given (lease <n> is current)` / `push: refused: <cr> is <status>`.
- the surface, external mode: `push surface: only the writer pushes the surface; never by hand`.

### F.2 Cards and evidence

- `concepts.md` names the command; `driver.md`, `griller.md`, `foreman.md`: on a refusal they do
  not understand, run `access` before asking.
- `tests/test_access.py`, parametrized: each line above from a prepared state (in-project;
  external with and without a writer entry; a CR with a live, expired and stale lease; no slot; a
  dependency not ready), and `access` writing nothing (the tree fingerprint unchanged).

---

## Part G. Outside contributions

A PR or MR merged on the project without chantier ends, on the user's word, as a report in the
archives. No CLI tool (no measured cost yet):

- `chief-of-staff.md`: on "archive <link>" (a PR or MR merged outside chantier), read it with the
  forge's CLI (`gh pr view`, `glab mr view`: title, link, author, merged at, the files changed and
  its description), and write `5-archives/<YYMMDD-HHMM>-outside-<forge number>-<slug>/` with
  `intake/request.md` (the description, as received) and `delivery.md` (the PR, its author, the
  merge time, what changed in a few lines, `Archive in the PR: no`), then `summary set` on it. The
  writer publishes it like any write; with no writer, nothing is written.
- `lifecycle/layout_check.py` (`validate`) accepts an archive named
  `<YYMMDD-HHMM>-outside-<number>-<slug>`.
- `docs/planning-modes.md`, "Outside contributors": the archive path.
- Evidence: `tests/test_validate.py` gains an outside archive (valid) and a malformed name (an
  error).

---

## 5. Host and default matrix

The CR depends on the host (how `close` tells a held agent runs; whether a watcher's end wakes the
session) and on no configured value (every time is a constant, with a test seam).

| Host | Cell | Expected |
| --- | --- | --- |
| Claude Code | `close` with a held Driver whose lease is live and whose transcript ended | passes: the transcript decides; the lease is shown |
| Claude Code | a Driver's `round` with a stale lease | exit 3, `claim lost` |
| Claude Code | a writer's `sync-conflict@1` with the watcher running | the watcher ends and wakes the Chief of Staff |
| Copilot | `close` with a held Driver whose lease is live | refused: `<agent> (<cr>) holds lease <n> until ...` |
| Copilot | `close` with every lease expired or ended, the Foreman's heartbeat older than 10 min | passes |
| Copilot | `close` on a batch opened before this version | refused: `not measured (no lease)` |
| Copilot | a writer's journal line | reaches the Chief of Staff at the user's next message (the pull path); the watcher's wake is unproved there, as today |
| both | no writer, `file` in external mode | exit 2, C.8's text |
| both | in-project mode, any command | no writer, no refusal, no `writer:` line |

## 6. Evidence, all parts together

- `just check` (the project's rule), `just test` within its time budget (AGENTS.md: at most 30 s
  above 18.5 s): the writer's tests use one bare origin per test module and the `poll(now)` seam;
  they are few and parametrized.
- `just eval-dry-run` (the change is under the CLI's `src/`).
- `just scenario`, green on the pipeline's `just scenario (ubuntu-latest)` job; the top CR of the
  batch also passes it locally on Windows (`chantier gate`), as AGENTS.md says.
- Every check that guards a shipped file reads it from the repository at the head under test:
  `hub/schemas.json` (A.4), the cards' texts named in C.11, D.5, E.4 (the existing
  `test_plugin_files.py` and `test_startup_manifest.py` structure tests), `board/web/` and its
  `DESIGN.md` (`test_board_design.py`). The prepared texts named above (a journal with unknown
  lines, a `writer` entry per state) are only for cases the shipped files cannot hold.
- No CI job is added or changed.

## 7. Self-containment notes for the Driver

- Existing seams to follow: `hub/loop.py` (a server thread with `poll(now)`), `hub/lock.py` (an
  OS lock never waited on), `hub/state.py` (`server.json` entries), `hub/times.py` (the test-times
  seam), `hub/journal.py` (`append`, the one writer path), `core/git.py` (`git`), `rails.py`
  (`running`, `check_take`), `commands/driver.py` (`take`, `round`, `handback`),
  `commands/batch_status.py` (`_autosync_lines` replaced), `commands/preflight.py` (P13),
  `board/routes.py` (the routes table).
- AGENTS.md's portability: every git call through `core/git.py` (UTF-8, no shell); paths with
  forward slashes in messages; Windows file locks (a rebase touching a file open in another
  process fails: `git-error`, never a retry loop).
- The writer never stages an ignored path, never runs `git add -A` without its pathspec, never
  forces a push, never skips hooks, never deletes a branch or a file.

## 8. Rollout

- The release notes say: the surface server now commits, rebases and pushes the surface; stop the
  surface's autosync tool and remove its rules and the "commit by hand" rule from the surface's
  `AGENTS.md`; with no surface server running, chantier writes nothing to the surface.
- Mixed versions: a chantier of an earlier version reading version 2 journal lines counts them
  and wakes no one; a board of another version is already refused (the server's election).

## 9. Out of scope

- Beads as the store, a bridge, or an export (`bd ready --json`): only on a measured need.
- Vercel Board, hosted or local, for messages or plans; Board's `tasks run -- <cmd>`, conditional
  writes, schedules and per-principal grants (only `access`, an explanation, is taken).
- Hash IDs; Dolt; OKF; a database or a hidden ref as the store.
- The dedicated-branch backend (declared in the conformance test, not built).
- Authentication beyond the board's key, and a team-wide guarantor role on several machines.
- Typed versions for the batch's own `events.jsonl` (the record's log).
- Waits on CRs outside a batch (in the backlog).
- Secret scanning of what the writer commits (the autosync tool ran Gitleaks; chantier ships no
  scanner).

## 10. Open questions for the user

1. **Parts.** Split this CR into its seven parts (A to G, §2), each a CR of its own in that order,
   or keep one CR delivered as a stack of seven PRs?
2. **Who writes the files.** Sessions keep writing the surface's working tree themselves (under
   the CLI's locks) and only the writer commits and pushes (this specification); or every write
   goes through the server, the CLI becoming a thin client (the intent's point 2, and the 11-10
   "the other sessions talk to the Chief of Staff's session")?
3. **Dedicated branch.** Build the dedicated-branch backend (the plan on a branch of the project's
   repository, for projects with no separate surface) in a later CR, or never?
4. **A board started by hand.** Does it run the writer too (this specification: yes, the user
   guarantees it), or only a board a Chief of Staff starts?
5. **Lease length.** 10 minutes, renewed every 3 (this specification, to spare a Driver waiting
   on CI too many calls), or Board's 5 minutes, renewed every 100 s? Configurable in
   `chantier.yaml` or a constant?
6. **Leases on Claude Code.** `close` keeps reading the transcripts there (exact) and shows the
   lease; should a live lease also be a cause on Claude Code?
7. **QA orders.** A QA driver's agent (an order's `agents set`) gets no lease here, so on Copilot
   it stays `not measured`. Give QA orders a lease too, in this CR?
8. **Waits.** The intent named "a merged review request" as a wait; the 11-20 answer names an
   approval. Add a fourth type, `merge` (a review request merged), or is `approval` enough? And do
   waits belong on backlog CRs too (a CR waiting for the user's answer between grills)?
9. **The surface's other files.** The writer commits only `projects/` and the root `chantier.yaml`
   (this specification); edits to the surface's `AGENTS.md`, `scripts/` or `justfile` stay
   committed by hand. Should the writer commit every path the surface does not ignore, as an
   Obsidian-like vault would?
10. **Secrets.** The autosync tool refused to push a detected secret. Is the loss acceptable, or
    should the writer refuse a commit on some rule (and which, with no new tool to install)?
11. **Pre-staged changes.** A file staged by hand for two cycles blocks the writer (`staged`).
    Block, or commit the staged files with the rest?
