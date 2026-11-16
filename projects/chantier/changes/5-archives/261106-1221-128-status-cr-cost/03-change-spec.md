# `status` gives every CR's cost, merged ones included

## Problem

The Chief of Staff's report has a cost column, and `status`, the command it is built from, has no
cost on a CR's row. So the figure is looked up elsewhere, and a merged CR is missing from each place
looked at: `3-requests/STATUS.md` and the live folders list active CRs only, and `cost --by cr` is
cut at `MAX_LINES`. The report then says it has no figure, while `batch.json` holds it.

## Change

- `status`: a CR's row ends with its cost, `$2.19`, or `-` when it has none yet. It holds for every
  state, merged included, and comes from `cost_usd` in `batch.json`.
- `cli.py`: `cost` joins `FULL_OUTPUT`, so `cost --by cr` lists every CR.
- `chief-of-staff.md`: a report's cost column comes from the rows of `status --refresh`; a merged CR
  has its figure there too.

## Out of scope

`3-requests/STATUS.md`, the board, and the archives: they stay as they are. No new command.

## Done when

- On a batch with a merged CR, `status` prints that CR's cost, and `cost --by cr` prints every CR.
- `just check` and `just scenario` pass.
