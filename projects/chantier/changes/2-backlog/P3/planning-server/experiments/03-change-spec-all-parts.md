# Change Specification, all seven parts: the surface's writer, and five ideas borrowed from Vercel Board

Origin: verbal (2026-11-10, Beads study; grilled 2026-11-20). No tracker issue.

**This file is the reference for parts A, B, D, E, F and G**, each filed as an inbox item of its
own that names `planning-server`; their specifications start from the part here, with every
answer of `../02-answers.md` (up to planning-server-Q23, 2026-11-20) folded in. **Part C, the
writer, is specified in this CR's `../03-change-spec.md`**, which ranks above Part C's text here
when the two differ.

The parts were filed under these slugs: A `1-inbox/typed-journal-events`, B
`1-inbox/plan-store-interface`, D `1-inbox/driver-leases`, E `1-inbox/typed-waits` (which also
depends on `1-inbox/forge-connectors`, planning-server-Q24, 2026-11-20), F `1-inbox/explain-access`,
G `1-inbox/outside-contributions-archive`.

## 1. Goal, in the user's terms

The plan lives outside the project, in a planning surface, as Markdown and JSON that anyone can
browse on the forge (GitHub or GitLab). Putting the plan in the project "hits its limits very
fast"; the external surface is the answer, even if heavier. In it:

- **One writer.** One process commits, rebases and pushes the surface: the surface server that a
  Chief of Staff starts and guarantees (or the user, for a board started by hand). Every change
  reaches the forge within 5 minutes. The surface's own autosync tool is no longer needed. A
  conflict between two clones that did not sync is raised to the Chief of Staff, who resolves it to
  its best guess or asks the user.
- **No writer, no write.** While no surface server runs, the CLI refuses every write to the
  surface, with no fallback. A Griller alone records nothing.
- **Five ideas from Vercel Board, built in chantier, with no Board dependency:** leases on the
  work a Driver holds, typed waits (gates), typed journal events `name@N`, an "explain access"
  command, and the plan's storage behind a minimal interface checked by one conformance test.

Several machines are not weighed: two writers on two machines meet as any two git clones do, and
their conflict follows the conflict path of Part C.

## 2. The seven parts, seven CRs

The user's answer (planning-server-Q7, "7 CR séparés"): one CR per part, in this order of
dependency. Part C stays in `planning-server`; the six others are inbox items of their own.

| Part | CR | What | Needs |
| --- | --- | --- | --- |
| A. Typed events | inbox item | the journal's lines become `name@N`, a published schema never changing | none |
| B. Store interface | inbox item | the plan's published writes go through one interface, with a conformance test | none |
| C. The writer | `planning-server` | the surface server commits, rebases and pushes; writes refused with no writer; the surface's autosync support replaced | A, B |
| D. Leases | inbox item | a Driver's lease on its CR, on the stack, on a QA order; `close` on Copilot reads it until `copilot-close-end-event` lands | A |
| E. Typed waits | inbox item | a blocked CR, in a batch or in the backlog, records what it waits for; the hub signals when the forge shows it done | A |
| F. `access` | inbox item | why a session may or may not write, claim or push | C, D |
| G. Outside contributions | inbox item | a PR merged without chantier ends as a report in the archives | C |

Each part publishes its own event types in Part A's schema file (A.2): Part A the four existing
kinds, Part C the `sync-*@1` types, Part D `lease-expired@1`, Part E `wait-cleared@1`.

Pending items the parts compose with (named so they align; none is edited by these CRs):

- `2-backlog/P2/one-read-interface-over-the-planning-fol`: one module `store`, the only way the
  board, the hub and `status` read the planning folder; it waits for this work. Part B builds the
  write half of that same `store` module (B.1); that item adds the read half to it.
