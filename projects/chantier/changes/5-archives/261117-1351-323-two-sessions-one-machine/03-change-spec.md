# Two chantier sessions on one machine

## Goal

The user runs two (or more) Chief of Staff sessions at once on one PC, over the same planning
surface (2026-11-17: chantier's batch-23 with a Foreman, markdown-okf-schema-studio's batch-05).
They must work well together:

- one web board for the surface, never a second one, never a stale one served in silence;
- each session commits only its own project's files in the shared surface checkout;
- each session sees the other batches running on the same surface, with how many Drivers they
  run, and picks its own slots knowing it: no cap, no message between sessions.

This CR joins the running stack batch-23 on top.

## Decisions carried (from `02-answers.md`)

| Answer | Decision | Where below |
|---|---|---|
| Q1 | One board per surface: `board` sees one already serves it, starts no second one, prints its link | A |
| Q2 | Each session stages only its own project's folder (`projects/<name>/`), never `git add -A` nor a wider folder; then `git pull --rebase --autostash` and `git push` | B |
| Q3 | No machine-wide cap; at the plan and in `status` a session sees how many Drivers the other batches run | C, D |
| Q4 | `preflight` and `status` list the other batches on the same surface (project, batch, steering mode, state), read from the folders; no message between sessions | C |
| Q5 | A board already there of another version, or silent: say it (version, PID, how to stop it), start nothing, kill nothing; the user decides | A |
| Q6 | Only the batches of the projects of the same surface; another surface or repository is not seen | C |

## What changes

All paths below are in chantier's repository; `cli/` is `skills/chantier/scripts/cli/`.

### A. One board per planning surface (Q1, Q5)

Today (`cli/src/chantier/board/command.py`, `board()`): the key is shared per surface already
(`board/key.py`, `key_path`: `<git common dir>/chantier/board.json`, the surface's git folder for
every project), and `_running()` probes only the configured address (`board/address.py`,
`settings()`, `probe()`). So a board started on another port (`--port 0`, or another project's
`board.port` in its own `chantier.yaml`) is not found and a second one starts; and a board of
another chantier version on the same address answers, `_running()` accepts it, and the new
session reuses a stale board (the "no batch, 18 inbox" board the user saw).

