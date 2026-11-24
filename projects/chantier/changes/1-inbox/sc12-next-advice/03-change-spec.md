# SC12: `chantier next` and `next:` lines

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
