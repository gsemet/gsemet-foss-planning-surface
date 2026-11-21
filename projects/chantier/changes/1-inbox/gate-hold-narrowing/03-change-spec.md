# gate runs only named commands; lease hold runs nothing

Step 2 of the permissions-bypass split (perm-bypass-Q17). Today `chantier gate <cr> "<command>"`
runs any text through a shell (`commands/gate.py`, `_spawn`) and
`chantier lease <unit> hold -- <command>` runs any program (`commands/leases.py`, `_hold`).
Both are chantier commands, so chantier's allow rules let them through with no prompt: an agent
with Bash can run anything through them. This CR closes those two doors.

It depends on CR-432 (permissions-bypass, step 1: real paths in P10's chantier rules) and joins
batch-30 after it: the Driver works on CR-432's merged head. Places are named by their text and
their function, never by a line number (CR-432 and the commits since this was written move the
lines); section 6 names where this CR meets CR-432 and the other CRs of batch-30.

Spec v3: v2 with the spec critic's eight findings applied (gate-hold-Q7 and Q8 included).

## Goal

In the user's terms: `gate` runs only the long gate the project wrote down in its code
repository's `chantier.yaml`, asked for by its name; `lease hold` runs nothing, it only keeps a
lease alive for a while. A project with no gate written there is offered the entry once, written
on the user's yes.

Known limit (gate-hold-Q2's restatement): `just scenario` runs the worktree's justfile, which a
Coder edits. This guards against the read-only roles (Inspector, Verifier...) running anything
through chantier, not against a Coder.

## Decisions carried from the grill

- perm-bypass-Q1 (held by gate-hold-Q2): `gate` runs only a command named in `chantier.yaml`,
  called by its name (`gate CR-430 scenario`); a free command is refused.
- perm-bypass-Q9 (held): at its first turn, the Chief of Staff that sees a declared long gate with
  no command configured offers the `long_gate.commands` entry, written on the user's yes, in the
  code repository's root `chantier.yaml` (Q8); the no-setup bullet of `AGENTS.md` says a runnable
  long gate needs it.
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
- gate-hold-Q7 (a Fable advisor's answer): before this CR merges, its own gates use the old free
  form, `gate <cr> "just scenario"` (the CLI runs live from the main checkout, still the old one);
  after the merge, the refusal's `named: scenario` is enough for a running Driver, and the Chief
  of Staff tells the live Drivers of batch-30 once. No ordering of the batch for it. Evidence,
  "Gates owed".
- gate-hold-Q8 (a Fable advisor's answer): only the code repository's root `chantier.yaml` may
  name a gate's command. `long_gate.commands` in a planning surface's `chantier.yaml` (its root or
  the project's folder) is ignored for running, and `playbook` and `validate` say so;
  `long_gate.parallel` keeps merging across all layers. The planning surface is written by agents,
  by the board's `config.put` and by anyone who can push it, and the writer fetches it with no
  prompt; the code repository's file is under PR review.

## What changes

Paths: `CLI/` is `skills/chantier/scripts/cli/src/chantier/`, `REF/` is
`skills/chantier/references/`, `TESTS/` is `skills/chantier/scripts/cli/tests/`. Exit codes are
`core/errors.py`'s: `EXIT_USAGE` is 1, `EXIT_PRECONDITION` is 2.

### 1. The `long_gate.commands` key (`CLI/playbook/config.py`, `CLI/playbook/layers.py`, `CLI/playbook/lines.py`, `CLI/commands/validate.py`)

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
- Where the commands are read (Q8): only from the layer `_places` (layers.py) labels
  `"repository"`: the code repository's root, `Repo.root`, the main checkout even when `gate` runs
  in a worktree, so a worktree's own `chantier.yaml` does not change which command a name runs.
  In an external planning surface, the `"surface"` and `"surface project"` layers'
  `long_gate.commands` is ignored for running; their `long_gate.parallel` still merges as today.
- `load_long_gate` (layers.py) also returns the names and their commands from that one layer
  (none when absent), and the paths of the surface layers that hold an ignored
  `long_gate.commands`. The shipped defaults (`config/chantier.defaults.yml`) hold no command.
- `$CHANTIER playbook` prints one line for it, beside its `ci:` line (lines.py): `long gate:
  <name> (<command>)[, ...] (chantier.yaml: long_gate.commands)`, or `long gate: none named in
  chantier.yaml (long_gate.commands)`; and, for each surface layer holding one, `long gate:
  long_gate.commands in <path> ignored: only the code repository's root chantier.yaml names a
  long gate's command`. The Chief of Staff reads the first for Q9 (section 5).
- `$CHANTIER validate` (it reads no `chantier.yaml` today): one finding of severity `gap` (exit
  0, as gaps are) for each planning surface `chantier.yaml` (root or project folder) that holds
  `long_gate.commands`, with the same "ignored: only the code repository's root chantier.yaml
  names a long gate's command" text.
- The board's Configuration page and `config.put` edit only the two limits and the roles: a save
  keeps `long_gate.commands` as it is in the file it writes, and never adds one.

### 2. `gate` runs names (`CLI/commands/gate.py`, `CLI/declare/gate.py`, `CLI/commands/facts.py`)

- New form: `gate <cr> <name> [<name>...]`. Each name is looked up in `long_gate.commands`; the
  gate runs their commands in the order given, as today (stop at the first failure, the queue, the
  slots, `--stop`, `--first`, the dirty-tree refusal, the moved-head rule: all unchanged).
- Refused before anything runs or is logged:
  - a word that is not a configured name (a free command such as `"just scenario"` included),
    exit 1 (`EXIT_USAGE`):
    `gate <cr>: "<word>" is not a long gate named in chantier.yaml (long_gate.commands); named: <names>`;
  - no `long_gate.commands` in the code repository's root `chantier.yaml`, exit 2
    (`EXIT_PRECONDITION`; Q5: the refusal names the lines to add):
    `gate <cr>: chantier.yaml names no long gate; add to the code repository's root chantier.yaml:`
    followed by the three lines `long_gate:` / `  commands:` / `    <name>: <the long gate's command>`,
    then `(the Chief of Staff offers it to the user)`. When a surface layer holds an ignored
    `long_gate.commands`, the refusal adds the `playbook` line that says so.
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
  45 when absent; outside that range, refused (exit 1, `EXIT_USAGE`). Anything after `--` is
  refused (exit 1): `lease hold runs no command: start your wait yourself, then run lease <unit>
  hold --lease <n>`.
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
- The hold leftovers, each found by its text:
  - `core/files.py`, `IGNORED`: the `".lease-hold.*.run"` pattern **stays**, so a record left by
    an older version is never published;
  - `core/leases.py`: the `drop` parameter of `check_free` and `liveness` (and of `hold_records`,
    which goes) is removed with its docstring sentences ("unless `drop` is False", "`drop` False:
    read-only, no dead hold record is removed");
  - `commands/take_checks.py`: the call `check_free(..., drop=not read_only)` loses `drop`; its
    docstring's "`read_only`: no dead lease-hold record is removed." goes (the `read_only`
    parameter keeps whatever else it still means; if nothing, it goes too, with its callers'
    argument in `access`);
  - `board/fingerprint.py`: `HOLDS = ".lease-hold.*.run"` and its comment go (section 6, CR-429).
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
  "the running `lease hold`s of this lease"; `clients/tui/model.py`, `lease_left`, drops the
  `held` branch and its docstring's "else `held` when a `lease hold` runs". `docs/server-api.md`
  (`project.state`) drops `holds` from the lease object: a change of the published API, named in
  the PR's body.

### 4. chantier's own repository

- New root `chantier.yaml` (Q14): `long_gate:` / `commands:` / `scenario: just scenario`.
- `AGENTS.md`:
  - the Windows coverage sentence: "passes `just scenario` locally (`chantier gate`)" becomes
    "passes the long gate `scenario` locally (`chantier gate <cr> scenario`)" (Q15); the pipeline
    job's name `just scenario (ubuntu-latest)` stays, it is the CI job's name;
  - the no-setup bullet: a runnable long gate needs its `long_gate.commands` entry in the code
    repository's root `chantier.yaml` (Q9, Q8); "(with the `.lease-hold.*.run` records of `lease
    hold`, never published)" goes from what chantier writes;
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
  command per argument"): the named form.
- `REF/concepts.md`:
  - the long gate sentences of the `$CHANTIER` entry (they start "The long gate is `gate <cr>"
    and say "one command per argument"): the named form, and the commands live in the code
    repository's root `chantier.yaml`, `long_gate.commands`;
  - the **Lease:** entry: "renewed by the commands that carry `--lease <n>`, by `lease <unit>
    renew` and by a `lease <unit> hold` child that runs" becomes "renewed by the commands that
    carry `--lease <n>` and by `lease <unit> renew`; `lease <unit> hold` sets its expiry ahead (45
    minutes, 90 at most)"; "a long gate of the CR runs or waits, or a hold runs" becomes "or a long
    gate of the CR runs or waits" (the expiry a hold set counts as within its time).
- `REF/chief-of-staff.md`:
  - the first-turn paragraph ("A project with no long gate written down is a question for the
    user ..."): a long gate declared in the project's rules while `$CHANTIER playbook` prints
    `long gate: none named in chantier.yaml` is a question to the user, with the exact lines
    proposed (a name and the rules' command), written on the user's yes in the code repository's
    root `chantier.yaml` (Q9, Q8; Q5: this is also how a project that updated the plugin
    mid-batch gets the entry). A `playbook` line saying a surface's `long_gate.commands` is
    ignored is told to the user with the same offer. "When the user says 'our long gate is
    `<command>`', propose the exact `AGENTS.md` lines" becomes: the `AGENTS.md` line naming the
    gate by its name and the `chantier.yaml` entry holding the command; "propose the
    `long_gate:` / `parallel: <n>` lines of `chantier.yaml`" applies when `chantier.yaml` has no
    `long_gate.parallel` (a file holding only `long_gate.commands` still gets the question).
  - the `chantier.yaml` example shows `commands:` under `long_gate:`, with a note that only the
    code repository's root file names commands.
- `REF/init.md`, the long gate item (the one that ends "Not asked when `chantier.yaml` already has
  `long_gate`"): the `long_gate.commands` entry is proposed too, on the same yes, for the code
  repository's root `chantier.yaml`; the test becomes "Not asked when `chantier.yaml` already has
  `long_gate.parallel`" (a `long_gate:` holding only `commands` still gets the parallel
  question); "one command per item" stays for `AGENTS.md`.
- `REF/hosts/claude-code.md`: the sentence CR-432 adds to the "Risk accepted" of the chantier
  rows of "Allow rules" (its text: "`gate` and `lease hold` still run the command they are given,
  until `gate-hold-narrowing`") becomes "`gate` runs only the long gates the code repository's
  `chantier.yaml` names, and `lease hold` runs nothing".
- `docs/gates.md`: the long gate is declared in two places: `AGENTS.md` names it, the code
  repository's root `chantier.yaml`, `long_gate.commands`, holds its command (a planning
  surface's is ignored); the example shows both; the sentence "the Driver passes each as its own
  argument to `chantier gate`" speaks of names.
- `docs/planning-folder.md`: "and the `.lease-hold.*.run` records of a running `lease hold`"
  goes.
- `scenario/README.md`: section 3a's "the lease stays live, held by 1 background task" becomes
  "the lease stays live through the hold's minutes, with no process running"; its gate texts give
  names.
- The release notes (Q5): the PR's body carries a paragraph headed **Before you update**: add the
  `long_gate.commands` entry to the code repository's root `chantier.yaml` before updating the
  plugin (the three lines, an example), since from this version `gate` refuses a free command and
  every gate of a running batch is refused until the entry is there. The Release driver of the
  next release carries it into its notes, where the release-template's sections allow (open
  question 1).

Both hosts' agent files are untouched (their bodies stay identical).

### 6. Where this meets the other CRs of batch-30

Read on CR-432's merged head, by text:

- CR-432 (permissions-bypass):
  - `REF/hosts/claude-code.md`: the one sentence CR-432 writes into the chantier rows' "Risk
    accepted" (section 5 rewrites it). When the merged text differs from the one quoted in
    section 5, the Driver rewrites the sentence that names `gate-hold-narrowing`, whatever its
    words.
  - `REF/chief-of-staff.md`: CR-432 edits "The allow rules (P10, Claude Code)" (the **Broad
    rules** and **Stale rules** bullets); this CR edits the first-turn long gate paragraph just
    above it and the `chantier.yaml` example below it. Neighbouring text, no shared sentence.
  - `REF/concepts.md`: CR-432 adds a sentence to the `$CHANTIER` entry; this CR edits the long
    gate sentences of the same entry and the **Lease:** entry. Same entry, different sentences:
    the Driver keeps CR-432's sentence as merged.
  - `scenario/run_scenario.py`: CR-432 changes the P10 section (the settings it writes, a broad
    rules check); this CR changes the workspace's `chantier.yaml`, the gate calls and section 3a.
    No shared function.
  - `TESTS/test_cli_runs.py`: CR-432 adds P10 cases; this CR's changes sit in the same file. No
    shared test.
  - `CLI/commands/permissions.py`, `CLI/commands/preflight.py`, `CLI/plugin_files.py`, the four
    SKILL.md files: CR-432's only; this CR changes what the rules let run, not the rules.
  - `AGENTS.md`: CR-432 leaves it unchanged; this CR edits it (section 4).
- CR-429 (`4-batch/2-actives/429-board-fingerprint-cache`): its watch covers the paths
  `board/fingerprint.py` covers (`SINGLE`, `HOLDS`, `DEEP`, `SHALLOW`), and this CR removes
  `HOLDS`. Whichever merges second rebases on the other: if CR-429 is in first, this CR also
  drops the `.lease-hold` pattern wherever CR-429 carries it (its watch's path filter, its
  tests), keeping `core/files.py`'s `IGNORED` entry; if this CR is in first, CR-429's Driver finds
  `HOLDS` gone and drops it from its watch. The Chief of Staff tells CR-429's Driver at this CR's
  merge.
- CR-436 (`4-batch/1-pending/436-sync-blocked-by-others`): it changes only the `cli_command`
  callers in `commands/driver.py`, `commands/facts.py` and `commands/orders.py`; this CR edits
  other lines of those files (the stack driver's and the QA order's `lease:` lines,
  `_gate_lines`). Same files, no shared line.

### 7. The eval kit (Q4)

- `evals/kit/sandbox/chantier.yaml` (new): `long_gate:` / `commands:` / `tests: uv run --locked
  pytest -q`, the command of the sandbox's `AGENTS.md` long gate line, word for word. A new file
  under `evals/kit/sandbox/` changes the sandbox's deterministic base (`evals/README.md`, "To
  change the project"): the Driver runs `sandbox.py build --record` and commits the new
  `evals/kit/sandbox.json` in the same PR, or `just check` is red.
- `evals/kit/fixture/chantier.yaml` (new): `long_gate:` / `commands:` / `tests: uv run pytest
  -q`, the command of the fixture's `AGENTS.md` long gate line.
- Both `AGENTS.md` files stay as they are (the judge and the sandbox CRs quote their command); the
  Driver reads the name from the facts and `playbook`.
- `evals/kit/dry_run.py`: `GATE` becomes the name `tests` (its comment says so); the PR body's
  test plan text keeps the command; the workspace it builds carries the sandbox's
  `chantier.yaml` (when the build copies tracked files, nothing more to do; else it writes it).
- After the merge, the maintainer's own published sandbox still sits at the old base: the PR's
  body says to run `sandbox.py reset --yes` once the PR is merged (`evals/README.md`: "Once that
  PR is reviewed, run `reset --yes`").

## Out of scope

- The allow rules themselves and P10 (CR-432). The push rules (dropped, perm-bypass-Q17).
- A gate keeping the stack lease live (Q6): `gate_keeping` stays as it is; the stack driver holds
  its lease itself.
- A transition period for the free command (Q5).
- A gate's command named in a planning surface's `chantier.yaml` (Q8: ignored; widening it is the
  user's to decide).
- The fast gate, run by agents directly, never through `gate`.
- A Coder editing the justfile or the scripts a named command runs (the known limit).
- `handback --no-gate`, exemptions and a pipeline job named as the long gate: unchanged.
- The Q9 offer in an eval (Q4: the evals ship the entry).

## Default and configured matrix

| Cell | Expected |
| --- | --- |
| Shipped defaults only (no `long_gate.commands`) | `gate <cr> <anything>` refused, exit 2, the text giving the three lines to add; nothing logged; `playbook` prints `long gate: none named` |
| `long_gate.commands.scenario` set in the code repository's root, `gate <cr> scenario` | runs the command, as today's gate |
| Same, `gate <cr> "just scenario"` (a free command) or an unknown name | refused, exit 1, listing `scenario`; nothing logged |
| Two names, `gate <cr> a b` | runs a then b; stops at a's failure |
| `long_gate.commands` set only in the surface's project folder or root | ignored, said by `playbook` (its "ignored" line) and `validate` (a gap); `gate` refused, exit 2, as with none |
| `long_gate.parallel` set in the surface's project folder or root | merged as today |
| A worktree's own `chantier.yaml` changes a name's command | ignored: the main checkout's root file is read |
| `lease hold`, no `--minutes` | live 45 minutes |
| `lease hold --minutes 90` / `--minutes 0` or `91` / `-- cmd` | live 90 minutes / refused, exit 1 / refused, exit 1 |
| `lease stack hold`, then the hold lapses | "not confirmed"; the stack driver's next command with the same `--lease` accepted, logged `lease-late` |

## Evidence

- Tests (`TESTS/`, in-process, parametrized, within `AGENTS.md`'s time budget):
  - the config key: `commands` accepted; a bad name, an empty command and an unknown key under
    `long_gate` each give a problem with its line;
  - `gate` refuses, before any log or event, a free command and an unknown name (exit 1) and a
    project with no entry (exit 2, its text holds the three lines); with an entry, the event
    carries the name and the command;
  - the ignored layer (Q8), one test: in an external planning surface, `long_gate.commands` in
    the surface's project folder only: `gate` is refused exit 2, `playbook` prints the "ignored"
    line, `validate` gives one gap; the same layer's `long_gate.parallel` still applies;
  - `lease hold`: default 45, `--minutes 90` accepted, 0, 91 and a `--` command refused (exit 1);
    a renewal after a hold does not shorten its expiry; no `.lease-hold.*` file is written;
  - the tests that build hold records (`test_access.py`, the `.lease-hold.CR-101.1.run` case;
    `test_leases.py`, the cases that write a dead `.lease-hold.<unit>.1.run` and the one that
    asserts none is left; `test_live_model.py`, the `holds` facts and the `held` case) are
    removed or rewritten for a hold that sets the expiry;
  - the tests that call `gate` with a free command (`test_carry_ship.py`, its `GATE =
    "python -c pass"`; `test_cli_runs.py`, `chantier("gate", "CR-101", "true")`, which asserts
    `EXIT_PRECONDITION` for a CR not taken) write a `chantier.yaml` naming that command in their
    prepared repository's root and call `gate` with its name, keeping what they assert;
  - one test reads the repository's root `chantier.yaml` as it ships, at the head under test, and
    checks `long_gate.commands.scenario` is `just scenario`; another reads `AGENTS.md` as it ships
    and checks it names `chantier gate <cr> scenario`; another reads `evals/kit/sandbox/` and
    `evals/kit/fixture/` as they ship and checks each `chantier.yaml`'s `tests` command is the
    command of its `AGENTS.md` long gate line.
- Scenario (`scenario/run_scenario.py`): its workspace's root `chantier.yaml` (`w.work /
  "chantier.yaml"`, the code repository's) gets the names its gates use (the `GATE` constant, and
  the slow and queue gates of the long gate sections, each a name); the sections that rewrite that
  file (the board host checks, section 11) keep the `long_gate.commands` entry in what they write
  or restore it after; every `chantier("gate", cr, <command>)` becomes the name; one new check: a
  free command is refused, exit 1, nothing logged. Section 3a (`lease_cases`, "3a. Leases: a stale
  one, and a CI watch under `lease hold`") becomes "a stale one, and a wait under `lease hold`":
  with the shortened TTL (3 s) and `CHANTIER_LEASE_TEST_MINUTE` set to a few seconds, `lease
  CR-102 hold --lease <n> --minutes 1` keeps the lease live past the TTL with no process running
  (the wait for a `.lease-hold.CR-102.*.run` file goes); after the hold lapses, `lease CR-102` says
  not confirmed; a `--` command is refused, exit 1. One assertion for the stack (Q6): after a
  `lease stack hold --minutes 1` lapses, a command with the same `--lease` on `stack` is accepted
  (`lease-late` in the log). 3a runs before any `take stack`; this check goes right after the
  scenario's first `take stack` printed `lease: stack <n>`, under 3a's name.
- Eval kit: `just eval-dry-run` passes with the gate called by name and the sandbox's
  `chantier.yaml` in its workspace; `just check` passes with the re-recorded `sandbox.json`.
- Gates owed (`AGENTS.md`): `just check`, `just eval-dry-run` (the CLI's `src/` and the eval kit
  change), the pipeline's `just scenario (ubuntu-latest)` job at the PR's head, and, on top of the
  stack, the local long gate. Q7: until this CR merges, the CLI that runs is the main checkout's
  old one, so this CR's own local gate is `gate <cr> "just scenario"` (the free form), and so are
  the other batch-30 Drivers'; after it merges, a Driver whose free command is refused types the
  `scenario` the refusal names, and the Chief of Staff tells the live Drivers once. No `hooks/` or
  `types/` change.
- The PR's body: the **Before you update** paragraph (section 5), the published API change
  (`holds` gone from `project.state`'s lease object), the re-recorded `evals/kit/sandbox.json`
  and the maintainer's `sandbox.py reset --yes` after merge (section 7).

## Open questions for the Chief of Staff

1. **Where the "Before you update" line lives until the release.** The release notes are written
   by the next Release driver from what shipped; `REF/release-template.md` has no section for an
   upgrade step.
   - A (recommended, built): the PR's body carries the **Before you update** paragraph, and the
     Release driver carries it into the notes as it does any notable change; the template is
     unchanged.
   - B: this CR also adds a "Before you update" section to `REF/release-template.md`, filled from
     PRs that carry one.
