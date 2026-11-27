# CR-515 verification

Head: 22ccbe0b1679de7e56bfb5795b2d2c3681c2acb6

Base: fbdb53d2a2860a95257235dc7f592ab0e75ce45e (origin/main). Worktree clean (`git status --porcelain | wc -l` prints 0).
Commands ran from Bash (NO_COLOR unset there), from `<worktree>` unless said. `C` is the CLI package
`skills/chantier/scripts/cli/src/chantier`. Evidence files are in `work/verifier/evidence/`; the scripts there
are copies with machine paths replaced by placeholders. Every claim was judged at 22ccbe0.

## 1. The removed names and files are gone: PASS (22ccbe0)

`git grep -nE "cards-inventory|cards_inventory|inventory_rows|quiz-row-id"` at the head prints nothing:

```
exit=1
```

`git grep -lE "<same>" fbdb53d2` lists six files: `docs/proofs/cards-inventory.md`, `evals/README.md`,
`evals/kit/dry_run.py`, `evals/kit/quiz.py`, `.../tests/cards_inventory.py`, `.../tests/test_cards_inventory.py`
(12 `cards-inventory`, 3 `cards_inventory`, 3 `inventory_rows`, 4 `quiz-row-id`).

`git cat-file -e <rev>:<file>` prints base yes, head no for `docs/proofs/cards-inventory.md`,
`docs/proofs/cards-inventory-open.tsv`, `tests/cards_inventory.py`, `tests/test_cards_inventory.py`.
`git diff --shortstat fbdb53d2 HEAD`: 9 files changed, 269 insertions(+), 8036 deletions(-).
Evidence: `claim1-4-tree.txt`.

## 2. The last reading of the open rows: PASS (22ccbe0)

`python count.py` (open rows from the base TSV against the PR body's lines):

```
rows 329 unique 329 {'a': 62, 'b': 139, 'c': 1, 'd': 11, 'e': 112, 'f': 4}
pr lines 112 unique 112
not open: []
per kind {'a': 52, 'b': 15, 'c': 1, 'd': 2, 'e': 42}
```

These are the PR's counts. `python rowspans.py` (every line's quoted span in the file it names, at the head):
`checked 112`, no miss. Evidence: `claim2-counts-spans.txt`.

Meaning, by reading: `python sample.py <scratch> <work> 42` printed 24 rows of all listed kinds with the base
inventory line and the text around the home at the head (`claim2-sample-24.txt`): H-897, D-036, D-018, P-007,
D-080, D-068, FM-B047, FM-486, W-025, FM-436, H-1429, H-1071, H-449, H-1181, C-472, C-011, C-027, C-1312,
C-1442, H-313, W-323, H-331, C-1244, H-1002. All 24: the home holds the rule.

Unlisted rows: `python unlisted.py` prints the 217 others (`217 27481`); they were searched by keyword and
these read closely (`claim2-unlisted-examined.txt`): H-854, D-039, D-010, D-078, C-098, H-433, H-459, H-1549,
H-1547, H-1187, H-1215. Judged: none is a protective rule held nowhere (git listing economy, a recording
step, prose and host observations; H-854's risk, a review step writing, is held by `review-step.md`
"Never write a file, commit, push, rebase, merge, `git stash`"). This part is a sample and a judgment, not a
reading of all 217.

## 3. docs/protective-rules.md: PASS (22ccbe0)

`python listcheck.py` (`claim3-listcheck.txt`; abridged here):

```
rows 111 {'`held`': 99, '`to add`': 12} cells!=4 []
dup ids []
P 19 max 19 missing []   A 25 max 25 missing []   B 22 max 22 missing []
C 24 max 24 missing []   D 25 max 25 missing []   N 10 max 10 missing []
spans checked 264
MISS P7/C16/D21 (floor 7), B19 (skills/griller/SKILL.md), P11 (chief-of-staff.md)
```

The script reports three misses; each is its own parsing (it joins two spans, or reads the wrong file), shown
by hand (`claim3-to-add-code.txt`): "is not a CR in the configured inbox" is at `C/lifecycle/stages.py:150`;
each B19 span is found in the file named (both SKILL.md and host rows); "Asks first" and the P10 allow rules
are at `chief-of-staff.md:12-13` and `AGENTS.md:42`. Refusal spans resolve in the code
(`REFUSAL` lines of `claim3-listcheck.txt`). So no `held` span is missing.

