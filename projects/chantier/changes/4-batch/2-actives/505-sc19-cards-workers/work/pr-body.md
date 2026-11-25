## Summary

The role cards are far heavier than the roles need. This PR writes the small replacement cards for eleven roles (coder, conflict-resolver, debugger, investigator, demo-explorer, spec-writer, spec-critic, retro-critic, inspector, verifier and the board Griller's "Started from the board" section) as new files in `skills/chantier/cards-next/`, beside the old ones. Nothing loads the new folder yet: it is an input of a later swap. A rule inventory of the old cards is written alongside, so that nothing is lost at the swap.

## Deliverables

Sizes of the old cards against the new ones (bytes, read from git):

| Role | Old card | New card | Budget |
| --- | --- | --- | --- |
| coder | 4609 | 1434 | 1500 |
| conflict-resolver | 3893 | 1378 | 1500 |
| debugger | 3682 | 1165 | 1500 |
| investigator | 3554 | 1370 | 1500 |
| demo-explorer | 3422 | 1487 | 1500 |
| spec-writer | 3254 | 1498 | 1500 |
| spec-critic | 3729 | 1499 | 1500 |
| retro-critic | 2901 | 1492 | 1500 |
| inspector | 6044 | 1985 | 2000 |
| verifier | 14581 | 2991 | 3000 |
| board Griller section | 2198 | 1630 | 2000 |

Also added: a copy of `floor.md` (byte-identical to `skills/chantier/references/floor.md`), nine topic files under `cards-next/topics/` (each at most 1,500 bytes) and their index `cards-next/topics.json`.

## Blast radius

Grade: 1. Only new, unloaded files are added; `git revert` restores everything. The old cards, the CLI and the hooks are untouched.

## Autonomous decisions

- The inventory is grouped by rule group, not one row per sentence, to keep it readable; it names how the sources were walked.
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
- The rule inventory (one row per rule sentence of the old cards, 374 rows) and the byte, brief-size, link and reply-block checks are kept as evidence files of the change, not in this diff.
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
