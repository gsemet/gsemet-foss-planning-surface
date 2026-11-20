# Investigation: CR-397, order drop names where the CR goes

Worktree `C:/Users/gaeta/Projets/chantier.worktrees/batch-29-CR-397`, based on CR-394's branch
(`held`, `order hold`, `is_held`, `_held` in forge_stack are all there). Paths below are under
`skills/chantier/scripts/cli/src/chantier/` (written `src/`) unless said. Read only; the project's
rules (`rules`) hold AGENTS.md, CONTRIBUTING.md, scenario/README.md, evals/README.md: AGENTS.md's
pane-screenshot rule and the gates apply, nothing else changes the plan.

## 1. Files and entry points (real lines)

### CLI: the order
- `src/declare/orders.py:19-40`: `kind` help (line 19-25) and `--note` help (27-34): add "drop: trash,
  inbox or P1..P4".
- `src/commands/orders.py`:
  - `_check_args` (35-63): the usage refusal (exit 1) belongs here or in `_normalise_args`, before
    the lock, so nothing is recorded.
  - `_normalise_args` (186-199 region, `def` at ~193): returns `note`; the drop's value
    (`trash|inbox|P1..P4`, case-insensitive) becomes `6-trash`, `1-inbox`, `2-backlog/P<n>` here, and
    the folder is what `_Req.note`, the `OrderRecord.note` and the printed line carry (line 313
    `text = f" {note}"`).
  - `_record_order` (~170-200): `applied = ... not (kind == "drop" and status in LIVE)`; a held
    drop must be `applied` (not LIVE, so already true; a held CR is `ready`, never LIVE). Add
    `to=` to `b.log("order", ...)` for a drop.
  - `_ordered` (~265-300): the printed line `[chief-of-staff→foreman] order O-1: drop CR-103 <folder>`
    is built at the end from `note`; the PR clause `; close its PR <link>` must be appended to
    that line (and to the record's note? spec: the line, not the record: keep `note` = folder
    only). The handler's `effect` lines print after it.
  - `ORDER_KINDS`/`CR_ORDERS` unchanged.
- `src/commands/orders_apply.py:153-164` `_drop`: refusals in order (merged -> as today, live ->
  records `left_to` and returns the "Foreman stops its Driver" line, cancelled -> exit 2), then
  `trash_cr` + `touch(status="cancelled")` + `w.ended`. Rewrite to: validate destination for
  release/fix CR (exit 2), name-clash check, held unset, `left_to`, move, PR clause.
  `w.note` holds the folder; the release/fix check reads `c.kind` (as `forge_stack._dropped` does).
- `src/commands/orders_hold.py`: `unhold` does `c.unset("held")` (line ~74); `is_held` in
  `src/stacks.py:18` already treats a cancelled CR as not held, so the explicit unset at the
  drop is for a clean record only. A held CR is status `ready` (hold refuses others), so its
  drop is the non-live path: moves at once, `applied`. Print `<cr> was held: no stack driver
  needed`.
- `src/commands/orders_word.py`: `Word` has `b, c, note, own, ended`; nothing to change except
  maybe a `to_pr` helper (see PR clause).

### CLI: the move
- `src/lifecycle/stages.py:236-243` `trash_cr` (guard `source.parent not in (done, archives,
  trash)`); `_relocate` (188); `stage_layout` (25-41: `inbox`, `backlog`, `ready`, `trash`...).
  Add a sibling (`move_out_cr(batch, cr, folder)` or one function with the destination): moves
  to `1-inbox/<name>` or `2-backlog/P<n>/<name>` where `<name>` = the current folder name
  (`381-<slug>`, no date; from `cr_directory(...).name`, as `add_cr` named it
  `f"{number:03d}-{slug}"`: note the zero padding `003-...`, `restored.json` takes `int`).
  - **Re-move guard (risk):** `trash_cr`'s guard only stops a CR already in done/archives/trash.
    `cancel` of a CR that `order drop` already moved to inbox/backlog (status cancelled, folder
    elsewhere) must not move it again; `cancel` must also skip when `c.path`'s parent is not in
    `4-batch/1-pending|2-actives`. Scenario 1175 (`cancel` of an already cancelled CR) and 627
    (fake Foreman) depend on this.
  - `formerly.json`, the `formerly` line and `restored.json`: reuse `commands/intake.py`
    `_remember` (lines ~181-192: writes `restored.json` via `write_restored_number`, appends
    `formerly CR-n of batch` to `01-intent.md`/`notes.md`) and `_check_free` (166-180) +
    `_owners`: move the shared logic into `lifecycle/stages.py` (or a new small module) so both
    `restore` and the drop call it; `_check_free`'s message says "restore: ... restore again with
    --slug", so parametrize the verb/hint. `batch_crs` there holds slugs (`cr_slug`), while the
    drop's name is `<number>-<slug>`: the clash test for the batch must compare the slug part
    (spec: "a CR of the open batch with that slug"), the folder tests the full name.
  - Write `formerly.json` with `core/` writers (UTF-8, `json.dumps(..)+"\n"`, like
    `write_restored_number`); fields `cr, batch, branch, worktree, pr, pr_draft` from `CrEntry`
    (`pr_draft` is already on `CrEntry`, `core/records.py:87`).
  - Order of effects: check clash, then move, then write files (all inside `changes_lock` and
    `RenderedBatch`, which writes the dashboard on exit, `lifecycle/session.py:16`).
  - `core/batch.py:283` `next_cr_number` reads `restored.json` already (`RESTORED_NUMBER_FILE`,
    line 280); nothing to change there.
