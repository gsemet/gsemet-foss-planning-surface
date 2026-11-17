## Summary

A use case (StRS) describes a whole journey, but its requirements (SwRS) are tested one by one, so nobody could see how they chain into the journey the user wants. Each active use case now has a `### Main paths` section: one or two step-by-step paths, each step backed by the SwRS that moves the user to the next state, with the SwRS of the other outcomes at that state as options. A new check keeps those citations honest.

## Deliverables

- 78 of the 80 active StRS have a Main paths section. The two without one (TRUST-012, TRUST-014) have only unrelated constraints, not a path; the reason is in the requirements log.
- `scripts/check_main_paths.py`, run by `just requirements-lint` (so by `just check` and CI), fails when a cited SwRS does not exist, is not active, or does not derive from that StRS.
- The format is documented in `requirements/guidelines/project.guidelines.md`, section "Main paths of a StRS".

```markdown
### Main paths

#### Path 1: <name>

1. <state>
   - SwRS-<ID>: <what moves the reader to the next state>
   - Option SwRS-<ID> (<nominal|boundary|refusal>): <another outcome here>
2. <final state>
```

```
$ uv run --no-sync --group requirements python scripts/check_main_paths.py requirements
main paths: 78 StRS checked, 536 SwRS citations, all valid
```

## Changes

- Check script and its pytest (`test/build/test_check_main_paths.py`, added to `release-tests`), `justfile` wiring, guideline section.
- Main paths written in the StRS files, one commit per scope. Nothing else in those files changes except the approval stamps below; no SwRS, scenario or Links block is touched.
- Dated entry in `requirements/tiers/log.md`.

## Impacts

No visual change. Requirement text only, plus a new lint step.

## Blast radius

Grade: 1. Documentation and a lint step; a revert restores the previous state. The check can only fail CI on a wrong citation.

## Approved requirements changed

16 `approved` StRS got Main paths, with the owner's agreement ("Yes, all 16"): BLOCK-003, BLOCK-025, CORE-001, DIAG-001, DIAG-006, GFM-002, LAYOUT-001, LAYOUT-003, MYST-001, PALETTE-015, REVIEW-001, REVIEW-003, REVIEW-012, REVIEW-015, TABLE-001, TABLE-012. Their `approved_at` was stamped again (`approved_by` is unchanged). Owner review requested.

## Autonomous decisions

- The check script carries no SwRS (owner decision): it is build tooling.
- A path may cite a `draft` SwRS (owner decision).

## Test plan

- [x] New or changed tests (`test/build/test_check_main_paths.py`)
- [x] Requirements: no behaviour change; `just requirements-update` leaves no diff
- [x] Local gates: `just requirements-lint`, `just release-tests` (178 passed), `just requirements-update` (no diff); `just preflight` static and visual stages pass, its local real-window integration step times out on the author machine (no source change in this PR)
- [x] Review (inspector, verifier: mutation checks of the new script confirmed)
- [x] CI green (static on Linux and Windows, visual)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
