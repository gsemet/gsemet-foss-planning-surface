# Gate proof and small CLI fixes

Change Specification for the CR `gate-proof-cli-fixes` (batch-11 retro; folds the inbox items
gate-log-commit, driver-budget-refusal and undrop-cr). Sources: `intake/request.md`,
`01-intent.md`, `02-answers.md` (2026-11-11; every design decision delegated by the user, taken by
the Fable advisor, accepted by the Chief of Staff; answers 16-20 decided by the Chief of Staff
under the user's delegation). Code paths are under `skills/chantier/scripts/cli/src/chantier/`;
cards under `skills/chantier/references/`. Line numbers are those of `main` at 24cc7eb.

## Goal

1. The long gate's proof binds to one exact commit that anyone can read: the gate log says which
   commit it ran at, and `handback ready` refuses anything but that commit, committed, clean and
   pushed.
2. The budget is a real bound on new rounds, as `driver.md` already says: `round` is refused once
   the batch's budget is spent.
3. The user has a CLI way to bring a dropped, cancelled or abandoned CR back from `6-trash` to the
   inbox, instead of a hand move.

## Today (what the grill found)

- `gate` reads the head after the run (`git rev-parse --short HEAD`, commands.py:1720) and records
  it in each `gate` event (commands.py:1721-1724); the log file holds only `$ <cmd>` lines
  (commands.py:1710) and the commands' output, no commit.
- `handback ready` already refuses without a passed gate and a `VERIFIED` verdict at the head
  `ship` recorded (commands.py:1504-1513), but it does not check that the worktree is still at that
  head, clean, or pushed.
- Heads are short and compared by string equality: `gate` and `verdict` record `git rev-parse
  --short HEAD` (commands.py:1720, 1754), `ship` records `head[:7]` (commands.py:1782). Git
  abbreviates past 7 characters in large repositories (or with `core.abbrev`), so `gate`'s head
  and `ship`'s head differ there and `handback ready` is refused forever (found by reading, not
  exercised).
- `round` refuses only on the round limit (`check_round`, rails.py:196-202, called at
  commands.py:1459); the budget is checked only by `take` (`check_take` → `check_budget`,
  rails.py:179). `driver.md:96` already says `budget:` follows a refusal of `take` or `round`.
- There is no way back out of `6-trash` but a hand move. `abandon` (commands.py:388-402) and
  `trash_cr` (lifecycle.py:172-179) name a trashed folder `<yymmdd-hhmm>-<name>`, where `<name>` is
  the inbox slug or a batch CR's `<NNN>-<slug>`.

## What changes

### 1. The commit a gate ran at (decision 1)

In `gate` (commands.py:1690-1733):

- Read the worktree's HEAD as the **full 40-character SHA** (`git rev-parse HEAD`) **before the
  gate's first command**, after the dirty check below.
- Write it as the **first line of the gate log**, with the CR and the branch (for example
  `gate CR-180 branch chantier/batch-12/cr-180-… head <40-char sha>`). It is the first line of the
  file: written before the long-gate lock is taken, so before any `waiting for the long gate of …`
  line that `_LongGateLock._wait_note` writes.
- The log's **last line gives the result** (the pass, the failed command with its exit code, or
  the head moved, see 4).
- Record the same full SHA in each `gate` event (`head=`), as the start head.
- The printed lines may show a short form of the SHA (display only, see 2).

### 2. Full SHA everywhere (decision 2)

- Record and compare heads as the full SHA in `gate`, `verdict` (commands.py:1754), `ship`
  (commands.py:1782, 1790, 1794-1795), `handback` (commands.py:1504-1511) and `handoff`
  (`_facts`, commands.py:1372-1381). `ship` stores the full head in the CR (`head=`) and in its
  event; its "no long gate passed at …" check uses the full head.
- A short form (7 characters) is for display only: printed lines, `STATUS.md` (status.py:146,
  148), the `PR: …; head …` line of the facts.
- `handoff`'s checklist ("gates before handback ready, at the PR's head …") gives the **full SHA**,
  so the Verifier can cite it (decision 7).
- **Upgrade tolerance:** a head recorded short before this change (in `batch.json`'s CR `head` or
  in `events.jsonl`) matches a full SHA when it is a prefix of it, so an open batch survives the
  upgrade; the same tolerance the code already gives an event with no `run` (commands.py:440-442).
  `gate_passed` and `last_verdict` (commands.py:433-450) and the new `handback` checks compare
  through that rule.

### 3. A dirty tree at `gate` (decision 3)

`gate` is refused, **exit 2**, before running anything (no log command run, no event), when the
worktree has tracked changes or untracked files, by the same test `verdict` uses
(`git status --porcelain --untracked-files=normal`, commands.py:1751-1753). The message says a gate
binds to a commit: commit first.

### 4. HEAD moves during the gate (decisions 4, 16)

