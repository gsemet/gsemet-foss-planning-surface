# Answers

1. Q: What is wanted? User, 2026-11-18: "Alors mets ça aussi en configuration, max parallel
   spec-writer. Default: 4. Il faudrait que ces slots et max spec-writer soient configurables dans
   la page config et qu'un événement soit déclenché pour réveiller le watcher sur cet événement."

## Settled by the Chief of Staff (2026-11-18, the user asks no questions)
- Two keys in the configuration (`config/chantier.defaults.yml`, overridable by the project's and
  the surface's `chantier.yaml` as every key): the most spec-writers running at once, default 4,
  and the batch slots, default the value `open` uses today. The names are the spec-writer's.
- The limit counts spec-writers only (the user's word); a spec-critic, short and read-only, does
  not count. It holds for the Chief of Staff and a Griller together on one project: before a
  spec-writer starts, the session counts the running ones (the `work/specifying` markers of the
  project's planning folder) and starts none at the limit; the next one waits for a hand-back.
- The slots key is the default of `open` (with no `--slots`); `--slots` still wins. A running
  batch keeps its recorded slots until an `order slots <n>`.
- The Configuration page of the board edits both keys, with the same checks as its other keys
  (whole numbers; slots 0 or more, spec-writers 1 or more).
- The event: when the board saves a change to one of these keys, it appends one line to the
  project's `forge-journal.jsonl` (`config` event: key, old and new value). A running watcher
  reads it as it reads a merge and ends, which wakes the Chief of Staff. `status` prints the line
  until it is acted on, as for the journal's merges.
- What the Chief of Staff does on that event: slots changed and a batch runs: it gives
  `order slots <n>` for the running batch (an order, recorded, relayed to the Foreman as every
  order), and says so to the user in one line; spec-writers raised: it starts the next waiting
  ones up to the new limit; lowered: it stops none, and starts none until the count is under it.
- The board never edits a batch and never messages an agent: the change to a running batch stays
  an order of the Chief of Staff. AGENTS.md names the new journal line among the board's writes.
- With no watcher running (no batch runs), the event waits for the next `status`.

## Settled by the spec-writer (2026-11-18)
- Key names: `spec_writers.parallel` and `batch.slots`, checked like `long_gate.parallel` in
  `playbook/config.py`.
- Each value resolves with its layer: the user layers strongest first, then the shipped
  defaults, as timing does. The CLI's own fallback for an older defaults file is 4 and 4.
- `playbook` prints a `limits:` line with the running count and slugs (the `work/specifying`
  markers in `1-inbox`, `2-backlog/P1..P4` and `3-ready`); the cards read it before each start.
- The journal line's shape: `kind: config`, `key`, `old`, `new` (effective values), `batch` (the
  running or paused batch, or null), `by: board`. It has its own dedup key, and there is no line
  for a dry run or an unchanged value.
- `edit_text` is generalised to top-level `<key>.<sub>` paths. A `null` value removes the key
  from the surface project's file.
- Stacks after CR-375, CR-370 and CR-369; rebases on CR-374, CR-372, CR-376, CR-377 and CR-373.

## Settled by the Chief of Staff (spec-writer's questions, 2026-11-18)
- Q1 (A): `status` prints the spec-writers line until it is acted on: for a raised limit, once a
  spec-writer has started after the line; for a lowered one, once fewer run than the new limit.
- Q2 (A): a configured `batch.slots: 0` makes `open` with no `--slots` refuse (exit 2), naming the
  file and the key, as `--slots 0` is refused today.
- Q3 (A): a paused batch gets the `order slots <n>` too, so it resumes with the new value.
