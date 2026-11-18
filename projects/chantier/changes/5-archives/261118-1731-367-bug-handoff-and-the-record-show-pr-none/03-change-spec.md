# Change Specification: a release CR's merged PR stays in its record

Short name: `release-pr-recorded`

## Goal

A release CR's version PR shows in its record the same way any CR's PR does: `handoff`, `status`,
`STATUS.json`/`STATUS.md`, `delivery.md`, the closed batch's record and the board all name it,
before and after its merge. Today they say `PR: none` / `-` once the release PR is merged (CR-352,
v0.12.0, PR 322; CR-366, v0.13.0, PR 331).

## The cause (found, read-only)

The PR is not lost by the Driver, and the cards are not at fault. The CLI records it and then
clears it:

1. The Release driver of CR-366 ran `ship CR-366 https://github.com/gsemet/chantier/pull/331`. The
   batch's `events.jsonl` holds the `ship` event (2026-11-18T15:45:42Z, `pr`, `base: main`,
   `head 543b0d0`), and `STATUS.json`'s steps show "Shipped ... pull/331". `ship`
   (`commands/delivery.py`, `b.touch(..., pr=args.pr, ...)`) wrote `CrEntry.pr` as for any CR.
2. The Chief of Staff's `order merged CR-366` (order O-16) runs `_merged` in
   `commands/orders_apply.py`. For a release CR that calls `release_merged` in
   `skills/chantier/scripts/cli/src/chantier/rails_release.py`:

   ```python
   b.touch(c, status="queued", pr=None, pr_base=None, pr_draft=None, head=None,
           merged_pr=c.pr or "the release PR")
   ```

   It moves the link from `pr` to `merged_pr` on purpose: the merge is the go for the rest of the
   procedure (`release_go` reads `merged_pr`), and a later attempt (after a fix) opens a PR of its
   own. `batch.json` now holds CR-366 with `pr: null`,
   `merged_pr: https://github.com/gsemet/chantier/pull/331`.
