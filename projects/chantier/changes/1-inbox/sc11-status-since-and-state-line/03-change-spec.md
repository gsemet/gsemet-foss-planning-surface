# SC11: `status --since` and the watcher's `state:` line

Child 11 of 28 of the program CR `simplify-cards-and-prompts`. Its `03-change-spec.md`, "Child
11", and its `02-answers.md` answers 17 to 22 rank above this file. One Driver, one PR, in the
running stack batch (batch-31). Code read: `origin/main` at `8a960d34`. Short forms used below:

- `src/` is `skills/chantier/scripts/cli/src/chantier/`;
- `tests/` is `skills/chantier/scripts/cli/tests/`.

## Goal

The owner's words (answer 1): progressive disclosure to the fullest, through the watcher's and
the server's state lines. Today the steering session reads the whole batch at each wake: plain
`status` prints one row per CR, merged ones included, at every call (study-fable-v2 2.4,
`commands/batch_status.py`). This child adds two read-only outputs:

- `status --since <seq>` prints only what changed in the batch since an event sequence. Merged
  CRs show as one count, and the output ends with the sequence to pass next time.
- A `state:` line on the steering session's told blocks: the batch's counts by state and the
  number of things due, so a wake knows where the batch stands without a `status` call.

Plain `status` does not change, and nothing is recorded.

## Place in the chain

- **Base:** child 10's branch (`brief-prompts`), the previous CR of the stack. Child 10 touches
  `brief`, `references/floor.md` and `driver_prompt.py`, not the files below. No code of child 10
  is used here.
- **Depends on this child:** child 12 (`next-advice`). Its `next --epoch` prints the steering
  session's due list. This child writes that list's first form, `src/status/due.py`, and prints
  only its count. Child 12 imports `due()` for `next --epoch` and adds the one kind this child
  cannot read from the record, `restack owed` (see "Due" below). Once child 12 adds it, the
  `due` count on the `state:` line follows with no change here.
- **Later:** the card rewrite (children 19 to 24) may tell the steering session to use
  `status --since` and to read the `state:` line. No card changes in this child.

## Decisions carried

| Source | Decision | Here |
| --- | --- | --- |
| Program child 11, Scope | `status --since <seq>`: only what changed since a sequence; merged CRs as one count; prints the sequence to pass next time; plain `status` unchanged | "1. `status --since`" |
| Program child 11, Scope | A `state:` line on the steering session's told blocks (`src/hub/watch_lines.py`), with the counts by state and the due count | "3. The watcher's `state:` line" |
| Program child 11, Must not | Plain `status` does not change; nothing is recorded | "Out of scope"; the scenario's byte check |
| Answer 22, F14 | `next` is split from `status --since` and its `state:` line | `next` is child 12; only the due count is here |
| Answer 18 | Tools first: only additions; every intermediate `main` keeps working with the old cards | No existing line, flag or card changes |
| Answer 22, F20 | The PR states the seconds its tests add to `just test`, measured before and after on the same machine | "Gates and evidence" |
| Program rules | A new command or flag adds a scenario step and a coverage bullet; long gate owed; `just check` and `just eval-dry-run` before the first push; the local Windows `scenario` run only if this CR is the stack's top when presented | "4. Scenario", "Gates and evidence" |
| Program child 11, Risk | AGENTS.md: nothing beyond child 9, since `status` already exists | "AGENTS.md" |

## What changes

### 1. `status --since <seq>` (`src/declare/batch_status.py`, `src/commands/batch_status.py`)

**The sequence.** The `<seq>` is the batch's event sequence: the 1-based number of a line of the
batch's `events.jsonl`, counting every physical line, including any half-written line that
`read_events` skips. Batch events carry no `seq` field today, so the line number is the
sequence. The journal's `seq` (`forge-journal.jsonl`, the watcher's cursor) is not used: the
journal lines `status` prints (`_seen_lines`) are open conditions that disappear once recorded,
not history, so they are printed whenever they hold (below). `0` means "since the start".

- **Parser.** Add `s.add_argument("--since", type=int, metavar="SEQ", help=...)` to `status` in
  `src/declare/batch_status.py`. The help text says: only what changed since this event sequence
  of the batch (`0`: everything); merged and cancelled CRs as counts; the last line gives the
  sequence for next time; it records nothing. The command's one-line summary string does not
  change.
- **Reader.** Add `numbered_events(store, folder) -> list[tuple[int, EventRecord]]` beside
  `read_events` in `src/core/records.py`. It reads the same file, numbers each physical line
  from 1, and skips an unparsable line without renumbering the rest. Also return the file's line
  count; a helper that returns `(numbered, last)` is fine. `read_events` does not change.
