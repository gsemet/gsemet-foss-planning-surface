# Change Specification: every steering command refuses a missing `--epoch`

## Goal

A Foreman's (or a steering Chief of Staff's) command that changes the batch must say which
Foreman it comes from. Today `take`, `pause`, `order done`, `agents set` and `foreman transcript`
still accept a call with no `--epoch`: a stale or confused session that forgets the flag slips
past the stale-Foreman check (exit 3) and acts on a batch another Foreman now runs. After this CR,
every steering command refuses a call with no `--epoch` (exit 2), and only the reading of the
status goes without it (`status --refresh`, and plain `status`). To the user, the number is never
called an epoch: it is the Foreman's number within its batch, `batch-18, Foreman n°2`. The flag
keeps its name, `--epoch`.

## Decision carried

- EP-Q1 (A), `02-answers.md`, 2026-11-14: every Foreman steering command refuses a call with no
  `--epoch` (exit 2); only the reading of the status (`status --refresh`) goes without it. To the
  user the number is shown as the Foreman's number within its batch (`batch-18, Foreman n°2`),
  never with the word epoch; the flag's name may stay.

## The steering commands, and what each does after the change

"Steering command": a command only the steering session (the Foreman, or the Chief of Staff in a
direct batch) runs, which the cards already list as carrying `--epoch`. The CLI's root is
`skills/chantier/scripts/cli/src/chantier/`; paths below are relative to it.

| Command | Today with no `--epoch` | After |
|---|---|---|
| `foreman set <session> --epoch <n>` | refused, exit 1 (`foreman set <session-id> --epoch <n>`, `commands/seat.py`) | refused, **exit 2**; a missing session id stays exit 1 |
| `foreman transcript <uuid> --epoch <n>` | **accepted** (`check_epoch` returns on `None`) | refused, exit 2 |
| `status --stop-heartbeat --epoch <n>` | refused, exit 1 (`commands/batch_status.py`, `_stop_heartbeat`) | refused, **exit 2** |
| `take <cr>` / `take stack` `--epoch <n>` | **accepted** (`commands/driver.py`, `take`) | refused, exit 2 |
| `agents set <cr>\|stack\|O-<k> <id>\|- --epoch <n>` | **accepted** (`commands/batch_status.py`, `agents`) | refused, exit 2 |
| `order done <O-k> --epoch <n>` | **accepted** (`commands/orders.py`, `_order_done`) | refused, exit 2 |
| `pause --epoch <n>` | **accepted** (`commands/closing.py`, `pause`) | refused, exit 2 |
| `gate <cr> --first --epoch <n>` | refused, exit 2 (`commands/gate.py`, `_gate_first`) | unchanged |
| `cancel <cr> --epoch <n>` | refused, exit 2 (`commands/release.py`, `cancel`) | unchanged |

Unchanged, by design:

- `status` and `status --refresh` with no `--epoch`: the read and the refresh before a report;
  they move no heartbeat. `status --refresh --epoch <n>` stays the loop's wake.
- `order merged <cr>` and `order add --note ... --fix-for <cr>`: with `--epoch` they are the
  steering session's own merge or fix; without it they are the Chief of Staff's order (the user's
  merge, a fix the user ordered), as today. They are orders, not steering commands; the CLI keeps
  both forms (see Open questions, Q1).
- `foreman get`: a read; it takes no `--epoch`.
- Every other command and order kind: unchanged (`order note`, `order after`, `order add` without
  `--fix-for`, `note`, `asks`, `close`...).

### The refusal

- Raised before anything is written: no lock taken for long, no event, no `batch.json` change, no
  STATUS file rewritten. Where the handler already checks early (`cancel` checks before
  `open_repo()`), do the same; at the latest it is the first statement inside the batch's context,
  before `check_epoch`, and it must leave the batch's files byte-identical.
- Exit code `EXIT_PRECONDITION` (2), as `cancel` and `gate --first` already do.
- The message names the command and the flag, says it is the steering session's command, and
  uses no "epoch" word outside the flag's own name, in the style of `cancel`'s:
  `take <cr> --epoch <n>: the steering session's command; <n> is your number as Foreman of the
  batch (Foreman n°<n>)`. The exact wording is the Driver's; each command's message names that
  command's own form (`take stack --epoch <n>`, `agents set <cr> <id> --epoch <n>`,
  `order done <O-k> --epoch <n>`, `pause --epoch <n>`, `foreman transcript <uuid> --epoch <n>`,
  `status --stop-heartbeat --epoch <n>`, `foreman set <session-id> --epoch <n>`).
- Implementation suggestion (the Driver judges): one helper in `core/batch.py` next to
  `check_epoch`, e.g. `require_epoch(epoch, usage)`, raising `ChantierError(usage,
  EXIT_PRECONDITION)` when `epoch is None`, called by each handler above; `cancel` and
  `_gate_first` may move to it. `check_epoch` keeps returning on `None` for the commands where
  `--epoch` stays optional (`status --refresh`, `order merged`, `order add --fix-for`).

