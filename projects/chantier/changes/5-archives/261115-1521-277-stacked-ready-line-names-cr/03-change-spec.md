# Change Specification: the ready line of a stacked CR names the CR it waits on

Short name: `stacked-ready`. No issue (origin: verbal, from the study of batch-18's real eval runs
of 2026-11-15, retro point R12).

## Goal

When a Driver hands back `ready` and the CR reads **PR in draft**, the line the CLI prints says
what the Driver needs and nothing false: whether its own PR is a draft or out of draft **as the
forge has it** (as `ship` last read it), and the **CR, with its PR, that it waits on**, not the
forge's base branch. In run 1 (stack) the line read `PR in draft: it waits on main` for PRs that
were out of draft and stacked on another CR; four Drivers stopped on it and in batch-18 one Driver
put its PR back to draft because of it.

## Today

`skills/chantier/scripts/cli/src/chantier/commands/driver.py`, `_ready_lines()` (called by
`_record_ready()` from `handback ... ready`):

- line 1, to the Foreman: `[driver <cr>→foreman] hand-back <word><tail>`;
- line 2, when the word is `PR in draft`: `<cr> PR in draft: it waits on <pr_base_of(...)>`, or,
  for a prepared release, `<cr> PR in draft: the release PR <pr> waits on <base>`.

`pr_base_of()` (`stacks.py`) is the forge's base as `ship` recorded it (`c.pr_base`), else the
plan. The word comes from `ready_word()`: a PR out of draft over a CR not out of draft also reads
`PR in draft`, so the line printed "PR in draft" for an out-of-draft PR and named `main` (a stale
or unretargeted forge base) instead of the CR below. The status views already name the right CR:
`draft_waits()` in `stacks.py`, used by `status/words.py` `state_label()` (`🟤 PR in draft, waits
for <cr>`) and `notify()`.

## What changes

### 1. The CLI's ready line (`commands/driver.py`, `stacks.py`)

Line 2 of a `PR in draft` hand-back becomes, for a CR:

```
<cr> PR in draft: its PR <pr> is <state>; it waits on <what>
```

and for a prepared release (`prepared`):

```
<cr> PR in draft: the release PR <pr> is <state>; it waits on <what>
```

- `<state>`, from the record's `c.pr_draft` (the forge's state as `ship` last read it):
  - `pr_draft is True`: `a draft on the forge`;
  - `pr_draft is False`: `out of draft on the forge`;
  - `pr_draft is None` (no `ship` read it, a failed read, an older record):
    `of unknown draft state (draft not read: ship <cr> <pr>)`; the word stays `PR in draft`, as
    today (never ahead of the forge).
- `<what>`, the same answer as `draft_waits()` (one source for the line, the label and the
  STATUS files; the line and `🟤 PR in draft, waits for <x>` never disagree):
  - a CR of the batch: `<cr-id> (<its pr>)`, or `<cr-id> (no PR yet)` when that CR has no PR
    recorded;
  - a base branch that is no CR of the batch (today `draft_waits` returns the branch itself):
    `the branch <branch> (no CR of this batch)`;
  - nothing under it (`its turn out of draft`): the clause reads `it waits for its turn out of
    draft`.
- The forge's base branch is no longer printed on this line (it stays in `ship`'s own output,
  `(base <b>, head ...)`, and in `notify()`).
- A PR recorded out of draft never reads `it waits for its turn out of draft`: `ready_word` gives
  it `PR in draft` only when something under it, or its non-default base, holds it, and that is
  what the line names.

Implementation is the Driver's: for instance `draft_waits()` keeps its string contract for the
views and a sibling in `stacks.py` returns the waited `CrEntry` (or the branch, or none) so the
line can add its PR; `_ready_lines()` no longer calls `pr_base_of()`. Line 1 (to the Foreman) is
unchanged: its tail is the Driver's own note. The `ready to merge` and `ready locally` lines are
unchanged. The `; it was blocked: <reason>` suffix still goes on the last line.

### 2. Cards (`skills/chantier/references/`)

