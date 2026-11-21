# Part B, round 1
Readers take the store first: read_batch_json, read_events, read_restored_number (core/records.py, 387 lines),
waits.read_file, summaries/store.read/read_or_new, summary_view, gap_of (store first, gaps.py), summary_findings (store first),
title_source (TYPE_CHECKING import), read_record, read_retro; read_seat/last_closed keep repo and read via repo.store.
Callers updated in commands/, lifecycle/, core/batch.py, gate_queue.py (next_merge_cr builds a FolderStore over queue.parent, lazy import, ordered() unchanged),
commands/{driver,facts,close_archive,batch_status} also follow part D's shown_title(store, ...) and journal.read(store, changes).
Tests: test_batch_end, test_came_back, test_leases (incl. fingerprint(found.store, found.changes)), test_order_drop_to.
Gates: ruff format/check clean on my files; mypy clean except 8 errors in test_board_journal.py and test_board_config.py (part D, forge_journal.read call lines);
pytest of my 5 test files green (test_gate_queue_order too).
Left direct on purpose (split-out, spec 284): summaries/sources.py checksums, gaps.py request look, origin.py, core/batch.py _load exists look.
