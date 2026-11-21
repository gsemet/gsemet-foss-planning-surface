# Change Specification: a CR taken out of a batch comes back under its number, with its branch and PR

## Goal

At batch-28's end, CR-381 and CR-382 were only postponed. The user wanted them back later as
CR-381 and CR-382, with their PRs #346 and #347, not as new CRs with new numbers and fresh
branches.

The CR `order-drop-asks-where-the-cr-goes-trash-` (CR-397, batch-29) lets `order drop` send a CR to
the inbox or the backlog. Its folder keeps its number (`2-backlog/P2/381-<slug>`), the number is
reserved in `restored.json`, and the drop writes `formerly.json` in the folder:
`{"cr", "batch", "branch", "worktree", "pr", "pr_draft"}`. It stops there.

This CR reads and consumes `formerly.json`: when such a folder joins a batch, it gets its number
back, and its new Driver picks up its branch and its PR, rebased on the new base. It starts fresh
only when its branch is gone. A moved-out CR whose PR the user merges later is recorded under its
own number and PR.

## What changes

### 1. CLI: `add_cr` reads `formerly.json`

`skills/chantier/scripts/cli/src/chantier/commands/opening.py` (`add_cr`), with a new helper
beside it (for example `_came_back(b, prepared) -> Formerly | None`). `add_cr` is the one path
of every join: `open` (`_open_crs`), `order add` (`commands/orders_apply.py` `_add`), a factory's
`triage --ready` (`commands/intake.py` `_join_factory`, through `add_order`), the fix CR and the
release CR (`orders_release.py`). So all of them get the behaviour.

- **Reading:** after `prepared_cr` and `ensure_unclaimed`, before any move, `add_cr` reads
  `<prepared folder>/formerly.json` when it is there.
  - It holds a JSON object with `cr` matching `CR-<digits>`. `batch`, `branch`, `worktree`, `pr`
    are strings or null, `pr_draft` is a boolean or null.
  - Anything else (not UTF-8 JSON, missing `cr`, a wrong type) is refused with exit 2
    (`EXIT_PRECONDITION`), before anything moves, naming the file and the expected form:
    `<path>: expected {"cr": "CR-<n>", "batch", "branch", "worktree", "pr", "pr_draft"}`.
  - No `formerly.json`: today's behaviour, unchanged.
- **The number:** with `formerly.json`, the CR id is its `cr` (`CR-381`), not `next_cr_number`'s.
  The folder goes to `1-pending/<number:03d>-<slug>` as today, with that number (`381-<slug>`).
  `next_cr_number` is not called. The number is already in `restored.json`, so it is never given to
  another CR.
- **A clash:** the batch's record already holds that id, and it is not the reopen case below (the
  same CR, `cancelled`, with a `left_to`, in the batch `formerly.json` names). It is refused with
  exit 2 before anything moves: `<folder>: formerly.json names CR-381, which batch-NN already
  holds`.
- **Same batch, reopened** (the record of the batch being joined holds `cr`, `cancelled`, with a
  `left_to`): the existing entry is reopened, and no second entry is added.
  - `status` becomes `queued`.
  - Reset: `round` to 0, `attempts` to 0, `stacked` to false, and `agent`, `left_to`, `head`,
    `pr_base`, `start_on`, `blocked_reason`, `gate_waiver`, `phase`, `phase_detail`, `phase_at`
    unset (`clear_phase()` for the three `phase*`).
  - Set as for a new CR: `title`, `kind`, `path`, `specification`, `updated`.
  - From `formerly.json`, by the branch rule below: `branch`, `worktree`, `pr`, `pr_draft`.
  - Kept: `notes`, `cost_usd`, `cost_unpriced`, and every other field.
  - `order` becomes `max(order) + 1`, as for any CR that joins (choice 1).
  - `after` is emptied, then `declare_dependencies` sets it from the folder's `depends.json`, as for
    any CR that joins (choice 2).
  - The event log: `b.log("add", …, came_back=True, origin=…)`.
  - The rest is today's: `declare_dependencies`, `join_release`, the stack waiver of `_add`.
- **Another batch** (`formerly.json` names another batch, or this batch's record does not hold the
  CR): a new `CrEntry` is appended, as today, with the id from `formerly.json`. Its `branch`,
  `worktree`, `pr` and `pr_draft` follow the branch rule.
