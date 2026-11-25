# SC11 + SC12 + SC13: `status --since` and the watcher's `state:` line; `chantier next` and `next:` lines; A Driver messages the steering session through the board

This CR carries children 11, 12, 13 of the program `simplify-cards-and-prompts` in ONE Driver, ONE PR, in this order, as the owner asked on 2026-11-25 ("regroupe les CR entre elles pour en faire des plus grosses"). Each part below is the full Change Specification of one child, unchanged: do them in order, one after the other, commit by commit. Where a part says "child N's branch", "on child N" or "waits for child N" and child N is another part of this CR, it means the earlier part of this same branch, not another PR. The gates of the parts are all owed, run once at the PR's head (the strictest part decides which long gate). If the context runs short, hand back with the exact state at about 100k tokens: parts done, parts left. The answers of every part are appended to this folder's `02-answers.md`.


---

# PART 1 of 3: SC11: `status --since` and the watcher's `state:` line

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


---

# PART 2 of 3: SC12: `chantier next` and `next:` lines

Child 12 of 28 of the program CR `simplify-cards-and-prompts`. Its `03-change-spec.md`
("Child 12", "Rules for every child", "Order") and its `02-answers.md` answers 11, 13 and 17 to 22
rank above this file. This child needs one Driver and one PR, in the running stack batch
(batch-31). Code read: `origin/main` at `8a960d34`.
Short forms used below:
- `src/` is `skills/chantier/scripts/cli/src/chantier/`;
- `tests/` is `skills/chantier/scripts/cli/tests/`.

## Goal

The owner's words (answer 11): `next` is advice, for choosing a CR and for wording. Safety steps
stay refusals, not advice. Answer 13: in direct mode, the Chief of Staff gets the Foreman's
tools, `next` among them. The measure behind it (study-behaviour 3.5) is the Foreman's heartbeat.
It is 37 to 64 % of the Foreman's weighted tokens. One tick is about 7 model calls at 180,000
tokens of context (`status`, `agents`, `take`, a start, `ScheduleWakeup`). A command that
answers "nothing due" in one call removes most of that.

This child adds one read-only command, `chantier next`, and a `next:` line at the end of the
eight commands that move a CR or the batch. Both come from one function, so the advice a role
gets after a command is the advice `next` gives. Later, the new cards (children 19 to 24) rely on
this instead of listing steps.

## Place in the chain

- **Base:** child 11's branch (`sc11-status-since-and-state-line`, its recorded `chantier/*`
  branch), the CR below in the stack. The stack also holds child 1 (`chantier push`, whose
  `push` event this child reads), child 3 (refusals name the next command) and child 9 (the
  AGENTS.md sentence "the CLI ... advises with `next` and its `next:` lines, and never decides a
  merge or a take-back").
- **Child 11's due count.** Child 11 puts a `state:` line on the steering session's told blocks
  (`src/hub/watch_lines.py`), with "the due count". Two cases:
  - If child 11's head already has a function that counts what is due, `next --epoch` is built on
    that function: one list, whose length is the count.
  - If not, this child adds `due()` (below) and points child 11's count at `len(due(...))`. That
    change touches the count only; the `state:` line's form stays as child 11 shipped it.

  Either way, a test asserts that the count equals the number of items `next --epoch` prints, on
  the same record.
- **What depends on it:**
  - child 13 (`msg steering`) builds on this branch;
  - child 14 (`judge`) switches one entry of the due list's wording to `judge <cr>` (open
    question 1);
  - child 16's retro draft names "`next:` line" as one rung of the M5 ladder;
  - children 19 to 24's cards say "`$CHANTIER next` says what is due" instead of listing
    the steps.

## Decisions carried

| Source | Decision | Here |
| --- | --- | --- |
| Answer 11 (simplify-cards-Q11) | `next` is advice for choosing a CR and for wording. Safety steps are refusals, not advice | "Must not"; every rail keeps its refusal |
| Answer 13 (Q15) | In direct mode the Chief of Staff gets the Foreman's tools, `next` among them | `next --epoch` serves the Chief of Staff as steering session; plain `next` points to it in direct mode |
| Answer 22, F7 / child 9 | The CLI advises with `next` and its `next:` lines, and never decides a merge or a take-back | "Must not"; the AGENTS.md line |
| Answer 22, F14 | `next` is split from `status --since` and its `state:` line | This child's scope, separate from child 11. Shared only: the due count |
| Answer 22, F20 | State the seconds added to `just test` | "Evidence" |
| Program "Rules for every child" | New command: a scenario step plus its coverage bullet. One AGENTS.md line per new tool, with its source. No card text edited. No version edited | "What changes", "Gates" |
| Program child 12, Risk | A wrong `next:` line misleads every run, so each line is a scenario check | "Scenario" |
| Answer 14 / merge rule (Q8) | Nothing merges while the owner sleeps. The child is presented as ready | "Gates" |

## What changes

### 1. The command `chantier next`

**Declaration.** New `src/declare/next.py`, registered in `src/cli.py`'s `_MODULES` (keep the
alphabetical place). It follows `src/declare/access.py`:

```python
s = add_command(sub, "next", "chantier.commands.next_advice:next_", HELP, BATCH_EPOCH)
s.add_argument("cr", nargs="?", help="the CR: its Driver's next step")
add_lease(s)  # optional; checked, never renewed
```

- `HELP`: "read-only advice: with `--epoch`, what the steering session has due; with `<cr>`,
  that CR's next step; with neither, the Chief of Staff's view. It records nothing, renews no
  lease and reads no forge".
- `--lease` and `--epoch` together are a usage error (exit 2):
  `next: --lease is a Driver's, --epoch the steering session's; give one`.
- `--lease` with no `<cr>` is a usage error too: `next --lease <n> needs the CR: next <cr>
  --lease <n>`.

**Handler.** New `src/commands/next_advice.py`, `next_(args) -> list[str]`. It reads only:
- `Repo.find(readonly=True)`, as `access` does;
- `read_batch`, `read_events` and `cr_events` from the record;
- the git reads listed under "Git reads" below.

It opens no `RenderedBatch` and takes no lock. It writes nothing: not to the record, the events,
the planning folder or the journal, and not even a STATUS file. It exits 0 whenever it prints
advice.

**The three forms.**

