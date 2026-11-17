# Change Specification: the project says how many long gates may run at once

## Goal

The gate lock is chantier's. The long gate is the project's. Today the lock lets one long gate run
in the whole repository, whatever the project. A project whose long gate is isolated per worktree
(its own ports, temporary folders and services) loses hours for nothing. In batch-17 every
`just scenario` ran alone, about 35 minutes each, and with four CRs ready together the last waited
about two hours (`intake/request.md`).

This CR does four things:

- The project says in `chantier.yaml` how many long gates may run at once (default 1, today's
  behaviour), and the lock admits that many.
- Only the long gate the project names takes the lock. Short gates run freely.
- The steering session can move a queued long gate to the head of the queue.
- The Chief of Staff asks the project once whether its long gate is isolated per worktree.

Making chantier's own `just scenario` isolable per worktree is a separate project item. It is filed
apart once this CR lands.

## Decisions carried from `02-answers.md` and the request

| Decision | Where this spec carries it |
| --- | --- |
| Request: a `chantier.yaml` key for the number of long gates at once, default 1; the lock admits that many | A, B |
| Request, after the critic: gate-lock-priority is merged here; a manual move-up is enough, no automatic ordering by dependents | D |
| Request, after the critic: only the generic part; chantier's own isolable `just scenario` is a project item filed apart | "Out of scope", "After the merge" |
| Request, after the critic: after CR-235 (gate-liveness), which rewrites `gate_lock.py` | "Order in batch-17", "On top of CR-235" |
| Request: init or the grill asks the project once whether its long gate is isolated per worktree | E |
| 1. Grill and specify first, then add the CR at the end of batch-17's stack, one native stack, budget raised to $210 | "Order in batch-17" |
| 2. The Foreman uses the move-up on its own, to put a critical-path CR's gate first, and says so in its report | D, F |
| 3. Only the long gate the project names (here `just scenario`) takes the lock; short gates (`just check`) run freely, outside the lock | C |
| 4. Grilled enough, after the full restatement | (this specification) |

## Order in batch-17

The CR joins the end of batch-17's stack (answer 1), after CR-235 `gate-liveness` (PR #178, not
merged when this was written). CR-235 rewrites `commands/gate_lock.py` and adds
`commands/gate_run.py`. This CR reshapes both, so the dependency is real: it is not just a shared
file.

**For the Chief of Staff:** record `{"after": ["gate-liveness"]}` in this CR's `depends.json`. This
spec writes nothing outside `03-change-spec.md`.

The Driver works on CR-235's code as it is on its branch (worktree `batch-17-CR-235`, head
`be7034f` when this was written), or as merged if it has merged by then. The Driver keeps the CLI's
targets: file and function sizes, ruff, `mypy --strict`, and no import cycle. All paths below are in
`skills/chantier/scripts/cli/src/chantier/`.

## On top of CR-235: what is already there, and what this CR changes

CR-235 leaves a lock with **one slot**:

- `.long-gate.lock`: byte 0 is the OS lock, and the rest is the holder text `<cr> pid <n>[ pg<m>]`
  (`gate_lock.lock_holder`, `parse_holder`, `Holder`).
- `.long-gate.run` and `.long-gate.stop`: the running gate's run file and its stop marker
  (`gate_run.run_file`, `stop_file`, `run_read`, `run_write`, `stop_asked`).
- Liveness by identity: a pid counts only if `procs.alive_since(pid, mtime of the file that recorded
  it)` holds (`holder_alive`, `lock_mtime`, `mtime`).
- The queue: tickets `.long-gate.queue/<ns:020d>-<pid>`, content `<cr> pid <pid>`. Only the first
  live ticket may try the lock (`LongGateLock._ahead`, `_ticket_cr`). Dead tickets are deleted by the
  gates. `read_ticket` and `queued_crs` only read.
- `gate_state(repo, cr)`: `gate running`, `gate queued behind <cr>` or `gate queued`, used by
  `commands/activity.py`.
- `gate_run.stop_gate(repo, h, b, fallback_head)`: the one stop, shared by `gate --stop`
  (`gate._gate_stop`) and `order merged` (`orders_apply._stop_gate`).
- `cancel` (`commands/release.py`): stops the lock's `pg<m>` for its CR, after the identity check.
- `_acquire`'s hour: it restarts when the holder (without its `pg`) changes. `_wait_suite`: waits for
  a dead gate's suite that still runs.

