# CR-429: fingerprint calls and CPU of a served board, one page open, 60 s

Head: `c9c0852` plus the round-3 working tree (uncommitted at the time of the measure); base:
`7c1d890` (the commit before CR-429). Windows 11, Python 3.15, 2026-11-21.

## Method

`fp_measure.py` (this folder) builds the board's push loop in one process, on the live planning
surface (`gsemet-foss-planning-surface`, four projects), read-only: no socket, no forge hub, no
writer. It subscribes the four topics of one board page (`board`, then `project`, `costs` and
`prs` of `chantier`) and lets the push thread run for 60 s. It counts every call of
`board.fingerprint.fingerprint` and the process CPU. At the head it also starts the file watch as
the board does (`ctx.settle` per project, then `FileWatchThread`).

Two stubs apply to both runs:
- The forge connectors fail at once, so there is no `gh` call and no network.
- The live cost (`board.costs.compute`) returns a constant. On a running batch, a page triggers
  the 5-minute rule, which parses the session transcripts once: about 30 s of CPU in a
  short-lived thread, the same at base and head. A first run without this stub hid the difference
  (base 68%, head 75 to 89% of a core); the per-thread figures showed the cause.

The live surface was not idle. Batch-30 was running, so its Foreman and Drivers rewrote every
CR's `STATUS.json` and `STATUS.md` and the gate logs. At the head, each of the 4 fingerprints
after startup is a settle of `chantier` that real changes caused: 864 changed paths in the
minute. The base walks every pass whether anything changed or not.

## Results (60 s after startup)

| | base `7c1d890` | head `c9c0852`+ |
|---|---|---|
| file watch | none (a walk per topic read) | notify (ReadDirectoryChangesW) |
| push passes in 60 s (due every 2 s) | 11 (each ran about 5.5 s) | 33 |
| fingerprints after startup | 70 | 4 (each a settle on a real change) |
| time in fingerprints | 37.7 s | 2.1 s |
| per fingerprint | 539 ms | 535 ms |
| process CPU | 38.3 s, 63.8% of one core | 4.75 s, 7.9% of one core |
| CPU of the push thread | 38.3 s | 2.6 s |
| startup fingerprints | 7 (3.4 s) | 4 (6.4 s, one per project) |

A quiet pass at the head, with nothing settling, costs 21 ms for the four topics (cProfile of 5
passes: 0.104 s, `work/scratch/fp_profile.py`). Most of it is `server.json`'s writer entry
(`psutil` status) and the projects' list. Neither is a walk.

The audit's figure (0.65 to 1 s of work per 2 s pass, 194 ms per walk of chantier alone) matches
the base here. Under a running batch, chantier's planning folder has grown to about 540 ms per
walk; at the base the push loop could not keep its 2 s pace.

Raw output: `fp-cache-measure-base.json`, `fp-cache-measure-head.json`.