- `2-backlog/P3/batch-takeover`: it publishes `batch.json` as `resume.batch` in the batch's record
  (its §1), and names the record's way to the surface as "the surface's autosync or the Chief of
  Staff's own commit" (its §1) and the pull before a takeover as "the surface's autosync `sync`,
  or a plain pull" (its §3). With Part C, both become the surface's writer: the record is a
  published path the writer commits and pushes, and the writer's fetch and integrate (or `sync
  now`) bring the other machine's record. Its strip list gains Part D's leases (D.1); waits are
  kept (E.1). Whichever lands second carries the alignment.
- `2-backlog/P2/copilot-close-end-event`: `close` reads a Copilot agent's end from
  `events.jsonl`. Until it lands, Part D's leases are what `close` reads on Copilot; once it lands,
  the lease is only shown there, as on Claude Code (D.4, planning-server-Q14).
- `4-batch/1-pending/398-retro-batch-28-drivers-end-before-closin`: the 45,000-byte cap on a CR
  Driver's common path (D.5).

## 3. Decisions carried from `02-answers.md`

| Decision (date) | Where it lands |
| --- | --- |
| "No setup" is for the target project; the surface may take a YAML/JSON configuration; coding rules stay in the project's `AGENTS.md` (11-10) | §C.1: the writer needs nothing but the surface's clone with an upstream; no new key in the project's repository; §C.12 the surface's setup |
| Minor outside contributions without chantier; ideally a report in the archives (11-10) | Part G |
| Upstream churn rules out Beads as the store; installing a binary is not the problem (11-10) | §9 out of scope |
| Hash IDs rejected: "ce serait pas trié et j'ai déjà un slug" (11-10) | §9; leases and waits use the CR's id and small numbers |
| Heartbeat/reclaim "ça vaudrait le coup" (11-10); leases replace the "session file written in the last 5 minutes" heuristic (11-20) | Part D |
| Gates stay generic: GitHub PR and GitLab MR; Claude Code, Codex, GitLab Duo, Copilot (11-10) | Part E: types named by the fact, never by the forge |
| The external surface is the most important point (11-10) | Part C |
| The only writer is the Chief of Staff, who guarantees the server (11-10) | §C.2 |
| One Chief of Staff per project, several projects in one surface repository (11-10) | §C.3 |
| Everything in Markdown, browsable on the forge; a separate planning project is better than a dedicated branch; a hidden ref and a database are ruled out (11-10) | §C: the writer pushes the surface's default branch; Part B: the dedicated branch is a later CR of its own |
| The storage table (11-10): events as additional Markdown and JSON files; files read directly on the forge; sync within 5 minutes; conflicts raised to the Chief of Staff, best guess or ask the user; setup to be defined; Dolt set aside | §C.5, §C.7, §C.12; Dolt in §9 |
| Chantier takes the sync over; n Chiefs of Staff on n projects of one surface synchronise their pushes; about three checkouts at worst (11-10, from planning-repo) | §C.3, §C.7 |
| A running batch's state stays local to the steering machine (11-10, planning-repo answer 4) | §C.4: the writer never stages an ignored file; leases and batch waits live in `batch.json` |
| No OKF for now (11-10) | §9 |
| Messages and plan storage are two things; no Board dependency, hosted or local; chantier's journal, surface server and watchers stay the channel (11-20, Q1-Q2) | §9; Part A extends the existing journal |
| All five Board ideas go in this work (11-20, Q3) | Parts A, B, D, E, F |
| Chantier takes the sync over: the surface server is the one writer; commits, rebases and pushes within 5 minutes; raises conflicts to the Chief of Staff; the autosync tool no longer needed (11-20, Q4) | Part C |
| With no server, writes are refused until a Chief of Staff starts it again; no fallback; a Griller alone records nothing (11-20, Q5) | §C.8, §C.11 |
| One watcher-autosync at a time for the surface; several machines not weighed; specify every state and message (11-20, Q6) | §C.3 (one writer per surface and machine, by an OS lock), §C.7, every part's states and messages |
| Spec critic: yes (11-20) | run by the Chief of Staff |
| Q7: seven separate CRs, A and B first, then C, then D to G (11-20) | §2; this file for A, B, D, E, F, G; Part C in `planning-server` |
| Q8: a Driver's lease stays live while a background task recorded for the CR runs (the CI watch), as the long gate today (11-20) | §D.1 (liveness), §D.2 (`lease <unit> hold`) |
| Q9: `access`, `wait` and `lease` are built and named as exceptions in AGENTS.md by this work, citing the user's 11-20 answer ("tout") (11-20) | §D.5, §E.4, §F.2 (each part's AGENTS.md line) |
| Q10: sessions write the surface's files under the CLI's locks; only the writer commits, rebases and pushes; "the other sessions talk to the Chief of Staff's session" and "thin client" superseded (11-20) | §3 note below; §C.8 |
| Q11: never add the code's clone and worktrees under `projects/<name>/`: the writer excludes the paths `checkout.yml` names and blocks on any other nested repository (11-20) | §C.5 step 3, §C.6 `nested-repo` |
| Q12: the remote moved while files are not committed: commit everything pending first, so any conflict is a rebase conflict (11-20) | §C.5 step 6 |
| Q13: secrets: git hooks only; the writer runs the user's hooks, never `--no-verify`; a secret scan goes in a pre-commit hook if the user wants one; nothing more in chantier (11-20) | §C.5 step 4, §C.6 `git-error`, §8, §9 |
| Q14: leases serve Copilot's `close` until `copilot-close-end-event` lands; then Copilot reads the agent's end and the lease is only shown (11-20) | §D.4 |
| Q15: a board started by hand (no seat) runs the writer too; the user guarantees it (11-20) | §C.1 |
| Q16: a Driver's lease is 10 minutes, renewed every 3, a constant in the code (11-20) | §D.1 |
| Q17: the surface's other files (`AGENTS.md`, `scripts/`, `justfile`) stay committed by hand; the writer touches only `projects/` and the root `chantier.yaml` (11-20) | §C.4 words, §C.5 steps 3-4 |
| Q18: files staged by hand for two cycles: the writer blocks (`staged`) and tells the Chief of Staff to commit or unstage them (11-20) | §C.6 `staged` |
| Q19: the conformance test runs on one real storage only for now; the interface stays; the test proves it the day a second backend is built; the dedicated branch becomes a CR of its own, later (11-20) | §B.1, §B.2, §9 |
| Q20: on Claude Code a live lease is shown only; the transcripts stay the exact source for `close` (11-20) | §D.4 |
| Q21: QA orders get leases in this work: the QA driver takes and renews a lease as a CR's Driver does (11-20) | §D.3 |
| Q22: a fourth wait type, `merge` (a review request merged); a backlog CR may carry a wait too (e.g. the user's answer between two grills) (11-20) | §E.1, §E.2 |
| Q23: GitLab approvals unproved: the GitLab approval read is marked unproved; one read on a real GitLab MR (Free and Premium) before the GitLab half of `approval` ships (11-20) | §E.3, §E.6 |

Superseded, as Q10 confirms: the 11-10 table's "the other sessions talk to the Chief of Staff's
session" and the intent's "thin client, the write sent to the server". Sessions on the machine
write the surface's working tree as today, under the CLI's locks; only the writer commits,
rebases and pushes.

## 4. Words

- **Writer:** the thread of the surface server (`chantier board`) that commits, rebases and pushes
  the planning surface. It exists only in external mode.
- **Published path:** a path of the surface's working tree that git does not ignore, under
  `projects/` or the surface root's `chantier.yaml` / `chantier.yml`, and not under a path a
  project's `checkout.yml` names. A path the planning folder's `.gitignore` lists
  (`core/files.py`, `IGNORED`) is local, never published. The surface's other files (its
  `AGENTS.md`, `scripts/`, `justfile`, ...) are neither: the writer never touches them; they are
  committed by hand, like code.
- **Published write:** a CLI write that creates, changes, moves or deletes a published path.
- **Lease:** a numbered, time-limited hold of a Driver on its unit (a CR, the stack, or a QA
  order), renewed by the Driver's commands, ended by its hand-back or the order's end.
- **Wait:** what a blocked CR waits for, typed by the fact: `answer`, `approval`, `pipeline`,
  `merge`.
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
`source` is one of `hub`, `board`, `cli`, and `writer` (added by Part C). `audience` is as in
version 1.

Published types, each `@1`, and the part that publishes each:

| Type | Part | Payload | Written by | Wakes a watcher |
| --- | --- | --- | --- | --- |
| `merged@1` | A | `batch`, `cr`, `pr`, `into`, `into_cr`, `merged_at`, optional `landed_with`, `landed_at` | hub, board | yes |
| `checks-red@1` | A | `batch`, `cr`, `pr`, `head` | hub | yes |
| `config@1` | A | `key`, `old`, `new`, `batch` | board | yes |
| `board@1` | A | `action`, `items`, `text`, `wakes` | board | when `wakes` |
| `sync-conflict@1` | C | `upstream` (sha), `local` (sha), `files` (paths relative to the surface root), `projects` | writer | yes |
| `sync-blocked@1` | C | `reason` (one of C.6's reasons), `text` | writer | yes |
| `sync-late@1` | C | `since` (time of the oldest change not pushed), `paths` (count), `ahead` (commits) | writer | yes |
| `sync-resumed@1` | C | `after` (`conflict`, `blocked`, `offline`) | writer | no |
| `lease-expired@1` | D | `batch`, `cr` (a CR id, `stack`, or an order id `O-k`), `lease` (its number), `expired_at` | hub | yes |
| `wait-cleared@1` | E | `batch` (null for a backlog CR), `cr`, `wait` (its id), `wait_type` (`approval`, `pipeline` or `merge`), `ref`, `seen_at` | hub | yes |

The first four are the version 1 kinds frozen as they are today; their payloads do not change.

### A.3 Reading and writing

- `journal.append(repo, events, source)` takes events as `{"type": "name@N", "audience"?, ...}`,
  validates each payload against its model, and raises `ValueError` (a code fault) on an unknown
  type, a payload its model refuses, a wrong source or audience. It keeps its lock, its `seq` and
  its duplicate rule; `_key` dispatches on the type's name. Every writer (hub, board, CLI, and
  later the writer) still goes through this one function.
- `journal.read` gives every line an effective `type`: a version 0 or 1 line's `kind` becomes
  `<kind>@1`, its `source` from `source` or `by`, its audience `project` when it has none. A
  version 0 or 1 line is never rewritten.
- A version 2 line whose `type` is not in `PUBLISHED` (a newer chantier wrote it), or whose
  payload its model refuses, counts for `seq`, is listed with the unreadable lines by number, and
  wakes no one. A line with `v` above 2 is as today's newer line.
- `event_text` dispatches on the type's name; the texts of the four existing kinds do not change.
  The texts of the later types are in C.10, D.7 and E.5.
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
- Each later part that publishes a type adds its model and its `schemas.json` entry; the same test
  covers it.

---

## Part B. The plan's storage behind a minimal interface

### B.1 What changes

New package `skills/chantier/scripts/cli/src/chantier/store/`. It is the module `store` that the
pending P2 item `2-backlog/P2/one-read-interface-over-the-planning-fol` names: this part builds its
**write half** and the low-level reads the conformance test needs (`read_text`, `exists`,
`listdir`); that item adds the read half (records, backlog, configuration, journal) to the same
protocol and backends and moves the readers onto it. One package, one `PlanStore`, one
`Repo.store`, one conformance test that both halves extend; no second store module.

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
  - `check_publish(rels)`: raises a refusal when one of `rels` is published and the store cannot
    publish now; returns otherwise. In Part B no backend refuses; Part C gives `SurfaceStore` its
    gate (C.8).
  - Features: `publishes` (published paths reach a remote), `local-files` (ignored files kept beside
    the published ones), `refuses-without-publisher` (a published write is refused while the
    publisher is down; declared by `SurfaceStore` from Part C on).
- `folder.py`: `FolderStore(changes)`: the in-project planning folder. Features: `local-files`.
  Publishes nothing, never refuses (in-project mode is unchanged).
- `surface.py`: `SurfaceStore(repo)`: the external planning folder, the same files. Features:
  `publishes`, `local-files`. This is the "server" backend of the user's list.
- `Repo.store` (in `core/repo.py`): the store of the repository, chosen by `repo.external`.

Both backends built here keep the same files on disk: the conformance test runs on that one real
storage (planning-server-Q19). The interface stays; the test proves it as an interface the day a
second backend is built. The dedicated-branch backend (the plan on a branch of the project's
repository) is a CR of its own, later; the conformance test declares it, skipped with the reason
`dedicated-branch backend: a later CR (planning-server-Q19)`.

Every published write of the CLI goes through `repo.store`: `file`, `triage`, `abandon`,
`restore`, `init`, `open`, `take`, `handback`, `order` (each kind that moves or writes a CR's
folder: `add`, `merged`, `drop`), `cancel`, `close`, `summary set`, `summary label`, `summary
group`, `verdict` when it writes in a CR's folder, the release commands that write the archive,
and the board's backlog writes (`board/write_api.py`, through `lifecycle/backlog.py`) and its
Configuration page's save (`board/config_api.py`, `projects/<name>/chantier.yaml`). Each command
calls `check_publish` with every published path it will touch **before** it changes anything, so a
refused command leaves the folder and the batch's record as they were. Local files (`batch.json`,
`events.jsonl`, STATUS files, locks, the journals, `seat.json`) may keep `core/files.py`'s
functions directly; they are never refused. Parts D and E add their own published writes (a QA
order's lease is local; a backlog CR's `waits.json` is published) through the same store.

### B.2 Evidence

- `tests/test_store_conformance.py` (new): one test body parametrized over the backends `folder`,
  `surface` and `dedicated-branch` (skipped, B.1). A case whose feature the backend declares
  absent is skipped by feature, never failed:
  - UTF-8 round trip of a text with non-ASCII letters, no BOM written, LF kept;
  - `write_json` then `read_text` gives the same JSON;
  - `move` of a CR folder from `2-backlog/P3/` to `3-ready/` keeps every file's bytes; a move onto
    an existing folder is refused and changes nothing;
  - `lock` is exclusive: a second `lock()` from another thread waits, and times out with the
    lifecycle lock's message;
  - `published` agrees with `IGNORED` for `seat.json`, `4-batch/batch.json`, `work/gates/x.log`
    (local) and `3-ready/x/01-intent.md`, `5-archives/batches/batch-01.json` (published);
  - `refuses-without-publisher` (from Part C on): see `../03-change-spec.md`, §6
    (`test_store_conformance.py`).
- A test over the command table of B.1 on a prepared external surface: each command calls
  `check_publish` with its published paths before any change (a spy store records the call order).
  Part C turns the same table into the refusal test (`test_surface_writes.py`).

---

## Part C. The writer

Specified in full in `../03-change-spec.md` (this CR, `planning-server`). Summary, for the parts
that need it:

- The writer is a daemon thread of the surface server (`chantier board`) in external mode, for a
  board started by a Chief of Staff (`--seat`) and for one started by hand (the user guarantees
  it). One per surface and machine, by the OS lock `chantier/writer.lock` in the git folder.
- It commits the published paths only (`projects/` and the root `chantier.yaml` / `.yml`,
  excluding the paths `checkout.yml` names), within `max_wait + every` (150 s), fetches,
  integrates (committing everything pending first, then fast-forward or rebase), and pushes,
  never forced, never skipping hooks.
- States `syncing`, `synced`, `pending`, `offline`, `conflict`, `blocked` (reasons `not-a-branch`,
  `no-upstream`, `git-busy`, `nested-repo`, `staged`, `foreign-autosync`, `git-error`), and `off`
  when no live `writer` entry is in `server.json`.
- With no writer, `SurfaceStore.check_publish` refuses every published write: exit 2,
  `error: <command>: the surface's writer is not running: nothing written; for the Chief of Staff: start the surface server ($CHANTIER board --seat <session id>)`.