This CR turns that one slot into **N slots**. N is read from `chantier.yaml`. All of CR-235's
behaviour is kept per slot: the identity check, the stop route, the activity lines, the hour, and
the suite left behind. With N = 1, every file name, every message and every scenario step of CR-235
stays exactly as it is.

## What changes

### A. The `chantier.yaml` key

```yaml
long_gate:
  parallel: 2     # long gates that may run at once in this repository; 1 when absent
```

- **Where it is read.** In `playbook/config.py`:
  - `load()` accepts the top-level key `long_gate`. The unknown-key message lists it: `the top-level
    keys are "roles", "prices", "board" and "long_gate"`.
  - A `_long_gate(node, kline, bad)` validates the key, in the style of `_board`. Its one key is
    `parallel`, an integer of 1 or more, with no upper limit. The problems are:
    - `long_gate: unknown key "<k>": one of parallel`;
    - `long_gate: "parallel" is a whole number, 1 or more, found "<v>"`;
    - `"long_gate" holds its key: `parallel:`` when it is empty or not a mapping.
  - A `load_long_gate(path) -> tuple[int, list[str]]`, in the style of `load_board`, returns `(1,
    [])` when the file or the key is absent.
- **Who reads it.** Only `gate` reads it, at each run, from `repo.root / chantier.yaml`: the main
  checkout, or in external mode the project's clone. It is not frozen when the batch opens. A change
  that the user commits to the main checkout applies to the next `gate`. A change in a CR's worktree
  applies once it is merged into the main checkout.
- **An invalid key.** `gate` exits 2 with the first problem (`chantier.yaml:<line>: long_gate: …`),
  as `board` and `cost` do, and runs nothing. Preflight's P12 and `playbook` report it through
  `load()`, as they report every other key.
- **No `chantier.yaml`.** Chantier runs as if the key were 1, which is today's behaviour
  (`AGENTS.md`: with no `chantier.yaml`, chantier runs as if it were empty).

### B. The lock admits N gates: slots

The lock becomes N slot files. The first slot keeps CR-235's names:

| Slot | Lock (byte 0 locked, holder text after it) | Run file | Stop marker |
| --- | --- | --- | --- |
| 1 | `.long-gate.lock` | `.long-gate.run` | `.long-gate.stop` |
| k ≥ 2 | `.long-gate.<k>.lock` | `.long-gate.<k>.run` | `.long-gate.<k>.stop` |

The holder text, the ticket format and the run file's content (`RunRecord`) do not change.

- **Taking a slot (`LongGateLock._acquire`).** The queue rule stays the same: only the first live
  ticket tries. That gate tries slots 1 to N in order with `try_lock` and takes the first free one.
  If none is free, it waits and tries again every second, as today. Arrival order is therefore kept
  exactly: the next ticket becomes first only when this gate takes a slot and deletes its ticket.
- **The suite left behind (`_wait_suite`).** It applies to the slot the gate took. The gate waits
  for the suite of that slot's previous holder, with the same note and the same hour. A suite left
  behind in another slot does not hold this gate.
- **The wait note.** `waiting for the long gate of <holder>` keeps its prefix, which the Driver card
  quotes. When every slot is held, it names each live holder, joined by ` and `. With N = 1 it is
  today's text. `; queued ahead: …` does not change.
- **The hour.** It restarts whenever the holder of any slot changes. After an hour with no change,
  `gate` is refused (exit 2). The refusal names each gate that holds a slot: `the long gate of <cr>
  (pid <n>) has held the lock for over an hour: check it; …` for N = 1 (unchanged), and `the long
  gates of <cr> (pid <n>) and <cr> (pid <n>) have held …` when more than one holds a slot.
- **Reading the slots.** `lock_holder(repo)` is replaced by a function that lists the slots: each
  existing lock file (`.long-gate.lock`, then `.long-gate.<k>.lock` in k order) with its holder text
  and its modification time. It globs the files, so it does not need N. A stop or a status therefore
  works whatever N is now, even when N was lowered while gates ran. `lock_mtime` and `holder_alive`
  take the slot's lock path.
- **Lowering N while gates run.** A gate already running in a slot above the new N finishes. New
  gates only try slots 1 to N. For a while, more than N gates may run.
- **`holding()`, `__exit__`, the run file and the stop marker** apply to the slot the gate took.
  `gate.gate` and `_run_commands` use that slot's `run_file`, `stop_file` and `stop_asked`, so
  `gate_run`'s helpers take the slot (for example `run_file(repo, slot)`).
