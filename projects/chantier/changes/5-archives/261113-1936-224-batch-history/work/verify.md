# Verify CR-224

Head: 4891c446f8d5eaa78f1cb9ef7c6f690f830292df

Scratch repo (git, bare remote, AGENTS.md) driven by the CLI of this worktree at that head. Outputs in evidence/ (close-preview.txt, close-yes.txt, scratch-batches/).

Claims, all judged at 4891c44:

1. Gate pass: gate log first line `gate CR-224 ... head 4891c446...`; `just check` and `just scenario` pass at that head (github 695/695, gitlab 676/676), `result: pass at 4891c446...`. CI: 5 checks green per Driver's log note; PR head on the forge is 4891c44.
2. Backfill (spec "The backfill", step 8): seeded archives `01-eval-real` (merged), `batch-03` (merged + trashed, with a top-level retro.md), `.batch-number` 4, no `batches/`. First `status` printed once on stderr `backfilled 5-archives/batches: batch-01 to batch-04 (2 with no trace)`; wrote batch-01..04 json+md. batch-01: closed, `former_id` `01-eval-real`; batch-02 and 04 unknown; batch-03: one merged, one dropped, retro listed and linked from batch-03.md, retro still in place. A second `status` wrote nothing and printed no backfill line. PASS.
3. `status` with no batch: `error: no running batch: run chantier open first; last closed: batch-03`. PASS (spec step 7).
4. Next number: records up to 04 and .batch-number 4 gave `opened batch-05`; `.batch-number` still 5. PASS.
5. `open` record: batch-05.json schema 1, running, `opened` equal to batch.json `created`, mode, steering, host, budget_usd 50.0, crs [], report null, backfill null. `status` second line: `last closed: batch-03 (backfilled, no close date), 1 merged, 1 dropped`. PASS.
6. `close` preview: prints `retro: ... goes into .../batch-05.md` and `record: ...`; hashes of every file under .agents/changes identical before and after. PASS.
7. Planted batch-05.md: preview and `--yes` both exit 3, "refusing to overwrite ... nothing was closed", all files unchanged by hash. PASS. (The mid-close rollback path is proved by the scenario's step 6, not re-run here.)
8. `close --yes`: lines `retro: kept in ...batch-05.md` and `record: ...batch-05.json closed`; JSON closed with `closed` set, cost_usd 3.0 equal to printed Total $3.00, two crs with result, archive, pr, rounds; batch-05.md has the header line, Completion table, Cost bullets, and the retro verbatim; 4-batch/retro.md gone and no new retro.md in an archive (only the old pre-existing backfilled one). Then `status` with no batch names batch-05. PASS.
9. Index: scenario step 9 checks `merged`/`merged_total` skip `batches`; code diff in status.py `_past` read. PASS (carried from gate run, same head). External mode: scenario step 10 in the same gate run.
10. Ignore list: `git check-ignore` exits 1 for batch-05.json, `.gitignore` lists only `.batch-number`, none of the records. PASS.
11. PR description as posted equals work/pr-body.md; Summary and Changes match the 15-file diff; Known gaps "None" is consistent (no UNVERIFIED claim; the pane rule does not apply, no hooks/ or register.tsx change). Review box `approved at 4891c44` matches the log note `r2 approved at b3cc2bec, committed as 4891c44`. The unticked Verified/Evidence/CI boxes are the later steps' to tick. PASS.

Notes (not failures):
- In my scratch, I hand-edited the dropped CR to `cancelled` without `cancel`, so it stayed in 3-done and its archive path is `5-archives/...`; the real `cancel` flow trashes it and the scenario (step 4) checks the `6-trash/` prefix.
- batch-02 `unknown` has `report: null` though a batch-02.md is written; the spec's field table says `report` is set once written, but its backfill paragraph says "everything else null". Harmless to the UI.
- The planted-md refusal text says "batch-05 is already closed" (the preview/refusal cause); spec wording only requires "refusing to overwrite".
- Not run by me: Linux/macOS (CI covers), the on-this-machine backfill (post-merge).

VERIFIED