1. **`next --epoch N`: the steering session's due list.** The epoch is checked as
   `core/batch.py`'s `check_epoch` checks it, but on the record that `read_batch` returns, so
   nothing is written. Factor the comparison into one function that `check_epoch` and `next`
   both call; its text and exit 3 stay unchanged. With a stale epoch, `next` prints the same
   `stale Foreman: ... stop now` and exits 3.

   The output is one line per item, each starting `due: `, in this order (the program's order):
   1. **A free slot and the next CR to take.** Shown when `rails.slot_free(d)`, not
      `over_budget(d)`, and `status/words.py`'s `next_to_start(d)` names a CR:
      `due: a free slot (<held> of <slots> held): take <CR> (`take <CR> --epoch <N>`)`.
      In a stack batch, when `stacks.stack_due(d)` is not empty, also print, with
      `stack_line`'s facts:
      `due: take stack now: <ids> ready with a PR, no stack made yet (`take stack --epoch <N>`)`.
   2. **A CR handed back with no ask.** A CR whose status is `ready`, where no ask in
      `d.asks` (read or unread) with `rails_release.readiness_key(...) == ("cr", <CR>)` was sent
      after the `t` of the CR's last `handback ready` event (compare the ask's `sent`).
      - In a stack batch, a CR of `stacks.chain(d)` makes no per-CR item, because its readiness
        goes up with the stack's (`check_shape`). Instead there is one stack item: when every
        open CR of the chain (release and fix aside) is `ready`, and no ask with key
        `("stack", "")` was sent after the last of their hand-backs.
      - Line: `due: <CR> handed back <word>, no ask yet (`asks "<word> <CR> …" --epoch <N>`)`,
        where `<word>` is `stack_words.ready_word(d, c, repo)` (or `pr-in-draft`). The stack
        item uses `stack-ready-to-merge`. Open question 1 covers the command named here.
   3. **An order not done.** One item per `o` in `d.orders` with no `done`, worded as
      `batch_status_orders.order_lines` words its two groups:
      - pending: `due: order <O-k> <kind>[ <CR>][ <note[:40]>]: pending; do your part, then
        `order done <O-k> --epoch <N>``;
      - applied: `due: order <O-k> ... : the CLI applied it; `order done <O-k> --epoch <N>``.
   4. **A restack owed.** In a stack batch: an open CR of `chain(d)` that has a PR, whose last
      `ship` event is older than the latest `order` event with `order_kind == "merged"` of a CR
      below it in the chain. In other words, a merge moved the CR's base after its last ship.
      One item lists them all, worded as `orders_merged.restack_line` words its two cases (a
      stack driver recorded: send it `merged: <CR>`; none: one `take stack --epoch <N>`).
      Factor the wording so both print the same words.
   5. **A stale lease.** Each unit whose lease is `not confirmed` (`leases.not_confirmed`):
      - a working CR's lease;
      - the stack lease when `d.stack_agent` is set;
      - an open QA order's lease.

      Line: `due: <unit>: <not_confirmed text>; check with the host that its Driver ended, then
      `<leases.reclaim_command(unit, lease)>``. A **live** lease is never an item; reclaiming
      a live lease stays "only on the user's word", as `check_free` says.

   With no item, the output is exactly one line: `nothing due: wait`.

2. **`next <cr> [--lease N]`: the CR's next step.**
   - With `--lease`, the number is checked against `leases.lease_of(d, cr)` and nothing is
     renewed. A number that is not the CR's live or not-confirmed lease prints
     `leases.lost(...)`'s `claim lost: ... stop now` text and exits 3, as `round` would.
     The check reads only; no `claim` is made.
   - With `--epoch`, the epoch is checked as in form 1. This form serves the steering session
     reading one CR.
   - A CR that is not `working` gets one line, `next: ` plus the second sentence of
     `status/now_next.py`'s `now_next` (queued, blocked, held, parked, unheld, ready, merged,
     dropped). That sentence already names who acts.
   - A working CR of kind `release` gets the `Release` sentence of `now_next` (out of scope
     below).
   - A working CR gets the first step the table below finds undone.

