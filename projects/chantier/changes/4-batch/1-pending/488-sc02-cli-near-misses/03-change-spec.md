# SC02: Accept the CLI's near-miss argument forms

Child 2 of 28 of the program CR `simplify-cards-and-prompts` (folder
`1-inbox/simplify-cards-and-prompts`). Its `03-change-spec.md`, its `02-answers.md` answers 17
to 22 and its `work/study-*.md` rank above this file. One Driver, one PR, in the program's single
stack batch (batch-31).

Code read: `origin/main` at `8a960d34` (chantier 0.15.1 plus CR-471). Short forms:
- `src/` is `skills/chantier/scripts/cli/src/chantier/`;
- `tests/` is `skills/chantier/scripts/cli/tests/`.

## Goal

Answer 3 (simplify-cards-Q6): no stumbling on the common path. A usage error or refusal seen in
more than 2 % of a role's runs is a tool bug, not a card gap. study-behaviour section 3.2 counted
six such stumbles: S1, S2, S3, S6, S9 (with S8) and S10. Each costs a failed call, then a
`--help`, then a retry. This child makes the CLI accept the form the agent typed when that form
can mean only one thing, gives it the same effect as the canonical form, and lists it in the
command's `--help`. No card changes. The agents keep typing what they type, and it now works.

## Place in the chain

