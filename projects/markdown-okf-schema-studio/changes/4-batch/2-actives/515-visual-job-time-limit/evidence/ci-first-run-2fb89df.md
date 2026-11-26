# First CI run, pull request 541, head 2fb89df (run 45827873343, attempt 1)

Source: `gh run view 45827873343 --json jobs`, the job logs (`work/ci-45827873343-*.log`) and the
artifact `studio-reports-attempt-1` (`work/scratch/artifacts-45827873343/`).

| Job | Conclusion | startedAt | completedAt | Seconds |
| --- | --- | --- | --- | --- |
| visual | success | 13:18:33Z | 13:25:26Z | 413 |
| visual-2 | success | 13:18:33Z | 13:26:29Z | 476 |
| static | success | 13:18:33Z | 13:25:36Z | 423 |
| static-windows | success | 13:18:33Z | 13:25:56Z | 443 |
| viewer-graph | success | 13:18:33Z | 13:20:48Z | 135 |
| report | success | 13:26:31Z | 13:27:10Z | 39 |
| checks | success | 13:27:13Z | 13:27:16Z | 3 |

`report`, step `just ci-report visual`:

```
visual part 1: passed, 269 scenarios, 343 s
visual part 2: passed, 254 scenarios, 393 s
visual parts: merged
...
ci-report: passed
```

Merged `e2e/screenshots/run-manifest.json`: `status` passed, `partial` false, `parts` 2,
`scenarioCount` 523 (269 + 254), `passedScenarioCount` 523, `failedScenarioCount` 0,
`screenshotCount` 412, `pngCount` 497 (497 PNG files in the folder), `duplicateImages` 0.
The render step of both parts printed `rendered 225 pages, 523 scenarios`.

System packages, both jobs (restore key `apt-archives-visual-Linux-ubuntu26-X64-`, saved by an
earlier run's `visual` job):

```
visual    dev-ci: system packages installed from .cache/apt-archives, no mirror contacted
visual-2  dev-ci: system packages installed from .cache/apt-archives, no mirror contacted
```
