# CR-507 before and after (Verifier)

- Before: base `24111e6d9920a7ff3e8f210613186dd65d802ec8` (a detached worktree of the base, removed after the capture).
- After: head `03f973e4f0d0756c9b5fa77ed0f888f941745dbe`.
- No screenshot or video: the CR has no visual change and no UI.
- Raw logs stay in `work/verifier/*.log`; the scripts, with local paths replaced by placeholders, in `work/verifier/scripts/`.

## Pair 1: files and card bytes

Shows what the CR adds under `cards-next/` and the size of each main card.

Reproduce in each worktree: `git ls-tree -r -l HEAD skills/chantier/cards-next evals/quiz/chief-of-staff` (`scripts/pairs.py`).

| Reading (bytes) | Before | After |
| --- | ---: | ---: |
| files under `cards-next/` | 71 | 306 |
| files under `evals/quiz/chief-of-staff/` | 8 | 17 |
| `foreman.md` | absent | 3998 |
| `chief-of-staff.md` | absent | 5994 |
| `griller-skill.md` | absent | 3497 |
| `griller.md` | 1758 | 1925 |
| `concepts.md` | absent | 18565 |
| `pr-template.md` | absent | 11849 |
| `review-step.md` | absent | 1385 |
| `cr-driver.md` | 3280 | 3749 |
| `stack-driver.md` | 3321 | 3783 |
| `release-driver.md` | 3277 | 3811 |
| `qa-driver.md` | 1337 | 1567 |
| `floor.md` | 554 | 554 |

`git diff --stat 24111e6d..HEAD`, last line: `263 files changed, 6080 insertions(+), 27 deletions(-)`; by status 244 added, 19 modified.

## Pair 2: brief bytes, today's cards against `--cards skills/chantier/cards-next`

Both readings run at the head (the CR changes no file today's cards are read from). Reproduce: `chantier brief <role> [unit] --batch batch-31`, then the same with `--cards <worktree>/skills/chantier/cards-next`, and the size of the file the command names (`scripts/briefs.py`).

| Role (unit) | Today | New |
| --- | ---: | ---: |
| coder (CR-507) | 9048 | 5972 |
| conflict-resolver (CR-507) | 8332 | 5933 |
| debugger (CR-507) | 8121 | 5720 |
| inspector (CR-507) | 10483 | 6439 |
| investigator (CR-507) | 7993 | 5925 |
| verifier (CR-507) | 19020 | 7551 |
| spec-writer (inbox item `driver-context-second-cut`) | 4668 | 3081 |
| spec-critic (same item) | 5143 | 2986 |
| board-griller (same item) | 11817 | 2985 |
| retro-critic | 4225 | 2889 |
| demo-explorer | 4746 | 2936 |
| chief-of-staff | 22322 | 24652 |
| griller | 6349 | 6623 |
| foreman | 55206 | 22277 |
| cr-driver, release-driver, stack-driver, qa-driver | 59216 (role only, no unit) | exit 2: `cards-next/driver.md` missing |
| the four Drivers, staged copy of the new role card as `driver.md` | 59216 | 8010, 8072, 8044, 5828 |

## Pair 3: `just test`

Same machine, one run after the other. Reproduce: `just test` in each worktree.

| | Before | After |
| --- | --- | --- |
| result | 2932 passed, 20 skipped | 2932 passed, 20 skipped |
| pytest time | 192.40 s | 171.16 s |
| wall time | 197.9 s | 172.6 s |

No test is added or changed. The head is not slower; the difference is run-to-run variation, not a claim of a speed-up.

## Pair 4: `griller.md`

Reproduce: `git diff 24111e6d..HEAD -- skills/chantier/cards-next/griller.md`. Two lines change: the run-limits paragraph gains "never a secret or personal data", and the "How you grill..." sentence is added to the grill paragraph. 1758 to 1925 bytes.

## Not captured

- No model run: no `just quiz` score and no real run, before or after (no spend, by the Driver's evidence plan).
- No old-start reading (the 91 KB declared, 144 KB measured and 218 KB / 36 KB figures of the specification) was measured again.
