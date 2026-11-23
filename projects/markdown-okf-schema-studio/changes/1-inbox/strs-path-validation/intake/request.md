# StRS validation tests that walk each main path end to end

# StRS validation tests that walk each StRS main path end to end

Owner's idea (2026-11-23, filed by a Griller session):

Add validation tests at the StRS level: end-to-end tests that run the complete scenarios
the StRS describe (their "Main paths"), without duplicating the SwRS tests that check the
transitions one by one. The complete user journey has value because it holds steps the SwRS
do not test.

Traceability through okfreq with a dedicated marker, `@validates_req`; the coverage of a
StRS = its validation tests + the coverage of each of its SwRS.

End goal: validate this use case in the Studio, to support a feature request to okf-schema
(okfreq) itself. Everything stays forge-neutral (GitHub and GitLab).

Context checked in the repository on 2026-11-23:

- `requirements/config.yml` already sets `strs_test_coverage_mode: linked-swrs-and-validation-test`:
  a StRS is covered when each SwRS has a `@tests_req` and at least one direct
  `@tests_req StRS-...` exists.
- 185 `@tests_req StRS-...` markers in 62 files under `test/` (36 files in
  `test/integration`, 10 in `test/integration/realInput`, 8 in `test/visual`; 65 markers in
  `test/visual/scenarioDefinitions1.ts` and `2.ts`), naming 93 distinct StRS.
- 152 StRS documents, 93 with a "Main paths" section, 151 paths in all.
- Sampled visual scenarios carry a StRS and a SwRS marker on the same single-state snapshot
  (e.g. `preview-sticky-headings-1`, `okf-schema-dark`, `schema-validation-error-dark`): they
  photograph one state, they do not walk a path.
