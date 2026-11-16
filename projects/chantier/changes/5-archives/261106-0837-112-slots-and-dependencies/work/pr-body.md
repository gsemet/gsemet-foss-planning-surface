CR-112. A CR says what it depends on, and a slot is what really runs: a Driver.

## What changes

- **Declaring a dependency:** a CR's folder may hold `depends.json`, `{"after": ["<slug>", …]}`, written during the grill. `open` and `order add` record `after` as CR ids; a slug archived as merged is met and not recorded. They exit 2, naming it, on an unknown slug, a malformed file or a cycle, and a refused `open` opens and moves nothing. A CR without the file depends on nothing.
- **Starting a dependent CR:** `take` refuses a queued CR until each CR of its `after` is `ready` or `merged`, and names what it waits for. A cancelled dependency stays unmet.
- **Its base:** the branch of its last dependency still open, in the order of `after`, or the default branch when all are merged; `take` prints it.
- **The stack:** `stack` refuses an order that puts a CR below one of its `after`.
- **Showing it:** `status` and the STATUS files show what a queued CR waits for. One rule, `waits_for` in `rails.py`, serves `take`, `status` and `status.py`. `STATUS.json` stays at `schema` 2 and gains a `waits` list; the mod shows the new label and needs no change.
- **Slots:** a slot is a running Driver: a CR in `working`, or a QA driver. An open `order qa` holds a slot until `order done`, and `order qa` is refused when no slot is free, so its Driver can always start. A `ready` or `blocked` CR holds none.
- **Cards and docs:** `concepts.md`, `chief-of-staff.md`, `foreman.md`, `driver.md` and `README.md`.

## Decisions the specification left open

- A QA order that finds every slot busy is refused rather than queued: the Chief of Staff orders it again later.
- A CR with an `after` takes its base from that rule in a stack too, not from its place in the chain.

## Checks

- `just check` and `just scenario` pass at this head, on Windows; CI runs them on the other platforms.
- The scenario has a new case: a CR refused until its dependency is ready, then based on its branch; a dependency already archived; a cycle refused at `open`; a stack order refused; a QA driver holding a slot.
