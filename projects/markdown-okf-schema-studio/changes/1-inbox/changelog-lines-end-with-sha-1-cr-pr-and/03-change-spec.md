# CHANGELOG lines end with their commit, CR, PR or MR and issue

Short name: `changelog-refs`. No tracker issue (origin: the owner, batch-08 retro, 2026-11-22).

## Goal

Every line of `CHANGELOG.md` ends with its references in parentheses: the commit, the change
request, the pull request (or merge request) and the linked issue when there is one. A reader of
the changelog finds where each line came from without searching, and no `docs(changelog)` commit
on `main` is needed afterwards to add a forgotten number (as 95d34013 and 369e8bad had to in
batch-07).

The owner's standing word holds for every rule, word and script of this change: forge-neutral.
GitHub, GitLab and Jira are equals; the text says "pull request (merge request on GitLab)", never
assumes `gh`, and the script uses `git` only.

## Decisions carried from `02-answers.md`

| Q | Decision | Where it lands below |
| --- | --- | --- |
| Q1 | The commit is added at release by a script: for each line of `## Unreleased`, it finds on `main` the commit that added the line (git blame) and adds its short SHA-1. No follow-up commit on `main`. | 3, 4, 5 |
| Q2 | The PR/MR number is added by the author right after opening the pull request, in the same branch, before it is marked ready. | 1 |
| Q3 | Labelled references in the forge's own notation; a piece that does not exist is left out. | 1, 3 |
| Q4 | No check enforces the rule; it lives in the guidelines only. The release script is not a check. | 1, "Out of scope" |
| Q5 | The rule lives in the project only: the pull-request guideline (CHANGELOG part) and the release-process guideline (the SHA-1 step). No chantier CR. | 1, 2 |
| Q6 | Specified for the running batch, batch-09. | - |

## The format (Q3)

One group in parentheses at the end of the line (the end of the last physical line of the bullet),
its items separated by `, `, in this order:

1. `commit <short SHA-1>`: added by the release script only, never by hand.
2. `CR-<number> <short name>`: the change request's number and short name, when the change has one
   (a pull request opened directly has none).
3. The pull request in the forge's notation: `PR #476` on GitHub, `MR !476` on GitLab.
4. `issue <ref>` for the linked issue, when there is one: `issue #413` (GitHub or GitLab),
   `issue PROJ-12` (Jira). Several issues: one `issue` item each (see "Writer's choices").

Examples:

- GitHub, as written by the author: `(CR-463 change-bar-tooltip, PR #476, issue #413)`; after
  release: `(commit 1a5b98b, CR-463 change-bar-tooltip, PR #476, issue #413)`.
- GitLab: `(commit 1a5b98b, CR-463 change-bar-tooltip, MR !476, issue #413)`.
- Jira issue: `(commit 1a5b98b, PR #476, issue PROJ-12)` (no CR: a pull request opened directly).
- Minimum, a pull request with no CR and no issue: `(PR #476)`, then `(commit 1a5b98b, PR #476)`.

## What changes

### 1. `.agents/guidelines/pull-request.guidelines.md`: new section "CHANGELOG line"

Add a section `## CHANGELOG line`, between "PR body for an external reader" and "Draft until
mergeable". It says, in the guideline's own plain style:

- The `## Unreleased` line a `feat` or `fix` pull request adds to `CHANGELOG.md` (when and where:
  [release-process.guidelines.md](release-process.guidelines.md), step 2) ends with its
  references in parentheses, in the format above, with the three examples (GitHub, GitLab, Jira).
- Whoever opens the pull request writes the CR item and the issue item with the line, and adds the
  PR/MR item right after opening the pull request (the forge gives the number only then), in a
  commit on the same branch, before the pull request is marked ready. A piece that does not exist
  is left out.
- The commit item is never written by hand: the release adds it (link to the release-process
  guideline, step 5).
- No check enforces the format; it is read in review like the rest of the diff.
- The CHANGELOG line is not the PR body: the rule "no CR numbers in the body text" still holds for
  the body; the references belong in the CHANGELOG line.

In "Draft until mergeable", the bullet "Mark it ready ... only when ..." gains the condition "the
CHANGELOG line, when there is one, names its pull request". Keep that bullet's `gh` commands as
they are (see "Out of scope").

The project guidelines name no process role (`test/build/test_guideline_isolation.py`, regex
`ROLES`): write "whoever opens the pull request" or "the author", never "Driver" or "coder".

### 2. `.agents/guidelines/release-process.guidelines.md`

- Step 2: after "adds one user-facing line to `CHANGELOG.md` `## Unreleased`", add that the line
  ends with its references, written as in "CHANGELOG line" of
  [pull-request.guidelines.md](pull-request.guidelines.md).