3. Every reader that shows a CR's PR reads `c.pr` only, never `merged_pr`:
   - `commands/facts.py` (`handoff`): `PR: {c.pr or 'none'}`, and the stack line
     `PR {x.pr or 'none'}`.
   - `commands/batch_status.py` `_cr_row` (`status`): `{c.pr or '-'}`.
   - `status/views.py`: `cr_view` (`STATUS.json`'s `pr`, hence `STATUS.md`), `_row` (the batch's
     `STATUS.json` rows), `_done_rows` (the merged list's rows from `3-done`).
   - `status/steps.py`: the "Merged" step's note (`c.pr or ""`).
   - `lifecycle/stages.py` `_delivery`: `delivery.md`'s `- PR: {cr.pr or 'none'}`. Both archived
     release CRs show `- PR: none`.
   - `history.py` `cr_entry`: the closed batch's record (`"pr": c.pr`).
   - `board/crs.py` `_row`: the board's CR rows (`"pr": link_of(c.pr)`).

So the fix goes in the CLI (answers: "the CLI if it ... drops it").

## What changes

### 1. One reading of "the CR's PR to show" (`core/records.py`)

Add to `CrEntry` a method `shown_pr()`. It returns the CR's open PR (`pr`) when there is one,
else the release PR its `order merged` recorded (`merged_pr`), and `None` when neither is an
http(s) link. `merged_pr` may hold the fallback text `"the release PR"` (set when no PR was
recorded), which is not a link and is never shown as one. Use the same test as
`board/crs.py`'s `link_of` (`https?://`). Do not import the board from core; repeat the
one-line regex, or move `link_of` into core and import it from there in `board/crs.py`.

`pr` and `merged_pr` keep their meanings. `release_merged` does not change: `pr` stays "the open
PR of the current attempt", which `release_go` (`c.pr and not granted` -> `merge`),
`order confirm` (`if c.pr:` refuses), `commands/driver.py` (`prepared`), `stacks.py`, the gate
and the forge readers still rely on.

### 2. The readers that show a PR use `shown_pr()`

Replace `c.pr` with `c.shown_pr()` where a CR's PR is shown, and only there:

- `commands/facts.py`: the `PR:` line of `handoff` (`cr_facts`) and the `PR` of each line of
  `stack_lines` (what `stack` and `take stack` print). These are the lines agents read. A
  release PR already merged (the shown PR comes from `merged_pr`, `c.pr` empty) carries a mark
  there: `PR: <link> (merged)` in `handoff`, `PR <link> (merged)` in a stack line. An open PR
  shows as today, with no mark.
- `commands/batch_status.py` `_cr_row`: the PR column of `status`, the plain link with no mark
  (as `STATUS.json` and the board show it).
- `status/views.py`: `cr_view` (`pr` and its number), `_row` (`pr`), `_done_rows` (`pr`).
  `_past` reads it back from `STATUS.json` and needs no change.
- `status/steps.py`: the note of the "Merged" step.
- `lifecycle/stages.py` `_delivery`: the `- PR:` line of `delivery.md`. `done_cr` writes
  `delivery.md` (external planning surface only). For a release CR, `done_cr` runs at
  `handback <cr> ready <version>` once no unmerged PR is recorded (the "released" branch of
  `commands/driver.py`, `prepared = c.kind == "release" and bool(c.pr)` false, around lines
  233-237), not at `order merged`. By then `pr` is empty and `merged_pr` holds the link, so the
  shown PR is the link.
- `history.py` `cr_entry`: `pr` of the closed batch's record (the board's PRs page shows a closed
  batch's rows read from the forge, judged against nothing, and never signalled).
- `board/crs.py` `_row`: `pr` (the board's cards, panel, timecards, merged list, receipt).
  Also add to the row `"pr_merged": True` when the shown PR is the release PR its merge
  recorded (`c.pr` empty, `merged_pr` a link), else `False`.

Leave the logic readers on `c.pr` as they are: `rails_release.py`, `orders_apply.py`
`_confirm`, `commands/driver.py`, `commands/driver_checks.py`, `commands/delivery.py`,
`commands/forge_stack.py`, `commands/forge_stack_gh.py`, `commands/forge_base.py`,
`commands/intake.py`, `stacks.py`, `status/gate.py`, `status/words.py` (`CI` vs `Round`), and
the forge hub (`hub/cycle.py` `state_of`, `to_read`).

### 3. The forge readers do not report the release PR's merge again

Between `order merged` and the release's end, the release CR's status is `queued` (then
`working`/`blocked`/`ready` through the tag and publish steps), not `merged`. A forge read that
sees PR 331 merged while the record says `queued` would count it as a merge the record does not
hold and would append a `merged` line to `forge-journal.jsonl`. The Chief of Staff would then
record it with `order merged`, which runs `release_merged` a second time, with `c.pr` empty, and
writes `merged_pr = "the release PR"` over the real link.

- The forge hub: unchanged. It keeps reading `link_of(c.pr)`: it reads the open release PR (the
  record holds it since `ship`) and never the merged one, which the record already holds merged.
- The board's PRs page (`board/prs.py`): with item 2 the live batch's rows (`_in_order`) include
  the merged release PR. `why_not` returns `None` for a row whose CR has `pr_merged` true when
  the forge shows it merged (`c.get("pr_merged")`, so the hub's dicts, which have no such key,
  are judged as today). So the page shows the row as merged with no disagreement, and
  `journal.merged_events` writes nothing for it.

### 4. The board's open-PR lists leave a merged release PR out (`board/web/`)

A row with `pr_merged` true has a PR that is already merged, while the CR's state can still be
`queued`, `working`, `blocked` or `ready` until the release ends. The board shows its link on the
CR's card, panel, timecard and merged list, but leaves it out of every open-PR list and count:

- `board/web/js/views/home-prs.js`: the home's open PRs
  (`rows.filter((c) => c.pr && c.state !== 'merged')`) also leaves out `c.pr_merged`.
- `board/web/js/views/registry.js`: the PRs nav count
  (`crsOf(...).filter((c) => c.pr && c.state !== 'merged')`) also leaves out `c.pr_merged`.
- `board/web/js/model/semantics.js` `mergeOrder`: the open CRs with a PR
  (`c.pr && isOpen(c)`) also leave out `c.pr_merged`, so the merge order does not list it.

Each test is one predicate. Write it once, for example `openPr(c)` in `semantics.js`, and use
it in all three. Before editing, read `board/web/DESIGN.md` (AGENTS.md). It holds the board's
visual rules and tokens and names none of these lists today. The change draws nothing new and
adds no token, so `DESIGN.md` stays true as it is. If the Driver finds that it does describe one
of these lists, it updates it in the same PR.

### 5. Cards and docs

No card changes. `driver.md` (release part) already has the Driver record the release PR with
`ship`, and the Driver of CR-366 did. No `docs/` page describes `merged_pr`. If the Driver finds
one that says a merged release CR shows no PR, it corrects it in the same PR.

## Decisions carried from `02-answers.md`

- A release CR's version PR is recorded in its record as any CR's PR is, so `handoff`, `status`,
  `STATUS.json`, the board and the forge hub see it: items 1 to 3. The hub sees the open release
  PR, as it does today. Once the PR is merged the record holds it merged, so the hub has nothing
  left to read (item 3).
- The fix goes where the cause is: the CLI, since `release_merged` moves the link out of `pr`
  and the readers read only `pr`. No card changes (item 5).
- Already-archived release CRs (CR-352, CR-366) are not rewritten: no migration, and no step of this change edits their
  files or a closed batch's record. CR-366 is
  still in `4-batch/3-done/` of batch-27. Its `batch.json` entry already holds `merged_pr`, so
  any `status` refresh after this change is merged and loaded regenerates CR-366's
  `STATUS.json`/`STATUS.md` from `batch.json`, and they name PR 331. So does `status`. At
  `close`, batch-27's closed record (`history.py` `cr_entry`) is built from `batch.json` and
  names PR 331. Both are regenerated from the record, not migrated: no step of this change
  writes them. The one file already written, CR-366's `delivery.md` (written at its
  `handback ... ready v0.13.0`), stays `- PR: none`. CR-352's archive
  (`5-archives/261118-0810-352-release-0-12`) and batch-24's closed record are not touched.
- A test covers it, the fix being in the CLI (see Evidence).
- (spec critic) The board leaves a row whose PR is already merged (`pr_merged`) out of the open-PR
  lists and counts: the home's open PRs, the PRs nav count, the merge order. `board/web/` and
  its `DESIGN.md` are in scope (item 4).
- (spec critic) `handoff` and `stack` show a release PR already merged as `PR: <link> (merged)`;
  `status`, `STATUS.json` and the board show the plain link (item 2).

## Out of scope

- Changing what `pr` and `merged_pr` mean, or `release_merged` itself.
- Rewriting the archives of CR-352 or CR-366, or a closed batch's record.
- Keeping more than the last merged release PR when a release has more than one attempt that
  merged: `merged_pr` holds the latest, as today.
- Any new drawing on the board: the merged release PR shows as any PR link does (item 4 only
  filters lists).
- Any change to the CR board pane's code (`hooks/register.tsx`). The pane draws `pr`: the
  batch table's `prCell(r.pr)` (around line 991, from `status/views.py` `_row`), the merged list's
  `prCell(p.pr)` (around line 1006, from `_done_rows` and `_past`) and the CR page's
  `PR #<n>` link (around line 1089, from `cr_view`). It will now show a merged release PR there.
  That changes what the pane draws through the `STATUS.json` fields of `status.py`, so the
  AGENTS.md rule applies. The PR's Deliverables carry one screenshot of the pane from a real
  Claude Code session running the PR's head, with a release CR merged showing its PR, captioned
  with the head's SHA (seven characters). Until it is there, the PR's Known gaps names "no
  screenshot of the pane from a real session", so the ready line quotes it and the Chief of Staff
  asks the user for one. `STATUS.json`'s `pr` keeps its shape (`{"url", "number"}` or `null`).

## Evidence

Tests (`skills/chantier/scripts/cli/tests/`, in-process, on a prepared state; few and
parametrized, as AGENTS.md asks):

- In `test_batch_end.py`, extend
  `test_a_release_crs_order_merged_and_the_drop_of_a_live_cr_pause_nothing`, or add one test next
  to it built on the same `started`/`patch`/`merge` helpers. Use a release CR with
  `pr="https://example.com/pr/1"`, then `order merged`. Assert that:
  - `batch.json` holds `pr: null` and `merged_pr` set to the link (unchanged behaviour);
  - `handoff <cr>` prints `PR: https://example.com/pr/1 (merged)`;
  - `status` prints the CR's row with the plain link in place of `-` (no mark);
  - the CR's `STATUS.json` has `pr.url` set to the link;
  - `release go <cr> --note ...` still answers `go` with "the release PR ... was merged" (the
    logic still reads `merged_pr`, and the empty `pr` does not refuse it).
  Parametrize on a second case: `merged_pr` holding `"the release PR"` (no PR recorded). There
  `handoff` prints `PR: none` and `STATUS.json`'s `pr` is `null`.
- `delivery.md` of a released CR, in `test_external_archive.py` (its external planning surface
  setup): a release CR with a PR recorded, `order merged`, then `handback <cr> ready v1.0.0`
  (released). The CR's `3-done` folder holds `delivery.md` with the line
  `- PR: https://example.com/pr/1`.
- A stack line: a stack batch whose release CR's PR is merged. `stack` prints
  `PR https://example.com/pr/1 (merged)` on its line, and an open CR's line shows its link with
  no mark.
- In `test_board_prs.py`: one case where a live batch's release row has `pr_merged: True`, the
  CR's state `queued` and the forge showing the PR merged. `why_not` gives `None` and the answer
  appends nothing to `forge-journal.jsonl`. Pair it with the existing case where a non-release
  row merged on the forge, not in the record, still gives `merged` (it must keep passing).
- `test_forge_hub.py` keeps passing unchanged (the hub still reads `c.pr` only).
- The board's open-PR lists (item 4): the repository has no JS tests for the board's model, so
  the proof is in the Driver's evidence, on a board served from the PR's head. Use a prepared
  batch with a merged release CR (`pr_merged` true) and an open CR with a PR. The release CR's
  card shows its PR. The home's open PRs, the PRs nav count and the merge order list only the
  open CR. Give one capture that has been looked at, or the served JSON plus the three counts.
- The pane: the screenshot (see Out of scope), or the Known gaps line.

Gates (AGENTS.md):
- `just check` passes in the worktree at the rebased head before the first push, and
  `just eval-dry-run` too (the change is under the CLI's `src/`).
- The pipeline's `just scenario (ubuntu-latest)` is green at the PR's head. `scenario/run_scenario.py`
  reads `merged_pr` (around line 6730) and must keep passing. No scenario step is owed: the
  tests above cover the behaviour.
- No change to `hooks/` or `types/`: `just mod` is not owed.

No host or default matrix: the behaviour does not depend on the host or on a configured value
(`archive_in_pr` only changes `delivery.md`'s third line, not its `PR:` line).

## Open questions

None for the user.
