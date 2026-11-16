# Version PR for chantier v0.10.0

## Goal

One PR from an up-to-date `main` that makes v0.10.0 ready to tag: the release folder
`docs/release-notes/<today>-v0.10.0/`, the claims file `evals/results/claims-v0.10.0.md`, and the
commit `release: v0.10.0` made by `just release minor`. The user merges it; that merge is the go for
CONTRIBUTING.md "Release" steps 4 and 5, each irreversible step on the user's approval.

## What the Driver does

1. Read CONTRIBUTING.md "Release", docs/release-process.md and evals/README.md "Before a release:
   the claims" (the rules), then the commits since `v0.9.0` on `main`
   (`git log --no-merges v0.9.0..origin/main`) and the CRs they come from (the archived folders
   in `.agents/changes/5-archives/`, merged since v0.9.0: each `03-change-spec.md`, PR description
   and evidence).
2. Write `evals/results/claims-v0.10.0.md` as evals/README.md says: one row per `feat:` and `fix:`
   commit since v0.9.0. The runs are the two of 2026-11-15 (real-foreman run 2 and real-direct
   run 3, their reports in `evals/results/`); a claim they brought is `exercised`, a claim proved by
   a named check of `just scenario` or `just test` is `scenario only`, else `not exercised`.
3. Write `docs/release-notes/<today>-v0.10.0/` as docs/release-process.md says: `release-notes.md`
   (header, links at `v0.10.0`, two to four highlights, Smaller changes, folded All fixes and For
   contributors with its `**Not exercised by an eval.**` bullet; every `feat:` and `fix:` commit
   since v0.9.0 exactly once; N counted before the version commit), `tweet.md` (three posts), and
   the images it cites. Images come from batch-18's real run: its archive
   (`5-archives/batches/batch-18.json`, `.md`), this CR's `report.md` and `conversation.md`, CLI
   output; rendered and anonymised as docs/release-process.md says (headless Chrome; if it is
   missing, hand back `blocked question:`). No docs SVG diagram (the user's word). None invented: a
   highlight with no real capture uses a CLI call and its output.
4. Run `just release minor` (0.9.0 to 0.10.0, runs `just check`, commits `release: v0.10.0`; pushes
   nothing), then push and open the PR; its body shows `release-notes.md`, then `tweet.md`, each
   after a `---` rule. The body says that the `full` campaign did not run before this release (the
   user's word: the two runs of 2026-11-15 are this release's evals).
5. Hand back ready with the PR. The Driver never runs `just tag`, `gh release create` or anything
   after the merge.

## Out of scope

- Tag, forge release, thread (CONTRIBUTING.md "Release" steps 4 to 6): after the user's merge, the
  steering session runs steps 4 and 5 on the user's approval; step 6 is the user's.
- Any code or card change: the version PR changes only the version files `just release` touches,
  the release folder and the claims file.

## Evidence

- `just check` passes at the PR's head (it runs `scripts/release_notes.py --check`).
- `git log --oneline -1` at the head is `release: v0.10.0`; the version files say 0.10.0.
- A list in the PR body (or `work/`) mapping each `feat:` and `fix:` commit since v0.9.0 to its
  place in the notes.
- No `just scenario`: the PR changes no CLI, card or scenario.
