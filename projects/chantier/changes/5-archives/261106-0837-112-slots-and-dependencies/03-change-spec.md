# A CR declares what it depends on; a slot is a running Driver

Run this CR after `batch-folder`: it assumes one open batch, a stack by default and `--parallel`.

## Declaring a dependency

A CR's folder may hold `depends.json`, written with the Chief of Staff during the grill:

```json
{"after": ["batch-folder", "foreman-session-name"]}
```

`after` lists slugs, the folder's name without its number, because a CR in the backlog has no
number yet. A CR without the file depends on nothing: nothing else is needed, and no setup.

`open` and `order add` read the file and record `after` in the CR's state as CR ids. A slug found
in `4-archives/` as merged is met and not recorded. They exit 2, naming the slug, on a slug in
neither the batch nor the archives, on a malformed file, and on a cycle.

## Starting a dependent CR

`check_take` in `rails.py` refuses a queued CR until each CR of its `after` is `ready` or
`merged`, and names the ones it waits for. A cancelled dependency stays unmet: the Foreman brings
it to the Chief of Staff as an ask, and the user drops the CR or changes it.

A dependent CR starts on the branch of its last dependency still open, in the order of `after`,
and on the default branch when all are merged: `take` prints that base. A dependency sent back to
a Driver after its dependent started is the stack driver's to restack, as a change is today.

`$CHANTIER stack` refuses an order that puts a CR below one of its `after`. `status` shows what a
queued CR waits for, and the Foreman's card says it picks among the CRs `take` would accept.

## Slots

A slot is a running Driver: a CR in `working`, as today, or a QA driver, which `live` in
`rails.py` does not count yet. A `ready` or `blocked` CR holds none. `concepts.md` says so.

## What follows

- `skills/chantier/scripts/cli/src/chantier/`: `commands.py`, `rails.py`, `status.py`.
- `scenario/run_scenario.py`.
- The cards: `concepts.md`, `chief-of-staff.md` (the grill and the plan show the dependencies),
  `foreman.md`, `driver.md` (the stack driver).
- `README.md`, where it describes a CR's folder or the slots.

## Done when

- `just check` and `just scenario` pass; the scenario covers a CR refused until its dependency is
  ready, then based on its branch; a dependency already archived; a cycle refused at `open`; a
  stack order refused; and a QA driver holding a slot.
