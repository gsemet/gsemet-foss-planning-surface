# Release chantier v0.16.0: the card cleanup and the live view

## Goal

Ship the work of this batch as a new version (`01-intent.md`, `intake/request.md`; card-cleanup-Q5,
2026-11-27: the inventory's last reading, then steps 1 to 3 of the cleanup, with a new version).
The release change request sits on top of the batch's stack (answer 2). It makes one pull request
that leaves v0.16.0 ready to tag, then publishes it on the owner's approvals.

Version: 0.16.0, from 0.15.1 (`just release minor`).

## What it delivers

- chantier 0.16.0: the commit `release: v0.16.0` merged on `main`, the tag `v0.16.0` pushed, and
  the GitHub release `v0.16.0` with the reviewed notes and their images.
- The release folder `docs/release-notes/<today>-v0.16.0/` (`release-notes.md`, `tweet.md`, the
  images).
- The claims file `evals/results/claims-v0.16.0.md`.

Other projects run the plugin from this checkout: the new version is what makes their cached CLI
match the new cards.

## How

By the project's own procedure: `CONTRIBUTING.md` "Release", `docs/release-process.md`, and
`evals/README.md` "Before a release: the claims". Those files rank over this summary of them.

### 1. The claims file, with no campaign (answer 4)

No eval campaign runs before this release (the owner's word, card-release-Q1: « B. Aucun avant »).
A real run on a test project comes later, and a fault it finds takes a patch release.

`evals/results/claims-v0.16.0.md`, as the evals README says:

- `# Claims of v0.16.0`, then `Since v0.15.1, at <sha7 of origin/main>. Runs: none.`, then one line
  saying that no eval ran for this release, on the owner's word (2026-11-27).
- One row per `feat:` and `fix:` commit of `v0.15.1..HEAD` on the release branch before the version
  commit, `main`'s commits and the stack's, each by its sha on that branch.
- With no run, each claim is `scenario only` (a named check of `just scenario` or `just test`
  proves it; the evidence names the unit and case) or `not exercised` (evidence empty). No claim is
  `exercised`.

The file is committed in the release pull request: it is new, so it is added with `git add` before
`just release minor`, whose commit otherwise holds only tracked changes and `docs/release-notes/`.

### 2. The release folder

On a new branch from the top change request's branch, `docs/release-notes/<today>-v0.16.0/`, as
`docs/release-process.md` says, from the commits `v0.15.1..HEAD` and from the specifications, pull
requests and evidence of the change requests they come from (this batch's, and those merged on
`main` since v0.15.1).

- `release-notes.md`: the header and links at `v0.16.0`; two to four highlights, chosen by the
  Driver from what ships (this batch holds the card cleanup and the live view's wider, resizable
  columns; `main` already holds other work since v0.15.1); Smaller changes; All fixes; For
  contributors with its `**Not exercised by an eval.**` bullet listing every claim that is not
  `exercised`. Every `feat:` and `fix:` commit appears exactly once. N is counted before the
  version commit.
- Removals and behaviour changes go on `Removed:` or `Changed:` lines in the visible part. The
  Driver reads them from the merged diffs, and at least checks these planned ones: help topic names
  removed; the new spellings of the role commands (the old names still run); `chantier live` writes
  its column widths and, with the mouse on, a plain drag no longer selects text; on macOS the
  configuration folder moves and `chantier login` is run again; the breaking change of the role
  cards already on `main` (`feat(cards)!`).
- `tweet.md`: three posts.

### 3. The images

All from this batch, as `docs/release-process.md` says: the board, the batch's `STATUS.md`,
`report.md` and `conversation.md` in this change request's folder (the Chief of Staff writes both
when it joins the batch and refreshes them until the pull request is prepared), and CLI output.

One diagram goes in the notes, on the owner's word (card-release-Q2: « B. Schéma du serveur »):
`docs/surface-server.svg` as this batch leaves it (`tui-mouse-resize` corrects its `chantier live`
box), rendered from the release branch's head. No other docs diagram.

Each source is anonymised and passes `uv run --script scripts/release_notes.py --scan <page>...`,
each image is rendered with headless Chrome at no more than 1200x600, read before it is committed,
and shows no username and no home folder (floor rule 8). If headless Chrome is missing, the Driver
hands back a `blocked question:`; nothing replaces it.

### 4. The version commit and the pull request

`just release minor` bumps the version, runs `just check` and commits `release: v0.16.0`; it pushes
nothing. The Driver pushes, opens the pull request (its body shows `release-notes.md`, then
`tweet.md`, each after a `---` rule, and says that no eval ran before this release), runs
`ship <cr> <pull request link>` before `handback ready`, and hands back ready: it waits for the
merge. A change inserted in the stack later makes the release pull request update its notes, its
claims and its count.

### 5. After the merge

The owner merges the stack by rebase, the release commit last. No release grant is recorded: each
irreversible action waits for the owner's approval.

1. `just tag` from the main checkout, run by the steering session once approved, never by the
   Driver.
2. `--prepare`, then `gh release create v0.16.0 --verify-tag ...`, once approved
   (`CONTRIBUTING.md` "Release", step 5).
3. The owner posts the thread from `tweet.md`; no agent posts it.

## Out of scope

- Any eval campaign before publishing (answer 4).
- Any change of code, cards, topics or diagrams: the pull request changes only the files
  `just release` touches, the release folder and the claims file. A fault found while preparing the
  release is handed back as a fix.
- The `review_by: 0.16.0` field some help topics carry: the code and the tests check only its
  format, so it blocks nothing; this change request does not edit it.
- Steps 4 to 7 of the cleanup plan.

## Evidence

- `just check` passes at the pull request's head; it runs `scripts/release_notes.py --check`.
- The head commit is `release: v0.16.0` and the version files say 0.16.0.
- A list, in the pull request or in `work/`, maps each `feat:` and `fix:` commit since v0.15.1 to
  its place in the notes.
- CI green on the pull request. As the top of the batch's stack, the long gate `scenario` run
  locally on Windows (`chantier gate <cr> scenario`) at the pull request's head (`AGENTS.md`).
- Done when `gh release view v0.16.0` shows the release and the tag is on the
  `release: v0.16.0` commit.
