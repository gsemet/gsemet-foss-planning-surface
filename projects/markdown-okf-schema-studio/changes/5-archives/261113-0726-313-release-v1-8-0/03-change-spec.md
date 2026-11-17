# Change Specification: release v1.8.0

## Procedure

The project's own: `.agents/guidelines/release-process.guidelines.md` (read on `origin/main`, and as
the `changelog-line-in-each-pr` CR of this batch changes it) and "How to Release" in
`CONTRIBUTING.md`. They rank above this file.

## Decisions (from 02-answers.md)

- Version: **1.8.0**, from v1.7.1 (`just bump-version` gives it from the `feat:` commits).
- Delivery: the version PR is the **top of the batch's stack**, not opened after the stack merged
  (owner's word, written in the guideline by `changelog-line-in-each-pr`). It is based on the last
  CR branch of the stack and contains only the `chore: version 1.8.0` commit.
- Gate: before the version PR turns ready, the heavy run is dispatched on the version PR's branch
  (`gh workflow run ci.yml --ref <branch> -f heavy=true`) and `integration` and `stress` are green on
  its exact head. A restack of the stack starts the gate again. A locked screen on the local
  preflight is no blocker: the branch heavy run is the proof.
- Changelog: each CR of the stack adds its `## Unreleased` line in its own PR; the version commit
  turns `## Unreleased` into `## 1.8.0 - <date>` and adds nothing else.
- Release notes in `docs/releases-notes/<date>-v1.8.0/`, per "Release notes" of the guideline: short,
  for a user. Highlights: Cmd+S saves from the preview; GitHub alerts keep a heading as a heading,
  as on GitHub; the sticky heading band stays on one line. The other fixes in the folded part. One
  hero image of a user-visible change (the sticky band or the alert). No docs diagram. No mention of
  Open VSX.
- `tweet.md`: the three-post thread of the guideline; never posted by an agent.
- The owner merges the whole stack by rebase, in order, the version PR last; the version push on
  `main` stays the final gate and makes the tag.
- Grant: default. Every irreversible action waits for the owner's approval; no fix is merged without
  the owner.
- After the merge: monitor tag, GitHub release, Marketplace (check of record per the updated step 6),
  Pages; archive with `report.md` and `retro.md`. Step 8: no GitHub issue is open, so the list is
  empty: one line in `report.md`.
