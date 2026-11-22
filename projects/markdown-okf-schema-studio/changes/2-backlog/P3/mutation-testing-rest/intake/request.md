# Mutation testing: one campaign on the whole code, one night, one CR (P3)

Owner, 2026-11-22: "On fera tout d'un coup, sur une nuit et une CR unique. Met tout ce qui concerne
les mutation tests en P3 avec les conclusions et analyses de cet essai."

This CR replaces both `mutation-testing-core-finish` (filed and dropped the same day) and the
earlier plan of a part 2 split by layer. The original part 2 request is kept below as history.

## Scope

One CR, one overnight run of every layer that has unit tests: the whole of `src/core` (not a
sample), `src/session`, `src/page`, `src/node-services`, `src/host-api`, `src/host-memory`,
`src/host-vscode` (the parts the unit tests reach) and the `build` and `site` code the unit tests
reach. The tool of CR-450 (`just mutation-core`) is extended to the other layers, or a sibling
target is added; no other new tooling.

## Removal rule: prudent (owner, 2026-11-22: "Prudente")

- remove only a test that kills no mutant on the full run (not "load-time coverage only");
- merge near-duplicates into a table-driven test that keeps every assertion;
- keep a focused unit test even when a broad test (render pipeline, features) kills the same
  mutants: a focused test says where it broke;
- keep regression and boundary tests; a `@tests_req` marker moves only to a kept test of the same
  SwRS, `just requirements-update` stays clean, and no published requirement is removed.

## Holes

Fill the holes that matter, by cluster, weakest folders first; list the holes not worth a test
(equivalent mutants, by reading). No folder score drops.

## Conclusions and analysis of the trial (CR-450, PR #461, merged 2026-11-21)

Evidence: `4-batch/3-done/450-mutation-testing/evidence/` (`mutation-campaign-note.md`,
`holes-core.md`, `redundant-tests-core.md`, `r3-rerun.md`). The run logs and the Stryker
incremental file lived in the CR-450 worktree, removed at merge; the branch
`chantier/batch-07/cr-450-mutation-testing-campaign-on-src-core-re` stays on the forge.

What worked:
- The tool runs on Windows with TypeScript 7 (own `node:test` runner with per-test coverage, own
  TS 7 checker, message-string ignorer); a second phase checks whether another layer's tests kill
  a core hole.
- Time: 0.66 s of wall time per mutant at 15 workers; 51 files, 6,007 mutants in 91 min. The whole
  of `src/core` is projected at about 7.5 h (about 29,000 mutants). Compile errors are 28% of
  mutants and cost a check but no test run.
- Holes found are real: round 3 added `*.holes.test.ts` on 25 clusters and killed 319 of 416
  holes. Scores rose: mapping 62 to 93%, navigation 72 to 95%, protocol 77.5 to 99%, frontmatter
  52 to 74%, comments 80 to 91%.

What the sample showed:
- Start score 70%. 1,289 holes, of which 1,254 are killed by no test anywhere.
- Much more holes than fat: only 75 removal candidates out of about 1,400 core tests (about 5%).
  The main gain of a campaign is filling holes, slimming the suite is a small one.
- 118 "zero-kill" tests, of which 97 were a measurement artefact (load-time coverage of module
  constants credited to every test of a file); the reader now classes them "not judged".
- Weak folders left as they were: palette 3.3%, export 57%, paste 58.5%, edits 68.5%.
- Many "redundant" candidates are focused tests whose mutants a broad test also kills (e.g. the
  blank-line tests vs the render pipeline): hence the prudent rule.

What was not done:
- No test removed; the core suite grew from 1,396 to 1,475 tests.
- Every reading is on a sample (51 of 162 files); no removal is final before a full run.

Time to plan for one night: `src/core` about 7.5 h alone; `src/page` (about 27k lines) is the
largest layer, so the night may not hold everything: measure `src/page` first on one folder, and
say in the PR what did not fit.

Lessons for the Driver (from the campaign note): name the sample and keep it; never edit `test/`
or `src/` while a run lives; run in the background and poll the log; read the load-time warning
before acting on zero-kill; work by hole cluster, not by single mutant; re-run only the touched
folders with the same files for the after figures.

## Done

- Score per layer and per sub-folder, before and after, in the PR.
- The unit suite is no larger, net of new hole tests, removals and merges, or the PR says why.
- The lessons for chantier's `mutation-testing-driver` note, sent to the chantier Chief of Staff.

---

## History: the original part 2 request

### Mutation testing campaign, part 2: everything except core (P1)

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
