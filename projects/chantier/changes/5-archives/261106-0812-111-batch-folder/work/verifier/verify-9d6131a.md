# Verify CR-111, head 9d6131a

NOT VERIFIED

Every claim I could run holds (table below). One specified claim is unmet: the host proof of the Foreman reuse was not done. Nothing else failed.

Method: the worktree's own chantier.py against temporary repositories (a bare remote and a clone each), never this project's .agents/changes/. Commands and trimmed output in evidence/proof.txt; the two PowerShell scripts that produced them sit beside it.

## Claim by claim

| Claim | Result | Proof |
|---|---|---|
| id `batch-<nn>`, folder `3-requests/batch-<nn>/`, CR folder `<number>-<slug>` | proved | batch-01, 101-alpha-one |
| branch `chantier/batch-<n>/<cr>-<slug>`, worktree `<repo>.worktrees/batch-<n>-<cr>` | proved | chantier/batch-01/cr-101-alpha-one, repo.worktrees/batch-01-CR-101 |
| numbering continues from `.batch-number`; after 04 comes batch-05 | proved with `.batch-number` = 4 and an old `04-old` in 4-archives: batch-05. Counter kept after `close` (batch-02 after batch-01 closed) | evidence |
| `open` takes no name | proved; `open <folders>` only |
| `--batch`/`$CHANTIER_BATCH` take `4` or `batch-04` | proved (1, batch-01, env 1, env batch-01; a wrong number names the unknown batch, exit 2) |
| second `open` refused, exit 2, names the batch, also while landed, until `close` | proved: open then landed state; after `close --yes` the next `open` works |
| `order add` joins the open batch | proved: CR-103 in batch-01, on top of the stack, no new batch |
| slots default 4 | proved ("4 slots", batch.json slots 4, cli.py default=4); `--slots 2` still honoured |
| `--stack` gone, `--parallel` there | proved: unrecognized argument; mode parallel on `--parallel` |
| stack merged in part | proved: bottom merged alone, archived at once, batch stays open; `take stack` shows the remaining CRs, first on origin/main, the next on the first's branch; land refused until all done |
| old folder in 4-archives, old CR record readable | proved for a folder in 4-archives (listed under landed in STATUS.json/status) and for a legacy `04-old` batch.json (status --batch 04-old reads it) |
| STATUS.json fields kept, `batch`/`folder` = `batch-<n>` | proved: field lists above, batch=batch-05, folder=batch-05 |
| spec's grep `<NN>-<batch>` in skills, docs, README.md | proved: no match |

## Observations (not failures)

1. A legacy landed batch folder still in `3-requests/` (form `04-old`) is read by `--batch 04-old` but not by `--batch 4` (unknown batch-04), and it blocks `open` as a landed batch until closed, naming `04-old`. The spec only promises readability for 4-archives and old CR records, and says to run the CR with no batch open, so this is outside scope. `close` also refuses it while its CR folder still holds files, as before.
2. `chief-of-staff.md` (step 4) has two lines wrapped irregularly after the edit (a long "The Foreman claims its epoch itself. When the host refuses to start" line); cosmetic.

## Not proved (needs the host)

The Foreman reuse: that the epoch claim works in a reused session, and whether a message wakes a stopped one. The card checked: `chief-of-staff.md` step 4 says "Not proved on the host ... do not tell the user either as a fact", states the `/compact` recommendation, the reuse as optional and the new session as default; `foreman.md` says a new prompt starts from the state alone. It claims nothing beyond what was proved. Listed as not proved, not as failure.

## Host proof of the Foreman reuse (judged as a claim)

The spec says: prove on the host that the epoch claim works in a reused session, and whether a message wakes a stopped one; the card says what was proved, and only that.
- Attempted: nothing on the host. My tools (shell, file read and write) cannot start, stop or message a Claude Code session, so I did not try. I only read the cards.
- Done: the card half holds. `chief-of-staff.md` step 4 says the two points are not proved and tells the Chief of Staff not to state either as fact.
- Not done: the proof itself. The spec asks for it, so I count it as unmet, not as a failure of the code. It needs an agent with host session tools.

## The old-form `--batch` fact

`--batch batch-folder`, `--batch 5` and no `--batch` fail on this batch, and only `--batch 05-batch-folder` reads, because this batch was opened by the old CLI in the old form. I do not count it against the CR: the spec says to run it with no batch open and promises no migration. It is not a defect of the new CLI. It matches my observation 1 above.