### Messages the user may see: "Foreman n°<k>", never "epoch"

The CLI's refusals are reported to the user with their exact text (the cards' rule on refusals),
so the messages this CR touches drop the word:

- `core/batch.py`, `check_epoch`: `stale Foreman: epoch {epoch}, batch {b.id} is at epoch
  {current}; stop now` becomes, in substance, `stale Foreman: Foreman n°{epoch} of {b.id}, which is
  now at Foreman n°{current}; stop now` (exit 3 unchanged).
- `commands/seat.py`, `foreman set`: `epoch {n} cannot be claimed: batch {id} is at epoch
  {current}; stop now` becomes `Foreman n°{n} of {id} cannot be claimed: the batch is at Foreman
  n°{current}; stop now` (exit 3 unchanged); `foreman transcript`'s `epoch {k} of batch {id} is
  already run by transcript {t}; stop now` becomes `Foreman n°{k} of {id} is already run by
  transcript {t}; stop now`.
- The `--epoch` help in `commands/registry.py` (`the Foreman's epoch; stale ones exit 3`) becomes
  e.g. `the steering session's number in the batch (Foreman n°<n>): missing on a steering command
  exits 2, stale exits 3`. The `--refresh` and `--stop-heartbeat` help in
  `declare/batch_status.py` stay as they are, or lose the word where it is not the flag's name.
- Not changed: `foreman get`'s output (`<session> epoch <n>`, read by the Chief of Staff to
  compute the next number), the `status` line's `e<n>`, the record's field `foreman_epoch` and the
  events' `epoch` key: agent-facing or data, not shown to the user as such.

## The cards

All in `skills/chantier/references/` (shared by both hosts; no file in `agents/` or
`com.github.copilot/agents/` changes).

