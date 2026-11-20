## Summary

A shared rule (for example a lifecycle or block-table rule) is relied on by many stakeholder requirements (StRS). Until now a StRS that cited such a rule in its `### Main paths` section also had to derive it, so the rule showed as a child of up to ten StRS. The Main paths checker now also accepts a cited software requirement (SwRS) that the StRS lists in its own `depends_on`, so shared rules can be cited without being derived.

## Deliverables

Rule applied by `scripts/check_main_paths.py` to each SwRS cited in a StRS's Main paths:

| Cited SwRS is... | Before | After |
| --- | --- | --- |
| missing | error | error |
| not active (`deprecated`, `superseded`) | error | error (including when only listed in `depends_on`) |
| active, in the StRS's `derives_from` link | valid | valid |
| active, listed in the StRS's `depends_on` | error | valid |
| active, neither derived nor depended on | error | error: `does not derive from <StRS> and is not in its depends_on` |

## Changes

- `scripts/check_main_paths.py`: reads the citing StRS's `depends_on` (list or single string) and accepts a cited SwRS found there; the error message and the module docstring name both ways.
- `requirements/guidelines/project.guidelines.md` ("Main paths of a StRS"): the citation rule allows `depends_on`, and says a shared rule is cited with `depends_on` rather than derived by every StRS that relies on it.
- `test/build/test_check_main_paths.py`: cases for a `depends_on` citation (valid), an active SwRS neither derived nor depended on (error with the new message) and a superseded `depends_on` SwRS (error).
- `requirements/tiers/log.md`: dated entry for the guideline change.
- No requirement is moved or edited.

## Impacts

No visual change. Requirements authors may cite a `depends_on` SwRS in Main paths; the current bundle's citations are all still valid.

## Blast radius

Grade: **1**. Only the Main paths lint and its guideline change, and the check only gets more permissive for `depends_on`. A plain `git revert` restores the previous rule.

## Autonomous decisions

- The change is logged in `requirements/tiers/log.md` because the project instructions ask for an entry on edits under `requirements/`.

## Known gaps

None.

## Test plan

- [x] New or changed tests (they fail on the previous code): `test/build/test_check_main_paths.py`, 12 passed at `72eb59f`.
- [x] Requirements: no behaviour change (no SwRS added or moved; `just requirements-lint` unchanged count: 78 StRS, 536 citations, all valid, at `72eb59f`).
- [x] Changelog: no user-facing change.
- [x] Local gates: `just preflight` passed at `72eb59f` (on Windows its static stage only; the other stages run in CI).
- [x] Review: approved at `72eb59f` (the restack onto CR-340 re-reviewed; patch carried from `f16dbc3`)
- [x] Verified at `72eb59f`
- [x] CI green at `72eb59f` (checks, report, static, static-windows, visual pass; the other jobs are skipped by their conditions)

## Internal references

CR-341 req-main-paths-depends-on (batch batch-06).