- **Stopping a gate.** `gate <cr> --stop`, `order merged` and `cancel` look for the slot whose holder
  names the CR, and act on that slot only:
  - `gate_run.stop_gate` gets the slot and uses its lock's mtime, run file and stop marker.
  - `_gate_stop`'s refusal `the long gate running is <cr>'s: not stopped` becomes: when no slot
    names this CR but some slot is held, `no long gate of <cr> running (running: <crs>): not
    stopped`, exit 2. When no slot is held, the message stays `no long gate running for <cr>:
    nothing to stop`, exit 0.
  - The other slots' gates are not touched.
- **Status (`gate_state`).** The lines follow these rules:
  1. `gate running` when any slot's holder names the CR and passes CR-235's liveness test.
  2. Otherwise, for a CR with a live ticket (`gate_state` does not read N):
     - when live holders exist: `gate queued behind <the CRs of the live holders, in slot order,
       joined by ", ">`;
     - otherwise, when a live ticket is ahead in the queue's order (D): `gate queued behind <that
       first ticket's CR>`;
     - otherwise `gate queued`.

     With one slot this gives exactly CR-235's lines. `gate_state` still only reads.
- **The ignored files.** `core/files.py`'s `IGNORED` gains `.long-gate.*.lock`, `.long-gate.*.run`
  and `.long-gate.*.stop`, so a planning surface never publishes them.
- **The docstrings and the help.** `LongGateLock`'s docstring ("One long gate at a time…") becomes
  "as many long gates as `chantier.yaml`'s `long_gate.parallel` admits (one by default)". The `gate`
  help ("alone in the repository, a second one waits its turn") becomes "as many at once as
  chantier.yaml's long_gate.parallel (1 by default), the others wait their turn, first come first
  served".

### C. Only the long gate takes the lock

`gate` is the command for the long gate that the project's rules name, and only for it. The CLI
does not judge which command is long: it knows no project rule. The cards say it (a card says what
the role judges):

- **`driver.md`, the long gate bullet (lines 112 to 131 on CR-235's branch):** "`$CHANTIER gate`
  runs only the long gate the project's rules name. A short gate (the fast gate, or the check that
  the rules ask of a CR they exempt from the long gate, such as a docs-only change) you run yourself
  in the worktree, never through `gate`: it would wait in the lock behind the long gates. A CR the
  rules exempt hands back with `--no-gate "<the rule>"`." The text "alone in the repository (a
  second long gate waits its turn, in arrival order)" becomes "as many at once as the project
  allows (`chantier.yaml`, one by default), the others in arrival order".
- **`worker.md`, Verifier (line 101):** the Verifier runs `$CHANTIER gate` only for the project's
  long gate. A short check is run directly and cited with its command and output, as any other
  claim.
- **`concepts.md`, lines 225 to 233:** "Long gates run one at a time, in arrival order" becomes "As
  many long gates run at once as `chantier.yaml`'s `long_gate.parallel` says (one when absent), the
  others in arrival order; `gate` is only for the long gate the project's rules name, and a short
  gate runs outside it". The `--stop` sentence says it acts on the slot that names the CR.
- **`docs/gates.md`, lines 10 and 11:** "alone in the repository, in arrival order when several
  wait" becomes "as many at once as your `chantier.yaml` allows (one by default, see below), in
  arrival order when more wait". Add a short paragraph: an isolated long gate (its own ports,
  folders and services per worktree) can run several at once with `long_gate: parallel: <n>`; the
  number is what your machine carries. The fast gate is never run through `chantier gate`.

### D. The move-up: `gate <cr> --first`

The steering session's command, never a Driver's:

```
chantier gate <cr> --first --epoch <n>
```

- **What it does.** It puts the CR's waiting long gate at the head of the queue. It creates an empty
  marker `.long-gate.queue/first-<ticket name>` for each live ticket of that CR. A marker does not
  match the tickets' glob `[0-9]*`, so CR-235's readers and the scenario's `tickets()` do not see
  it.
- **The order.** The queue's sort key becomes (no marker, ticket name): marked tickets come first,
  and among them the order is arrival. `_ahead`, `queued_crs` and `gate_state` all use this key. The
  waiting gate reads its own key again on each loop, because a marker can arrive while it waits.
