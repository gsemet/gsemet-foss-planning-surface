## Summary

The user docs disagreed on whether a CR's cleaned archive goes into its PR when the project says nothing. The CLI decides no (since v0.13.0), and `docs/planning-modes.md` already says no, but `docs/planning-folder.md` said "default yes". This fixes that one line so the docs match the CLI and each other.

## Deliverables

None (a one-line docs fix).

## Blast radius

Grade: 1 — text only; a plain `git revert` restores the previous wording.

## Autonomous decisions

None

## Known gaps

None

<details>
<summary>Details</summary>

## Changes

- `docs/planning-folder.md` line 55: "(default yes)" becomes "(default no)" for the archive copy in the PR.

## Impacts

No visual change; the page now matches `docs/planning-modes.md` and the CLI.

## Test plan

- [x] New or changed tests: No behaviour change (docs only)
- [x] Local gates at `d64a996`: `just check`
- [x] Evidence: `git grep -n -i "default yes" -- docs ':!docs/release-notes'` prints nothing at `d64a996`
- [x] Review: approved at `4fdf6fc`
- [x] Verified at `d64a996`
- [x] CI green at `d64a996`

## Internal references

- CR-392 docs-planning-folder-md-says-the-archive

</details>
