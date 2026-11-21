# Conflicts: CR-431 rebased onto CR-430 (head 6fb2b35), new head db75bff6

Both CRs defined the same shared pieces (is_held, is_parked, apart, out_of_order, candidates,
apart_owner, the base rule, the stack's dependents, `held:` lines). Rule followed: CR-430's
versions stand (they are the base), CR-431's live hold is grafted on them; CR-431's duplicates
are removed.

- rails.py (6 hunks): CR-430's helpers kept (`base_owner`, `candidates`, `_open_owner`,
  `_unmet_word`, `apart_owner` non-Optional). Dropped CR-431's `_out_of_order`, `base_candidate`,
  `apart_kind`, `dependents_of`. Kept CR-431's `_check_no_held` (no release starts while a CR is
  held, any mode); removed its unused `found` in `series_predecessor`.
- stacks.py (6): CR-430's `_outside_base` / `_dependent_base` / `start_on_for` (it already
  records the series `start_on`). Dropped CR-431's `unset_started_on` (CR-430's
  `stack_apart.leave_stack_starts` is the same) and `_apart_base`. Kept CR-431's `refuse_held`
  and `held_text` wording, and `held_lines` for a live hold, now using `stack_apart.dependents`.
- stack_words.py (4), delivery.py (3), forge_stack.py (4), forge_stack_apart.py (3),
  forge_stack_gh.py (2), orders_drop.py (2): CR-430's side (`refuse_out_of_stack`,
  `Held`/`waiting` tuples, `_apart_line`); CR-431's `_refuse_out_of_order` and its unused import
  removed. In forge_stack.py's `check 2` waiting line I kept CR-431's tail ("and still in stack
  #n: `forge-stack rebuild`") on CR-430's wording; CR-431's test_hold_live_stack.py follows
  CR-430's wording (`, waits with held CR (order O-n): left out`).
- driver.py (4): CR-430's `_record_take` and imports; both `is_held` and `is_parked` imported;
  `handback` refuses a held CR (CR-431) before the parked refusal (CR-430).
- orders_hold.py (2): CR-431's live hold, but it calls CR-430's `leave_stack_starts`; the
  unhold placement now calls `place_on_top` (new, split out of CR-430's `unpark` in park.py, which
  now calls it too: same behaviour).
- status/words.py (5), status/now_next.py (add/add): both kept. `step`, the blocked phase and
  `now_next` answer Parked (CR-430), Held and Unheld (CR-431); `now_next` split in
  `_apart_now_next` to stay under the return limit.
- scenario/README.md: both lines. scenario/run_scenario.py: `park_live` and `hold_live` both kept
  (`hold_live` is section 13c, in the `stack` unit after `park_live`).
- Cards: chief-of-staff.md "Holding a CR" keeps CR-431's text and CR-430's parked sentences (the
  held/parked report sentences stay under 400 chars apart, as test_came_back requires);
  driver.md keeps CR-430's park paragraph, CR-431's live-hold paragraph and unhold paragraph
  (CR-430's shorter unhold paragraph dropped as a duplicate); foreman.md: CR-430's parked bullet,
  CR-431's held bullet (with CR-430's parked release-ask sentence folded in), then CR-430's
  parking bullet.
- test_came_back.py: both tests kept. test_hold_live*.py: `dependents_of` -> `stack_apart.dependents`,
  `apart_kind` -> `stack_apart.waits_with`.

Fast gate: `just check` in the worktree (lint, mypy, uv lock, biome, pytest, release notes): passed,
1584 passed, 20 skipped. `just scenario` not run.