- A rebase conflict is aborted and raised (`sync-conflict@1`) to the Chief of Staff, who
  integrates by hand in the surface's checkout; the writer pushes once integrated.
- Commands `sync` and `sync now`; a `writer:` line in `status`, `seat`, `board`, preflight P13;
  the board's pill.

---

## Part D. Leases

### D.1 What a lease is

- A lease is started for a unit: each `take` of a CR or of the stack, and each `order qa` for its
  order `O-k` (D.3). Number `n` (1 at the first lease of the unit, then the last number plus one),
  `taken` and `expires` = now + `TTL`.
- `TTL` is 10 minutes, renewed every 3: constants in `core/leases.py` (new), never configured
  (planning-server-Q16). The test seam `CHANTIER_LEASE_TEST_TTL` is read only there.
- The lease is in `batch.json` (local, never published): `CrEntry.lease`, `BatchRecord.stack_lease`
  and `OrderRecord.lease`, each `{n, taken, renewed, expires, ended}` or null
  (`core/records.py`). A batch opened before this version has none; its units work as today, with
  no `--lease`.
- A lease means something only on the machine that runs the batch: `batch-takeover`'s published
  `resume.batch` (§2) strips each CR's `lease`, the record's `stack_lease` and each order's
  `lease`, as it strips worktree paths and session ids; a takeover restores them as null, and the
  next lease of a unit on the new machine is lease 1 (no last number is kept).
