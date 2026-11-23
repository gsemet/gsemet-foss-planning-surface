# okfreq: acceptance markers, declared scenarios, two counters per StRS

Type: feat (okfreq, requirements) · Filed 2026-11-23 by the Griller of markdown-okf-schema-studio from the owner's grill ([request](intake/request.md)) · Forge-neutral (GitHub and GitLab)

## Intent

Let a project state, and `okfreq` measure, that a StRS is proved by tests that walk its main paths,
not by a bare link: declare the paths (StRS) and the transition scenarios (SwRS) in one shared
frontmatter field `scenarios:` with stable ids; add the marker `@accepts_req StRS-X#S<n>` for an
end-to-end acceptance test; report two counters per StRS by test bench ("tested" on the simulated
bench, "accepted" on the real one); lint the declarations; help migrate existing requirements.

## Starting point (checked 2026-11-23)

- `okfreq` knows two markers, `@implements_req` and `@tests_req` (`markers:` of `config.yml`, scan in
  `marker_scan`, `src/okf_schema/okfreq/core.py`). A direct `@tests_req StRS-X` is the StRS
  "validation test" of `strs_test_coverage_mode: linked-swrs-and-validation-test`.
- The Studio counts 93 of 94 live StRS as validated; a 1-in-6 sample shows 13 of 31 markers walk a
  path ([audit](../../../markdown-okf-schema-studio/changes/2-backlog/P2/strs-path-validation/experiments/02-audit-sample.md)).
- The base frontmatter schema accepts extra properties (`additionalProperties: true`); the tier
  schemas, the report schema and the config schema are to check.
- The Studio CR `strs-path-validation` is blocked by this one.

## Open

Everything below the request's five points: see `02-answers.md`.
