# Speed (spec section 6, answer 13) and golden output

Machine: one Windows 11 machine, back to back. Before: worktree CR-418 (a391c1eb). After: CR-419 head
(uncommitted, with the fix below). Prepared folder (a script outside the repo, `build.py`): a git repo
with `.agents/changes/`, 240 synthetic backlog CRs (P1..P4, 60 each: `03-change-spec.md`, a third with
`02-answers.md`, `work/` notes) plus the project's real inbox and backlog (273 backlog summaries read in all),
the running batch-29 (batch.json, events, 20 active CR folders) and 56 archived batch records.

## Commands

- `chantier status`, 5 runs each, alternated before/after:
  `cd <folder>; uv run --no-sync --project <worktree> chantier status`
- `board.state.project_state`, 5 calls in one process (as the board does):
  `Repo.find(<folder>, readonly=True)` then `project_state("p", repo, False, None)`
  (`uv run --no-sync --project <worktree> python ps.py <folder> 5 <out.json>`).

## Figures (round 2, median of 5 runs, seconds)

| | before (CR-418) | head, round 2 |
|---|---|---|
| `chantier status` | 0.577 | 0.585 (+1 %) |
| `project_state` (5 calls, 2 sessions) | 0.851 / 0.876 | 0.895 / 0.902 (+5 %) |

Round 1 shortcut (a folder trusted for one second, across calls) is gone: it let a leaf symlink to a folder
outside the root through. Round 2 keeps no cache across calls. Measured on this machine: `os.lstat` is 21 us
on Windows; a state makes 5706 reads of about 3.9 components, so one `lstat` per component on every read
cost 1.55 s (+78 %). Fix: `FolderStore.reading()`, a per-thread scope that `project_state` opens, in which a
component already checked for a link is not checked again; it ends with the call (nested scopes share it).
`status` opens no scope and pays no measurable cost.

## The fix (worktree, uncommitted)

- `store/base.py`: `inside_path` and `guard` take an optional `resolved_root`; `PlanStore.reading()`.
- `store/folder.py`: root resolved once per store. A read (`_r`: reads, `exists`, `is_file`, `is_dir`,
  `listdir`, `glob`, `stat`, `walk`) checks the `rel` lexically (as the guard does: no `..`, absolute, drive,
  NUL), then `os.lstat` on each component under the root, the leaf included, a symlink or a Windows
  junction (reparse point) sending it to the full guard (`resolve`) with the same refusal and text. An absent
  component stops the walk of components. Writes, moves and removals keep the full guard on every call.
  `walk` guards its top `rel` once and builds the rels from the text.
- Conformance tests: a symlinked leaf folder (a symlink, or a junction where the OS refuses symlinks)
  pointing outside is refused by `exists`, `is_dir`, `is_file`, `listdir`, `stat`, `read_text`, `glob`, `walk`;
  a link made after a `reading()` pass is seen by the next pass.
- Known trade-off: inside one `reading()` pass (a board state), a link swapped into an already checked folder
  is not seen until the pass ends.

## Golden diff

- `chantier status` text, before vs after: identical (round 2 not re-run; code path unchanged), but the `watch: not running` line, which prints the
  `--project <worktree>` path of each tree (41st line); with the two worktree paths normalised, no difference.
- `project_state` JSON (`json.dumps(sort_keys)` of the whole dict, 5 calls each): byte-identical (round 2: `cmp` of both JSON files, identical), with no
  timestamp differing (the prepared folder is unchanged between the runs).
- pytest on the touched modules: `test_store_reads`, `test_store_conformance`, `test_board`, `test_factory`,
  `test_leases`: round 2: 103 passed, 18 skipped (dedicated-branch backend). `ruff check` and `ruff format` on `store/`: clean.

## Re-measured at the restacked head (b3fbfa3, base CR-418 58df3be)

Same folder and machine, back to back, median of 5: `chantier status` 0.585 s before, 0.590 s head (+1 %);
`project_state` 0.833 s before, 0.891 s head (+7 %, under the 10 % limit). Golden output: the board state JSON
is identical; `status` text differs only by the worktree path in the `watch:` line.