- **The branch rule:** `core/git.py` `branch_exists(formerly.branch, cwd)`, with `cwd` the clone of
  an external planning surface or the project's root (as `closing.py` and `endpause.py` read it).
  - **The branch exists:** `branch`, `worktree`, `pr` and `pr_draft` come from `formerly.json` (a
    null `pr` stays null). The line: `CR-381 joins with its branch <branch> and PR <link>`, or
    `CR-381 joins with its branch <branch> and no PR` when `pr` is null (choice 3).
  - **The branch is gone** (or `branch` is null): the same number, with a fresh branch and worktree
    named the usual way (`chantier/<batch>/<cr-id lower>-<slug of the title>`,
    `<worktrees>/<batch>-<cr-id>`), `pr` and `pr_draft` unset. The line: `CR-381 joins fresh: its
    branch <branch> is gone`. When `formerly.json` held a PR, it ends `; its former PR <link> is
    left as it is` (choice 4).
  - The check is a local-branch read only. A branch left only on the remote counts as gone, as
    `branch_exists` reads it.
- **The output:** the join line is printed by the command that joined the CR, right after its
  `added …` line: `order add`'s and `triage --ready`'s output list, and `open`'s output.
  - `order add` keeps its first line `added CR-381, queued[, after …]` unchanged, so
    `_join_factory` still reads the id from it.
- **Consumed:** `formerly.json` is deleted once the record holds the CR again: after the folder's
  move into `1-pending` and the entry appended or reopened, inside the same command, before the
  record is written.
  - A refusal before that leaves the file and the folder where they were.
  - The `formerly CR-381 of batch-28` line that CR-397 appends to `01-intent.md` stays: it is for a
    person.

### 2. CLI: what `take` shows

