# Intent

Split, 2026-11-20, by the Chief of Staff from `one-read-interface-over-the-planning-fol` (CR-419,
merged 2026-11-21 in PR 394; its answers 4, 6 and 11 name this item). Not grilled: on 2026-11-21
the user delegated the night's specification questions ("plus de question"); the open choices are
the specification's numbered questions, each written on its recommendation.

The user's goal, carried from CR-419: the surface server "lit les fichiers mais on va bientot lui
donner une persistance pour etre plus rapide (dolt?)"; "poser des bases solides pour permettre ca
plus tard". CR-419 gave the plan's store (`store/`, `PlanStore`) its read half and moved onto it
the board, the hub, `status` and the record readers they call; a static structure test
(`tests/test_store_reads.py`) follows that list.

What is left:

- The other modules that read the planning folder with no store: `lifecycle/`, `core/batch.py`,
  `core/leases.py`, `gate_queue.py`, `gate_slots.py`, the rest of `summaries/` (`sources.py`,
  `gaps.py`, `origin.py`, `title.py`), `rails.py`, `history.py` and `commands/`. They join the
  structure test's list as they move.
- A proof at run time, beside the static test: while the board builds a project's state, while
  `status` runs and while the hub runs one cycle, on a prepared surface, no file of the planning
  folder is opened or listed outside a store method (an audit hook on `open`, `os.listdir` and
  `os.scandir`). It can pass only once what those three reach has moved.
- The configuration: whether the store, which already owns the project's file (`config_path`,
  `write_config`), also reads it, or its reads stay with `playbook/`.

Not built: an index or a cache. No behaviour or output changes. One batch CR of at most 3 rounds
(CR-419's rule): what does not fit is named, not built.
