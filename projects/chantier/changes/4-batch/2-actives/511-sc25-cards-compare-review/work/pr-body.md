## Summary

The role cards (the instructions each agent reads) were rewritten to be much shorter. Nothing showed
that no rule protecting the user or the repository was dropped on the way. This change puts every
rule of the old card set in one table, restores the serious lost ones, corrects card text about
output the CLI no longer prints, and adds a test that keeps the table consistent. It does not close
every row: 329 stay open in a committed list (see Known gaps).

## Deliverables

- `docs/proofs/cards-inventory.md` (generated, 1,474,636 bytes): 4629 rows from 78 old source files
  (11,391 lines, 900,129 bytes); by kind a 601, b 169, c 139, d 165, e 3493, f 62. Ranges holding no
  rule, four lists for the project owner (601, 12, 2 and 601 rows) and a hand-over checklist.
- `docs/proofs/cards-inventory-open.tsv`: the exact list of open rows, with a reason each.
- `test_cards_inventory.py` (reader in `cards_inventory.py`): homes and checks resolve, every old
  line is covered, a rule that protects the user or the repository is homed only in a floor rule, a
  role card or a CLI refusal (or is listed as open).
- The eval kit's quiz cases may cite an inventory row id.
- The old base is `f08cf41`; `git diff --stat f08cf41 ea11a9e -- skills/chantier/references
  'skills/*/SKILL.md'` prints nothing. The Sources table copies `git ls-tree -r f08cf41 -- …` and
  `git show f08cf41:<path> | wc -l -c`.
- Back in the Driver cards, among others: the hand-back on context at 130,000 tokens, never ending a
  turn to wait for a worker, never taking a large output whole.
- Corrected: the cards and topics that described a prompt skeleton, a worker's opening lines and a
  `writes:` line the CLI no longer prints.

Restored rules, one line per row id (files under `skills/chantier/references/`):

| row | restored in |
|---|---|
| D-006 | cr-driver.md |
| D-014 | cr-driver.md |
| D-024 | cr-driver.md |
| D-026 | cr-driver.md |
| D-027 | cr-driver.md |
| D-028 | cr-driver.md |
| D-030 | cr-driver.md |
| D-032 | cr-driver.md |
| D-035 | cr-driver.md |
| D-041 | cr-driver.md |
| D-045 | cr-driver.md |
| D-047 | cr-driver.md |
| D-048 | cr-driver.md |
| D-050 | cr-driver.md |
| D-051 | cr-driver.md |
| D-052 | cr-driver.md |
| D-055 | cr-driver.md |
| D-077 | stack-driver.md |
| D-082 | qa-driver.md |
| D-084 | release-driver.md |
| FM-494 | foreman.md |
| FM-495 | foreman.md |
| FM-507 | foreman.md |
| FM-508 | foreman.md |
| FM-541 | foreman.md |
| FM-558 | foreman.md |
| FM-584 | foreman.md |
| H-425 | cr-driver.md |
| P-001 | cr-driver.md |
| P-011 | cr-driver.md |
| P-016 | stack-driver.md |
| P-017 | stack-driver.md |
| P-018 | stack-driver.md |
| W-052 | conflict-resolver.md |
| W-062 | conflict-resolver.md |
| X-004 | stack-driver.md |
| X-005 | stack-driver.md |

Also restored without a row id: a release with no PR yet is no anomaly (stack driver card), the
Foreman card's pointer to the session-shell topic, and "say it once to the user as printed" (board
restart topic).

## Blast radius

- **2**: card text every batch role reads, a proof file, tests and the eval kit's loader; a plain
  revert restores it.

## Autonomous decisions

- Row ids accept an optional `B` and four digits: the existing ids must stay unchanged, and the
  planned pattern refused 1469 of them.
- No row's kind was changed to make it pass; a protective rule goes to a card or a refusal, or stays
  listed as open.
- The inventory test is two files, because of the project's 400-line limit on a code file.
- The written plan announces five sections for the inventory and lists six; it has the six, so that
  the hand-over checklist has its own place.
- Test ceilings raised to fit the restored lines (see Known gaps).

## Known gaps

- 329 rows stay open (62 of kind a, 139 inferable with no quiz case, 128 others), listed in
  `docs/proofs/cards-inventory-open.tsv`. The goal that every row has a resolving home is not met.
  Only serious lost rules were restored, on the owner's choice to finish quickly.
- The 62 open kind-a rows were read one by one against the new cards; the other 267 open rows were
  judged from their wording, not searched one by one.
- A sample suggests up to about one in ten automatically mapped homes of non-protective rows may not
  hold its rule; no test can see this.
