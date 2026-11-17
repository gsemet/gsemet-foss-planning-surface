# Report — lifecycle-generic-split

Status: **done** (2026-11-05, branch `change-requests/263-lifecycle-generic-split`, PR #326, merge commit `e20c6432`).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | The change request process is split into a generic process guideline and project guidelines by theme (local worktree, owner review, pull request, stacked PRs); `AGENTS.md` and the constitution set the precedence; vocabulary aligned on Chantier 0.5.0 without adopting it | `f321681e`, `e20c6432` |

## Proof of completion

- Tests added: `test/build/test_guideline_isolation.py` (9 passed; failed on the old guidelines); `test/build/test_generate_orchestrator.py` updated (15 passed).
- `just check` exit 0 at the final head; CI run 42129343609 green (`static`, `static-windows`, `visual`, `report`, `checks`).
- Three rounds: two driver rounds plus one round on the owner's critical review. `just preflight` was not run locally.

## Open items

- Folder rename of `.agents/changes/`: done by the main session after the merge (old names kept as temporary symlinks).
- `approved_on` still appears in the okfreq skills (the schema field is `approved_at`).
- Two line-wrap nits (lifecycle guideline, `CONTRIBUTING.md`) and partly overlapping isolation tests.
