# CR-511 verification

Head: 5d2626debacb20ffa6a5599ff21ba3397d781ff0

Base: `266b784f008d6d9c6a5e7e1f9eabacefb0552dee` (origin/main). PR
https://github.com/gsemet/chantier/pull/489 (draft). Scope: orders O-179 and O-180
(`02-answers.md` 8 and 9). No quiz or eval run (owner's word).

Verdict: **NOT VERIFIED**. Claims 1 to 4 hold. Claim 5, the PR description, has two false
statements (5A, 5B). Both are fixed in the description alone; no code change is needed for them.

Short names, all at the full head above:

- `WT` = `C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-511`
- `CRF` = `C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/chantier/changes/4-batch/2-actives/511-sc25-cards-compare-review`
- `PY` = `uv run --no-sync --project C:/Users/gaeta/Projets/chantier python -I -B -X utf8`
- scripts in `CRF/work/verifier/`; before and after in `CRF/work/verifier/evidence/before-after.md`

Head and tree:

    git -C WT status --porcelain            -> (empty)
    gh pr view 489 --repo gsemet/chantier --json headRefOid --jq .headRefOid
    5d2626debacb20ffa6a5599ff21ba3397d781ff0
    git -C WT diff --shortstat 266b784 5d2626d
    26 files changed, 8059 insertions(+), 48 deletions(-)

## Claim 1. The serious lost rules are restored, with O-158 and O-176 (SHA 5d2626d): VERIFIED

Open rows (judgment by reading):

    PY vf_dump.py WT counts
    rows 4629 open tsv 329
    open rows 329 [('a', 62), ('b', 139), ('c', 1), ('d', 11), ('e', 112), ('f', 4)]
    PY vf_dump.py WT opena      (the 62 kind-a rows, read one by one)
    PY vf_dump.py WT openo      (the other 267, read in two halves)

None is clearly serious in the sense of O-180 (an irreversible or outward act without the user's
yes, a refusal or safety stop passed over, lost work, a batch unable to run). This is my reading of
the rows, not a mechanical proof; every open row stays listed in
`docs/proofs/cards-inventory-open.tsv`.

Serious rows the CR calls held or restored:

    PY vf_held.py WT CRF/work/r2-triage.md held 0 24       -> count 24
    PY vf_held.py WT CRF/work/r2-triage.md restored 0 31   -> count 31

All 55 head lines read: each holds its rule (held: `floor.md:5,7,12,14`,
`chief-of-staff.md:13,14,20`, `foreman.md:23`, `cr-driver.md:20,27`, `stack-driver.md:5`,
`release-driver.md:7,27`, `rails.py:313`). Pointers checked where a card line leans on a topic: the
shell exception for `gate` (`topics/session-shell-p1.md:6`, `cr-driver.md:23`), "never stop a
holder" at a sync (`sync-checkout.md`, Chief of Staff card, `foreman.md:23`), the allow rules
block (`hosts/claude-code.md:74-85`).

    PY vf_claims.py WT restored D-006,D-014,D-024,D-026,D-027,D-028,D-030,D-032,D-035,D-041,D-045,D-047,D-048,D-050,D-051,D-052,D-055,D-077,D-082,D-084,FM-494,FM-495,FM-507,FM-508,FM-541,FM-558,FM-584,H-425,P-001,P-011,P-016,P-017,P-018,W-052,W-062,X-004,X-005
    (37 lines "<id> <card> head: True base: False") count 37

O-158:

    git -C WT grep -n -E "130,000" 266b784 5d2626d -- skills/chantier/references/cr-driver.md skills/chantier/references/stack-driver.md skills/chantier/references/release-driver.md
    266b784:skills/chantier/references/stack-driver.md:11:- At 130,000 tokens on the `context:` line of `$CHANTIER stack`, send the context hand-back and end.
    5d2626d:skills/chantier/references/cr-driver.md:15:- At 130,000 tokens or more on that line (...)
    5d2626d:skills/chantier/references/release-driver.md:13:- At 130,000 tokens or more on the last `context:` line (...)
    5d2626d:skills/chantier/references/stack-driver.md:13:- At 130,000 tokens or more on the `context:` line of `$CHANTIER stack`, (...)

O-176:

    git -C WT grep -n -i -E "opening lines|skeleton|writes:. line|writes line" 266b784 5d2626d -- skills/chantier/references

Base: stale lines at `concepts.md:78,82,88,99,103,105`, `topics/cr-review-step.md:3`,
`topics/cr-workers.md:5`, `topics/direct-mode-p2.md:4`, `topics/direct-mode-switch-p4.md:3`,
`topics/qa-order.md:3`, `topics/trouble-worker.md:3`. Head: none of them. The remaining head
matches are unrelated or still true: `status-layout.md:14,21,64`, `hosts/claude-code.json:664`,
`hosts/copilot.json:654`, `topics.json:2416`, `topics/cr-review-step.md:15`,
`topics/host-auto-mode.md:10`, `topics/host-write-guard-shell.md:14`. `concepts.md:93` now says `brief:`, as
`driver_prompt.py:171` and `commands/facts.py:155` print it.

## Claim 2. The inventory test and the switched-lines test pass; a new unlisted open row fails (SHA 5d2626d): VERIFIED

    uv run --no-sync --project WT pytest WT/skills/chantier/scripts/cli/tests/test_cards_inventory.py WT/skills/chantier/scripts/cli/tests/test_card_names.py -q -p no:cacheprovider --rootdir WT -c WT/pyproject.toml --basetemp CRF/work/scratch/vf/pt
    .............................                                            [100%]
    29 passed in 1.21s

`test_cards_inventory.py`, read whole: `open_problems` reports a bad line, a duplicate, an open row
missing from the TSV (`unlisted: <id>`) and a listed row that is not open (`not open: <id>`);
`test_refusals` has the cases `unlisted` and `a-unlisted`, in the 29 passes. Base: the test file is
absent (`cat-file -e`, exit 128).

## Claim 3. CI is green at the head, scenario included (SHA 5d2626d): VERIFIED

    gh pr checks 489 --repo gsemet/chantier
    just check (macos-latest)          pass 6m13s  .../runs/45828591210/job/139939091007
    just check (ubuntu-latest)         pass 1m48s  .../job/139939091051
    just check (windows-latest)        pass 10m4s  .../job/139939091235
    just eval-dry-run (ubuntu-latest)  pass 1m12s  .../job/139939090612
    just scenario (ubuntu-latest)      pass 7m6s   .../job/139939090925

    gh run view --repo gsemet/chantier --job 139939090612 --log
    ... HEAD is now at 45257c2 Merge 5d2626debacb20ffa6a5599ff21ba3397d781ff0 into 266b784f008d6d9c6a5e7e1f9eabacefb0552dee
    ... 26 lines " ok <case>: ", among them:
    ... ok quiz-row-id: a case naming the row id C-001 loads; one naming X-9999 is refused with exit 2

## Claim 4. The long gate passed at the head on Windows (SHA 5d2626d): VERIFIED (cited, not rerun)

`CRF/work/gates/20261126-142332.log`:

    line 1:  gate CR-511 branch chantier/batch-31/cr-511-sc25-read-the-old-cards-against-the-new- head 5d2626debacb20ffa6a5599ff21ba3397d781ff0
    line 2:  $ just scenario  [scenario]
    line 35: result: pass at 5d2626debacb20ffa6a5599ff21ba3397d781ff0

    $CHANTIER handoff CR-511
    gates before handback ready, at the PR's head 5d2626debacb20ffa6a5599ff21ba3397d781ff0 (the full SHA; the gate log's first line names it):
      [x] long gate passed (gate CR-511 scenario; ...)
      [ ] verdict VERIFIED (the Verifier: ...)

