## Summary

After a restack, a PR body could keep a proof claimed at a commit that had left the branch's history, and screenshots linked into such a commit could be dropped by the forge. `ship`'s check of the body skipped every line holding `carried from` or `STALE`, so these cases went unnoticed. `ship` now also checks image links on every line and only exempts the SHA right after `carried from`.

## Deliverables

`ship` prints a new line for a stale image, and checks the text of a carried proof more strictly.

| Body line | Before | After |
| --- | --- | --- |
| `Verified at 15359cc (carried from 7f07565)` | skipped whole | names `15359cc` when it left the history; the SHA after `carried from` is exempt |
| `![after](https://github.com/o/r/blob/<sha>/a.png?raw=true) carried from ...` | skipped | `shows an image from <sha7>, not in <head7>'s history: attach it with the forge's CLI` |
| `STALE <img src="https://raw.githubusercontent.com/o/r/<sha>/b.png">` | skipped | same image line (text of a `STALE` line stays exempt) |

The cards say that a carried proof is written `at <head7> (carried from <sha7>)`, that a link into a branch commit is not an upload, and that an image found after a move is attached with the forge's CLI before the PR turns ready.

## Blast radius

Grade: **1**. `ship` only reports more lines; the cards gain wording. A `git revert` restores the previous behaviour.

## Autonomous decisions

None.

## Known gaps

None.

<details>
<summary>Details</summary>

## Changes

- `delivery.py`: `_stale_body_shas` checks Markdown and HTML image URLs first on every line, then the text of the line (not for `STALE` lines) with the image URLs and the SHA right after `carried from` removed.
- `pr-template.md` and `driver.md`: the carried-proof form, the upload rule for images, and the restack paragraphs.
- Scenario: the stale-body step now expects four named lines; its README line is updated.

## Impacts

No visual change. A Driver sees more `off:` lines after a restack when a body still links an image into a dropped commit.

## Test plan

- [x] New or changed tests: the scenario's stale-body step is widened (four lines named, none once the body is fixed)
- [x] Local gates: carried from `5e73a36` (`just check`, `just eval-dry-run`; clean rebase onto CR-350, head `3f16473`); local Windows `just scenario` at `3f16473` (the stack's top): pass
- [x] Evidence: No visual change
- [x] Review: carried from `5e73a36` (clean rebase onto CR-350, head `3f16473`)
- [x] Verified: carried from `5e73a36` (clean rebase onto CR-350, head `3f16473`)
- [x] CI green at `3f16473` (macOS, Ubuntu, Windows checks, eval dry run and scenario)

## Internal references

- CR-351 restack-rechecks-pr-bodies

</details>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