- **No rewrite of a ticket.** A ticket is never rewritten. A marker whose ticket is gone is ignored
  and deleted by the gate that reads it, as a dead ticket is. The gate deletes its own marker with
  its ticket (in `__enter__`'s `finally`). A marker made for a ticket that a gate is deleting at the
  same moment is therefore harmless.
- **Output.** One line: `moved the long gate of <cr> to the head of the queue (ahead of: <crs>)`,
  or `… (it was first)` when no live ticket of another CR was ahead. The command exits 0 and writes
  a `gate-first` event with the CR in `events.jsonl`, through the batch record.
- **Refusals.**
  - Without `--epoch`: exit 2, `gate <cr> --first --epoch <n>: the steering session's command to put
    a critical-path CR's long gate first; a Driver never moves its own gate`. This follows
    `cancel`'s refusal. A stale epoch is exit 3, as everywhere.
  - With commands or with `--stop`: exit 1, a usage error.
  - When no live ticket names the CR: exit 0, `no long gate of <cr> waiting: nothing to move`.
- **Running gates.** It does not touch a running gate or a slot. It only orders the queue.

### E. The question to the project, asked once

- **`init.md`, step 5.1 ("Check the two gates"):** when the project declares a long gate, or when
  the tour proposes one, ask once whether that long gate is isolated per worktree. Isolated means
  its own ports, temporary folders and services, so that two runs in two worktrees do not break each
  other. On a yes, ask how many runs at once the user's machine carries. Then propose the
  `chantier.yaml` lines `long_gate:` / `parallel: <n>`, and write them only on the user's yes.
  - On a no, propose `parallel: 1`, written on the user's yes, so the question is not asked again.
  - When `chantier.yaml` already has `long_gate`, the question is not asked.
  - The impact when the key is missing: long gates run one at a time, and four ready CRs wait their
    turns.
- **`chief-of-staff.md`, "The project" (lines 77 to 82):** at the same moment as the long-gate
  question ("When the user says 'our long gate is `<command>`'…"), the same question is asked once,
  on the same rule. The `chantier.yaml` section (lines 86 to 112) lists the key beside `roles`. You
  edit the key only on the user's word, as for every key.
- **`docs/agents-and-models.md`, line 28:** "The file's other keys are `prices` and `board`" becomes
  "`prices`, `board` and `long_gate` (how many long gates may run at once, [your gates](https://github.com/gsemet/chantier/blob/main/docs/gates.md))".

### F. The Foreman card: the move-up and the report

`skills/chantier/references/foreman.md`, "Your means" (near line 100), gains one bullet:

> `$CHANTIER gate <cr> --first --epoch <n>`: when a CR on the critical path (other CRs wait for it,
> by `after` or by the stack) has its long gate queued (`gate queued behind …`), put it first. Say
> it in your next report: which CR, ahead of which. Never for any other reason, and never at a
> Driver's request alone.

This is the Foreman's own call (answer 2). In a direct batch the Chief of Staff steering reads the
same card. No agent file changes (`agents/`, `com.github.copilot/agents/`). The `report-format`
progress table does not change: the move-up is one line of the report's text.

## Out of scope

- Making chantier's own `just scenario` isolable per worktree (ports, temporary folders, the fake
  forge), measuring its CPU load with several at once, and setting chantier's own `long_gate` key.
  This is a project item, filed apart when this CR lands ("After the merge").
- Automatic ordering of the queue by dependents or priority: the move-up is manual.
- A CLI judgement of which command is long, or a list of long-gate commands in `chantier.yaml`. The
  cards say it, and the project's rules name the command.
- A cap tied to the batch's slots, or to CPU measures, inside the CLI.
- Changes to CR-235's rules: identity check, stop route, activity lines, the one-hour limit
  `LONG_GATE_WAIT_S`, the holder and ticket formats.
- The CR board pane: `STATUS.json` and `hooks/register.tsx` do not change, so no screenshot and no
  `just mod` are needed.

## After the merge (for the Chief of Staff)

File the project item in the inbox: "make chantier's `just scenario` isolable per worktree (ports,
temporary folders, the fake forge), measure the CPU load of several at once on the user's machine,
then set `long_gate.parallel` in chantier's `chantier.yaml`". The source is this CR's request.

## Evidence

