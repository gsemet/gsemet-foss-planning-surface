# okfreq: path acceptance marker, declared scenarios, two counters

# okfreq: acceptance tests that walk a StRS main path, declared scenarios, two counters

Feature request from the markdown-okf-schema-studio project (filed 2026-11-23 by its Griller,
from the owner's grill of `markdown-okf-schema-studio/changes/1-inbox/strs-path-validation`).
Forge-neutral (GitHub and GitLab).

## Problem

With `strs_test_coverage_mode: linked-swrs-and-validation-test`, any direct `@tests_req StRS-...`
counts as the StRS's validation test. A marker is a link, not a proof: in the Studio, 93 of 94
live StRS count as validated, yet a 1-in-6 sample of the 185 direct markers
(`markdown-okf-schema-studio/changes/1-inbox/strs-path-validation/experiments/02-audit-sample.md`)
shows only 13 of 31 walk a StRS main path (4 of those a one-step path), 6 photograph one state,
8 repeat one SwRS transition, 3 name a flow that is not a path of the StRS.

## What the Studio needs from okfreq

1. A shared frontmatter field `scenarios:` for both tiers: on a StRS it declares its main paths, on
   a SwRS its transition scenarios. Each entry has a stable short id (`S1`, `S2`, never reused) and
   a title; no `kind` (the tier says what it is). Accepted by the schema (today
   `additionalProperties: false` in places).
2. A third marker, `@accepts_req StRS-X#S<n>`: an end-to-end acceptance test that walks one main
   path of a StRS. The fragment `#S<n>` is also accepted, and optional, on `@tests_req SwRS-X#S<n>`;
   with no fragment `@tests_req` still covers the whole SwRS.
3. Two counters per StRS, by test bench (benches named in the project's config, e.g. a simulated
   bench and the real host): "tested" = its paths have an `@accepts_req` test on the simulated
   bench; "accepted" = on the real bench. SwRS coverage stays as today, shown on each SwRS.
4. A lint: every live StRS declares at least one path; a `#S<n>` names a declared scenario.
5. Help for the migration: declaring `scenarios:` from the existing `### Main paths` /
   `### Scenario` headings, metadata only (approval_lock: the project records one owner agreement
   for that scripted change).

## Out of scope here

The Studio's own migration (sorting the 185 markers, writing the acceptance tests) is the Studio
CR, which waits for this one.
