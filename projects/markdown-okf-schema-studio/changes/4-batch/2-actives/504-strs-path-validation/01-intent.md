# StRS validation tests that walk each main path end to end

Type: feat (test, requirements) · Filed 2026-11-23 by a Griller session from the owner's idea ([request](intake/request.md))

## Intent

Prove each StRS use case as a whole: an end-to-end test walks one "Main path" of a StRS from its
first step to its final result, including the steps no SwRS tests, without repeating the SwRS
tests that check each transition alone. Trace these tests to the StRS (and its path) with a
marker okfreq can tell apart from `@tests_req`, and report a StRS's coverage as its validation
tests plus the coverage of each of its SwRS.

Final aim: use this project as the proving ground for a feature request to okf-schema (okfreq)
itself, written forge-neutral (GitHub and GitLab).

## Starting point (checked 2026-11-23)

- `requirements/config.yml`: `strs_test_coverage_mode: linked-swrs-and-validation-test` already
  makes one direct `@tests_req StRS-...` the StRS "validation test".
- 185 such markers in 62 test files, naming 93 of 152 StRS; 93 StRS have a "Main paths" section,
  151 paths in all.
- Sampled visual scenarios put a StRS and a SwRS marker on one single-state snapshot: today's
  "validation" count likely overstates what walks a path.
- Some paths hold a human step: StRS-MDOKFSTUDIO-CORE-007 path 1, step 3 (the maintainer reviews
  the release notes).

## Open

What "validation" means here (V&V), the method per path, the anti-duplicate rule, the marker,
the fate of the 185 existing markers, the cost (one e2e per path), the status shape, and the
destination (audit, project CR, okf-schema request): see `02-answers.md`.
