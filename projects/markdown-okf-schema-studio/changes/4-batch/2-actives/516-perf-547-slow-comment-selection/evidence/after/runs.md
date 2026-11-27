# CR-516 "after" runs of the `perf-547` scenario, against the "before" runs

Head e52cd28a16a65201a4df800ae6b69667d0a4bef3. Same job, runner kind, VS Code 1.148.0, preview
671 x 799 and generated document (3114 elements, 9 threads before, 21 after) as
`../before/runs.md`.

Each run value is the median of that run's samples.

| Measure | Run 45918715713 | Run 45918718450 | Run 45918721402 | Median of runs, after | Median of runs, before | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| Elements restyled by one comment creation | 41 | 41 | 41 | 41 | 3109 | drops |
| Comment creation (ms) | 47.1 | 45.9 | 37.1 | 45.9 | 53.4 | faster: runs do not overlap |
| Selection release (ms) | 18.2 | 17.65 | 18.05 | 18.05 | 17.8 | not separable from runner noise |
| Longest task, text drag (ms) | 2.72 | 2.68 | 2.62 | 2.68 | 2.65 | not separable from runner noise |
| Longest task, cell drag (ms) | 2.54 | 3.40 | 2.71 | 2.71 | 2.64 | not separable from runner noise |
| Longest task, text release (ms) | 2.41 | 2.55 | 2.92 | 2.55 | 2.28 | not separable: the sets touch at 2.41 ms |
| Longest task, cell release (ms) | 2.73 | 2.92 | 2.91 | 2.91 | 2.62 | not separable: the sets overlap (2.73 to 2.79 ms) |

Run values before (runs 45895473044, 45895477080, 45896724578), for the overlap: comment creation
53.4, 51.0, 53.9; selection release 17.8, 18.45, 17.75; text drag 2.65, 2.46, 2.66; cell drag
2.64, 2.62, 2.69; text release 2.28, 2.41, 2.17; cell release 2.62, 2.79, 2.60.

Largest samples after: restyle 44; comment creation 78.1 ms (before 454.4); any longest task
4.9 ms (before 12.26), far under the 50 ms threshold of item 4.

The two release longest tasks have medians about 0.3 ms higher after the change. The runs of the
two sets touch or overlap, so no slowdown is separated from the spread of the runners; no cause was
searched for a difference of that size.

Raw reports: `perf-547-run-<run id>.json` in this folder. Run URLs:
`https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/<run id>`.
