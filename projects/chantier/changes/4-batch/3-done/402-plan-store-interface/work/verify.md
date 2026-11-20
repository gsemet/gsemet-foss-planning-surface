# Verify CR-402 (the plan's storage behind a minimal interface)

Head: f5e1365b72fec4604d3078cc729d89d2d33e08d8

All claims judged at f5e1365b (the pushed head; `git status` clean; origin/main = merge base 8bd198b1).

## 1. Spec section 7 tests exist and pass, and the spy catches a missing check - f5e1365b

- `uv run --locked --group dev pytest -q skills/chantier/scripts/cli/tests/test_store_conformance.py skills/chantier/scripts/cli/tests/test_store_command_table.py -rs`
  -> `50 passed, 13 skipped` (11 skipped: `dedicated-branch backend: a later CR (planning-server-Q19)`; 2 skipped: backend does not declare `refuses-without-publisher`, as the spec asks).
- Mutation, in a throwaway `git archive HEAD` copy under the scratch folder (the worktree untouched): replaced `repo.check_publish(stages)` in `commands/intake.py` (`init`) by `pass`, ran
  `PYTHONPATH=<copy>/src pytest <copy>/.../test_store_command_table.py -k init`
  -> `1 failed`: `AssertionError ... assert 'check_publish' in ['make_folder', 'make_folder', ...]`. The copy was removed.

## 2. Table rows call repo.store, check_publish first - f5e1365b (code read, diff origin/main...HEAD)

- file/order qa/fix copy: `filing.new_request` checks folder + `intake/request.md` then `store.make_folder`/`write_bytes`; `crs.filed_fix` checks target, request, `03-change-spec.md` then `write_bytes` copy.
- triage/abandon/restore/moves: `batch.move_directory(repo, ...)` -> `check_publish([source, destination])` then `store.move`; restore checks `restored.json`, `01-intent.md`, `notes.md` before the move; `moveout.remember_cr` writes `restored.json` and the appended line through `write_bytes` (own line endings).
- init: `check_publish(stages)` then `make_folder(..., True)`. open/order add/release: `check_joins` (all sources, targets, `formerly.json`) before the first move; `Batch.__enter__` checks the record path of `open`; `consume` checks. take/round: `_check_take` / `check_publish([work])` before `make_folder`. Rollback: `_rollback_moves` through `store.move`.
- done_cr (handback/release/order merged): checks source, target, `delivery.md`. close: `archive_and_delete` checks archived sources and targets, own files, record and report before any move; `write_close`/`undo_close` through the store. summary set/label/group: `check_publish([... summary.json])` then `store.write`. Board: `write_api` runs each op on `replace(repo, command=<route>)`; `edit_markdown`, `declare_next_batch`, labels/groups, move/new through the same paths; Configuration save: `check_publish([], config=True)` then `repo.store.write_config`.
- Grep of `commands lifecycle summaries playbook board core` for direct write/mkdir/unlink/rename/copy calls outside the store: only local files remain (gate queue, `batch.json`, `brief.md`, seat, `.closing-*` rmtree, `.batch-number`, `.lock`) and the planning folder itself in `init`.
- `.gitignore` written through `store.ensure_gitignore`, never passed to `check_publish`.

## 3. Imports, layering, suite - f5e1365b

- `grep` of imports in `store/*.py`: only stdlib, `chantier.core.errors`, `chantier.core.files`, and `chantier.store.*`.
- `python -I -c "import chantier.store, chantier.core.files; print('pydantic' in sys.modules)"` -> `False` (modules loaded: chantier.core.errors, core.files, store.*).
- `uv run --locked --group dev pytest -q -n auto skills/chantier/scripts/cli/tests` -> `1036 passed, 14 skipped in 92.50s` (machine loaded by other sessions; includes `test_code_targets`, the start-up import test). No existing test file is changed in the diff (only the new `store_spy.py`, `test_store_*.py` added).

## 4. Behaviour and messages vs origin/main (8bd198b1) - f5e1365b

Scratch in-project repo (git init, origin remote = itself), same script on a detached base worktree (code of 8bd198b1) and at the head; paths and timestamps normalized: `init`, `file` x4 (one duplicate refusal, exit 2), `triage` (ok, and a missing folder, exit 1), `abandon`, `restore 6-trash/x` (refusal exit 2), `open` of two CRs, `take`, `order qa`, `order drop`, `status`, `summary set`, `restore` of the trashed folder, and the CRLF bytes of the restored intent.
`diff before.txt after.txt` -> `IDENTICAL` (66 lines, 13 exit-0 commands, the refusals with their exit codes equal).
Not run by hand: `handback` and `close` (need a forge); their output texts are covered by the unchanged existing suite (`test_batch_end`, `test_external_archive`, ...) at 3. and by CI's scenario at this head (reported green by the Driver; not re-run by me). Scratch files and the base worktree were removed.

## 5. PR body vs diff - f5e1365b

- Posted body equals `work/pr-body.md` (`gh pr view 373 --json body | diff` -> no difference except a trailing newline).
- Summary, Deliverables (store/, Repo.store, the protocol), Changes (store/, Repo.store, changes_lock delegation, move_directory, routed writes, both tests, CONTRIBUTING.md `core/` layer line) all match the 32-file diff; no delivered change is unmentioned. Autonomous decisions match the code read (restored.json via `restored_bytes` write_bytes; the appended line in own endings and file created with the line alone; `check_joins` once at entry; close's `CR folder not found` / `ChantierError` put-back; `repo.COMMAND` set in `cli.main` and `command=` per board route). Known gaps lists the skipped backend and feature, the missing `release`/`board ungroup` rows, and the unmeasured test time.
- Note for the Driver: the Test plan still holds `<sha7>` placeholders (Local gates, Review, Verified, CI): fill them at ship. The test-time figures (66.9 s to 81.3 s) were not re-measured by me (my run was under load).
- Review box: not yet filled, so not judged.

VERIFIED

## Description pass at f5e1365b72fec4604d3078cc729d89d2d33e08d8

Head: f5e1365b72fec4604d3078cc729d89d2d33e08d8

- Description (gh pr view 373 --json body) judged against `git diff origin/main...HEAD` (32 files) and the spec at f5e1365: sections in template order, fold with blank lines, nothing after `</details>`, no `issue:` line so no Issues References, no internal reference outside Internal references, Mermaid and code sketch names exist (store/base.py, folder.py, surface.py; `write_config` is in the protocol and named in Human decisions). CONTRIBUTING.md change matches (`git diff` shows the `core/` list line).
- Test plan SHAs: gates `just check` 1036 passed and eval-dry-run 18 of 18 (gates-check.log, gates-evaldry.log); Review: `$CHANTIER log` note "r3 approved at 8bd198b, committed as f5e1365" proves the box's cited SHA; CI: `gh pr checks 373` shows check x3, eval-dry-run, scenario all pass; Verified at f5e1365 (above).
- Known gaps match the notes (skipped backend, missing release/ungroup rows, unmeasured test time); no UNVERIFIED claim, no screenshots.

DESCRIPTION: VERIFIED
