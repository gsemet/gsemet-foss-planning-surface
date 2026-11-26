# CR-507 before and after (Verifier)

- Before: base `24111e6d9920a7ff3e8f210613186dd65d802ec8`.
- After: head `88d9ab40d706ce2442821ad77385812af35ba846`.
- No screenshot or video: the CR has no visual change and no UI.
- Raw logs stay in `work/verifier/*.log`; the scripts, with local paths replaced by placeholders, in `work/verifier/scripts/`.
- The move since the previous verification (`03f973e..88d9ab4`) changes `cards-next/` only, so pairs 1 and 2 were read again; pairs 3 and 4 are carried or cited, as each says.

## Pair 1: files and card bytes

Shows what the CR adds under `cards-next/` and the size of each main card.

Reproduce in `<worktree>`: `git ls-tree -r -l <rev> skills/chantier/cards-next` and `git ls-tree -r --name-only <rev> evals/quiz/chief-of-staff`, with `<rev>` the base, then `HEAD`.

| Reading (bytes) | Before (`24111e6d`) | After (`88d9ab4`) |
| --- | ---: | ---: |
| files under `cards-next/` | 71 | 334 |
| files under `evals/quiz/chief-of-staff/` | 8 | 17 |
| `foreman.md` | absent | 3997 |
| `chief-of-staff.md` | absent | 5999 |
| `griller-skill.md` | absent | 3621 |
| `griller.md` | 1758 | 1925 |
| `concepts.md` | absent | 26100 |
| `pr-template.md` | absent | 12032 |
| `review-step.md` | absent | 1497 |
| `cr-driver.md` | 3280 | 3749 |
| `stack-driver.md` | 3321 | 3783 |
| `release-driver.md` | 3277 | 3809 |
| `qa-driver.md` | 1337 | 1567 |
| `floor.md` | 554 | 554 |

`git diff --shortstat 24111e6d..HEAD`: `295 files changed, 6405 insertions(+), 42 deletions(-)`. No path outside `skills/chantier/cards-next/` and `evals/quiz/`.

## Pair 2: brief bytes, today's cards against `--cards skills/chantier/cards-next`

Both readings run at `88d9ab4` (the CR changes no file today's cards are read from). Reproduce: `chantier brief <role> [unit] --batch batch-31`, then the same with `--cards <worktree>/skills/chantier/cards-next`; the bytes are those of the text the run writes, line ends LF (`scripts/briefs2.py` runs the command in process and captures the write, so no brief file is written).

| Role (unit) | Today | New |
| --- | ---: | ---: |
| coder (CR-507) | 9179 | 6173 |
| conflict-resolver (CR-507) | 8463 | 6064 |
| debugger (CR-507) | 8252 | 5851 |
| inspector (CR-507) | 10614 | 6570 |
| investigator (CR-507) | 8124 | 6056 |
| verifier (CR-507) | 19151 | 7682 |
| spec-writer (inbox item `simplify-cards-and-prompts`) | 4815 | 3228 |
| spec-critic (same item) | 5290 | 3133 |
| board-griller (same item) | 11964 | 3132 |
| retro-critic | 4225 | 2889 |
| demo-explorer | 4746 | 2936 |
| chief-of-staff | 22322 | 24657 |
| griller | 6349 | 6747 |
| foreman | 55206 | 22276 |
| direct mode: chief-of-staff, then `foreman --epoch 1` | 77528 | 46933 |
| cr-driver, release-driver, stack-driver, qa-driver | refused today too for these units (not CR-507's live lease or no such order) | exit 2: `cards-next/driver.md` missing |
| the four Drivers, role only; new: a staged copy of the role card as `driver.md` | 59216 | 8010, 8070, 8044, 5828 |

## Pair 3: `just test`

Before: carried from `03f973e` (same base, same machine, `just test`). After: the pytest line of `just check` at `88d9ab4` (`work/verifier/just-check-88d9ab4.log`), which runs the same suite.

| | Before | After |
| --- | --- | --- |
| result | 2932 passed, 20 skipped | 2933 passed, 19 skipped |
| pytest time | 192.40 s | 134.96 s |

No test is added or changed. The two runs differ in invocation and in machine load: this shows the head is not slower, and claims no speed-up. Why one test ran at `88d9ab4` that was skipped before was not traced.

## Pair 4: `griller.md`

Carried from `03f973e`: `git diff --quiet 03f973e..HEAD -- skills/chantier/cards-next/griller.md` exits 0. Reproduce: `git diff 24111e6d..HEAD -- skills/chantier/cards-next/griller.md`. Two lines change: the run-limits paragraph gains "never a secret or personal data", and the "How you grill..." sentence is added to the grill paragraph. 1758 to 1925 bytes.

## Not captured

- No model run: no `just quiz` score and no real run, before or after (no spend, by the Driver's evidence plan).
- No old start reading (the 91 KB declared, 144 KB measured and 218 KB / 36 KB figures of the specification) was measured again.
