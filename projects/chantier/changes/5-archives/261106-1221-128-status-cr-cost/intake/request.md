# `status` gives every CR's cost, merged ones included

The user, after the Chief of Staff's report showed "n/d" for the merged CRs, not for the first time:
"ca fait plusieurs fois que tu fais ca, donc il y a un probleme a regler pour que ca soit bon meme
dans des sessions suivantes"

Found:

- `batch.json` holds `cost_usd` for every CR, merged ones included, and each archive's `STATUS.json`
  keeps it. Nothing is lost.
- `status` is the command a report is built from, and its CR rows carry no cost.
- `cost --by cr`, which `chief-of-staff.md` names for a CR's figure, is cut by `MAX_LINES` in
  `cli.py`: `cost` is not in `FULL_OUTPUT`, so batch-06's output ends in "… 5 more lines" and
  CR-119 is not in it.
- `3-requests/STATUS.md` and the live folders list active CRs only: a merged CR is gone from both.
