# Conflicts: rebase of CR-409 onto origin/main (c51aea6a)

Conflicts were all in the first commit (f184ed02, typed waits); the second (scenario) applied cleanly.
Rule everywhere: keep both sides.

- AGENTS.md (CLI scope): main added the `lease` exception paragraph, CR-409 the `wait` one. Kept the
  lease paragraph as is and appended `wait` as "And one more" after it (main's text on the "rescan" cost
  unchanged, the duplicated sentence from CR-409's side dropped).
- commands/batch_status.py (`_cr_row`): main moved the working-row tail into `_working_tail` (with the
  lease check); CR-409 added `wait_view.status_segment`. Kept `row += wait_view.status_segment(repo, c)`
  then `if c.status == "working": row += _working_tail(...)`; CR-409's inlined copy of the old tail dropped.
- commands/driver.py imports: both `from chantier.commands.waits import add_to_cr` and
  `from chantier.core import leases`, in sorted order.
- core/records.py (`CrEntry`): both fields, `lease: Lease | None` and `waits: list[dict[str, Any]]`.
- declare/driver.py: `_register_lease(sub)` and `_register_wait(sub)` both called; `_register_wait` kept.
  Not a conflict but a gate failure after the merge: `_register_record` grew to 53 lines (size test),
  so `note`, `phase` and `log` moved into a new `_register_notes` (same registration order).
- lifecycle/moveout.py import: `from chantier.core import leases, waits`.
- tests/test_validate.py: both sides' new cases kept: main's long-title/heading cases and tests, and
  CR-409's "bad waits" case and `test_a_waits_file_of_the_backlog_is_ok`.

No file started with a byte-order mark before or after; none added.

Fast gate: `just check` in the worktree (after the rebase and the `_register_notes` split), result:
pass, 1199 passed, 14 skipped, release-notes ok. First run failed only on
`test_files_and_functions_are_small_and_the_imports_have_no_cycle` (`_register_record` 53 lines), fixed
as above. Log: work/gates/conflict-resolver-check.log. `just eval-dry-run` not run (Driver's step).
