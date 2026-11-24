# Change Specification: Release v1.12.1

## 1. What

Release version 1.12.1 of Markdown OKF-Schema Studio, by the project's own procedure:
`.agents/guidelines/release-process.guidelines.md` (rules, release folder, steps, "The version PR on
top of a stack", notes, thread), and "How to Release" and "Recovery and Release Notes" in
CONTRIBUTING.md. That procedure rules; this spec only fixes what the owner settled (02-answers.md).

## 2. Scope

- Everything on `main` since `v1.12.0`, plus batch-09's stack: `raw-text-opens-studio` (the urgent
  revert of the opening watcher), CR-475 `save-guard-never-hangs`, CR-476
  `blank-line-block-per-line`. The release waits for every other CR of the batch.
- The version PR tops the stack ("The version PR on top of a stack"): the version commit is made on
  the top branch, with `just changelog-refs origin/main --skip-missing` before the heading, the notes
  folder `docs/releases-notes/2026-11-23-v1.12.1/` (date of the PR) with `release-notes.md`,
  `tweet.md` and the images, and the PR body showing both.
- The heavy run on the top branch (`gh workflow run ci.yml --ref <top-branch> -f heavy=true`),
  `integration` and `stress` green at the top head, before the version PR is marked ready.

## 3. The notes

By the procedure's "Release notes". The revert leads: "Open With... > Text Editor" stays text again,
"every Markdown file in Studio" is VS Code's own editor association again (restored for you from the
setting), a search result opens the text editor at the line again with default settings, and opening
Studio at a line comes back in a later version; plus the known limitation of the side preview marker
under the association (raw-text-Q13). Then CR-475 and CR-476, and the lines already on `main`.
Every CHANGELOG line appears once. No docs diagram (release-Q5).

## 4. Approvals

The owner merges the whole stack with the version PR, bottom up, by rebase. Every irreversible step
after that merge (tag, GitHub release with notes and images, Marketplace and Open VSX publications)
is approved in advance (release-Q4), recorded with `order approve` at the merge. The announcement
thread is a draft for the owner. The issue comments of step 8 keep the procedure's one owner
approval.

## 5. Done

The tag `v1.12.1`, the GitHub release, both registries serving 1.12.1 (checks of record of step 6),
and `04-report.md` (and `retro.md`) in this CR's folder, as step 7 says.

## 6. Open questions

None.