After the run, read the worktree's HEAD again. If it differs from the start head, the run is
recorded as **not passed at either head**: `gate_passed` must be false at the start head and at the
new head for this invocation (the run's events record that, at both heads). The output says the
head moved (from which SHA to which), and so does the log's last line. `gate` then exits **4**
(external), as a failed gate command does.

### 5. `handback ready` refuses (decision 5)

For a CR that is not a release (the release path, commands.py:1494-1501, is unchanged), after the
"a PR recorded" check, `handback ready` refuses with **exit 2, one line per cause**, all causes
listed together as today's `missing` list does, when:

- the worktree's HEAD is not the head `ship` recorded (a commit made after `ship`);
- the worktree is dirty (tracked changes or untracked files, same test as `verdict`);
- the remote-tracking branch `<remote>/<branch>` (as `ship` reads it, commands.py:1777-1778) is not
  at that head (not pushed);
- the long gate has not passed at that head (as today);
- the last verdict at that head is not `VERIFIED` (as today).

It runs **no fetch**: it reads the local remote-tracking ref only (concepts.md:164-166: the CLI
runs no git command that changes anything).

### 6. `--no-gate` (decision 6)

`--no-gate "<rule>"` skips **only** the gate check. The head, dirty and pushed checks, and the
verdict check, still apply.

### 7. The CLI refuses; the Verifier cites (decision 7)

The CLI is what refuses. In `worker.md`, "Verifier" (worker.md:74-79), the card says: the
Verifier cites the gate's pass in `verify.md` by the gate log's header line and `handoff`'s
checklist, at the full SHA; it runs `$CHANTIER gate` itself **only when no pass exists at that
head** (today the card has it run the gate for any claim only the long suite proves; the facts it
reads are `_facts`, commands.py:1375-1381).

### 8. The budget refuses a round (decisions 8, 10, 17)

- `round` (commands.py:1449-1464) is refused, **exit 5**, once the budget is spent, with the round
  count unchanged and nothing logged. The message is **distinct from the round-limit message**
  (rails.py:200-201) and names the budget, so the Driver hands back `blocked budget: …`, not
  `rounds: …` (driver.md:96, concepts.md:169). The round-limit refusal keeps its own message.
- **Both spent:** when the round limit is reached and the budget is spent, `round` gives the
  **budget** refusal, and the Driver hands back `budget:`: more rounds alone would not let it go
  on. So the budget is checked before the round limit.
- The spend figure is the last recorded `spent_usd` (from the last `status --refresh`); `round`
  prices nothing. No budget, or no priced refresh yet, means no refusal: the rule of `over_budget`
  (rails.py:140-142).
- Align the texts so they say the same thing: the `check_budget` docstring (rails.py:155-157,
  today "No Driver of any kind starts past the budget; the ones already live, and their workers,
  go on"), the `round` docstring (commands.py:1450-1451), the `round` help in cli.py:129 (today
  "exit 5 past the limit"), `foreman.md:51-52` (today "`round` past the limit"), `driver.md:96`
  and `concepts.md:117-121, 169`.

### 9. What stays open past the budget (decision 9)

`gate`, `verdict`, `ship`, `note` and `handback` are never refused for the budget: "never skip a
proof pass to save budget" (driver.md:96-97). No budget check on workers or mid-round.

### 10. `restore`: a trashed CR back to the inbox (decisions 11-15, 18, 19)

A new command, `restore <6-trash/item> [--slug <name>]`, with no `--batch` argument
(`cmd(..., batch=False)` in cli.py, next to `abandon`), run on the user's word by the Chief of
Staff or a Griller. It is the reverse of `abandon` (commands.py:388-402), under `changes_lock`,
then `write_dashboard`.

- **From and to:** from `6-trash` only, always to `1-inbox` (every dropped, cancelled or abandoned
  CR ends in `6-trash`, lifecycle.py:172-179). A merged CR is delivered: new work is a new `file`.
- **Name:** the date stamp is removed (every leading `<yymmdd-hhmm>-`, as `cr_slug` strips them,
  commands.py:505-508). A number is stripped **only from a folder known to be a batch CR's (its
  record says so)**, never a leading number of a plain slug: an abandoned inbox item `2026-plan`
  comes back as `2026-plan`, not `plan`. `--slug <name>` replaces the name; it follows `file`'s
  slug rule (`[a-z0-9][a-z0-9-]{0,80}`, commands.py:371-372).
- **Content:** kept whole: `intake/`, `01-intent.md`, `02-answers.md`, `03-change-spec.md`, `work/`
  and anything else in the folder; the folder is moved, not copied.
- **A former batch CR's identity:** the restored CR's `01-intent.md` or notes keep a line
  `formerly CR-<n> of batch-<m>`.
