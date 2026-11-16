# CR-221 coder, round 4

## Done
- `ruff check`: 46 findings to 0, by extracted helpers, dispatch dicts, generators and small dataclasses (`Scope`, `Reading`, `_Req`, `_Part`, `_Chief`). No noqa, no config change. `ruff format --check` clean.
- Every function is at most 50 lines; no file is over 400 lines (`status/views.py` was trimmed back to 400 after the typing edits).
- Behaviour kept: signature changes are `session_costs(..., scope=Scope(...))`, `usage(..., reading=Reading(...))` and `cr_view(repo, d, c, where)`; callers and `tests/test_costs.py` updated. A long test was split in three; two test helpers added.
- mypy --strict started: 430 errors after the refactors, then 186 in 47 files after typing bare `dict`/`list` as `dict[str, Any]`/`list[Any]` and giving `Subparsers` a type-checking alias.
- `just test`: 62 passed. `just scenario` (after the last edit): github 695/695, gitlab 676/676.

## Remaining
| Check | Count |
| --- | --- |
| ruff | 0 |
| mypy --strict | 186 errors in 47 files |
| functions over 50 lines | 0 |
| files over 400 lines | 0 |

mypy kinds: no-untyped-def 85, arg-type 24, no-untyped-call 22, no-any-return 20, union-attr 12, operator 6, assignment 4, type-arg 4, attr-defined 3, return-value 2, others 4 (psutil stubs, fcntl/killpg on Windows, one var-annotated, one misc).

## Notes
- `$CHANTIER rules` was not run.
- The empty untracked `chantier.py` at the worktree root is still there; I did not add it. Nothing is committed.
