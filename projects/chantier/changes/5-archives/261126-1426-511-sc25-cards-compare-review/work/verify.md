# CR-511 verification

Head: 5d2626debacb20ffa6a5599ff21ba3397d781ff0

Base: `266b784f008d6d9c6a5e7e1f9eabacefb0552dee` (origin/main). PR
https://github.com/gsemet/chantier/pull/489 (draft). Scope: orders O-179 and O-180
(`02-answers.md` 8 and 9). No quiz or eval run (owner's word).

Verdict: **VERIFIED**. Claims 1 to 4 are carried from the first pass at this same head (no move,
so nothing they exercise changed). Claim 5, the PR description, was judged again on the body as
edited and posted again: the two statements that failed (5A, card size targets; 5B, "restored
without a row id") are fixed.

Short names, all at the full head above:

- `WT` = `C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-511`
- `CRF` = `C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/chantier/changes/4-batch/2-actives/511-sc25-cards-compare-review`
- `PY` = `uv run --no-sync --project C:/Users/gaeta/Projets/chantier python -I -B -X utf8`
- scripts in `CRF/work/verifier/`; before and after in `CRF/work/verifier/evidence/before-after.md`

Head and tree (run again in the description pass):

    git -C WT status --porcelain            -> (empty)
    git -C WT rev-parse HEAD                -> 5d2626debacb20ffa6a5599ff21ba3397d781ff0
    gh pr view 489 --repo gsemet/chantier --json headRefOid,isDraft,body
    "headRefOid":"5d2626debacb20ffa6a5599ff21ba3397d781ff0","isDraft":true
    git -C WT diff --stat 266b784 5d2626d
    26 files changed, 8059 insertions(+), 48 deletions(-)

## Claim 1. The serious lost rules are restored, with O-158 and O-176 (SHA 5d2626d): VERIFIED

Carried: judged at this head in the first pass.

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

Carried: judged at this head in the first pass.

    uv run --no-sync --project WT pytest WT/skills/chantier/scripts/cli/tests/test_cards_inventory.py WT/skills/chantier/scripts/cli/tests/test_card_names.py -q -p no:cacheprovider --rootdir WT -c WT/pyproject.toml --basetemp CRF/work/scratch/vf/pt
    .............................                                            [100%]
    29 passed in 1.21s

`test_cards_inventory.py`, read whole: `open_problems` reports a bad line, a duplicate, an open row
missing from the TSV (`unlisted: <id>`) and a listed row that is not open (`not open: <id>`);
`test_refusals` has the cases `unlisted` and `a-unlisted`, in the 29 passes. Base: the test file is
absent (`cat-file -e`, exit 128).

## Claim 3. CI is green at the head, scenario included (SHA 5d2626d): VERIFIED

Run again in the description pass:

    gh pr checks 489 --repo gsemet/chantier
    just check (macos-latest)          pass 6m13s  .../runs/45828591210/job/139939091007
    just check (ubuntu-latest)         pass 1m48s  .../job/139939091051
    just check (windows-latest)        pass 10m4s  .../job/139939091235
    just eval-dry-run (ubuntu-latest)  pass 1m12s  .../job/139939090612
    just scenario (ubuntu-latest)      pass 7m6s   .../job/139939090925

From the first pass:

    gh run view --repo gsemet/chantier --job 139939090612 --log
    ... HEAD is now at 45257c2 Merge 5d2626debacb20ffa6a5599ff21ba3397d781ff0 into 266b784f008d6d9c6a5e7e1f9eabacefb0552dee
    ... 26 lines " ok <case>: ", among them:
    ... ok quiz-row-id: a case naming the row id C-001 loads; one naming X-9999 is refused with exit 2

## Claim 4. The long gate passed at the head on Windows (SHA 5d2626d): VERIFIED (cited, not rerun)

`CRF/work/gates/20261126-142332.log`:

    line 1:  gate CR-511 branch chantier/batch-31/cr-511-sc25-read-the-old-cards-against-the-new- head 5d2626debacb20ffa6a5599ff21ba3397d781ff0
    line 2:  $ just scenario  [scenario]
    line 35: result: pass at 5d2626debacb20ffa6a5599ff21ba3397d781ff0

    $CHANTIER handoff CR-511      (first pass)
    gates before handback ready, at the PR's head 5d2626debacb20ffa6a5599ff21ba3397d781ff0 (the full SHA; the gate log's first line names it):
      [x] long gate passed (gate CR-511 scenario; ...)

The log's tail also warns of units over their time budget (`parallel` 407.5 s > 380 s, `stack`
898.1 s > 750 s, `series-deps` 387.0 s > 380 s, `surface-board` 822.4 s > 780 s); the result is a
pass.