- **CR numbers are never reused:** a number once given by a batch is never given to another CR,
  even after `restore` strips it from a restored folder and that batch is closed. Today
  `next_cr_number` (state.py:577-593) takes the highest number among the folder names of
  `6-trash`, `5-archives` and the open batch's state folders and the open batch's record, so a
  restored folder that held the highest number would free it; how the CLI ensures no reuse is the
  implementer's call.
- **Refusals, exit 2 with nothing moved:**
  - the name is already used in `1-inbox`, in `2-backlog/P1..P4`, in `3-ready`, or by a CR of an
    open batch (its folder's name without its number); `--slug` renames, as `file` has;
  - the item is not directly under `6-trash` (an item of `5-archives`, `3-done` or anywhere else).
- **A cancelled CR of an open batch:** restoring it is allowed. It stays `cancelled` in that batch
  and is never revived there; `close` (commands.py:1940-1979) must still work with its folder gone
  from `6-trash`. Its old branch, worktree and PR are not touched; the output says so in **one
  line** (naming them). Re-entering a batch goes through `order add`.
- Output: the new inbox path (as `abandon` prints its target), plus that one line when it applies.
- Cards: `chief-of-staff.md` "Backlog and grill" (the command block at line 128) gains a
  `$CHANTIER restore <6-trash/item> [--slug <slug>]  # only on the user's word` line; `griller.md:21`
  says the Griller may `restore` on the user's word. `concepts.md` names `restore` where it
  describes `6-trash` and the CLI's commands, if it does.

### Cards, in one list

- `driver.md`: the long gate (lines 35-38: refused on a dirty tree, the log's header names the
  commit, a head moved during the run is no pass), `ship` (48-49), the end (84-89: `handback
  ready`'s refusals: head not the shipped one, dirty, not pushed, gate, verdict; `--no-gate` waives
  the gate only), the budget (96: unchanged in meaning, made consistent; both limits spent gives
  `budget:`).
- `worker.md`, Verifier: decision 7.
- `foreman.md:51-52`: `round` refused past the limit or the budget.
- `concepts.md:164-177`: exit 2 and exit 5 lists, the gate's head (full SHA, the log header), what
  `handback ready` needs.
- `chief-of-staff.md`: the `restore` line; and the push judgement at lines 342-344, which reads
  "the last `gate` invocation at the local short sha in the batch's `events.jsonl`": it reads the
  full sha, aligned with decision 2 (decision 20).
- `griller.md:21`: the `restore` line.
- No agent file changes (`agents/`, `com.github.copilot/agents/`).

## Out of scope

- Re-gating or invalidating a `ready` CR after the stack driver moves it.
- Any git write or fetch by the CLI.
- A budget check on workers or mid-round; re-pricing at `round`.
- Restoring from `3-done` or `5-archives`, or straight into the backlog or a batch.
- Reviving a cancelled CR inside its batch.
- Changing the long gate's commands.

## Evidence

`just check` passes (structure tests only, `tests/test_structure.py`), and `just scenario` passes
on both forges (`--forge github`, `--forge gitlab`): the CLI and the cards change. The acceptance
checks below go into `scenario/run_scenario.py`, mostly beside `handback_proofs` (line 1851),
`rails` (1750) and `changes_tree` (2608). Existing steps that hand back ready (`ship` then
`handback ready`) must still pass with the new head, dirty and pushed checks: the scenario's own
`commit`/`push`/`ship` helpers (402-431) push before `ship`.

1. After a passing `gate`, the log's first line holds the CR and the 40-character HEAD, and the
   event holds the same SHA.
2. In a repository with `core.abbrev` set to 12, `gate`, `ship`, `verdict` then `handback ready`
   succeed (fails on main today).
3. `gate` on a worktree with a modified or untracked file exits 2 and runs nothing.
4. A gate command that commits during the run leaves no pass at either head.
5. `handback ready` exits 2 with the named cause for: a commit made after `ship`; a dirty tree; a
   head not pushed; a gate passed only at an earlier head. With `--no-gate` the first three still
   refuse.
6. A batch record holding short-head events from before the change still reaches `handback ready`.
7. With `spent_usd` at or over `budget_usd`, `round` exits 5 with a budget message and the round
   count unchanged; `gate`, `verdict`, `ship` and `handback` still work. With no budget, `round` is
   unchanged, and the round-limit refusal keeps its own message.
8. `restore 6-trash/<stamp>-<slug>` puts `1-inbox/<slug>` back with its files and updates
   STATUS.md; a former batch CR loses its number.
9. A name clash exits 2 with nothing moved, and `--slug` resolves it; an item from `5-archives` is
   refused.
10. After restoring a cancelled CR of a paused batch, `close` (without `--yes`) still runs.
11. `driver.md`, `foreman.md`, `concepts.md`, the rails docstring and the `round` help say the same
    thing about the budget. `just check` and `just scenario` pass on both forges.

Runs in parallel with `driver-liveness`; no `depends.json`.

## Open questions

None.
