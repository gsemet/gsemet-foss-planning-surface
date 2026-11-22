# Version PR for chantier v0.15.0

## Goal

One PR, from an up-to-date `main`, that makes v0.15.0 ready to tag. It holds three things:
- the release folder `docs/release-notes/<today>-v0.15.0/`;
- the claims file `evals/results/claims-v0.15.0.md`;
- the commit `release: v0.15.0`, made by `just release minor`.

The user merges it. That merge is the go for CONTRIBUTING.md "Release" steps 4 and 5, and each
irreversible step still waits for the user's approval.

## What the Driver does

1. Read the rules: CONTRIBUTING.md "Release", docs/release-process.md, and evals/README.md
   "Before a release: the claims". Then read the commits since `v0.14.0` on `main`
   (`git log --no-merges v0.14.0..origin/main`) and the CRs they come from (the archived and done
   folders of the planning surface's `projects/chantier/changes/`, merged since v0.14.0: each
   one's `03-change-spec.md`, PR description and evidence).
2. Write `evals/results/claims-v0.15.0.md` as evals/README.md says, one row per `feat:` and
   `fix:` commit since v0.14.0.
   - Runs: real-foreman 2026-11-22 run 4, whose report is
     `evals/results/real-foreman-2026-11-22-run4.md` (on `main` once PR #436 is merged; if it is
     not merged yet, read it from that PR's branch `eval/real-foreman-2026-11-22-run4`).
   - A claim that run shows at work is `exercised`, with the report's evidence; one proved by a
     named check of `just scenario` or `just test` is `scenario only`; any other is
     `not exercised`.
3. Write `docs/release-notes/<today>-v0.15.0/` as docs/release-process.md says:
   - `release-notes.md`: the header and links at `v0.15.0`; two to four highlights, from these
     (merge or reorder them for the reader): the web board as the place to steer (Inbox, History,
     Dashboard, Help, the batch graph and Kanban, the Griller's discussion panel); the CLI run
     remotely through the surface server, with a private key and a public read-only key
     (`serve`, `webui`, `login`, `live`); the forge followed for you (a hub that reads only what
     is awaited, typed waits, the writer that publishes the plan); Smaller changes; folded
     "All fixes"; folded "For contributors" with its `**Not exercised by an eval.**` bullet;
     every `feat:` and `fix:` commit since v0.14.0 exactly once, N counted before the version
     commit.
   - `tweet.md`: three posts.
   - The images it cites: from batch-30's merged PRs' evidence, the release CR's `report.md` and
     `conversation.md`, the batch's `STATUS.md` and CLI output; anonymised as
     docs/release-process.md says, no local user path, no username, no key; rendered with
     headless Chrome. If Chrome is missing, hand back `blocked question:`. No docs SVG diagram.
     Nothing invented.
4. Run `just release minor`: 0.14.0 to 0.15.0, `just check`, commit `release: v0.15.0`; it pushes
   nothing. Then push and open the PR, whose body shows `release-notes.md`, then `tweet.md`, each
   after a `---` rule, and names the eval run.
5. Hand back ready with the PR. The Driver never runs `just tag`, `gh release create`, or
   anything after the merge.

## Out of scope

- Tag, forge release and thread (CONTRIBUTING.md "Release" steps 4 to 6). After the user's
  merge, the steering session runs steps 4 and 5 on the user's approval; step 6 is the user's.
- Any code or card change. The version PR changes only the version files that `just release`
  touches, the release folder and the claims file.

## Evidence

- `just check` passes at the PR's head; it runs `scripts/release_notes.py --check`.
- `git log --oneline -1` at the head is `release: v0.15.0`, and the version files say 0.15.0.
- A list, in the PR body or in `work/`, maps each `feat:` and `fix:` commit since v0.14.0 to its
  place in the notes.
- No `just scenario`: the PR changes no CLI, card or scenario.
