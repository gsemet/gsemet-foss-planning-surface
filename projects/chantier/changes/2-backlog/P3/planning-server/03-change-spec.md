# Change Specification: the surface's writer (Part C of seven)

Origin: verbal (2026-11-10, Beads study; grilled 2026-11-20). No tracker issue.

This CR is Part C, the writer, of the seven-part work the user split into seven CRs
(planning-server-Q7, 2026-11-20). The whole specification, every answer folded, is
`experiments/03-change-spec-all-parts.md`: the reference for parts A, B, D, E, F and G, filed as
inbox items of their own. Where the two differ on Part C, this file ranks.

## 1. Goal, in the user's terms

The plan lives outside the project, in a planning surface, as Markdown and JSON that anyone can
browse on the forge (GitHub or GitLab). Putting the plan in the project "hits its limits very
fast"; the external surface is the answer, even if heavier. This CR gives it:

- **One writer.** One process commits, rebases and pushes the surface: the surface server that a
  Chief of Staff starts and guarantees, or that the user starts by hand and guarantees. Every
  change reaches the forge within 5 minutes. The surface's own autosync tool is no longer needed.
  A conflict between two clones that did not sync is raised to the Chief of Staff, who resolves it
  to its best guess or asks the user.
- **No writer, no write.** While no surface server runs, the CLI refuses every write to the
  surface, with no fallback. A Griller alone records nothing.

Several machines are not weighed: two writers on two machines meet as any two git clones do, and
their conflict follows the conflict path below (C.7).

## 2. Dependencies and neighbours

This CR needs two of the split-off CRs merged first (their slugs are given when they are filed):

| Part | Split-off CR | What this CR needs from it |
| --- | --- | --- |
| A | **Typed events** | the journal's version 2 line, `type: "name@N"`, `hub/schemas.py`'s `PUBLISHED` and the shipped `hub/schemas.json` checked by `test_event_types.py`; `journal.append` validating each payload. This CR adds the source `writer` and publishes four types there (C.10). |
| B | **Store interface** | the package `store/` (`PlanStore`, `FolderStore`, `SurfaceStore`, `Repo.store`), every published write of the CLI and the board going through `repo.store` and calling `check_publish` with its published paths before it changes anything, and `test_store_conformance.py`. This CR gives `SurfaceStore` its gate (C.8). |

Parts D (leases), E (typed waits), F (`access`) and G (outside contributions) come after; F and G
need this CR. Nothing here depends on them.

Pending items this CR composes with (named so they align; neither is edited by this CR):

- `2-backlog/P3/batch-takeover`: it names the record's way to the surface as "the surface's
  autosync or the Chief of Staff's own commit" (its §1) and the pull before a takeover as "the
  surface's autosync `sync`, or a plain pull" (its §3). With this CR, both become the surface's
  writer: the published record is a path the writer commits and pushes, and the writer's fetch and
  integrate (or `sync now`) bring the other machine's record. Whichever lands second carries the
  alignment.
- `2-backlog/P2/one-read-interface-over-the-planning-fol`: the read half of Part B's `store`; it
  reads the `writer` entry through whatever it adds, if it lands after this CR.

## 3. Decisions carried from `02-answers.md`