- **Base:** child 1's branch (`push-own-cr-branch`). Child 1 adds `chantier push` and its lease
  check (three leases count: the CR's own, the stack's, a QA order's). This child may reuse that
  choice (see S1).
- **Depends on it:** child 3 (`refusals-name-next-step`, M9) is built on this branch. Every new
  refusal text written here names a backticked next command, so child 3's gate passes on them as
  written.
- **Merge:** children 1 to 18 keep the old cards working. This child may merge, in order, once
  the owner says so. Nothing merges while the owner sleeps; the child is handed back as ready.

## What changes

### One argv step for the forms argparse would reject: new `src/near_misses.py`

- New module `src/near_misses.py`, with `normalize(argv: list[str]) -> list[str]`. It rewrites
  only the two forms below (S2 and S10). Any other argv comes back unchanged, element for
  element.
- To find the command name, the function skips the root options and their values (`--project`,
  `--profile`, `--skill`, also in their `--opt=value` form). The command name is the first token
  that is not an option.
- Callers:
  - `src/cli.py`, `main`: `argv = normalize(sys.argv[1:] if argv is None else argv)` before
    `parser.parse_args`. The same normalized list goes to `client.forward`, so a profile's
    server gets the canonical form.
  - `src/board/cli_run.py`, `judge`: normalizes `a.argv` before `parser.parse_args`. Otherwise
    `cli.run` would refuse a form that the local CLI accepts.
- The module imports only `chantier.core.phases` and the command names that declare `--epoch`.
  It never imports pydantic or a command module: `tests/test_cli_units.py`-style start-up time
  is unchanged.

### S1: `--lease N` on every command a Driver runs against a CR or unit

The commands are the program's list: `handoff`, `verdict`, `rules`, `log`, `wait` and `lease`.

- **Declaration.** `handoff` (`src/declare/facts.py`), `verdict` (`src/declare/delivery.py`),
  `rules` (`src/declare/rules.py`), `log` and `wait` (`src/declare/driver.py`) call
  `add_lease(s)` from `src/commands/registry.py` (optional, never required).
- **Effect, by command.** In each case the check is `leases.claim(..., required=False)` in
  `src/core/leases.py`:
  - a missing `--lease` changes nothing;
  - a valid lease renews;
  - a number that is not the unit's current lease, or a lease that has ended, exits 3 with
    `claim lost: …; stop now: nothing recorded`.
  - `handoff <cr>` and `log <cr>` read only. With `--lease`, they renew through
    `leases.renewed_in_session(repo, batch, unit, args.lease, what=f"handoff {cr}",
    required=False)`, which logs a `lease` event, as `gate` does. Without `--lease`, they write
    nothing, as today.
  - `verdict <cr> …` claims inside its existing `RenderedBatch`, before `b.log("verdict", …)`, so
    the verdict event saves the renewal. A stale lease refuses before the verdict is recorded.
  - `wait <cr> add …` (a CR of the batch) claims inside its `RenderedBatch` in `_in_batch`. When
    `--epoch` is given, the steering session runs it and the lease is ignored: `claim(epoch=…)`
    already returns None. `wait <cr>` with no action and `--lease`, on a CR of the batch, renews
    in its own session, like `handoff`.
  - `wait <backlog folder> …` holds no lease, so `--lease` is ignored.
  - `rules` names no unit, so `--lease` is accepted and ignored.
- **Which unit the number claims.** A stack driver's or a QA driver's number must never read as
  `claim lost` against the CR's own lease. The number claims, in this order:
  1. the stack's lease (unit `"stack"`), when the CR is in a stack batch's chain and the stack
     lease's number is N;
  2. an open QA order's lease on that CR (unit `O-k`), when its number is N;
  3. otherwise the CR's own lease. That one exits `claim lost` when N is stale. A CR with no
     lease (a batch opened before leases) ignores N, as `claim` does today.

  If child 1's branch already holds this choice as a helper in `src/core/leases.py`, reuse it.
  Otherwise add it there as `leases.unit_for(d: BatchRecord, cr: str, number: int | None) -> str`
  and leave `push` as child 1 left it.
- **`lease`.** `src/declare/driver.py`, `_register_lease`, adds `add_lease(s)`. Then `lease
  --lease 3 CR-7 renew` (the number before the unit) parses. `src/commands/leases.py`, `lease`,
  merges it with the number `_parse` finds in `rest`. Two different numbers exit 1 (usage) with
  `lease <unit>: --lease given twice (<a> and <b>); `lease <unit> renew --lease <n>``. Also,
  `lease <unit> --lease N` with no action is `renew` (today it says "say `renew` or `hold`"). A
  lease given with no number and no action still shows the lease, as today.
- **Help.** `add_lease`'s help text gains one variant for these commands: "accepted on this
  command too: a valid one renews, a stale one exits 3 (`claim lost`); without it nothing is
  checked". `rules` says "accepted and ignored: `rules` names no unit". `handoff`'s command help
  becomes "the CR's facts, for any agent; changes nothing (with --lease: renews it)".

### S2: `phase <cr> "gate preflight"`

- In `normalize`: when the command is `phase`, find its second positional. Skip `--lease`,
  `--batch` and the root options with their values. If that token holds a space and its first
  word is one of `PHASES` (`src/core/phases.py`), split it on its first space into two tokens:
  the phase, then the rest as the first word of the detail. Everything else stays as typed.
- The result is exactly `phase <cr> gate preflight`. The handler `phase` in
  `src/commands/driver_notes.py` and its 40-character detail limit are unchanged.
- A token whose first word is no phase (for example `"gate-ish x"`) is not touched. argparse
  refuses it as today (`invalid choice`, exit 2), so a canonical refusal keeps its text and code.
- The `phase` declaration (`src/declare/driver.py`, `_register_notes`) keeps `choices=PHASES`.

### S3: a Driver's `take` names `handoff`

- `src/core/batch.py`, `require_epoch(epoch, usage, tail: str = "")`: the refusal appends `tail`
  when given.
- `src/commands/driver.py`, `take`, for a CR (not `stack`), passes ``tail=f"; a Driver does not
  take: `handoff {args.cr}` prints the take's facts"``. The full refusal reads ``take CR-7
  --epoch <n>: the steering session's command; <n> is your number as Foreman of the batch
  (Foreman n°<n>); a Driver does not take: `handoff CR-7` prints the take's facts``.
- The exit code (2) and the words `the steering session's command` stay, because
  `scenario/run_scenario.py` (around line 6373) matches them. `take stack` keeps today's text.
- One-Driver-per-CR is not touched: `check_take` in `src/rails.py` (the `c.agent` refusal,
  ``agents set CR-N - --epoch <n>` first``, lines 256 to 260) stays as it is (F12).

### S6: CR folder paths and short names

- **Path forms.** These go in `Repo.planning_path` (`src/core/repo.py`), so every caller gets
  them. A relative value is resolved as today first, from the planning folder. Only when that
  path does not exist are two more readings tried:
  1. **The planning prefix repeated.** If the value (with `\` read as `/`) starts with the
     planning folder's path as seen from the session's root, that prefix is stripped. In a
     surface the prefix is `projects/<name>/changes/`; in a project it is `.agents/changes/`. A
     prefix that repeats is stripped as many times as it leads. Example:
     `projects/chantier/changes/1-inbox/x`, or
     `projects/chantier/changes/projects/chantier/changes/1-inbox/x`, reads as `1-inbox/x`.
  2. **Relative to the shell's folder.** When the process's real working folder
     (`os.getcwd()`, never `CHANTIER_ROOT`) is inside the planning folder, the value is read from
     there. So `.` or `work/..` from inside `1-inbox/x` is `1-inbox/x`. This reading is skipped
     when the command runs through `cli.run` (the env `wire.VIA_SERVER` is set), because a
     client's folder is not the server's.

  A reading is kept only if it exists and lies strictly inside the planning folder. If several
  readings exist and differ, the command exits 1 with `<value> is ambiguous: name it as `<a>` or
  `<b>``. If none exists, the value comes back as today, so each caller keeps its own refusal
  (`not a CR folder: …`, `triage expects a CR folder: …`). A value that resolves today is never
  read another way.
- **Short names.** A new function, `lifecycle/stages.py`: `cr_folder_arg(repo, item, label)`.
  It returns `repo.planning_path(item, label)` when that path exists. Otherwise, when `item` has
  no `/` and no `\`, it looks the name up among `cr_folders(repo.store, stage_layout(repo),
  include_archives=True)` (every stage but `6-trash`):
  - exactly one match: that folder;
  - several matches: exit 1 with `<name> names several CR folders: name one: `<rel-a>`,
    `<rel-b>``;
  - no match: as today.

  Each command's own stage refusal then applies unchanged. For example, `triage` of a CR in
  `4-batch/` is still refused.
- **Call sites switched to `cr_folder_arg`**, the ones that expect a CR folder:
  - `commands/summary.py` `_cr_folder` (`summary lint`, `set`, `label`, `group`);
  - `commands/intake.py` `triage` (line 104) and `abandon` (line 116);
  - `lifecycle/backlog.py` `move_item`;
  - `lifecycle/stages.py` `move_backlog_item` and `prepared_cr` (`open`, `order add --note`);
  - `lifecycle/running_batch.py` `mark_running_batch` (`triage --running-batch`);
  - `commands/waits.py` `_folder` (a backlog CR's `wait`).

  `restore` keeps `planning_path`: its folders sit in `6-trash`, which the lookup leaves out.
  Recorded paths (`c.path`) and `fix` files keep `planning_path`.
- **`file` is not covered.** The program's list names `summary`, `triage` and `file`, but
  `file`'s argument is the request's text or `@path`, not a CR folder. Reading a short name there
  would turn a request text into a folder, which changes the meaning. The program's Must-not
  forbids that, so `file` is left as it is. The PR says so in Known gaps.

### S9 (with S8): `summary lint` prints the limits and the exact `summary set` form

`src/summaries/gaps.py`, `gap_line`: every gap that `summary set` closes ends with a complete
form naming both limits (`TITLE_MAX` 72, `SUMMARY_MAX` 300 from `core/records.py`):

- no summary: `→ summary set <path> --title "<one line, at most 72 characters>" --summary "<one
  line, at most 300 characters: the CR's state now>"`;
- late: `→ read them, then summary set <path> --summary "<one line, at most 300 characters>" or
  summary set <path> --unchanged`;
- long title: as today, plus `(limit 72)` already in the text. Unchanged but for the placeholder
  wording, which uses the same form;
- unreadable: `→ repair or remove it, then summary set <path> --title "<…72…>" --summary
  "<…300…>"`, the no-summary form. `tests/test_validate.py` line 264 is updated to the new end;
  `validate` prints the same `gap_line`.

The head line (`N gap(s) in M CRs`) and `no gap (M CRs)` are unchanged, because
`scenario/run_scenario.py` (lines 11324, 11582, 11590) and `tests/test_summary_lint.py` match them
exactly. `summary set --help` already shows both limits; its `folder` help gains "or the CR's
short name".

### S10: `--epoch` in any position

- In `normalize`: a `--epoch N` or `--epoch=N` found before the command name is moved to just
  after the command name. This is done only when that command declares `--epoch`: the
  `BATCH_EPOCH` commands, each named in `near_misses.EPOCH_COMMANDS`, a tuple a test keeps equal
  to the parser's. This is the measured case: `$CHANTIER --epoch 3 take CR-7`, where `$CHANTIER`
  ends with `--project …`, which argparse rejects today as `invalid choice: '3'`.
- After the command name, argparse already accepts `--epoch` anywhere, so nothing is added there.
- F12: `take` never clears a recorded Driver by itself. The refusal ``agents set CR-N - --epoch
  <n>` first`` stays word for word.

### `--help` lists every accepted form

Each command touched gains an `epilog` (with `formatter_class=argparse.RawDescriptionHelpFormatter`
so each form stays on its own line), headed `also accepted:`. One line per form:

| Command | Form listed |
| --- | --- |
| `handoff`, `log`, `verdict`, `wait` | `--lease N`, renewed when valid |
| `rules` | `--lease N`, ignored |
| `lease` | `--lease N` before the unit; `lease <unit> --lease N` = `renew` |
| `phase` | `phase <cr> "<step> <detail>"` = `phase <cr> <step> <detail>` |
| `summary` (each action), `triage`, `abandon`, `open`, `wait` | a path repeating the planning prefix; a path from a shell inside the planning folder; the CR's short name |
| every `BATCH_EPOCH` command | `--epoch N` before the command name |

`take` gets no epilog: its forms are unchanged, and only its refusal text grows.

## Decisions carried

| Source | Decision | Here |
| --- | --- | --- |
| Answer 3 (simplify-cards-Q6) | A stumble in more than 2 % of a role's runs is a tool bug | the whole child |
| Program child 2, S1 | `--lease` on `handoff`, `verdict`, `rules`, `log`, `wait`, `lease`, through `add_lease`; valid renews, unneeded ignored, stale exits `claim lost` | S1 |
| Program child 2, S2 | the quoted phase is split on its first space | S2 |
| Program child 2, S3 | a Driver's `take` refusal names `handoff <cr>` | S3 |
| Program child 2, S6 | the repeated prefix, a path from inside a CR folder and the short name resolve | S6 |
| Program child 2, S9 / study S8 | `summary lint` prints the limits and the exact `summary set` form | S9 |
| F12 (answer 22) | `take` never clears a recorded Driver; of S10 only `--epoch` in any position | S10, S3 |
| F14 (answer 22) | M9 is split out of this child (child 3) | out of scope |
| F20 (answer 22) | the added `just test` seconds are stated | evidence |
| Program Must-not | no canonical behaviour changed, no meaning-changing form, rail at `rails.py:256-260` intact, no card touched | throughout; `file` left out |

## Out of scope

- M9 (every refusal names its next command): child 3. This child's new refusals already do.
- `take` clearing a recorded Driver (F12). `take` accepting `--lease` (see the open question).
- `--epoch` on a command that does not declare it (for example `handoff --epoch 3`): see the open
  question.
- `--lease` before the command name.
- Inferring `--project` from a shell inside `projects/<name>/`. study-behaviour S6 counts 70 of
  the refusal "this is a planning surface with projects …: pass --project". The program's S6
  names only the path forms and the short name; that refusal goes to M10 through child 5's S-list.
- S4, S5, S7, S8 beyond its `summary lint` line, S11, S12, S13 (the program's Out of scope).
- Any card, wrapper, `SKILL.md`, hook or AGENTS.md text.
- A new command: none is added, so no scenario step and no coverage bullet are owed.

## Acceptance evidence

- **New `tests/test_near_misses.py`**, in-process through the `chantier` fixture (`run.bare` for
  the lease cases, so the fixture adds no lease of its own), on the prepared batch states the
  other tests use. It is parametrized with one case per form. Each case runs the canonical form
  and the near-miss form on twin states and asserts the same exit code and the same effect (the
  record's changed fields, the events logged, the files moved, the output lines):
  - S1: `handoff`, `log`, `verdict`, `wait <cr> add`, `wait <cr>`, each with a valid `--lease`
    (renewed: `renewed` moves, one `lease` or command event), with a stale `--lease` (exit 3,
    `claim lost`, the record unchanged), and with no `--lease` (nothing written for `handoff`
    and `log`). `rules --lease 3` gives the same output as `rules`. A stack batch's
    `handoff <cr> --lease <stack n>` renews the stack lease and never exits `claim lost`
    against the CR's ended own lease. `lease --lease N CR-7 renew` equals `lease CR-7 renew
    --lease N`. `lease CR-7 --lease N` equals `renew`. Two different numbers exit 1.
  - S2: `phase CR-7 "gate preflight"` equals `phase CR-7 gate preflight` (phase, detail,
    event). `phase CR-7 "gate-ish x"` exits 2 with argparse's `invalid choice`, as today.
  - S3: `take CR-7` without `--epoch` exits 2, and its text holds both `the steering session's
    command` and ``handoff CR-7``. `take stack` without `--epoch` is unchanged.
  - S6, on an external surface and on an in-project planning folder:
    - the prefix form, once and doubled;
    - `.` from a `monkeypatch.chdir` into the CR folder;
    - the short name. Each is checked on `summary set`, `summary lint <folder>`,
      `triage --priority P2`, `wait <folder> add` and `open` (one command per form is enough
      when the code path is shared; at least one case per form).
    - An ambiguous short name, the same name in `1-inbox/` and `5-archives/`, exits 1 and names
      both paths.
    - A value that resolves today keeps its reading, even when a CR of that short name exists
      elsewhere.
  - S9: a no-summary gap line and a late gap line each contain `72` and `300` and a full
    `summary set <path> --title "…" --summary "…"` (or `--unchanged`) form. The head line is
    unchanged.
  - S10: `["--project", <p>, "--epoch", "3", "take", "CR-7", ...]` equals the canonical
    order. `["--epoch", "3", "handoff", "CR-7"]` keeps today's argparse refusal.
    `near_misses.EPOCH_COMMANDS` equals the set of subparsers of `cli._parser()` that hold an
    `--epoch` option.
  - `cli.run`: `board/cli_run.judge` accepts the S2 and S10 forms, read from the normalized
    argv. The S6 shell-folder reading is not used when `wire.VIA_SERVER` is set.
- **`--help` check:** the same file builds the help from the shipped parser (`cli._parser()`,
  each subparser's `format_help()`) at the head under test, not from a prepared text. It asserts
  that each form in the table above appears in its command's help.
- **Untouched behaviour:** the existing tests pass unchanged, except `tests/test_validate.py`
  line 264 (the unreadable gap line's new end), which the PR names.
- **Rail:** `check_take`'s `c.agent` refusal is asserted word for word (``agents set CR-7 -
  --epoch <n>` first, once it ended``).
- **`just test` time (F20):** the Driver measures `just test` before and after on the same
  machine and states the added seconds under Deliverables. Expected under 3 s (one parametrized
  file, in-process, `-n auto`). The ceiling stays open (`2-backlog/P2/test-ceiling-decision`).
- **Gates (AGENTS.md):**
  - `just check` and `just eval-dry-run` in the worktree before the first push (a change under
    `src/`);
  - the long gate `just scenario (ubuntu-latest)`, green at the PR's head (a CLI change);
  - the local Windows run `chantier gate <cr> scenario` only while this child is the stack's top.
- No host or default matrix: nothing here depends on the host or on a configured value.

## AGENTS.md

No change. No new command, no git or network use, no new configuration.

## Risk

- A form accepted wrongly could hide a real mistake. Each form can mean only one thing, refuses
  when two readings exist, and is listed in `--help`. A value that resolves today keeps its
  reading.
- The S1 unit choice (stack, QA order, own) must not turn a stack driver's valid number into
  `claim lost`. The stack-batch case is tested.
- `normalize` sits in front of every command. Its contract (unchanged argv for any other form)
  is asserted on the whole existing suite, which passes through it.
- `handoff` and `log` gain a write (the lease renewal in `batch.json`, local, never published),
  but only with `--lease`.

## Open questions

1. **`take --lease N`.** study-behaviour S1 also counts Drivers typing `take <cr> --lease N`,
   which argparse rejects before S3's refusal can say "`handoff <cr>` prints the take's facts".
   The program's S1 list leaves `take` out, so this specification does not accept `--lease` on
   `take`. Should `take` accept `--lease N` only so that the call reaches S3's refusal (it
   records nothing, since `take` still needs `--epoch`)?
2. **`--epoch` on a command that does not declare it.** "Accepted in any position" is read here
   as before the command name, the position argparse rejects for the commands that take
   `--epoch`. Commands without it, such as `handoff`, `asks` and `log`, still refuse
   `--epoch 3` (`unrecognized arguments`). Should those accept `--epoch N` and ignore it, as
   `rules` ignores `--lease`?