- `src/commands/release.py:89-128` `cancel`: `trash_cr(b, c)` (122) becomes "move to
  `c.left_to`"; refuse exit 2 with the spec's text when `left_to` is None and status not
  already cancelled; an already cancelled CR keeps today's path (no refusal, `left_to`
  present or legacy none). Its `b.log("cancel", ..., path=c.path)` gains `to=`; output
  line `cancelled CR-103 to 1-inbox; stopped …` for non-trash; the PR clause line for a
  trash outside a stack with a PR (`b.record.mode != "stack"`). `declare/release.py:23-25` help text
  ("stop a CR's processes and mark it cancelled") may be updated.
- `src/core/records.py:74-121` `CrEntry`: add `left_to: str | None = None` (beside `held`, 117).

### CLI: close, history, final pages, labels
- `src/commands/closing.py:151-170` `_to_remove` (cancelled filter at 156-159): keep only
  `left_to in (None, "6-trash")`; a new line builder for `left_to` in inbox/backlog (the recorded
  `c.path` is the folder; if `repo.planning_path(c.path)` no longer exists print `(moved since
  from <left_to>)`). The `tail` list in `_closing` (~195-212) gets the `kept, moved out with
  their work` line next to the removal line; the removal sentence there ("the dropped CRs and
  the merged CRs' leftovers ...") must be reworded for trashed only.
  `_closing`'s `archived` list takes only CRs whose folder parent is `3-done`: moved CRs are
  not in it, nothing to do.
- `src/history.py:33-55` `archive_of` / `cr_entry`: for `left_to` in inbox/backlog `archive`
  None and `"to"`; trash: archive path kept and `"to": "6-trash"` (also for legacy `left_to`
  None cancelled? spec says "trashed CR keeps ... `to: 6-trash`": a legacy cancelled record with
  no `left_to` should read as trash: decide in code, one helper `dest_of(c)`). `result` stays
  `dropped`. `link_to` (80) and the table at 95-97 already tolerate `archive` None.
  Consumers of `batch-NN.json` entries to check: `history.py:97`, the board's reading (grep
  `"archive"` in `board/`).
- `src/status/write.py:40-50` `write_final_pages`: skip `c.left_to` in inbox/backlog.
  (`write_batch` 26-37 rewrites STATUS files wherever the folder is: no change.)
- `src/status/words.py:119-140`: `label` builds `state = {"cancelled": "dropped", ...}`:
  for a cancelled CR with `left_to` in inbox/backlog the state is `dropped to <left_to>`. `icon`
  unchanged (`⚪`). Other readers of the label word: `status/words.py:20,33,52` (`Dropped`
  tag and severity "grey": keep), search for `"dropped"` in `board/web` JS/Python
  (grep before coding; `DESIGN.md` of `board/web` is read only if that folder changes: the spec
  says it does not).
- `src/commands/endpause.py:14-48` `_cleanup` runs on merged CRs only: no change.
  `src/commands/opening.py:56`, `core/batch.py:283`: numbers; unchanged.

