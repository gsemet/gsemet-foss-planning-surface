# Change Specification: release v1.10.1

## Procedure

The project's own: `.agents/guidelines/release-process.guidelines.md` (read on `origin/main`) and
"How to Release" in `CONTRIBUTING.md`. They rank above this file.

## Decisions (from 02-answers.md)

- Version: **1.10.1**, from v1.10.0 (owner: "fais une release (patch)").
- Content: batch-07, merged on `main` before the version commit: CR-435 (CRLF test fixtures kept
  CRLF, save tests on CRLF/LF/mixed files, PR #445) and CR-436 (block editor no longer stuck on
  "Saving Markdown..." in CRLF files; each file's own line endings kept). The release is prepared
  after CR-436's merge.
- Heavy gate: the procedure's long check on `main` HEAD (the real VS Code `integration` and
  `stress` jobs) must be green on the head the version commit is built on; if `main` moves, it is
  awaited again.
- Changelog: the `## 1.10.1 - <date>` section, one line per user-visible change since v1.10.0,
  from the merged PRs and `git log v1.10.0..main`.
- Release notes in `docs/releases-notes/<date>-v1.10.1/`: short, for a user, per "Release notes"
  of the guideline, with the owner's new shape (answer 3): each highlight is its heading, then its
  text (at most two sentences), then its picture, cropped to where the change happens (no toolbar
  or empty margin around it). The headline: editing a CRLF file no longer leaves the editor stuck,
  and Studio keeps the file's own line endings. A fix with nothing to show may have no picture.
  No docs diagram.
- `tweet.md`: the guideline's thread.
- Version PR: one `chore: version 1.10.1` commit (bump, changelog, notes folder), body per the
  template and "The version PR body". The owner merges it by rebase.
- Grant: default. Every irreversible step after the merge (tag, GitHub release, Marketplace
  publication) waits for the owner's yes, asked with the merge; the announcement stays the
  owner's.
- After the merge: monitor tag, GitHub release, Marketplace, Pages; archive with `report.md` and
  `retro.md`.