- Reported by review on an earlier state and not changed since: some homes point at text that does
  not state the rule (W-001, W-038, W-076, W-108, W-156, W-238, W-283, H-119, H-120, C-1220, C-1223,
  C-1535, C-1536, FM-474, FM-475); H-173 and H-217 resolve only in code docstrings; the trigger
  `none (rare)` was set from the home, so the rare-rule test cannot fail on those 129 rows; the role
  column mixes spellings.
- The stack driver card's context hand-back points to a host means that names direct mode only (it
  already did for another line), and its answer-every-message line names only one of the two message
  tags the topics use.
- The 539 kind-a rows that have a home are checked by quote only (the text is still where the row
  says), with no behaviour check yet; the other 62 are open. The owner lists (601 kind-a rows) are in
  the inventory and are not repeated here. Rows homed in the incidents file: H-439, H-989, H-1040,
  H-1041, H-1059, H-1069, H-1191, H-1192, H-1203, H-1212, H-1306, H-1551; no row is homed as
  inferable.
- 20 of the 36 hand-over checklist items end as known gaps, each with its reason in the inventory,
  among them: the scorecard rails J11 and J22 are not reconciled with the new wording, one sentence
  of CONTRIBUTING.md is not aligned, and no new quiz case was written.
- H-1360 (a rule dropped by default, pending the owner's confirmation) needs that confirmation.
- Card size targets exceeded by this change, in LF bytes (before to now, target): cr-driver 3749 to
  5066 (4000), stack-driver 3783 to 4821 (4000), release-driver 3809 to 4685 (3000, already over),
  foreman 3997 to 4426 (4000), conflict-resolver 1494 to 1535 (1500). Already over and unchanged:
  coder, demo-explorer, retro-critic, spec-critic, spec-writer, griller, verifier.
- Brief byte ceilings raised in `test_brief_bytes.py`: cr-driver 9900 to 11100, release-driver 9600
  to 10500, stack-driver 9200 to 10300, qa-driver 6100 to 6300, foreman 22200 to 22600.
- Not run: skipped on the owner's word, 2026-11-26: `just quiz <role> --plan --max-usd 10`,
  `just quiz <role> --cards f08cf41f2c80e2e4f7ab834adc3dc06820ae7f93 --max-usd 10 --save old-<role>`
  and `just quiz <role> --max-usd 10 --against <the saved old results>`, for each role under
  `evals/quiz/` (the session roles add `--model`). So no result shows the new cards answer as well
  as the old ones.
- Real run not done (a later, separate campaign).
- No separate verification run has judged the claims yet.
- The long gate `scenario` on Windows is not yet proven; it is run at the final head.
- The seconds the new test adds to `just test` were not measured as two runs before and after; the
  test file alone took 2.8 s of pytest wall time at an earlier state.

<details><summary>Details</summary>

## Changes

- `docs/proofs/cards-inventory.md`, `docs/proofs/cards-inventory-open.tsv`: new.
- `skills/chantier/scripts/cli/tests/cards_inventory.py`, `test_cards_inventory.py`: new;
  `test_brief_bytes.py`: ceilings.
- `skills/chantier/references/`: Driver, Foreman and conflict resolver cards, `concepts.md` and
  eleven topics.
- `evals/kit/quiz.py`, `evals/kit/dry_run.py`, `evals/README.md`: inventory row ids in `rules`.

## Human decisions

- No quiz run and no evaluation campaign in this change; the owner runs them later, and their absence
  does not block it.
- The priority is the simpler cards and the stronger command line; a quiz or evaluation finding is a
  known gap, never blocking.
- The card text about output the command line no longer prints is fixed here.
- Cut further to finish quickly, even if things are fixed afterwards. How it was applied: only the
  serious lost rules are restored, the other open rows stay listed for a follow-up change.

## Impacts

Agents read slightly longer cards. No visual change.

## Test plan

- [x] New tests: `test_cards_inventory.py` and the dry-run case `quiz-row-id`, passing at `5d2626d`
  (the file they read does not exist on the previous code)
- [x] Local gates at `5d2626d`: `just check` passes (2789 passed, 19 skipped); `just eval-dry-run`
  passes (26 of 26 cases)
- [x] Evidence: no visual change, so no before and after images
- [x] Review: approved at `5d2626d` (carried from `7263861`)
- [ ] Verified at the head: **UNVERIFIED:** until the verification run
- [x] CI green at `5d2626d`: `just check` (ubuntu, macos, windows), `just eval-dry-run` and
  `just scenario` (ubuntu) pass
- [ ] Long gate `scenario` on Windows: **UNVERIFIED:** until it runs at the final head

## Internal references

CR-511 sc25-cards-compare-review

</details>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