| Decision (date) | Where it lands |
| --- | --- |
| "No setup" is for the target project; the surface may take a YAML/JSON configuration; coding rules stay in the project's `AGENTS.md` (11-10) | §C.1: the writer needs nothing but the surface's clone with an upstream; no new key in the project's repository; §C.12 the surface's setup |
| The external surface is the most important point (11-10) | this CR |
| The only writer is the Chief of Staff, who guarantees the server (11-10) | §C.2 |
| One Chief of Staff per project, several projects in one surface repository (11-10) | §C.3: one writer per surface and machine serves every project of the surface; seats unchanged |
| Everything in Markdown, browsable on the forge; a separate planning project is better than a dedicated branch; a hidden ref and a database are ruled out (11-10) | the writer pushes the surface's default branch, plain files |
| The storage table (11-10): events as additional Markdown and JSON files; files read directly on the forge; sync within 5 minutes; conflicts raised to the Chief of Staff, best guess or ask the user; setup to be defined; Dolt set aside | §C.5 (the 5-minute bound), §C.7 (conflicts), §C.12 (setup); Dolt in §9 |
| Chantier takes the sync over; n Chiefs of Staff on n projects of one surface synchronise their pushes; about three checkouts at worst (11-10, from planning-repo) | §C.3, §C.7 |
| A running batch's state stays local to the steering machine (11-10, planning-repo answer 4) | §C.4 words: the writer never stages an ignored file |
| Messages and plan storage are two things; no Board dependency; chantier's journal, surface server and watchers stay the channel (11-20, Q1-Q2) | §9; the writer's lines go through the existing journal |
| Chantier takes the sync over: the surface server is the one writer; commits, rebases and pushes within 5 minutes; raises conflicts to the Chief of Staff; the autosync tool no longer needed (11-20, Q4) | this CR |
| With no server, writes are refused until a Chief of Staff starts it again; no fallback; a Griller alone records nothing (11-20, Q5) | §C.8, §C.11 (cards) |
| One watcher-autosync at a time for the surface; several machines not weighed; specify every state and message (11-20, Q6) | §C.2 (one writer per surface and machine, by an OS lock), §C.7 (two machines meet as clones), every state and message of C.4 to C.10 |
| Q7: seven separate CRs; A and B first, then C (11-20) | §2; `experiments/03-change-spec-all-parts.md` |
| Q10: sessions write the surface's files under the CLI's locks; only the writer commits, rebases and pushes; "the other sessions talk to the Chief of Staff's session" and "thin client" superseded (11-20) | §C.8; the note below |
| Q11: never add the code's clone and worktrees under `projects/<name>/`: the writer excludes the paths `checkout.yml` names and blocks on any other nested repository (11-20) | §C.5 step 3, §C.6 `nested-repo` |
| Q12: the remote moved while files are not committed: commit everything pending first, so any conflict is a rebase conflict raised to the Chief of Staff (11-20) | §C.5 step 6 |
| Q13: secrets: git hooks only; the writer runs the user's hooks, never `--no-verify`; a secret scan goes in a pre-commit hook if the user wants one; nothing more in chantier (11-20) | §C.5 step 4, §C.6 `git-error`, §8, §9 |
| Q15: a board the user starts by hand (no seat) runs the writer too; the user guarantees it (11-20) | §C.1 |
| Q17: the surface's other files (`AGENTS.md`, `scripts/`, `justfile`) stay committed by hand, like code; the writer touches only the plan (`projects/` and the root `chantier.yaml`) (11-20) | §4 words, §C.5 steps 3-4 |
| Q18: files staged by hand for two cycles: the writer blocks (`staged`) and tells the Chief of Staff to commit or unstage them (11-20) | §C.6 `staged` |
| Spec critic: yes (11-20) | run by the Chief of Staff |

The other decisions (Beads, hash IDs, heartbeat and leases, gates, outside contributions, the five
Board ideas, Q8, Q9, Q14, Q16, Q19 to Q23) land in parts A, B, D, E, F and G:
`experiments/03-change-spec-all-parts.md`, §3, maps each.

Superseded, as Q10 confirms: the 11-10 table's "the other sessions talk to the Chief of Staff's
session" and the intent's "thin client, the write sent to the server". Sessions on the machine
write the surface's working tree as today, under the CLI's locks; only the writer commits,
rebases and pushes.

## 4. Words

- **Writer:** the thread of the surface server (`chantier board`) that commits, rebases and pushes
  the planning surface. It exists only in external mode.
- **Published path:** a path of the surface's working tree that git does not ignore, under
  `projects/` or the surface root's `chantier.yaml` / `chantier.yml`, and not under a path a
  project's `checkout.yml` names (C.5 step 3). A path the planning folder's `.gitignore` lists
  (`core/files.py`, `IGNORED`) is local, never published.
- **The surface's other files:** every other path of the surface (its `AGENTS.md`, `scripts/`,
  `justfile`, `.agents/`, ...). The writer never stages, commits or reverts them; they are
  committed by hand, like code (Q17).
