# Change Specification: Release v1.13.0

## 1. What

Release the work on `main` since `v1.12.1`, by the project's own procedure:
`.agents/guidelines/release-process.guidelines.md` (rules, release folder, steps, notes, thread, the
version PR body), and "How to Release" and "Recovery and Release Notes" in CONTRIBUTING.md. That
procedure rules; this specification only fixes what is settled (02-answers.md).

## 2. Scope

- Everything on `main` since `v1.12.1`: the lines of `CHANGELOG.md` `## Unreleased`, plus any missing
  line of a `feat` or `fix` PR (a gap of that PR, procedure step 2).
- The default way of the procedure: the stack is already on `main`. No stack tops the version PR; its
  base is `main`.
- Version **1.13.0** (a minor release: `main` holds new features since 1.12.1). Check it against what
  `just bump-version` computes and report a difference. The owner is asked to agree
  (release113-Q1); an answer in 02-answers.md replaces this number.
- Procedure step 4: the heavy run of `main` HEAD. At the time of writing it is run
  [45958381383](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/45958381383) on
  `b1e23cc`. Read the result of each of `integration`, every `acceptance` shard and `stress`; a merge
  since then starts the step again. The version commit comes only after all are green.
- A red job: one re-run for a flake, as the procedure says. A job still red is reported to the
  steering session with its diagnosis; the fix is a change request of its own, not a commit of this
  release.

## 3. The notes

By the procedure. The notes and the thread come from `## Unreleased` and the reports of the changes.
A feature clip that already exists under `docs/demo-video/clips/` for a feature of this release may
be a highlight; no new clip is made. No docs diagram, unless the owner says yes (release113-Q2).

## 4. Approvals

The owner merges the version PR; no agent merges and auto-merge is never enabled. The irreversible
steps after that merge are asked with the merge go, one by one (`order approve`). The announcement
thread stays a draft for the owner. The issue comments of step 9 keep the procedure's one owner
approval. Nothing is posted on issue 547 without it.

## 5. Done

The version PR ready (CI green, containing `main`); after the owner's merge: the tag `v1.13.0`, the
GitHub release with notes and images, both registries serving 1.13.0 (checks of record of step 6),
and `04-report.md` and `retro.md` in this CR's folder.

## 6. Open questions

None that stops the preparation: release113-Q1 (version) and release113-Q2 (docs diagram) have the
default above.
