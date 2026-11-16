# Verification of CR-235

Head: be7034f33a56ef91668ade8cfee31da63c3fdce8

Method: the long gate passed at this head (work/gates/20261114-055458.log: pytest 63 passed, github 705/705, gitlab 686/686, `result: pass at be7034f`). I did not rerun it. I read the diff against the base and the two scenario transcripts, and ran one targeted repro (evidence/repro.py, output evidence/repro.out).

| Claim | Head | Proof | Result |
| --- | --- | --- | --- |
| E1 `order merged` stops the CR's gate (group named, suite gone, STOPPED exit 4, last gate event `stopped`, 3-done, next gate runs at once) | be7034f | scenario check present and `[x]` in both transcripts (evidence/scenario-checks-*.txt); code `orders_apply._stop_gate` -> `gate_run.stop_gate`, shared with `gate --stop`, after the refusals, release and plain CR | pass |
| E2 lock names another CR: nothing stopped | be7034f | `_stop_gate` returns `[]` when `h.cr != cr_id` (diff, orders_apply.py) | pass (code; no dedicated scenario line) |
| E3 reused pid is not the suite (lock, cancel, order merged) | be7034f | `alive_since` repro: process started after the file time returns False; scenario checks "lock naming a reused pid", "`cancel` does not signal a reused pid", "`order merged` does not signal a reused pid" `[x]` | pass |
| E4 ticket with reused pid deleted | be7034f | `_ticket_cr` uses `alive_since(pid, mtime(ticket))`; scenario check "a ticket naming a reused pid is deleted" `[x]` | pass |
| E5 activity lines | be7034f | repro.out: holder live -> `gate running`; others -> `gate queued behind CR-3`; empty lock -> `gate queued` / `gate queued behind CR-2`; dead holder + reused pg -> not running; dead ticket -> no line, ticket kept (status reads only); scenario checks `[x]` | pass |
| E6 card diff | be7034f | `git diff` of foreman.md: the "Your means" list and the lost-Driver Suspect rule only. Cosmetic: two lines wrapped short/long, harmless | pass |
| E7 check and scenario, both forges | be7034f | gate log above; PR body records mypy for three platforms; CI still pending | pass locally, CI pending |
| Unreadable creation time: alive for waiting, not stopped | be7034f | `stop_gate` passes `unreadable=False`; waiting and activity pass `True` | pass |
| pr-body.md matches the diff | be7034f | Deliverables, new modules (`gate_run.py`, `activity.py`), changed files and the order-before-move decision all match the diff. Test plan boxes "New or changed tests", Evidence, Verified, CI stay open for the caller | pass |

Not run: Linux and macOS behaviour of `alive_since` (psutil), covered only by CI.

Verdict: VERIFIED

## Pass on the posted description (be7034f)

Checked the posted body (gh pr view 178) against the diff, the previous table and pr-template.md: sections and fold in order, Known gaps present, no internal reference outside Internal references, Deliverables names (procs.alive_since, gate_lock, gate_run.stop_gate, activity) exist in the diff, Test plan SHAs be7034f, CI green at be7034f (all five jobs pass). Cosmetic only: the Test plan item 'New or changed tests' is still unchecked though the scenario steps it names exist; for the caller to tick.

Verdict: VERIFIED

## Delta pass at the restack (6641ff1ca862bb3a0192663eb35cf4ec1b8a833f)

Head: 6641ff1ca862bb3a0192663eb35cf4ec1b8a833f

Move: be7034f -> 6641ff1, rebased onto main febd917 (CR-237 merged).
- `git range-diff 2d9a2aa..be7034f febd917..6641ff1 --stat`: the CR's commit is `=` (identical patch); the other six are CR-237's, now in main.
- `git diff --stat be7034f 6641ff1`: only `chief-of-staff.md` and `status-layout.md` differ; no code, scenario, foreman.md or CLI file.
- Claims E1 to E6, unreadable creation time: carried from be7034f: the tree they exercise is byte-identical (command above).
- Rerun at 6641ff1: `uv run --locked python evidence/repro.py` from the worktree: dead pid False, reused pid False, live True; holder live -> `gate running`; `gate queued behind CR-3`; empty lock -> `gate queued`; dead ticket -> no line, ticket kept. Same as repro.out.
- E7: no local gate at this head by the user's waiver (Rebase-Q1 A: clean rebase, gate passed at be7034f). CI at 6641ff1: check on Linux, macOS, Windows and eval dry run pass; scenario (ubuntu) pending when judged.
- Description (gh pr view 178): clean, matches the 10-file diff; Known gaps present and matches the open scenario gap; Test plan names the pre-restack head for carried proofs; "Verified at 6641ff1" and "CI green at 6641ff1" are open for the caller.

Verdict: VERIFIED