The Verifier keeps each item in `work/verifier/evidence/`, and the PR body quotes them. The CLI and
the cards change, so `just check` and `just scenario` (both forges) apply (`AGENTS.md`). The
scenario steps go in `scenario/run_scenario.py`, in `rails()` beside the queue steps (lines 2863 to
2944 on CR-235's branch), and in `playbook_config()` (17b) for the key. A step that writes
`chantier.yaml` writes it at `w.work / "chantier.yaml"` and removes it at the end, as 17b and the
board's step 9 do. Every step works on Linux, macOS and Windows.

- **E1. Default unchanged.** With no `chantier.yaml`, every existing step of the queue, of 18
  (cancel during a gate), of 18b (`--stop`) and of 12c (activity) passes unchanged, including "a
  second long gate waits for the first".
- **E2. Two at once.** With `long_gate:` / `parallel: 2`:
  1. A held gate of `one` and a gate of `two` both run. `lock_names` sees `one` in `.long-gate.lock`,
     and a new helper sees `two` in `.long-gate.2.lock`.
  2. `two`'s log has no `waiting for the long gate`, and it ends before `one`'s held gate ends.
  3. A third gate waits. Its log names both holders (`waiting for the long gate of <one> … and <two>
     …`), and it runs once one of them ends.
  4. Arrival order is kept for three waiters behind two slots.
- **E3. Status with two slots.** Both running CRs show `activity <cr> gate running`. The waiting one
  shows `gate queued behind <one>, <two>`.
- **E4. A stop acts on its slot only.** With two slots held:
  - `gate <two> --stop` stops `two`'s suite. Its gate exits 4 with `STOPPED`, and `one`'s suite
    still runs.
  - The same holds for `order merged <two> --epoch 1` and for `cancel <two>`.
  - `gate <three> --stop`, with no slot naming `three`, exits 2 and names the running CRs.
- **E5. The move-up.** With `parallel: 1` and one held gate, gates of `two` then `three` queue.
  - `gate <three> --first` without `--epoch` exits 2 with the refusal's text.
  - `gate <three> --first --epoch 1` prints `moved the long gate of <three> to the head of the queue
    (ahead of: <two>)`, and an event `gate-first` with `cr: <three>` is recorded.
  - `three`'s gate runs before `two`'s (the order of the `gate` events), and `status` shows `gate
    queued behind` the holder for `three` while it waits.
  - `gate <two> --first --epoch 1` when `two` has no ticket prints `nothing to move`, with exit 0.
  - No `first-*` marker is left in the queue at the end.
- **E6. The key's validation (17b).**
  - `long_gate:` / `parallel: 0` and `parallel: two` each make `gate` exit 2 with
    `chantier.yaml:<line>: long_gate:`, and make `playbook` exit 2 and preflight's P12 fail with the
    same line.
  - `long_gate:` / `slots: 2` is refused as an unknown key.
  - A valid `long_gate` leaves `playbook` valid and P12 ok.
- **E7. The surface publishes no slot file.** `LOCAL_FILES` gains `.long-gate.2.lock`. The
  surface step runs one gate with `parallel: 2` held in slot 2, and checks that the surface's git
  lists no `.long-gate.*` file.
- **E8. The cards.** The `git diff` of `driver.md`, `worker.md`, `concepts.md`, `foreman.md`,
  `chief-of-staff.md`, `init.md`, `docs/gates.md` and `docs/agents-and-models.md` shows only the
  lines named in C, E and F. The scenario's card checks pass.
- **E9.** `just check` passes on Windows locally, then in CI on Linux, macOS and Windows, including
  `lint` (ruff, `mypy --strict`, sizes). `just scenario` passes on both forges on the Windows dev
  machine and in CI. The locks differ per system (`try_lock`), and CI runs the scenario on Linux
  only.

## Open questions (defaults taken, for the Chief of Staff to confirm with the user)

1. **How the short gate stays out of the lock (answer 3).** Default: by the cards. `gate` is only
   for the long gate the rules name, a short gate runs directly, and an exempt CR hands back with
   `--no-gate "<rule>"`. The CLI does not change for it. The alternative is a `gate <cr> --free
   "<cmd>"` flag that records a short gate's pass without taking the lock. It keeps a recorded pass
   for a docs-only CR, but it adds a CLI option that no measured cost asks for.
2. **"Init or the grill".** Default: the init tour (step 5.1) and the Chief of Staff's long-gate
   moment in "The project". Neither the Griller nor the grill of a CR asks it. Is that what "the
   grill" meant?
3. **A "no" recorded as `parallel: 1`.** Default: proposed and written on the user's yes, so the
   question is asked only once. The alternative leaves the file untouched and asks again at the next
   init.
4. **The key's name and shape.** Default: `long_gate:` / `parallel: <n>`, an integer of 1 or more,
   with no upper limit. The alternative is a flat `long_gates: <n>`, or a cap (for example the
   batch's slots).
5. **Who may move a gate up.** Default: the steering session with its `--epoch` (the Foreman, or the
   Chief of Staff in a direct batch), as `cancel` works. The Chief of Staff of a Foreman batch does
   not run it, but it can ask the Foreman by an `order note`.
