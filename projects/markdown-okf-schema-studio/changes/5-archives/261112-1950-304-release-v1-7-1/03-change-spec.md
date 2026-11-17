# Change Specification: release v1.7.1

## Procedure

The project's own: `.agents/guidelines/release-process.guidelines.md` (read on `origin/main`) and
"How to Release" in `CONTRIBUTING.md`. They rank above this file.

## Decisions (from 02-answers.md)

- Version: **1.7.1**, from v1.7.0.
- Heavy gate: run 43262188098 on `main` HEAD `cf51f12f` is green (`integration`, `stress`). If `main`
  HEAD moves before the version commit, the gate is awaited again on the new HEAD.
- Changelog: `## Unreleased` is empty. The version commit adds the `## 1.7.1 - <date>` section with
  one line per user-visible change since v1.7.0, written from the merged PRs #371 to #374 and the
  commits `v1.7.0..cf51f12f`: the share picture card of site pages, the Main paths of every use case
  (StRS) and their SwRS check, the requirements viewer on the published site (with its accessibility
  and no-JavaScript fixes), and the one cream look of the whole site (with the header breadcrumb fix).
  This replaces step 2's "changelog lines in the stack PRs" for this release only (owner's word).
- Release notes in `docs/releases-notes/<date>-v1.7.1/`: short, for a user, centred on the site (the
  requirements viewer, the cream site, the share cards), following "Release notes" of the guideline
  (header, links, two or three highlights, folded fixes and contributors parts). Hero image: a capture
  of the requirements viewer in the cream theme. No docs diagram.
- `tweet.md`: the three-post thread of the guideline.
- Version PR: one `chore: version 1.7.1` commit (bump, changelog, notes folder), body per the template
  and "The version PR body". The owner merges it by rebase.
- Grant: default. Every irreversible action waits for the owner's approval; no fix is merged without
  the owner.
- After the merge: monitor tag, GitHub release, Marketplace, Pages; archive with `report.md` and
  `retro.md`; draft the issue comments of step 8 for one owner approval.