- **Refusals** (exit `EXIT_USAGE`, before anything is printed):
  - `--since` below 0: `status --since <n>: a sequence is 0 or more; `status --since 0` lists
    everything`.
  - `--since` past the last line: `status --since <n>: <batch>'s events stop at <last>; pass the
    sequence a `status --since` printed, or `status --since 0``. This also catches a journal
    cursor passed by mistake when it is larger than the batch's events.
- **What "changed" means.** For the events numbered above `<seq>`:
  - a CR changed when one of these events has `cr` equal to its id;
  - an order changed when one of these events has `order` equal to its id (`order`, `order-done`
    and every other kind that logs `order=`);
  - the batch changed when one of these events has no `cr` and its kind is not one of
    `heartbeat`, `heartbeat_stopped`, `cost`, `order`, `order-done`, `ask`, `asks-read` or
    `agent`.
- **Output.** A new function `since_lines(repo, d, events, numbered, since, notes, stopped)` in a
  new module `src/commands/batch_status_since.py` builds it. It reuses the plain-status helpers
  on the full record, so each row reads exactly as it does in plain `status`. In this order:
  1. the `state:` line (section 2);
  2. when the batch changed: `_batch_line(d, ...)` and `batch_line(...)`, the two head lines of
     plain `status`;
  3. one `_cr_row` for each changed CR whose status is neither `merged` nor `cancelled`, in
     `order`;
  4. the `handed back:` line of each changed CR whose status is `ready`. Add a public
     `ready_line(repo, d, c, events, stopped)` in `src/status/ready_line.py` that wraps the
     existing `_line`; `ready_lines` stays as it is;
  5. `order_lines` on a copy of the record whose `orders` hold only the changed open orders
     (`d.model_copy(update={"orders": [...]})`);
  6. `merged: <total> (<k> since <seq>)`, always printed, `0` included. `<total>` counts the CRs
     whose status is `merged`, and `<k>` those among them that changed. Then
     `cancelled: <total> (<k> since <seq>)`, printed only when `<total>` is above 0;
  7. `no change since <seq>`, when items 2 to 5 printed nothing;
  8. the open conditions, printed whenever they hold, as plain `status` prints them:
     `_unpaused_line(d)`, `watch_lines(repo, d)`, `_seen_lines(repo, d)`, the
     `<n> asks unread: `chantier asks`` line, and `not_running_line(repo)`;
  9. the `extra` lines of `--refresh` or `--stop-heartbeat`, when either flag is given;
  10. last: `since <seq>, now <last>: next time `status --since <last>``.
- **Not printed with `--since`:** `shape_line`, `writer_lines`, `_other_batches_lines`,
  `no_cr_lines`, `running_batch_lines`, `last_closed_text`, `stack_line`, `held_lines`,
  `parked_lines`, `stack_driver_lines`, and the arrival lines. `arrival_lines` moves the told
  mark (`arrivals-told.json`), which is a write. With `--since`, call `not_running_line(repo)`
  directly, not `closing_lines`, so the mark stays for plain `status` and the watcher. Plain
  `status` still prints all of these.
- **Wiring.** In `status(args)`, after `d`, `events` and `stopped` are read, return the
  `since_lines` output when `args.since is not None`. Otherwise run the existing body unchanged.
  `--since` goes with `--notes` (it applies to the rows), `--refresh` and `--stop-heartbeat`.
  The records those two flags make are theirs and stay as they are; `--since` itself records
  nothing.
- `--since` reads a running or a paused batch, as plain `status` does (`_resolve`).

### 2. The `state:` line and the due list (`src/status/state_line.py`, `src/status/due.py`, new)

**The line.** The template is a constant in `src/status/state_line.py`, so the tests read it from
there:

`STATE = "state: {batch} {status} e{epoch} | {counts} | slots {held}/{slots} | due {due}"`

- `{batch}`, `{status}` and `{epoch}` are `d.id`, `d.status` and `d.foreman_epoch`, as
  `_batch_line` prints them.
- `{counts}` is the CRs counted by their record status, in the order `working`, `ready`,
  `blocked`, `queued`, `merged`, `cancelled`, then any other status in alphabetical order. A zero
  count is left out, and the words are joined by `, ` (for example `working 2, ready 1,
  queued 1, merged 3`). A batch with no CR prints `no CR`.
- `{held}/{slots}` is `len(held(d))`/`d.slots`, the `batch:` line's `slots` figures
  (`rails.held`).
- `{due}` is `len(due(repo, d, events))`.
- `state_line(repo, d, events) -> str` builds it. It reads only; it writes and records nothing.

**Due** (`src/status/due.py`). `due(repo, d, events) -> list[Due]`, where
`Due = NamedTuple(kind: str, unit: str, text: str)`, read from the record and the events only. The
kinds, in this order:

1. `take`, `<cr>`, `take <cr> (slot free)`: in a running batch that is not `stack`, each queued
   CR with no `waits_all(d.crs, c, d.mode)`, not `held` and not `parked`, in `order`. There are
   at most `d.slots - len(held(d))` of them, and none when no slot is free (`rails.slot_free`).