- `driver.md`, the hand-back bullet (around lines 425-434, "the CLI prints which state the CR is,
  ready to merge, PR in draft or ready locally"): add that for `PR in draft` the printed line says
  its PR's draft state on the forge and the CR (and PR) it waits on, and that this line asks for no
  change on the forge: it is not a reason to turn the PR to draft or ready, to retarget it, or to
  stop; the hand-back is done. (Turning a PR back to draft stays governed by the existing rules: a
  CR sent back for a round, a rebase that needs a long gate, a stack being changed.)
- `concepts.md`, the **PR in draft** entry (line 24): today "whose PR is open and a draft"; say it
  is a PR that is a draft, or out of draft over a CR that is not (a stack, a PR on another CR's
  branch), and that its hand-back line names its own draft state and the CR it waits on.
- No agent file (`agents/`, `com.github.copilot/agents/`) changes.

### 3. Docs

`scenario/README.md` (the line on the three words of a ready CR, around line 162): if it describes
what the `PR in draft` hand-back names, say "its PR's draft state and the CR (and PR) it waits
on". No other doc names the line's text.

## Decisions carried from `02-answers.md`

- The request's scope stands as written: the line says the draft state as the forge has it, and
  for a stacked PR names the CR (and PR) below it that it waits on, not the forge's base branch.
- Planned for the next batch (parallel), before the next release.
- Implementation detail is the agents'.

## Out of scope

- The state words themselves (`ready locally`, `PR in draft`, `ready to merge`), `ready_word()`'s
  rule, the icons, the board and the CR pane: unchanged (no `STATUS.json` field changes, so no
  pane screenshot is due).
- `notify()`'s now line in a CR's `STATUS.md` (`PR in draft: <pr> on <base>, waits for <cr>.`)
  and `state_label()`: unchanged (see the open question).
- The Driver's own hand-back note (`draft on <base>: waits for <what>`) and line 1.
- `ship`'s reading of the forge, and refreshing a stale `pr_base`.

## Evidence

Changes to the CLI and the cards: `just check` passes (Linux, macOS, Windows) and the pipeline's
`just scenario (ubuntu-latest)` job is green at the PR's head before its PR. Not a change to
`hooks/` or `types/`: no `just mod`. No new unit test is needed (the line is the scenario's).

Scenario (`scenario/run_scenario.py`):

1. `base_from_pr` (around lines 4362-4368, a parallel batch, q's PR out of draft on p's branch, p's
   PR a draft): the hand-back's line 2 is
   `<q> PR in draft: its PR <qlink> is out of draft on the forge; it waits on <p> (<plink>)`, and
   does not contain `waits on <pb>`; the label and `STATUS.md` checks stay as they are.
2. `ready_words` step 3 (lines 5964-5967, b's PR a draft on a's branch): line 2 starts
   `<b> PR in draft: its PR <b's pr> is a draft on the forge; it waits on <a> (<a's pr>)`.
3. `ready_words` step 4 (lines 5972-5975, c out of draft over the draft b): line 2 reads
   `its PR <c's pr> is out of draft on the forge; it waits on <b> (<b's pr>)`; the label still
   waits for b (the line and the label agree).
4. `ready_words` step 9 (lines 6091-6095, a prepared release a draft on the top CR's branch):
   line 2 reads `the release PR <pr> is a draft on the forge; it waits on <top> (<top's pr>)`.
5. A new check reproducing run 1, in `ready_words` (a stack a, b, c): c's PR out of draft with the
   forge's base recorded as `main` (`forge_base(..., "main")`, `ship`), b not out of draft: c's
   hand-back line 2 reads `out of draft on the forge; it waits on <b> (<b's pr>)` and contains no
   `waits on main`.
6. A new check: a CR waited on with no PR recorded reads `(no PR yet)` (for instance c handed back
   while b is working with no PR, or b's `pr` dropped by `edit_cr`).
7. A new check: a PR with no recorded draft state (`edit_cr(..., drop=("pr_draft",))` before the
   hand-back) reads `of unknown draft state (draft not read: ship ...)` and stays `PR in draft`.
8. Every existing `ready to merge` / `ready locally` hand-back check passes unchanged.

## Open questions for the user

1. The `STATUS.md` now line of a PR in draft (`notify()`: `PR in draft: <pr> on <base>, waits for
   <cr>.`) also starts with "PR in draft: <pr>" and names the forge's base; it can read, like the
   old line, as "this PR is a draft on main". Should it take the same wording (its PR's draft state
   on the forge, the CR and PR it waits on, no base) in this CR, or stay as it is (this spec leaves
   it unchanged, as the request names only the ready line)?