The log's tail also warns of units over their time budget (`series-deps` 387.0 s > 380 s,
`surface-board` 822.4 s > 780 s); the result is a pass.

## Claim 5. The PR description as posted (SHA 5d2626d): NOT VERIFIED

    gh pr view 489 --repo gsemet/chantier --json headRefOid,isDraft,body

### 5A. "Card size targets exceeded by this change ... Already over and unchanged: ... griller ...": NOT VERIFIED

Posted (Known gaps): "cr-driver 3749 to 5066 (4000), stack-driver 3783 to 4821 (4000),
release-driver 3809 to 4685 (3000, already over), foreman 3997 to 4426 (4000), conflict-resolver
1494 to 1535 (1500). Already over and unchanged: coder, demo-explorer, retro-critic, spec-critic,
spec-writer, griller, verifier."

    git -C WT ls-tree -r -l 266b784 -- skills/chantier/references/cr-driver.md skills/chantier/references/stack-driver.md skills/chantier/references/release-driver.md skills/chantier/references/foreman.md skills/chantier/references/conflict-resolver.md skills/chantier/references/qa-driver.md skills/chantier/references/griller.md skills/chantier/references/griller-skill.md
    (and the same command at 5d2626d)
    griller.md 1925 / 1925; griller-skill.md 3621 / 3621

    CR-505 spec, 3-done/505-sc19-cards-workers/03-change-spec.md
    line 112: | `skills/chantier/cards-next/griller.md` | board-griller: only its `## Started from the board` section (section 2.3) | 2,000 for that section |
    lines 584-587: cr-driver 4 KB (4,096); stack-driver 4 KB (4,096); release-driver 3 KB (3,072); qa-driver 2 KB (2,048)
    3-done/507-sc21-cards-foreman/evidence/part3-proofs.md
    line 82: | griller-skill.md | none | 3,290 | 3,621 | 4,000 | within |
    line 83: | griller.md | 10,757 | 1,892 | 1,925 | 2,000 | within |
    3-done/510-sc24-cards-swap/work/pr-body.md line 101: the cards over target name no griller card

