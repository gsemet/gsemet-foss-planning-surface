## Summary

The requirements bundle moves to okf-schema 0.18.1, which lets a requirement declare the paths or scenarios a test must name (`#S<n>`) and adds the `@accepts_req` marker for acceptance tests. This PR keeps the current StRS coverage mode and prepares the declarations: the bundle schemas and configuration, the exemption of retired requirements, and a marker check that understands the new marker and the `#S<n>` fragments.

Work in progress: the scenario declarations, the marker sort and the viewer land in later commits of this PR.

## Deliverables

The marker check gains six rules and a baseline for StRS markers still in integration tests:

| Rule | What it rejects |
| --- | --- |
| `fragment-undeclared` | a `#S<n>` the target does not declare |
| `fragment-required` | a fragmentless marker on a target that declares `scenarios:` |
| `fragment-unexpected` | a fragment on a target with no `scenarios:` |
| `accepts-on-swrs` | `@accepts_req` on a SwRS |
| `accepts-placement` | `@accepts_req` outside the files the config allows |
| `strs-tests-in-integration` | a new `@tests_req StRS-...` in `test/integration` (46 files, 101 lines are baselined and must be emptied) |

Choices made:

- The coverage mode is not switched here; the old mode keeps working with the new schemas.
- The 97 retired SwRS get an explicit exemption so they declare no scenarios.
- A new SwRS (`SwRS-MDOKFSTUDIO-CORE-096`) states the behaviour of the marker check, each rule tested by its own test.

## Blast radius

Grade: **2**. The check script, the bundle schemas and the Python lock change; a `git revert` restores the previous state, but the new schemas and the exemptions must go back together.

## Autonomous decisions

- The migration script that will declare `scenarios:` is proven on a scratch copy and is not applied yet: a group can only be migrated once its markers carry the fragments.
- The new SwRS keeps the legacy scenario headings until the viewer reads the new ones.
- Exemption reasons of the retired SwRS reuse one generic text per kind of retirement.

## Known gaps

- The scenarios, the renamed headings, the marker sort and the viewer are not in this commit.
- Nine test files sit at the 1500-line limit and must be split before their markers gain fragments.

<details>
<summary>Details</summary>

## Changes

- `pyproject.toml`, `uv.lock`: `okf-schema>=0.18.1`.
- `requirements/config.yml`: `markers.accepts: '@accepts_req'` and the generated `accepted_in_files` field.
- `requirements/tiers/_schema/{base,strs,swrs}.schema.yaml`: `scenarios`, `acceptance_exemption`, `tested_in_files`, `accepted_in_files`.
- 97 retired SwRS files: `annotation_exemption` and its reason.
- `scripts/check-marker-companions.mjs`, `scripts/marker-baseline.json`: the rules above.
- `test/build/checkMarkers.test.ts`: seven new tests; `test/build/test_check_main_paths.py`: a `Path S1:` case.
- `requirements/tiers/swrs/rendering-core/SwRS-MDOKFSTUDIO-CORE-096.md` (new) and its regenerated StRS and index; `requirements/tiers/log.md`.

## Human decisions

- Paths of a StRS and scenarios of a SwRS share one `scenarios:` field with stable ids `S<n>`, never reused, and the fragment `#S<n>` on both markers.
- Acceptance tests use a distinct marker, `@accepts_req`.
- Headings are renamed to `Path S<n>:` and `Scenario S<n>:`.
- The scripted rename of the 15 approved StRS headings is agreed; their re-approval is the owner's review of this PR.
- A SwRS never declares a scenario that is not tested.

## Impacts

No visual change. Contributors see the new marker rules in `just check`.

## Test plan

- [ ] New or changed tests (they fail on the previous code): six of the thirteen marker-check tests fail on the old script
- [ ] Local gates at `<sha7>`: `just check`, `just release-tests`, `just requirements-lint`
- [ ] Evidence: none for a visible change
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

- CR-504 strs-path-validation (batch-09), `work/coder/r1.md`, `evidence/migration-report.json`, `evidence/line-budget.md`.

</details>