2. `take`, `stack`, `take stack (first stack due)`: one item when `stacks.stack_due(d)` is not
   empty.
3. `judge`, `<cr>`: each `ready` CR with no `ask` event after its last `handback` event whose
   `cr` is that CR. In a stack batch, any `ask` event after it counts, since the stack's asks are
   one ask.
4. `order`, `<O-k>`: each order with no `done`.
5. `reclaim`, `<unit>`: each `working` CR whose `leases.not_confirmed(repo, c.id, c.lease)` is
   not None; the stack's lease (`d.stack_lease`, unit `stack`); each open QA order's lease. The
   text holds `leases.reclaim_command(unit, lease, short=True)`.

`restack owed` is not a kind here. Today it is printed by `order merged` (`restack_line`) and is
not held in the record. Child 12 adds it to this list. The module's docstring says so in one
line, so child 12 finds the place.

### 3. The watcher's `state:` line (`src/hub/watch.py`)

- **Who gets it.** Only the steering session's watcher:
  - the Foreman's watcher (`self.foreman` is not None), for its batch;
  - or a seat watcher (`self.foreman` is None) when the open batch's `steering` is `direct`.

  The Chief of Staff's watcher of a batch steered by a Foreman gets no `state:` line, and
  neither does a watcher with no open batch.
