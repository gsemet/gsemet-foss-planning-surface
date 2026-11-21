# Change Specification: `chantier access` explains why a session may or may not write, claim or push

Origin: verbal (2026-11-10, Beads study; grilled 2026-11-20 in `planning-server`). No tracker issue.

Part F of the seven-part split of `planning-server` (planning-server-Q7, "7 CR séparés"). This CR
was grilled in that CR, not here. Its grill is
`2-backlog/P3/planning-server/02-answers.md` (Q1 to Q30), and its reference is that CR's
`experiments/03-change-spec-all-parts.md`, "Part F" (with §1 to §4, the docs map in §2, and §5 to
§9 where they name F). The specified CRs it builds on rank above the reference where they differ:

- Part C, the writer: `2-backlog/P3/planning-server/03-change-spec.md` (approved). This CR uses its
  `writer` entry, states, blocked reasons and refusal text.
- Part D, leases: `1-inbox/driver-leases/03-change-spec.md` and its `02-answers.md`. This CR uses
  the lease's live, expired and ended states, its refusals, `--reclaim`, and which commands take
  `--lease`.
- Part B, the store: `1-inbox/plan-store-interface/03-change-spec.md` and its `02-answers.md`. This
  CR uses `check_publish(..., command=)` and `Repo.find(readonly=True)`.
- Part E, typed waits (`1-inbox/typed-waits`), is still being specified. This CR relies on the
  reference's E.2: "A wait changes no rule".

This CR's own open questions were settled by the Chief of Staff on 2026-11-20, in
[`02-answers.md`](02-answers.md) (answers 1 to 5). They are written below as decisions.

`depends.json`: `{"after": ["planning-server", "driver-leases"]}`. This CR lands after both.

## 1. Goal, in the user's terms

One of the five ideas borrowed from Vercel Board, built in chantier with no Board dependency (the
user, 2026-11-20, Q3: "tout"). The idea is "an 'explain access' command: why a session may or may
not write, claim or push".

The three rules are spread over several CRs: no writer means no write (Part C), a lease protects a
CR (Part D), and `take` checks slots, the budget, dependencies and the epoch. One read-only command
gives a session, in a few lines, what each rule says now for it. The session learns it before it
acts, or after a refusal it does not understand, instead of asking. The command explains and changes
nothing. Board's per-principal grants, conditional writes and schedules are not taken (reference
§9). Only the explanation is taken.

## 2. Words

- **Session key:** the key `hub/autostart.py`'s `session_key()` gives this CLI run. It is the
  host's session id (the transcript) kept to `[A-Za-z0-9-]`, else `none`. The seat holds a session
  when the seat's `transcript`, kept the same way, equals that key. This is the comparison
  `commands/seat.py`'s `_own_watch_line` makes.