### CLI: forge stack
- `src/commands/forge_stack.py`:
  - `_plan` (41-81) returns 5 values; `_dropped` (132-141) filters `c.status == "cancelled" and
    kind != "fix"` and `PR_LINK` only (GitLab links are not matched here: an existing gap;
    `_held` uses `PR_LINK or GITLAB_LINK`). Split: `_dropped` gets `left_to in (None, "6-trash")`;
    new `_moved(data)` returns `{number: (cr_id, left_to)}` (GitHub and GitLab links).
    `_plan` returns a 6th value (or `Apart` built in `_plan`): every call site unpacks 5 values
    (`_rebuild` 185, `_create` 231, `_show` 322): touch all three.
  - `_held_rows` (127-129) builds `{"number", "base"}`; a `_moved_rows` with a `why`
    `(moved to <dest>)` per row. `retarget(rows, where, done, why)` in
    `forge_stack_gh.py:145` takes one `why` for all rows: since each moved PR has its own
    destination, call it once per PR, or add a `why` key to the row (the held path uses the
    function argument). The line: `#346 base <old> -> main (moved to 2-backlog/P2)`.
  - `_rebuild` (181-227): after `_unstack_all` and the held retarget, retarget moved rows;
    `_unstack_all` (169-178) triggers an unstack on `planned | set(apart.held)`: a stack that
    holds only a moved PR with the planned ones is covered by `planned`, but moved/held PRs
    should be in the trigger set too (decide with the held code). `_create` (230-244) same.
  - `_checks` (247-297): `foreign` must exclude moved PRs; add moved text to check 2 (`said`
    tuple); a moved PR still inside the forge stack is probably a check 2 failure as for held
    (`... moved to X and still in stack #n: forge-stack rebuild`): the spec only says "not
    called foreign" and names it apart: choose the held-like line.
  - GitLab: `forge_stack_gitlab.py:183` `make(rows, come, where, held)` retargets held MRs with a
    hardcoded `(held out of the stack)` suffix at 195: add a moved list or give rows their
    `why`; `show` (GitLab) has no dropped/held notion: nothing for check 2 there.
  - `forge_stack_gh.py:80-112` `Apart(left, dropped, held)` + `held_outside`: add `moved`
    (3-tuple unpack at 92 and callers `forge_stack_gh.py:195` `Apart({}, {}, {})` and
    `forge_stack.py:195` `Apart(left(come), dropped, held_prs)`). Message e.g. `it also held #346
    of CR-381, moved to 2-backlog/P2: left out, on main`.
  - `unstack_rows` (151-176, used by `forge-stack unstack` and mode switches) already skips ENDED CRs.
- `src/commands/permissions.py:38-99` `SAMPLES`: add 4 tuples (`("batch", "github", "gh pr close
  12", "gh pr close*")`, same for `gh pr reopen`, `("batch", "gitlab", "glab mr close 12", ...)`,
  `glab mr reopen`); `RECOMMENDED_ALLOW` (176) and P10 derive from `SAMPLES`. Check
  `tests/test_cli_units.py` and any test/doc that counts or lists the patterns (grep
  `gh pr ready*`).
- `src/lifecycle/layout_check.py:25-36` `CR_FILES`: add `"formerly.json"`.
  (`restored.json` is at `repo.changes`, not a CR file.)
- `skills/chantier/references/concepts.md` "Change Request" tree: add the line (see the cards part).

### What did not change (verified)
- `ensure_unclaimed` (`lifecycle/stages.py:171`) skips cancelled CRs: a moved folder can be
  added again. `lifecycle/backlog.py` finds items by slug among inbox/backlog/ready: the moved
  folder `381-<slug>` is found as `381-<slug>`. `commands/validate.py` / summary lint reads inbox
  and backlog CR folders: STATUS.md/STATUS.json already in `CR_FILES`; a moved CR's `summary.json`
  etc. stay valid. Check `summaries/format.py` raises no gap for a CR with `STATUS.*` + `work/`
  in the backlog (a CR in the backlog with no `summary.json` is already a gap case today).

## 2. The smallest change

1. `CrEntry.left_to`, `_drop` + `cancel` + a shared `move_out` helper, the clash check shared
   with `restore`, `formerly.json`, `restored.json`.
2. Refusal rules in `_normalise_args`/`_check_args` (exit 1) and `_drop` (exit 2, release/fix).
3. `closing`/`history`/`write_final_pages`/`label`.
4. forge-stack `_moved` plumbing and the 4 allow rules.
5. Cards, docs, scenario.

Live-CR semantics (my reading of section 1): for a LIVE CR the order only records `left_to` (and
the line says the Foreman stops the Driver, then `cancel`); `status` flips to `cancelled` and the
folder moves at `cancel`. "A second drop of a live CR replaces the destination" only works when
`status` stays live until `cancel`. The spec's sentence "the CR's status becomes cancelled for every
destination" is true at the move, not at the order for a live CR. If the user meant the status to
flip at the order for a live CR, `slot_of`/`cancel`'s guards and the "second drop replaces" rule
conflict: keep status at `cancel`.

## 3. Risks

