## Summary

Once a release's version PR was merged and recorded, `handoff`, `status`, `STATUS.json`/`STATUS.md`, `delivery.md`, the closed batch's record and the board all showed `PR: none` for it. The record moves the link from the open-PR field to a merged-PR field on purpose (the release procedure reads it), but every reader looked only at the open-PR field. This change gives the readers one shared reading of "the PR to show", so a release CR keeps its PR in view before and after its merge.

## Deliverables

One new reading on the CR record, used by every place that shows a CR's PR:

```python
def shown_pr(self) -> str | None:
    """The open PR if it is a link, else the merged release PR if it is a link, else None."""
```

| Reader | Open PR | Merged release PR |
| --- | --- | --- |
| `handoff` | `PR: <link>` | `PR: <link> (merged)` |
| stack lines | `PR <link>` | `PR <link> (merged)` |
| `status`, `STATUS.json`, board, `delivery.md`, closed record | link | the same plain link |

The board marks such a row `pr_merged`, so its open-PR lists (home, PRs count, merge order) leave a merged release PR out while its card still shows the link, and the PRs page does not report that merge a second time.

Evidence (before at `380eca4`, after at `4833e30`): the new tests for the release-PR cases fail on the previous code (4 failed, 65 passed) and all pass at the head (69 passed). A real run of a release CR through `order merged` shows `PR: <link>;` before the merge and `PR: <link> (merged);` after it, `status` with the plain link and `STATUS.json` with the PR object. Served board state at the head: the merged release CR is marked `pr_merged`, the home's open PRs, the PRs count and the merge order hold only the other CR, and the merged one still shows its link on its card.

## Blast radius

Grade: **1**. Readers only; the record's fields and the release logic are unchanged. A plain `git revert` restores the previous display.

## Autonomous decisions

- The board's three open-PR lists share one predicate (`openPr`, as the specification suggests). It also treats a cancelled CR as not open, where the home list and the PRs count only excluded merged ones before; a cancelled CR's PR no longer counts as open there. Reason: the merge order already used that test, so the three lists now agree.

## Known gaps

- No screenshot of the pane from a real session.
- The board's open-PR lists have no JS test; they are proven by a served board in the PR's evidence.

<details>
<summary>Details</summary>

## Changes

- `core/records.py`: `CrEntry.shown_pr()`.
- `commands/facts.py`, `commands/batch_status.py`, `status/views.py`, `status/steps.py`, `lifecycle/stages.py`, `history.py`, `board/crs.py`: show `shown_pr()` instead of the open PR only.
- `board/prs.py`: a row flagged `pr_merged` is not judged against the forge.
- `board/web/js/...`: `openPr` in `semantics.js`, used by the home's open PRs, the PRs count and the merge order.
- Tests: `test_batch_end.py`, `test_external_archive.py`, `test_board_prs_release.py`.

## Impacts

A merged release PR now shows on the release CR in every view. Already-written `delivery.md` files of earlier releases are not rewritten.

## Test plan

- [x] New or changed tests (they fail on the previous code: 4 failed, 65 passed at `380eca4`; 69 passed at `4833e30`)
- [x] Local gates at `4833e30`: `just check` pass, `just eval-dry-run` pass (17 of 17)
- [x] Evidence: before at `380eca4`, after at `4833e30`
- [x] Review: approved at `4833e30` (reviewed at `380eca4`, committed as `4833e30`)
- [x] Verified at `4833e30`
- [x] CI green at `4833e30` (all 5 jobs, scenario included)

## Internal references

- CR-367 release-pr-recorded.

</details>
