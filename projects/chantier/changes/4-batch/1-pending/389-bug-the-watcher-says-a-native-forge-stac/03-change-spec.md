# Change Specification: a native forge stack's merges are told landed

## Goal

When the user merges a GitHub native stack in one go, every PR of the stack lands on the default
branch, but GitHub reports each PR above the bottom one as merged into the branch below it. Today
the forge hub and the board's PRs page then write, for each of those PRs, a `merged` journal line
with no `landed_with`, and `status` and the watcher print "not landed, tell the user, record
nothing until <cr below> lands", forever. Following that line would leave the stack's merges
unrecorded (13 of 14 at batch-28's end). After this change, a PR of the stack merged into a branch
below it whose merge is on the default branch is told as the bottom one is: `landed with <bottom
cr>`, `for the Chief of Staff: order merged <cr>`.

## What happened (the facts this specification rests on)

Read on the forge (read-only) on 2026-11-20 for batch-28's stack:

- #335 (CR-369, the bottom) merged into `main` at 09:29:53Z; #342 (CR-370) merged into CR-369's
  branch at 09:29:54Z; each PR above it one second after the one below, up to #354 at 09:30:08Z.
- `prs.landed_with` (`skills/chantier/scripts/cli/src/chantier/board/prs.py`) calls a stacked PR
  landed only when each base below it was merged at the same instant or later. A native stack
  merge goes bottom-up, so each base is merged one second *before* the PR it carries: the rule
  returns `None`, and the journal (`forge-journal.jsonl`, lines 14 to 26) holds 13 `merged` lines
  with `into_cr` and no `landed_with`.
- GitHub's GraphQL `PullRequest.mergeCommit.oid` of each stacked PR is a commit of `main`
  (#342: `958ac5a6`, #354: `18b251d7`, both in `main`'s history; also #336 of the earlier part of
  batch-28: `7ee43d0d`). The PR's `headRefOid` is not on `main` (the merge rebases it: `compare`
  says DIVERGED). So the PR's merge commit, not its head, tells whether its merge reached the
  default branch.
