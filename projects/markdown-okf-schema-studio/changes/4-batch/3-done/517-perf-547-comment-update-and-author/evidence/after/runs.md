# CR-517 "after" runs of the `perf-547` scenario

Head 44a2e9365a238ba8cd813dece5645b66665551e3 (PR #550). Job `perf-547`,
`gh workflow run ci.yml --ref <CR branch> -f perf_547=true`, Linux runner, VS Code 1.148.0,
preview 671 x 799, generated document 464 lines, 3114 elements, 9 threads before and 21 after.

Compared sets:

- Lower CR: the three "after" runs of CR-516 (45918715713, 45918718450, 45918721402, head
  e52cd28), `../../516-perf-547-slow-comment-selection/evidence/after/`. Their test folder was not
  a Git repository.
- Same test folder: the three runs of this CR's measure commit 7d24547 (45928962519, 45928965278,
  45928968671), `../measure-ci/`. Test folder a Git repository with a user name, comment update
  behaviour of the lower CR.

## Medians per interaction (ms; each value is the median of one run's samples)

| Interaction | Run 45947065460 | Run 45947068376 | Run 45947071021 | Median of runs | Lower CR, 3 runs | Same test folder, 3 runs |
| --- | --- | --- | --- | --- | --- | --- |
| Comment creation | 32.4 | 35.4 | 23.7 | 32.4 | 47.1 / 45.9 / 37.1 (45.9) | 46.6 / 35.2 / 35.5 (35.5) |
| Selection release | 16.9 | 16.65 | 3.6 | 16.65 | 18.2 / 17.65 / 18.05 (18.05) | 17.45 / 17.8 / 18.05 (17.8) |
| Longest task, text drag | 2.16 | 2.29 | 1.92 | 2.16 | 2.72 / 2.68 / 2.62 (2.68) | 2.97 / 2.30 / 1.95 (2.30) |
| Longest task, cell drag | 2.22 | 2.18 | 1.87 | 2.18 | 2.54 / 3.40 / 2.71 (2.71) | 2.81 / 2.09 / 2.41 (2.41) |
| Longest task, text release | 2.21 | 1.98 | 1.98 | 1.98 | 2.41 / 2.55 / 2.92 (2.55) | 2.33 / 2.19 / 2.21 (2.21) |
| Longest task, cell release | 2.28 | 2.44 | 2.10 | 2.28 | 2.73 / 2.92 / 2.91 (2.91) | 2.68 / 2.48 / 2.32 (2.48) |
| Elements restyled by one comment creation | 4 | 4 | 4 | 4 | 41 / 41 / 41 | 41 / 41 / 41 |

Verdicts:

- Elements restyled by one comment creation: drops from 41 to 4 in every run.
- Comment creation: lower than all three runs of the lower CR, but the sets of the same test folder
  overlap (35.4 against 35.2 ms): not separable from runner noise.
- Selection release: not separable from runner noise. Every set holds samples near 4 ms and near
  17 ms; the median of a run follows the count of each (run 45947071021: 12 of 14 near 4 ms).
- Longest tasks of drags and releases: each median of runs is at or below that of both compared
  sets; dragging and releasing post no thread list, and the runs overlap those of the same test
  folder: not separable from runner noise.
- No interaction got slower.

## `authorWait` (ms, wait of one comment write for the Git user name)

| Run | Samples | Median |
| --- | --- | --- |
| 45947065460 | 9.45, 9.66, 9.41, 6.71, 6.8, 6.77, 5.25, 4.65, 6.59, 6.76, 6.79, 6.79 | 6.78 |
| 45947068376 | 12.46, 12, 12.27, 12.86, 11.79, 36.15, 7.88, 7.81, 7.61, 7.75, 7.44, 7.59 | 9.83 |
| 45947071021 | 12.74, 13.11, 13.96, 8.91, 9.17, 8.54, 7.93, 7.85, 8.31, 8.33, 8.79, 8.78 | 8.79 |

Median of the runs 8.79 ms, median of all 36 samples 8.32 ms. The measure runs at 7d24547, on
which the decision not to cache the name was taken: 10.74, 8.69, 6.79 ms (median of runs 8.69).

## `threadIndex` (ms, medians, plain Node v24 on the runner)

| Run | Document | `createDocumentIndex` | `reanchorThreads` | `commentCreate` of the run |
| --- | --- | --- | --- | --- |
| 45947065460 | 464 lines, 64579 bytes, 9 threads | 1.41 | 1.96 | 32.4 |
| 45947068376 | same | 1.41 | 1.74 | 35.4 |
| 45947071021 | same | 1.04 | 1.35 | 23.7 |
| 45947065460 | 1856 lines, 261223 bytes, 36 threads | 5.62 | 8.94 | not measured at this size |
| 45947068376 | same | 5.48 | 8.35 | not measured at this size |
| 45947071021 | same | 4.20 | 6.37 | not measured at this size |

At 7d24547 (same code of the index): 1.77/2.11, 1.41/1.75, 1.21/1.55 and 7.00/10.28, 5.53/8.36,
4.79/7.70.

## User actions on which the host runs these two functions

As read in the code (`src/session/features/comments.ts`; this change does not alter when the two
functions run, it only times the Git name wait in that file).
`createDocumentIndex` is "index", `reanchorThreads` (which indexes too) is "re-anchor".

| User action, on a previewed document | What runs |
| --- | --- |
| First preview of a document that has comments, or a preview switching to one | index and re-anchor all threads |
| Preview page reloaded or restored | threads posted again; re-anchored only when no result is kept for that text |
| Comment created, answered, resolved or deleted | index and re-anchor all threads, once per write for each preview of the document; nothing when the last thread is deleted |
| Comments file created or changed outside the preview | index and re-anchor all threads |
| First change of a document with no unsaved changes (first keystroke or paste, reload, revert) | index and re-anchor all threads |
| Undo or redo | index and re-anchor all threads |
| Later typing while a thread is orphaned | index, and re-anchor the orphaned threads |
| Every save | index, even with no comments file; re-anchor when the comments file is valid; nothing when the comments file has unsaved changes in an editor. A save that moves stored lines while a thread is orphaned indexes a second time, to place the orphans again |

A save indexes and re-anchors once, however many previews of the document are open; everything
else in the table, the second index of a save included, runs once for each open preview. Apart from
the save, a document without comment threads runs neither function. While a document has unsaved
changes and no thread is orphaned, further typing does not index again.

Raw reports: `perf-547-run-<run id>.json` in this folder. Run URLs:
`https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/<run id>`.

## Issue 547

Drag and release never block for more than 50 ms in these runs (largest sample 9.21 ms), as in the
lower CR's runs: the slow text selection is not reproduced. Comment creation has no target; this
change's gain on it is not separable from runner noise. The PR references the issue and does not
close it.
