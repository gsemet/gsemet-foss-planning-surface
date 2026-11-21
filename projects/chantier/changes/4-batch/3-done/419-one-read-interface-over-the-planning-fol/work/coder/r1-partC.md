# Round 1, part C (board/)

Changed (store first, Path kept, rel via rel_in; PlanStore imported under TYPE_CHECKING):
- backlog.py: _candidates, description, count_files, depends_of, grill_of, summary_fields, open_waits, backlog_items(store, changes, rows) (the `.resolve()` of the folder dropped: reads only).
- archived.py recovered_after(store, changes, record); journal.py _lines/since_rescan(store, changes).
- state.py _history(store, changes) (RECORDS.as_posix()), call forms; crs.py (_folder_of, shown_title/count_files/description with repo.store).
- files.py tree/read(store, root, rel), _listed(store, root, folder): walk/stat/is_file/read_bytes(limit); resolve real-place check and core.files.inside kept.
- fingerprint.py fingerprint(store, changes, extra): store.stat/walk/listdir/glob, no file opened; hash differs from before (allowed).
- api/ops.py, api/topics.py (_journal rev via store.stat, _entries(ctx, store, changes)), api/http.py, reads.py, write_api.py, projects.py (check_planning: store.is_dir(".")), config_api.py (_open_batch), costs.py.
- `# direct:` mark: state.py origin_of (code repo folder) and checkout.yml read. board/state.py check_planning etc. no other direct read left outside static/command/key/address.
Tests: test_board_archived, test_board_description, test_board_waits, test_board_prs (fingerprint/since_rescan calls), test_waits (open_waits call; belongs to B's file, call form only).
Gates: ruff format/check on board + my tests pass; mypy: board/ clean; remaining errors are hub journal.read callers in test_board_journal.py:54,93, test_board_config.py:130,231 (part D tests). pytest of my files and server_api*: 93 passed.
Open: tree is red until D/B/E join (read(store, changes) of hub journal; batch_status).