- No griller card is over its target: **griller is wrongly listed**. (The source is
  `work/coder/r2.md:101`, "griller.md 1925 (1500)".)
- The targets of cr-driver and stack-driver are 4,096, not 4000, and release-driver's is 3,072,
  not 3000. Those three are still over, so only the figures are wrong.
- The five before and after sizes are right. `foreman` (4,000) and `conflict-resolver` (1,500)
  targets are right.
- Also (not counted as its own failure): the specification's evidence 5 asks each card's size; the
  description gives no size for the unchanged ones.

### 5B. "Also restored without a row id: ...": NOT VERIFIED

Posted (Deliverables): "Also restored without a row id: a release with no PR yet is no anomaly
(stack driver card), the Foreman card's pointer to the session-shell topic, and "say it once to the
user as printed" (board restart topic)."

    git -C WT grep -n -E "^\| (X-004|C-640) \|" 5d2626d -- docs/proofs/cards-inventory.md
    :4723: | X-004 | stack driver | take stack | ... a release with no PR yet is no anomaly: ... | card stack-driver.md: "nor a release CR with no PR yet" | quote |
    :1905: | C-640 | chief-of-staff | ... say it once to the user as printed, with the offer of the restart. | ... | topic board-restart | quote |
    CRF/work/r2-triage.md:460: | X-004 | yes | restored at skills/chantier/references/stack-driver.md:10 | ...
    inventory line 7141 (sc24-3): "the release with no PR yet (X-004, stack-driver.md), ..."

The first item **has** a row id: X-004, listed in the restored table directly above the sentence.
The third is the rule of inventory row C-640 (home: the same topic). "Without a row id" is false.
The restorations themselves are present (`stack-driver.md:10`, `foreman.md:39`,
`topics/board-restart.md:3`).

### Checked and holding