- **Published write:** a CLI write that creates, changes, moves or deletes a published path.
- **Nested repository:** a folder under the writer's paths that holds a `.git` (folder or file),
  or a gitlink (mode 160000) in the index.

## C.1 Where it runs

- In the surface server (`chantier board`), as a daemon thread beside the hub's
  (`board/command.py` starts it as it starts `HubThread`), only when the folder served is an
  external planning surface. An in-project board starts no writer, and the in-project mode runs no
  git write, as today.
- A board started by a Chief of Staff (`board --seat <id>`) and a board started by hand (no
  `--seat`, the "With no agent" path of `docs/planning-modes.md`) both run the writer; the one who
  started it guarantees it, the user for a board started by hand (Q15).
- New package `skills/chantier/scripts/cli/src/chantier/writer/`: `loop.py` (`WriterLoop.poll(now)`
  and `WriterThread`, the shape of `hub/loop.py`), `cycle.py` (one cycle, C.5), `git_ops.py` (the
  git commands, through `core/git.py`'s `git`), `paths.py` (the writer's pathspec and the nested
  repositories, C.5 step 3), `record.py` (the `writer` entry, C.4), `times.py` (C.5's times and the
  test seam), `lines.py` (C.10's texts).
- The writer needs nothing beyond what the surface has: `git`, the surface's clone on its default
  branch with an upstream, and the network for fetch and push. Git LFS is needed only when the
  surface's `.gitattributes` names LFS files that change; git's own error then blocks the writer
  (C.6, `git-error`).

## C.2 Election and lifetime

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

## C.3 Several projects, several Chiefs of Staff, several machines

- One writer serves every project of the surface on its machine. Each Chief of Staff of a project
  of the surface guarantees it through its seat on the server; the writer stops only with the
  server.
- Commits touch `projects/<name>/` sub-trees; the writer commits all projects' changes of a cycle
  together, the commit message naming the projects (C.5).
- Two machines, each with its writer, meet as two git clones: a push refused because the other
  pushed first is integrated by rebase (C.5), and a rebase conflict goes to the Chief of Staff
  (C.7). Nothing else coordinates them.

## C.4 The record: the `writer` entry of `server.json`

Written by the writer only, through `hub/state.py`'s `modify` (its lock and its atomic replace);
the `hub/state.py` docstring names it. Fields:

- `pid`, `version`, `started` (as the other entries; an entry whose process has not been alive
  since `started` is no entry, `live_entry`).
- `state`: one of `syncing`, `synced`, `pending`, `offline`, `conflict`, `blocked`.
- `reason`: empty, or C.6's reason word; `text`: one line, at most 200 characters (git's message,
  cut, or the nested repository's path).
- `since`: when the state began.
- `pending`: the count of published paths changed and not committed; `pending_since`: the time
  the oldest of them was first seen, or null.
- `ahead`: the count of local commits not pushed; `unpushed_since`: the time of the oldest, or
  null.
- `last_commit`: `{sha, at}` or null; `last_push`: `{sha, at}` or null; `last_fetch`: time or null.
- `conflict`: while `state` is `conflict`, `{upstream, local, files}`, else null.

Readers derive one more state, `off`, when there is no live `writer` entry. `state.py` gets
`WRITER = "writer"` and `write_writer(git_dir, record)`; `remove_entry` removes it at the end.

## C.5 The cycle

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
3. **Changes.** The writer's pathspec (`writer/paths.py`): `projects`, `chantier.yaml`,
   `chantier.yml`, and one `:(exclude)<path>` per path a project's `checkout.yml` names (`repo:`,
   `worktrees:`, read by `core/repo.py`'s `read_keyed`, resolved from the project's folder) that
   falls inside the surface's working tree (Q11); a path outside it needs no exclusion. `git status
   --porcelain=v1 -z --untracked-files=all -- <pathspec>` (ignored files are never listed). An
   untracked entry that ends with `/` (git lists a nested repository as its folder and does not go
   in), or a changed gitlink, is a nested repository: C.6's `nested-repo`, checked at step 2 from
   the same listing. A fingerprint of the list and each path's size and mtime tells whether the
   changes moved since the last cycle. With changes: state `pending`, `pending` counted,
   `pending_since` kept from the first sighting.
4. **Commit**, when there are changes and (`quiet` has passed since they last moved, or
   `pending_since` is older than `max_wait`, or this is the final cycle, or a `sync now` asked, or
   step 6 needs it): under every project's lifecycle lock (`changes_lock`, taken in the projects'
   sorted order), `git add -A -- <pathspec>`, then `git commit -m <message>
   --pathspec-from-file=- --pathspec-file-nul` with the paths listed at step 3 on its standard
   input, so the commit holds only the writer's paths even when someone else staged another file
   (the `staged` rule, C.6, blocks only at the second cycle). It runs with the user's own git
   identity and hooks, never `--no-verify` (Q13): a hook that refuses (a secret scan the user put
   in `pre-commit`) is a `git-error` block whose `text` is the hook's message. The message: first
   line `chantier: <projects, comma-separated>: <n> files`, then a blank line and the paths, at
   most 20, then `and <k> more`.
5. **Fetch**, when `ahead` > 0, or `fetch_every` has passed since `last_fetch`: `git fetch <remote>
   <branch>` (the branch's upstream). A network failure (the rule below): state `offline`.
6. **Integrate**, when the upstream has commits `HEAD` lacks. Under the projects' lifecycle locks,
   first everything pending in the writer's paths is committed (step 4, whatever `quiet` says), so
   the plan holds no uncommitted change when it integrates and any conflict is a rebase conflict
   (Q12). Then, with `ahead` = 0, `git merge --ff-only <upstream>`; else `git rebase --autostash
   <upstream>`. The `--autostash` only ever holds the surface's other files edited by hand and not
   yet committed (the plan is committed); a stash git cannot reapply is a `git-error` block, git
   keeping the stash. A rebase that stops on a conflict: C.7.
7. **Push**, when `ahead` > 0: `git push <remote> HEAD:<branch>`, never forced. Refused as not a
   fast-forward: back to step 5, at most 3 times in the cycle, then the commits stay to push and
   the next cycle tries again. A network failure: state `offline`. Done: `last_push`, `ahead` 0.
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

These messages are git's English texts: every git call of the writer (`writer/git_ops.py`) runs
with `LC_ALL=C` and `LANGUAGE=C` in its environment, so a translated git (a French `LANG`, a
localized Git for Windows) still prints them. `core/git.py`'s `git` sets no locale today: it gains
an optional keyword `env: dict[str, str] | None`, merged over its own environment, and an optional
`input: bytes | None` for the commit's pathspec list, which the writer passes; the other callers do
not change. Paths stay byte-exact (`-z`, UTF-8 decoding) and the commit message is passed as
given, so the C locale changes nothing but git's messages.

## C.6 Preconditions and blocked reasons

Checked at each cycle's step 2, in this order:

| Reason | When | Way out (C.10) |
| --- | --- | --- |
| `not-a-branch` | `HEAD` is detached, or not on the surface's default branch (`origin/HEAD`, `core/git.py`'s `default_branch`) | check out the default branch |
| `no-upstream` | the branch has no upstream | set it (`git branch -u <remote>/<branch>`) |
| `git-busy` | a rebase, merge, cherry-pick or revert is in progress that is not the writer's own conflict | finish or abort it |
| `nested-repo` | a nested repository under the writer's paths that no project's `checkout.yml` names (Q11); `text` gives its path | move it out of the surface, or, when it is the project's code clone or worktrees folder, name it in the project's `checkout.yml` |
| `staged` | the index holds changes the writer did not stage, seen at two cycles in a row (Q18) | commit or unstage them by hand |
| `foreign-autosync` | the surface's autosync tool still runs: `<git dir>/ai-autosync/control.json` enabled and a live leader in `watcher.json` (read by the existing `autosync/records.py` and `autosync/reading.py`, which stay for this check only) | stop the tool (`uv run scripts/ai-autosync-git.py stop .`) |
| `git-error` | any other git command of a cycle failed (a hook, LFS, a lock file left by a crash, a stash git cannot reapply) | read `text`, repair, then `sync now` |

The `staged` rule waits one cycle so that a person staging and committing by hand within seconds
(the surface's other files, Q17) is not blocked.

## C.7 Conflicts

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

## C.8 Writes with no writer

- In external mode, `SurfaceStore` (Part B) gains the feature `refuses-without-publisher`, and its
  `check_publish` refuses a published write while there is no live `writer` entry (state `off`).
  Exit 2 (precondition). Text, one line:
  `error: <command>: the surface's writer is not running: nothing written; for the Chief of Staff: start the surface server ($CHANTIER board --seat <session id>)`
