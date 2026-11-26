# CR-516 "before" runs of the `perf-547` scenario

Head 1fc952897df11915ce2b4f060414fde732567d17 (base origin/main 1953eaa; part 1 only, no change
to `src/`). Job `perf-547`, `gh workflow run ci.yml -f perf_547=true`, Linux runner, VS Code
1.148.0, preview 671 x 799. Generated document: 464 lines, 22 tables, 197 rows, 11 images,
9 threads, 3114 elements.

Each value is the median of one run's samples.

| Measure | Run 45895473044 | Run 45895477080 | Run 45896724578 | Median of runs | Largest sample |
| --- | --- | --- | --- | --- | --- |
| Elements restyled by one comment creation | 3109 | 3109 | 3109 | 3109 | 3111 |
| Selection release (ms) | 17.8 | 18.45 | 17.75 | 17.8 | 25.3 |
| Comment creation (ms) | 53.4 | 51.0 | 53.9 | 53.4 | 454.4 |
| Longest task, text drag (ms) | 2.65 | 2.46 | 2.66 | 2.65 | 5.76 |
| Longest task, cell drag (ms) | 2.64 | 2.62 | 2.69 | 2.64 | 12.26 |
| Longest task, text release (ms) | 2.28 | 2.41 | 2.17 | 2.28 | 2.68 |
| Longest task, cell release (ms) | 2.62 | 2.79 | 2.60 | 2.62 | 4.54 |

Raw reports: `perf-547-run-<run id>.json` in this folder. Run URLs:
`https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/<run id>`.

Item 4 verdict: no drag or release blocks for more than 50 ms in any sample of the three runs
(largest 12.26 ms). The slowness of a drag or a release is not reproduced in a real window.

Not counted: run 45895468941, whose `perf-547` job failed before the window opened
(`ETIMEDOUT 150.171.110.194:443` while resolving the VS Code version); run 45896724578 replaces it.
