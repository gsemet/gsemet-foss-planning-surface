**Eval run: do not merge.** The maintainer decides what happens to this PR.

## Why

The batch report's `Orchestration ... work ...` line counted a Driver that starts a worker as
orchestration, so the split said little about the cost of the frame.

## What changes

- `_cost_summary` prints one line with three amounts and shares:
  `Foreman $0.39 (24%), Drivers $0.91 (57%), workers $0.31 (19%)`. The Foreman is the main
  session, the Drivers are any agent that started another one, and the workers are the rest. It
  comes from the transcripts' parent links, and the CLI still knows no role.
- `status`, `STATUS.md`, `cost --summary` and `land` all go through `_cost_summary`.
- A helper, `_apportion` (largest remainder), makes the three printed amounts add up to the printed
  total in cents and the shares add up to 100%. A printed amount can therefore differ by one cent
  from its true value.
- The CLI help, `README.md` and `docs/use-cases.md` follow. The cards and the eval kit did not
  mention the old line, so they are unchanged.
- The scenario's fake transcripts give each CR Driver a worker child, and a new check asserts that
  the three amounts add up to the total.

## Checks

- `just check`: 25 passed.
- `just scenario`: passed at cd7cb11, through `chantier gate`.