- A writer in `pending`, `offline`, `blocked` or `conflict` is running: the write is done and the
  command's output adds one line: `writer: <state>: not pushed yet (<reason or ahead count>)`.
- Local writes (Part B's list: `batch.json`, `events.jsonl`, STATUS files, locks, the journals,
  `seat.json`) are never refused: a running batch keeps its record, its rounds, its notes and its
  asks with no writer; what moves a CR's folder (`open`, `take`, `handback`, `order merged`,
  `close`) is refused.
- Writes made outside the CLI (an agent writing `02-answers.md` with its own tool) cannot be
  refused by the CLI; the cards say that a session records nothing with no writer (C.11). Such
  files left in the working tree are committed by the next writer.
- The board's backlog writes and Configuration saves with no writer: impossible, the board is the
  server and runs the writer. A writer that could not start (its lock held by another process on
  the machine) leaves the board serving with the line `board: writer not started: <reason>`, and
  the board's write routes answer 409 with C.8's text.

## C.9 Commands

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

## C.10 Messages

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

Journal types this CR publishes in Part A's `hub/schemas.py` and `hub/schemas.json`, each `@1`,
source `writer` (a new source value of the version 2 line):

| Type | Payload | Wakes a watcher |
| --- | --- | --- |
| `sync-conflict@1` | `upstream` (sha), `local` (sha), `files` (paths relative to the surface root), `projects` | yes |
| `sync-blocked@1` | `reason` (one of C.6's reasons), `text` | yes |
| `sync-late@1` | `since` (time of the oldest change not pushed), `paths` (count), `ahead` (commits) | yes |
| `sync-resumed@1` | `after` (`conflict`, `blocked`, `offline`) | no |

Journal texts (`event_text`), for `status` and a watcher's end:

- `sync-conflict@1`: `writer saw a conflict with the remote on <files>; for the Chief of Staff:
  integrate by rebase, resolve to your best guess or ask the user`
- `sync-blocked@1`: `writer blocked (<reason>): <text>; for the Chief of Staff: <way out>`
- `sync-late@1`: `writer late: <n> paths and <k> commits not pushed since HH:MM; for the Chief of
  Staff: read sync, tell the user if it lasts`
- `sync-resumed@1`: `writer resumed after <after>` (it wakes no one; it rides with the next).

`status` prints the journal's writer lines only while their episode lasts (the `writer` entry
still in that state), so a resolved conflict leaves no line.

