# Answers

This CR was split out of `planning-repo`'s grill of 2026-11-10. The user's decisions are recorded
there (`../planning-repo/02-answers.md`, "Grill of 2026-11-10"):

- answer 1: chantier adopts the surface's tree in both modes;
- answer 4: a running batch's state stays local;
- answer 6: the split into three CRs;
- answer 7: chantier's CR numbers are kept;
- answer 9: the meaning of `3-ready`;
- answer 10: the states of `4-batches`;
- the closing: the name `3-ready`, kept apart from "PR ready to merge".

The tree:

- `1-inbox`;
- `2-backlog/P1..P4`;
- `3-ready`: specified CRs waiting for the next batch;
- `4-batches/1-pending`, `4-batches/2-actives` and `4-batches/3-done`: the states of the CRs of
  the one current batch of the project, with no `batch-<n>` level. The batch's own files
  (`batch.json`, `events.jsonl`, STATUS) stay local to the steering machine;
- `5-archives`;
- `6-trash`.

No migration command (planning-repo answer 8). An existing in-project tree of chantier's own still
has to work after the change; how is the specification's call.

## The specification's open questions (2026-11-10)

1. **`3-done`.** The user chose "Oui, jusqu'au close" (recommended):
   - a merged CR stays in `4-batches/3-done` until `close`, which moves it to `5-archives`;
   - a dropped CR goes to `6-trash` at once.
2. **What puts a CR in `3-ready`.** The user's words: "oui c'est verbal. elle peut aller en ready
   sans spec, c'est le mode "automatable"".
   - It is the user's word.
   - It is NOT refused without a specification: a CR may go to `3-ready` with no specification.
     That is the "automatable" mode, where the Driver works from the request alone.
   - The priority: the recommendation stands (a CR in `3-ready` keeps no priority), since the
     user said yes and did not take up the point.
3. **Converting this repository's existing tree.** The user chose "Oui, conversion auto"
   (recommended): the CLI converts it once, all or nothing, with one line of information. A CR
   whose Driver is working is moved only at its merge or drop.
4. **Diagrams.** The user chose "Dans cette CR" (recommended): the six SVGs are redrawn in this
   CR, and the user reviews their PNG renders in the PR.

Left to the Driver, the recommendation stands:

- `open` and `order add` also take a CR from `3-ready`, proposed first;
- the index moves to `.agents/changes/STATUS.md`.

## Review of PR 95 (2026-11-10)

- The user saw `<changes folder>/4-batches/1-pending/` and asked: since only one batch runs at a
  time ("ce qui est en fait logique"), should the folder not be called `4-batch`?
- The Chief of Staff confirmed: one batch at a time (`concepts.md`, `rails.py`). The missing
  `batch-<n>` level is intended (answer 10). Only the plural misleads.
- The user chose: "4-batch alors", then "corrige dans 95 stp".
- **Decision:** the folder is `4-batch/` (`4-batch/1-pending`, `4-batch/2-actives`,
  `4-batch/3-done`), everywhere `4-batches` appears in PR 95: code, conversion, tests, scenario,
  board, cards, README, docs, SVGs and their PNG renders, and the PR description. The fix goes in
  PR 95, before its merge, in round 3.