| statement | proof at 5d2626d | judgment |
|---|---|---|
| renders: sections in the template's order, one fold with blank lines, no image | posted body read | VERIFIED |
| no internal reference or chantier role as doer outside Internal references (role names are product terms of the changed cards) | posted body read, pr-template "The rules" | VERIFIED |
| 1,474,636 bytes; 4629 rows; 78 sources, 11,391 lines, 900,129 bytes | `vf_claims.py WT sources`: "source files matched 78 lines 11391 bytes 900129 mismatches 0"; blob 1474636 | VERIFIED |
| kinds a601 b169 c139 d165 e3493 f62; owner lists 601, 12, 2, 601 | `vf_dump.py WT counts`; `vf_claims.py WT sections`; `test_owner_lists` | VERIFIED |
| the test: homes and checks resolve, every old line covered, kind a only floor, role card, refusal, or open | claim 2; `test_coverage`, `kind_a_homed` read | VERIFIED |
| quiz cases may cite a row id | `evals/kit/quiz.py` diff; CI case `quiz-row-id` | VERIFIED |
| `git diff --stat f08cf41 ea11a9e` prints nothing; old base f08cf41 | `git -C WT diff --stat f08cf41f ea11a9e0 -- skills/chantier/references "skills/*/SKILL.md"` -> empty | VERIFIED |
| context hand-back, no end of turn to wait, no large output whole; stale prompt text corrected | claim 1; `cr-driver.md:15-16`, `stack-driver.md:13-14`, `release-driver.md:13` | VERIFIED |
| the table of 37 restored rows | claim 1, `restored` run | VERIFIED |
| Changes list matches the 26 files (7 cards or concepts, 11 topics, 2 proof files, 3 tests, 3 eval files) | `git -C WT diff --stat 266b784 5d2626d` | VERIFIED |
| Blast radius one grade; Impacts "No visual change" (no UI file in the diff) | same diff | VERIFIED |
| ids with B or four digits, 1469 refused by the planned pattern | `vf_claims.py WT kinds` | VERIFIED |
| no row's kind changed | `vf_seed.py WT 3-done`: "common 4616 kind differs 0", 13 X rows new, none lost | VERIFIED |
| two test files for the 400-line limit | 255 + 238 lines; `CONTRIBUTING.md:368` | VERIFIED |
| plan announces five sections, lists six | spec lines 70-134; six `## ` headings | VERIFIED |
| ceilings raised | `test_brief_bytes.py` diff | VERIFIED |
| 329 open = 62 a, 139 inferable, 128 others; 539 kind a homed by quote only; 12 incidents ids; none homed inferable; 129 rare | `vf_claims.py WT kinds` | VERIFIED |
| 62 read one by one, 267 judged from wording; about one in ten; 2.8 s | the authors' records `work/coder/r2.md:24-25`, `work/r1.md:65-66`, `work/r1.md:36` | disclosure, matches the record |
| H-173 and H-217 resolve only in docstrings | grep of both spans: `commands/joining.py:130`, `commands/orders_after.py:70`, docstrings | VERIFIED |
| stack card names the direct-mode host means (also before), answers one of two tags | `stack-driver.md:11,13`; base `:23`; `topics/stack-run.md:3` | VERIFIED |
| 20 of 36 checklist items are known gaps, J11/J22, CONTRIBUTING, no new quiz case | `vf_claims.py WT checklist` (16 done, 20 known gap) | VERIFIED |
| H-1360 needs the owner | inventory line 4296 | VERIFIED |
| skipped quiz commands as written; no real run | spec lines 211-219; `02-answers.md` 5 | VERIFIED |
| the weak homes listed as reported by review, rare trigger set from the home, mixed role spellings | not judged row by row (disclosed gaps) | not checked |
| Human decisions | `02-answers.md` 5-9 | VERIFIED; note: "does not block" and "never blocking" are recorded there as the Chief of Staff's reading, to confirm |
| new tests pass; absent before | claim 2 | VERIFIED |
| `just check` and `just eval-dry-run` pass at 5d2626d | CI jobs at the head (claim 3). The local counts (2789 passed, 19 skipped) come from the Driver's note, not rerun, on my brief's order | VERIFIED |
| Evidence: no visual change | diff holds no UI file | VERIFIED |
| Review approved at 5d2626d, carried from 7263861 | `$CHANTIER log CR-511`: "r3 approved at 4380df52..., committed as 7263861..."; "move 7263861..5d2626d ... pass carried"; `range-diff` -> "1: 7263861f = 1: 5d2626de" | VERIFIED |
| "Verified at the head: UNVERIFIED" and its Known gaps bullet | true when judged; to update after the next pass | VERIFIED |
| CI green; long gate on Windows passes | claims 3 and 4 | VERIFIED |

The line after `</details>` ("Generated with Claude Code") is the attribution line the host
requires. `pr-template.md` says nothing follows `</details>`; it renders, it claims no change, and
it is not counted as a failure.