- `foreman.md`, the bullet "Exactly these commands carry `--epoch <n>`" (near the end): add
  `gate <cr> --first` to the list (the card uses it at "Your means" but the list omits it), and
  say that each listed command refuses a call without `--epoch` (exit 2), except `order merged`
  and `order add --fix-for`, whose form without it is the Chief of Staff's order, and `status
  --refresh`, which without it is the refresh before a report and records no heartbeat. Keep the
  exit 3 line.
- `foreman.md`, every example of a listed command written without `--epoch`: line ~20
  (`$CHANTIER pause` in the overview) becomes `pause --epoch <n>`; "Your means", `take stack` and
  `agents set stack <id>` (the stack driver's start order, ~line 115-117) carry `--epoch <n>`;
  check the rest of the card for any other bare `take`, `agents set`, `order done` or `pause`
  meant as a command to run (prose naming a command, like "the first `take` sets it running",
  may stay bare).
- `chief-of-staff.md`, "Steering a batch yourself", "Your epoch": the same two changes to its
  list (add `gate <cr> --first`; each refuses a call without it, exit 2, with the same two
  exceptions and the refresh before a report). The bullet's title becomes "Your number as
  Foreman" or similar; the text the agent reads may keep the word where it names the flag.
- `chief-of-staff.md`, "Recovery" (~line 1183-1186): the quoted "Resume:" text added to the new
  Foreman's prompt carries `--epoch <n>` on `agents set <cr> -`, `take <cr> --note ...` and
  `agents set <cr> <id>`, since a Foreman copying it would now be refused.
- `chief-of-staff.md`, "Starting a batch", the Foreman's prompt: its first line,
  `chantier Foreman of batch <batch>, epoch <n>, for the Chief of Staff <your session id>.`, is
  pasted by the user in the remote "For you" block (`hosts/claude-code.md`, "A new Foreman, from a
  remote client"), so it becomes `chantier Foreman n°<n> of batch <batch>, for the Chief of Staff
  <your session id>.`; the sentence after it ("`<n>` its epoch ...") says `<n>` is the Foreman's
  number, the value of its `--epoch`. `foreman.md`'s first lines ("gives the batch, your epoch,
  ...") say the prompt gives "your number as Foreman of the batch (n°<n>), the value of your
  `--epoch`". No code reads this line (checked: no match in `agents/`, `com.github.copilot/`,
  `hooks/`, `scenario/`, `evals/`).
- `concepts.md`, "Steering session" (~line 260): add one sentence: to the user, a claim's number
  is the Foreman's number within its batch (`batch-18, Foreman n°2`), never the word epoch; the
  flag stays `--epoch`.
- `concepts.md`, the exit codes (~line 284): `a cancel without --epoch` becomes `a steering
  command without --epoch (the cards list them)`; `3 stale Foreman epoch` becomes `3 a stale
  Foreman (a later Foreman n° claimed the batch)`.
- `chief-of-staff.md` and `status-layout.md`: any text the Chief of Staff says or writes to the
  user (reports, asks relayed, the "For you" blocks, the Completion report) that names a Foreman's
  number says `Foreman n°<k>`. Today none uses the word (checked); add the rule once, in the
  report rules of `chief-of-staff.md` (or by reference to `concepts.md`), so a stale-Foreman
  refusal or a relay is reported as "batch-18, Foreman n°2 is stale: Foreman n°3 runs it".
- `hosts/claude-code.md`, "Reusing the last Foreman" and "A Foreman in a worktree asks": agent
  text, may keep the word; change only if the Driver finds a sentence the Chief of Staff repeats
  to the user.

## The scenario (`scenario/run_scenario.py`)

1. **Existing calls without `--epoch` now meant to pass, or to be refused for another reason**,
   must carry the batch's current number, so each check keeps proving what it proved. Found
   (line numbers at the CR's writing; the Driver re-greps
   `chantier\(\s*"(take|pause|agents)"|"order",\s*"done"|"foreman",\s*"transcript"` without
   `epoch`): 327 (`Foreman.turn`, the `agents set` after a start: the call continues on 328, check
   it carries `--epoch`), 672, 767, 768, 3202, 3215, 3228, 3232, 3233, 3633, 3635, 3639, 3643,
   3653, 3656, 3657, 3667, 3668, 3790, 3816, 3824, 4706, 4712, 4717, 4731-4792, 4818, 5090,
   5213, 5225, 5296, 5301, 5402, 5902, 5907, 5959-6064 (including `order done O-1` at 6047).
   A call with `expect=2` or `expect=5` whose point is another refusal (a slot, `waits for`, the
   budget, a working CR without `--note`, an agent still recorded) must keep failing for that
   reason: add `--epoch` and, where the check does not already read the stderr, check its cause
   in `w.last_stderr`, so the new exit 2 cannot make it pass vacuously. Where a section never
   claims a number (`foreman set`), the Driver claims one (`foreman set ... --epoch 1`) or passes
   the batch's current one (`0` when none was claimed, which `check_epoch` accepts today: see
   Q2); its choice.
2. **New step, "a steering command needs its number":** in a batch with a claimed Foreman, each of
   `foreman set <s>` (no `--epoch`), `foreman transcript <u>`, `status --stop-heartbeat`,
   `take <cr>`, `take stack` (in a stack batch, or the section that has one), `agents set <cr> -`,
   `order done <O-k>` and `pause` without `--epoch` exits 2, its stderr names the command's
   `--epoch <n>` form and does not contain the word "epoch" outside `--epoch`, and
   `batch.json` and `events.jsonl` are byte-identical before and after. The existing refusals of
   `cancel` (line ~3106) and `gate --first` (~3447) stay.
3. **The exceptions still pass:** `status --refresh` without `--epoch` exits 0 and leaves the
   heartbeat where it was (an existing step may already prove it: keep it); `order merged <cr>`
   without `--epoch` is still recorded as the Chief of Staff's order (existing steps).
4. **The wording:** the stale refusal (line ~778, `foreman set ... --epoch 2` after a later claim,
   exit 3) also checks its stderr says `Foreman n°` and not ` epoch `.

## Out of scope

- Renaming the flag `--epoch`, the record's `foreman_epoch` field, the events' `epoch` key, or
  `foreman get`'s output.
- Rewording the cards' agent-facing vocabulary ("claim your epoch") beyond what is named above.
- `asks "<text>"` (a Foreman's own ask) and `note`: not steering commands in the cards' list; they
  stay without `--epoch`.
- The eval kit's audit (`evals/kit/audit.py`, check C9, which flags a steering call without
  `--epoch` in a transcript): it stays as it is; a refused call is still visible to it.
- The docs' lifecycle diagram texts (`docs/*-lifecycle-texts.md`), which name commands without
  their flags.
- A refusal of `--epoch 0` on a batch no Foreman has claimed (Q2).

## Evidence

- `just check` passes (Linux, macOS, Windows in CI).
- `just scenario` passes, with the new step and the updated calls (a change to the CLI, the cards
  and the scenario: the long gate is required).
- By hand, in the PR's Evidence: one run of `take <cr>` without `--epoch` on a scenario-like batch
  showing exit 2, its message, and `git diff --no-index` (or a hash) of `batch.json` before and
  after showing no change.
- No change to `hooks/` or `types/`: `just mod` not required. No change to what the CR board pane
  draws: no screenshot required.

## Open questions

- **Q1 (scope).** `order merged <cr>` and `order add --fix-for <cr>` keep their form without
  `--epoch`, because that form is the Chief of Staff's order (the user's merge, a fix the user
  ordered), not a steering command. A steering session that forgets the flag on its own merge is
  then recorded as the Chief of Staff's order rather than refused. Is that the reading you want
  (this specification assumes it), or must these two refuse a missing `--epoch` too when the
  caller is the steering session (which the CLI cannot tell without knowing the role)?
- **Q2 (risk).** `--epoch 0` on a batch where no Foreman has claimed a number yet is accepted
  today (the batch starts at 0). Should a steering command also refuse while no Foreman has
  claimed the batch, or is that left as it is (this specification leaves it)?