- Step 5: the version commit becomes `just bump-version`, then `just changelog-refs` (adds the
  commit item to every line of `## Unreleased`), then the changelog heading, then the amend. One
  sentence says why: the SHA-1 is known only once the line's commit is on `main`, and the release
  adds it in the version commit, so no follow-up commit on `main` is ever needed for it.
- "The version PR on top of a stack", step 1: see open question 1; write what the owner answers.
- "Release notes", "Writing": the references at the end of a changelog line are not copied into
  the notes (the section already forbids ticket numbers; name the references explicitly).

### 3. New script `scripts/changelog_refs.py`

A Python script in the style of `scripts/version.py` and `scripts/release_notes.py` (module
docstring, `argparse`, `main() -> int`, a `git(*arguments)` helper, `from __future__ import
annotations`). It uses `git` only, no forge API, no network.

Behaviour:

- Reads `CHANGELOG.md` at the repository root and finds the `## Unreleased` section (up to the next
  `## ` heading). Each bullet starts with `- ` and continues on the indented lines below it.
- Refuses to run, exit 1 with a message, when `CHANGELOG.md` has uncommitted changes
  (`git status --porcelain -- CHANGELOG.md` not empty): blame line numbers would not match.
- For each bullet, `git blame --porcelain -L <n>,<n> HEAD -- CHANGELOG.md` on the bullet's first
  line gives the commit that added the line. Its short form is `git rev-parse --short <sha>` (7
  characters unless git needs more to stay unique).
- Checks that commit is on the base: `git merge-base --is-ancestor <sha> <base>`, where `<base>` is
  the option `--base` (default `origin/main`). A commit not on the base stops the script, exit 1,
  naming the line's first words and the commit, and nothing is written.
- Writes the item:
  - the bullet ends with a reference group (a final `( ... )` whose items each start with one of
    `CR-`, `PR #`, `MR !`, `issue `): insert `commit <short>, ` right after its `(`;
  - otherwise: append ` (commit <short>)` at the end of the bullet.
- A bullet whose group already starts with `commit ` is left as it is, so a second run changes
  nothing.
- Writes the file only when every bullet succeeded, with LF line endings (as `use_lf` in
  `scripts/version.py`: Python writes CRLF on Windows otherwise). It never stages or commits; the
  release amends the version commit with `CHANGELOG.md` as today.
- Prints one line per bullet changed (`commit <short>: <first words>`) and a count; an empty
  `## Unreleased` prints "No line to update" and exits 0.
- Mark the code with `@implements_req <new SwRS-ID>` (section 6).

### 4. `justfile`

- New recipe, near `bump-version`:

  ```just
  # Add the commit of each line of ## Unreleased in CHANGELOG.md (release, before the changelog heading).
  changelog-refs BASE="origin/main":
      uv run --no-sync python scripts/changelog_refs.py --base "{{ BASE }}"
  ```

- `release-tests`: add `test/build/test_changelog_refs.py` to its pytest list. It is then run by
  `just check` (which depends on `release-tests`) and the `static` CI job, on Linux and Windows.
- Run `just format` after the edit.

### 5. `CONTRIBUTING.md`, "How to Release" (mechanics)

- Step 2: "one user-facing line" gains "ending with its references (see 'CHANGELOG line' in the
  pull-request guideline)".
- Step 3: before "Add a `## X.Y.Z - YYYY-MM-DD` heading", run `just changelog-refs`, which adds the
  commit of each line of `## Unreleased`; then the heading; then the existing amend command, which
  already includes `CHANGELOG.md`.

### 6. Requirements (okfreq)

Read the requirements guideline, the okfreq baseline and `requirements/guidelines/project.guidelines.md`
("During a change") first.

- New SwRS with `okfreq new`, scope `rendering-core`, `derives_from: StRS-MDOKFSTUDIO-CORE-007`
  (proposed, not approved: no owner re-approval). Title in the spirit of "The release adds the
  commit of each changelog line"; normative behaviour: the release script SHALL add to each line
  of `## Unreleased` the short SHA-1 of the commit on the base that added it, as the first item of
  the line's reference group, and SHALL write nothing when a line's commit is not on the base or
  the file has uncommitted changes. Scenarios: nominal (group present, group absent), boundary
  table (already has a commit, not on base, dirty file, empty section).
- `implemented_in_files: scripts/changelog_refs.py`, `tested_in_files:
  test/build/test_changelog_refs.py`; markers `@implements_req` in the script, `@tests_req` on each
  test.
- `just requirements-update`; a dated entry in `requirements/tiers/log.md`.

### 7. Current `## Unreleased` lines

See open question 2: the lines already there use `(#475)`, `(#469)`, `(#479)` or nothing. Apply the
owner's answer in this pull request.

### 8. This pull request's own CHANGELOG line

The change is `docs` + `build` tooling (the script is release tooling, not a user-facing change of
the extension): no `## Unreleased` line; the template's Changelog box says "No user-facing change".

## Evidence

