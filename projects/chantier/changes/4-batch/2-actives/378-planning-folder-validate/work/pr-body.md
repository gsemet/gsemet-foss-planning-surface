## Summary

A planning folder (a surface's project folder, or a project's own `.agents/changes/`) had no check of its own: a surface kept a drifting script of its own. `chantier validate` now checks the whole folder, read-only, and tells whether it follows chantier's layout and stays readable by the board. Gaps (to fix, nothing breaks) pass with their count shown; errors (chantier or the board misreads the folder) fail.

## Deliverables

```text
chantier [--project <folder>] validate
no error, no gap (<k> CRs)                  exit 0
<m> gap(s) in <k> CRs                       exit 0
<n> error(s), <m> gap(s) in <k> CRs         exit 3, then `error <path>: ...` lines, then `gap <path>: ...`
could not run                               exit 1, `error: <cause>` on stderr
```

| Area | Stages | Findings |
|---|---|---|
| Placement | all | errors |
| `summary.json` format | all | error when unreadable, gaps otherwise |
| Missing or late summary (same lines as `summary lint`) | live | gaps |
| CR folder shape | live | gaps, errors for a file/folder kind mismatch |
| Broken links between Markdown files (exact-case) | live and top level | gaps |

Real run from the planning surface, one per project, read-only (first line, exit code; no error line anywhere):

| Project | First line | Exit |
|---|---|---|
| `agentic-planning-surface` | `7 gap(s) in 3 CRs` | 0 |
| `chantier` | `14 gap(s) in 364 CRs` | 0 |
| `markdown-okf-schema-studio` | `22 gap(s) in 407 CRs` | 0 |
| `okf-schema` | `1 gap(s) in 1 CRs` | 0 |

## Blast radius

Grade: 1. A new read-only command; the one moved function (`gap_line`) keeps `summary lint`'s output byte for byte. A `git revert` restores the previous behaviour.

## Autonomous decisions

None.

## Known gaps

- The measured `just test` time on Windows grew from 37.4 s to 46.1 s (about 9 s).

<details>
<summary>Details</summary>

## Changes

- New `validate` command (`declare/validate.py`, `commands/validate.py`), listed in `cli.py` and in its full-output set.
- `lifecycle/layout_check.py` (placement, shape), `lifecycle/links.py` (links), `summaries/format.py` (summary format).
- `summaries/gaps.py` gains `gap_line`, shared with `summary lint`.
- Docs: `AGENTS.md`, `concepts.md`, `docs/planning-folder.md`, `scenario/README.md`; tests `test_validate.py` and scenario units.

## Impacts

No visual change. A surface can call `chantier validate` instead of its own script.

## Test plan

- [x] New or changed tests (`test_validate.py`)
- [x] Local gates at `224d067`: `just check` pass, `just eval-dry-run` pass
- [x] Evidence: real run on the chantier project, `14 gap(s) in 364 CRs`
- [x] Review: approved at `224d067`
- [x] Verified at `224d067`
- [x] CI green at `224d067`: 3x `just check`, `just eval-dry-run`, `just scenario`

## Internal references

CR-378 planning-folder-validate. Coder notes: work/r1.md.

</details>
