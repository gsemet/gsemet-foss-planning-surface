# SC13: A Driver messages the steering session through the board

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