1. **The running board's record.** When `board` has bound its socket (after `_bind()`, before the
   start line), it writes, in the same `board.json`, next to `key` and `created`, a `running`
   object: `pid` (`os.getpid()`), `host`, `port` (the bound one, so `--port 0` records the real
   port), `version` (`__version__`), `served` (`projects.served.as_posix()`), `started` (UTC,
   as `clock.now()` writes it). On its way out (`_run()`'s `finally`), the board removes
   `running` when it still names its own PID. A board killed hard leaves it: the reader below
   treats a record whose process is gone as no record.
   - `key.load_or_create(..., new=True)` (`--new-key`) keeps `running` (and any other key) when it
     replaces the key; `read_key()` and `KeyFile` keep reading `key` only (a write of `running`
     changes the file's time: `KeyFile.current()` reads the same key again, harmless).
   - A small module, `cli/src/chantier/board/running.py`, holds the read, the write, the removal
     and the stop command's text; `command.py` calls it.
2. **`GET /api/board` tells its PID** (`board/routes.py`, `board()`): a `pid` field
   (`os.getpid()`), next to `version` and `served`.
3. **What a new `board` does, before it binds anything** (`command.py`, replacing `_running()`):
   - Read `running` from `board.json`. It counts only when its process is alive and is the one
     recorded: `procs.alive_since(pid, <started as epoch seconds>, unreadable=True)`. A dead one
     is ignored (and overwritten at this start).
   - With a live record, probe the recorded `host` and `port` (`address.probe()`), whatever this
     session's own `--port` or `board.port` says:
     - **Same version, it answers, same `served`:** as today: register `--seat` on it
       (`register_seat()`, refused as today when it does not take the seat) and print
       `board already running at <its link>`, exit 0.
     - **Another version:** start nothing, signal nothing; one line, exit 4 (`EXIT_EXTERNAL`):
       `error: board not started: chantier board <its version> (PID <pid>) already serves this
       surface at <its link>; this is chantier <this version>: to replace it, stop it
       (<stop command>), then run board again`.
     - **Silent** (the probe gets no answer, another key, or not a chantier board, while the
       recorded process lives): start nothing, signal nothing; one line, exit 4:
       `error: board not started: a chantier board <recorded version> (PID <pid>) holds this
       surface at <host>:<port> and does not answer: stop it (<stop command>), then run board
       again`.
   - With no live record (a board of a version before this CR writes none): today's probe of the
     configured address, with the version now compared: same version and same `served`, reuse
     as above; another version, the "another version" line, its PID from the answer's `pid`, else
     looked up among this user's processes whose command line runs `chantier` `board` and that
     listen on that port (`psutil`, already a dependency through `procs.py`), else `PID unknown`
     with the stop command replaced by "stop it from the session that started it, or end the
     process that listens on port <port>". The port-held cases of `_held_by()` stay as they are.
   - The stop command is the platform's: `taskkill /PID <pid> /T /F` on Windows, `kill <pid>`
     elsewhere. The CLI only prints it.
4. **Scope of the rule.** The record lives in the git folder of the served folder, so the rule
   holds per planning surface, and the same way per repository in-project (see Open questions).
5. **Seats are unchanged:** a second session's `board --seat <id>` registers its seat for its own
   project on the running board (`Seats.add`), which then stops only when no registered session
   holds its project's seat.
6. **`AGENTS.md`** (chantier's), the line on what chantier writes: "the board keeps its key in the
   repository's git folder (`chantier/board.json`)" becomes "the board keeps its key, and while it
   serves its PID, address and version, in the repository's git folder (`chantier/board.json`)".
   Nothing else is written anywhere new.

### B. Each session stages only its own project's folder (Q2)

Cards only; the CLI keeps no git write.

- `skills/chantier/references/chief-of-staff.md`, "With a planning surface" (today: "explicit
  paths (`git add -- <path>`), a plain push to the default branch, a rebase on a rejected push"):
  stage only this project's folder or paths inside it (`git add -- projects/<name>/...`), never
  `git add -A`, `git add .` nor a wider folder: another session on the same surface may have its
  own files unstaged there; a file outside the project's folder (the surface's own `AGENTS.md`, its
  root `chantier.yaml`) only by its own path. Then commit, `git pull --rebase --autostash`,
  `git push`; never a force push (unchanged). The bullet "Stopped by the user, or no autosync"
  points to this same rule. The autosync rules are unchanged (enabled: nothing by hand).
- `skills/chantier/references/griller.md`, "In a planning surface": a Griller in the surface's
  checkout follows the same staging rule.
- `skills/chantier/references/concepts.md`, "Planning surface": one sentence: several sessions
  may work one surface on one machine; each stages only its own project's folder, one board serves
  the surface, `preflight` and `status` list the other batches.
- Any other card that tells a session to commit the surface by hand: grep for it and apply the
  same rule. Agent files (`agents/`, `com.github.copilot/agents/`) are not touched.

### C. The other batches of the surface, in `preflight` and `status` (Q3, Q4, Q6)

- **Reader:** a new module `cli/src/chantier/core/surface_batches.py`: for a project in a surface
  (`repo.external`), for each other name of `surface_projects(repo.surface_root)`, read
  `<surface>/projects/<name>/changes/4-batch/batch.json` when it exists
  (`records.read_batch_json`), read-only, no lock, no git call. Each batch gives: the project (its
  folder's name), the batch id, the state (`status`: running or paused; `closing` when
  `closing` is true), the steering mode (`status/words.py`, `steering_word`), and the Drivers it
  runs: `len(rails.held(d))` (CRs working and open QA orders) plus one when `stack_agent` is set.
  An unreadable `batch.json` gives `<project>: batch.json unreadable`. In-project, or a batch
  folder of another surface or repository: nothing is read (Q6). No cap, no refusal, nothing
  written, no message to any session.
- **Text,** one line, the batches sorted by project:
  `other batches on this surface: markdown-okf-schema-studio batch-05 running, steering Foreman,
  3 Drivers; other batch-02 paused, steering direct (the Chief of Staff), 0 Drivers`.
- **`preflight`** (`cli/src/chantier/commands/preflight.py`, `_check_project()`): on a surface, a
  new informational line `P14 ok   <the text>`, or `P14 ok   no other batch on this surface`;
  never a warning, never a failure. In-project and at a surface's root with no project named: no
  P14 line.
- **`status`** (`cli/src/chantier/commands/batch_status.py`, `status()`): the same line after the
  autosync line, only when at least one other batch exists. `STATUS.md`, `STATUS.json` and the CR
  board pane are not changed (so no pane screenshot is due).

### D. The plan (Q3)

`skills/chantier/references/chief-of-staff.md`, "Starting a batch":

- step 1 (the preflight's list of checks): P14 named: the other batches on this surface and their
  Drivers; informational.
- step 2 (Show the plan), where it says how many CRs start at once on how many slots: also the
  other batches of this surface from P14 (project, batch, steering, Drivers), so the user picks
  the slots knowing the machine's load. No cap is proposed or applied.
- The Foreman reads the `status` line as it is; `foreman.md` needs no change.

### E. The board cards and docs

- `skills/chantier/references/session-start.md`, "The board": one board serves a planning surface;
  a second session's `board --seat <id>` registers its seat and prints `board already running at
  <URL>` (the existing bullet). A new bullet for the two new lines (`error: board not started:
  chantier board <v> (PID <n>) already serves this surface ...` and `... does not answer ...`): one
  line to the user with the version, the PID and the stop command as printed; never stop it
  yourself, never start one on another port to get round it; the user decides, then the session
  runs `board --seat <id>` again on the user's word.
- `skills/chantier/references/chief-of-staff.md`, Routes table, "board on my phone" row: unchanged
  except that a board refused as above is the user's to stop.
- `docs/web-board.md`, "The link" and "When it stops": the record next to the key; one board per
  surface whatever the port; the two refusals. `docs/planning-modes.md`: a short paragraph "Two
  sessions on one surface" (staging rule, one board, P14 and the `status` line).
- `scenario/README.md`: the new scenario checks.

## Out of scope

- Any machine-wide slot limit or refusal across batches (Q3: see it, no limit).
- Any message, lock or shared file between sessions beyond the board's record (Q4).
- Stopping, killing or replacing a running board from the CLI or a card (Q5).
- Batches of another surface or repository on the machine (Q6), and batches on another machine
  (`batch.json` is local, never pushed).
- The board's pages (it already serves every project of the surface); `STATUS.md`/`STATUS.json`.
- uv's file locks on Windows (os error 32): unchanged; preflight's P5 already names it.
- The cost of two sessions: each batch's bill stays its own.

## Evidence

- **Tests** (`cli/tests/`, in-process, few and parametrized; `just test` within its budget):
  - `test_board.py`, one parametrized test over the start decision, with `probe`,
    `alive_since` and the bind/serve monkeypatched and a check that no process is signalled:
    live record + same version → `board already running at <recorded link>` though the
    configured port differs; live record + another version → exit 4, both versions, the PID, the
    platform's stop command; live record + silent → exit 4, the "does not answer" line; dead
    record → the board starts and writes a fresh `running`; no record + an older board answering
    with no `pid` → its version and `PID unknown` (or the psutil-found PID).
  - `--new-key` keeps `running`; the exit removes only its own record.
  - One parametrized test of `surface_batches`: a surface with three projects (a Foreman batch with
    two working CRs and a QA order, a paused direct batch, none) gives the one line, the own
    project left out; in-project gives none; an unreadable `batch.json` is named.
- **Scenario** (`scenario/run_scenario.py`):
  - `external_surface`, once `demo` and `other` both have a batch open: `status --project demo`
    holds `other batches on this surface: other batch-NN running, steering direct (the Chief of
    Staff), 0 Drivers`; `preflight --project other` holds a P14 line naming demo's batch and still
    passes; in the board block, while demo's board runs on its port-0 address, `board --project
    other --host 127.0.0.1 --port 0 --seat <id>` prints `board already running at <the same
    link>`, exit 0, and `/api/board` answers its `pid`.
  - `remote_board`, step 9: a board started with `--port 0` while another board of the same
    repository runs is now reused, not started: reorder the "board with no seat" check so it
    starts after the previous board has stopped, and add one check that a second `board --port 0`
    with a live one prints `board already running at <its link>`.
  - The in-project scenario's preflight passes with no P14 line.
- `just check` passes on Linux, macOS and Windows; this CR changes the CLI and the cards, so the
  pipeline's `just scenario (ubuntu-latest)` job is green at the PR's head, and, as the top of the
  batch-23 stack, `just scenario` passes locally (`chantier gate`) at its head. No `hooks/` or
  `types/` change: no `just mod`. No change to what the pane draws: no screenshot.
- In the stack, `chief-of-staff.md` and `session-start.md` are also edited by CRs below (for
  instance 322's titles): rebase and keep both texts.

## Open questions

None. The Chief of Staff settled the spec-writer's two questions with the user (02-answers.md,
round 3): the one-board rule applies in-project too (two-sessions-Q7, A), and `board.json` keeps
the running board's PID, address and version beside its key, with `AGENTS.md` saying so
(two-sessions-Q8, A).