- A lease is **live** while `ended` is null and one of:
  - `expires` is in the future;
  - a long gate of the unit runs: its `.long-gate*.run` record (`RunRecord`) names the CR and its
    process is alive (`procs.py`'s `alive`);
  - a background task recorded for the unit runs (planning-server-Q8): a `.lease-hold.<unit>.<k>.run`
    record (D.2, `lease <unit> hold`) names it and its process is alive.

  Else it is **expired** (not ended) or **ended**.

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
- `lease <unit>` (new, `declare/driver.py`; `<unit>` a CR, `stack` or `O-k`): `lease <n> of
  <unit>: live until HH:MM:SS (renewed HH:MM:SS)` (with `, held by <k> background task(s)` when a
  hold runs), `lease <n> of <unit>: expired at HH:MM (<k> min ago)`, `lease <n> of <unit>: ended
  at HH:MM`, or `<unit>: no lease`.
- `lease <unit> renew --lease <n>`: renews, prints the first form; a stale number: the `claim
  lost` refusal.
- `lease <unit> hold --lease <n> -- <command> [args...]` (new, planning-server-Q8): checks the
  lease as `renew` does (the `claim lost` refusal on a stale number, nothing run), renews it, then
  runs `<command>` as its child process (no shell, as `core/git.py` runs git), writes
  `.lease-hold.<unit>.<k>.run` in the planning folder (`{unit, lease, pid, command, started}`, its
  own pid, `k` the first free number), streams the child's output, removes the record when the
  child ends, and exits with the child's exit code. It is how a Driver runs its CI watch in the
  background (`lease <cr> hold --lease <n> -- gh pr checks --watch`, `glab ci status --live`): the
  lease stays live while the watch runs, with no renewal call, as the long gate keeps it today. A
  record whose process is gone (a crash) holds nothing and is removed by the next `lease`, `take`
  or `status` that reads it. `IGNORED` (`core/files.py`) gains `.lease-hold.*.run`. It runs only
  what the Driver gives it; it is no task runner (§9).
- `status`: a working CR, the stack driver or an open QA order whose lease expired gets `, lease
  expired HH:MM (<k> min ago)` on its line. `handoff` prints the lease line.

### D.3 The stack's lease and a QA order's lease

- `take stack` starts `stack_lease`; the stack driver passes `--lease <n>` on its commands that
  name `stack` (`forge-stack`, `stack`, `handback stack`), with the same rules.
- `order qa` starts the order's lease (planning-server-Q21): `OrderRecord.lease`, lease 1 of
  `O-k`. The skeleton `order qa` prints carries the line `lease: <n> of O-k (renew within 3 min:
  lease O-k renew --lease <n>; run a long test under lease O-k hold --lease <n> -- <command>)`.
  The QA driver renews it as a CR's Driver does (it runs no `round` or `handback`, so `lease
  renew` and `lease hold` are its means). `order done` on the order ends the lease. `take` of the
  order is not a thing: a QA driver restarted by the Foreman's restart path gets a new lease from
  `agents set <O-k> <agent>` when the previous one expired or ended (`lease <n+1> of O-k`, printed
  by `agents set`); a live lease refuses that `agents set` as `take` refuses (exit 3, `--reclaim`
  on the user's word).

### D.4 `close` on Copilot and on Claude Code

`rails.running` (`rails.py`) on a Copilot batch no longer reads the session files' age:
`COPILOT_QUIET_SECONDS` and the `idle_seconds` call go. Instead (planning-server-Q14):

- each held agent of a CR, of the stack or of a QA order is a cause while that unit's lease is
  live: `<agent> (<unit>) holds lease <n> until HH:MM:SS`; an expired or ended lease is no cause;
- a held agent of a unit with no lease (a batch opened before this version): `<agent> (<unit>):
  not measured (no lease)`, a cause, as `not measured` is today;
- the current Foreman is a cause while its last heartbeat (`status --refresh --epoch`) is younger
  than `TTL`: `Foreman n°<k>: heartbeat <m> min ago (under 10 min)`.

This holds until `2-backlog/P2/copilot-close-end-event` lands. From then on Copilot's `close` reads
the agent's end from `events.jsonl`, as that item specifies, and the lease is only shown beside
it, never a cause, as on Claude Code. Whichever of the two lands second carries this: if that item
lands first, Part D ships the shown-only form on Copilot directly.

On Claude Code, `close` keeps reading the transcripts' ends, the exact source; a live lease is
shown beside them, never a cause (planning-server-Q20). The cards' texts on the 5-minute heuristic
(`concepts.md`, the "Batch" word; `chief-of-staff.md`, "Closing" and the refusal table's row D)
say the lease instead.

### D.5 Cards, docs and project rules

- `driver.md`: the lease line of its facts; `--lease <n>` on the named commands; while it waits
  (CI, a review, a worker) longer than 3 minutes, `lease <cr> renew --lease <n>` at least every 3
  minutes, or the wait run under `lease <cr> hold --lease <n> -- <command>`; `claim lost` means
  stop at once, record nothing more, tell the Foreman. `## QA driver`: the order's lease, renewed
  or held the same way.
- `foreman.md`: `take` refused for a live lease: wait for its expiry, or `--reclaim` on the user's
  word through the Chief of Staff; an expired lease counts as the Driver's end for `agents set <cr>
  -`; the `lease expired` mark of `status` is a Driver presumed gone: check its end by the host's
  means, then take the CR again with `--note "resume: lease expired"` (a QA order: the restart
  path, D.3).
- `chief-of-staff.md` (direct mode): the same as the Foreman's.
- `concepts.md`: the word "lease".

`driver.md`'s common path is capped: `4-batch/1-pending/398-retro-batch-28-drivers-end-before-closin`
(§2) limits what a CR Driver reads on its common path (the opening, the sections
`startup-manifest.json` lists under `actions["cr-driver"]`, and `## CR driver`) to 45,000 bytes,
with a test in `test_startup_manifest.py` summing them. Parts D, E and F's text fits it: on the
common path only the lease line of the facts, `--lease <n>` on the named commands, and "`claim
lost`: stop at once, record nothing more, tell the Foreman", at most 600 bytes together; the
renewal and the hold while waiting longer than 3 minutes, the `--wait` block (E.4, a blocked
hand-back is off the common path) and "run `access` on a refusal you do not understand" (F.2) go
in trigger-read level-2 sections the card's links name, not listed in the manifest.
`test_startup_manifest.py` stays green; when 398 has not landed yet, the same placement holds and
whichever lands second keeps the total within the cap.

AGENTS.md (planning-server-Q9): "The CLI's scope" names `lease` (with `take --reclaim` and `lease
hold`) as an exception to "a new CLI tool comes from measured token-costly behaviour", built on
the user's answer of 2026-11-20 ("tout": all five of Board's ideas). The hub's sentence ("it
appends to that project's `forge-journal.jsonl` ... and nothing else") adds one line per lease of
a running batch that expires (`lease-expired@1`, D.7). The write list adds the
`.lease-hold.*.run` records in the planning folder.

### D.6 Docs

`docs/` where the 5-minute heuristic or `close` on Copilot is described (the Driver checks with a
search for `5 minutes` and `COPILOT_QUIET`).

### D.7 Messages

- `lease-expired@1` (the hub, once per batch, unit and lease number, for running batches only):
  `lease expired: <unit> lease <n> at HH:MM; for the Chief of Staff: tell the steering session (the
  Foreman sees it in status), record nothing`.

### D.8 Evidence

- `tests/test_leases.py`, parametrized, on a prepared batch (the clock frozen through
  `core/clock.py`'s seam): `take` starts lease 1; a second `take` with the lease live is refused
  (exit 3, the text), with `--reclaim` it starts lease 2 and logs `reclaim`; `round`, `ship`,
  `handback` without `--lease` exit 2; with lease 1 after lease 2 started, exit 3 `claim lost` and
  `batch.json` unchanged; an expired current lease is accepted and logs `lease-late`; `handback`
  ends it; `lease <unit>` prints each of its four forms; a live long gate keeps an expired lease
  live; a live `lease hold` (a child that sleeps) keeps an expired lease live, its record is
  removed at the child's end and the exit code is the child's; a hold record with a dead pid holds
  nothing; `lease hold` with a stale number runs nothing; `order qa` starts lease 1 of `O-k`,
  `order done` ends it; a batch with no lease needs no `--lease`.
- `tests/test_rail_refusals.py`: the Copilot `close` causes of D.4 (a live lease, an expired one,
  no lease, a QA order's lease, the Foreman's heartbeat) replace the session-file cases; on Claude
  Code a live lease is no cause.
- `tests/test_forge_hub.py`: one `lease-expired@1` line per expired lease of a running batch,
  never twice.
- Scenario: in unit `parallel`, the scripted Drivers pass `--lease`; one case runs a stale lease
  (`claim lost`); one runs a CI watch under `lease hold` past the shortened TTL and is not
  expired; in unit `direct` (or the unit the Driver judges closest), a Copilot-host batch's
  `close` refused while a lease is live and passing once it expired (with `CHANTIER_LEASE_TEST_TTL`).

---

## Part E. Typed waits (gates)

### E.1 What a wait is

A blocked CR records what it waits for, typed by the fact, never by the forge or the host:

| Type | Waits for | `ref` |
| --- | --- | --- |
| `answer` | a person's answer (the user, through the Chief of Staff) | the question, one line |
| `approval` | the review request's approval (a GitHub PR's review decision `APPROVED`; a GitLab MR's approvals met, unproved: E.3) | the PR or MR link |
| `pipeline` | a green pipeline on a head (every required check passed) | the head's sha (and the PR or MR link) |
| `merge` | the review request merged (planning-server-Q22) | the PR or MR link |

A wait is `{id, type, ref, since, note, cleared_at, cleared_by}`; `id` is `w1`, `w2`, ... per CR.

Where it lives:

- **In a batch:** `CrEntry.waits` in `batch.json` (local). Unlike leases, waits are facts of the
  CR, not of the machine: `batch-takeover`'s `resume.batch` keeps them (§2).
- **In the backlog** (planning-server-Q22; e.g. the user's answer between two grills): the CR
  folder's `waits.json` (`{"schema": 1, "waits": [...]}`), a published file that moves with the
  folder, browsable on the forge, written through `repo.store` (refused with no writer in external
  mode, Part C). `open` carries the open waits into the CR's `CrEntry.waits` and removes the file
  (in the same published write as the folder's move); a cleared wait is dropped there.
  `layout_check.py` (`validate`) accepts `waits.json` in a backlog CR's folder (inbox, `2-backlog/`,
  `3-ready/`) and checks its shape.

### E.2 Commands

- `handback <cr> blocked --lease <n> --wait <type>[=<ref>] <reason>` (new repeatable option): the
  hand-back adds each wait. `--wait` on a `ready` hand-back: exit 2.
- `wait <cr> add <type> [--ref <ref>] --note "<text>"` (new command, `declare/driver.py`):
  - in a batch, by the Driver (`--lease`) or the steering session (`--epoch`): records a wait
    without ending the Driver. An `approval`, `pipeline` or `merge` wait with no `--ref`: the CR's
    recorded PR, and for `pipeline` its recorded head; none recorded: exit 2;
  - on a backlog CR (named by its folder, as `summary` takes it), with no `--epoch` or `--lease`:
    any session (the Chief of Staff, a Griller); `--ref` is required for `approval`, `pipeline`
    and `merge` (a backlog CR has no recorded PR).
- `wait <cr> clear <id>`: in a batch with `--epoch <n>` (the steering session; a clear without it
  exits 2); on a backlog CR with no `--epoch`. Prints `<cr> <id> cleared`.
- `wait [<cr>]`: `<cr> waits for: w1 answer since HH:MM: "<ref>"; w2 pipeline on <sha7> since
  HH:MM` or `<cr> waits for nothing`; with no CR, one line per CR of the batch with an open wait,
  then one per backlog CR with an open wait.
- `status`: a CR line with open waits gains `, waits: <types>`; `handoff` prints the `wait` line.
  The backlog summary (`summary` listings) marks a backlog CR with an open wait `waits: <types>`.
- The board's CR card shows the open waits (`board/state.py`, a `waits` field, from `batch.json` or
  `waits.json`). `STATUS.json`'s fields that the CR board pane shows do not change (no pane
  change, so no screenshot owed).
- A wait changes no rule: `take`, `close`, `open` and the slots read the CR's status as today.

### E.3 The hub's part

For each running batch, each open `approval`, `pipeline` or `merge` wait of a CR with a PR: the
hub's cycle (`hub/cycle.py`, through `board/forge_read.py`) reads, within its existing query budget
(one query per project and cycle), the review decision (GitHub GraphQL `reviewDecision`), the
checks of the `ref` head, and the merge state it already reads for `merged@1`. When the forge shows
the wait met, it appends `wait-cleared@1` once per batch, CR and wait id. It records nothing in
the batch. Backlog CRs' waits are not read by the hub (E.7 question 1); they are cleared by hand.

GitLab approvals (planning-server-Q23): the read of a GitLab MR's approvals (`approved` of the
MR's approvals) is **unproved**. Before the GitLab half of `approval` ships, Part E's Driver runs
one read on a real GitLab MR on a Free and on a Premium project and records each answer in the
CR's evidence (the command, the output's relevant fields, the plan). Until both are recorded, the
hub reads no approval on GitLab: an `approval` wait on a GitLab project is recorded, shown with
`(GitLab approval: cleared by hand until proved)`, and cleared by hand; `pipeline` and `merge`
waits are read on GitLab as on GitHub (their reads are those the hub already makes).

### E.4 Cards and project rules

`driver.md`: block with `--wait` when the block is a wait of one of the four types, in a
trigger-read section off the common path (D.5's cap). `foreman.md` and `chief-of-staff.md`: clear a
wait on the user's answer or on a `wait-cleared@1` line, then take the CR back as today (`take
--note`). `chief-of-staff.md` and `griller.md`: a backlog CR left waiting for the user's answer
between two grills gets `wait <cr> add answer --ref "<the question>"`, cleared when the answer is
recorded. `concepts.md`: the word "wait".

AGENTS.md (planning-server-Q9): "The CLI's scope" names `wait` as an exception to "a new CLI tool
comes from measured token-costly behaviour", built on the user's answer of 2026-11-20 ("tout").
The hub's sentence adds one line per wait of a running batch the forge shows met
(`wait-cleared@1`), and its forge read adds, within the same query budget, the review decision and
the checks of the open waits' refs. The write list: a backlog CR's `waits.json` is a published file
of the planning folder (already covered by "chantier writes only in the planning folder").

### E.5 Messages

- `wait-cleared@1`: `forge saw <wait_type> met: <cr> <wait> (<ref, sha cut to 7>); for the
  steering session: wait <cr> clear <wait> --epoch <n>, then take it back`.
- `status` shows the `wait-cleared@1` lines of the batch while the wait is open, as it shows the
  `merged` lines.

### E.6 Evidence

- `tests/test_waits.py`, parametrized over the four types: `handback blocked --wait` records them;
  `wait add` with and without `--ref`; `wait clear` by the steering session; a clear without
  `--epoch` in a batch exits 2; `wait` prints both forms; a `--wait` on `ready` exits 2; on a
  backlog CR, `wait add answer` writes `waits.json`, `wait clear` clears it, `open` carries the
  open wait into `batch.json` and removes the file; in external mode with no writer, the backlog
  `wait add` is refused (C.8) and writes nothing.
- `tests/test_validate.py`: a valid `waits.json` and a malformed one in a backlog CR.
- `tests/test_forge_hub.py`, with the fake forge world (`forge_world.py`): on GitHub an approval, a
  green pipeline and a merge each give one `wait-cleared@1` line, never twice; a red pipeline gives
  none; on GitLab a green pipeline and a merge each give one line, an approval gives none (unproved).
- The GitLab approval proof (E.3): the two real reads, recorded in Part E's CR, before the GitLab
  approval read is enabled; no fake forge stands for it.
- Scenario, unit `gates` (GitHub) and unit `gitlab`: a Driver blocks with `--wait pipeline`, the
  fake forge turns green, the journal holds `wait-cleared@1`, the scripted Foreman clears and takes
  back.

### E.7 Open for Part E's CR

1. Should the hub also read the forge for a backlog CR's `approval`, `pipeline` and `merge` waits
   (a larger query budget than AGENTS.md's "one query per project of the surface whose running
   batch has a PR ..."), or do backlog waits stay cleared by hand (this text)?

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

### F.2 Cards, project rules and evidence

- `concepts.md` names the command; `driver.md` (off the common path, D.5), `griller.md`,
  `foreman.md`: on a refusal they do not understand, run `access` before asking.
- AGENTS.md (planning-server-Q9): "The CLI's scope" names `access` as an exception to "a new CLI
  tool comes from measured token-costly behaviour", built on the user's answer of 2026-11-20
  ("tout").
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

The work depends on the host (how `close` tells a held agent runs; whether a watcher's end wakes
the session) and on no configured value (every time is a constant, with a test seam).

| Part | Host | Cell | Expected |
| --- | --- | --- | --- |
| D | Claude Code | `close` with a held Driver whose lease is live and whose transcript ended | passes: the transcript decides; the lease is shown |
| D | Claude Code | a Driver's `round` with a stale lease | exit 3, `claim lost` |
| D | Copilot, before `copilot-close-end-event` | `close` with a held Driver (or QA driver) whose lease is live | refused: `<agent> (<unit>) holds lease <n> until ...` |
| D | Copilot, before `copilot-close-end-event` | `close` with every lease expired or ended, the Foreman's heartbeat older than 10 min | passes |
| D | Copilot, before `copilot-close-end-event` | `close` on a batch opened before this version | refused: `not measured (no lease)` |
| D | Copilot, after `copilot-close-end-event` | `close` with a live lease and the agent's end in `events.jsonl` | passes: the end decides; the lease is shown |
| D | both | a CI watch run under `lease hold` past the TTL | the lease stays live |
| C | Claude Code | a writer's `sync-conflict@1` with the watcher running | the watcher ends and wakes the Chief of Staff |
| C | Copilot | a writer's journal line | reaches the Chief of Staff at the user's next message (the pull path); the watcher's wake is unproved there, as today |
| C | both | no writer, `file` in external mode | exit 2, C.8's text |
| C | both | in-project mode, any command | no writer, no refusal, no `writer:` line |
| E | GitHub | an `approval` wait, the PR approved | one `wait-cleared@1` |
| E | GitLab | an `approval` wait, before the proof | no line; cleared by hand; shown as unproved |

## 6. Evidence, every part

- `just check` (the project's rule), `just test` within its time budget (AGENTS.md: at most 30 s
  above 18.5 s): tests are few and parametrized; the writer's use one bare origin per test module
  and the `poll(now)` seam.
- `just eval-dry-run` (each part changes the CLI's `src/`, Part G's `layout_check.py` included).
- `just scenario`, green on the pipeline's `just scenario (ubuntu-latest)` job; the top CR of the
  batch also passes it locally on Windows (`chantier gate`), as AGENTS.md says.
- Every check that guards a shipped file reads it from the repository at the head under test:
  `hub/schemas.json` (A.4), the cards' texts named in C.11, D.5, E.4, F.2 (the existing
  `test_plugin_files.py` and `test_startup_manifest.py` structure tests), `board/web/` and its
  `DESIGN.md` (`test_board_design.py`). The prepared texts named above (a journal with unknown
  lines, a `writer` entry per state) are only for cases the shipped files cannot hold.
- No CI job is added or changed.

## 7. Self-containment notes for the Drivers

- Existing seams to follow: `hub/loop.py` (a server thread with `poll(now)`), `hub/lock.py` (an
  OS lock never waited on), `hub/state.py` (`server.json` entries), `hub/times.py` (the test-times
  seam), `hub/journal.py` (`append`, the one writer path), `core/git.py` (`git`), `procs.py`
  (`alive`, `alive_since`), `rails.py` (`running`, `check_take`), `commands/driver.py` (`take`,
  `round`, `handback`), `commands/orders.py` (`order qa`), `commands/gate_run.py` (a run record
  beside a child process), `commands/batch_status.py`, `commands/preflight.py` (P13),
  `board/routes.py` (the routes table).
- AGENTS.md's portability: every git call through `core/git.py` (UTF-8, no shell); every child
  process with no shell; paths with forward slashes in messages; Windows file locks (a rebase
  touching a file open in another process fails: `git-error`, never a retry loop).

## 8. Rollout

- The release notes of Part C say: the surface server now commits, rebases and pushes the
  surface; stop the surface's autosync tool and remove its rules and the "commit by hand" rule
  from the surface's `AGENTS.md`; with no surface server running, chantier writes nothing to the
  surface; the autosync tool's secret scan goes with it: put a secret scan in the surface's
  pre-commit hook if wanted, the writer runs the user's hooks.
- Mixed versions: a chantier of an earlier version reading version 2 journal lines counts them
  and wakes no one; a board of another version is already refused (the server's election).

## 9. Out of scope

- Beads as the store, a bridge, or an export (`bd ready --json`): only on a measured need.
- Vercel Board, hosted or local, for messages or plans; Board's `tasks run -- <cmd>` as a task
  runner (Part D's `lease hold` runs one command only to keep a lease live), conditional writes,
  schedules and per-principal grants (only `access`, an explanation, is taken).
- Hash IDs; Dolt; OKF; a database or a hidden ref as the store.
- The dedicated-branch backend: a CR of its own, later (planning-server-Q19).
- Authentication beyond the board's key, and a team-wide guarantor role on several machines.
- Typed versions for the batch's own `events.jsonl` (the record's log).
- A secret scanner in chantier: the user's pre-commit hook does it, if wanted
  (planning-server-Q13).
- The writer committing the surface's other files (`AGENTS.md`, `scripts/`, `justfile`): committed
  by hand (planning-server-Q17).

## 10. Open questions

Every question of the earlier draft and of the spec critic is answered in `../02-answers.md`
(planning-server-Q7 to Q23). What remains, for the part's own CR:

1. Part E: E.7 question 1 (does the hub read the forge for backlog CRs' waits?).
