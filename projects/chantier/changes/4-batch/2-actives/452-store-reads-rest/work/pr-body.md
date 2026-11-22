## Summary

Moves the last readers of the planning folder that the board, `status` and the hub reach onto the plan's store (`repo.store`): the whole `lifecycle/` package, `core/batch.py`, `core/leases.py`, `gate_queue.py`, `gate_slots.py`, `rails.py`, `history.py`, `summaries/{sources,gaps,origin,title}.py`, `commands/crs.py`. Adds `tests/test_store_runtime.py`, a run-time proof (audit hook) that the board, `status` and the hub open or list no planning-folder file outside the store. No behaviour or output change; no index, no cache.

## Deliverables

- Readers moved (spec §5.2); `tests/test_store_reads.py` lists them, with `EXEMPT` entries for the worktree looks and the held gate lock's text (§5.3, §5.4).
- `tests/test_store_runtime.py` (§6).
- `CONTRIBUTING.md` sentence (§8).

## Review

- [ ] Inspector

## Known gaps

- The 20 other modules of `commands/` (60 calls) still read directly; nothing is filed for them (store-reads-Q2 (b)).
- Speed timing (spec §7) not yet stated.