1. **Bare callers become exit 1.** Every bare `order drop` / `order drop` followed by a
   `cancel` fails. Real lines in the worktree (the spec's numbers shifted by 1 to 78):
   - tests: `test_batch_end.py:73,74,140,225` (as listed), `test_factory.py:143`,
     `test_rail_refusals.py:136` (no epoch refusal unchanged; it must still hit the epoch
     refusal before the destination refusal: `cancel`'s epoch check is first, keep it first).
     `test_board_times.py:75,84` only build events.
   - scenario (`scenario/run_scenario.py`): `order drop` at 1090, 1958, 1959, 2792, 7208, 7213,
     7219, 7223, 7293, 7311, 7340, 7479 (fix CR), 7737, 8298 (the spec said 8220); bare
     `cancel` at 2645, 3486, 4031, 4130, 4491, 4671, 5606, 5607, 7686; keep 627 (fake Foreman,
     after a drop order, its drop line now has a folder) and 1175. **7219 and 7223 are
     `expect=2` refusals of an already dropped CR: they must carry `--note trash` too, or
     they return exit 1 (usage refusal runs first) and the scenario fails.** Order of
     refusals in `_drop`: usage (1) first, then merged / already cancelled (2).
   - Other texts calling it bare: `evals/claude-planted/RUNBOOK.md:70`,
     `evals/full/RUNBOOK.md:83`, `evals/README.md:177,183`, `evals/SCORECARD.md` C16/C19 (lines
     42, 45), `docs/hosts.md:46` (cancel; unchanged text, still true), `chief-of-staff.md:1031,
     1237, 1248, 1439`, `foreman.md:25,127,186`, `scenario/README.md` (check), `driver.md`
     `drop:` notes (1055-1115), `init.md:113` ("drop CR-<n>" phrase: fine).
     `evals/kit/audit.py:78-80` matches `cancel` as an epoch command: unchanged; check whether the
     kit scores `order drop` with a regex (grep showed none).
2. **`cancel` re-moving a CR already moved to inbox/backlog** (see 1): add a guard.
3. **Name collisions.** The folder name is `<NNN>-<slug>` (zero padded to 3 in `add_cr`).
   `restore`'s `_check_free` tests a bare name. Mixed number/slug comparison with
   `batch_crs` (slugs only) is easy to get wrong; test with a number present on both sides.
4. **Legacy records** with `cancelled` and no `left_to`: read as trash everywhere (`_dropped`,
   `_to_remove`, `cr_entry`, `label`). One helper (in `core/records.py` or `rails.py`).
5. **`_dropped` on GitLab:** matches `PR_LINK` only; GitLab moved MRs need `GITLAB_LINK`
   (`_held` has it, `_dropped` does not). Existing gap, not widened by this CR, but the moved list
   must use both.
6. **Stack-mode PR clause:** the clause appears only outside a stack (`b.record.mode != "stack"`).
   Series mode counts as "outside a stack"? The spec says "the batch's mode is not `stack`": yes.
7. **`close`'s `kept` line reads `c.path`:** `Closing` and `check_closable` or archive code may
   assume every CR with a `path` is under `4-batch` or `5-archives` (`_closing` filters on
   `cr_directory(...).parent == done`: safe). `status/write.py` `write_batch` for a CR in the
   backlog: `where[2] = cr_folder.parent.parent == folder` False, fine.
8. **`write_dashboard` after the move:** done by `RenderedBatch`'s exit; `cancel` and `_drop` both
   run inside it. Verify the dashboard counts the item in its new stage (the pane/board text
   unchanged).
9. **CR-394 interface:** `held` unset at the drop; `hold` refuses a non-ready CR so a held CR is
   never LIVE. The "held part" test needs `order hold` working in the same worktree (it is).
10. **Pane screenshot:** the label changes `STATUS.json`'s state word the CR board pane shows
    (AGENTS.md rule): the PR carries a screenshot captioned with the head SHA or names "no
    screenshot of the pane from a real session" in Known gaps.
11. **Test budget:** `just test` has a 30 s allowance above 18.5 s; the new tests must be few
    and parametrized (extend `test_batch_end.py:59`'s existing parametrization, add one
    forge-stack test to `test_stack_hold.py`'s world, one in `test_stack_label.py`, one
    refusals parametrization in `test_rail_refusals.py`, one `validate` case).
12. **Windows:** paths in `formerly.json` (`worktree` is an OS path, `path`s in `/`);
    UTF-8 without BOM; `restored.json` write with `encoding="utf-8"` (the existing writer).

## 4. Questions only the user can answer

None blocking. One to confirm at the end, not before coding: a live CR keeps `status` live until
`cancel` (see section 2); the spec's wording suggests it, and a "second drop replaces" rule requires
it.

## 5. Proposed split: two coder rounds

**Round 1: CLI and its tests** (one coherent unit; everything the scenario and the cards describe
must exist before they are written).
- `core/records.py` (`left_to`), a legacy-trash helper, `lifecycle/stages.py` (move-out,
  shared clash check, `formerly.json`, `restored.json`), `commands/intake.py` (use the shared
  helpers; `restore` behaviour and messages unchanged), `commands/orders.py`,
  `orders_apply.py` (`_drop`), `commands/release.py` (`cancel`), `declare/orders.py`,
  `commands/closing.py`, `history.py`, `status/write.py`, `status/words.py`,
  `lifecycle/layout_check.py`, `commands/forge_stack*.py`, `commands/permissions.py`.
- Tests: the refusals (`test_rail_refusals.py`), per-destination drop and cancel
  (`test_batch_end.py:59` parametrization over trash/inbox/P2), clash, PR clause, `close` lines
  and `batch-NN.json`, labels (`test_stack_label.py`), forge-stack (GitHub fake in
  `test_stack_hold.py`'s fixture at line ~349, plus GitLab), held drop, allow rules
  (`test_cli_units.py`), `validate` (`test_validate.py`), bare call sites
  (`test_batch_end.py` 73/74/140/225, `test_factory.py:143`).
- Gates after the round: `just test`, `just check`, `just eval-dry-run`.

**Round 2: cards, docs, SVGs, scenario and the other texts.**
- Cards: `chief-of-staff.md` (steering block 1031, the question rule, direct-mode line, "Dropping a
  CR from a stack" 1237, Table D 1600, `close` offer ~1723, restart line ~1554 (the spec's
  1545-1546)), `foreman.md` (25, 127, 186, the close-PR exception, "A drop in the stack"),
  `driver.md` ("Removing a dropped CR" 1055-1115), `concepts.md` (lifecycle 160, tree, stack bullet
  256). Agent files do not change.
- Docs: `docs/planning-folder.md:24,31`, `cr-folder-lifecycle-texts.md:3,194`,
  `cr-lifecycle-texts.md:3,533`, `cr-lifecycle-simple-texts.md:3,141`, and the 3 SVGs (2 matches
  each); text label `order drop → 6-trash/, 1-inbox/ or 2-backlog/Pn/, with its work`; check that
  the longer label fits its box (width change: search each SVG for the old text length/box).
- Evals texts: `evals/README.md:177,183`, both RUNBOOKs, `SCORECARD.md` C16/C19.
- Scenario: the bare calls above (with `--note trash`; 7219/7223 with it too), the P3 move at 2792,
  the step 5 and `close` checks. `just scenario (ubuntu-latest)` must be green at the PR's head;
  Windows: `chantier gate` locally by the batch's top CR.

## 6. Evidence plan

Kind: CLI behaviour change (plus one pane label change).
- **Before/after command outputs** (a log in `evidence/`, from the throw-away scenario world or
  the pytest tmp repo): `order drop <cr> --note P2` on a CR with a PR (order line, `dropped to
  2-backlog/P2: <folder>`), the folder listing with `formerly.json`, `01-intent.md`'s last line and
  `restored.json`; the same with `trash` (line ends `; close its PR <link>` in parallel mode, no
  clause in stack mode); `order drop` with no `--note` (exit 1) and `cancel` with no drop order
  (exit 2); `status` showing `⚪ dropped to 2-backlog/P2`; `close` (no `--yes`) showing the two
  lines; `forge-stack rebuild` against the forge fake showing `moved to 2-backlog/P2: left out,
  on main` and the retarget line.
  Technique: the pytest cases and `just scenario` step logs already hold these; capture the
  command lines with `chantier` runs in the scenario's workspace (`scenario/run_scenario.py` at
  its step 5 and the 2792 step), saved as `evidence/*.log` (Windows run by the top CR's `chantier
  gate`).
- **Pane screenshot:** one screenshot of the CR board pane from a real Claude Code session at the
  PR's head showing a CR labelled `⚪ dropped to 2-backlog/P3`, captioned with the head's 7-char
  SHA (AGENTS.md). Cannot be produced by an agent without a real interactive session: until the
  user supplies it, the PR's Known gaps says "no screenshot of the pane from a real session".
- **Cannot be shown:** the real forge calls (`gh pr close`/`reopen`) and a real Foreman closing a
  PR: no real eval in this CR; the fake `gh`/`glab` of the scenario cover the CLI part only.
- Docs/SVG: render the three SVGs (or their texts) before/after to show the new label fits;
  `just check` output as the gate log (`work/gates/`).
