# Version PR for chantier v0.13.0

## Goal

One PR, from an up-to-date `main`, that makes v0.13.0 ready to tag. It holds three things:
- the release folder `docs/release-notes/<today>-v0.13.0/`;
- the claims file `evals/results/claims-v0.13.0.md`;
- the commit `release: v0.13.0`, made by `just release minor`.

The user merges it. That merge is the go for CONTRIBUTING.md "Release" steps 4 and 5, and each irreversible step still waits for the user's approval.

## What the Driver does

1. Read the rules: CONTRIBUTING.md "Release", docs/release-process.md, and evals/README.md "Before a release: the claims".
   Then read the commits since `v0.12.0` on `main` (`git log --no-merges v0.12.0..origin/main`) and the CRs they come from. Those are the archived and done folders of the planning surface's `projects/chantier/changes/`, merged since v0.12.0; read each one's `03-change-spec.md`, PR description and evidence.
2. Write `evals/results/claims-v0.13.0.md` as evals/README.md says, with one row per `feat:` and `fix:` commit since v0.12.0.
   - No eval ran for this release (the user's word).
   - A claim proved by a named check of `just scenario` or `just test` is `scenario only`.
   - Every other claim is `not exercised`.
3. Write `docs/release-notes/<today>-v0.13.0/` as docs/release-process.md says:
   - `release-notes.md`, holding:
     - the header, and links at `v0.13.0`;
     - two to four highlights: the forge hub and `chantier watch` (a merge on the forge wakes the steering session; the notes say it is on Claude Code only, observed once and still on trial, unproved on Copilot, as the host references mark it; the claims file and the `**Not exercised by an eval.**` bullet name it), switching a Foreman batch to direct mode with CRs in flight, and the CR archive kept out of the PR unless the project says yes (named as a change of default);
     - Smaller changes;
     - folded "All fixes";
     - folded "For contributors", with its `**Not exercised by an eval.**` bullet;
     - every `feat:` and `fix:` commit since v0.12.0 exactly once, with N counted before the version commit.
   - `tweet.md`: three posts.
   - The images it cites:
     - they come from batch-26's and batch-27's merged PRs' evidence, the release CR's `report.md` and `conversation.md`, the batch's `STATUS.md` and CLI output (`status`, `watch`);
     - they are anonymised as docs/release-process.md says, with no local user path and no username;
     - they come from headless Chrome. If Chrome is missing, hand back `blocked question:`.
   - No docs SVG diagram. Nothing invented.
4. Run `just release minor`. It goes from 0.12.0 to 0.13.0, runs `just check`, and commits `release: v0.13.0`; it pushes nothing.
   Then push and open the PR. Its body shows `release-notes.md`, then `tweet.md`, each after a `---` rule. The body says that no eval campaign ran before this release (the user's word, 2026-11-18).
5. Hand back ready with the PR. The Driver never runs `just tag`, `gh release create`, or anything after the merge.

## Out of scope

- Tag, forge release and thread (CONTRIBUTING.md "Release" steps 4 to 6). After the user's merge, the steering session runs steps 4 and 5 on the user's approval; step 6 is the user's.
- Any code or card change. The version PR changes only:
  - the version files that `just release` touches;
  - the release folder;
  - the claims file.

## Evidence

- `just check` passes at the PR's head; it runs `scripts/release_notes.py --check`.
- `git log --oneline -1` at the head is `release: v0.13.0`, and the version files say 0.13.0.
- A list, in the PR body or in `work/`, maps each `feat:` and `fix:` commit since v0.12.0 to its place in the notes.
- No `just scenario`: the PR changes no CLI, card or scenario.
