# Change Specification: the board sees a stacked PR that landed with its base

## Goal

When the user merges a stack on the forge, a PR merged into the branch of another CR of the batch
lands on the default branch with that CR's PR. The board's PRs page sees this on the forge and
`status` tells the Chief of Staff to record it (`order merged <cr>`), instead of "not landed,
record nothing until <base> lands" when the base has already landed. The batch-24 case: PR 288
(CR-330) merged at 18:58:14Z into `chantier/batch-24/cr-329-cr`, CR-329's PR then merged into
main (content on main as 75a748e8), and `status` still said CR-330 had not landed; the record kept
CR-330 ready and `forge-stack create` was refused (HTTP 422 on the merged PR).

The decisions are those of `02-answers.md` (A1 to A5); none is the user's beyond putting the CR in
the batch.

## What changes

### 1. The PRs page judges "landed" from its own forge read (A1, A2)

`skills/chantier/scripts/cli/src/chantier/board/prs.py`:

- A new pure function, for example `landed_with(row, by_cr) -> dict | None`, where `by_cr` maps a
  CR id to its row of the same read (all rows, also those whose CR the record holds merged). For a
  row merged on the forge:
  - `merged_into.cr` is None (merged into a branch that is no CR's branch): not a stacked merge;
    the function returns None and nothing changes for it (today's `into main` line).
  - `merged_into.cr` is a CR `B`: the PR has landed when `B`'s row is `merged` on the forge, with a
    `merged_at` equal to or later than this row's `merged_at`, and `B` itself either merged into a
    branch that is no CR's (then it returns `{"cr": B, "at": B's merged_at}`) or landed the same
    way into a third CR's branch (follow the chain to its end; the CR returned is the one whose PR
    reached the non-CR branch, and `at` its merge time). A cycle, a missing row, a base not merged,
    a base merged before this PR, or a missing `merged_at` on either side: None (not landed).
  - Times compare as instants (parse the ISO 8601 strings the forge read gives), not as text.
- `row_of`/`answer` add the result to each row as `"landed_with"` (None when not merged, not
  stacked or not landed), computed after all rows of the read are built. No new forge call: the
  read (`forge_read.read`, GitHub and GitLab alike) already gives each PR's `state`, `base` and
  `merged_at`. No git read, no patch-id (A2).

### 2. The signal carries it (A3)

`skills/chantier/scripts/cli/src/chantier/board/seen.py`, `signal`:

- An entry for a row with `landed_with` adds two fields: `"landed_with": <cr>` and
  `"landed_at": <time>`; an entry without keeps today's fields only (old lines stay readable).
- The "once" key becomes (batch, CR, landed or not): a stacked merge first read not landed, then
  read landed after its base merged, writes one second line, once; any later read writes nothing.
  A merge read landed at its first read writes one line. The module docstring says so.
- The board still records nothing, writes nothing else, and this stays its only write
  (`board-seen.jsonl`, local, ignored by git). AGENTS.md's limits hold unchanged.

### 3. `status` prints the landed line (A3, A4)

The choice of entry and the text of each line live in
`skills/chantier/scripts/cli/src/chantier/board/seen.py`, in one new function (for example
`lines(entries, batch, open_crs) -> list[str]`, taking what `seen.read` returns), which also moves
there the text of today's two lines. `commands/batch_status.py`, `_seen_lines`, only reads the file,
names the unreadable lines as today, and calls it: `batch_status.py` (379 lines today, and another
CR of the batch grows it) stays at or under 400 lines with this change.

- Per open CR of the batch, an entry with `landed_with` wins over one without; else the first
  entry, as today.
- The landed line:
  `board saw merged: <cr> <pr> into <base cr>'s branch at <merged_at>, landed with <landed_with>
  at <landed_at>; for the Chief of Staff: order merged <cr>`
- The other two lines are unchanged (`into <branch> at <t>; for the Chief of Staff: order merged
  <cr>`, and the `not landed, tell the user, record nothing until <base cr> lands` one).
- The line stops printing once the CR is recorded merged or cancelled, as today. Nothing is
  written by `status`.

### 4. The cards and the docs

- `skills/chantier/references/chief-of-staff.md` (the paragraph at "A `board saw merged: <cr> …`
  line in `status`"): a line that says `landed with <other cr>` is a merge to record, like the
  `into <branch>` one (`order merged <cr>`, then the Foreman's line in Foreman mode); only a line
  that ends `not landed …` is not one to record (tell the user, wait), with one exception added
  in the same paragraph: on GitLab, a fold (`forge-stack show` prints `folded into <cr below>`) is
  recorded at once by the fold rule below, whatever the board's line says. This keeps the paragraph
  consistent with the fold rule (`chief-of-staff.md`, "When the user merges a middle MR anyway",
  today lines 1096-1098). No agent file changes (the
  role's contract is in the card); `foreman.md` is unchanged (the Foreman does nothing with the
  line).
- `docs/web-board.md` (the "The signal" paragraph): the landed case, its line, and the second line
  once a stacked merge is later seen landed.
- `scenario/README.md` and AGENTS.md: unchanged (no new scenario step; AGENTS.md's "appends one
  line" still describes each write).

## Out of scope

- `forge-stack create` and its HTTP 422: it already skips a CR recorded merged
  (`forge_stack_gh.py`, `ENDED`); once the Chief of Staff records the merge, it no longer touches
  the PR (A5).
- A stacked PR that never landed (its base merged before it): today's "not landed" line stays;
  re-targeting it is the user's.
- A merge with no PR merged on the forge (a push to main), a patch-id check on main (the user,
  retro-Q2: out of scope), or any git read by the board or `status` (A2).
- The board's page text and the PRs row's `disagrees` words (the row still says "merged on the
  forge, not recorded yet: tell the Chief of Staff", which holds).
- Who records: the board and the Foreman record nothing; the Chief of Staff does (A4).
- The CR board pane (`hooks/register.tsx`) and `STATUS.json`: untouched, so no screenshot is owed.

## Evidence

Unit tests, in `skills/chantier/scripts/cli/tests/test_board_prs.py`, few and parametrized,
in-process, on the existing `Board` fixture (fake forge rows with `state`, `base`, `merged_at`):

1. One parametrized test on the signal written for a PR merged into CR-0's branch
   (`chantier/b/cr-0`), by CR-0's forge row:
   - CR-0 merged into `main` later: one line with `landed_with` CR-0 and its `landed_at`;
   - CR-0 merged into `main` at the same instant: landed;
   - CR-0 merged into `main` earlier: one line with no `landed_with`;
   - CR-0 open: no `landed_with`; then CR-0 merged into main later, read fresh: exactly one second
     line with `landed_with`; a third read writes nothing;
   - a chain (CR-2 into CR-1's branch, CR-1 into CR-0's branch, CR-0 into main, each later):
     CR-2's line `landed_with` CR-0; CR-0 recorded merged in the record still counts.
2. The existing `test_status_names_what_it_cannot_read_and_prints_only_the_open_crs_of_its_batch`
   (or a parametrization of it) gains an entry pair for one CR, not landed then landed: `status`
   prints only the landed line, word for word as in section 3; the existing not-landed line is
   unchanged for a CR with no landed entry.
3. The existing tests stay green unchanged (an entry with no `landed_with` keeps today's fields).

`just test` stays within AGENTS.md's time limit. `batch_status.py` stays at or under 400 lines.

Unproved: the forge gives `merged_at` to the second. When the user's stacked merge puts the
stacked PR and its base in the same second, the rule counts it landed (A1's "at the same time"),
but whether the forge can also show a base merged before the stacked PR in that same second (a
base that did not carry it) is not proved by the unit tests, which use made-up times. Trial: the
next stacked merge on the real forge (the batch's next stack); the Driver names it in the PR's
Known gaps ("same-second ordering of a stacked merge unproved; trial: the next stacked merge"),
so the ready line quotes it.

Gates AGENTS.md requires for this change (CLI `src/`, cards, docs):

- `just check` passes in the worktree at the rebased head the Driver pushes (Linux, macOS,
  Windows in CI).
- `just eval-dry-run` there, before the first push (the change is under the CLI's `src/`).
- The pipeline's `just scenario (ubuntu-latest)` job green at the PR's head (a CLI and card
  change). Windows coverage: if this CR is on top of the batch's stack, `chantier gate` runs
  `just scenario` locally at its head before the user merges.
- No `just mod` (no `hooks/` or `types/` change); no pane screenshot (the pane is untouched).

## Open questions

None for the user: the behaviour choices are settled in `02-answers.md` (A1 to A5 by the Chief of
Staff; retro-Q2 by the user: no patch-id check, the Chief of Staff records).
