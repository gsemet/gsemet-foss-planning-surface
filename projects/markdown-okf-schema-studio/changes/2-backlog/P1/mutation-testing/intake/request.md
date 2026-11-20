# Mutation testing campaign, part 1: `core` (P1, after the 1.10.0 release)

Priority: P1, after the 1.10.0 release (CR-434), for the next batch.

**Split (owner, 2026-11-20: "fait 2 CR, P1 apres la release sur Core et un second sur tout le reste").**
This CR runs the campaign on `src/core` and its tests only. It builds the tool (StrykerJS and the
`node:test` adapter), measures the real run time, and writes the note for chantier. The second CR,
`mutation-testing-rest`, runs the same campaign on everything else and starts after this one lands.

Owner's request, 2026-11-20: "comment faire du
mutation testing efficace dans Studio ?", then: "le but est un peu double: ameliorer les tests
de Studio; donner les instructions pour que Chantier fasse un Mutation Testing Driver", "ce que
tu proipose on dirait que c est pas du one shot, cest sur une PR on a un job ou un tache de
mutation testing et pas on va faire du mutation testing pour reduire le nombre de test actuels",
then: "je te demande qqu chose de one-shot et tu me dis que c'est PR par PR".

## Intent

**A one-shot campaign, not a job on every PR.** Studio runs mutation testing once over its
existing code and tests, acts on the result, and is done. A mutant is a small change to the
code (a `<` into `<=`, a `true` into `false`, a deleted call). A test that never kills a mutant
proves little, and a mutant that no test kills shows a hole.

Two goals:

1. **Improve Studio's tests, and reduce their number.**
   - Find the redundant tests: tests that kill no mutant that other tests do not already kill.
     Remove them, or merge them into fewer tests.
   - Find the holes: surviving mutants in code that matters. Add the few tests they call for.
   - The result is a smaller suite that catches as much or more.
2. **Give chantier the instructions for a Mutation Testing Driver.** Studio's campaign is the
   first case. It ends with a note on how such a campaign was run, which chantier uses to write
   that role (filed in chantier's inbox as `mutation-testing-driver`). The note covers:
   - the command;
   - the scope;
   - the report and how it was read;
   - the rules for removing a test;
   - the time it took.

## Limits

- **Every requirement stays covered.** A test that carries a `@tests_req` marker is removed only
  when another test that stays covers the same SwRS, and its marker moves to that test. The
  coverage must stay intact (`just requirements-update`).
- **No published requirement is removed.**
- **Scope.** `src/core` (about 30k lines, 156 files) and the unit and contract tests that reach it.
  Not the real-window e2e tests.

## What exists today (main 049b543)

- About 70k lines of TypeScript in `src/`. Unit tests run on `node:test` over the compiled
  `out/` and take a few minutes. There is no mutation tool yet.

## Feasibility (measured 2026-11-20, main 049b543)

- **Size.** `core` + `page` hold about 57k lines, which gives an estimated 15–25k mutants. The unit
  suite has 4,138 tests and runs in 63 s.
- **Run time.**
  - A naive run (the whole suite for each mutant) takes about two weeks: not workable.
  - With per-test coverage (only the tests that reach the mutant), it takes about 1–3 s per
    mutant: roughly 10–15 h on one process, 2–3 h on 8 workers. Workable.
- **The crux.** StrykerJS has no `node:test` runner with per-test coverage. A small adapter, or
  another runner, is the first risk of the CR.
- **Reading the result.** Stryker's JSON report gives, for each mutant, the tests that reach it
  (`coveredBy`) and the tests that kill it (`killedBy`). From that report:
  - a test that reaches code but never kills a mutant checks nothing useful;
  - a test whose every kill is also made by other tests is redundant;
  - a mutant that no test kills is a hole.
- **Cheap first pass.** Before the mutation run, an agent reads the tests (about an hour) for:
  - tests with no assertion;
  - tests that only check "does not throw";
  - near-duplicate tests.
- **Order.** Run `core` first (30k lines), to validate the adapter and measure the real run time,
  then everything else in the second CR (`mutation-testing-rest`).

## Points for the grill

0. **Settled by the owner (2026-11-20, "je suis d accord").** A one-shot campaign that removes
   or merges redundant tests and fills the holes; first an agent reads the tests, then the
   mutation run.
1. **Tool.**
   - StrykerJS with a TypeScript checker, run locally or as a one-off CI dispatch.
   - Open point: how to run `node:test` so that each mutant runs only the tests that reach it.
2. **Reading the result.**
   - A score per layer and per SwRS requirement.
   - The list of redundant tests, by killed mutants.
   - Logs and message strings left out.
3. **Shape of the change.**
   - Removals and merges in one PR or by layer.
   - The new tests for the holes that matter.
   - The few holes judged not worth a test, listed rather than tested.
4. **Budget.**
   - Time of the full run.
   - How much of the suite to run per mutant.
