A batch now runs its CRs in parallel by default: a CR starts as soon as a slot is free, and the stack driver rebases afterwards. Touching the same file is no reason to wait.

This replaces PR 55, which was merged into CR-121's branch and not into `main`. It holds the same commit, alone on `main`.

## What changes

- **Cards:** `depends.json` is only for a CR that needs another's result. The Chief of Staff may propose a queue with no real dependency, with a reason in the plan that the user's go approves. The plan says how many CRs start at once, on how many slots. The Foreman takes every CR `take` accepts and holds none in reserve. `concepts.md` says the same.
- **Start base:** a stack's CR with no open dependency starts on the default branch, and `take` prints that base. A CR with an open dependency still starts on the branch of its last open dependency. `take stack` is unchanged: start base and place in the stack are kept apart.
- **`order after <cr> --note "<CR ids, comma separated, or - for none>"`:** replaces the `after` of a queued CR, with no drop and no new number. It exits 2 on a CR that is not queued, an unknown CR or a cycle.
- **Scenario:** runs a stack with independent CRs taken at once, then stacked, and changes a dependency with `order after`.

## Known limit

An independent CR's first `ship` logs the CR below it as its base, while its PR opens elsewhere, until the stack driver ships it again. Nothing reads that field to decide anything; the Inspector judged it not a defect against the specification.

## Checks

- `just check`: 26 passed.
- `just scenario`: passed at 4cbc948 through `chantier gate`.
