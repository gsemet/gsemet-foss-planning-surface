# CR-515: before and after

- Before: base `b9a1abd074ab34ba49920448315c86452d80d832`
- After: head `2fb89df9c1d19c9e882702f7b2f8328ccc105ae8`

The change touches CI, its scripts, its tests and the contributor documents only. Nothing visible
changes, so no screenshot is captured. The pairs below are command outputs.

## Pair 1: duration of the visual jobs

| | Run | Job | Duration |
| --- | --- | --- | --- |
| Before | 45825388443 (`main`, base) | `visual` | 877 s |
| After | 45827873343 attempt 1 (pull request, head) | `visual` | 413 s |
| After | 45827873343 attempt 1 | `visual-2` | 476 s |

Shows: each of the two jobs ends far from the 900 s limit, where the single job ended 23 s under it.

Reproduce, once per run id:
`gh api repos/gsemet/markdown-okf-schema-studio/actions/runs/<run id>/jobs --jq '.jobs[] | [.name, .conclusion, .started_at, .completed_at] | @tsv'`

## Pair 2: content of the visual campaign

Before: artifact `e2e-visual` of run 45825388443. After: artifact `studio-reports-attempt-1` of run
45827873343 (the merged reports).

| | Before | After |
| --- | --- | --- |
| Scenarios, passed, failed | 523, 523, 0 | 523, 523, 0 |
| Captures (step, final screenshot) | 497 (85, 412) | 497 (85, 412) |
| Machine check rows | 2092 | 2092 |
| Parts in the manifest | none | 1 and 2 |
| Table breakout report, first-gap and width-margins files | 1, 56, 12 | 1, 56, 12 |

Same scenario identifiers in the same order; no difference in the capture files, machine checks,
capture flag, status or assertion keys of any scenario. `MACHINE-CHECKS.md` is identical;
`INDEX.md` differs by its revision line only. The only added files are the six per-part reports.

Reproduce: download both artifacts as zip files, then
`python -I -B <work folder>/verifier/compare_runs.py <before zip> <after zip>`.

## Pair 3: the new and changed tests

Test files: `test/build/test_visual_parts.py`, `test/build/test_workflows.py`,
`test/build/test_select_e2e_run.py`.

| Code under test | Tests | Output |
| --- | --- | --- |
| Base | the base's own `test_workflows.py` and `test_select_e2e_run.py` (control) | `142 passed` |
| Base | the head's `test_workflows.py` and `test_select_e2e_run.py` | `18 failed, 137 passed` |
| Base | the head's `test_visual_parts.py` | collection error, `ModuleNotFoundError: No module named 'capture_report'` |
| Head | the three head files | `184 passed` |

Reproduce: add a detached worktree of the base, run the base's own tests, copy the three test files
of the head into it, and run
`uv run --directory <worktree> --no-sync --group docs --group release --group requirements python -B -m pytest <test files> -q -p no:cacheprovider`
(`<worktree>` supplies the environment; the test file paths point into the base worktree).

## The conditional local check of the plan

The specification asks for a local `just ci-visual` and `just ci-report visual` on Linux or macOS only if
such a machine is available, and otherwise names the first CI run as the proof. None is available, so
no pair is missing: pairs 1 and 2 are that proof.