3. **`next` with neither: the Chief of Staff's view.**
   - The unread asks: `asks to carry: <n> unread (`asks`)`, or `asks to carry: none`.
   - The ready CRs: the running batch's `handed back:` lines, exactly as `status` prints them
     (`status/ready_line.py`'s `ready_lines`, with `stopped_agents` as `status` computes it), or
     `ready: none`.
   - `hub/autostart.py`'s `not_running_line(repo)` when the session's watcher is not running.
   - In a batch steered `direct`, one more line:
     `direct mode: you steer: `next --epoch <n>` for what is due`.
   - With no running batch: `no running batch`, then the watcher line if any.

**Git reads** (read-only; AGENTS.md's "The rest of the CLI keeps no git write" holds). Form 2
and the Driver's `next:` lines read the worktree with the same calls the rails already make:
- `git rev-parse HEAD` and `git status --porcelain --untracked-files=normal` in the CR's
  worktree, as `verdict` and `handback_refusals` do;
- `git rev-parse --verify --quiet <remote>/<branch>`, as `handback_refusals` does. This reads the
  local remote-tracking ref, with no fetch and no network.

Keep these reads behind one small reader that returns the facts (head, dirty, pushed head). The
step logic then takes the record, the events and those facts, so its tests need no git.

### 2. The Driver's step table

New `src/core/driver_steps.py`, beside `src/core/phases.py`, with the same intent: light, importable
by the parser, data only. It holds `DRIVER_STEPS`, the ordered steps with each one's command
template:

| Step | Done when (read from the record, the events, the facts) | `next:` text (`<CR>`, `<n>`, `<h>` = head's 7 characters, `<pr>` filled) |
| --- | --- | --- |
| `round` | `c.round >= 1` | `` `round <CR> --lease <n>` before the round's Coder `` |
| (in the round) | the last `round` event's `wt_head` differs from HEAD, or an event other than `round`/`note`/`phase` follows it | `the round's Coder, then its reviews; commit in <worktree>; then the long gate (`gate <CR> <name> --lease <n>`)` |
| (dirty) | the worktree is clean | `commit the worktree's changes: a gate, a push and a verdict bind to a commit` |
| `gate` | `heads.gate_passed(events, HEAD)`, or `carry_at(events, HEAD, "gate_from")`, or `stacks.waived_gate(d, c)` | Not run at HEAD: `the long gate at <h>: `gate <CR> <name> --lease <n>`, or `--no-gate "<the project's rule>"` on the hand-back when the project's rules exempt <CR>`. Failed at HEAD: `the long gate failed at <h>: fix it in a new round (`round <CR> --lease <n>`)` |
| `push` | the remote-tracking `<remote>/<branch>` is at HEAD | `` `push <CR> --lease <n>` (<remote>/<branch> is at <x> / not pushed) `` |
| `ship` | `c.pr` is set and `same_head(c.head, HEAD)` | No PR: `open the PR, then `ship <CR> <pr link> --lease <n>``. Else: `` `ship <CR> <pr> --lease <n>` `` |
| `ci` | `c.phase == "verifier"`, or any `verdict` event at HEAD | `CI on <pr> at <h>: green, start the Verifier at <h>; red, a new round (`round <CR> --lease <n>`)` |
| `verdict` | `last_verdict(events, HEAD) == "VERIFIED"`, or `carry_at(events, HEAD, "verdict_from")` | Waiting: `the Verifier's `verdict <CR> VERIFIED` (or "NOT VERIFIED") at <h>, with work/verify.md's Head: line`. NOT VERIFIED at HEAD: `verdict NOT VERIFIED at <h>: a new round (`round <CR> --lease <n>`)` |
| `handback` | the CR is no longer `working` | `` `handback <CR> ready <pr> --lease <n>`, then send its line to <the Foreman / the Chief of Staff> `` |

- `<name>` is the long gate's name from the code repository's `chantier.yaml`
  (`long_gate.commands`, read as `commands/gate.py`'s `_long_gate` reads it):
  - with one name, that name;
  - with several, `<name>` followed by `(named: a, b)`;
  - with none, the gate row says `chantier.yaml names no long gate: the hand-back takes
    --no-gate "<the project's rule>"` and counts as done.
- `<n>` is the CR's own lease number, `c.lease.n`. "Foreman" or "Chief of Staff" follows
  `d.steering`.
- The table rows are data. The function that walks them, `driver_step(d, c, events, facts) ->
  str`, goes in a new `src/status/advice.py`, beside `now_next.py`. That module also holds
  `due(repo, d, epoch) -> list[str]`, `chief_view(repo) -> list[str]` and `next_line(...)`.
- The step logic agrees with the refusals it stands before. The gate, push, ship and verdict tests
  are the ones `handback_refusals` and `ship` apply (`gate_passed`, `carry_at`, `waived_gate`,
  `last_verdict`, the remote ref). A test checks that a record which `next <cr>` calls
  "handback" is one that `handback_refusals` accepts.

### 3. The `next:` lines

`next_line(...)` in `src/status/advice.py` returns one line, `next: <text>`, from the same
`driver_step` or `due` the command uses. It is appended at the end of the successful output of:

| Command | Handler | Text |
| --- | --- | --- |
| `round` | `commands/driver.py`, `round_` | `driver_step` of the CR, after the record |
| `gate` (the run form only; not `--first`, not `--stop`) | `commands/gate.py`, `_finish` and `_finish_stopped`'s caller in `gate` | `driver_step` after the gate's events, on pass and on FAIL (the FAIL line says "a new round"); exit codes unchanged |
| `push` | child 1's `src/commands/push.py` | `driver_step` after the `push` event |
| `ship` | `commands/delivery.py`, `ship` | `driver_step` after the `ship` event (a missing gate shows as the gate step, beside ship's `off:` line) |
| `verdict` | `commands/delivery.py`, `verdict` | `driver_step` after the `verdict` event |
| `handback` | `commands/driver.py`, `handback` | the `handback` row: `send the hand-back line above to <the Foreman / the Chief of Staff>; nothing else is due from you` (ready or blocked) |
| `order merged` | `commands/orders.py`, `_ordered` | the first `due` item (or `nothing due: wait`), followed by ` (+<k> more: `next --epoch <N>`)` when there are more |
| `order done` | `commands/orders.py`, `_order_done` | same as `order merged` |

Rules:
- **Order commands.** For `order merged` and `order done`, the line is printed only to the
  steering session: when `--epoch` is given, or when `d.steering == "direct"`. A Chief of
  Staff's `order merged` in a Foreman-steered batch gets no `next:` line, because the due list
  is the Foreman's.
- **At most one `next:` line per output.** When the output already holds one (an
  `order merged` that ends the batch prints `commands/endpause.py`'s `next: the retro ...`),
  `next_line` adds none.
- **Refusals stay as they are.** A refusal (a `ChantierError`) prints no `next:` line. Child 3
  already makes each refusal name its next command.
- **The four existing `next:` lines are not touched.** These are `commands/endpause.py:47`,
  `commands/opening.py:277` and `:333`, and `rails_release.py:215`, the last inside a refusal.
  They keep their text, byte for byte.
- **Placement.** The line comes after every existing line of the output, so tests that read a
  line by position from the top keep passing. Tests that compare a whole output list gain the
  one line.

### 4. AGENTS.md

Add one paragraph to the named exceptions of the "The CLI's scope" bullet, right after the
`access` paragraph:

```
  `next`: read-only advice: the steering session's due list (`next --epoch`), a CR's next step
  (`next <cr> --lease`) and the Chief of Staff's view (plain `next`), and the one `next:` line
  that `round`, `gate`, `push`, `ship`, `verdict`, `handback`, `order merged` and `order done`
  print from the same function; it records nothing, renews no lease, reads no forge, and never
  decides a merge or a take-back (a safety step stays a refusal); built on the user's answer
  simplify-cards-Q11 and on study-behaviour 3.5 (the Foreman's heartbeat, 37 to 64 % of its
  weighted tokens), its measured cost.
```

No other AGENTS.md line changes. Child 9's sentences already name `next`.

### 5. Scenario

- New case `next_advice(w)` in `scenario/run_scenario.py`, added to `CASES` and to the
  `parallel` unit's list in `UNITS`. Raise that unit's budget literal by the measured seconds.
  It runs:
  - **`next --epoch` at three moments of one batch:**
    1. just after `open` with queued CRs and free slots: the line names
       `take <first CR> --epoch <n>`;
    2. with every slot held and nothing else due: exactly `nothing due: wait`;
    3. after a hand-back ready with no ask, plus a pending order: both items, in the order above.
       Then, after the ask and `order done`, only what is left.
  - **A scripted Driver that follows the `next:` lines.** One CR goes from `take` to
    `handback`, and at each step the Driver runs only what the last `next:` line names. The
    step's command word is mapped to the scenario's existing helpers (`round` -> `w.chantier
    ("round", ...)`, then `commit`; `gate` -> `w.chantier("gate", cr, GATE_NAME)`; `push` ->
    child 1's `chantier push`; `ship` -> `open_pr` and `w.chantier("ship", ...)`; `ci` ->
    `phase <cr> verifier`; `verdict` -> `w.verified`; `handback` -> `w.ready`). Checks:
    - each command's `next:` line equals what `next <cr> --lease <n>` prints at that moment;
    - the sequence of steps is round, (in the round), gate, push, ship, ci, verdict, handback;
    - the CR ends `ready`, reached with no refusal.
  - **One stale lease** (with `CHANTIER_LEASE_TEST_TTL`, as `lease_cases` does):
    `next --epoch` names `take <CR> --reclaim ...`, and a live lease is never named.
  - **Read-only:** `batch.json` and `events.jsonl` keep the same bytes across every `next` run.
  - **In a stack** (in the `stack` unit's `stack_batch`, one added check): after `order merged`
    of the bottom CR, `next --epoch` holds the restack item.
- `scenario/README.md`, "## Coverage": one bullet for `next` and the `next:` lines, ending
  `(unit: parallel)` and naming the pytest file, as `tests/test_scenario_coverage.py` requires.

## Out of scope

- Anything that writes, renews or decides. `next` never runs `take`, `asks`, `order` or `judge`
  itself. It never renews a lease and never clears a recorded Driver (F12).
- The forge. `next` does not read CI, a PR's state or a merge. The `ci` step only says what to
  read, because a new forge read would need its own AGENTS.md exception.
- `next stack` and the stack driver's or a QA driver's steps. The release CR's steps, which
  print `now_next`'s Release sentence.
- Parked or unheld CRs to take back, and a Driver ended with no hand-back recorded. These are not
  among the program's five due kinds: the take-back is the steering session's choice, and
  `status` keeps showing them. See open question 2.
- `judge` (child 14), `msg steering` (child 13), `status --since` and the `state:` line's form
  (child 11).
- Rewording the four existing `next:` lines, or any refusal.
- Any card, `SKILL.md` or wrapper text. No child before 19 edits one.
- The hook (`hooks/`), so `just mod` is not owed.
- A journal type, so `hub/schemas.json` does not change.
- A version change.

## Must not

- Record anything. The tests prove that the record and the events keep the same bytes.
- Take the place of a safety step. Every rail keeps its refusal, and `next` only names it.
- Decide a merge or a take-back. Due items name a command to run, worded as the record shows it.
  Reclaiming a live lease is never advised.

## Gates

- **Before the first push:** `just check` in the worktree, at the rebased head it pushes. Also
  `just eval-dry-run`, because the change is under `src/`.
- **Long gate:** owed (the CLI and the scenario change). `just scenario (ubuntu-latest)` must be
  green at the PR's head. In this stack only the CR on top owes the local Windows run
  (`chantier gate <cr> scenario`). If this CR is the top when presented ready, it owes that run;
  when child 13 joins on top, the run moves there.
- **Merge:** nothing merges while the owner sleeps. The CR is presented as ready, and the owner
  merges, in order, after child 11.

## Evidence

- **Pytest** (`tests/test_next_advice.py`). It uses prepared records, built with
  `BatchRecord`, `CrEntry` and `EventRecord` and a `SimpleNamespace` repo, as
  `tests/test_ready_line.py` does. The pure functions get injected facts and need no git.
  - `due` is parametrized over one record per due kind:
    - free slot and next CR;
    - `take stack` due;
    - handed back with no ask, in parallel and as a stack item;
    - an ask sent after the hand-back clears it;
    - pending and applied orders;
    - restack owed after a chain merge, cleared by a later `ship`;
    - a not-confirmed lease of a CR, of the stack and of a QA order;
    - a live lease that gives no item;
    - nothing due.

    Each case asserts the exact line and the order of the items.
  - `driver_step` is parametrized over each row of the table: no round; in the round; dirty;
    gate not run; gate failed; gate carried; gate waived; no gate named; not pushed; pushed at
    another head; no PR; PR at an old head; CI; Verifier; NOT VERIFIED; handback. Plus the
    non-working states through `now_next`.
  - Agreement: on the record where `driver_step` returns the handback row, the same checks as
    `handback_refusals` (gate, verdict, remote ref, head) find nothing missing.
  - In-process CLI (the `chantier` fixture on the `repo` fixture), few cases:
    - `next --epoch` with a stale epoch exits 3 with the `stale Foreman` text;
    - `--lease` with `--epoch` exits 2;
    - `next <cr> --lease <old>` exits 3 with `claim lost`;
    - `batch.json` and `events.jsonl` keep the same bytes after each form;
    - `round` and `handback` end with the `next:` line that `next <cr>` gives;
    - an `order done --epoch` ends with the first due item;
    - a Chief of Staff's `order merged` in a Foreman batch prints no `next:` line;
    - an `order merged` that ends the batch prints exactly one `next:` line (endpause's).
  - Child 11's due count equals `len(due(...))` on two records.
  - Tests that compare a whole output of the eight commands are updated with the one line, and
    with nothing else.
- **Scenario:** the `next_advice` case and the stack check above, green in `just scenario`.
- **`just test` seconds (F20).** The PR's Deliverables state the before and after durations of
  `just test` on the same machine, and the difference. Expected: about +2 s (pure parametrized
  cases, under 0.5 s; about eight in-process CLI cases on the `repo` fixture).
- **AGENTS.md:** the diff shows the one paragraph above.
- **No host or default matrix.** The advice does not depend on the host. The one configured value
  it reads, `long_gate.commands`, has its three cases (one name, several, none) in the pytest
  rows.

## Cost

`just test`: about +2 s. Scenario: one case in `parallel`, about 20 to 40 s, measured and written
into the unit's budget literal. One Driver round, two at most.

## Open questions

1. **The no-ask item names a command that does not exist yet.** The program words the item as
   "`judge <cr>`", but `judge` only lands in child 14, two CRs above this one. Children 1 to 18
   may each merge in order, so a `main` with this child and without child 14 would advise a
   command that is not there. This specification has child 12 print the existing route,
   `asks "<word> <CR> …" --epoch <N>`, and leaves child 14 to switch that one entry to
   `judge <CR> --epoch <N>`, which adds one line to child 14's scope. Should child 12 print
   `judge <CR>` from the start instead, as the program words it?
2. **CRs to take back.** These are a parked CR whose wait has cleared, and a CR the user
   unheld. Neither is among the program's five due kinds, so with nothing else due,
   `next --epoch` prints `nothing due: wait` while such a CR sits there. Taking a CR back stays
   the steering session's choice either way. Should `next --epoch` list each one as a plain fact
   line with no command (for example `due: <CR> parked, its wait cleared: taking it back is
   yours`), or leave them to `status` and the watcher's wake, as specified here?
3. **"Ready CRs" in the Chief of Staff's view.** This specification reads it as the running
   batch's CRs handed back ready, the `handed back:` lines. Should the view also count the
   planning folder's `3-ready/` CRs, which wait for a batch?


---

# PART 3 of 3: SC13: A Driver messages the steering session through the board

Child 13 of 28 of the program CR `simplify-cards-and-prompts`. The program's `03-change-spec.md`,
"Child 13", and its `02-answers.md` (answers 4, 13 and 17 to 22) rank above this file. One Driver
and one PR, in the running stack batch (batch-31). Code read: `origin/main` at `8a960d34`. Short
forms used below:

- `src/` is `skills/chantier/scripts/cli/src/chantier/`;
- `tests/` is `skills/chantier/scripts/cli/tests/`;
- `scenario/` is the repository's root `scenario/` folder.

## Goal

The owner's words (answers 1, 4 and 18): agents message the steering session through the board
instead of waking it. A Driver that hits an anomaly or a blocker during its run tells the Foreman
(or the Chief of Staff in a direct batch) at once, through the project's journal and the steering
session's own watcher. It no longer waits for its hand-back or relies on the host's means. Only
`anomaly` and `blocked` wake the steering session. A `note` waits for its next wake.

This child only adds things: two commands, one journal type, and one more type the Foreman's
watcher reads. No card text changes (program rule: no child before 19 edits a card). Every
intermediate `main` keeps working with the old cards, which do not yet name `msg` or `inbox`.

## Place in the chain

- **Base:** child 12's branch (`sc12-next-advice`), the previous CR of the stack. Children 1 to 12
  are below it.
- **What it uses from below:**
  - nothing of child 12's code;
  - child 8's `chantier host`, named in the not-delivered line (the host's means of reaching the
    steering session);
  - child 3's rule that a refusal names the next command, followed by every refusal added here.
    Child 3's gate scans only `rails.py`, `rails_release.py`, `rails_idle.py` and
    `core/leases.py`, so the new refusals are not in its scan.
- **Shared files with neighbours:** `src/cli.py` (`_MODULES`, `FULL_OUTPUT`), `AGENTS.md`, and
  `scenario/README.md`'s coverage list. Each child adds its own lines there. Rebase conflicts are
  line-level only.
- **What depends on it:**
  - child 14 (`judge-asks`) sits on top of it;
  - children 20 (Drivers' cards) and 21 (Foreman's card) write the new cards' lines for `msg` and
    `inbox`;
  - child 25's review checks that the old "a Driver tells its steering session" rules are found
    again through these commands;
  - child 28 measures `msg` deliveries in a real run.

## Decisions carried

| Source | Decision | Where |
| --- | --- | --- |
| Answer 4 (simplify-cards-Q7) | `msg` and `inbox` exist. Only `anomaly` and `blocked` wake the steering session. Notes wait for its next wake | sections 1, 3, 4 |
| Answer 13 (simplify-cards-Q15) | In direct mode the Chief of Staff gets the Foreman's tools, so it is the steering session that `msg` targets and that runs `inbox` | sections 1, 4 |
| Answer 22, F8 | `msg steering` only. With no watcher subscribed it prints `not delivered: no watcher subscribed` and exits non-zero. No `user` or `cr:` targets | section 1 |
| Program, Child 13 | One `msg@1` line per message, through the one append function. Schema in `src/hub/schemas.py` and `hub/schemas.json`. Delivery by the `events` topic and the steering session's watcher. The Foreman's watcher's delivery is unproved, and child 28 measures it | sections 2, 3 |
| Program, Must not | The board and the server send nothing to an agent themselves. No message crosses projects. `note <cr>` is not replaced | sections 1, 6 |
| Program, Out of scope | The surface server's protocol and the board's pages do not change, except the `msg@1` type and its delivery on `events` | section 1 (subscription read) |
| Program rules | New command: a scenario step and a coverage bullet. New journal type: `just journal-schemas`. New tool: an AGENTS.md line with its source. The added `just test` seconds stated. Long gate owed. No version edit | sections 5 to 8, "Gates and evidence" |
| Program rules (F17) | A claim not proved here is marked "unproved" in the specification and the PR | "Risk" |

## What changes

### 1. The command `chantier msg` (new `src/declare/msg.py`, handler in new `src/commands/msg.py`)

**Form:**

```
chantier msg steering <kind> <text...> --cr <CR-id|stack> --lease N [--batch B]
```

- `steering` is the only target, a positional with `choices=["steering"]`. There is no `user`
  target and no `cr:<id>` target (F8). Any other word exits 1 through argparse, which names the
  choice.
- `<kind>` is one of `anomaly`, `blocked`, `note` (`choices=`).
- `<text...>` is `nargs="+"`, joined with one space and stripped. It is refused, with exit 1 and
  nothing written, when:
  - it is empty;
  - it holds a newline (`text is one line: write it again on one line`);
  - it is longer than 300 characters. The constant is `TEXT_MAX = 300`, as in
    `hub/journal_add.py`. The message reads `text is at most 300 characters (got <n>): shorten it`.
- `--cr` is required. It is the unit whose lease the Driver holds: a CR id, normalized with
  `core.ids.normalize_cr`, or `stack` for the stack driver.
  - **Why `--cr` is added to the program's form:** a lease number alone does not name a unit.
    Numbers are per unit (`core/leases.py`, `start`: "the unit's last number plus one"), so
    `--lease 1` matches every CR's first lease.
  - It is a flag, so the program's positional form `msg steering <kind> <text>` stays as written.
- `--lease N` is required, through `add_lease(s, required=True)` (`commands/registry.py`).
- `--batch` comes from scope `BATCH` (`add_command(..., BATCH)`). It defaults to
  `$CHANTIER_BATCH`, else the only running batch. There is no `--epoch`: this is a Driver's
  command, not a steering one.

**What it does, in this order.** The two steps are not nested, because both take the planning
folder's lifecycle lock (`lifecycle.stages.changes_lock`, the store's lock). Do not call
`journal.append` inside the `RenderedBatch` block.

1. **The record.** It opens `RenderedBatch(repo, find_cr_batch(repo, unit, args.batch),
   actor="driver")` (for `stack`, the batch resolved as `resolve_batch` does). Inside the block:
   - The batch must be `running` or `paused`. Otherwise it exits 2:
     `msg: <batch> is <status>: no steering session to message; hand back instead`.
   - It runs `leases.claim(b, unit, args.lease, what=f"msg {unit}", required=True)`. A stale or
     ended lease exits 3 with the existing `claim lost: ...; stop now: nothing recorded`, and no
     journal line is written. A valid lease is renewed.
   - It logs `b.log("msg", unit, kind=kind, note=text)`. This event saves the renewal, as every
     Driver command's event does, and keeps the message in the CR's log (`chantier log <cr>`).
   - It reads the **steering session's key** and the **steering word**:
     - In a batch whose `steering` is `"direct"`, the word is `direct` (the Chief of Staff steers
       it). The key is `autostart.kept(d.foreman_transcript or d.chief_transcript)`. In direct
       mode the Chief of Staff's transcript is the recorded Foreman transcript (`commands/seat.py`,
       `_transcript`).
     - In any other batch, the word is `foreman`. The key is
       `autostart.kept(d.foreman_transcript)`.
     - An empty key means no steering session ever recorded its transcript.
2. **The journal.** After the block closes, it appends one event with
   `journal.append(repo, [event], "cli")`, the one writer path. `"cli"` is already in
   `journal.SOURCES`. The event is:

   ```
   {"type": "msg@1", "audience": [<audience>], "batch": <id>, "unit": <unit>, "kind": <kind>,
    "text": <text>, "wakes": <kind in ("anomaly", "blocked")>, "steering": <"foreman"|"direct">}
   ```

   The audience is `session:<key>` when the key is known, else `role:steering`.
   - **Why `session:<key>`:** a watcher's subscription already holds its own `session:<key>`
     (`hub/watch_reads.py`, `subscription`). So the line is for the steering session's watcher
     alone, and never for the Chief of Staff's watcher of a batch that has a Foreman (whose
     subscription is `project` plus its own session).
   - **Why `role:steering` with no key:** the line is still kept for `inbox`, but no watcher
     subscribes to that value. The audience is never `project`.
   - The journal is the project's own `forge-journal.jsonl`, so a message never crosses projects
     (Must not).
3. **The delivery check.** It reads the same steering key. The message counts as **delivered**
   when all three hold:
   - the key is known;
   - the key is in `hub.lock.watchers(repo.git_dir, project_name(repo))`, the held watcher locks
     `chantier/watch-<project>/<session>.lock`;
   - `hub.state.live_entry(repo.git_dir, state.SERVER)` is not None: a surface server runs, so
     its `events` topic carries the line.

   **Why there is no read of the server's subscriptions:** the server publishes no per-session
   list of its subscriptions, and adding one would change its protocol, which the program keeps
   out of scope. A watcher takes its lock before it links (`hub/watch.py`, `Watch.start`). A
   Foreman's watcher with no server ends at once (`FOREMAN_NO_SERVER`). The one case the server
   check catches is a Chief of Staff's watcher that holds its lock while it waits for a board
   (`NO_BOARD`).

**Output.**

- **Delivered:** one line, exit 0:
  - `msg: seq <n> <kind> from <unit> to the Foreman (batch-31): delivered to its watcher`;
  - for a `note`, the line ends with `delivered to its watcher, told at its next wake`;
  - in a direct batch, the line says `to the Chief of Staff (direct)`.
- **Not delivered:** the line is still appended, and the command exits 2 (`EXIT_PRECONDITION`)
  with two lines. The handler returns `(lines, 2)`, as `watch_cmd.watch` returns a code:
  1. `msg: seq <n> <kind> from <unit> to the Foreman (batch-31)`
  2. `not delivered: no watcher subscribed; the steering session reads it with inbox; reach it by
     your host's means (chantier host) or hand back`

  The second line starts with the program's exact words, `not delivered: no watcher subscribed`.

`msg` never writes in the CR's folder, never messages a session itself and never touches the
server. It replaces nothing: `note <cr>` stays the line in the CR's record shown in its
`STATUS.md` (Must not).

### 2. The journal type `msg@1` (`src/hub/schemas.py`, `hub/schemas.json`)

- **Model:**

  ```python
  class Msg1(Payload):
      batch: str
      unit: str
      kind: str
      text: str
      wakes: bool
      steering: str
  ```

  `unit`, `kind` and `steering` are plain strings. This follows the module's rule that open sets
  are plain strings: a later unit kind (a QA order `O-k`) or message kind would otherwise need a
  `msg@2`. The command's own `choices` close the sets today, as `journal_add.IssueInput` does for
  `issue@1`.
- **Text:** `msg_text(e)`, the sentence a watcher, the pull path and the server's `events`
  answer tell:

  ```
  message from <unit>'s Driver (<kind>, seq <seq>): "<text>"; for the steering session: act on
  it, then inbox --read <seq> --epoch <n>
  ```

  It is one line in the code. `<n>` is literal, as in `wait_cleared_text`.
- **Entry in `PUBLISHED`:** `"msg@1": Entry(Msg1, "wakes", msg_text, None, <example>)`.
  - The wake rule is the payload's `wakes` field, as for `board@1` and `issue@1`.
  - The key is `None`: each line is its own event, so two identical messages are two lines.
  - The example: `{"batch": "batch-29", "unit": "CR-12", "kind": "blocked", "text": "the base
    branch moved under the stack", "wakes": True, "steering": "foreman"}`.
- **`hub/schemas.json`** is regenerated with `just journal-schemas`, never by hand.
- **Docstrings:** `schemas.py`'s module docstring and `hub/journal.py`'s docstring name `msg@1`
  among the published types and the `cli` source's writer (`chantier msg`). Replace "`"cli"` is
  room for a command" with the `msg` command.

### 3. Delivery: the watchers (`src/hub/watch_lines.py`, `src/hub/watch.py`)

- **`FOREMAN_TYPES`** gains `"msg@1"`. `watch_reads.foreman_lines` already filters on the type and
  on `e["batch"] == batch`. So the Foreman's watcher reads its own batch's messages and no other
  batch's. Update the comment ("the lines the Foreman acts on") and `watch.py`'s module docstring
  ("merge, red-CI, wait-met and message lines").
- **The Chief of Staff's watcher** (direct mode) needs no code change. It reads every line whose
  audience holds `project` or its own `session:<key>`. Before this child the `watch_reads.py`
  docstring named only the three forge types; the read is generic.
- **Wake:**
  - `journal.waking` already reads the `wakes` field, so `anomaly` and `blocked` start or extend
    the watcher's wait, and the watcher tells its block 20 s after the last such line
    (`hub_times.quiet_s()`).
  - A `note` (`wakes: false`) is gathered in `Watch.events` and moves the cursor. It is told only
    in the next block that something else wakes, or in the watcher's end lines. That is the
    "next told block" of the program.
- **The pull path** (`watch --once --after SEQ`) and the server's `events` topic need no change.
  The topic serves every journal line with its type's `text` (`board/api/topics.py`, `_events`
  and `_told`).
- **`status`** does not list `msg@1` lines. `journal.lines` keeps its three kinds.

### 4. The command `chantier inbox` (declared in `src/declare/msg.py`, handler in `src/commands/msg.py`)

**Form:**

```
chantier inbox [--read <seq>|all] --epoch N [--batch B]
```

- The scope is `BATCH_EPOCH`. `require_epoch(args.epoch, "inbox --epoch <n>")` runs first, then
  `check_epoch(b, args.epoch)` inside the `RenderedBatch` block. A stale steering session exits 3,
  as every steering command does. In direct mode the Chief of Staff runs it with its own number,
  as it runs the Foreman's other commands (answer 13).
- **Messages of the batch:** the journal's `msg@1` lines, read by `journal.read`, that are
  `journal.listed` and whose `batch` is the batch's id, whatever their audience. A message sent
  while the batch had another steering session, or no recorded key, is still in the inbox.
- **Read marks:** the batch's own log. `inbox --read` logs `b.log("inbox-read", None, seqs=[...])`
  in the batch's `events.jsonl`. A message is read when its `seq` is in the `seqs` of any
  `inbox-read` event of the batch. The journal is append-only and never rewritten
  (`hub/journal.py`), so the marks cannot live there.
- **Plain `inbox`:** one line per unread message, oldest first:
  `#<seq> <HH:MM> <unit> <kind>: "<text>"`, time in UTC from the line's `t`. Then one closing
  line:
  - `inbox: <k> unread; once handled: inbox --read <seq>|all --epoch <n>`;
  - or, with none, `inbox: nothing unread`.
  It records nothing.
- **`--read <seq>`:**
  - It marks that message read and prints `inbox: #<seq> read; <k> unread`.
  - An integer that is not a `msg@1` seq of this batch exits 1:
    `inbox: #<seq> is no message of <batch>; inbox --epoch <n> lists them`.
  - An already-read seq prints `inbox: #<seq> already read` and logs nothing.
  - A word that is neither an integer nor `all` exits 1, through the argument check.
- **`--read all`:** marks every unread message of the batch read, in one `inbox-read` event, and
  prints `inbox: <k> read; nothing unread`.
- **`FULL_OUTPUT`:** `inbox` is added to the set in `src/cli.py`. A list of messages is useless
  cut at `MAX_LINES` (10).

### 5. Registration (`src/cli.py`)

- `from chantier.declare import msg`, and `msg` added to `_MODULES`.
- `src/declare/msg.py` declares both commands, so the handlers load lazily.
- The help strings:
  - `msg`: "a Driver tells the batch's steering session (the Foreman, or the Chief of Staff in
    direct mode) through its watcher: anomaly and blocked wake it, a note waits for its next wake".
  - `inbox`: "the steering session's unread messages from the batch's Drivers; --read marks them
    read".
- A profile's `cli.run` runs both, like any command not in its refused list. No change there.

### 6. Docs

- `docs/planning-folder.md`, the journal section:
  - the `type` row's list gains `msg@1`;
  - the `source` row says `cli` is `chantier msg` (and `file` and `triage`, which already write
    `arrived@1` with source `cli`);
  - the sentence "Every line written today is for `["project"]` ... routes to no role, CR or user
    yet" becomes: every line is for `["project"]` except `msg@1`, which is for the batch's
    steering session (`session:<key>`, or `role:steering` when no steering session recorded its
    transcript);
  - the type table gains the row: `` | `msg@1` | a Driver, through `chantier msg steering` | when `wakes`: true for `anomaly` and `blocked` | ``.
- `docs/server-api.md`: no change. The `events` row already serves every line with its `text`.
- The board's pages and protocol: no change. The board shows a `msg@1` line wherever it shows
  journal lines, and sends nothing to an agent (Must not).

### 7. Tests: new `tests/test_msg_steering.py`, few and parametrized

They call the CLI in-process (`conftest.Chantier`), on a prepared batch (`batch_helpers`), with
`watch_fakes.FakeBoard` and `served`, as in `tests/test_watch_foreman.py`. No test sleeps.

1. **Schema round trip.** `msg@1` is in `PUBLISHED` and in the shipped `hub/schemas.json`.
   - The parametrized tests of `tests/test_event_types.py` cover the append, the refusal of an
     extra or a missing field, and the duplicate rule, once the entry exists. They read the
     shipped file as it ships at the head.
   - The new file adds one case: the line `msg` appends reads back through `journal.read` with
     `type == "msg@1"`, `source == "cli"`, the audience `["session:<key>"]` and the payload
     intact.
2. **Wake by kind,** parametrized over `anomaly`, `blocked` and `note`. A `msg steering <kind>` on
   a running batch whose `foreman_transcript` is `fm-1`, with the Foreman's `Watch` polled on the
   fake clock:
   - `anomaly` and `blocked` give an `EVENTS` block whose first line is `msg_text` of the line;
   - `note` alone gives no block within twice `quiet_s()`;
   - the same `note`, then a `merged@1` of the batch, gives one block holding both lines, the note
     first (the next told block).
   - A `msg@1` of another batch is not told.
   - The Chief of Staff's watcher (key `cos-1`, the seat its own) does not tell the Foreman's
     message.
3. **Direct mode.** In a batch with `steering: "direct"` and the Chief of Staff's transcript as
   the Foreman transcript, the message's audience is the Chief of Staff's session, and its plain
   watcher tells a `blocked` message.
4. **No subscriber,** parametrized over three cases:
   - no watcher lock held;
   - a lock held but no live server (`server.json` with no live `server` entry);
   - no steering key recorded (audience `role:steering`).

   In each case `msg` exits 2. Its output holds the line starting
   `not delivered: no watcher subscribed`, and the journal still holds the line.
5. **`inbox`:**
   - two messages are listed unread;
   - `--read <first seq>` leaves one, and a second `--read` of it prints `already read`;
   - `--read all` leaves none;
   - an unknown seq exits 1;
   - a missing `--epoch` exits 2, and a stale one exits 3;
   - the marks are `inbox-read` events in the batch's `events.jsonl`, and the journal file is
     byte-identical before and after.
6. **Refusals of `msg`** (one parametrized test):
   - a newline in the text, or a text over 300 characters: exit 1;
   - a stale lease: exit 3;
   - a closed batch: exit 2.

   In each case the journal is unchanged.

**`just test` seconds:** an estimate of +1 to +2 s, 6 test functions on in-process calls with
no sleep. The Driver measures `just test` before and after on the same machine and states both
figures in the PR's Deliverables (F20).

### 8. Scenario (`scenario/run_scenario.py`, `scenario/README.md`)

In the `forge_hub` case (unit `surface-board`), section 13, "the Foreman's watcher (CR-479)":

- **After the first `forge saw merged` block** of the Foreman's watcher `wf`:
  - A Driver's call for `f2`, under another session id
    (`env={"CLAUDE_CODE_SESSION_ID": "uuid-driver"}`):
    `msg steering blocked the fake base moved --cr <f2> --lease 1 --batch <c_batch>`. `f2` was
    set working with no lease, so `leases.claim` accepts any number.
  - Check: it exits 0 and prints `delivered to its watcher`; `block(wf)` returns the `message
    from <f2>'s Driver (blocked, ...)` line, then the `told up to cursor` line; and `wf` stays
    alive.
  - A `msg steering note ...` gives no block within the quick quiet window.
  - The Foreman's `inbox --epoch 1` lists both messages.
  - `inbox --read all --epoch 1` then prints `nothing unread`.
- **After the last check of the section** ("a record naming another Foreman ends it"), with no
  watcher of `uuid-fm-2` running:
  - `msg steering anomaly ...` exits 2;
  - its output holds `not delivered: no watcher subscribed`;
  - `journal("third")`'s last line is a `msg@1` with the audience `["session:uuid-fm-2"]`.

The README's Foreman's-watcher bullet gains these steps, with `(unit: surface-board)` and
`(test: test_msg_steering.py::<the wake test>, test_msg_steering.py::<the no-subscriber test>)`.
`tests/test_scenario_coverage.py` checks that both names exist. The `surface-board` unit's budget
(735 s) holds: the steps add a few seconds, on the 1-second hub and quick times already in use.

### 9. AGENTS.md

Two edits, sourced to the user's answers (program rule "AGENTS.md lines"):

1. In the watcher sentence ("each session's watcher ... subscribes to the surface server's
   `events` topic for its project (the hub's lines, the board's, the writer's and an outside
   poller's `issue@1` lines)"), add: "and a Driver's `msg@1` lines, each addressed to the batch's
   steering session's own watcher".
2. A named-exception paragraph after `journal add`'s:

   > `msg` and `inbox`: a Driver's `msg steering <kind> <text> --cr <unit> --lease <n>` appends
   > one `msg@1` line to the project's journal through the one append function, addressed to the
   > batch's steering session (its Foreman, or the Chief of Staff in direct mode), whose watcher
   > wakes on `anomaly` and `blocked` and tells a `note` at its next block; with no watcher of
   > that session subscribed (its watcher lock and a live surface server), it still appends the
   > line, prints `not delivered: no watcher subscribed` and exits non-zero; `inbox` lists the
   > batch's unread messages for the steering session and records the ones read in the batch's
   > events; no message goes to the user, to a CR or to another project, and the board and the
   > server send nothing to an agent; built on the user's answers simplify-cards-Q7 and Q22 (F8),
   > with no measured cost.

The rule "every journal line ... goes through the one append function" already covers `msg@1`.
The CLI writes only in the planning folder (`forge-journal.jsonl`, the batch's `events.jsonl`), so
the write list is unchanged. The four role sentences are child 9's.

## Out of scope

- A `user` target, a `cr:<id>` target, a message from the steering session to a Driver, or any
  other target (F8).
- A message across projects, or to another project's seat.
- Any change to the surface server's protocol, ops or topics, or to the board's pages. There is
  no server-side subscription list (section 1).
- Listing unread messages in `status`, in `next --epoch` (child 12's due list) or on the board.
  Child 28's measure tells whether a later CR needs that.
- Replacing or changing `note <cr>`, `handback` or the hand-back's carriage.
- Any card, wrapper, hook or `references/` text: children 20 and 21 write `msg` and `inbox` into
  the new cards.
- A `msg` from a QA driver (order `O-k`) or a worker. `--cr` takes a CR id or `stack` only.
- Retrying or queueing an undelivered message. The line stays in the journal, and `inbox` lists
  it.

## Gates and evidence

- `just check` before the first push, and `just eval-dry-run` (a change under `src/`).
- `just journal-schemas` run; `hub/schemas.json` gains exactly the `msg@1` entry. The test reads
  the shipped file at the head.
- `tests/test_msg_steering.py` green. `tests/test_event_types.py` green with `msg@1` in its
  parametrization. `tests/test_scenario_coverage.py` green.
- The long gate `just scenario (ubuntu-latest)` green at the PR's head (a CLI and scenario
  change). The local Windows `chantier gate <cr> scenario` is owed only while this CR is the
  stack's top when presented.
- The PR's Deliverables state the `just test` seconds before and after.
- **Host and defaults matrix:** the delivery depends on the host's watcher.
  - **Claude Code, shipped defaults:** the tests, and the scenario (host Claude Code, the watcher
    streaming).
  - **Copilot, shipped defaults:** the tests only, on the plain watcher (`stream=False`), whose
    end lines hold the message. No real run.
  - A project's own `chantier.yaml` changes nothing here (`events.wake_every` delays a block as
    it does today, and is not re-tested).

## Risk

- **Long gate owed** (CLI and scenario).
- **Unproved (F17):** the Foreman's own watcher (CR-479) has never run in a real batch. That the
  Foreman's host wakes it on the `msg@1` block, and that the Foreman then acts on the message, is
  unproved here. Child 28 measures `msg` deliveries. The PR says so in its Known gaps.
- **Unproved (F17):** in direct mode the steering key is `foreman_transcript`, falling back to
  `chief_transcript`. The tests prove it on a prepared record, not in a real direct batch.
- **Delivered is not read.** "Delivered" means a subscribed watcher and a live server, not that
  the session read the message. The wording "delivered to its watcher" says only that.
- The old cards do not name `msg`, so until the swap no agent uses it unless told. Nothing breaks.

## Open questions

None. The program's answers settle the behaviour. Two choices made here belong to the
implementation, and the PR names them:

- `--cr`, added to the form because a lease number alone names no unit;
- read marks kept in the batch's `events.jsonl`, because the journal is append-only.

