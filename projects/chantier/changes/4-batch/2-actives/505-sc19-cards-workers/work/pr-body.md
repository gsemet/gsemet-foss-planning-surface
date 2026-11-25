## Summary

The role cards are far heavier than the roles need: an agent starts by reading thousands of bytes of rules, most of them for cases that do not come up. This PR writes the small replacement cards for fifteen roles: the four Driver roles (CR driver, stack driver, QA driver, release driver) and eleven others (coder, conflict-resolver, debugger, investigator, demo-explorer, spec-writer, spec-critic, retro-critic, inspector, verifier and the board Griller's "Started from the board" section). They are new files in `skills/chantier/cards-next/`, beside the old ones, with 45 Driver topics for the rare cases and 9 topics for the other roles. Nothing loads the new folder yet: it is an input of a later swap. A rule inventory of the old worker cards is written alongside, so that nothing is lost at the swap.

## Deliverables

Sizes of the old worker cards against the new ones (bytes, read from git at `5be593b`):

| Role | Old card | New card | Budget |
| --- | --- | --- | --- |
| coder | 4609 | 1417 | 1500 |
| conflict-resolver | 3893 | 1378 | 1500 |
| debugger | 3682 | 1165 | 1500 |
| investigator | 3554 | 1370 | 1500 |
| demo-explorer | 3422 | 1496 | 1500 |
| spec-writer | 3254 | 1493 | 1500 |
| spec-critic | 3729 | 1499 | 1500 |
| retro-critic | 2901 | 1492 | 1500 |
| inspector | 6044 | 1999 | 2000 |
| verifier | 14581 | 2996 | 3000 |
| board Griller section | 2198 | 1758 | 2000 |

Sizes of the Driver cards (the old shared Driver card is 54,955 bytes):

| Role | New card | Target |
| --- | --- | --- |
| cr-driver | 3,280 | 4,096 |
| stack-driver | 3,321 | 4,096 |
| qa-driver | 1,337 | 2,048 |
| release-driver | 3,277 | 3,072 |

Brief sizes (the start brief an agent receives: card, floor, facts and host rows; bytes, old cards against new, `brief <role> --cards cards-next`): coder 7549 to 4357, conflict-resolver 6833 to 4318, debugger 6622 to 4105, investigator 6494 to 4310, verifier 17521 to 5936, inspector 8984 to 4939, spec-writer 4815 to 3054, spec-critic 5290 to 3060, board Griller 11964 to 2965, retro-critic 4225 to 2816, demo-explorer 4746 to 2820. Driver role-only briefs, re-measured at the head: old 59,216 each against new 7,442 (cr), 7,483 (stack), 7,439 (release), 5,499 (qa); the targets are 6, 6, 5 and 4 KB. The full table, with the study's declared boot figures, is in the change's evidence.

Also added: a copy of `floor.md` (byte-identical to `skills/chantier/references/floor.md`), nine topic files for the first eleven roles (each at most 1,500 bytes), 45 topic files for the Drivers and their index `cards-next/topics.json`.

## Blast radius

Grade: 1. Only new, unloaded files are added; `git revert` restores everything. The old cards, the CLI and the hooks are untouched.

## Autonomous decisions

- The inventory has one row per rule sentence of the old worker cards (374 rows), walked file by file, line by line; its line numbers are read from the old cards at the base of this change (the main branch).
- `brief` refuses a change in `4-batch/` for spec-writer, spec-critic and board-griller, so the brief sizes for those three use an inbox folder as the unit.
- One pull request holds the worker cards and the four Driver cards: they share the floor, the topic index and the budgets, and nothing loads either until the swap.

## Known gaps

- **UNVERIFIED:** the quiz pass rule (no case worse than the old cards) for all fifteen roles; no quiz was run. Workers: the quiz plan (24 runs, about $8.51 against a $10 cap) leaves no room to also run the old cards for the comparison. Drivers: the host CLI is not on this machine, the full CR driver quiz costs about $19.35 against the cap, and the QA driver has no case.
- **UNVERIFIED:** any real run of the new cards. The real run is the final campaign of the cards work, a later child of it, and the merge waits on it: that wait is not recorded yet. Do not merge before it; this merges with the rest of the cards work as one unit.
- release-driver is 3,277 bytes against its 3,072 target (the Inspector reported it as minor and it is accepted here).
- 23 of the 45 Driver topics are over the 1,536-byte target (worst: release-merged 2,845, cr-ship 2,413, stack-changes 2,354, retake 2,328, release-ship 2,306); the full list with sizes is in the change's evidence report.
- Driver briefs are over their boot targets (7,442, 7,483, 7,439, 5,499 against 6, 6, 5, 4 KB): the fixed host rows (3,414 bytes), the floor and the facts set the floor, and the role data file is out of scope here.
- The brief sizes of spec-writer, spec-critic and board-griller use an inbox folder as the unit, as `brief` refuses a change in `4-batch/` for them.
- Two forward links point at files a later part of the cards work writes: `../pr-template.md` and `../concepts.md` (2 and 4 uses). No link points into `references/`.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/cards-next/<role>.md` for the eleven worker roles (the board Griller's is `griller.md`) and `cr-driver.md`, `stack-driver.md`, `qa-driver.md`, `release-driver.md`, each with its byte budget or target (release-driver over it, see Known gaps); the Driver topics (for example refused-push, retake, closing, ci, conflicts, lease) are in `topics/` and `topics.json` (54 topic files in all: 9 for the workers, 45 for the Drivers).
- `skills/chantier/cards-next/floor.md`, `topics.json` and the worker topics: worker-shell, verifier-scratch, verifier-description, verifier-review-box, verifier-delta-matrix, verifier-before-after, verifier-images, inspector-audit, spec-writer-extras.
- The rule inventory (`evidence/cards-inventory-workers.md` of the change folder: one row per rule sentence of the old worker cards, 374 rows) and the byte, brief-size, link and reply-block checks are evidence files of the change, not in this diff.
- `git grep -n cards-next HEAD -- . ':(exclude)skills/chantier/cards-next'` prints no line at this head: nothing outside the folder names it.
- The PR's own two commits change 71 files, all under `skills/chantier/cards-next/` (15 cards, `floor.md`, `topics.json`, 54 topics); no CLI source and no test is changed.

## Impacts

No visual change and no behaviour change: the folder is read only by `brief --cards`.

## Test plan

- [x] New or changed tests: no behaviour change; no CLI `src/` or test file changes, so `just test` adds 0 s
- [x] Local gates at `5be593b`: `env -u NO_COLOR just check` exit 0 (2932 passed, 20 skipped, 204 s); `just eval-dry-run` exit 0 (25 of 25 cases as expected)
- [x] Evidence: bytes, brief sizes, links, floor comparison, reply-block diffs at `5be593b`
- [x] Review: approved at `5be593b` (Inspector round 4 on the Driver cards, content as committed; the worker cards were approved at an earlier round with the same content)
- [ ] Verified at `5be593b`
- [ ] CI green at `5be593b`

## Internal references

CR-505 (SC19 worker cards, SC20 Driver cards and topics: both parts of the one CR); the final real run of the cards work is its child 28.

Driver note: proofs stated at the pushed head `5be593b7486739c435eaf3db8922ce1f0d490637`, base main; Verified and CI stay unticked until they happen.

</details>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
