# A restack re-checks PR bodies' SHAs and evidence links

## Goal

After a restack (or any rebase), no PR body keeps a proof claimed at a SHA that left the head's
history, and no evidence image hangs on a commit the forge may drop. `ship`, which every moved CR
already runs after its push, names both, and the cards say how images are attached and what to do
with one found after a move.

## Why `ship` missed them in batch-24

`delivery._stale_body_shas` (in `skills/chantier/scripts/cli/src/chantier/commands/delivery.py`)
skips any line of `work/pr-body.md` that holds `STALE` or `carried from`. CR-345's body had, on one
line, "Screenshots of the new tabs, at `15359cc` (carried from `7f07565` ...)", and on the next lines
images linked as `https://github.com/<owner>/<repo>/blob/<15359cc full>/docs/...png?raw=true`.
After the next restack, `15359cc` left the head's history: the caption line was skipped whole, and
the Test plan line "after at `15359cc` (carried from `7f07565`)" too. The image lines themselves
are only caught when no `carried from` sits on them; their stale link is a broken image in waiting,
whatever the caption says.

## What changes

Shares `delivery.py`'s `ship` with ship-refuses-foreign-commits (same batch): no ordering needed,
expect a rebase.

### CLI: `ship`'s stale body lines (`commands/delivery.py`)

`_stale_body_shas(repo, c, wt, head)` keeps its signature, its read-only git and its output
place (`off:` lines of `ship`, logged in the `ship` event's `off`). Per line of `work/pr-body.md`:

1. **Images first, on every line** (`STALE` and `carried from` lines included). The image links of
   the line are the targets of Markdown images (`![...](<url>)`, the URL up to the first space or
   `)`) and the `src` of HTML `<img>` tags. When a token of those URLs is a commit of the worktree
   not in the head's history (the same test as today's `_stale_token`), the line gives one off line:
   `pr-body.md line <n> shows an image from <sha7>, not in <head7>'s history: attach it with the
   forge's CLI: <text>` (`<text>` cut at `HISTORY_CHARS` as today), and no second off line for that
   line.
2. **Then the text**, unless the line holds `STALE` (left out, as today): the tokens of the line,
   the image URLs removed, are checked as today, except a token that follows `carried from` after
   any spaces and at most one backtick (e.g. `carried from 7f07565`, ``carried from `7f07565` ``),
   which is the SHA the proof came from and may lie outside the head. A remaining token that is a
   commit not in the head's history gives today's line, unchanged in wording:
   `pr-body.md line <n> names <sha7>, not in <head7>'s history: <text>`.

The occurrence right after `carried from` is removed from the text before the scan (exempted by
position, not by value); the same SHA elsewhere on the line is still checked. `_stale_token(line,
wt, head)` takes that stripped text; the digits-only rule and the `rev-parse` / `merge-base
--is-ancestor` test stay as they are. The docstring of `_stale_body_shas` says the new exemptions.
No new command, no forge read, no new event kind or field.

### Cards

- `skills/chantier/references/pr-template.md`:
  - the bullet "Each proof names the SHA it covers": a carried proof is written `at <head7>
    (carried from <sha7>)`: it names the head it now stands at and the SHA it came from; only the
    SHA after `carried from` may lie outside the head's history, and `ship` names any other.
  - the before/after bullet (Deliverables visuals): images are attached with the forge's CLI as
    driver.md says; a link into a commit of the CR's branch (`/blob/<sha>/`,
    `raw.githubusercontent.com/.../<sha>/`, GitLab's `/-/raw/<sha>/`) is not an upload: a restack
    drops that commit and the forge may delete it.
  - the `Verified at` box comment (around line 196): the carried form reads `at <head7> (carried
    from <sha7>)`.
