# The rest of the CLI's readers onto the plan's store

Split, 2026-11-20, by the Chief of Staff from `one-read-interface-over-the-planning-fol` (its answer 4: that CR is kept to one batch CR of at most 3 rounds; the user asks no questions that day).

That CR gives the plan's store (`store/`, `PlanStore`) its read half and moves onto it the direct reads of `board/`, `hub/`, `status/`, `commands/cost/`, `core/surface_batches.py`, `core/repo.py` and of the record readers they call (`core/records.py`, `core/seat.py`, `core/waits.py`, `core/batch_records.py`, `summaries/store.py`, `summaries/view.py`, `core/files.title_source`). Its structure test (`tests/test_store_reads.py`) follows that list only.

What is left, for this item:

- The other modules that read the planning folder with no store, as measured at main on 2026-11-20 (calls of a `Path` or `os` read, the reads of other places included): `lifecycle/` (`stages.py` 16, `layout_check.py` 17, `backlog.py` 10, `links.py`, `moveout.py`, `filing.py`), `core/batch.py` 10, `core/leases.py` 5, `gate_queue.py` 4, `gate_slots.py` 3, `summaries/` (`sources.py` 4, `gaps.py` 2, `origin.py` 2, `title.py` 2), `rails.py` 2, `history.py` 1, and `commands/` (75 over the package, `crs.py` and `factory.py` first). They join the structure test's list as they move.
- A proof at run time, beside the static test: while the board builds a project's state, while `status` runs and while the hub runs one cycle, on a prepared surface, no file of the planning folder is opened or listed outside a store method (an audit hook on `open`, `os.listdir` and `os.scandir`). It can pass only once the modules above have moved.
- The configuration (the intent names it): its files are outside the planning folder (`chantier.yaml` at the project's root, at the surface's root and in the project's folder, and the shipped defaults), read by `playbook/layers.py` and `playbook/edit.py`. To judge: whether the store, which already owns the project's file (`config_path`, `write_config`), also reads it, or the configuration stays with `playbook/`.

Not built: an index or a cache. No behaviour or output changes.