- **Write:** a published write to the planning folder (Part B, Part C's §4). Local files
  (`batch.json`, `events.jsonl`, the STATUS files, the locks, the journals, `seat.json`) are never
  refused (C.8).
- **Claim:** `take <cr> --epoch <n>`: a Driver given a CR.
- **Push:** a `git push` of a CR's branch by its Driver, and, in external mode, the push of the
  surface, which is the writer's alone (Q26).
- **Lease, live, expired, ended, current:** as Part D defines them (D.1, its §2). In that CR's
  `02-answers.md` (spec critic, point 1), "expired" means "not confirmed", not "gone".
- **Writer, `off`:** as Part C defines them (§4, C.4). `off` means `server.json` has no live
  `writer` entry.

The CLI knows no role (AGENTS.md). `access`'s own words name the seat, the epoch, the lease and
the writer, and never a role. A refusal of another command is quoted as that command prints it.
Never "epoch" in a text to the user: the flag `--epoch` keeps its name, and the number is said
"Foreman n°<k>" as `require_epoch` says it today.

## 3. Decisions carried

| Decision (date) | Where it lands |
| --- | --- |
| Q3 "tout": all five Board ideas, the "explain access" command among them (11-20) | §4 |
| Q1-Q2: no Board dependency, hosted or local (11-20) | built in chantier; no grant, no conditional write (§9) |
| Q7: seven CRs; F needs C and D (11-20) | `depends.json`; §4 reads C's `writer` entry and D's leases |
| Q9 "Exception nommée": `access` is built and named in AGENTS.md as an exception to "a new CLI tool comes from measured token-costly behaviour", citing "tout" (11-20) | §6.3 |
| Q5: no writer, no write; no fallback (11-20) | §4.3, the `write` refusal |
| Q26: the writer pushes every commit of the surface; nobody pulls or pushes the surface by hand while a writer runs (11-20) | §4.5, the `push surface` line |
| Q27: with no writer and an older board serving, the line names its version, PID and stop command (11-20) | §4.3 |
| Q10: sessions write the surface's files under the CLI's locks; only the writer commits, rebases and pushes (11-20) | §4.3 (writes allowed while a writer runs, whatever its state) |
| Q14, Q20: the lease's role in `close` per host | not read by `access` (`close` is not one of the three actions) |
| Q16: the lease is 10 minutes, renewed every 3; its times are UTC (driver-leases answer 5) | §4.4, §4.5: lease times in UTC |
| driver-leases, spec critic 1: an expired lease means "not confirmed"; a `take` on it still needs `--reclaim` | §4.4 |
| driver-leases: `--lease` required on `round`, `ship`, `handback`, the stack driver's writing forms and `release start\|go\|published`, optional on `gate`, `note`, `phase`; a valid one renews | §4.5 (`push` reads `--lease`); §4.1 (`access` never renews) |
| plan-store-interface answer 5: `check_publish` names its command | §4.4: the claim quotes `take`'s refusal, with the command's name |
| The split carries its docs and SVGs as a list (11-20) | §7 |
| explain-access 1: push on an expired current lease nobody took again is allowed, "renew it first" (11-20) | §4.5, step 7 |
| explain-access 2: `chief-of-staff.md` gets the "run `access` before asking" line (11-20) | §6.1 |
| explain-access 3: claim on a working, ready or blocked CR is not refused; the line names `--note` (11-20) | §4.4 |
| explain-access 4: no scenario case (11-20) | §8 |
| explain-access 5: `claim` and `push` take a CR only (11-20) | §4.1, §9 |
| Reference E.2: "A wait changes no rule: `take`, `close`, `open` and the slots read the CR's status as today" | §4.4: no wait is read |

## 4. What changes

### 4.1 The command

`chantier access [write|claim|push] [<cr>] [--lease <n>] [--epoch <n>] [--batch <b>]`

- Declared in a new module `skills/chantier/scripts/cli/src/chantier/declare/access.py`, registered
  in `cli.py`'s module list. Its handler is in a new `commands/access.py` (`access`). Its scope is
  `BATCH_EPOCH` (`commands/registry.py`), so it takes `--batch` and `--epoch` as `take` does, plus
  its own `--lease` (int).
- Positionals: the first one is the action when it is `write`, `claim` or `push`, else it is the
  CR. The CR is normalized as every command does (`cli._one_spelling_of_a_cr`).
- With no action, all three actions are answered: `write` always, `claim` and `push` only when a
  CR is named. With `claim` or `push` and no CR, the command exits 1 (`EXIT_USAGE`) with
  `access <action> <cr>: name the CR`. That is a usage error, not an answer.
- **Read-only**, exit 0 whatever the answers. It reads the repository with
  `Repo.find(readonly=True)` (Part B: no `.gitignore` written), reads the batch with `read_batch`
  (never `RenderedBatch`, which renders the STATUS files), and reads `server.json` with
  `hub/state.py`'s `live_entry`. It does not refresh the spend (`refresh_for_check` is `take`'s, not
  `access`'s): the budget answer uses the recorded spend and says so (§4.4). It renews no lease, even
  when given a valid `--lease`. It removes no dead `.lease-hold.*.run` record: a dead one holds
  nothing, as D.1 says, and stays for the next `lease`, `take` or `status`. It runs no git write.
  `check_release_branch`'s read-only `git rev-parse` and `git merge-base --is-ancestor` are allowed.
  It appends no journal line and writes no log event.
- An option an action does not read changes nothing: `--epoch` is read by `claim`, `--lease` by
  `push`.
- Output order: the session line, then `write`, `claim` and `push` (with `push surface`). At most 6
  lines, under `cli.py`'s `MAX_LINES` (10). No `FULL_OUTPUT` entry is needed.

### 4.2 The session line (always first)

- `session <key>: holds the seat of <project>`
- `session <key>: the seat is <other session> (<link>)`: `<other session>` is the seat's `session`
  and `<link>` its `link`, or `unknown`, as `seat` prints them.
- `session <key>: no seat recorded`

`<key>` is `session_key()`. `<project>` is `board/projects.py`'s `project_name(repo)`. The seat is
read with `core/seat.py`'s `read_seat`.

### 4.3 `write`

- In-project: `write: allowed: in-project planning folder, under the lifecycle lock; chantier
  commits nothing`
- External, a live `writer` entry: `write: allowed: the surface's writer runs (pid <p>, <state>);
  it commits and pushes within 5 min`. When `<state>` is `pending`, `offline`, `blocked` or
  `conflict` (the states for which C.8 adds `writer: <state>: not pushed yet (...)` to a write), the
  line adds `; not pushed yet: <reason or ahead count>`, with the same content C.8 gives in its
  parenthesis, from one function shared with C.8's line. `synced` and `syncing` add nothing. `<p>`
  is the entry's `pid`.
- External, no live `writer` entry (`off`): `write: refused: the surface's writer is not running;
  start the surface server ($CHANTIER board --seat <session id>)`
- External, `off`, and a live `server` entry of another version than the reader's (C.8 and C.10,
  Q27: an older board serving with no writer): `write: refused: the surface's writer is not
  running: chantier board <version> (PID <pid>) serves this surface with no writer; stop it (<stop
  command>), then start the surface server ($CHANTIER board --seat <session id>)`. The version,
  PID and stop command come from the same reading C.8's text uses (`board/command.py`'s
  `_another_version`, `running.stop_command(pid)`). In both `off` lines, `$CHANTIER` is printed as
  `cli_command(repo)` prints it, as C's lines do.

