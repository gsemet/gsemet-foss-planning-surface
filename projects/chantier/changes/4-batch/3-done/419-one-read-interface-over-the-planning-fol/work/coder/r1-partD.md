# Part D, round 1
Changed: hub/{batch_prs,watch,journal,autostart,journal_add,lines}.py; status/{views,write}.py; core/repo.py; core/surface_batches.py; tests forge_world.py, test_event_audience.py, test_event_types.py, test_titles.py.
New signatures: hub journal.read(store, changes); status.views folder_title(store, folder), shown_title(store, recorded, folder), spec_state(store, folder), _backlog(store, paths, start), _past(store, stage, start); status.write._events_by_cr(repo, folder).
Callers outside part D still to update: commands/batch_status.py:270 (journal.read), board/api/topics.py (journal.read), board/crs.py, commands/close_archive.py:129, commands/driver.py:115, commands/facts.py:81 (shown_title(store, ...)), tests test_board_config.py/test_board_journal.py (journal.read).
Gates: ruff format/check on my files pass; mypy: no error in my files; pytest on my tests: only failures from commands/batch_status.py:270.