Every line has a state. The plan section 5 table and verdicts section D ids P1-P19, A1-A25, B1-B22, C1-C24,
D1-D25, N1-N10 are all present (above). The owner's wording: P11 is `to add` (plan step 20, card-cleanup-Q3,
today's text quoted from `chief-of-staff.md` and `AGENTS.md`); P2-code is `to add` (plan step 15,
card-cleanup-Q2). The twelve `to add` lines each name a plan step or "no step". No removed file is named
(claim 1's grep).

`to add` lines are rules no code holds (outputs in `claim3-to-add-code.txt`):

| line | command | result |
|---|---|---|
| P2-code, P11 | `git grep -n -e add.rules -e add_rules -- C` | exit=1, no such command; `push.py` only points to `help refused-push` |
| P3-code | `git grep -nE "stash\|reset --hard\|add -A" -- hooks` | exit=1 |
| P12-code | `git grep -niE "pattern check\|secret.*pattern\|...\|redact" -- C` | exit=1 |
| P13-restart | `git grep -nE 'restart = \|"restart": True' -- C/commands/driver.py` | only a flag `take` logs (lines 150, 165) |
| P13-seat | `sed -n 24,63p C/commands/seat.py` | `foreman set` checks the epoch only |
| A23-code | `sed -n 347,376p C/commands/delivery.py` | `_check_out_of_draft` has no local gate check |
| A24-code | `sed -n 32,47p C/commands/gate.py` | `_gate_stop` runs before any lease check |
| D16-code | `git grep -n "the seat is held by" -- C` | only `seat.py:120` and `:149` (leave, take) |
| D20-code | `sed -n 160,179p C/lifecycle/stages.py` | checks the file exists, not that it is final |
| P15-code | `sed -n 64,103p C/commands/judge.py` | refuses status, epoch, no ask; nothing on a claimed waiver |

P14-code probed at run time on a throwaway project in an export of the head
(`pytest -c pytest.ini -s -q test_zz_probe.py`, `claim3-probe-P14.txt`, 1 passed; abridged here):

```
PROBE ship second link, working: exit 0: 'recorded .../pull/8 ...'; status=working
PROBE order merged: exit 0: 'merged CR-101: moved to 3-done'
PROBE push on merged CR: exit 0: 'pushed chantier/batch-01/cr-101-cr-a at e2cb588 (was ccc4f14)'; status=merged
PROBE ship on merged CR, third link: exit 0: 'recorded .../pull/9 ...'; status=merged
PROBE remote tip == worktree head: True
```

Note, not a failure: line P15/C8 ("... recorded with the user's own words and a follow-up CR filed first ...",
`held`) is broader than the stack form. `C/commands/orders_waive.py` `waive_stack` refuses `--follow-up`
("order waive stack: the top's gate validates, no --follow-up") and records the waiver with none
(`topics/long-gate-waiver.md` has both forms; section D C8 marked the stack form not verified). The protective
part (the user's words, never in a brief) is held.

## 4. No file under skills/chantier/references changed: PASS (22ccbe0)

`git diff --quiet fbdb53d2 HEAD -- skills/chantier/references`: `exit=0`. Evidence: `claim1-4-tree.txt`.

## 5. test_card_homes.py: PASS (22ccbe0)

`python homes3.py` (specification section 3's rule applied to the base's HOMES against the list, and the PR
body's per-key list), `claim5-homes-rule.txt` (abridged here):

```
base 18 210 head 16 127
mismatches against the rule: []
homes added: []
removed keys: {'test_triage_moves': ['topic session-shell'], 'test_board_running_lane': ['topic where-cr-goes']}
floor with no line: test_cli_stop floor 4 / test_launch_modes floor 4, "a floor line, every one stays"
keys in PR list 16 missing set() errors 0
```

210 homes, 127 kept, 83 dropped, the removed keys and each key's counts, names and ids match the PR.

AST compare of the top-level definitions, base against head (`claim5-test-functions.txt`): `_gone`,
`_file_gone`, `test_a_home_that_is_gone_is_named`, `test_every_rule_pinned_in_a_removed_card_has_its_home`,
`REFS` unchanged; `FLOOR`, `HOMES` changed (FLOOR gains lines 2 and 8, so all ten);
`test_the_floor_reads_word_for_word` added.

Floor test on an export of the head under work/scratch, never the worktree (`claim5-floor-test.txt`; summarised here):

```
unmodified: 18 passed
floor line 1..10 altered, one at a time (-k word_for_word): 1 failed, 17 deselected (each of the ten)
eleventh line added: 1 failed, 17 deselected
line 2 removed, whole file: only test_the_floor_reads_word_for_word fails (1 failed, 17 passed)
restored: 18 passed
```

Note, not a failure: under a looser reading (a topic counts as named when any of its readings in
`topics.json` is named) eight dropped homes would stay (`claim5-loose-reading.txt`). Each named page there
belongs to a narrower topic, and the PR states its rule under Autonomous decisions.

## 6. Eval kit: PASS (22ccbe0)

`uv run --no-sync --project <worktree> python evals/kit/quiz.py cr-driver --plan --cases-dir <scratch>/q/<d>`,
one prepared case each (`claim6-eval-kit.txt`; summarised here):

```
J1, floor-10, R-001: exit=0
X-9999: exit=2  ...q\x\cr-driver\row.json: key rules: 'X-9999' is no floor rule, no J row of evals/SCORECARD.md and no R-nnn id
H-897, D-036, FM-B047 (inventory row ids): exit=2, same message, naming file and key
```

`python evals/kit/dry_run.py --case quiz-cases`: `ok ... the 59 shipped cases load and their rules resolve ...
five prepared broken cases are refused with exit 2`; `--case quiz-rule-id`: `ok ... a case naming the J row J1
loads; one naming X-9999 is refused with exit 2`; each `dry run: 1 of 1 cases as expected`, exit 0.
`git diff fbdb53d2 HEAD -- evals/README.md`: "Cases" no longer lists the inventory row id.

## 7. just check and the pipeline: PASS (22ccbe0)

`gh pr checks 491` (`claim7-ci.txt`): `just check` macos, ubuntu, windows pass; `just eval-dry-run` ubuntu
pass; `just scenario` ubuntu pass. `gh run view 46017348690 --json headSha,conclusion`:
`success`, headSha 22ccbe0b1679de7e56bfb5795b2d2c3681c2acb6. Log: macos and ubuntu `2781 passed, 23 skipped`,
windows `2785 passed, 19 skipped`, `dry run: 26 of 26 cases as expected`. PR: base main, head 22ccbe0, draft,
open. I did not run `just check` myself: CI at the head covers the claim. The long gate is waived
(`handoff CR-515`: `gate: waived (O-15, stack): run no long gate; validated by CR-523`).

## 8. The posted PR body against the diff: PASS (22ccbe0)

`gh pr view 491 --json body --jq .body | diff - work/pr-body.md`: one difference, a trailing empty line
(`claim8-body.txt`). Its claims against the diff and the checks above:

- figures: 111 lines, 99 held, 0 restored, 12 to add; 4 files removed; homes 210 in 18 keys to 127 in 16;
  floor pinned from 8 lines as homes to 10 (claims 1, 3, 5);
- approval carry: `git range-diff 5d7549e~1..5d7549e 22ccbe0~1..22ccbe0` shows `=`, both patch-ids
  `d8fd174a45571e4314af81f844fcf40da487fe8e`; 5d7549e's parent is 4d12a5b, 22ccbe0's is fbdb53d;
- local eval dry run `26 of 26` (the Driver's log) and the CI counts as above;
- "19 more protective": the first judging counted 93 (a 47, b 11, c 1, d 2, e 32,
  `work/investigator/investigation-rows.md`) against 112;
- no inventory row id in the list (`grep -cE` prints 0); no test reads the list (`git grep -n
  protective-rules -- skills/chantier/scripts evals tests` finds only the docstring of `test_card_homes.py`);
- N5 is row H-855; the B6 note is in the list;
- Known gaps: N1, N7 and C4 are the held lines whose homes are all on pages the 516 and 517 specifications
  delete; the B18 line-wrap gap is as described.

VERIFIED