The reference's "5 min" is the user's bound (Q4), as C's §1 states it.

### 4.4 `claim <cr>`

`take`'s checks, run read-only, in `take`'s order. To keep the two from drifting, `take`
(`commands/driver.py`) and `access` call **one** function that holds the checks, so a check added
to `take` later is answered by `access` with no second edit. At this CR's base, that order is:

1. the CR's batch (`find_cr_batch`: `no batch holds <cr>`);
2. the epoch (below);
3. `refuse_held` (a CR held out of the stack);
4. Part D's lease check, where Part D placed it: a live lease, and an expired one (driver-leases'
   spec critic 1: a `take` on an expired lease still needs `--reclaim`). The refusal is quoted as
   Part D prints it, `--reclaim` way out included;
5. `check_take` (`rails.py`): the CR's status, an agent recorded, the budget, the slot, the
   dependencies, a release's fixes;
6. `check_release_branch` (a release in an ordered batch);
7. Part B's `check_publish` with `take`'s published paths (`command="take"`). In external mode with
   no writer, this is Part C's refusal (C.8).

Where Parts B and D put their checks in `take` at the rebased head decides 4's and 7's places. The
shared function follows them.

Lines:

- `claim: allowed: <cr> is <status>; <k> of <s> slots held; dependencies ready; budget left <x>`.
  `<k>` and `<s>` are `len(held(d))` and `d.slots`. For the budget, `<x>` is the budget minus the
  recorded spend, printed with `rails.usd_text`. With no budget set it is `none set`. With the spend
  not yet priced, it is `budget $<b>, spend unknown`. In every form it is followed by ` (last
  recorded spend)`, because `take` refreshes the spend first and may answer otherwise (concepts.md,
  "Slots, budget, rounds").
- `claim: refused: <the refusal take would print>`: its text with no `error: ` or `take: ` prefix.
  That covers a live or expired lease, no slot, a dependency, the budget, an agent recorded, the
  CR's status, a held CR, a release's branch, and no writer. Only the first refusal is printed, as
  `take` stops at the first.
- `take`'s `--note` rule (a working, ready or blocked CR needs `--note` saying why) is not a refusal
  of the claim, because `access` has no `--note` (explain-access answer 3). The allowed line then
  ends with `; take needs --note saying why (<cr> is <status>)`.
- The epoch. With no `--epoch`, or a stale one, the checks are still answered, and a second line
  follows: `claim: needs the steering session's --epoch (Foreman n°<k>)`, where `<k>` is the batch's
  `foreman_epoch`. With the current one, nothing more is printed. A stale `--epoch` is not the first
  refusal, because the claim explains every other check too.
- Waits (Part E) are not read. A wait changes no rule (reference E.2), so a CR with open waits gets
  the same answer as without.
- A batch opened before Part D's version has no lease. Step 4 has nothing to check, as `take` does
  today.

### 4.5 `push <cr>`

The CR's branch is `c.branch` from the record. Lease times are UTC (driver-leases, answer 5). The
lines below are tried in this order:

