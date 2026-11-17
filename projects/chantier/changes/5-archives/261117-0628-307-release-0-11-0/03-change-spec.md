# Version PR for chantier v0.11.0

## Goal

One PR on top of batch-22's stack that makes v0.11.0 ready to tag: the release folder
`docs/release-notes/<today>-v0.11.0/`, the claims file `evals/results/claims-v0.11.0.md`, and the
commit `release: v0.11.0` made by `just release minor`. The user asked for it on 2026-11-17
("livrer à la fin de cette nuit une stack and PR de release tout en haut"). The user merges it;
that merge is the go for CONTRIBUTING.md "Release" steps 4 and 5, each irreversible step on the
user's approval.

## What the Driver does

1. Read CONTRIBUTING.md "Release", docs/release-process.md and evals/README.md "Before a release:
   the claims", then the commits since `v0.10.0` up to the top of the stack under this CR (the
   branch of the CR just below, not only `origin/main`: CR-302 to CR-306 are not merged yet), and
   the CRs they come from (their folders in the planning surface's `4-batch/3-done/`,
   `4-batch/2-actives/` and `5-archives/`: each `03-change-spec.md`, PR description and evidence).
2. Write `evals/results/claims-v0.11.0.md` as evals/README.md says: one row per `feat:` and `fix:`
   commit since v0.10.0 up to the stack's top. No campaign has run for v0.11.0 yet: the user chose
   (2026-11-17) the two quick campaigns, `real-direct` in stack mode and `real-foreman` in
   parallel mode, to run at the desk after the stack under this PR is merged and before the user
   merges this PR; `full` and `copilot` are not run for this release (the user's word). So today a
   claim proved by a named check of `just scenario` or `just test` is `scenario only`, else `not
   exercised`; the `Runs:` line says the campaigns are pending. Note that `9eaef4a` is a `wip:`
   commit (the short startup core): it is not a `feat:` row, but say in the PR body that it changes
   how every role starts and that the campaigns are what bring it to the test.
3. Write `docs/release-notes/<today>-v0.11.0/` as docs/release-process.md says: `release-notes.md`
   (header, links at `v0.11.0`, two to four highlights, Smaller changes, folded All fixes and For
   contributors with its `**Not exercised by an eval.**` bullet; every `feat:` and `fix:` commit
   once; N counted before the version commit), `tweet.md` (three posts), and the images it cites.
   Images come from the merged CRs' own evidence (the docs pictures under `docs/web-board/`, the
   CRs' PR screenshots) or CLI output; anonymised as docs/release-process.md says (no local user
   path, no username: use made-up paths). None invented. No docs SVG diagram.
4. Run `just release minor` (0.10.0 to 0.11.0, runs `just check`, commits `release: v0.11.0`;
   pushes nothing), then push and open the PR on the branch of the CR below; its body shows
   `release-notes.md`, then `tweet.md`, each after a `---` rule, and says the campaigns are pending
   and that the claims file and notes get their results before the user merges.
5. As the top CR of the stack, run the local Windows `just scenario` (`chantier gate`) at the PR's
   head, as AGENTS.md says.
6. Hand back ready with the PR. The Driver never runs `just tag`, `gh release create` or anything
   after the merge. When a CR below changes (a restack), the notes and claims are updated by the
   release Driver started again.

## Out of scope

- Running the eval campaigns (they need the user at the desk).
- Tag, forge release, thread (CONTRIBUTING.md "Release" steps 4 to 6).
- Any code or card change: the version PR changes only the version files `just release` touches,
  the release folder and the claims file.

## Evidence

- `just check` passes at the PR's head (it runs `scripts/release_notes.py --check`).
- `git log --oneline -1` at the head is `release: v0.11.0`; the version files say 0.11.0.
- A list in the PR body (or `work/`) mapping each `feat:` and `fix:` commit since v0.10.0 to its
  place in the notes.
- The local `just scenario` at the head (the top of the stack).
