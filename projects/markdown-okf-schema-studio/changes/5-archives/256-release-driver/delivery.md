# Report: release driver and green heavy run on main before the version commit

PR: [#313](https://github.com/gsemet/markdown-okf-schema-studio/pull/313) · merged 2026-11-03 as `ee9e4eb7` (rebase, owner approved) · CI run 41730244819 green · rounds: 2/3

First PR [#312](https://github.com/gsemet/markdown-okf-schema-studio/pull/312) (CI run 41721886595, reviewed) closed unmerged: the merge was refused (branch behind `main`) and the cleanup script deleted its branch anyway; the same commit was rebased and reopened as #313.

## Delivered

- Release driver role in the change-requests lifecycle guideline (role, merge rights, prompt).
- Release process guideline: seven driver steps; heavy run green on `main` HEAD before the
  version commit; no owner question between notes review and publication; change count without
  unpublished version commits; images from a CR `-assets` branch allowed before the tag.
- CONTRIBUTING "How to Release", AGENTS.md and CI rule 14 aligned.

## Open items

- Optional: one 103-character line in ci.guidelines.md rule 14.
- CI changes (heavy jobs on PRs, nightly run, bump gate) stay in the P1 backlog item
  `release-stability-heavy-runs-before-version`.
