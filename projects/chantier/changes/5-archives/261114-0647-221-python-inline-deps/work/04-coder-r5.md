# CR-221 coder, round 5

## Done
- `mypy --strict`: 186 errors in 47 files to 0 ("Success: no issues found in 77 source files"). Config not loosened.
- Real annotations: `args: argparse.Namespace` on every command; a `Bad` callable alias in `playbook/config.py`; `HasData` Protocol in `rails.py` (replaces the `SimpleNamespace` mismatches); `normalize_cr` overloads; `Iterator`/`Iterable`/`Popen[bytes]`/`IO[str]` and tuple/set type arguments; typed test helpers.
- `Repo` gained `project_folder`, `surface_root`, `clone` (non-optional, raise if not external) in place of the `Path | None` attributes used where external.
- Platform facts handled without `# type: ignore`: `try_lock` has an `else` branch for fcntl, `stop_group` tests `sys.platform` directly (killpg), `--with types-psutil` added to the mypy line of the justfile.
- No `# type: ignore` added anywhere.
- Behaviour kept (small guards only: `forge_stack._pr_parts` helper, `since is not None` in the heartbeat text, `steering_word`/`shape_word` accept None).

## Remaining
| Check | Count |
| --- | --- |
| mypy --strict | 0 |
| ruff check / format | 0 / clean |
| functions over 50 lines | 0 |
| files over 400 lines | 0 |

## Gates
- `just check`: passes (ruff, mypy, uv lock check, 62 tests, release notes).
- `just scenario`: github 695/695, gitlab 676/676.
- `just eval-dry-run`: 7 of 7 cases as expected.

## Not done
- Reading the batch record through the pydantic models instead of `Batch.data`: not cheap (`Batch.data` is a dict read by name in about every command and view); left for a later round.
- The empty untracked `chantier.py` at the worktree root is still there; not added. Nothing is committed.