## Claim 5. The PR description as posted (SHA 5d2626d): VERIFIED

    gh pr view 489 --repo gsemet/chantier --json headRefOid,isDraft,body
    PY vf_desc.py WT body CRF/work/pr-body.md
    posted == pr-body.md: True 8753 8753
    gh api repos/gsemet/chantier/pulls/489 -H "Accept: application/vnd.github.html+json" --jq .body_html
    h2 Summary, h2 Deliverables (one table, 37 rows), h2 Blast radius, h2 Autonomous decisions,
    h2 Known gaps, <details><summary>Details</summary> holding h2 Changes, h2 Human decisions,
    h2 Impacts, h2 Test plan (7 ticked task items), h2 Internal references, </details>, then the
    attribution line. No <img>.

### 5A (failed before, judged again): card size targets: VERIFIED

    PY vf_desc.py WT cards
    chief-of-staff.md base 5999 head 5999 target 6000 within unchanged
    griller-skill.md base 3621 head 3621 target 4000 within unchanged
    foreman.md base 3997 head 4426 target 4000 over changed
    cr-driver.md base 3749 head 5066 target 4096 over changed
    stack-driver.md base 3783 head 4821 target 4096 over changed
    release-driver.md base 3809 head 4685 target 3072 over changed
    qa-driver.md base 1567 head 1755 target 2048 within changed
    coder.md base 1603 head 1603 target 1500 over unchanged
    conflict-resolver.md base 1494 head 1535 target 1500 over changed
    debugger.md base 1281 head 1281 target 1500 within unchanged
    investigator.md base 1486 head 1486 target 1500 within unchanged
    demo-explorer.md base 1612 head 1612 target 1500 over unchanged
    spec-writer.md base 1667 head 1667 target 1500 over unchanged
    spec-critic.md base 1572 head 1572 target 1500 over unchanged
    retro-critic.md base 1565 head 1565 target 1500 over unchanged
    inspector.md base 2000 head 2000 target 2000 within unchanged
    verifier.md base 3112 head 3112 target 3000 over unchanged
    griller.md base 1925 head 1925 target 2000 within unchanged
    floor.md base 554 head 554 target 1200 within unchanged

The changed cards over target are exactly the five listed, with the right sizes; the unchanged
ones over target are exactly the six listed; griller is gone from the list. The targets are those
each card's own child set, as recorded in `3-done/510-sc24-cards-swap/evidence/e7-bytes.md:20-21`
("child 19: 1 KB = 1,000 bytes; child 20: 1 KB = 1,024"). This CR's specification restates the
program budgets with 1 KB = 1,000 bytes; read that way the three Driver targets would be 4,000,
4,000 and 3,000, and every over or within state above stays the same.

### 5B (failed before, judged again): what is back outside the table: VERIFIED

Posted: "Also back, outside the table: the Foreman card's pointer to the session-shell topic, and,
in the board restart topic, saying the line to the user once, as printed (inventory row C-640)."

    git -C WT diff --word-diff=plain 266b784 5d2626d -- skills/chantier/references
    foreman.md: + `foreman`; a shell call that waits or changes folder: `help session-shell`.
    topics/board-restart.md: + "say that line to the user once, as printed, and"
    PY vf_desc.py WT body CRF/work/pr-body.md
    table rows 37; each: home-names-card True, open False, span head True, base False
    (X-004 is one of them, and is no longer named as lacking a row id)

### The other statements

Judged in the first pass at this head unless marked "again".

