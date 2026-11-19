# Change spec: spec-writers and slots set from the board's configuration

Source: the user, verbally, 2026-11-18 (no issue). Short name: `config-spec-writers-slots`.
Checked against `main` at `3a9afc2c`.

## Goal

The user sets two numbers in the project's configuration and changes them from the web board's
Configuration page:

- how many CRs are specified at once on the project (the spec-writers running; default 4);
- how many slots a new batch gets (default 4, the value `open` uses today).

When the user saves a change to either number on the board, the Chief of Staff learns about it at
once, through the forge journal the watcher already reads, and acts on it without asking (the
save is the user's word):

- slots changed while a batch runs or is paused: it gives `order slots --note <n>`;
- specifying limit raised: it starts the waiting spec-writers up to the new limit;
- specifying limit lowered: it lets the running ones end and starts no new one until the count is
  under the limit.

## Decisions carried (02-answers.md)

1. Two keys in the configuration, in `config/chantier.defaults.yml`, overridable by the
   surface's, the surface project's and the repository's `chantier.yaml` like every key. Names
   (spec-critic's findings, role-free name, B): `specifying.parallel` ("CRs being specified at
   once", default 4) and `batch.slots` (default 4). The CLI names no role for them; the cards say
   the spec-writer reads `specifying.parallel`. AGENTS.md needs no new exception for a role name.
2. The limit counts spec-writers only; a spec-critic does not count. The Chief of Staff and a
   Griller share one limit on one project. What counts (spec-critic's findings, A): the
   `work/specifying` markers of the project's planning folder. The cards remove a CR's marker at
   its spec-writer's hand-back, before any critic starts. Before starting a spec-writer, the
   session reads the count and starts none at the limit; the next one waits for a hand-back.
3. `batch.slots` is `open`'s default when `--slots` is not given; `--slots` still wins. A running
   batch keeps its recorded slots until an `order slots --note <n>`.
4. The board's Configuration page edits both keys, checked like its other keys: whole numbers,
   slots 0 or more, specifying 1 or more.
5. When the board saves a change to either key, it appends one `config` line to the project's
   `forge-journal.jsonl` (key, old value, new value). `config` is a waking kind: a running watcher
   reads it as it reads a merge, then ends, which wakes the Chief of Staff.
6. `status` (spec-critic's findings, replaces the earlier Q1): it prints a `config` line for
   `batch.slots` only, until an `order slots --note <n>` is recorded after it. It prints none for
   the specifying limit (no file records the waiting spec-writers): the watcher's end line and
   `playbook`'s `limits:` line say that change.
7. What the Chief of Staff does on the event, alone (spec-critic's findings, A: a board save of
   these two keys is the user's word for them; the card names it as the one exception to
   events-Q5, "merges only"; any other configuration change gets one line to the user and no
   action):
   - slots changed and a batch runs or is paused (Q3, A): it gives `order slots --note <n>`
     (recorded and relayed to the Foreman like every order) and tells the user in one line;
   - specifying raised: it starts the next waiting spec-writers up to the new limit;
   - specifying lowered: it stops none and starts none until the count is under the limit.
8. The board never edits a batch and never messages an agent. The change to a running batch is
   always the Chief of Staff's order. AGENTS.md names the new journal line among the board's
   writes.
9. When no watcher runs, the slots event waits for the next `status`; the specifying event is
   read from `playbook`'s `limits:` line before the next start.
10. A configured `batch.slots: 0` makes `open` with no `--slots` refuse (exit 2), naming the file
    and the key (Q2, A).
11. The wake on a configuration change is unproved (spec-critic's findings, A): the PR's Known
    gaps names it; the host rows' trial adds a board save with an idle session; `status` stays the
    fallback for the slots.
12. Kept whole (spec-critic's findings, B): both keys in this one CR, as the user asked.
13. Factory batch (spec-critic's findings, A): the cards open it with `--mode stack` and no
    `--slots` unless the user names a number, so it takes `batch.slots`.

## What changes

Paths below are relative to `skills/chantier/scripts/cli/src/chantier/` unless they start at the
repository root.

### Shipped defaults: `config/chantier.defaults.yml`

Two new top-level keys, each with a one-line comment, role-free:

```yaml
specifying:
  parallel: 4   # the most CRs being specified at once on the project
batch:
  slots: 4      # the slots `open` gives a batch when no --slots is given
```

### Configuration checks: `playbook/config.py`

- `specifying` and `batch` join the known top-level keys.
- The unknown-key message adds them to its list: "hosts", "prices", "board", "ci", "long_gate",
  "specifying", "batch".
- Each key is checked the same way `long_gate` is:
  - `specifying: "parallel" is a whole number, 1 or more, found "<v>"`;
  - `batch: "slots" is a whole number, 0 or more, found "<v>"`.
  - An unknown sub-key under either key is refused the same way `long_gate` refuses one.
- A bad value in any layer is a configuration problem. As with any key, `open` and `playbook`
  report it with the file's path.

### Reading the limits: `playbook/layers.py`, `plugin_files.py`

- A new reader resolves each value with the layer it came from. It searches the user layers,
  strongest first (repository, surface project, surface), then the shipped defaults, the way
  `playbook/timing.py` resolves timing.
- `plugin_files.read_limits(repo)` sits next to `read_timing` and takes the shipped values only
  from the plugin's `config/chantier.defaults.yml` (`plugin_root()`), as `read_timing` does. The
  CLI holds no value of its own for either key (no fallback).
- A shipped defaults file without one of the two keys is a defaults-file problem: it is reported
  as the other problems of `layers.read_defaults` are, and `open` and `playbook` stop on it as
  they stop on any configuration problem. A check on the shipped file guards it (Evidence).
- With no plugin root (`plugin_root()` is `None`, a skill installed on its own), as `read_timing`
  does, the reader resolves from the user layers alone, and a key no user layer sets has no value:
  - `open` with no `--slots` and no `batch.slots` in any user layer refuses (exit 2):
    `open: no batch.slots: no plugin defaults file and no chantier.yaml sets it; give --slots <n>`;
  - `playbook`'s `limits:` line prints `specifying parallel: not set` (and `batch slots: not set`)
    for a key with no value. See open question Q1.

### `chantier open` (`declare/opening.py`, `commands/opening.py`, `commands/opening_record.py`)

- `--slots` no longer has a default of 4. When it is not given, `open` uses `batch.slots` from
  the configuration.
- When the slots came from a user layer, the first line of the output names that layer, using the
  same bracket labels the playbook uses (`[surface project]`, `[repository]`, `[surface]`):
  `opened <batch> on <host>: <n> CRs, <slots> slots [surface project], <mode>, steering ...`.
  A shipped default or a given `--slots` gets no label, so the output is the same as today.
- A configured `batch.slots: 0` with no `--slots` (Q2, A): `open` refuses with exit 2 (usage).
  The text follows CR-374's form (what is refused, why, what to do now):
  `open: batch.slots is 0 in <file>: a new batch needs 1 slot or more to start a Driver; give --slots <n>, or set batch.slots on the board's Configuration page`.
  An explicit `--slots 0` is refused as it is today ("slots and budget must be positive").
- `order slots --note <n>` (`commands/orders_apply.py`, `_slots`) does not change. It still
  accepts 0 or more, and 0 holds a running batch.

### `chantier playbook` (`playbook/lines.py`, `commands/` caller)

A new `limits:` line comes after the `timing:` lines. It follows the playbook's label rule: no
label for a shipped default, `[<layer>]` otherwise. It is role-free: it counts markers.

```
limits: specifying 4, markers 2 (cr-a, cr-b); batch slots 6 [surface project]
```

- "markers" counts the `work/specifying` files in `1-inbox/`, `2-backlog/P1`..`P4` and
  `3-ready/` of the project's planning folder.
- It lists the CR slugs, in folder order, so a stale marker shows (the user or the Chief of Staff
  removes it).
- The line ends with `at the limit` when markers >= the limit.

The cards read this line before each spec-writer start (see Cards). The CLI does not refuse a
spec-writer start: the limit is the session's to keep.

### The board's Configuration page

Read `board/web/DESIGN.md` first and keep it true. Add a short "Configuration page" note there
on the new tab, if the file names the page's tabs.

- `playbook/edit.py`:
  - `config_view` returns a new `limits` block. For each key it gives:
    - the effective value;
    - the layer that set it;
    - the value of each layer;
    - whether the repository's `chantier.yaml` overrides the surface project's file, since the
      board writes only the latter.
  - `edit_surface_file` accepts a second change shape, `{"key": "specifying.parallel" |
    "batch.slots", "value": <int> | null}`. `null` removes the key from the surface project's
    file, so the weaker layers take over again.
  - Each change keeps the same lock, SHA conflict check (`409 stale`), dry run and whole-file
    validation as the role edits.
  - A value outside the checks is refused with the check's own text from `config.py`.
- `playbook/edit_text.py`: the ruamel edit that keeps comments now also sets and removes a
  top-level `<key>.<sub>` path, not only `hosts.<host>.roles.<role>.<key>`.
- `board/config_api.py`, on a real (non-dry-run) PUT:
  - it appends one `config` journal line (below) per limit key whose effective value changed,
    in the order of the changes; a PUT with several changes writes one line for each such key,
    and none for role changes (a role edit keeps today's behaviour: no `forge-journal.jsonl`
    line);
  - the board journal's `config` line stays as it is today;
  - the response lines are role-free and say what happens next, in place of the bare
    `applies at the next batch` for these keys:
    - `batch.slots`, with a batch running or paused:
      `slots 4 -> 6: batch-29 keeps 4 until an order slots`;
    - `batch.slots`, with no batch running or paused: `slots 4 -> 6: from the next open`;
    - `specifying.parallel`: `specifying 4 -> 2: from the next start`;
    - role edits keep `applies at the next batch`.
- The board writes no journal line for a dry run, for a save that leaves the effective value
  unchanged, or for a key other than these two.
- `board/web/js/views/config.js`, `config-timing.js`:
  - a third tab, "Limits", next to Models and Timing, with its own hash address;
  - two number inputs (min 0 for slots, min 1 for specifying), labelled in the user's words
    ("CRs specified at once", "slots of a new batch") through `t()`;
  - each input shows the effective value and its layer;
  - each has a "use the inherited value" control that sends `null`;
  - the same judge (dry run), save, stale and read-only banner as the Models tab;
  - when the repository's `chantier.yaml` overrides the key, the tab says so beside the input
    (`config.limits.overridden`): a save to the surface file changes nothing until that line is
    removed.
- `board/web/js/api/config.js`: `changeConfig` sends the new shape unchanged; no new endpoint.
- i18n: new `config.limits.*` keys in every language file (en, fr), words only through `t()`.

The board still writes only the surface project's `chantier.yaml`. A project with no planning
surface sees the tab read-only, like the Models tab today.

### The forge journal: `hub/journal.py`

- A new kind, `config`, written by the board (`by: "board"`), and a waking kind (a new line of it
  ends the watcher as a merge does):

  ```json
  {"seq": 12, "t": "...", "by": "board", "kind": "config", "key": "batch.slots", "old": 4, "new": 6, "batch": "batch-29"}
  ```

  - `key` is a dotted path into the configuration. This CR writes it for `batch.slots` and
    `specifying.parallel` only; the shape holds a role edit later as
    `hosts.<host>.roles.<role>.<key>` (session-events-board-griller extends it to every key, one
    kind of line for a configuration change).
  - `old` and `new` are the effective values before and after the save, all layers included;
  - `batch` is the batch running or paused at the save, or `null` when there is none.
- Dedup: a `config` line has its own key (`kind`, `key`, `old`, `new`, `t`). Two saves with the
  same values make two lines. The merge key does not swallow a config line.
- `event_text` gets a `config` branch, role-free:
  - `config changed on the board: batch.slots 4 -> 6; batch-29 keeps 4 until an order slots`
  - `config changed on the board: batch.slots 4 -> 6; from the next open (no batch)`
  - `config changed on the board: specifying.parallel 4 -> 6`
  - `config changed on the board: specifying.parallel 4 -> 2`
- `lines(...)`, used by `status`, prints the newest `batch.slots` line while it is not acted on:
  - the line's batch is the current batch (running or paused), and no order of kind `slots` is in
    that batch's record (`orders`, written by `commands/orders.py`) with a time after the line's
    `t`;
  - a newer `batch.slots` line replaces an older one; a line for a closed batch, or with
    `batch: null`, is not printed.
  - It prints no `specifying.parallel` line, and no line for any other key.
- The module's docstring names the board's new line.

### The watcher: `hub/watch.py`

- `Watch.poll` already reads every line with `seq` above its cursor, whatever its kind. A `config`
  line counts as a new event like a merge: the watcher ends 20 s after the last one and prints
  `event_text` for it.
- The watcher's other end lines (`no-batch`, and the end line CR-375 brings) stay as they are.
- The forge hub does not change: the board writes the line, and the hub never reads or writes
  `config` lines.
- That this end wakes an idle Claude Code session on a board save is unproved (decision 11): see
  Known gaps.

### `chantier status` (`commands/batch_status.py`)

- `_seen_lines` prints the `batch.slots` `config` line from `journal.lines`, after the merges.
- With no batch running or paused, `status` refuses as it does today, and nothing is lost:
  - `open` reads `batch.slots`;
  - each spec-writer start reads the `limits:` line.

### Cards (`skills/chantier/references/`)

- `chief-of-staff.md`:
  - Entry points: a row for `config changed on the board` (from the watcher's end or `status`).
    It says:
    - this is the one named exception to what you do alone when woken (merges only,
      events-Q5): a board save of `batch.slots` or `specifying.parallel` is the user's word for
      it; act without asking. Any other configuration line: one line to the user, no action;
    - for `batch.slots` with a running or paused batch: `order slots --note <n>`, then one line
      to the user;
    - for `specifying.parallel`: start the waiting spec-writers up to the limit, or let the
      running ones end.
  - The spec-writer paragraph (the `work/specifying` guard, ~line 305):
    - the spec-writer reads `specifying.parallel`: read `playbook`'s `limits:` line before each
      spec-writer start; start none at the limit; keep the waiting CRs in order and start the next
      on a hand-back;
    - remove the CR's `work/specifying` at its spec-writer's hand-back, before any critic starts
      (this replaces "Remove `work/specifying` when the (last) one ends");
    - a spec-critic is not counted and writes no marker.
  - "The spec critic", step 2 (~lines 443-447): `work/specifying` no longer stays through the
    critic. A spec-writer's next run writes the marker again (and counts against the limit);
    while the critic runs, the steering session starts no spec-writer on that CR, as the steps'
    order already says.
  - "The project": the yaml example shows `specifying: parallel` and `batch: slots`, and says
    that `--slots` wins over `batch.slots`.
  - "The watcher", *A watcher's end*: a `config` line is handled as above. Act on it, then start
    the watcher again as the card already says.
  - The factory batch's opening line (the paragraph CR-370 adds): open with `--mode stack` and no
    `--slots` unless the user names a number, so it takes `batch.slots`.
- `griller.md` (~line 17): the spec-writer line names the shared limit (`specifying.parallel`,
  read in `playbook`'s `limits:` line) and the marker's removal at the hand-back.
- `foreman.md`: the `config changed on the board` line in `status` is the Chief of Staff's; the
  Foreman does nothing with it and takes the `order slots` that follows as any order.
- `concepts.md`:
  - "Slots, budget, rounds": `batch.slots` is `open`'s default;
  - "Starting an agent": the playbook's `limits:` line and the marker's removal at the
    spec-writer's hand-back (~line 535 names the marker's line).
- `session-start.md`: the watcher paragraph says the watcher also wakes on a board configuration
  change of these two keys.
- `hosts/claude-code.md` (and the Copilot host file if it holds the watcher's trial row): the host
  row's watcher trial adds a board save of `batch.slots` with an idle session; until it is run,
  the row says the wake on a configuration change is unproved and `status` is the fallback.

### Docs

- `AGENTS.md`, the board exception (no new exception; the CLI names no role):
  - the board edits "each role's agent, model and escalation, per host, and the two limits
    `specifying.parallel` and `batch.slots`, in the project's configuration file in the planning
    surface";
  - the second exception adds: "and, when it saves a change to one of those two limits, one
    `config` line per changed limit (key, old and new value), which wakes the watcher and which
    `status` prints for the batch slots".
  - The sentence "the board itself records nothing and messages no agent" stays.
- `CONTRIBUTING.md`: the same wording in its mirror of that text.
- `docs/web-board.md`:
  - "### Configuration" describes the Limits tab and what a save of each key does;
  - "The signal" names the `config` line.
- `scenario/README.md`: maps the new checks.

## Host and default matrix

The host does not change these keys. The cells differ by where the value comes from. Each cell is
proved by a real CLI flow (`open`, `playbook`, a board PUT through the test client), never a
hand-built record or file shape. The shipped values are read from `config/chantier.defaults.yml`
at the head under test, not copied into the test.

| Key | Source | `open` (no `--slots`) | `playbook` `limits:` | Board tab |
|---|---|---|---|---|
| `batch.slots` | shipped default | slots = shipped value, no label | `batch slots <shipped>`, no label | editable on a surface; shows the default |
| `batch.slots` | surface project `chantier.yaml` (set from the board) | slots = configured, `[surface project]` | `[surface project]` | shows the value; a save writes this file |
| `batch.slots` | repository `chantier.yaml` | slots = configured, `[repository]` | `[repository]` | shows "overridden by the repository" |
| `batch.slots` | any, with `--slots 3` | slots 3, no label | unchanged | unchanged |
| `batch.slots` | configured 0 | refused, exit 2, names the file (Q2) | `batch slots 0 [<layer>]` | saved; journal line written |
| `batch.slots` | no plugin root, no user layer | refused, exit 2, "give --slots" | `batch slots: not set` | n/a |
| `specifying.parallel` | shipped default | n/a | `specifying <shipped>`, no label | shows the default |
| `specifying.parallel` | surface project (from the board) | n/a | `[surface project]` | a save writes this file |
| `specifying.parallel` | repository | n/a | `[repository]` | shows "overridden by the repository" |
| `specifying.parallel` | no plugin root, no user layer | n/a | `specifying parallel: not set` | n/a |
| either | shipped file lacks the key | stops: defaults-file problem | stops: same problem | shows the problem |
| either | no planning surface | as above | as above | read-only, no write, no journal line |

## Order with batch-28

This CR stacks after (its `depends.json` names them): CR-375 (watcher-autostart), CR-370
(factory) and CR-369 (open an empty batch).

- CR-375: `hub/watch.py`'s end lines, `status`'s last lines and the watcher's paragraphs in the
  cards. The `config` event lines print before CR-375's end line.
- CR-370 and CR-369: `open`'s first line and `opening.py`. This CR's `[layer]` label on the slots
  goes in the line as those CRs leave it, including the `no CR, paused, <slots> slots` form; the
  factory's opening line in the cards is CR-370's.

It rebases on whichever of these lands first:

- CR-374 (refusals explained): this CR's `batch.slots: 0` refusal follows its what / why / what
  to do now form;
- CR-376, CR-377, CR-373: AGENTS.md and the cards;
- CR-378 (planning folder validate): AGENTS.md's CLI scope;
- CR-379 (startup core): the Chief of Staff and session-start cards.

## Out of scope

- The CLI refusing or counting spec-writer starts beyond the `limits:` line: the limit is the
  session's (the cards) to keep.
- A limit on spec-critics.
- The board changing a running batch's slots, or messaging any agent.
- A `status` line for the specifying limit.
- A `forge-journal.jsonl` line for a role edit (session-events-board-griller's, later).
- Board writes to the repository's `chantier.yaml` or to the surface's root file: the board keeps
  writing only the surface project's file.
- Live re-reading of `batch.slots` by a running batch: only `order slots` changes it.
- Making timing or any other key editable.

## Evidence

Tests (`tests/`, in-process, few and parametrized, `just test` within its budget):

- Config checks, parametrized over both keys:
  - whole number accepted;
  - 0 accepted for slots and refused for specifying;
  - negative, text and float refused with the exact message;
  - unknown sub-key refused;
  - the unknown-key message lists the new keys.
- The shipped defaults file read from the repository at the head under test:
  `specifying.parallel` and `batch.slots` are present and pass the checks. Paired with it, a
  prepared defaults file lacking one key (a case the shipped file cannot hold) gives the
  defaults-file problem on `playbook`.
- `open` with no `--slots`:
  - shipped default, no label;
  - surface project value, `[surface project]` label;
  - repository value, `[repository]` label;
  - `--slots` wins;
  - configured 0 refused, exit 2, naming the file and the key;
  - no plugin root (`CHANTIER_PLUGIN_ROOT` empty) and no user value: refused, exit 2.
- `playbook` prints `limits:` with the marker count and slugs from real `work/specifying`
  markers, and `at the limit` at the limit.
- The board PUT on each key:
  - writes the surface project's file and keeps its comments;
  - `null` removes the key;
  - a stale SHA gives 409;
  - a dry run writes no file and no journal line;
  - a real save appends exactly one `config` line with old, new and batch;
  - a PUT changing both keys and one role appends two lines, none for the role;
  - an unchanged value appends none;
  - a bad value is refused with the check's text;
  - the response line is role-free (`batch-29 keeps 4 until an order slots`);
  - no surface: read-only, refused.
- `event_text` for each `config` line form; the watcher ends with `events` on a `config` line
  (in `tests/test_forge_hub.py`).
- `status` lines:
  - the `batch.slots` line shows until `order slots --note <n>` is recorded after it, then
    disappears;
  - no `specifying.parallel` line ever;
  - a newer `batch.slots` line replaces an older one.

Scenario (`scenario/run_scenario.py`, the surface-board unit, plus `scenario/README.md`):

1. With a batch running, save `batch.slots` from the board's PUT. A running `chantier watch`
   ends with the `config changed on the board` line; `status` prints it; `order slots --note 6`
   is recorded; `status` no longer prints it.
2. Save `specifying.parallel` to 1 with a `work/specifying` marker present. The watcher ends with
   its line; `playbook` shows `markers 1 (<slug>) ... at the limit`; `status` prints no line for
   it.
3. `open` with no `--slots` after the save gives the configured slots with the
   `[surface project]` label.

Gates: `just check`, and `just eval-dry-run` (the change is under the CLI's `src/`) in the
worktree before the first push. `just scenario` must be green before the PR, because the change
touches the CLI and the cards. The board's web files follow `board/web/DESIGN.md`. No `hooks/`
or `types/` change, so `just mod` is not owed, and there is no pane change.

## Known gaps (for the PR)

- The wake of an idle Claude Code session by the watcher's end on a board save is unproved: the
  scenario proves the watcher ends with the line, not that the host wakes the session. The host
  row's trial (a board save of `batch.slots` with an idle session) proves it; until then `status`
  is the fallback for the slots, and `playbook`'s `limits:` line for the specifying limit.

## Answered questions

- Q1, settled by the Chief of Staff (2026-11-18): A. No plugin root (a skill installed on its own) and no user layer sets a key: what holds?
  - A (recommended): `open` with no `--slots` refuses (exit 2, "give --slots <n>"); the
    `limits:` line prints `not set` for the specifying limit, and the cards then start no
    spec-writer until the user sets `specifying.parallel` (no value of the CLI's own, no
    fallback).
  - B: as A for `open`, but with `specifying.parallel` not set the cards start spec-writers with
    no limit, as today.
