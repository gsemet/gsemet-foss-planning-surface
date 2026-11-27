# Requirements page: show where @tests_req and @accepts_req sit

Filed on the owner's word of 2026-11-27, one of a series of small bugs to put in P1 for the next batch, in French:

> « aussi juste au dessus il faut expliquer ou se place les acceptances tests (@accepts_req) les tests (@tests_req sur SwRS et StRS). les test_req semble pointer vers les implements_req, met 2 boites avec @tests_req, une pour SwRS (pour expliquer que ca valide une transition dans un test d'integration), et une dans un StRS pour expliquer que ca valide un scenario en environmement virtuel (+ rapide) »

Screenshot given with the words: `evidence/requirements-how-it-works.png`.

Request: on the **Requirements** home of the published site, the "How it works" section (just above "The figures") explains where the acceptance tests (`@accepts_req`) and the tests (`@tests_req`, on a SwRS and on a StRS) sit. In the figure, `@tests_req` seems to point at `@implements_req`: draw two `@tests_req` boxes instead:

1. one for the **SwRS**, explaining (owner's words) that it validates a transition in an integration test;
2. one for the **StRS**, explaining that it validates a scenario in a virtual environment (faster).

Facts read in the code at `origin/main` `6b1dd90d`, not decisions:

- `test/site/requirementsViewer/home.ts`: `diagram()` draws four boxes in one row (StRS, SwRS, Code `@implements_req`, Test `@tests_req`) with an arrow from each to the next, so the last arrow goes from Code to Test; a dashed box of cross-cutting rules points at SwRS. The SVG's `<desc>` and the hint above name `@implements_req` and `@tests_req` only: `@accepts_req` appears nowhere in the section.
- `requirements/guidelines/project.guidelines.md` "Benches": `@tests_req <StRS>#S<n>` is a path walked on the simulated bench, outside `test/integration/`, on every pull request; `@accepts_req <StRS>#S<n>` is a path walked end to end in real VS Code, under `test/integration/`, on every push to `main`; `@accepts_req` never targets a SwRS.
- Same file, "Scenario and path markers": `@tests_req <SwRS>#S<n>` names the one scenario a test checks; no rule ties it to a kind of test, and `docs/how-we-test.md` lists several levels.
- At that commit, 354 of the 5767 `@tests_req SwRS-…` marker lines of `src/`, `test/`, `tests/` and `sphinx/` sit under `test/integration/` (`git grep`).
- SwRS-MDOKFSTUDIO-CORE-069 (`req_lifecycle: proposed`): the home "draws the chain from use case to test". `test/site/requirementsViewer/home.test.ts` checks that the section holds an SVG with `@implements_req` and `@tests_req`.

Open points for a grill:

- The words of the SwRS box: « une transition dans un test d'integration » against the rules, where a SwRS scenario may be checked by a unit, contract, simulated or real VS Code test.
- Where the `@accepts_req` box sits and what it says.

Related: `site-requirements-cards` (the figures of the same page), `strs-acceptance-remaining-groups` (every StRS path shows Tested by and Accepted by), `site-how-we-test-table` (names of the test levels).
