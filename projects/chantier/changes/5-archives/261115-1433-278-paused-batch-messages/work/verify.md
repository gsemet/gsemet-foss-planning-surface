# Verify CR-278

Head: 6114491c3396f6ef33423106adae0f543f288161

All claims judged at 6114491c3396f6ef33423106adae0f543f288161, running the worktree's code
(`uv run --no-sync --project C:/Users/gaeta/Projets/chantier.worktrees/batch-18-CR-278 chantier ...`)
in scratch projects under the session scratchpad (outside the repo). Setup: `init`, `file`, `triage --ready`,
`open`, `foreman set sess1 --epoch 1`, `cancel CR-101 --epoch 1`, `pause --epoch 1` gives a paused batch-01;
a fake Foreman transcript (`CHANTIER_CLAUDE_PROJECTS`) lets `cost` price.

## 1. Reading commands read the only paused batch (exit 0)
```
$ chantier cost --by cr          -> batch-01: $0.065 over 5 model calls / foreman: $0.065 (5 calls) ...   exit=0
$ chantier cost --by cr --batch batch-01 -> same first lines
$ chantier cost --explain        -> batch-01: $0.065 over 5 model calls / Foreman: $0.065 (5 calls, 100%) ...  exit=0
$ chantier cost --summary        -> Total: $0.07, no budget ...  exit=0
$ chantier status                -> batch-01 paused steering Foreman ... (paused, cost to date)   exit=0
```
(Without the transcript `cost` fails later with `no Foreman transcript recorded`, the same with and without
`--batch`: resolution succeeded.)

## 2. A writing command refuses naming the batch and --batch, no `chantier open`
```
$ chantier asks            -> error: no running batch; paused: batch-01: pass `--batch batch-01`   exit=2
$ chantier asks hello      -> same   exit=2
$ chantier status --refresh-> same   exit=2
```

## 3. Several paused batches
Only one batch folder can exist in the product (`open` refuses: "batch-01 is not closed"), so two paused
batches are reached by patching `Repo.open_batches`/`paused_batches` in a wrapper process (the worktree's `main`):
```
cost --by cr / cost --explain / status -> error: no running batch; paused: batch-17, batch-18: pass `--batch <name>`  exit=2
```
The parametrized unit test `test_a_paused_batch_is_read_when_alone_and_named_otherwise` covers the same states.

## 4. No batch at all: text unchanged
```
$ chantier status | cost --by cr | cost --explain | asks
error: no running batch: run `chantier open` first; no batch closed yet   exit=2   (identical to base batch.py:223)
```

## 5. Board on a held port
```
listening socket 127.0.0.1:53465, then: chantier board --host 127.0.0.1 --port 53465
exit=4  stdout=''
stderr='error: board not started: port 53465 on 127.0.0.1 is in use (a board may already run there, or another program): pass --port <n> (0: any free port)\n'
```
One line, names the port and --port.

## 6. Gate and PR description
- Long gate: CI `just scenario (ubuntu-latest)` green at 6114491 (Driver's note `CI: gh pr checks 229 at 6114491: all 5 pass`); it covers the scenario section 9 and held-port checks added in the diff. No local `gate` pass recorded; the project's rule names the pipeline job as the long gate.
- `gh pr view 229`: Summary, Deliverables table, held-port bullets, Changes (batch.py, repo.py, cost, batch_status, address.py, command.py, two docs, tests, scenario) match the diff of 11 files; exit codes unchanged; Known gaps lists the local scenario time-limit overrun. Renders (sections, table, details fold). Review/Verified/CI boxes pending, as expected before this verdict.

VERIFIED

## 7. Description pass at 6114491c3396f6ef33423106adae0f543f288161
`gh pr view 229 --json body,headRefOid`: head is 6114491. Sections in template order, fold with blank lines, nothing after `</details>`, Known gaps filled, no role names, CR name only in Internal references. Review box (`approved at 9d4136c`, committed as 6114491) matches `chantier log CR-278`: "r1 approved at 9d4136c, committed as 6114491". CI box matches the note "gh pr checks 229 at 6114491: all 5 pass". Summary, Deliverables, Changes match the 11-file diff (section 6). Test plan items carry 6114491.

VERIFIED
