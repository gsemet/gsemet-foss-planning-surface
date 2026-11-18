# Change spec: spec-writers and slots set from the board's configuration

Source: the user, verbally, 2026-11-18 (no issue). Short name: `config-spec-writers-slots`.

## Goal

The user sets two numbers in the project's configuration and changes them from the web board's
Configuration page:

- how many spec-writers run at once on the project (default 4);
- how many slots a new batch gets (default 4, the value `open` uses today).

When the user saves a change to either number on the board, the Chief of Staff learns about it at
once, through the forge journal the watcher already reads, and acts on it:

- slots changed while a batch runs: it gives `order slots <n>`;
- spec-writer limit raised: it starts the waiting spec-writers up to the new limit;
- spec-writer limit lowered: it lets the running ones end and starts no new one until the count is
  under the limit.

## Decisions carried (02-answers.md)

1. Two keys in the configuration, in `config/chantier.defaults.yml`, overridable by the
   surface's, the surface project's and the repository's `chantier.yaml` like every key. Names:
   `spec_writers.parallel` (default 4) and `batch.slots` (default 4).
2. The limit counts spec-writers only. A spec-critic does not count. The Chief of Staff and a
   Griller share one limit on one project. Before starting a spec-writer, the session counts the
   running ones (the `work/specifying` markers in the project's planning folder) and starts none
   at the limit. The next one waits for a hand-back.
3. `batch.slots` is `open`'s default when `--slots` is not given; `--slots` still wins. A running
   batch keeps its recorded slots until an `order slots <n>`.
4. The board's Configuration page edits both keys, checked like its other keys: whole numbers,
   slots 0 or more, spec-writers 1 or more.
5. When the board saves a change to either key, it appends one `config` line to the project's
   `forge-journal.jsonl` (key, old value, new value). A running watcher reads that line as it reads
   a merge, then ends, which wakes the Chief of Staff. `status` prints the line until it is acted
   on, as it does for the journal's merges.
6. What the Chief of Staff does on the event:
   - slots changed and a batch runs: it gives `order slots <n>` (recorded and relayed to the
     Foreman like every order) and tells the user in one line;
   - spec-writers raised: it starts the next waiting ones up to the new limit;
   - spec-writers lowered: it stops none and starts none until the count is under the limit.
7. The board never edits a batch and never messages an agent. The change to a running batch is
   always the Chief of Staff's order. AGENTS.md names the new journal line among the board's
   writes.
8. When no watcher runs (no batch runs), the event waits for the next `status`.

## What changes

Paths below are relative to `skills/chantier/scripts/cli/src/chantier/` unless they start at the
repository root.

### Shipped defaults: `config/chantier.defaults.yml`

Two new top-level keys, each with a one-line comment:

```yaml
spec_writers:
  parallel: 4   # the most spec-writers running at once on the project (Chief of Staff and Griller)
batch:
  slots: 4      # the slots `open` gives a batch when no --slots is given
```

### Configuration checks: `playbook/config.py`

- `spec_writers` and `batch` join the known top-level keys.
- The unknown-key message adds them to its list: "hosts", "prices", "board", "ci", "long_gate",
  "spec_writers", "batch".
- Each key is checked the same way `long_gate` is:
  - `spec_writers: "parallel" is a whole number, 1 or more, found "<v>"`;
  - `batch: "slots" is a whole number, 0 or more, found "<v>"`.
  - An unknown sub-key under either key is refused the same way `long_gate` refuses one.
- A bad value in any layer is a configuration problem. As with any key, `open` and `playbook`
  report it with the file's path.

### Reading the limits: `playbook/layers.py`, `plugin_files.py`

- A new reader resolves each value with the layer it came from. It searches the user layers,
  strongest first (repository, surface project, surface), then the shipped defaults, the way
  `playbook/timing.py` resolves timing.
- `plugin_files.read_limits(repo)` sits next to `read_timing` and reads the plugin's shipped
  defaults file. When the shipped file has no value (an older defaults file), the CLI's own
  defaults are 4 and 4.

### `chantier open` (`declare/opening.py`, `commands/opening.py`, `commands/opening_record.py`)

- `--slots` no longer has a default of 4. When it is not given, `open` uses `batch.slots` from
  the configuration.
- When the slots came from a user layer, the first line of the output names that layer, using the
  same bracket labels the playbook uses (`[surface project]`, `[repository]`, `[surface]`):
  `opened <batch> on <host>: <n> CRs, <slots> slots [surface project], <mode>, steering ...`.
  A shipped default or a given `--slots` gets no label, so the output is the same as today.
- A configured `batch.slots: 0` with no `--slots`: see open question Q2. The spec assumes the
  recommended answer: `open` refuses with exit 2 (usage) and names the file and the key:
  `open: batch.slots is 0 in <file>: a new batch needs 1 slot or more; give --slots <n>, or set it on the board's Configuration page`.
  An explicit `--slots 0` is refused as it is today ("slots and budget must be positive").
- `order slots <n>` does not change. It still accepts 0 or more, and 0 holds a running batch.

### `chantier playbook` (`playbook/lines.py`, `commands/` caller)

A new `limits:` line comes after the `timing:` lines. It follows the playbook's label rule: no
label for a shipped default, `[<layer>]` otherwise.

```
limits: spec-writers 4, running 2 (cr-a, cr-b); batch slots 6 [surface project]
```

- "running" counts the `work/specifying` markers in `1-inbox/`, `2-backlog/P1`..`P4` and
  `3-ready/` of the project's planning folder.
- It lists the CR slugs, in folder order.
- The line also ends with `at the limit: start none` when running >= the limit.

The cards read this line before each spec-writer start (see Cards). The CLI does not refuse a
spec-writer start: the limit is the session's to keep, as the decision says.

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
  - `edit_surface_file` accepts a second change shape, `{"key": "spec_writers.parallel" |
    "batch.slots", "value": <int> | null}`. `null` removes the key from the surface project's
    file, so the weaker layers take over again.
  - Each change keeps the same lock, SHA conflict check (`409 stale`), dry run and whole-file
    validation as the role edits.
  - A value outside the checks is refused with the check's own text from `config.py`.
- `playbook/edit_text.py`: the ruamel edit that keeps comments now also sets and removes a
  top-level `<key>.<sub>` path, not only `hosts.<host>.roles.<role>.<key>`.
- `board/config_api.py`, on a real (non-dry-run) write that changes one of the two keys' effective
  value in the file:
  - it appends the `config` journal line (below);
  - the board journal's `config` line stays as it is today;
  - the response lines say what happens next, in place of the bare `applies at the next batch`
    for these keys:
    - `batch.slots`, with a batch running or paused: `slots 4 -> 6: the Chief of Staff orders it for <batch>`;
    - `batch.slots`, with no batch running or paused: `slots 4 -> 6: from the next open`;
    - `spec_writers.parallel`: `spec-writers 4 -> 2: from the next spec-writer start`;
    - role edits keep `applies at the next batch`.
- The board writes no journal line for a dry run, for a save that leaves the value unchanged, or
  for a key other than these two.
- `board/web/js/views/config.js`, `config-timing.js`:
  - a third tab, "Limits", next to Models and Timing, with its own hash address;
  - two number inputs (min 0 for slots, min 1 for spec-writers);
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

- A new kind, `config`, written by the board (`by: "board"`):

  ```json
  {"seq": 12, "t": "...", "by": "board", "kind": "config", "key": "batch.slots", "old": 4, "new": 6, "batch": "batch-29"}
  ```

  - `old` and `new` are the effective values before and after the save, all layers included;
  - `batch` is the batch running or paused at the save, or `null` when there is none.
- Dedup: a `config` line has its own key (`kind`, `key`, `old`, `new`, `t`). Two saves with the
  same values make two lines. The merge key does not swallow a config line.
- `event_text` gets a `config` branch:
  - `config changed on the board: batch.slots 4 -> 6; for the Chief of Staff: order slots 6 for batch-29`
  - `config changed on the board: batch.slots 4 -> 6; from the next open (no batch)`
  - `config changed on the board: spec_writers.parallel 4 -> 6; for the Chief of Staff: start the waiting spec-writers up to 6`
  - `config changed on the board: spec_writers.parallel 4 -> 2; for the Chief of Staff: start none until fewer than 2 run`
- `lines(...)`, used by `status`, prints the newest `config` line per key while it is not acted on:
  - `batch.slots`: the line's batch is the current batch (running or paused), its recorded slots
    differ from `new`, and no `order slots` was recorded after the line's `t`;
  - `spec_writers.parallel`, by the recommended answer to Q1: when raised, until a
    `work/specifying` marker is newer than the line; when lowered, until the running count is
    under `new`.
  - A newer line for the same key replaces an older one. A line for a closed batch is not
    printed.
- The module's docstring names the board's new line.

### The watcher: `hub/watch.py`

- `Watch.poll` already reads every line with `seq` above its cursor, whatever its kind. A `config`
  line counts as a new event like a merge: the watcher ends 20 s after the last one and prints
  `event_text` for it.
- The watcher's other end lines (`no-batch`, and the end line CR-375 brings) stay as they are.
- The forge hub does not change: the board writes the line, and the hub never reads or writes
  `config` lines.

### `chantier status` (`commands/batch_status.py`)

- `_seen_lines` prints the `config` lines from `journal.lines`, after the merges.
- With no batch running or paused, `status` refuses as it does today, and nothing is lost:
  - `open` reads `batch.slots`;
  - each spec-writer start reads the `limits:` line.

  The line for a batch-less save is therefore only informative, and `status` does not print it.

### Cards (`skills/chantier/references/`)

- `chief-of-staff.md`:
  - Entry points: a row for `config changed on the board` (from the watcher or `status`). It
    says:
    - for `batch.slots` with a running or paused batch: `order slots <n>`, then one line to the
      user;
    - for `spec_writers.parallel`: start the waiting ones up to the limit, or let the running
      ones end.
  - The spec-writer paragraph (the `work/specifying` guard):
    - read `playbook`'s `limits:` line before each spec-writer start;
    - start none at the limit; keep the waiting CRs in order and start the next on a hand-back;
    - a spec-critic is not counted.
  - "The project": the yaml example shows `spec_writers: parallel` and `batch: slots`, and says
    that `--slots` wins over `batch.slots`.
  - "The watcher", *A watcher's end*: a `config` line is handled like a merge. Act on it, then
    start the watcher again as the card already says.
- `griller.md`: the spec-writer line names the shared limit and the `limits:` line.
- `foreman.md`: the `config changed on the board` line in `status` is the Chief of Staff's; the
  Foreman does nothing with it and takes the `order slots` that follows as any order.
- `concepts.md`:
  - "Slots, budget, rounds": `batch.slots` is `open`'s default;
  - "Starting an agent": the playbook's `limits:` line.
- `session-start.md`: the watcher paragraph says the watcher also wakes on a board configuration
  change.

### Docs

- `AGENTS.md`, the board exception:
  - the board edits "each role's agent, model and escalation, per host, and the spec-writers and
    batch slots limits, in the project's configuration file in the planning surface";
  - the second exception adds: "and, when it saves a change to those two limits, one `config`
    line (key, old and new value), which wakes the watcher and which `status` prints for the
    Chief of Staff to act on".
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
| `spec_writers.parallel` | shipped default | n/a | `spec-writers <shipped>`, no label | shows the default |
| `spec_writers.parallel` | surface project (from the board) | n/a | `[surface project]` | a save writes this file |
| `spec_writers.parallel` | repository | n/a | `[repository]` | shows "overridden by the repository" |
| either | no planning surface | as above | as above | read-only, no write, no journal line |

## Order with batch-28

This CR is new in the inbox and is not in batch-28. It changes files that batch-28 CRs also
change, so it stacks after:

- CR-375 (watcher-autostart): `hub/watch.py`'s end lines, `status`'s last lines and the
  watcher's paragraphs in the cards. The `config` event lines print before CR-375's end line.
- CR-370 (factory) and CR-369 (open an empty batch): `open`'s first line and `opening.py`. This
  CR's `[layer]` label on the slots goes in the line as those CRs leave it, including the
  `no CR, paused, <slots> slots` form.

It rebases on CR-374, CR-372 (which also changes `config/chantier.defaults.yml`), CR-376, CR-377
and CR-373, whichever lands first; all of them edit AGENTS.md. No `depends.json` is needed beyond
landing after CR-375, CR-370 and CR-369, and those three are in batch-28.

## Out of scope

- The CLI refusing or counting spec-writer starts beyond the `limits:` line: the limit is the
  session's (the cards) to keep.
- A limit on spec-critics.
- The board changing a running batch's slots, or messaging any agent.
- Board writes to the repository's `chantier.yaml` or to the surface's root file: the board keeps
  writing only the surface project's file.
- Live re-reading of `batch.slots` by a running batch: only `order slots` changes it.
- Making timing or any other key editable.

## Evidence

Tests (`tests/`, in-process, few and parametrized, `just test` within its budget):

- Config checks, parametrized over both keys:
  - whole number accepted;
  - 0 accepted for slots and refused for spec-writers;
  - negative, text and float refused with the exact message;
  - unknown sub-key refused;
  - the unknown-key message lists the new keys.
- The shipped defaults file read at the head: `spec_writers.parallel` and `batch.slots` are present
  and pass the checks.
- `open` with no `--slots`:
  - shipped default, no label;
  - surface project value, `[surface project]` label;
  - repository value, `[repository]` label;
  - `--slots` wins;
  - configured 0 refused, exit 2, naming the file.
- `playbook` prints `limits:` with the running count and slugs from real `work/specifying`
  markers, and `at the limit: start none` at the limit.
- The board PUT on each key:
  - writes the surface project's file and keeps its comments;
  - `null` removes the key;
  - a stale SHA gives 409;
  - a dry run writes no file and no journal line;
  - a real save appends exactly one `config` line with old, new and batch;
  - an unchanged value appends none;
  - a bad value is refused with the check's text;
  - no surface: read-only, refused.
- `event_text` for each `config` line form; the watcher ends with `events` on a `config` line
  (in `tests/test_forge_hub.py`).
- `status` lines:
  - the slots line shows until `order slots <n>` is recorded, then disappears;
  - the spec-writers line follows Q1's rule;
  - a newer line replaces an older one for the same key.

Scenario (`scenario/run_scenario.py`, the surface-board unit, plus `scenario/README.md`):

1. With a batch running, save `batch.slots` from the board's PUT. A running `chantier watch`
   ends with the `config changed on the board` line; `status` prints it; `order slots 6` is
   recorded; `status` no longer prints it.
2. Save `spec_writers.parallel` to 1 with a `work/specifying` marker present. `playbook` shows
   `running 1 ... at the limit: start none`.
3. `open` with no `--slots` after the save gives the configured slots with the
   `[surface project]` label.

Gates: `just check`, and `just eval-dry-run` (the change is under the CLI's `src/`) in the
worktree before the first push. `just scenario` must be green before the PR, because the change
touches the CLI and the cards. The board's web files follow `board/web/DESIGN.md`. No `hooks/`
or `types/` change, so `just mod` is not owed, and there is no pane change.

## Open questions

- Q1. When does `status` stop printing the spec-writers line?
  - A (recommended): when raised, once a newer spec-writer marker exists; when lowered, once the
    running count is under the limit.
  - B: never; the line shows only at the watcher's end.
  - C: no event line in `status`; the `limits:` line in `playbook` is enough.
- Q2. A configured `batch.slots: 0` with `open` and no `--slots`.
  - A (recommended): refuse with exit 2, naming the file and the key, as `--slots 0` is refused
    today.
  - B: open the batch held (0 slots, no Driver starts) until an `order slots <n>`.
- Q3. A paused batch when `batch.slots` changes.
  - A (recommended): the Chief of Staff orders `order slots <n>` for it too, so it resumes with
    the new value.
  - B: only a running batch gets the order; a paused one keeps its slots.
