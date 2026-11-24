# SC03: Every CLI refusal names the next command (M9)

Child 3 of 28 of the program CR `simplify-cards-and-prompts` (its `03-change-spec.md`, "Child 3",
and its `02-answers.md` answers 9, 17 to 22 rank above this file). One Driver, one PR, in the
running stack batch (batch-31). Code read: `origin/main` at `8a960d34`. Short forms:

- `src/` is `skills/chantier/scripts/cli/src/chantier/`;
- `tests/` is `skills/chantier/scripts/cli/tests/`.

## Goal

The owner's words (answers 1, 9, 17): roles stumble less when the CLI itself says where to go.
A refusal is the working progressive disclosure today (study-behaviour: "a retry follows in the
next call in most cases seen"). M9 makes it a gate: every refusal the batch rails raise names, in
backticks, the next command to run. A refusal that can only say "stop now" is listed, with its
reason, in an allow-list the test counts and prints. Nothing else about a refusal changes.

## Place in the chain

- **Base:** child 2's branch (`cli-near-misses`), the previous CR of the stack. Child 2 may add
  or reword refusal text in the same four files (its S3 and S10 refusals); this child's gate
  covers whatever text is there at its base, child 2's included.
- **Depends on it:** child 4 (`hook-scratch-writes`) builds on this branch. Child 7
  (`help-topics`) later adds `help <topic>` to the lease refusals of `src/core/leases.py`: the
  gate below must accept `help` as a command once child 7 registers it (it reads the command
  names from the parser, so it does with no edit). Children 19 to 24 (the card rewrite) lean on
  these refusals to drop card lines; the read-and-compare review (child 25) cites them.

## Decisions carried

| Source | Decision | Here |
| --- | --- | --- |
| Answer 9 (simplify-cards-Q9), M9 | A refusal names the next command; a pytest gate; final "stop now" refusals in an allow-list in the test | the whole CR |
| Program child 3, Scope | The four files: `rails.py`, `rails_release.py`, `rails_idle.py`, `core/leases.py`; texts that lack a next command are completed, meaning unchanged | "What changes" |
| Program child 3, Must not | No change to a refusal's condition or exit code; no refusal turned into advice; no card touched | "Out of scope" |
| Answer 22, F14 | M9 is its own CR, split out of the near-misses child | this CR |
| Answer 22, F20 | The PR states the seconds its tests add to `just test`, measured before and after on the same machine | "Evidence" |
| Answer 18 | Tools first: this child only adds text; no output the current cards rely on is removed | "What changes": every edit appends to or completes the existing text |
| Program rules | Long gate owed (CLI change); `just check` and `just eval-dry-run` before the first push; the local Windows `scenario` run only if this CR is the stack's top when presented | "Gates" |

## What changes

### 1. Refusal texts (`src/rails.py`, `src/rails_release.py`, `src/rails_idle.py`, `src/core/leases.py`)

A *refusal* is every `ChantierError(...)` constructed in these four files (raised, or returned as
`leases.lost` returns it). There are 36 at `origin/main`. Each completed text keeps its current
words in place and adds the command after them, so every substring the tests and the scenario
read today stays true (one exception, `STOPPED_HINT`, below). Exit codes and conditions do not
move. `<n>`, `<why>`, `<cause>` and `<release-cr>` are literal placeholders, as the texts already
use them. Before writing a command form, check it against that command's `--help` at the base;
the forms below are the ones `origin/main` accepts.

Already compliant, unchanged (a backticked span starting with a command): `check_no_open_batch`
(`close`, `order add`), `check_budget` (`order budget`), `check_take`'s agent-recorded refusal
(`agents set`), `_check_no_held` (`order unhold`), `check_round` (`order rounds`),
`check_stray_round` (`handoff`), `check_granted_fix`'s no-grant refusal (`order add --fix-for`),
`check_grant` (`open --budget`), `check_shape`'s stack refusal (`asks`), `leases.check_free`'s two
refusals (`agents set`, and the command `reclaim_command` returns).

Completed (the "Add" column is the new tail, written as it will read, backticks included; the text before it stays):

| File, function | Today ends with | Add |
| --- | --- | --- |
| `rails.py`, `check_slot` | `no free slot for <what>: <k> of <n> held (<list>)` | `; it waits for a hand-back, or for an `` `order slots` `` from the Chief of Staff` |
| `rails.py`, `check_take` (ready or blocked, no note) | `…only with `` `--note` `` saying why (an answer, a change, a rebase, a red check)` | `: `` `take <cr> --note "<why>" --epoch <n>` `` (with the CR's id in place of `<cr>`) |
| `rails.py`, `check_take` (working, no note) | `…only with `` `--note` `` saying why (resume: <cause>)` | `: `` `take <cr> --note "resume: <cause>" --epoch <n>` `` (the CR's id) |
| `rails_release.py`, `check_granted_fix` (three fixes) | `3 fixes under the grant: another one is the user's go` | ` (`` `order add --fix-for <release-cr>` ``)`, with the release's id |
| `rails_release.py`, `parse_grant` (both errors) | `grant: `` `releases=<n> fixes=<on|off> budget=<usd>` ``, any of them[; not '<word>']` | `; `` `order grant <release-cr> --note "<them>"` `` sets them` (verify the form against `order --help` and `orders_apply._grant`/`release_cr`) |
| `rails_release.py`, `check_shape` (`--outside-stack` on an ask the guard does not refuse) | `…that the stack guard refuses` | `; without it: `` `asks "<text>"` `` |
| `rails_release.py`, `check_shape` (`--outside-stack` reason not naming an open order) | `…that carries the user's word` | `: `` `asks "ready-to-merge <cr>" --outside-stack "O-<k>: <why>"` `` (the CR's id) |
| `rails_idle.py`, `STOPPED_HINT` | `close --stopped <name> for each` | backtick the command: `` `close --stopped <name>` for each `` (see "Scenario" below) |
| `rails_idle.py`, `check_idle` | `…: <causes>. Nothing was deleted.` | ` Run `` `close` `` again once none of these runs.` (before the optional hint) |
| `rails_idle.py`, `_declared` (stack agent) | `clear it: agents set stack - --epoch <n>. Nothing was deleted.` | backtick the command already there: `` clear it: `agents set stack - --epoch <n>`. `` |
| `rails_idle.py`, `_declared` (not an agent the batch holds) | `…it does not block close, drop the flag. Nothing was deleted.` | `drop the flag: `` `close` `` without `` `--stopped <name>` ``. Nothing was deleted.` (the words up to "drop the flag" kept) |
| `rails_idle.py`, `_declared` (no transcript by that name) | `…still running: <names>. Nothing was deleted.` | ` `` `close --stopped <name>` `` takes only a name listed as still running.` (after "Nothing was deleted.") |
| `rails_idle.py`, `_declared` (transcript shows it ended) | `…shows it ended; drop the flag. Nothing was deleted.` | as the not-held one: `drop the flag: `` `close` `` without `` `--stopped <name>` ``.` |
| `rails_idle.py`, `_declared` (transcript cannot be read) | `…covers only an agent that reads as running. Nothing was deleted.` | ` If it is not running, `` `agents set <owner> - --epoch <n>` `` clears it.` with `<owner>` the CR or order id that `held_agents(d)` maps the name to (the same way out `costs/endings.py`'s `_missing` already names); the literal `<owner>` when the name maps to none |
| `core/leases.py`, `lease_of` (unknown order, unknown CR) | `unknown order <unit>` / `unknown CR <unit>` | `: `` `status` `` shows the batch's CRs and orders` |
| `core/leases.py`, `require` and `claim` (missing `--lease`) | `<what> needs --lease <n> (the number take printed)` | `; `` `lease <unit>` `` prints it` (with the unit), before the `_late_ship_tail` when there is one |

Each placeholder in the table (`<cr>`, `<unit>`, `<release-cr>`, `<owner>`, `<name>`) is filled
with the real value where the function has it, exactly as today's texts fill theirs; the command's
first word stays literal text in the source, so the static gate below reads it.

### 2. The allow-list (final "stop now" refusals)

A refusal enters the allow-list only when it says stop, and no command run by the refused caller
lifts it. Seven entries, each with its reason in the test:

| File, function | Refusal | Reason in the test |
| --- | --- | --- |
| `rails.py`, `check_take` | `<cr> is <status>: nothing for a Driver to do` (merged, cancelled) | stop now: the CR has ended |
| `rails.py`, `check_take` | `<cr> waits for <crs>: it starts once each is …` | stop now: it starts by itself once each named CR is met |
| `rails.py`, `check_take` | `<cr> waits for <fixes>: a fix of the release must be merged or cancelled first` | stop now: the release starts once its fixes end |
| `rails_release.py`, `fix_go` | `<cr> is <status>: only a ready fix merges` | stop now: it merges once handed back ready |
| `core/leases.py`, `lost` | `claim lost: …; stop now: nothing recorded` | stop now: the unit is no longer this caller's |
| `core/leases.py`, `ttl_seconds` | `CHANTIER_LEASE_TEST_TTL is seconds, not …` | test seam: set only by the test suite, never met in a batch (see open question 1) |
| `core/leases.py`, `minute_seconds` | `CHANTIER_LEASE_TEST_MINUTE is seconds, not …` | test seam, as above |

### 3. The gate (`tests/test_rail_refusals.py`)

Added to the existing file, with no new fixture:

- **A static scan of the shipped files.** It reads the four modules' source as they ship at the
  head under test (`Path(chantier.rails.__file__)`, `chantier.rails_release`,
  `chantier.rails_idle`, `chantier.core.leases`: the repository's files, never a copied text),
  parses them with `ast`, and visits every `ast.Call` whose callee is `ChantierError`. For each, it
  builds the message's static text from its first argument: string constants, the constant parts
  of f-strings, both sides of a `+`; a formatted value or a call becomes a placeholder. It then
  finds each backticked span and takes its first whitespace-separated word.
- **The command names** come from the CLI's own parser: the subcommand names of
  `chantier.cli._parser()` (so `help`, once child 7 registers it, counts with no edit here).
- **One rule per refusal:** a refusal passes when one of its spans starts with a command name, or
  when its placeholder span is a call to a function named in `COMMAND_HELPERS = {"reclaim_command"}`
  (the one helper whose output is a command; a parametrized case checks that
  `leases.reclaim_command` for a CR, `stack` and `O-1` starts with a command name, short form
  included). Otherwise it must match an allow-list entry, keyed by module, enclosing function and
  a fragment of its static text of at most 40 characters (M13's limit); each entry carries its
  reason.
- **It fails** on a refusal that neither passes nor matches the allow-list (the message names the
  file, the line and the static text), on an allow-list entry that matches no refusal (a stale
  entry), and when the scan finds fewer refusals than a floor (`MIN_REFUSALS = 36`, today's count
  at the base, which the Driver recounts there) so a broken scan cannot pass empty.
- **The allow-list is counted and printed:** the test prints
  `M9: <k> refusals scanned in 4 files, <n> allow-listed` and asserts
  `len(ALLOW) <= MAX_ALLOWED` with `MAX_ALLOWED = 7`: a growth is a visible edit of that number.
- **Behavioural checks on texts this child completes**, by extending assertions the file already
  makes (no new state):
  - `test_slots_zero_holds_and_a_spent_budget_stops_the_next_driver_until_it_is_raised`: the
    no-slot refusal also holds `` `order slots` ``;
  - `test_a_ready_cr_goes_back_to_a_driver_only_with_a_note_and_cancel_needs_the_epoch`: the
    refusal also holds `` `take <one> --note ``;
  - in `tests/test_leases.py`, the parametrized missing-lease case (around line 94): the refusal
    also holds `` `lease <unit>` `` with the unit filled in.

  Each asserts a command span (short), never a phrase.

### 4. Scenario (`scenario/run_scenario.py`)

The scenario reads refusal substrings. All stay true by construction (texts only gain tails),
except `STOPPED_HINT`: the scenario's `hint = "close --stopped <name> for each"` (around line
5322, the `close` transcript section) becomes `` "`close --stopped <name>` for each" ``. No step is
added (no new command) and `tests/test_scenario_coverage.py` is unchanged. The Driver greps the
scenario and `tests/` for each completed refusal's text before pushing; any other exact-text check
found is updated to the new tail, never loosened.

## Out of scope

- Refusals outside the four files: the steering `--epoch` refusal, `Batch.cr`'s
  `unknown CR … in batch`, `costs/endings.py`'s cause texts (they appear inside the `close`
  refusal, unbackticked, and stay so), `commands/`, the board, the writer.
- The hook's refusals (`hooks/register.tsx`, child 4's file; M9's "and the hook's" part is not
  this child's).
- `help <topic>` in any refusal: child 7.
- Any card, `AGENTS.md`, the docs, `evals/`.
- A refusal's condition, order of checks or exit code; turning one into a warning or advice;
  rewording the existing words of a refusal.
- `access`'s own lines (`commands/access.py`): they quote these refusals and gain the tails as is.

## Gates and evidence

- `just test` green, with the new scan and the extended assertions; the PR prints the M9 line
  (`M9: <k> refusals scanned in 4 files, <n> allow-listed`, from `pytest -s -k M9` or `-rP`).
- The added `just test` seconds, measured before and after on the same machine, under the PR's
  Deliverables (expected well under 1 s: one `ast` parse of four files and one parser build).
- `just check` and `just eval-dry-run` (a change under `src/`) in the worktree at the rebased head
  before the first push.
- The long gate `just scenario (ubuntu-latest)` green at the PR's head (the CLI and the scenario
  change). The local Windows `chantier gate <cr> scenario` is owed only while this CR is the
  stack's top; it moves to the CR that joins above it.
- No host or default matrix: the refusal texts do not depend on the host or on a configured
  value.
- The check guards shipped files: the scan reads the four modules from the package at the head
  under test; no prepared text stands in for them.

## Risk

- The scenario and tests read refusal substrings: covered by appending only, by the
  `STOPPED_HINT` edit above and by the Driver's grep.
- A command form written wrong in a refusal sends a role to a usage error: each form is checked
  against `--help` at the base, and the scan checks at least that its first word is a command.
- No `AGENTS.md` change: no new tool, no new exception.

## Open questions

1. sc03-Q1: The two test-seam refusals of `core/leases.py` (`CHANTIER_LEASE_TEST_TTL`,
   `CHANTIER_LEASE_TEST_MINUTE` "is seconds") are not "stop now" refusals, yet no batch ever meets
   them and no command fixes an environment variable. This spec allow-lists them with the reason
   "test seam". The alternative is to leave them out of the scan's scope (the gate would then
   cover 34 refusals). Keep them allow-listed (default), or scope them out?
