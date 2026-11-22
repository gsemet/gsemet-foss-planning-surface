# Change Specification: release v1.12.0

## Procedure

The project's own: `.agents/guidelines/release-process.guidelines.md` (read on `origin/main`) and
"How to Release" in `CONTRIBUTING.md`. They rank above this file.

## Decisions (from 02-answers.md)

- Version: **1.12.0**, from v1.11.0 (minor: new features).
- Content: `git log v1.11.0..main` once CR-465 (dropdown content shown and mapped) is merged:
  side preview of the real file next to a text diff; target line arrow in the side preview on a
  jump; change-bar tooltip, removed-lines marker and click-to-diff; blank-line runs inside lists,
  quotes and containers shown as blank-lines blocks; marker lines on table rows, hidden tabs and
  the front matter row; requirement found by its full ID on the requirements site; copy, cut and
  paste on a list followed by blank lines; an impossible comment date refused; Git long paths in
  `just dev` on Windows; the local mutation campaign on `src/core` (contributor tool); the
  dropdown fix.
- Heavy gate: the procedure's long check on `main` HEAD (real VS Code `integration` and `stress`
  jobs) green on the head the version commit is built on; if `main` moves, awaited again.
- Changelog: the `## 1.12.0 - <date>` section, one line per user-visible change since v1.11.0.
- Release notes in `docs/releases-notes/<date>-v1.12.0/`, per the guideline's "Release notes":
  each highlight its heading, then its text (at most two sentences), then its picture cropped to
  where the change happens. Headlines: the side preview next to a diff with its target arrow and
  the change-bar tooltip; blank-line runs everywhere; the dropdown now shows its content. No docs
  diagram.
- `tweet.md`: the guideline's thread, a draft for the owner.
- Version PR: one `chore: version 1.12.0` commit (bump, changelog, notes folder), body per the
  template and "The version PR body". The owner merges it by rebase.
- Grant: default. Every irreversible step after the merge (tag, GitHub release, Marketplace
  publication) waits for the owner's yes, asked with the merge.
- After the merge: monitor tag, GitHub release, Marketplace, Pages; archive with `report.md` and
  `retro.md`.
