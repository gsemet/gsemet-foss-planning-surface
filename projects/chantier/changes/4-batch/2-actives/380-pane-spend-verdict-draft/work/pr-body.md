## Summary

The CR board pane, the web board and the status files did not say the same things as the `chantier status` command. This PR makes them agree: the spend shows how old it is, a draft PR's "now" line says what the forge says, and a verdict carried over a clean rebase gets its own step.

## Deliverables

- The spend's age. The pane's batch title line reads `batch-28  $0.82 / $20 █░░░░░░░░░ · 12 min old` (`age unknown` when the file has no time). The web board's home batch card shows a muted `computed 3 min ago` line under Spent, and the Batch page's Spent figure reads `of $20 · computed 3 min ago`. Nothing is added when no spend is recorded.
- The draft wording. For a PR in draft, the "now" line now takes the wording of the ready line: `PR in draft: its PR <pr> is out of draft on the forge; it waits on <cr> (<pr>).` The "next" line says `Ready to merge once what is under it is.` when the PR is already out of draft, and keeps asking for the turn out of draft otherwise.
- The carried verdict. A CR handed back over a clean rebase shows `Verdict carried from <sha7>` after `Long gate carried from <sha7>`, in its status file and in the pane's Steps table.
- The web board at `924d0d7`, on the fictional demo, in English (the pane's own screenshot is a Known gap):

![The project home's batch card, with the muted "computed 3 min ago" line under Spent, at 924d0d7](./home-card-age.png)

![The Batch page's Spent figure, "of $120.00 · computed 3 min ago", at 924d0d7](./batch-page-age.png)

```text
Long gate | carried from abc1234
Verdict   | carried from abc1234
Handed back
```

## Blast radius

Grade: **1**. Display wording and two display lines; no stored format changes (no new status field). A plain `git revert` restores the previous behaviour.

## Autonomous decisions

- The web board's age reads the live cost's own time, so it follows the figure shown.
- The shared age helper for the two web views is a new small script, `js/model/spend-age.js`.

## Known gaps

- No screenshot of the pane from a real session.

<details>
<summary>Details</summary>

## Changes

- `hooks/register.tsx`, `types/index.d.ts`: title line age from `spent_at`; `docs/boards.md` updated.
- Web board: `js/model/spend-age.js`, `js/views/home-batch.js`, `js/views/batch.js`, English and French words.
- `stacks.py`, `status/words.py`, `commands/driver.py`: one shared clause for the ready line and the "now" line.
- `status/steps.py`: the `Verdict` step.
- Tests: `test_cli_units.py`, `hooks/register.test.tsx`, and the scenario's checks.

## Impacts

The pane and the web board show the spend's age; status files word a draft PR's state like the ready line.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Local gates at `924d0d7`: `just check`, `just mod`, `just eval-dry-run` pass
- [x] Evidence: web board home card and Batch page captured at `924d0d7`; no screenshot of the pane from a real session (see Known gaps)
- [x] Review: approved at `924d0d7`
- [x] Verified at `924d0d7`
- [x] CI green at `924d0d7`

## Internal references

- CR-380 pane-spend-verdict

</details>