| statement | proof at 5d2626d | judgment |
|---|---|---|
| renders: sections in the template's order, one fold, table, no image | body_html above (again) | VERIFIED |
| no internal reference or chantier role as doer outside Internal references (role names are product terms of the changed cards); no UNVERIFIED or STALE mark | grep of the identical `pr-body.md` for `UNVERIFIED\|STALE\|CR-\d\|batch-\d\|.agents/changes\|O-\d{3}`: one hit, the Internal references line (again) | VERIFIED |
| 1,474,636 bytes; 4629 rows; 78 sources, 11,391 lines, 900,129 bytes | `vf_claims.py WT sources`: "source files matched 78 lines 11391 bytes 900129 mismatches 0"; blob 1474636 | VERIFIED |
| kinds a601 b169 c139 d165 e3493 f62; owner lists 601, 12, 2, 601 | `vf_dump.py WT counts`; `vf_claims.py WT sections`; `test_owner_lists` | VERIFIED |
| the test: homes and checks resolve, every old line covered, kind a only floor, role card, refusal, or open | claim 2; `test_coverage`, `kind_a_homed` read | VERIFIED |
| quiz cases may cite a row id | `evals/kit/quiz.py` diff; CI case `quiz-row-id` | VERIFIED |
| `git diff --stat f08cf41 ea11a9e` prints nothing; old base f08cf41 | `git -C WT diff --stat f08cf41f ea11a9e0 -- skills/chantier/references "skills/*/SKILL.md"` -> empty | VERIFIED |
| context hand-back, no end of turn to wait, no large output whole; stale prompt text corrected | claim 1; word diff (again) | VERIFIED |
| the table of 37 restored rows | claim 1; `vf_desc.py WT body` (again) | VERIFIED |
| Changes list matches the 26 files (6 cards, `concepts.md`, 11 topics, 2 proof files, 3 tests, 3 eval files) | `diff --stat` above; `vf_desc.py WT topics`: "changed topics 11" (again) | VERIFIED |
| Blast radius one grade; Impacts "No visual change" (no UI file in the diff) | same diff | VERIFIED |
| ids with B or four digits, 1469 refused by the planned pattern | `vf_claims.py WT kinds` | VERIFIED |
| no row's kind changed | `vf_seed.py WT 3-done`: "common 4616 kind differs 0", 13 X rows new, none lost | VERIFIED |
| two test files for the 400-line limit | 255 + 238 lines; `CONTRIBUTING.md:368` | VERIFIED |
| plan announces five sections, lists six | spec lines 70-134; six `## ` headings | VERIFIED |
| ceilings raised: 9900 to 11100, 9600 to 10500, 9200 to 10300, 6100 to 6300, 22200 to 22600 | `git -C WT diff 266b784 5d2626d -- .../test_brief_bytes.py`, the five pairs as posted (again) | VERIFIED |
| 329 open = 62 a, 139 inferable, 128 others; 539 kind a homed by quote only; 12 incidents ids; none homed inferable; 129 rare | `vf_claims.py WT kinds` | VERIFIED |
| 62 read one by one, 267 judged from wording; about one in ten; 2.8 s | the authors' records `work/coder/r2.md:24-25`, `work/r1.md:65-66`, `work/r1.md:36` | disclosure, matches the record |
| H-173 and H-217 resolve only in docstrings | grep of both spans: `commands/joining.py:130`, `commands/orders_after.py:70`, docstrings | VERIFIED |
| stack card names the direct-mode host means (also before), answers one of two tags | `stack-driver.md:11,13`; base `:23`; `topics/stack-run.md:3` | VERIFIED |
| 20 of 36 checklist items are known gaps, J11/J22, CONTRIBUTING, no new quiz case | `vf_claims.py WT checklist` (16 done, 20 known gap) | VERIFIED |
| H-1360 needs the owner | inventory line 4296 | VERIFIED |
| skipped quiz commands as written (full base SHA resolves); no real run | spec lines 211-219; `02-answers.md` 5; `rev-parse f08cf41` -> `f08cf41f2c80e2e4f7ab834adc3dc06820ae7f93` | VERIFIED |
| the weak homes listed as reported by review, rare trigger set from the home, mixed role spellings | not judged row by row (disclosed gaps) | not checked |
| Human decisions | `02-answers.md` 5-10, read again | VERIFIED; note: "does not block" and "never blocking" are recorded there as the Chief of Staff's reading, to confirm |
| new tests pass; absent before | claim 2 | VERIFIED |
| `just check` (2789 passed, 19 skipped) and `just eval-dry-run` (26 of 26) pass at 5d2626d | `log CR-511`, notes 13:14:06Z and 13:21:50Z; CI jobs at the head (claim 3); local counts not rerun (the first pass's brief ordered so) | VERIFIED |
| Evidence: no visual change | diff holds no UI file | VERIFIED |
| Review approved at 5d2626d, carried from 7263861 | `log CR-511` (again): "r3 approved at 4380df52..., committed as 7263861..."; "move 7263861..5d2626d ... pass carried"; first pass `range-diff` "1: 7263861f = 1: 5d2626de" | VERIFIED |
| "Verified at `5d2626d`" (ticked) | this note: claims 1 to 5 hold at the head. The box was posted while the last recorded verdict at the head was NOT VERIFIED (13:57:23Z); it holds from the verdict recorded with this pass | VERIFIED |
| CI green; long gate on Windows passes | claims 3 and 4 | VERIFIED |

Observed, not counted as failures:

- Topic sizes are not named in Known gaps (its bullet is about cards).
  `PY vf_desc.py WT topics`: `trouble-worker.md` 2173 to 2181 (over 1,500 and 1,536 before this
  change, 8 bytes longer after); `cr-workers.md` 1624 to 1521 (shorter, still over 1,500, within
  1,536). Neither overrun is new, and no statement of the body is made false by it.
- The line after `</details>` ("Generated with Claude Code") is the attribution line the host
  requires. `pr-template.md` says nothing follows `</details>`; it renders and claims no change.