1. The CR in no batch: `push: refused: <find_cr_batch's text>`.
2. The CR not `working`: `push: refused: <cr> is <status>`.
3. A batch with no lease (opened before Part D's version): `push: allowed: <cr> is working; no
   lease in this batch; push <branch> without force; a rewrite uses --force-with-lease (driver.md)`.
4. No `--lease`: `push: refused: no --lease given (lease <n> is current)`.
5. A `--lease` that is not the current one, or the current one ended: `push: refused: claim lost
   (lease <m> is current)`. When the current lease is ended, `<m>` is the ended one's number, and
   the line adds `, ended at HH:MM`.
6. The current lease, live: `push: allowed: lease <n> of <cr> is live; push <branch> without force;
   a rewrite uses --force-with-lease (driver.md)`.
7. The current lease, expired (nobody took the CR again), allowed (explain-access answer 1):
   `push: allowed: lease <n> of <cr> expired at HH:MM, not taken again; renew it first
   (lease <cr> renew --lease <n>), then push <branch> without force; a rewrite uses
   --force-with-lease (driver.md)`. Part D accepts a late Driver's command on such a lease.

In external mode, one more line follows: `push surface: only the writer pushes the surface; never
by hand` (Q26; C.7's resolution by the Chief of Staff pushes nothing either).

The force-push route of `driver.md` ("Means: a force push the host refuses") is unchanged: `access`
says what the rules allow, not what the host will accept.

## 5. Host and default matrix

`access` depends on the host only for the session key (`detect_host`, `own_transcript`). It
depends on no configured value: it reads the batch's own slots and budget from the record, never
`batch.slots` from a `chantier.yaml`. It does depend on the planning mode and the writer's state.

| Host / mode | Cell | Expected |
| --- | --- | --- |
| Claude Code | the session's transcript is the seat's | `session <key>: holds the seat of <project>` |
| Copilot | the session's transcript is the seat's | the same line, with the Copilot session's key |
| no host (a bare terminal) | any | `session none: ...` with the seat's line; never the "holds" form |
| any | another session holds the seat | `session <key>: the seat is <other session> (<link>)` |
| in-project | `write` | allowed, "chantier commits nothing"; no `push surface` line |
| external | writer `synced`, `syncing` | `write: allowed: ...`, no suffix |
| external | writer `pending`, `offline`, `blocked`, `conflict` | `write: allowed: ...; not pushed yet: ...` |
| external | writer `off` | `write: refused: ...` |
| external | writer `off`, an older board serving | `write: refused: ...` naming its version, PID and stop command (Q27) |
| external | `claim` with writer `off`, every other check passing | `claim: refused: <C.8's text for take>` |

## 6. Cards and project rules

### 6.1 Cards (`skills/chantier/references/`)

The contract is in the cards. No agent file (`agents/`, `com.github.copilot/agents/`) changes.

- `concepts.md`, "Words": a new entry, **`access`**. `$CHANTIER access [write|claim|push] [<cr>]`
  explains, read-only, what the rules say now for this session: whether it may write the planning
  folder (the writer), claim a CR (`take`'s checks, with `--epoch`) or push a CR's branch (its
  lease, with `--lease`). It changes nothing, renews no lease and is no permission. A refusal stays
  the refusing command's.
- `driver.md`: one line, **off the common path**, so the 45,000-byte cap of
  `test_startup_manifest.py` (`CR_DRIVER_COMMON_PATH_LIMIT`) is untouched: "A refusal you do not
  understand (a write, a `take`, a push): run `$CHANTIER access <cr> --lease <n>` before you ask;
  it explains and changes nothing." It goes in the level-2 lease section driver-leases adds off the
  common path (D.5, "a new `## Means: ...` section"). That section is linked already, so this CR adds
  no byte to the common path. When that section does not exist at the rebased head, the line goes in
  another level-2 section that the manifest does not list under `actions["cr-driver"]` and that the
  common path links, and that link adds at most the bytes the common path has free.
- `foreman.md`, "The batch's limits are the CLI's" ("a refusal is a fact, not an argument"): adds
  "a refusal you do not understand: `$CHANTIER access <cr> --epoch <n>` before you ask; it explains
  and changes nothing".
- `griller.md`, "In a planning surface" (as Part C rewrites it): adds "a refusal you do not
  understand: `$CHANTIER access` before you ask". With the writer `off` it prints the same fact as
  `seat`'s `writer:` line.
- `chief-of-staff.md` (explain-access answer 2): one line in its direct-mode steering text, where
  it takes a Griller's or a Driver's refusal: "a refusal you do not understand: `$CHANTIER access
  <cr> --epoch <n>` before you ask; it explains and changes nothing".
- `routing.md` and `startup-manifest.json`: unchanged (no new action, no new reading on a common
  path).

### 6.2 Structure tests

`tests/test_startup_manifest.py` and `tests/test_plugin_files.py` stay green on the shipped cards,
read from the repository at the head under test.

### 6.3 `AGENTS.md` (chantier's own; the user's merge of the PR is their approval)

One edit, in "The CLI's scope", made so that it composes with the other pending CRs that edit the
same sentence:

- `planning-server` adds the writer as a third named exception.
- `driver-leases` names `lease` (with `take --reclaim` and `lease hold`).
- `typed-waits` names `wait`.
- `outside-poller` names `interests` and `journal add`.

The rule:

- This CR adds **one item**, `access`, in the same form and place as the `lease` item stands at
  this CR's rebased head (`driver-leases` lands before this CR). The item reads: "`access`:
  read-only, it explains why a session may or may not write the planning folder, claim a CR or push
  its branch, and changes nothing; built on the user's answer of 2026-11-20 ("tout": all five of
  Vercel Board's ideas, planning-server-Q9), with no measured cost".
- When the sentence states a count ("Two named exceptions", "Three ...") or orders its items
  ("First", "Second", ...), the count becomes the number of items the text names once `access` is
  in, counted again at the rebased head, never incremented from a remembered number. `access`
  takes the next ordinal. This way an item that `typed-waits` or `outside-poller` landed in between
  is kept and counted. Whichever of these CRs lands later rebases and counts again the same way.
- Nothing else in AGENTS.md changes. `access` writes nothing, so the write list stays as it is. It
  uses no network, so the no-setup sentence stays. It runs no git write, so the git exceptions stay.
  It is neither the hub nor the watcher, so their sentences stay. The "CLI knows no role" sentence
  stays, because `access` names no role.

## 7. Docs, diagrams and other text made false (the list)

None. `access` adds a command and changes no behaviour a doc or a diagram describes. The reference's
docs map (§2) gives Part F no row. Searched:

- `README.md` and `docs/*.md`: no page lists the CLI's commands; each names those it uses.
  `docs/use-cases.md`, "When chantier says no", and `docs/tutorial-claude-code.md`, "If something
  goes wrong", stay true, because `access` explains a refusal and changes none. `docs/web-board.md`
  and `docs/boards.md` are unaffected: no board view, no `STATUS.json` field and no pane change,
  so no screenshot is owed. `docs/planning-folder.md` is unaffected: no new file and no journal
  type.
- Every `docs/*.svg` and its `docs/*-texts.md`, searched for "refus", "claim", "push", "explain"
  and "why": `batch-lifecycle` ("open is refused while a batch is not closed", "refused, naming the
  cause, while anything runs") and the other hits name refusals `access` does not change. No
  diagram draws who may write, claim or push. No SVG, no `-texts.md` and no `<desc>` changes.
- `docs/release-notes/` is history and never edited. The release's notes are a new file, written
  by the release process.

## 8. Evidence

- `skills/chantier/scripts/cli/tests/test_access.py` (new): parametrized, calling the CLI
  in-process on prepared states (the clock frozen through `core/clock.py`'s seam, the session key
  through the host seam the watcher tests use). One case per line of §4:
  - session: the seat held by this session, by another (its link, and `unknown`), and no seat;
  - write: in-project; external with a prepared `writer` entry (the test process's pid, so it is
    live) in each of `synced`, `syncing`, `pending`, `offline`, `blocked`, `conflict`; external with
    no entry; external with no `writer` entry and a live `server` entry of another version (Q27);
  - claim: allowed (with the slots, dependencies and budget fields, and the three budget forms);
    a live lease; an expired lease; no slot; a dependency not ready; the budget spent; an agent
    recorded; a CR `merged`; a `working` CR (the `--note` ending); no `--epoch` and a stale one (the second line); no writer in external
    mode; a batch with no lease;
  - push: allowed on a live lease; no `--lease`; a stale lease; an ended one; an expired current
    one (§4.5, step 7); a CR `ready`; a batch with no lease; the `push surface`
    line in external mode only;
  - `claim` and `push` with no CR exit 1 with the usage text; every answer exits 0;
  - **nothing written:** for every case above, every path of the planning folder and of the git
    folder's `chantier/` (with its bytes and its modification time), `batch.json` and
    `events.jsonl` are the same before and after. Part B's fingerprint helper is used when it
    exists, else one in this file. A valid `--lease` leaves the lease's `renewed` and `expires`
    unchanged. A dead hold record is still there afterwards.
  - **one check function:** for each refusal case of `claim`, `take` on the same prepared state is
    refused with the text `claim: refused:` quotes (both read from one run each). This ties the two
    together through the shared function of §4.4.
- Budget: `test_access.py` adds at most 1.5 s to `just test` on the user's Windows machine. That
  stays within AGENTS.md's 30 s above 18.5 s, because the states are small and in-process, with no
  git process but `check_release_branch`'s two reads in one case. Measure it with `pytest
  --durations=0` before and after, and record both numbers in the PR.
- `tests/test_startup_manifest.py` (the 45,000-byte common path) and `tests/test_plugin_files.py`
  stay green on the shipped cards, read from the repository at the head under test, not a copy.
- `just check`. `just eval-dry-run` (the change is under the CLI's `src/`). `just scenario`, green
  on the pipeline's `just scenario (ubuntu-latest)` job, and locally on Windows (`chantier gate`)
  when this CR is its batch's top (AGENTS.md). No scenario case is added (explain-access answer 4): the prepared-state tests cover it.
  No CI job is added or changed. Nothing changes under `hooks/` or `types/`, so `just mod` is not
  owed.

## 9. Out of scope

- Any change of a rule: `access` grants, waives, renews and reclaims nothing (no `--reclaim`, no
  `--note`, no lease renewal). The refusals stay their commands'.
- Board's per-principal grants, conditional writes, schedules and task runner (reference §9).
- `close`, `open`, `round`, `ship`, `gate` and the other commands as actions of `access`. Only
  write, claim and push are named (Q3).
- Waits (Part E): not read (reference E.2).
- The board, `STATUS.json` and the CR board pane: `access` is a CLI line only.
- `stack` and a QA order `O-k` as units of `claim` or `push` (explain-access answer 5): a CR only;
  `lease stack` and `lease O-k` (Part D) explain those leases.
- A JSON output of `access`.
- Several machines: `access` reads this machine's record, writer entry and leases, which are local
  (D.1).

## 10. Rollout

- The next release's notes say: `chantier access [write|claim|push] [<cr>]` explains, read-only,
  whether this session may write the plan, claim a CR or push its branch, and why.
- Nothing to migrate: no file, no record field, no configuration key. A batch opened before Part D's
  version is answered with the no-lease forms (§4.4, §4.5).
- Mixed versions: the cards that name `access` ship with the CLI that has it (one plugin). An older
  CLI answers `access` with argparse's unknown-command error.

## 11. Self-containment notes for the Driver

- Seams: `commands/driver.py` (`take`: the order of its checks, which become the one shared
  function), `rails.py` (`check_take`, `held`, `slot_free`, `unmet`, `over_budget`, `spent_text`,
  `usd_text`), `stacks.py` (`refuse_held`), `commands/driver_checks.py` (`check_release_branch`),
  `core/batch.py` (`find_cr_batch`, `read_batch`, `require_epoch`, `check_epoch`'s texts),
  `core/seat.py` (`read_seat`), `commands/seat.py` (`_own_watch_line`'s comparison),
  `hub/autostart.py` (`session_key`), `board/projects.py` (`project_name`), `hub/state.py`
  (`live_entry`, `other_version`, Part C's `WRITER`), Part C's C.8 helper for "not pushed yet" and
  its older-board reading, Part D's `core/leases.py` (live, expired, ended; the hold and gate
  records), Part B's `Repo.store.check_publish(..., command="take")` and `Repo.find(readonly=True)`,
  `commands/registry.py` (`add_command`, `BATCH_EPOCH`), `cli.py` (the module list, `MAX_LINES`).
- Code shape (`tests/test_code_targets.py`): files at most 400 lines, functions at most 50, no
  import cycle. `commands/driver.py` is at 377 lines, so the shared check function goes in
  `commands/driver_checks.py` or a new module, not in `driver.py`.
- Portability: no shell, paths with forward slashes in messages, UTF-8 output (as every command).

## 12. Open questions for the user

None. The first specification's five were settled in [`02-answers.md`](02-answers.md).