Tests, in a new `test/build/test_changelog_refs.py` (pytest, the temporary-repository style of
`test/build/test_release.py`: `git init` in `tmp_path`, commits made by the test, the script run by
`subprocess` with `cwd` in that repository and `--base` a local branch). Each test fails on the
current code, where the script does not exist.

1. A bullet whose group is `(CR-463 change-bar-tooltip, PR #476, issue #413)` becomes
   `(commit <sha of the commit that added it>, CR-463 change-bar-tooltip, PR #476, issue #413)`.
2. A bullet with `(MR !476, issue PROJ-12)` gets the commit as first item (GitLab and Jira
   notation recognised).
3. A bullet with no group gets ` (commit <sha>)` at its end.
4. A bullet on three physical lines: the SHA is the commit of its first line, written at the end
   of its last line, even when a later commit added the PR item on the last line (two commits, as
   a pull request merged by rebase lands them).
5. Two bullets added by two commits each get their own SHA.
6. A second run changes nothing (byte-identical file).
7. Uncommitted change to `CHANGELOG.md`: exit 1, file unchanged.
8. A line whose commit is not on `--base` (a commit on a side branch): exit 1, the message names
   the line, file unchanged.
9. Empty `## Unreleased`: exit 0, "No line to update", file unchanged; the sections under older
   version headings are never touched (asserted in test 1 too).
10. The written file has LF line endings (the test runs on the Windows `static` job too).

These tests use prepared changelog text on purpose: the script reads whatever changelog it is run
on, and the cases (dirty file, foreign commit) cannot be held by the shipped file. No check reads
the shipped `CHANGELOG.md` (Q4: no enforcement).

Gates: `just check` (formatting, `release-tests` with the new tests and
`test_guideline_isolation.py` on the edited guidelines, `requirements-lint`), `just
requirements-update`, then `just preflight` (on Windows, the static stage).

Scenario steps for the reviewer, in a scratch clone (not on `main`):

1. `git switch -c try origin/main`, then `just changelog-refs`: every line of `## Unreleased` gets
   `commit <sha>` and each SHA is the one `git log --format=%h -S"<first words>" -- CHANGELOG.md`
   shows for that line.
2. `just changelog-refs` again: `git diff` shows no further change.
3. Edit `CHANGELOG.md` without committing, run it: it refuses.

No CI job is added or changed; the new tests run in the existing `static` job (Linux and Windows)
through `just check`. No host or default matrix: the script does not depend on the host beyond the
line endings, which test 10 covers.

## Out of scope

- Any check (static CI, `release-notes-check`, PR template lint) that enforces the format (Q4).
- A chantier change (cards, `ship`) to add the PR/MR number automatically (Q5).
- Rewriting the GitHub-specific parts of the guidelines that this change does not touch (the
  section "GitHub issues", the `gh` commands of "Draft until mergeable", of the release steps and
  of the screenshots). New text written by this change is forge-neutral; existing text stays.
- `.github/PULL_REQUEST_TEMPLATE.md` (its Changelog box keeps its wording).
- The process guideline `change-requests-lifecycle.guidelines.md` ("Code" bullet unchanged; Q5).
- Adding commits to lines under already released version headings.

## Writer's choices (within the answers, for the Chief of Staff to confirm or overturn)

- The script name and recipe: `scripts/changelog_refs.py`, `just changelog-refs`, option `--base`
  default `origin/main`.
- The commit is the blame of the bullet's first line (a later edit of the last line, such as the
  PR item, does not move it).
- Several linked issues: one `issue` item each, in the order the author writes them.
- `CONTRIBUTING.md` "How to Release" gets the command in its mechanics (steps 2 and 3); the rule
  itself stays in the two guidelines (Q5).
- The release notes drop the references (one clause in "Release notes", "Writing").

## Open questions

1. **The version PR on top of a stack.** The commits of the stack are not on `main` when the
   version commit is made, and a rebase merge on GitHub rewrites every SHA-1 (GitLab's
   fast-forward merge keeps them). So `just changelog-refs` refuses there (its lines' commits are
   not on `origin/main`), and a SHA taken from the branch would be wrong after the merge.
   Recommended answer: in the stacked way, the lines of the stack's own pull requests are released
   without their commit item (the script run with `--base origin/main` adds it to the lines already
   on `main`, and an option `--skip-missing` leaves the others as they are, listed in its output);
   the guideline says so in "The version PR on top of a stack". Alternative: the stacked way is not
   used when the owner wants every SHA, and the release takes the default way (stack first).
2. **The lines already in `## Unreleased`.** Three end with a bare `(#475)`, `(#469)`, `(#479)`,
   the others have no reference. Recommended answer: this pull request rewrites them to the new
   format (`(PR #475)` etc., the CR and issue items added where the CR records show them, the PR
   number found with `git log` on the line's commit), so the next release reads one format. Without
   it, the script appends a second group, `(#475) (commit 1a5b98b)`.
