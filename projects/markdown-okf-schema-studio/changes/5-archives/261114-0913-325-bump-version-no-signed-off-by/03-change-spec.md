---
title: Change spec - the version commit carries no Signed-off-by trailer
cr: number given at Open (batch-04)
date: 2026-11-14
issue: none
priority: P1
source: v1.9.0 release check (2026-11-14); runs before the v1.9.1 release CR
blast_radius: 1 (release tooling only: the version script, its test, its SwRS and the release docs)
inspector: Sonnet
rounds: 2
---

# Change spec: the version commit carries no Signed-off-by trailer

> [!NOTE]
> Intent: `01-intent.md`. Answers: `02-answers.md`. Read code and guidelines on `origin/main`
> (`4b45b45e` at the time of writing). Rules: `.agents/constitution.md`, `AGENTS.md`,
> `requirements/guidelines/project.guidelines.md` ("During a change").

## Problem

`just bump-version` and `just version X.Y.Z` run `scripts/version.py`, which creates the version
commit with `git commit --only -s -m "chore: version X.Y.Z" -- <files>`. The `-s` adds a
`Signed-off-by` trailer with the committer's identity. Rule 6 of
`.agents/guidelines/git-commit-message.guidelines.md` forbids this: no `Signed-off-by` unless a
human asks for it, and never through `git commit -s`. The v1.9.0 version commit (`4b45b45e`)
carries `Signed-off-by: Gaetan Semet <...>` because of this.

The script, the tests, the requirement and the docs all describe the commit as "signed-off", so
they all say the same wrong thing:

| Place | Text to change |
| --- | --- |
| `scripts/version.py` | module docstring (line 1), the `-s` argument of `git commit`, the message `Created signed-off commit: ...` |
| `justfile` | comments of `bump-version` and `version` ("create a signed-off version commit") |
| `test/build/test_release.py` | docstrings of `test_automatic_version` and `assert_version`; the assertion `"Signed-off-by: Release Test <test@example.com>" in message` |
| `requirements/tiers/swrs/rendering-core/SwRS-MDOKFSTUDIO-CORE-075.md` | `description`, normative text and nominal scenario ("one signed-off commit") |
| `CONTRIBUTING.md` ("How to Release", step 3) | "create a signed-off commit with subject `chore: version X.Y.Z`, using `git commit -s`" |

## Target behaviour

1. `scripts/version.py` creates the version commit without `-s`. The commit message is exactly
   the subject `chore: version X.Y.Z`, with no trailer. Everything else stays: same five files
   with `--only`, staged work left alone, no tag, the identity checks (`git var
   GIT_AUTHOR_IDENT` / `GIT_COMMITTER_IDENT`) kept because a commit needs an identity.
2. The script prints `Created commit: chore: version X.Y.Z` (no "signed-off"). Its docstring and
   the two justfile comments say "version commit" with no "signed-off".
3. `test/build/test_release.py` checks the opposite: the version commit message has no
   `Signed-off-by` line (for example `assert "Signed-off-by:" not in message`). This assertion
   must fail on `origin/main` and pass after the change. The docstrings drop "signed-off".
4. SwRS-MDOKFSTUDIO-CORE-075: "one signed-off commit" becomes "one commit `chore: version X.Y.Z`
   with no `Signed-off-by` trailer" in the description, the normative text and the nominal
   scenario (and the generated `rendering-core/index.md` line through `just requirements-update`).
   This is a small normative change; it gets a dated entry in `requirements/tiers/log.md`.
5. `CONTRIBUTING.md`, "How to Release" step 3: the commands "create a commit with subject
   `chore: version X.Y.Z`" with no mention of `git commit -s` or sign-off.
6. Check `.agents/guidelines/release-process.guidelines.md`: it does not mention sign-off today
   (checked at `4b45b45e`). Its step 5 puts the release notes folder in the same
   `chore: version X.Y.Z` commit, which the release driver does by amending the version commit.
   Add one short sentence there that the version commit carries no `Signed-off-by` (do not amend
   with `-s`), so the amend does not bring the trailer back.
7. A last search (`rg -i 'signed-off|signoff|commit -s'` outside `.agents/changes/`, `out/` and
   `node_modules/`) finds nothing left, except the commit guideline's own rule 6.

## Decisions (Chief of Staff, by judgment, no user impact)

- The trailer is dropped, not made optional: no flag or setting to sign off. A human who wants it
  can still amend the commit by hand, as rule 6 allows.
- The v1.9.0 commit `4b45b45e` stays as it is: no history rewrite on `main`.
- The commit guideline (`git-commit-message.guidelines.md`) does not change: its rule 6 is already
  right. The attribution rule (rule 7, `Assisted-by`) was checked as the intake asked: the version
  commit message is written by the script, not by an AI, so the script adds no `Assisted-by`
  either. Whether the release driver adds one when it amends the commit with the notes is the
  release process's matter and is not changed here.
- Commit type for the change: `build` (local release tooling), no scope.

## Out of scope

- The other release fixes of batch-04 (Open VSX publish, flaky real-window steps) and the v1.9.1
  release itself.

## Acceptance checks

- On a scratch repository (the `repository` fixture of `test/build/test_release.py`),
  `scripts/version.py` and `scripts/version.py 1.2.3` create a commit whose full message
  (`git log -1 --format=%B`) is only `chore: version X.Y.Z`, with exactly the five versioned files.
- The new "no `Signed-off-by`" assertion fails on `origin/main` and passes on the branch.
- `rg -i 'signed-off|signoff|commit -s'` (excluding `.agents/changes/`, `out/`, `node_modules/`)
  matches only rule 6 of `git-commit-message.guidelines.md`.
- `just check`, `just requirements-lint` and `just requirements-update` pass; the log entry for
  SwRS-MDOKFSTUDIO-CORE-075 is present.
- `just preflight` passes.
- PR body per `.github/PULL_REQUEST_TEMPLATE.md`; Impacts says "no visible change" (release
  tooling only).
