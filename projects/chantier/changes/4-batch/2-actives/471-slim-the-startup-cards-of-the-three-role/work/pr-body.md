## Summary

The Chief of Staff, Foreman and Driver role cards were each read nearly whole at start, hundreds of kilobytes for the first two. Each card is now cut by moment of need: the entry card keeps its opening and a list of moments, and each piece is a new `<role>-<moment>.md` card that a `startup-manifest.json` action reads when that situation arrives. Text moves, it is not reworded; no rule is added or dropped (five duplicates were removed, each still stated elsewhere).

## Deliverables

Start reading per role (Claude host, bytes, each byte once; base = this branch's parent):

| Role | Base | After | Ratio |
|---|---|---|---|
| Chief of Staff | 380,314 | 177,821 | 0.47 |
| Foreman | 292,020 | 86,857 | 0.30 |
| CR Driver | 25,134 | 27,122 | 1.08 |
| Stack Driver | 66,302 | 32,692 | 0.49 |
| QA Driver | 36,137 | 24,064 | 0.67 |
| Release Driver | 47,462 | 25,391 | 0.53 |

- The 12,544-byte startup limit is unchanged; the highest reload is 12,511 (Chief of Staff, Copilot). To fit the larger manifest (4,556 to 5,405 bytes) bytes were freed in the Chief of Staff's startup text and the manifest itself, with no rule lost.
- The Chief of Staff and the Foreman read only their own host's card, by section for the Foreman.
- New tests: every level-2 section is reached by an action for each host; each entry card's moments agree with the manifest; 83 moved rules are checked at their new place; start readings are capped so they cannot grow back unnoticed.

## Blast radius

Grade: **2**. Instructions now arrive by action; a rule a role fails to read at its moment is the risk. Revert restores the single cards.

## Autonomous decisions

- The session-start reading takes only its own host card (also narrows the Griller's reading), to fit the limit.
- Five duplicate sentences removed, each still said elsewhere.

## Known gaps

- The CR Driver's start reading grew (1.08 of base): its boot now carries the list of moments that were links before.
- The Foreman's "a Driver's silence" section exists only in the Claude host card, so its action cannot name it in the one-host form; the Foreman's reference action reads the whole host card, so it is reached.
- The independent reading of each role's split on a second model is still to run before merge.

<details>
<summary>Details</summary>

## Changes

- New pieces `chief-of-staff-*.md`, `foreman-*.md`, `driver-*.md`, `stack-driver-*.md`, `release-driver-*.md`; entry cards trimmed; manifest actions added; links in cards, `CONTRIBUTING.md`, `evals/` updated; compaction sentence in `session-start.md`.
- Tests: `test_role_cards_split.py`, `test_start_reading.py`, `moved_rules.tsv`; nine tests read the file where a phrase now lives, assertions kept.

## Impacts

No visible change; roles read less at start.

## Test plan

- [ ] Full test suite and lint pass at `4a1b125` (2397 passed).
- [ ] Long gate at the PR head: pending.

## Internal references

CR-471 slim-cards; closes the backlog item role-cards-still-too-big-for-a-driver-s-.

</details>