- `skills/chantier/references/driver.md`:
  - "The evidence" bullet (around line 350): add one sentence: an image linked into a commit of the
    CR's branch is not an upload; one found after a move (`ship`'s `off: pr-body.md line <n> shows
    an image from …`) is attached by the Driver with the forge's CLI, using the same image file
    (from `work/`, or from `git show <old>:<path>` while the commit is still local), before the PR
    turns ready; it is captured again only when a Verifier is due anyway (a conflict, a refused
    carry).
  - The SHA-marks sentence (around line 652, "changes SHA marks to `carried from <sha7>`"): the
    mark becomes `at <head7> (carried from <sha7>)`.
  - The Review box sentence (around line 698, "a pass carried over a clean rebase is `carried from
    <sha7>`"): the pass is `at <head7> (carried from <sha7>)`.
  - The CR driver's clean-rebase paragraph (around lines 707-710, "Mark each proof … as `carried
    from <sha7>`"): write the mark as `at <new head7> (carried from <sha7>)`, and attach the image
    files `ship` names as the evidence bullet says (no long gate, no Verifier: the paragraph's rule
    stands).
  - The Stack driver's moved-PR paragraph (around line 819, "update the PR's Test plan SHAs"):
    "update the PR body's SHAs (the Test plan, the `Verified at` box, the evidence captions and
    image links)". The restack paragraph (around lines 916-919, "After a restack, `ship` names the
    lines …"): add "and the images (`shows an image from …`), attached as the evidence bullet says",
    before "run `ship` again until no such line remains".
- No other card changes; no change on `agents/` or `com.github.copilot/agents/` (no role's
  contract moves into an agent file).

### Scenario (`scenario/run_scenario.py`, the step after `# `ship` names the PR body lines whose SHA a restack made stale`, around lines 5057-5105) and `scenario/README.md` (around line 165)

- In the first body written (line 5077), the existing `carried from {old[:7]}` line stays
  unnamed (the token follows `carried from`). Add three lines and widen the check:
  - `Verified at {old[:7]} (carried from {old[:7]})`: named, as `line <n> names {old[:7]}`
    (the claimed SHA is stale; the same SHA after `carried from` is exempted by position only);
  - `![after at {old[:7]}](https://github.com/acme/demo/blob/{old}/a.png?raw=true) carried from {old[:7]}`:
    named, as `line <n> shows an image from {old[:7]}` and with "attach it with the forge's CLI";
  - `STALE <img src="https://raw.githubusercontent.com/acme/demo/{old}/b.png">`: named, as
    `line <n> shows an image from {old[:7]}` (an HTML image, on a `STALE` line).
  The check then expects four named lines (line 3, the `Verified at` line, the Markdown image line,
  the `STALE` HTML image line), and still none for the bare `carried from`, the `STALE` text and
  non-commit lines. Its label says so.
- The fixed body (line 5087) keeps passing: no line named.
- README, line 165: "(`carried from` and `STALE` lines left out)" becomes "(the SHA after `carried
  from` and the text of `STALE` lines left out; an image, Markdown or HTML, linked into a commit
  outside the head named on any line, `STALE` lines included)".

No unit test is added: `ship`'s stale body lines are covered in the scenario today, and
`just test`'s time budget stays untouched.

## Decisions carried from `02-answers.md`

- The re-check is `ship`'s; no new CLI tool, no forge read.
- `carried from` exempts only the SHA right after it, by position; `STALE` lines stay exempt for
  their text.
- A stale image link is named on every line, with its own off line.
- Images are attached with the forge's CLI; a link into a branch commit is not an upload; one found
  after a move is attached by the Driver from the same file; it is captured again only when a
  Verifier is due anyway.
- Proof in the scenario's existing step, no new unit fixture.
- No depends.json entry with ship-refuses-foreign-commits; a rebase is expected.

## Out of scope

- Reading the posted description on the forge (`ship` reads `work/pr-body.md`, which the cards
  already require to be what is posted).
- Rewriting or uploading images from the CLI; checking that an attachment URL still resolves.
- Images in the CR's archive or a release body; links to files at `main` or a tag (no commit SHA of
  the CR's branch).
- Bodies already merged (CR-345 is merged; nothing is backfilled).

## Evidence

- `just check` passes (lint, types, `just test`) in the worktree at the pushed head.
- `just eval-dry-run` passes (the change touches the CLI's `src/`).
- `just scenario` passes (ubuntu-latest in the pipeline; the top CR of the batch also locally with
  `chantier gate`), with the widened check: four lines named in the first body (line 3, the stale
  claimed SHA on the `Verified at … (carried from …)` line, the Markdown image linked into the old
  head, the HTML image on a `STALE` line), none for the SHA after `carried from`, the `STALE` text
  and the non-commit token; none once the body is fixed; the digits-only check unchanged.
- The Inspector reads the card edits listed under Cards (pr-template.md and driver.md) against this
  specification; their wording names `ship`'s two off-line forms exactly as `delivery.py` prints
  them.
