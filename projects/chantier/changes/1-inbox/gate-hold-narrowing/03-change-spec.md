# gate runs only named commands; lease hold runs nothing

Step 2 of the permissions-bypass split (perm-bypass-Q17). Today `chantier gate <cr> "<command>"`
runs any text through a shell (`commands/gate.py`, `_spawn`) and
`chantier lease <unit> hold -- <command>` runs any program (`commands/leases.py`, `_hold`).
Both are chantier commands, so chantier's allow rules let them through with no prompt: an agent
with Bash can run anything through them. This CR closes those two doors.

It depends on CR-432 (permissions-bypass, step 1: real paths in P10's chantier rules) and joins
batch-30 after it: the Driver works on CR-432's merged head. Places are named by their text and
their function, never by a line number (CR-432 and the commits since this was written move the
lines); section 6 names where the two CRs meet.

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
- gate-hold-Q4: the eval kit's sandbox and fixture each ship a `chantier.yaml` with the
  `long_gate.commands` entry (an eval tests the batch, not the Q9 offer; a night eval does not
  stop on a question). Section 7.
- gate-hold-Q5: a project updating the plugin mid-batch: the release notes say to add the entry
  before updating; the `gate` refusal names the lines to add; the Chief of Staff offers them at
  its first turn (Q9). No transition period: from this CR on, a free command is refused.
- gate-hold-Q6 (a Fable advisor's answer in the user's place): no new rule for waits longer than
  90 minutes. A long gate keeps only its own CR's lease (`gate_keeping` in `core/leases.py`,
  unchanged: it returns nothing for `stack` and for an order); the stack driver runs
  `lease stack hold --lease <n> --minutes 90` before its gate and again at each wake; past the
  hold the lease shows "not confirmed", the designed safe state, which is no failure. The cap is
  safe because the steering side never takes a unit whose lease is not confirmed without first
  checking with the host that its holder ended: `REF/foreman.md` ("It is refused too (exit 3)
  while the unit's lease is live ... or not confirmed. A `lease not confirmed since …` mark of
  `status` is not a Driver gone ...") and `REF/chief-of-staff.md`, "Steering a batch yourself",
  the **Leases** bullet (the same rule in direct mode); and the holder's next command with
  `--lease <n>` is accepted as `lease-late` (`core/leases.py`, the check that logs
  `lease-late`) while nobody took the unit again.

## What changes

Paths: `CLI/` is `skills/chantier/scripts/cli/src/chantier/`, `REF/` is
`skills/chantier/references/`, `TESTS/` is `skills/chantier/scripts/cli/tests/`.

### 1. The `long_gate.commands` key (`CLI/playbook/config.py`, `CLI/playbook/layers.py`, `CLI/playbook/lines.py`)

```yaml
long_gate:
  parallel: 1
  commands:
    scenario: just scenario
```

- `_long_gate` (config.py) accepts a second key, `commands`: a map from a name (one word:
  letters, digits, `-`, `_`) to one command (a non-empty string). Anything else is a problem with
  its line, as for `parallel`. `long_gate: commands:` alone (no `parallel`) is valid; the two
  error texts that name only `parallel` ("holds its key", "unknown key ... one of parallel") name
  both keys.
- `load_long_gate` (layers.py) also returns the names and their commands (none when absent). The
  shipped defaults (`config/chantier.defaults.yml`) hold no command.
- The layers are read from the main repository even when `gate` runs in a worktree (`Repo.root`),
  so a worktree's own `chantier.yaml` does not change which command a name runs.
- `$CHANTIER playbook` prints one line for it, beside its `ci:` line (lines.py): `long gate:
  <name> (<command>)[, ...] (chantier.yaml: long_gate.commands)`, or `long gate: none named in
  chantier.yaml (long_gate.commands)`. The Chief of Staff reads it for Q9 (section 5).
- The board's Configuration page and `config.put` edit only the two limits and the roles: a save
  keeps `long_gate.commands` as it is.

### 2. `gate` runs names (`CLI/commands/gate.py`, `CLI/declare/gate.py`, `CLI/commands/facts.py`)

- New form: `gate <cr> <name> [<name>...]`. Each name is looked up in `long_gate.commands`; the
  gate runs their commands in the order given, as today (stop at the first failure, the queue, the
  slots, `--stop`, `--first`, the dirty-tree refusal, the moved-head rule: all unchanged).
- Refused before anything runs or is logged (exit 2, `EXIT_USAGE`):
  - a word that is not a configured name (a free command such as `"just scenario"` included):
    `gate <cr>: "<word>" is not a long gate named in chantier.yaml (long_gate.commands); named: <names>`;
  - no `long_gate.commands` at all (Q5: the refusal names the lines to add):
    `gate <cr>: chantier.yaml names no long gate; add to the project's chantier.yaml:` followed by
    the three lines `long_gate:` / `  commands:` / `    <name>: <the long gate's command>`, then
    `(the Chief of Staff offers it to the user)`.
- No transition (Q5): no option, environment variable or version check lets a free command
  through.
- The command text a name gives is run as today (same process group, same log, through the shell
  as written in `chantier.yaml`: the text there is the user's, written on the user's yes).
- The log's `$ ` line and each `gate` event keep the command text run, and also carry the name, so
  `handoff`, `status` and the carry logic read as before.
- `declare/gate.py`: the positional becomes `name` ("the long gate's names from chantier.yaml's
  long_gate.commands, run in order"); the command's help says so.
- `facts.py`, `_gate_lines`: the checklist's `gate <cr> "<cmd>" ["<cmd>"...]` becomes
  `gate <cr> <the configured names, in their order>` (for chantier: `gate CR-n scenario`), or,
  with none configured, `gate <cr> <name> (none in chantier.yaml: ask the steering session)`; the
  `--no-gate` part stays.

### 3. `lease hold` runs nothing (`CLI/commands/leases.py`, `CLI/core/leases.py`, `CLI/declare/driver.py`)

- New form: `lease <unit> hold --lease <n> [--minutes N]`. `N` is a whole number from 1 to 90,
  45 when absent; outside that range, refused (exit 2). Anything after `--` is refused (exit 2):
  `lease hold runs no command: start your wait yourself, then run lease <unit> hold --lease <n>`.
- What it does: the same checks as `renew` (a stale number stops it; a not confirmed lease that
  nobody took again is accepted, logged `lease-late`, as today), then sets the lease's expiry to
  now + N minutes, logs one `lease` event with `minutes`, prints the lease line (live until
  `<hh:mm>` UTC) and exits 0.
- A later renewal (any command with `--lease`, or `renew`) never shortens an expiry set by `hold`:
  a renewal sets the expiry to the later of the current one and now + the TTL.
- A test seam beside `CHANTIER_LEASE_TEST_TTL`, read only in `core/leases.py`:
  `CHANTIER_LEASE_TEST_MINUTE`, the seconds a hold's minute lasts (60 when absent), so the
  scenario sees a hold lapse in seconds.
- The `.lease-hold.<unit>.<k>.run` records go: `write_hold`, `hold_records`, `HOLD`,
  `_HOLD_NAME`, `Liveness.holds` and the text `, held by N background task(s)` are removed. A
  lease is live while it has not ended and it expires in the future or a long gate of the CR runs
  or waits. `gate_keeping` is unchanged (Q6).
- Stale texts fixed (Q6 follow-ups):
  - `core/leases.py`, the module docstring: "..., or a `lease hold` of the unit runs" goes; it
    says a hold sets the expiry ahead;
  - `commands/driver.py`, the stack driver's `lease:` line: "run a long gate under lease stack
    hold --lease {n} -- <command>" becomes "before a long gate and at each wake while it runs or
    waits: lease stack hold --lease {n} --minutes 90";
  - `commands/orders.py`, the QA order's `lease:` line: "run a long test under lease {oid} hold
    --lease {n} -- <command>" becomes "before a long test: lease {oid} hold --lease {n}
    [--minutes N]";
  - `commands/leases.py`, the module docstring ("kept live while a background command runs") and
    `USAGE` give the new form; the `lease` help in `declare/driver.py` too.
- The board: `board/crs.py`, `lease_view`, drops `holds` from the lease facts and its docstring's
  "the running `lease hold`s of this lease"; `board/fingerprint.py` drops `HOLDS` and its comment;
  `clients/tui/model.py`, `lease_left`, drops the `held` branch and its docstring's "else `held`
  when a `lease hold` runs". `docs/server-api.md` (`project.state`) drops `holds` from the lease
  object: a change of the published API, named in the PR's body.

### 4. chantier's own repository

- New root `chantier.yaml` (Q14): `long_gate:` / `commands:` / `scenario: just scenario`.
- `AGENTS.md`:
  - the Windows coverage sentence: "passes `just scenario` locally (`chantier gate`)" becomes
    "passes the long gate `scenario` locally (`chantier gate <cr> scenario`)" (Q15); the pipeline
    job's name `just scenario (ubuntu-latest)` stays, it is the CI job's name;
  - the no-setup bullet: a runnable long gate needs its `long_gate.commands` entry in
    `chantier.yaml` (Q9); "(with the `.lease-hold.*.run` records of `lease hold`, never
    published)" goes from what chantier writes;
  - the `lease` exception's sentence "`lease hold` runs only what a Driver gives it, to keep a
    lease live" becomes "`lease hold` runs nothing: it keeps a lease live for a bounded time (45
    minutes by default, 90 at most)".

### 5. Cards and docs

- `REF/driver.md`:
  - "Means: the long gate": `$CHANTIER gate <cr> <name>…`, the names from `chantier.yaml`'s
    `long_gate.commands` (the facts' checklist and `$CHANTIER playbook` print them); a refused name
    is a `blocked` line to the steering session, never a free command; "One command per argument"
    becomes "One name per argument". The same named form where the card writes
    `$CHANTIER gate <cr> "<command>"…` (the early push's long gate) and
    `$CHANTIER gate <cr> "<the project's command>"…` (the top's local run).
  - "Means: CI": "`lease <cr> hold --lease <n> -- <the watch>`" becomes: start the forge's watch
    in a background shell yourself, then `lease <cr> hold --lease <n>` (45 minutes; `--minutes` up
    to 90), end your turn; and one sentence: a lease "not confirmed" past the hold is no failure,
    and the watch or the gate is never stopped for it ("Means: the lease").
  - "Means: the lease": the bullet "A wait over 3 minutes that runs a command ... runs it as
    `lease <cr> hold --lease <n> -- <command>` ... reads `--batch` and `--lease` only before `--`"
    becomes: a wait over 3 minutes runs `lease <cr> hold --lease <n> [--minutes N]` (45 by
    default, 90 at most) before the wait, and again at a wake when the wait goes on; `hold` runs
    nothing. "A long gate of yours ... keeps the lease live with no `hold`" stays. The "Not
    confirmed" bullet adds: past a hold too, and a running long gate is never stopped for it.
  - Stack driver, **Lease.**: "A long gate you run goes under `lease stack hold --lease <n> -- <the
    gate command>`, which keeps the stack lease live" becomes: before your local gate, `lease
    stack hold --lease <n> --minutes 90`, then `$CHANTIER gate <cr> <name>`; run the hold again at
    each wake while the gate runs or waits (a CR's gate keeps that CR's lease live, not the
    stack's); past the hold the stack lease is "not confirmed", no failure, and the gate is never
    stopped for it.
  - QA driver: "run a long test as `lease O-k hold --lease <n> -- <command>`" becomes "before a
    long test, `lease O-k hold --lease <n> [--minutes N]`; 'not confirmed' past it is no failure".
- `REF/verifier.md` (the sentence that starts "You run `$CHANTIER gate <cr>" and says "one
  command per argument"): the named form. `REF/concepts.md`: the long gate entry (it starts "The
  long gate is `gate <cr>" and says "one command per argument") gives the named form
  and says the commands live in `long_gate.commands`; the lease entry ("a long gate of the CR runs
  or waits, or a hold runs") says a hold sets the expiry ahead instead.
- `REF/chief-of-staff.md`:
  - the first-turn paragraph ("A project with no long gate written down is a question for the
    user ..."): a long gate declared in the project's rules while `$CHANTIER playbook` prints
    `long gate: none named in chantier.yaml` is a question to the user, with the exact lines
    proposed (a name and the rules' command), written on the user's yes (Q9; Q5: this is also how
    a project that updated the plugin mid-batch gets the entry). "When the user says 'our long
    gate is `<command>`', propose the exact `AGENTS.md` lines" becomes: the `AGENTS.md` line naming
    the gate by its name and the `chantier.yaml` entry holding the command, beside the existing
    `long_gate:` / `parallel: <n>` proposal.
  - the `chantier.yaml` example shows `commands:` under `long_gate:`.
- `REF/init.md`, step 1 (the long gate line): the `long_gate.commands` entry is proposed too, on
  the same yes; "one command per item" stays for `AGENTS.md`.
- `REF/hosts/claude-code.md`: the sentence CR-432 adds to the "Risk accepted" of the chantier
  rows of "Allow rules" (its text: "`gate` and `lease hold` still run the command they are given,
  until `gate-hold-narrowing`") becomes "`gate` runs only the long gates `chantier.yaml` names,
  and `lease hold` runs nothing".
- `docs/gates.md`: the long gate is declared in two places: `AGENTS.md` names it,
  `chantier.yaml`'s `long_gate.commands` holds its command; the example shows both; the sentence
  "the Driver passes each as its own argument to `chantier gate`" speaks of names.
  `docs/planning-folder.md`: "and the `.lease-hold.*.run` records of a running `lease hold`"
  goes.
- The release notes (Q5): the PR's body carries a paragraph headed **Before you update**: add the
  `long_gate.commands` entry to the project's `chantier.yaml` before updating the plugin (the
  three lines, an example), since from this version `gate` refuses a free command and every gate
  of a running batch is refused until the entry is there. The Release driver of the next release
  carries it into its notes, where the release-template's sections allow (open question 1).

Both hosts' agent files are untouched (their bodies stay identical).

### 6. Where this meets CR-432's merged head

Read on CR-432's merged head, by text:

- `REF/hosts/claude-code.md`: the one sentence CR-432 writes into the chantier rows' "Risk
  accepted" (section 5 rewrites it). When the merged text differs from the one quoted in section
  5, the Driver rewrites the sentence that names `gate-hold-narrowing`, whatever its words.
- `REF/chief-of-staff.md`: CR-432 edits "The allow rules (P10, Claude Code)" (the **Broad rules**
  and **Stale rules** bullets); this CR edits the first-turn long gate paragraph just above it and
  the `chantier.yaml` example below it. Neighbouring text, no shared sentence.
- `REF/concepts.md`: CR-432 adds a sentence to the `$CHANTIER` entry; this CR edits the lease and
  long gate entries. No shared sentence.
- `scenario/run_scenario.py`: CR-432 changes the P10 section (the settings it writes, a broad
  rules check); this CR changes the workspace's `chantier.yaml`, the gate calls and section 3a.
  No shared function.
- `TESTS/test_cli_runs.py`: CR-432 adds P10 cases; this CR's tests may sit in the same file. No
  shared test.
- `CLI/commands/permissions.py`, `CLI/commands/preflight.py`, `CLI/plugin_files.py`, the four
  SKILL.md files: CR-432's only; this CR changes what the rules let run, not the rules.
- `AGENTS.md`: CR-432 leaves it unchanged; this CR edits it (section 4).

### 7. The eval kit (Q4)

- `evals/kit/sandbox/chantier.yaml` (new): `long_gate:` / `commands:` / `tests: uv run --locked
  pytest -q`, the command of the sandbox's `AGENTS.md` long gate line, word for word.
- `evals/kit/fixture/chantier.yaml` (new): `long_gate:` / `commands:` / `tests: uv run pytest
  -q`, the command of the fixture's `AGENTS.md` long gate line.
- Both `AGENTS.md` files stay as they are (the judge and the sandbox CRs quote their command); the
  Driver reads the name from the facts and `playbook`.
- `evals/kit/dry_run.py`: `GATE` becomes the name `tests` (its comment says so); the PR body's
  test plan text keeps the command; the workspace it builds carries the sandbox's
  `chantier.yaml` (when the build copies tracked files, nothing more to do; else it writes it).

## Out of scope

- The allow rules themselves and P10 (CR-432). The push rules (dropped, perm-bypass-Q17).
- A gate keeping the stack lease live (Q6): `gate_keeping` stays as it is; the stack driver holds
  its lease itself.
- A transition period for the free command (Q5).
- The fast gate, run by agents directly, never through `gate`.
- A Coder editing the justfile or the scripts a named command runs (the known limit).
- `handback --no-gate`, exemptions and a pipeline job named as the long gate: unchanged.
- The Q9 offer in an eval (Q4: the evals ship the entry).

## Default and configured matrix

| Cell | Expected |
| --- | --- |
| Shipped defaults only (no `long_gate.commands`) | `gate <cr> <anything>` refused, exit 2, the text giving the three lines to add; nothing logged; `playbook` prints `long gate: none named` |
| `long_gate.commands.scenario` set, `gate <cr> scenario` | runs the command, as today's gate |
| Same, `gate <cr> "just scenario"` (a free command) | refused, exit 2, listing `scenario` |
| Two names, `gate <cr> a b` | runs a then b; stops at a's failure |
| `long_gate.commands` set in the surface's project folder or root | the same (the layers merge as for `parallel`) |
| A worktree's own `chantier.yaml` changes a name's command | ignored: the main repository's layers are read |
| `lease hold`, no `--minutes` | live 45 minutes |
| `lease hold --minutes 90` / `--minutes 91` / `-- cmd` | live 90 minutes / refused / refused |
| `lease stack hold`, then the hold lapses | "not confirmed"; the stack driver's next command with the same `--lease` accepted, logged `lease-late` |

## Evidence

- Tests (`TESTS/`, in-process, parametrized, within `AGENTS.md`'s time budget):
  - the config key: `commands` accepted; a bad name, an empty command and an unknown key under
    `long_gate` each give a problem with its line;
  - `gate` refuses, before any log or event, a free command, an unknown name and a project with no
    entry (the last one's text holds the three lines); with an entry, the event carries the name
    and the command;
  - `lease hold`: default 45, `--minutes 90` accepted, 0, 91 and a `--` command refused; a renewal
    after a hold does not shorten its expiry; no `.lease-hold.*` file is written;
  - one test reads the repository's root `chantier.yaml` as it ships, at the head under test, and
    checks `long_gate.commands.scenario` is `just scenario`; another reads `AGENTS.md` as it ships
    and checks it names `chantier gate <cr> scenario`; another reads `evals/kit/sandbox/` and
    `evals/kit/fixture/` as they ship and checks each `chantier.yaml`'s `tests` command is the
    command of its `AGENTS.md` long gate line.
- Scenario (`scenario/run_scenario.py`): its workspace's `chantier.yaml` gets the names its gates
  use (the `GATE` constant, and the slow and queue gates of the long gate sections, each a name);
  every `chantier("gate", cr, <command>)` becomes the name; one new check: a free command is
  refused, exit 2, nothing logged. Section 3a (`lease_cases`, "3a. Leases: a stale one, and a CI
  watch under `lease hold`") becomes "a stale one, and a wait under `lease hold`": with the
  shortened TTL (3 s) and `CHANTIER_LEASE_TEST_MINUTE` set to a few seconds, `lease CR-102 hold
  --lease <n> --minutes 1` keeps the lease live past the TTL with no process running; after the
  hold lapses, `lease CR-102` says not confirmed; a `--` command is refused. One assertion for the
  stack (Q6): after a `lease stack hold --minutes 1` lapses, a command with the same `--lease` on
  `stack` is accepted (`lease-late` in the log). 3a runs before any `take stack`; this check goes
  right after the scenario's first `take stack` printed `lease: stack <n>`, under 3a's name.
- Eval kit: `just eval-dry-run` passes with the gate called by name and the sandbox's
  `chantier.yaml` in its workspace.
- Gates owed (`AGENTS.md`): `just check`, `just eval-dry-run` (the CLI's `src/` and the eval kit
  change), the pipeline's `just scenario (ubuntu-latest)` job at the PR's head, and, on top of the
  stack, the local `chantier gate <cr> scenario`. No `hooks/` or `types/` change.

## Open questions for the Chief of Staff

1. **Where the "Before you update" line lives until the release.** The release notes are written
   by the next Release driver from what shipped; `REF/release-template.md` has no section for an
   upgrade step.
   - A (recommended, built): the PR's body carries the **Before you update** paragraph, and the
     Release driver carries it into the notes as it does any notable change; the template is
     unchanged.
   - B: this CR also adds a "Before you update" section to `REF/release-template.md`, filled from
     PRs that carry one.