## C.11 Cards, docs and project rules

Cards (`skills/chantier/references/`), each statement replaced where it is today:

- `concepts.md`, "Planning surface": the autosync paragraph becomes the writer: the surface server
  commits, rebases and pushes the surface's plan within 5 minutes; no session commits or pushes the
  plan by hand; the surface's other files are committed by hand; writes refused with no writer; a
  conflict goes to the Chief of Staff. "Planning folder": published versus local paths.
- `chief-of-staff.md`, "With a planning surface": the hand-commit rule for the plan and the
  autosync bullets go; in their place: never commit or push the plan by hand (the surface's other
  files stay yours to commit, by hand); on a `writer:` line or a writer's journal line, act as C.10
  says (conflict: C.7's resolution; blocked: the way out, else tell the user; offline or late: tell
  the user once per episode); `sync now` when a step must reach the forge at once. The table's
  "start autosync"/"stop autosync" row goes; "rescan" loses "without autosync, commit the planning
  folder by hand".
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
surface's autosync" becomes "The surface's writer", "With no agent" (a board started by hand runs
the writer, the user guarantees it), "Two sessions on one surface", "Setting one up" (the code's
clone and worktrees outside `projects/`, or named in `checkout.yml`)), `docs/web-board.md` (the
pill), `docs/boards.md` if it names the autosync, `README.md` where it names the surface's sync.

