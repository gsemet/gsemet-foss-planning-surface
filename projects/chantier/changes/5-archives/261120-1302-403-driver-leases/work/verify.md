Head: db78350cf36cc696157270dda0dbe1a9f9608112

All claims judged at db78350 (the pushed head, worktree clean). Hand-run probes were on a scratch
project (batch-01, CR-101/CR-102, claude host), removed at the end; expiry was set by editing the
scratch `batch.json` (the CLI has no clock flag outside the board), not by sleeping.

## Tests at db78350
`pytest tests/test_leases.py tests/test_rail_refusals.py tests/test_startup_manifest.py tests/test_plugin_files.py` -> `133 passed in 35.32s`.
Covering tests: take/refuse/reclaim `test_take_refuses_a_live_or_not_confirmed_lease_and_reclaim_starts_the_next`;
`--lease` missing/stale `test_a_guarded_command_needs_the_lease_and_a_stale_one_is_lost`; late accepted + handback ends
`test_a_not_confirmed_current_lease_is_accepted_late_and_a_handback_ends_it`; stack forms
`test_the_stack_drivers_writing_forms_need_its_lease_and_its_reading_forms_none`; lease forms/renew/hold
`test_the_lease_command_shows_renews_and_runs_a_command_under_it`; gate/ticket/hold keep live
`test_a_long_gate_a_queue_ticket_or_a_hold_keeps_an_expired_lease_live`; QA order
`test_a_qa_orders_lease_starts_with_the_order_and_a_restart_needs_it_free`; `agents set -`/cancel
`test_agents_set_dash_and_a_cancel_end_a_lease_and_the_old_driver_is_told`; status/handoff
`test_status_names_a_lease_that_is_not_confirmed_and_handoff_prints_its_line`; Copilot close
`test_copilot_close_causes_come_from_leases_and_the_foremans_heartbeat`, `test_copilot_close_reads_a_qa_orders_and_the_stack_agents_lease`;
Claude close `test_claude_close_shows_a_live_lease_beside_the_transcripts_and_it_is_no_cause`.
Driver card common path cap: `test_cr_driver_common_path_reads_at_most_the_card_budget` is in the 133 passed (45,000 cap unchanged: `git diff origin/main...HEAD -- tests/test_startup_manifest.py` empty).

## Hand-run (real CLI, scratch batch) at db78350
- `take CR-101 --epoch 1` -> `took CR-101 (1 of 2 slots held), lease 1 until 12:55:46`; facts carry `lease: 1 (pass --lease 1 on your commands; renew at each wake: lease CR-101 renew --lease 1)`. rc=0.
- `lease CR-101` -> `lease 1 of CR-101: live until 12:55:46 (renewed 12:45:46)`; `lease CR-102` -> `CR-102: no lease`.
- `round CR-101` (no lease) -> rc=2 `round CR-101 needs --lease <n> (the number take printed)`.
- `round CR-101 --lease 9` -> rc=3 `claim lost: CR-101 was taken again (lease 1) at 12:45; stop now: nothing recorded`.
- `lease CR-101 renew --lease 1` -> live form, rc=0. `lease CR-101 hold --lease 1 -- python -c "import sys;sys.exit(7)"` -> rc=7. `hold --lease 5 -- python -c "print('ran')"` -> rc=3 claim lost, nothing run.
- Lease live: `take CR-101 --epoch 1 --note "resume: x"` -> rc=3 `CR-101 is held: lease 2 live until 12:56:15; take it again with --reclaim only on the user's word`.
- Expired (expires set to 2020): `lease CR-101` -> `lease 1 of CR-101: not confirmed since 00:10 (3622356 min ago)`; `status` line carries `lease not confirmed since 00:10 (...)`; `take ... --note` -> rc=3 `CR-101: lease 1 not confirmed since 00:10 (...); check with the host that its Driver ended, then take it with --reclaim`.
- `take ... --reclaim` -> `took CR-101 ..., lease 2 until 12:56:15`; events.jsonl: `{"kind": "reclaim", "cr": "CR-101", "lease": 1, "state": "not confirmed"}`; `round CR-101 --lease 1` -> rc=3 `claim lost: ... taken again (lease 2)`.
- Hold past expiry: with lease 2 expired, `lease CR-101 hold --lease 2 -- python child.py chantier lease CR-101`: the child printed `live until 12:56:32 (renewed 12:46:32), held by 1 background task(s)`; after the child, no `.lease-hold` file, `lease CR-101` live (renewed at end).
- `agents set CR-101 - --epoch 1` -> `lease 2 of CR-101: ended at 12:46`.
- QA: `order qa --note "try it"` skeleton has `lease: 1 of O-1 (renew at each wake: lease O-1 renew --lease 1; run a long test under lease O-1 hold --lease 1 -- <command>)`; first `agents set O-1 qa-agent --epoch 1` keeps lease 1; second -> rc=3 `O-1 is held: lease 1 live until 12:57:04; ...`; `agents set O-1 - --epoch 1` ends it; `agents set O-1 qa2 --epoch 1` -> `lease 2 of O-1: live until 12:57:08 ...`; `order done O-1 --epoch 1 --note ok` then `lease O-1` -> `lease 2 of O-1: ended at 12:47`.
- Not hand-run (a stacked batch is needed): `take stack`, stack forms, Copilot `close` causes, long gate and queue ticket: proved by the named tests above.
- Accepted deviation `ended_ok`: after `agents set CR-101 -` ended lease 2, `ship CR-101 <link>` with no `--lease` passed the lease check (failed later on the missing worktree), while `round CR-101` still gave rc=2 `needs --lease`. Matches the PR's Autonomous decisions; it departs from D.2 (an ended lease -> claim lost).

## agents/ unchanged
`git diff --name-only origin/main...HEAD | grep -c agents/` -> `0` (agents/ and com.github.copilot/agents/ untouched).

## Diff vs PR description (work/pr-body.md)
Summary, Deliverables, Changes match the diff (core/leases.py, records, take/round/ship/handback/release/stack/forge-stack/agents/cancel/order drop/status/handoff, close on Copilot, cards, AGENTS.md, docs, scenario, dry-run). Image: none, none owed.
Description pass at db78350 (re-judged): `gh pr view 376` headRefOid = db78350cf36cc696157270dda0dbe1a9f9608112; the posted body equals work/pr-body.md (diff: one trailing blank line only).
Known gaps now holds the `ended_ok` departure ("Departs from the specification: ship, stack and forge-stack accept a unit whose lease ended...") and the `agents set O-k` bullet; both match the hand-run (claim at line 35) and Autonomous decisions. Test plan SHAs are db78350. Review box proven: `log CR-403` note "inspector approved at db78350cf36c... on the code" (and 8bd198b). Renders clean, no images. The one unchecked Test plan item (scenario units locally) is stated as not done, not as fact.

VERIFIED
