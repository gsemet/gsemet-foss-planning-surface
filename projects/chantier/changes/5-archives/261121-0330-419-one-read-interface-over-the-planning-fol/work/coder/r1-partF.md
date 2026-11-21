# Part F
- mypy: 4 calls fixed (test_board_journal, test_board_config) to journal.read(store, changes).
- tests/test_store_reads.py: ast test (receiver name holding "store" = store), EXEMPT table by (module, function) with reasons ("*" for the whole module), stale-exemption check, parametrized prepared-source cases. Leftovers found: only core/repo.py (read_keyed, surface_projects, Repo.find, _external, missing_clone + import of read_text), status/views.py _documents (code-repo file), all spec 5.5 in kind: exempted. board/config_api.py needs no entry (no direct read left).
- CONTRIBUTING.md: spec 7 sentence added (CRLF file kept).
- Docs search: no sentence made false.
- Caused by CR, fixed: test_code_targets cycle check now ignores `if TYPE_CHECKING:` blocks (core.files -> store -> core.files); test_leases.py back to 400 lines via batch_helpers.batch_of(repo).
- just lint (ruff format/check, mypy, lock, biome): pass. just test: 1443 passed, 18 skipped, 78 s (first run 111 s).
- Stray: an empty file `.git_tmp_edit.py` may sit in C:/Users/gaeta/Projets/ (my mistaken command); rm was refused; user to delete.
