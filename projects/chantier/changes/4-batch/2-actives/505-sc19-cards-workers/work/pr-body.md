## Summary

The role cards are far heavier than the roles need. This PR writes the small replacement cards for eleven roles (coder, conflict-resolver, debugger, investigator, demo-explorer, spec-writer, spec-critic, retro-critic, inspector, verifier and the board Griller's "Started from the board" section) as new files in `skills/chantier/cards-next/`, beside the old ones. Nothing loads the new folder yet: it is an input of a later swap. A rule inventory of the old cards is written alongside, so that nothing is lost at the swap.

## Deliverables

Sizes of the old cards against the new ones (bytes, read from git):

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

Brief sizes (old cards against new, bytes, `brief <role> --cards cards-next`): coder 7549 to 4357, conflict-resolver 6833 to 4318, debugger 6622 to 4105, investigator 6494 to 4310, verifier 17521 to 5936, inspector 8984 to 4939, spec-writer 4815 to 3054, spec-critic 5290 to 3060, board Griller 11964 to 2965, retro-critic 4225 to 2816, demo-explorer 4746 to 2820. The full table, with the study's declared boot figures, is in the change's evidence.

Also added: a copy of `floor.md` (byte-identical to `skills/chantier/references/floor.md`), nine topic files under `cards-next/topics/` (each at most 1,500 bytes) and their index `cards-next/topics.json`.

## Blast radius

Grade: 1. Only new, unloaded files are added; `git revert` restores everything. The old cards, the CLI and the hooks are untouched.

## Autonomous decisions

- The inventory has one row per rule sentence of the old cards (374 rows), walked file by file, line by line; its line numbers are read from the old cards at the base of this change (the main branch).
- `brief` refuses a change in `4-batch/` for spec-writer, spec-critic and board-griller, so the brief sizes for those three use an inbox folder as the unit.

## Known gaps

- Real run not done (the final campaign of the cards work). Do not merge: merges with the rest of the cards work as one unit, after that campaign.
- **UNVERIFIED:** the quiz pass rule (no case worse than the old cards). The quiz plan (24 runs, about $8.51 against a $10 cap) leaves no room to also run the old cards for the comparison, so no quiz was run.
- Two forward links point at files a later part of the cards work writes: `../pr-template.md` and `../concepts.md` (2 and 4 uses). No link points into `references/`.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/cards-next/<role>.md` for the eleven roles, each within its byte budget.
- `skills/chantier/cards-next/floor.md`, `topics.json` and these topics: worker-shell, verifier-scratch, verifier-description, verifier-review-box, verifier-delta-matrix, verifier-before-after, verifier-images, inspector-audit, spec-writer-extras.
- The rule inventory (`evidence/cards-inventory-workers.md` of the change folder: one row per rule sentence of the old cards, 374 rows) and the byte, brief-size, link and reply-block checks are evidence files of the change, not in this diff.
- `git grep -n cards-next HEAD -- . ':(exclude)skills/chantier/cards-next'` prints no line at this head: nothing outside the folder names it.
- `just test`: no test is added or changed, so 0 s are added; the full `just check` passed at the rebased head (2932 passed, 20 skipped).
- No change outside `skills/chantier/cards-next/`.

## Impacts

No visual change and no behaviour change: the folder is read only by `brief --cards`.

## Test plan

- [ ] New or changed tests: no behaviour change
- [ ] Local gates at `<sha7>`: `just check`
- [ ] Evidence: bytes, brief sizes, links, floor comparison, reply-block diffs at `<sha7>`
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

CR-505 (SC19, part 1 of the CR).

</details>
