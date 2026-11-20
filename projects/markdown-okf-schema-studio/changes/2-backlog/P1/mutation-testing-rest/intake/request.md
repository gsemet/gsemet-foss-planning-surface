# Mutation testing campaign, part 2: everything except core (P1)

Priority: P1, after `mutation-testing` (part 1, `core`) lands. Owner, 2026-11-20: "fait 2 CR, P1 apres la release sur Core et un second sur tout le reste".

Depends on: `mutation-testing` (part 1). Part 1 builds the tool (StrykerJS and the `node:test`
adapter), measures the run time on `core`, and sets the rules for reading the report and for
removing a test. This CR reuses all of that as it is and adds no new tooling, unless part 1's
note says a layer needs one.

## Intent

The same one-shot campaign as part 1, on every other layer that has unit tests:

- `src/page`: about 27k lines, the largest; to be split by folder if part 1's time measure calls for it;
- `src/session`: about 8k lines;
- `src/node-services`, `src/host-vscode`, `src/host-api`, `src/host-memory`: about 4k lines in all;
- the `build` and `site` code that the unit tests reach.

For each layer:
- **First pass.** An agent reads the tests and lists those with no assertion, those that only
  check "does not throw", and near-duplicates.
- **Mutation run.** Read the report (`coveredBy` / `killedBy`):
  - remove or merge the redundant tests, so the suite gets smaller;
  - add tests for the holes that matter;
  - list the holes not worth a test.

## Limits (same as part 1)

- Every requirement stays covered: a test that carries a `@tests_req` marker is removed only
  when a kept test covers the same SwRS, and its marker moves to that test
  (`just requirements-update` stays clean).
- No published requirement is removed.
- The real-window e2e and integration tests are out of scope. Code that only those tests reach
  (`host-vscode` parts) is listed, not mutated.

## Done

- The unit suite is smaller, or no larger, and its mutation score per layer is higher.
- The note for chantier's `mutation-testing-driver` gets its second-case lessons: the time per
  layer, and what changed from part 1. It is sent to the chantier Chief of Staff.