Nothing new is written. `take`'s facts (`commands/facts.py`) already print `PR: <link>` from the
record's `pr`. They also print `worktree: <path> branch <branch> …; not created yet: a Driver
creates it first` when the worktree folder is not there. A CR that came back with its branch
therefore shows its PR at its first take, and that is how the Driver card recognises it (section 3).

### 3. Cards

Both hosts read the same cards. The agent files (`agents/`, `com.github.copilot/agents/`) do not
change.

- **`skills/chantier/references/driver.md`**, the worktree bullet ("The worktree is your first
  step: …"). Add a sub-rule: a CR whose first take shows a `PR:` link came back to a batch (it was
  taken out of an earlier one with its work).
  - Use its branch, never a new one: its recorded worktree if it is there, else
    `git -C <main checkout> worktree add <path> <branch>` (with a planning surface, `git -C
    <clone>`), with the names `take` printed.
  - Before anything else on the forge, read the PR (`gh pr view <n> --json state`, `glab mr view
    <n>`):
    - **Open:** go on.
    - **Closed:** reopen it (`gh pr reopen <n>`, `glab mr reopen <n>`) before any push to its
      branch. When the reopen is refused, push nothing and hand back `handback <cr> blocked
      question: its PR <link> is closed and the forge refuses to reopen it: <exact text>`. Never
      open a second PR.
    - **Merged:** nothing to do. Hand back `handback <cr> blocked question: its PR <link> is already
      merged` for the Chief of Staff, who records it (`order merged <cr>`).
  - Then rebase it on the base `take` names (the existing "Rebase first" bullet) and ship to that
    same PR. Never open a second PR for it.
- **`skills/chantier/references/chief-of-staff.md`**, beside the "When the user merges a PR before
  its `ready-to-merge` line" rule, a route of its own: a moved-out CR whose PR the user merges
  later, outside any batch.
  - The CR's folder is in the inbox or the backlog with `formerly.json`.
  - On "I merged #n" for it: `order add --note <folder>`, which brings back its number and its PR,
    then `order merged <cr>` at once. In Foreman mode, send both lines to the Foreman in one
    message, the add first.
  - With no batch open: tell the user the merge is recorded the same way in the next batch, and
    leave the folder as it is (choice 5).
  - Also: a Driver's `blocked question: its PR <link> is already merged` is recorded the same way,
    with `order merged <cr>`.
- **`skills/chantier/references/concepts.md`**, the lifecycle line that CR-397 writes for
  `formerly.json`: add "; when that folder joins a batch, it gets its number back, and its branch
  and PR while its branch exists; `formerly.json` is then deleted".

### 4. The GitHub force-push claim, dropped

Intent asked for "GitHub refuses to reopen a PR after a force-push" to be proved or dropped. No
check in this CR can prove it: it needs a forge write, and the scenario and the tests run without
one. It is dropped. The rule "reopen before any push" stands on its own grounds: a push to a closed
PR's branch does not show on that PR. Any refusal of a reopen, whatever its cause, is handled the
same way: blocked, with the forge's exact text (section 3).

## Decisions carried from 02-answers.md

| Decision | Where |
| --- | --- |
| Origin: split from CR-397 (finding 10); that CR writes `formerly.json` with `pr_draft`, this one reads and consumes it | Goal, section 1 |
| The number: same number back, never given to another CR | section 1, "The number", "A clash" |
| Branch and PR: picked up and rebased on the new base; fresh only when the branch is gone | section 1, "The branch rule"; section 3, driver.md |
| Finding 1: a PR merged later: `order add`, then `order merged`; the Driver treats a merged PR as "nothing to do, ask the Chief of Staff"; chief-of-staff.md names the route | section 3 |
| Finding 6: the reopen resets every per-round and stack field; `pr_draft` from `formerly.json` | section 1, "Same batch, reopened" |
| Finding 8: reopen a closed PR before any push; the force-push claim marked unproved | section 3; section 4 |
| Depends on CR-397 | `depends.json`; "Dependencies" |

## Dependencies

`depends.json`: `{"after": ["order-drop-asks-where-the-cr-goes-trash-"]}`. CR-397 writes
`formerly.json`, the `left_to` field, the `formerly` line, the `restored.json` reservation, the
reopen allow rules (`gh pr reopen*`, `glab mr reopen*`) and concepts.md's line. This CR reads them,
so it lands after CR-397.

## Out of scope

- Writing `formerly.json`, `left_to` and the drop's destinations: CR-397.
- Recording a moved-out PR's merge by the hub or the board, without the user's word.
- A branch left only on the remote: no fetch of it. It counts as gone.
- Removing the former PR or branch of a CR that joins fresh.
- `restore` and `triage`: unchanged. `formerly.json` moves with the folder as any file does.

## Evidence

No host or default/configured dependency, so no matrix.

**Tests** (`skills/chantier/scripts/cli/tests/`, in-process, few and parametrized, within `just
test`'s budget; `test_opening_and_restore.py` or `test_batch_end.py`). Each `formerly.json` comes
from a real `order drop <cr> --note P2` (CR-397), never written by hand, except the malformed case:

- **Another batch, branch there:** drop a CR with a PR to P2 and close the batch. Open a new batch
  with that folder.
  - The CR is `CR-<same n>` in `1-pending/<n>-<slug>`, with the former `branch`, `worktree`, `pr`
    and `pr_draft`.
  - The output has `joins with its branch … and PR …`.
  - `formerly.json` is gone.
  - A later item gets a number above `<n>`.
- **Same batch, reopened, parametrized over branch there / branch deleted** (`git branch -D` in the
  fixture's repository):
  - `order add --note 2-backlog/P2/<n>-<slug>` leaves the batch with one entry for `CR-<n>`,
    `queued`, every reset field at its default, `notes` and `cost_usd` unchanged, and `order` the
    highest.
  - Branch there: `pr` and `pr_draft` from `formerly.json`, and the `joins with its branch` line.
  - Deleted: `pr` unset, the usual branch name, the `joins fresh: its branch … is gone; its former
    PR … is left as it is` line.
- **Factory:** `triage --ready` of such a folder in a factory batch joins it under its number, and
  the `factory …: CR-<n> joined on its own` line names it.
- **Refusals** (`test_rail_refusals.py`), each leaving `batch.json` byte for byte unchanged and the
  folder and `formerly.json` in place:
  - a malformed `formerly.json` (a prepared text, the one case the shipped flow cannot produce):
    exit 2;
  - a `formerly.json` whose `cr` the batch holds live: exit 2.
- **Cards** (`test_plugin_files.py` or the cards' structure test), reading the shipped
  `driver.md` and `chief-of-staff.md` at the head under test:
  - driver.md names `gh pr reopen`, `glab mr reopen` and "never open a second PR";
  - chief-of-staff.md names the `order add` then `order merged` route.

**Scenario** (`scenario/run_scenario.py`): after CR-397's step that drops the CR added to the
running direct batch with `--note P3` (near line 2791), add it back with `order add --note
2-backlog/P3/<n>-<slug>`. Check:

- it is `CR-<n>` again, one entry in `batch.json`, `queued`;
- its folder is `1-pending/<n>-<slug>` with no `formerly.json`;
- the output carries the `joins …` line that matches whether its branch exists at that point in the
  scenario.

Then end it as the step went on before (drop it to the trash), so the later checks hold.

Each check reads the shipped cards and CLI at the head under test.

**Gates:**

- `just check`;
- `just eval-dry-run` (a CLI `src/` change);
- `just scenario (ubuntu-latest)` green at the PR's head.

## Open questions

None. The choices left to the writer are numbered in the text (1 to 5).
