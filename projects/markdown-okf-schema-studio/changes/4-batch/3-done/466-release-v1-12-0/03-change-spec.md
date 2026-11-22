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
- Changelog: the version commit only moves the lines of `## Unreleased` under `## 1.12.0 - <date>`
  (guideline step 2). Two merged changes have no line: `1a5b98bb` (blank-line runs inside quotes and
  containers, PR #475) and `eb3b6ecc` (impossible comment date refused, PR #469). They are added at
  the end of `## Unreleased` by a separate `docs(changelog)` commit in CR-465's PR, with CR-465's own
  line, so one heavy run on `main` HEAD covers both. If they are not on `main` when the release
  starts, the Release driver stops and says so; it does not write them in the version commit.
- Hold: from CR-465's merge until the release is published, no other merge and no new change
  (guideline step 2).
- Release notes in `docs/releases-notes/<date>-v1.12.0/`, per the guideline's "Release notes":
  each highlight its heading, then its text (at most two sentences), then its picture cropped to
  where the change happens. Headlines: the side preview next to a diff with its target arrow and
  the change-bar tooltip; blank-line runs everywhere; the dropdown now shows its content. No docs
  diagram.
- Pictures: from the Verifier captures of the merged CRs (CR-455/456 side preview and arrow, CR-463
  tooltip, CR-448/462 blank-line runs, CR-465 dropdown). The dropdown fix gets one before | after
  image, both halves cropped to the same region at the same scale. Before the notes go to the
  owner, the Release driver checks picture order and crops against the guideline (CR-446 retro).
- Hero image (minor release, post 1 of the thread): the side preview next to a diff, from an
  existing capture or the showcase scenario.
- Placement: the side preview's limit with multi-file diffs and the merge editor (`b4d1da69`, PR
  #470) in the folded "Details"; Git long paths in `just dev` and the mutation campaign in "For
  contributors" (no changelog line).
- `tweet.md`: the guideline's thread, a draft for the owner.
- Version PR: one `chore: version 1.12.0` commit (bump, changelog, notes folder), body per the
  template and "The version PR body". The owner merges it by rebase.
- Grant: default. Every irreversible step after the merge (tag, GitHub release, Marketplace
  publication) waits for the owner's yes, asked with the merge.
- After the merge: monitor tag, GitHub release, Marketplace, Pages; archive with `04-report.md`
  (guideline step 7) and `retro.md`. Step 8: no issue is closed by this release (every batch-07 CR
  is of verbal origin, no merged PR names an issue): `04-report.md` says "No issue closed by this
  release", no owner approval asked.