Project rules: `AGENTS.md` of chantier changes (the user's merge of the PR is their approval):

- The write list ("chantier writes only in the planning folder ...") adds: the surface server's
  writer commits, rebases and pushes the planning surface's published paths (`projects/` and the
  root `chantier.yaml`, never the surface's other files), and keeps `chantier/writer.lock` and
  `chantier/writer.wake` in the git folder.
- "The CLI's scope": a third named exception: the surface server's writer (C.1 to C.7).
- "The CLI has two named git exceptions": becomes three: the writer's `git add`, `commit`,
  `fetch`, `merge --ff-only`, `rebase --autostash`, `rebase --abort` and `push` (never forced,
  never `--no-verify`), in the surface's checkout only; the board's autosync join goes.
- The server's description: "the server runs no git either, but its autosync join" becomes "the
  server runs no git but its writer's".
- The watcher's sentence "reads only its project's journal (the hub's lines and the board's)"
  becomes "(the hub's lines, the board's and the writer's)".
- "the board itself records nothing and messages no agent" adds: but its writer's commits of the
  planning surface's published paths (C.5) and its journal lines (`sync-*@1`, C.10).

## C.12 The surface's setup, and what goes

- Setup: unchanged (`projects/<name>/project.md`, `checkout.yml`, `changes/`), plus the surface's
  clone on its default branch with an upstream. No new configuration key. The project's code clone
  and worktrees live outside `projects/<name>/`, or under it only at the paths its `checkout.yml`
  names (Q11).
- Removed from the CLI: `board/autosync_api.py`, `board/autosync_tool.py`, the routes `GET
  /api/autosync` and its actions, the `autosync` key of `GET /api/board` (replaced by `writer`),
  `autosync/lines.py`, `autosync/view.py`'s naming of participants and the board's join; kept:
  `autosync/site.py`, `records.py`, `reading.py` for C.6's `foreign-autosync` only.
- Removed from the scenario: `scenario/fake_autosync.py` and its cases.
- The surface's own `AGENTS.md` and `.agents/guidelines/autosync.guidelines.md` belong to the
  user's surface, not to chantier: the release notes say to remove the autosync rules and the
  "commit by hand" rule for the plan there once the release runs, and P13 warns until then.

## C.13 The board

`skills/chantier/scripts/cli/src/chantier/board/web/`: read `DESIGN.md` first and keep it true.

- The autosync pill becomes the writer's pill, by state: `synced` green, `pending` and `syncing`
  blue, `offline` grey, `conflict` and `blocked` red, `off` grey with "writer off". On a phone, a
  dot, as today.
- Its panel: the state line's facts (state, since, last push, pending paths, commits to push, the
  conflict's files or the blocked reason with its way out). One button, **Sync now**, `POST
  /api/writer/sync` (behind the key, as the other write routes), which touches `writer.wake`; no
  Start, Stop or Approve.
- `GET /api/board` carries `writer`: the `writer` entry as read, or `{"state": "off"}`.

## 5. Host and default matrix

This CR depends on the host only through how a writer's journal line reaches the Chief of Staff,
and on no configured value (every time is a constant, with a test seam).

| Host | Cell | Expected |
| --- | --- | --- |
| Claude Code | a writer's `sync-conflict@1` with the watcher running | the watcher ends and wakes the Chief of Staff |
| Copilot | a writer's journal line | reaches the Chief of Staff at the user's next message (the pull path); the watcher's wake is unproved there, as today |
| both | no writer, `file` in external mode | exit 2, C.8's text |
| both | in-project mode, any command | no writer, no refusal, no `writer:` line |

## 6. Evidence

pytest (`skills/chantier/scripts/cli/tests/`, in-process, on a temporary surface with a bare
origin, the writer's `poll(now)` driven with no sleep):

- `test_writer_cycle.py`, parametrized:
  - a new file under `projects/a/changes/1-inbox/x/` is committed after `quiet` and pushed: the
    bare origin's `main` holds it, the message's first line is `chantier: a: 1 files`;
  - a file that keeps changing is committed once `max_wait` passes;
  - an ignored file (`seat.json`, `4-batch/batch.json`, `forge-journal.jsonl`) and a surface's
    other file (`scripts/x.py`, `AGENTS.md`) are never committed; a file staged by hand outside the
    writer's paths at the first cycle stays staged and out of the writer's commit;
  - `checkout.yml` naming `repo: code` and `worktrees: code.worktrees` under `projects/a/`, both
    holding a git repository: no `nested-repo`, neither staged; a git repository at
    `projects/a/changes/1-inbox/x/clone/` not named: state `blocked`, reason `nested-repo`, its path
    in `text`, one `sync-blocked@1`, nothing committed;
  - the origin moved (a second clone pushed a change to another project): the writer rebases and
    pushes, no conflict, both changes on `main`;
  - the origin moved while a local change is pending and still moving (inside `quiet`): it is
    committed before the rebase, then rebased and pushed;
  - the same file changed on both sides, the local side not yet committed: it is committed first,
    the rebase stops, `git rebase --abort` ran (no rebase in progress, local commits intact),
    state `conflict` with the file, one `sync-conflict@1` line in that project's journal; no commit
    while in conflict; after a resolution done in the test (rebase, resolve, continue), the next
    cycle appends `sync-resumed@1` and pushes;
  - each blocked reason of C.6 (detached HEAD, no upstream, a `MERGE_HEAD`, a nested repository, a
    staged file seen twice, a fake `ai-autosync` group enabled with a live leader pid, a failing
    `pre-commit` hook whose message lands in `text`): its state, reason and one `sync-blocked@1`
    line;
  - offline (the origin's path renamed away, so the push fails with `Could not read from remote
    repository`): state `offline`, commits go on; past `late`, one `sync-late@1`; the origin back:
    pushed and `sync-resumed@1`; this case runs with the test process's `LANG=fr_FR.UTF-8` and
    `LANGUAGE=fr` (and `LC_ALL` unset), and also asserts that every git call of `git_ops.py`
    receives `LC_ALL=C` and `LANGUAGE=C` (a runner with no French locale installed prints English
    anyway, so the environment check is what proves it there);
  - the final cycle commits and pushes a pending change on stop;
  - a second `WriterLoop` on the same git folder does not get `writer.lock`;
  - a board started with no seat starts the writer as a seated one does.
- `test_writer_lines.py`: every C.10 line, from a prepared `writer` entry per state (a case the
  shipped files cannot hold), and the absence of any `writer:` line in project mode.
- `test_event_types.py` (Part A's): the four `sync-*@1` models and their entries in the shipped
  `hub/schemas.json`, read from the repository at the head under test.
- `test_store_conformance.py` (Part B's): its `refuses-without-publisher` case now runs on
  `surface`: with no live writer, `check_publish(["3-ready/x/01-intent.md"])` raises exit 2 with
  C.8's text, and `check_publish(["4-batch/batch.json"])` returns; with a live writer entry, both
  return.
- `test_surface_writes.py` (new), parametrized over Part B's command table on a prepared external
  surface with no writer: each command exits 2 with C.8's refusal, and the planning folder's tree
  fingerprint (every path and its bytes) and `batch.json` are unchanged. The same table with a live
  writer entry: each command succeeds. In-project, no command is refused.

Scenario, unit `surface-board` (`scenario/run_scenario.py`, with `CHANTIER_WRITER_TEST_TIMES`
shortened): the board started with `--seat` on the two-project surface prints its `writer:` line;
`file` in project a, then `triage`, reach the bare origin within the shortened bound; `status` and
`seat` print `writer: synced`; a commit pushed from a second clone of the surface is integrated;
a conflicting change made on both sides yields the conflict line in `status` and the journal, and
the scripted Chief of Staff's resolution (fetch, rebase, a resolved file, continue) is pushed by
the writer; the board stopped, `file` is refused with C.8's text and the folder unchanged; the
autosync cases and `fake_autosync.py` are gone. `scenario/README.md`'s Coverage list is updated
(with each case's test name, as `test_scenario_coverage.py` checks).

The project's gates:

- `just check`, and `just test` within its time budget (AGENTS.md: at most 30 s above 18.5 s): the
  writer's tests use one bare origin per test module and the `poll(now)` seam; they are few and
  parametrized.
- `just eval-dry-run` (the change is under the CLI's `src/`).
- `just scenario`, green on the pipeline's `just scenario (ubuntu-latest)` job; the top CR of the
  batch also passes it locally on Windows (`chantier gate`), as AGENTS.md says.
- Every check that guards a shipped file reads it from the repository at the head under test:
  `hub/schemas.json`, the cards' texts named in C.11 (the existing `test_plugin_files.py` and
  `test_startup_manifest.py` structure tests), `board/web/` and its `DESIGN.md`
  (`test_board_design.py`). The prepared texts named above (a `writer` entry per state) are only
  for cases the shipped files cannot hold.
- No CI job is added or changed.

## 7. Self-containment notes for the Driver

- Existing seams to follow: `hub/loop.py` (a server thread with `poll(now)`), `hub/lock.py` (an
  OS lock never waited on), `hub/state.py` (`server.json` entries), `hub/times.py` (the test-times
  seam), `hub/journal.py` (`append`, the one writer path), `core/git.py` (`git`), `core/repo.py`
  (`read_keyed` for `checkout.yml`), `lifecycle/stages.py` (`changes_lock`),
  `commands/batch_status.py` (`_autosync_lines` replaced), `commands/preflight.py` (P13),
  `board/routes.py` (the routes table), `board/command.py` (where `HubThread` starts).
- AGENTS.md's portability: every git call through `core/git.py` (UTF-8, no shell); the commit's
  paths on standard input, never on the command line (Windows' length limit); paths with forward
  slashes in messages; Windows file locks (a rebase touching a file open in another process fails:
  `git-error`, never a retry loop).
- The writer never stages an ignored path or a surface's other file, never runs `git add -A`
  without its pathspec, never commits without the path list, never forces a push, never skips
  hooks, never deletes a branch or a file.

## 8. Rollout

- The release notes say: the surface server now commits, rebases and pushes the surface's plan;
  stop the surface's autosync tool and remove its rules and the "commit by hand" rule for the plan
  from the surface's `AGENTS.md`; with no surface server running, chantier writes nothing to the
  surface; the surface's other files stay committed by hand; the autosync tool's secret scan goes
  with it: put a secret scan in the surface's pre-commit hook if wanted, the writer runs the
  user's hooks (Q13); keep the project's code clone and worktrees outside `projects/`, or name
  them in `checkout.yml` (Q11).
- Mixed versions: a chantier of an earlier version reading the writer's version 2 journal lines
  counts them and wakes no one; a board of another version is already refused (the server's
  election).

## 9. Out of scope

- Parts A, B, D, E, F and G: their own CRs (`experiments/03-change-spec-all-parts.md`).
- Beads as the store; Vercel Board, hosted or local; Dolt; a database or a hidden ref as the store.
- The dedicated-branch backend: a CR of its own, later (Q19).
- The writer committing the surface's other files (`AGENTS.md`, `scripts/`, `justfile`): committed
  by hand (Q17).
- A secret scanner in chantier: the user's pre-commit hook does it, if wanted (Q13).
- Authentication beyond the board's key, and a team-wide guarantor role on several machines.

## 10. Open questions for the user

None for this CR: every question of the earlier draft (§10, 1 to 11) and of the spec critic is
answered in `02-answers.md` (planning-server-Q7 to Q23). The one point left open belongs to Part
E's CR (`experiments/03-change-spec-all-parts.md`, E.7: does the hub read the forge for backlog
CRs' waits?).
