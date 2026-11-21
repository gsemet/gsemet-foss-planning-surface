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

## Figures (median of 5, seconds)

| | before | head, first cut | head, fixed |
|---|---|---|---|
| `chantier status` | 0.568 | 0.570 | 0.563 (-1 %) |
| `project_state` | 0.80 (first call 2.27) | 2.28 (every call) | 0.887 (first call 1.08) |

The first cut of the head was 2.8x slower on `project_state`: the guard resolved the root and the
path (two `Path.resolve`, 2 to 3 `GetFinalPathNameByHandle` each) on each of 5706 reads. Fixed variants,
measured one by one: root resolved once per store (2.28 s to 1.7 s); reads trust a folder checked within
the last second (1.05 s); the walk builds its rels from the text, no `relative_to` (0.92 s); a folder not yet
checked is vouched for by a checked ancestor plus one `lstat` per plain name below it (0.89 s vs 0.83 to 0.86 s
before in the same session: within noise, under 10 %). Timings of this machine are noisy (single runs 0.78 to 1.2 s).

## The fix (worktree, uncommitted)

- `store/base.py`: `inside_path` and `guard` take an optional `resolved_root`.
- `store/folder.py`: `FolderStore` keeps `root.resolve()` once; a read-only `_r` (reads, `exists`, `is_file`,
  `is_dir`, `listdir`, `glob`, `stat`, `walk`) skips the resolve for a plain `rel` whose folder, or an
  ancestor, was checked in the last second and has no symlink below it; a symlinked leaf read for its content
  gets the full guard. Writes, moves and removals keep the full guard on every call. `walk` builds each rel
  from the text.
- Known trade-off: a symlink or junction swapped into a checked folder within one second is not seen by a read
  (a Windows junction under a checked folder, `os.path.islink` not seeing it); writes are unaffected. Worth
  stating in the PR's Known gaps.

## Golden diff

- `chantier status` text, before vs after: identical, but the `watch: not running` line, which prints the
  `--project <worktree>` path of each tree (41st line); with the two worktree paths normalised, no difference.
- `project_state` JSON (`json.dumps(sort_keys)` of the whole dict, 5 calls each): byte-identical, with no
  timestamp differing (the prepared folder is unchanged between the runs).
- pytest on the touched modules: `test_store_reads`, `test_store_conformance`, `test_board`, `test_factory`,
  `test_leases`: 99 passed, 16 skipped (symlink-dependent). `ruff check` and `ruff format` on `store/`: clean.
