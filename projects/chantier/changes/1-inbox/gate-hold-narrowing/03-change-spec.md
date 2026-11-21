# gate runs only named commands; lease hold runs nothing

Step 2 of the permissions-bypass split (perm-bypass-Q17). Today `chantier gate <cr> "<command>"`
runs any text through a shell (`commands/gate.py`, `_spawn`, lines 113-114) and
`chantier lease <unit> hold -- <command>` runs any program (`commands/leases.py`, `_hold`, line 95).
Both are chantier commands, so chantier's allow rules let them through with no prompt: an agent
with Bash can run anything through them. This CR closes those two doors.

Built as if CR-432 (permissions-bypass, step 1: real paths in P10's chantier rules) had landed.

## Goal

In the user's terms: `gate` runs only the long gate the project wrote down in `chantier.yaml`,
asked for by its name; `lease hold` runs nothing, it only keeps a lease alive for a while. A
project with no gate written there is offered the entry once, written on the user's yes.

Known limit (gate-hold-Q2's restatement): `just scenario` runs the worktree's justfile, which a
Coder edits. This guards against the read-only roles (Inspector, Verifier...) running anything
through chantier, not against a Coder.

## Decisions carried from the grill

- perm-bypass-Q1 (held by gate-hold-Q2): `gate` runs only a command named in `chantier.yaml`,
  called by its name (`gate CR-430 scenario`); a free command is refused.
- perm-bypass-Q9 (held): at its first turn, the Chief of Staff that sees a declared long gate with
  no command configured offers the `long_gate.commands` entry, written on the user's yes; the
  no-setup bullet of `AGENTS.md` says a runnable long gate needs it.
- perm-bypass-Q14 (held): chantier's own gate is in the root `chantier.yaml` of chantier's
  repository, shipped in this CR's PR: `long_gate.commands.scenario: just scenario`.
- perm-bypass-Q15 (held): `AGENTS.md` names the gate by its name (the long gate `scenario`); the
  command text lives only in `chantier.yaml`.
- gate-hold-Q1: `lease hold` runs no command. It keeps the lease live 45 minutes by default;
  `--minutes N` sets up to 90 at most; the Driver runs it again when it needs longer. This
  replaces perm-bypass Q2 and Q13 (`--pid` is dropped).
- gate-hold-Q3: destination batch-30, after CR-432.

## What changes

Paths: `CLI/` is `skills/chantier/scripts/cli/src/chantier/`, `REF/` is
`skills/chantier/references/`, `TESTS/` is `skills/chantier/scripts/cli/tests/`.

### 1. The `long_gate.commands` key (`CLI/playbook/config.py`, `CLI/playbook/layers.py`)

```yaml
long_gate:
  parallel: 1
  commands:
    scenario: just scenario
```

- `_long_gate` (config.py, lines 298-318) accepts a second key, `commands`: a map from a name
  (one word: letters, digits, `-`, `_`) to one command (a non-empty string). Anything else is a
  problem with its line, as for `parallel`. `long_gate: commands:` alone (no `parallel`) is valid;
  the error text "holds its key: `parallel:`" and "one of parallel" name both keys.
- `load_long_gate` (layers.py, line 386) also returns the names and their commands (none when
  absent). The shipped defaults (`config/chantier.defaults.yml`) hold no command.
- The layers are read from the main repository even when `gate` runs in a worktree (`Repo.root`),
  so a worktree's own `chantier.yaml` does not change which command a name runs.
- The board's Configuration page and `config.put` edit only the two limits and the roles: a save
  keeps `long_gate.commands` as it is.

### 2. `gate` runs names (`CLI/commands/gate.py`, `CLI/declare/gate.py`)

- New form: `gate <cr> <name> [<name>...]`. Each name is looked up in `long_gate.commands`; the
  gate runs their commands in the order given, as today (stop at the first failure, the queue, the
  slots, `--stop`, `--first`, the dirty-tree refusal, the moved-head rule: all unchanged).
- Refused before anything runs or is logged (exit 2, `EXIT_USAGE`):
  - a word that is not a configured name (a free command such as `"just scenario"` included):
    `gate <cr>: "<word>" is not a long gate named in chantier.yaml (long_gate.commands); named: <names>`;
  - no `long_gate.commands` at all: `gate <cr>: chantier.yaml names no long gate
    (long_gate.commands: <name>: <command>); the Chief of Staff offers it to the user`.
- The command text a name gives is run as today (same process group, same log, through the shell
  as written in `chantier.yaml`: the text there is the user's, written on the user's yes).
- The log's `$ ` line and each `gate` event keep the command text run, and also carry the name, so
  `handoff`, `status` and the carry logic read as before.
- `declare/gate.py`: the positional becomes `name` ("the long gate's names from chantier.yaml's
  long_gate.commands, run in order"); the command's help says so.

### 3. `lease hold` runs nothing (`CLI/commands/leases.py`, `CLI/core/leases.py`, `CLI/declare/driver.py`)

- New form: `lease <unit> hold --lease <n> [--minutes N]`. `N` is a whole number from 1 to 90,
  45 when absent; outside that range, refused (exit 2). Anything after `--` is refused (exit 2):
  `lease hold runs no command: start your wait yourself, then run lease <unit> hold --lease <n>`.
- What it does: the same checks as `renew` (a stale number stops it), then sets the lease's expiry
  to now + N minutes, logs one `lease` event with `minutes`, prints the lease line (live until
  `<hh:mm>` UTC) and exits 0.
- A later renewal (any command with `--lease`, or `renew`) never shortens an expiry set by `hold`:
  a renewal sets the expiry to the later of the current one and now + the TTL.
- The `.lease-hold.<unit>.<k>.run` records go: `write_hold`, `hold_records`, `HOLD`,
  `_HOLD_NAME`, `Liveness.holds` and the "held by N background task(s)" text are removed. A lease
  is live while it has not ended and it expires in the future or a long gate of the CR runs or
  waits (the module docstring says so).
- The board: `board/crs.py` (line 72-79) drops `holds` from the lease facts, `board/fingerprint.py`
  (line 23) stops watching the records, and `clients/tui/model.py` (line 55) drops its line.
  `docs/server-api.md` (`project.state`, line 78) drops `holds` from the lease object: a change of
  the published API, named in the PR's body.
- `USAGE` (leases.py, line 17) and the `lease` help (driver.py, lines 128-137) give the new form.

### 4. chantier's own repository

- New root `chantier.yaml` (Q14): `long_gate:` / `commands:` / `scenario: just scenario`.
- `AGENTS.md`:
  - the Windows coverage sentence: "passes `just scenario` locally (`chantier gate`)" becomes
    "passes the long gate `scenario` locally (`chantier gate <cr> scenario`)" (Q15); the pipeline
    job's name `just scenario (ubuntu-latest)` stays, it is the CI job's name;
  - the no-setup bullet: a runnable long gate needs its `long_gate.commands` entry in
    `chantier.yaml` (Q9); the `.lease-hold.*.run` records (lines 20-21) are removed from what
    chantier writes;
  - the lease bullet (lines 101-105): "`lease hold` runs only what a Driver gives it, to keep a
    lease live" becomes "`lease hold` runs nothing: it keeps a lease live for a bounded time (45
    minutes by default, 90 at most)".

### 5. Cards and docs

- `REF/driver.md`:
  - "Means: the long gate" (lines 207-217) and the lines 209, 560, 1101: `$CHANTIER gate <cr>
    <name>…`, the names from `chantier.yaml`'s `long_gate.commands`; a refused name is a
    `blocked` line to the steering session, never a free command; "one command per argument"
    becomes "one name per argument".
  - "Means: CI" (line 226): start the forge's watch in a background shell yourself, then
    `lease <cr> hold --lease <n>` (45 minutes; `--minutes` up to 90), end your turn.
  - "Means: the lease" (lines 755-757): a wait over 3 minutes runs `lease <cr> hold --lease <n>
    [--minutes N]` before the wait; run it again at a wake when the wait goes on; `hold` runs
    nothing. "A long gate of yours ... keeps the lease live with no `hold`" stays.
  - Stack driver (lines 1315-1317): before its local gate, `lease stack hold --lease <n>
    --minutes 90`, then `$CHANTIER gate <cr> <name>`; run the hold again at each wake while the
    gate runs or waits (a CR's gate keeps that CR's lease live, not the stack's).
  - QA driver (line 1328): `lease O-k hold --lease <n> [--minutes N]` before a long test.
- `REF/verifier.md` (line 76) and `REF/concepts.md` (lines 433, 437): the named form; concepts'
  long gate entry says the commands live in `long_gate.commands`.
- `REF/chief-of-staff.md`:
  - lines 95-102: at the first turn, a long gate declared in the project's rules with no
    `long_gate.commands` entry (`$CHANTIER playbook`) is a question to the user, with the exact
    lines proposed (a name and the rules' command), written on the user's yes (Q9). When the user
    says "our long gate is `<command>`", the proposal is the `AGENTS.md` line naming the gate by
    its name and the `chantier.yaml` entry holding the command.
  - the `chantier.yaml` example (lines 155-170) shows `commands:` under `long_gate:`.
- `REF/init.md` (step 1, lines 68-87): with the long gate line, the `long_gate.commands` entry is
  proposed too, on the same yes; "one command per item" stays for `AGENTS.md`.
- `REF/hosts/claude-code.md`: the sentence CR-432 adds to the "Risk accepted" of the chantier rows
  (lines 267-269: "`gate` and `lease hold` still run the command they are given, until
  `gate-hold-narrowing`") becomes "`gate` runs only the long gates `chantier.yaml` names, and
  `lease hold` runs nothing".
- `docs/gates.md`: the long gate is declared in two places: `AGENTS.md` names it, `chantier.yaml`'s
  `long_gate.commands` holds its command; the example shows both. `docs/planning-folder.md`
  (line 54): the `.lease-hold.*.run` records are removed.

Both hosts' agent files are untouched (their bodies stay identical).

### 6. Where this touches CR-432's code

- `CLI/commands/permissions.py`: no change here. CR-432 edits its chantier rows of `SAMPLES` and
  the rule functions; this CR changes what those rules let run, not the rules. A Driver rebasing on
  CR-432 has no conflict there.
- P10 (`CLI/commands/preflight.py`): no change.
- `REF/hosts/claude-code.md`: the one sentence in the chantier rows' "Risk accepted" (section 5),
  which CR-432 writes; this CR rewrites it.
- `AGENTS.md`: CR-432 leaves it unchanged; this CR edits it (section 4).

## Out of scope

- The allow rules themselves and P10 (CR-432). The push rules (dropped, perm-bypass-Q17).
- The fast gate, run by agents directly, never through `gate`.
- A Coder editing the justfile or the scripts a named command runs (the known limit).
- `handback --no-gate`, exemptions and a pipeline job named as the long gate: unchanged.

## Default and configured matrix

| Cell | Expected |
| --- | --- |
| Shipped defaults only (no `long_gate.commands`) | `gate <cr> <anything>` refused, exit 2, the text naming the key; nothing logged |
| `long_gate.commands.scenario` set, `gate <cr> scenario` | runs the command, as today's gate |
| Same, `gate <cr> "just scenario"` (a free command) | refused, exit 2, listing `scenario` |
| Two names, `gate <cr> a b` | runs a then b; stops at a's failure |
| `long_gate.commands` set in the surface's project folder or root | the same (the layers merge as for `parallel`) |
| A worktree's own `chantier.yaml` changes a name's command | ignored: the main repository's layers are read |
| `lease hold`, no `--minutes` | live 45 minutes |
| `lease hold --minutes 90` / `--minutes 91` / `-- cmd` | live 90 minutes / refused / refused |

## Evidence

- Tests (`TESTS/`, in-process, parametrized, within `AGENTS.md`'s time budget):
  - the config key: `commands` accepted; a bad name, an empty command and an unknown key under
    `long_gate` each give a problem with its line;
  - `gate` refuses, before any log or event, a free command, an unknown name and a project with no
    entry; with an entry, the event carries the name and the command;
  - `lease hold`: default 45, `--minutes 90` accepted, 0, 91 and a `--` command refused; a renewal
    after a hold does not shorten its expiry; no `.lease-hold.*` file is written;
  - one test reads the repository's root `chantier.yaml` as it ships, at the head under test, and
    checks `long_gate.commands.scenario` is `just scenario`; another reads `AGENTS.md` as it ships
    and checks it names `chantier gate <cr> scenario`.
- Scenario (`scenario/run_scenario.py`): its workspace's `chantier.yaml` gets the names its gates
  use (`GATE`, line 59, and the slow and queue gates of lines 4769-5266, each a name); every
  `chantier("gate", cr, <command>)` becomes the name; one new check: a free command is refused,
  exit 2, nothing logged. Section 3a (lines 914-952) becomes: `lease hold --minutes 1` with the
  shortened TTL keeps the lease live past the TTL, then not confirmed after the minute; a `--`
  command is refused.
- Eval kit: `evals/kit/dry_run.py` (lines 69, 439) writes `long_gate.commands` in its workspace's
  `chantier.yaml` and calls the gate by name; `just eval-dry-run` passes.
- Gates owed (`AGENTS.md`): `just check`, `just eval-dry-run` (the CLI's `src/` and the eval kit
  change), the pipeline's `just scenario (ubuntu-latest)` job at the PR's head, and, on top of the
  stack, the local `chantier gate <cr> scenario`. No `hooks/` or `types/` change.

## Open questions for the Chief of Staff

1. **A wait longer than 90 minutes.** The stack driver's local gate (queue plus run) and a slow CI
   watch can pass 90 minutes; past the hold, the lease is "not confirmed" (not a failure, but the
   steering session may then reclaim it). The spec has the Driver run `hold` again at each wake.
   Should a running or queued long gate also keep the stack lease live by itself, as it already
   keeps the CR's?
2. **The eval's sandbox and fixture.** `evals/kit/sandbox/AGENTS.md` and `evals/kit/fixture/AGENTS.md`
   declare a long gate with no `chantier.yaml`. Ship a `chantier.yaml` with the entry in both (the
   eval then does not see the Chief of Staff's offer of Q9), or leave them bare so a real eval
   exercises the offer (its first gate is refused until the user says yes)?
3. **User projects mid-batch.** A project that updates the plugin during a running batch has every
   `gate` refused until the entry is written; the Chief of Staff offers it at its next first turn
   (Q9). Is that acceptable, or should the release notes tell users to add the entry before
   updating?