- **Where.** Add `Watch._state() -> list[str]`. It reads `autostart.open_record(self.repo)`
  (running or paused, else None) and that batch's events (`read_events(repo.store,
  repo.batch_dir(d.id))`), then returns `[state_line(...)]` or `[]`. When the record or the
  events cannot be read (`OSError`, `ValueError`, `ChantierError`), it returns
  `["state: unreadable (<error>)"]`.
  - In `tell()` (the `--stream` block), the `state:` line goes just before the `STREAM_TOLD`
    line.
  - In `lines(reason)`, for `EVENTS` and `IDLE` (the Chief of Staff's and the Foreman's end
    texts), it goes just before the last line.
  - For `SEAT` and `END`, no `state:` line is added.
- The watcher's module docstring (`hub/watch.py`) gains one sentence: at each telling, the
  steering session's watcher reads its batch's record to print the `state:` line. It still reads
  no journal file and no forge.
- `src/hub/watch_lines.py` gains no constant. The template is `status/state_line.STATE`, which
  `status --since` uses too.

### 4. Scenario (`scenario/run_scenario.py`, `scenario/README.md`)

In the `parallel` unit's `scenario` function, section 5, around the `order note CR-101` step
(at `origin/main`: `_, out = w.chantier("order", "note", "CR-101", ...)` followed by
`status shows the pending order`):

- Before the `order note`, run `status --since 0`. Read `<s>` from its last line (`since 0, now
  <s>: next time ...`). Check that the first line starts with `state: batch-01` and holds
  `due `.
- After the `order note`, snapshot the bytes of `batch.json` and `events.jsonl`, run
  `status --since <s>`, then check:
  - one row starts with `CR-101 `;
  - the order line holds `note CR-101`;
  - no row starts with `CR-105 ` (taken before `<s>`);
  - a `merged: ` line is present;
  - the last line names a sequence larger than `<s>`;
  - the two files are byte-identical after the call ("`status --since` records nothing").
- After the unit's first recorded `order merged`, run `status --since <s>` again. Check that its
  `merged: <n>` equals the number of CRs whose status is `merged` in `w.batch()`.
- Check that plain `status` around these steps still prints its usual lines, using the checks
  that already read them. No existing check changes.
- `scenario/README.md`, "## Coverage": add one bullet:
  `- `status --since` and the `state:` line (unit: parallel): only the changed CRs and orders,
  merged CRs as one count, the next sequence on the last line, nothing written; the steering
  watcher's `state:` line (test: test_status_since.py::<the listing test>) (test:
  test_watch_state_line.py::<the watcher test>)`.

  `tests/test_scenario_coverage.py` checks that both test names exist.

### 5. Tests (`tests/test_status_since.py`, `tests/test_watch_state_line.py`, new)

Both use prepared records: `batch.json` and `events.jsonl` written by the test, as
`test_watch_stream.write_status` does, and the CLI called in-process.

- `test_status_since.py`:
  - **Listing, parametrized over `--since` values** (0, a sequence in the middle, the last line).
    Only the CRs and orders with events above the sequence get a row or an order line. The batch
    lines appear only after a batch-level event. A CR that changed but is merged gets no row.
    `no change since <n>` is printed at the last line.
  - **Merged count, parametrized** (no merged CR, one merged before the sequence, one merged
    after it): `merged: <total> (<k> since <n>)` is exact. The `cancelled:` line is printed only
    when its total is above 0.
  - **Numbering.** A half-written middle line counts in the sequence and is skipped as an event.
  - **Refusals.** A negative value, and a value past the last line, each exit with
    `EXIT_USAGE`, and the text names `status --since`.
  - **Nothing written.** The bytes of `batch.json`, `events.jsonl` and `arrivals-told.json` are
    equal before and after a `--since` call.
  - **Plain `status` unchanged.** The output of plain `status` on the same prepared record is the
    same before and after the change: assert that it holds no `state:` line and no `since `
    line, and that its rows include the merged CR.
  - **Due, parametrized over the five kinds** (a takeable queued CR with a free slot, a stack
    batch with `stack_due`, a ready CR handed back with no ask and then with one, an open order,
    a working CR whose lease is not confirmed). Each kind shows in `due()` and in the
    `state:` line's `due` count. A full batch (no free slot) gives no `take` item.
- `test_watch_state_line.py`, driven with an injected monotonic time as `test_watch_stream.py`
  does, with no sleep:
  - **Who gets it, parametrized:**
    - a Foreman's watcher of its batch: the line is present;
    - a seat watcher of a `direct` batch: present;
    - a seat watcher of a `foreman` batch: absent;
    - no batch: absent.
  - **Where.** The line is the second-to-last line of `tell()` and of `lines(EVENTS)`. It equals
    `STATE.format(...)` for the prepared record, and its counts and slots are checked.
  - **Unreadable.** An unreadable `events.jsonl` gives `state: unreadable (`.
- **Existing tests to adjust.** `tests/test_watch_foreman.py:111` asserts
  `len(first) == KINDS + 1` on a Foreman's told block. It becomes `KINDS + 2`, and the test also
  asserts that `first[-2]` starts with `state: `. Any other told-block length the suite asserts
  for a steering watcher with an open batch gets the same edit, nothing else.
  `test_watch_stream.py` runs with no batch, so it does not change.

## Out of scope

- Any change to plain `status`'s output, flags or records, or to `STATUS.md` and `STATUS.json`.
- Recording anything: no event, no record field, no journal line, no told mark moved by
  `--since`.
- `chantier next`, `next:` lines and the `restack owed` due kind: child 12.
- A `state:` line on plain `status`, on the Chief of Staff's watcher of a batch a Foreman steers,
  on `watch --once`, or on the board and `chantier live`.
- A journal cursor form for `--since` (see the open question).
- Any card, hook or wrapper text: answer 18 and the program's card rule. No child before 19 edits
  a card.
- A new journal type (so `just journal-schemas` is not run) and any version edit.

## Gates and evidence

- `just test` passes with the two new files and the adjusted Foreman test.
- The added `just test` seconds, measured before (at the base) and after (at the head) on the
  same machine, go under the PR's Deliverables. Expected: under 1.5 s (about twelve in-process
  status calls on small prepared records and four watcher runs with no sleep).
- `just check` and `just eval-dry-run` (a change under `src/`) are run in the worktree at the
  rebased head before the first push.
- The long gate `just scenario (ubuntu-latest)` is green at the PR's head, since the CLI and the
  scenario change. The local Windows `chantier gate <cr> scenario` is owed only while this CR is
  the stack's top. It moves to the CR that joins above it.
- No host or default matrix. The `state:` line goes into both the `--stream` block and the
  watcher's end lines, so it shows the same on Claude Code (`--stream` through `Monitor`) and on
  Copilot (the plain watcher). No configured value changes it.
- No check guards a shipped file. The tests assert the CLI's output on prepared records.
- No `hooks/` or `types/` change, so `just mod` is not owed.

## Risk

- A role passes the watcher's journal cursor (`told up to cursor <n>`) to `status --since`. When
  that cursor is past the batch's last event, the refusal catches it. When it is below, the
  output starts from the wrong point, but it is still a correct listing of the changes since
  that event. Plain `status` stays the complete view. No card asks for `--since` before the
  rewrite, which can name the right sequence.
- The due count leaves out `restack owed` until child 12, so it can read one lower than child
  12's list in a stack batch right after a merge. `order merged` already prints that line.
- The Foreman's told block gains a line. One test is adjusted. The old cards read the event
  lines, not the block's length.
- **AGENTS.md:** no change. No new command, and no new git, network or write exception:
  `status` exists, `--since` and the watcher's read of the record write nothing. The role
  sentences are child 9's.

## Open questions

1. The program says `status --since` takes "a journal or event sequence". This spec takes the
   batch's event sequence only (the line number in `events.jsonl`). The reason: the journal lines
   `status` prints are open conditions, printed whenever they hold, and the journal holds no
   hand-back, take or order. Should `--since` also accept the watcher's journal cursor, in a
   form that cannot be mistaken for the event sequence (for example `--since j<n>`)? Until you
   answer, only the event sequence is built.