- One GraphQL field reads the default branch's last commits in the same query as the PRs:
  `object(expression: "HEAD") { ... on Commit { history(first: 100) { nodes { oid } } } }`
  (checked: it returns 100 oids, among them `958ac5a6`, `18b251d7` and `e5c1f027`, #335's merge).

## What changes

### 1. The forge read: `skills/chantier/scripts/cli/src/chantier/board/forge_read.py`

- `GITHUB_FIELDS` gains `mergeCommit { oid }`.
- `github_query` gains, next to its `wf:` alias, one alias for the default branch's recent
  history: `dh: object(expression: "HEAD") { ... on Commit { history(first: N) { nodes { oid } } } }`,
  with `N` a module constant `DEFAULT_HISTORY = 100` (a named constant, documented in the module's
  docstring as the window inside which a stacked merge can be read as landed).
- `github_state` carries one new field, `merged_on_default`: for a merged PR, `True` when its
  `mergeCommit.oid` is in that history, `False` when it is not (or when the PR has no merge
  commit); `None` for a PR that is not merged. `_github_rows` reads the history once and passes the
  set of oids to `github_state` (its signature grows one parameter, as `has_workflows` did).
- `gitlab_state` carries `merged_on_default: None` always (GitLab is out of scope, below).
- The read stays one GraphQL call per batch, read-only: the hub's "one query per project" and the
  board's "one forge call per read" (AGENTS.md) still hold. The module's docstring names the new
  field next to `head`.

### 2. The judgment: `skills/chantier/scripts/cli/src/chantier/board/prs.py`

- `row_of` copies `merged_on_default` from the forge state into the row (`f.get(...)`, so a fake
  forge that does not give it reads `None`).
- `landed_with(row, by_cr)` keeps its present rule and gains a second way to land, tried when the
  first returns `None`: when `row["merged_on_default"]` is `True` and the walk down the chain of
  `merged_into.cr` reaches, through rows each merged on the forge (`state == "merged"`), a CR whose
  PR was merged into a branch that is no CR's, it returns `{"cr": <that CR>, "at": <that CR's
  merged_at>}`, whatever the order of the merge times. A missing row, a base not merged, a cycle,
  or `merged_on_default` not `True` keeps `None` (told "not landed", as today). Its docstring says
  both ways: the base merged at the same time or later (a stack merged top-down, PR by PR), or the
  PR's own merge commit on the default branch (a native stack merged in one go, bottom-up).
- `rows_of` is unchanged: it is the one function the PRs page and the hub both judge with, so both
  get the fix. `_closed_row` is unchanged (a closed batch's rows never carry `merged_into.cr`, so
  `landed_with` stays `None` there).

### 3. The journal and its texts: `skills/chantier/scripts/cli/src/chantier/hub/journal.py`

- No new kind, field or text. `merged_events` already writes `landed_with` and `landed_at` from
  the row; `merged_text` already prints `into <cr>'s branch at <t>, landed with <cr> at <t>; for
  the Chief of Staff: order merged <cr>` for such a line; `_key` already lets a landed line follow
  a not-landed one once. The module docstring's `merged` paragraph adds: "or when the forge shows
  the PR's merge commit on the default branch".

### 4. The Chief of Staff's card: `skills/chantier/references/chief-of-staff.md`

- The paragraph on `landed with <other cr>` (today: "the hub (or the board) read the PR merged into
  `<other cr>`'s branch and that CR's PR on the default branch at the same time or later") says
  instead: "...and that CR's PR on the default branch at the same time or later, or the PR's own
  merge on the default branch (a native stack merged in one go)". The watcher's-end paragraph's
  check on the forge ("for a `landed with` line, its base's PR merged into the default branch")
  stays true as it is: no change there. Only the card in `skills/chantier/references/` changes; no
  agent file changes (the contract lives in the card).

### 5. Tests (`skills/chantier/scripts/cli/tests/`)

Few, parametrized, in the files that already hold these cases; they call the code in-process with
the existing fakes, never a forge.

- `test_board_prs.py`, `LANDING` (the parametrized table of
  `test_a_stacked_merge_is_signalled_landed_with_its_base_once_the_base_landed`): the `merged`
  helper gains an optional `on_default` that sets `merged_on_default`, and the table gains rows:
  - the batch-28 case: the stacked PR merged at T1, its base into `main` at T3 (one second
    earlier), `merged_on_default` True: `landed_with` is the base's CR (today's row "the base
    merged before it: not landed" keeps its `None` with `merged_on_default` False or absent);
  - a chain of two bottom-up (each PR merged after the one below, all on the default branch):
    landed with the bottom CR;
  - `merged_on_default` True but the base not merged: `None`.
- `test_forge_hub.py`: one test drives the hub's cycle (`World`, its fake `read`) on a running batch
  of three stacked CRs merged bottom-up one second apart, the two upper ones with
  `merged_on_default: True`, and asserts the journal (`shape`) holds, for each upper CR, one
  `merged` line whose `landed_with` is the bottom CR, and that `journal.lines` / `merged_text`
  give `... landed with <bottom> at <t>; for the Chief of Staff: order merged <cr>` for them. This is
  the intent's "test on a prepared forge journal": the journal the hub writes from a prepared
  forge read, read back as `status` and the watcher read it.
- `test_board_forge_read.py`: one parametrized test of `_github_rows` on a prepared GraphQL answer
  (a `dh.history.nodes` list and two merged PRs): the one whose `mergeCommit.oid` is in the list
  reads `merged_on_default` True, the other False; an open PR reads None; a GitLab node reads None.
  One assertion that `mergeCommit` is in `GITHUB_FIELDS` and that `github_query([1])` holds
  `object(expression: "HEAD")` and `history(first: 100)` (the `DEFAULT_HISTORY` constant).
- `forge_world.OPEN` and the board test's fake forge need no change (absent reads `None`).

## Decisions carried from `02-answers.md`

- The intent is the grill; the Chief of Staff settled it on 2026-11-20 with no question to the
  user. Every behaviour above comes from `01-intent.md`: the line `order merged <cr>` for a PR of a
  native forge stack merged into a branch below it when the stack's bottom PR is merged into main
  and the PR's commits are on main, and a test on a prepared forge journal.
- The CR joins batch-29 (factory, stack) once specified.

## Out of scope

- GitLab: it has no native stack in chantier (a chain of MRs, each targeting the one below), and
  its fold rule already governs a merge into the MR below. `merged_on_default` is `None` there and
  the present time rule is unchanged.
- Recording anything: the hub and the board still record nothing; the Chief of Staff still runs
  `order merged` after its forge check, as its card says.
- Batch-28's existing journal lines: they stay as written (the journal is append-only); batch-28
  is closed.
- A stacked merge whose merge commit is older than the default branch's last 100 commits at the
  read: it is told "not landed", as today (the safe side: the Chief of Staff tells the user, who
  checks). The hub reads every 20 s while a batch runs, so a fresh merge is well inside the window.
- No new CLI command, no new journal kind, no change to the PRs page's web files
  (`board/web/`), to the watcher (`hub/watch.py`) or to `status`.

## Host and default matrix

None: the change depends on the forge (GitHub or GitLab), not on the agent host (Claude Code or
Copilot) nor on a shipped default versus a configured value. The forge cells, in the evidence:

- GitHub, native stack merged in one go: landed (new test rows, hub test).
- GitHub, stack merged PR by PR top-down: landed as today (existing `LANDING` rows).
- GitHub, PR merged into a base branch after the base landed, its merge not on the default branch:
  not landed, as today (existing row, `merged_on_default` False).
- GitLab: unchanged (`merged_on_default` None; the forge read test).

## Evidence

- `just check` passes in the worktree at the pushed head (Linux, macOS and Windows in CI), with
  `just test` inside the 30 s budget of AGENTS.md (the new cases are table rows and three tests).
- `just eval-dry-run` in the worktree (the change is under the CLI's `src/`).
- The pipeline's `just scenario (ubuntu-latest)` job green at the PR's head (a change to the CLI and
  a card); as the batch's top, `chantier gate` runs `just scenario` locally per AGENTS.md.
- The tests above, by name, in the PR's Deliverables.
- One read-only forge check, quoted in the PR: the new GitHub query run once with the user's `gh`
  on `gsemet/chantier` for #335, #342 and #354 returns `merged_on_default` True for the three
  (their merge commits `e5c1f027`, `958ac5a6`, `18b251d7` are in `main`'s last 100 commits today),
  and `prs.rows_of` on that read gives #342 and #354 `landed_with` CR-369. A Driver that cannot run
  `gh` says so in Known gaps; the tests stand alone.

## Open questions

None.
