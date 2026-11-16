# Rebase conflicts, CR-264

Rebase onto origin/main 33fc800, commit 9c42166 (now rewritten), one conflicted file.

## scenario/run_scenario.py, one hunk (end of `scenario(w)`)
- Main (CR-254): `section_end()`, the flat list of case calls is gone (cases run as UNITS).
- This CR: the old flat list with `base_from_pr(w)` added.
- Choice: main's side. `base_from_pr` is registered the main way: added to the `stack` unit's case list (after `stack_batch`) in `UNITS`, and to the cases name table (`"base_from_pr": base_from_pr`). The function body and its other edits merged cleanly.
- A BOM crept in while resolving (caught by `test_no_tracked_file_starts_with_a_utf8_byte_order_mark`); removed, commit amended.

## Gate
`just check`: pass (100 pytest, ruff, mypy, biome, lock, release notes). Full `just scenario` not run. Nothing pushed.
