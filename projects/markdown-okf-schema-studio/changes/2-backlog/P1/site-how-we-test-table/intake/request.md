# How we test page: simpler test table and a clearer level name

Filed on the owner's word of 2026-11-27, one of a series of small bugs to put in P1 for the next batch, in French:

> « dans la page how to test ce tableau n'est pas tres lisible. enleve la colonne where
>
> renomme "Simulated bench" par "Real VS Code host" »

Screenshot given with the words: `evidence/how-we-test-table.png`.

Request: on the **How we test** page, the table "Which test proves which requirement" is hard to
read: remove its **Where** column, and rename the level **Simulated bench** (the owner's wording:
"Real VS Code host", see `02-answers.md`).

Facts read at `origin/main` `b9b29c5a`, not decisions:

- The page is `docs/how-we-test.md`. The screenshot stops at the "Simulated bench" row; the next
  rows are "Real VS Code integration", "Acceptance", "Stress" and "Mutation".
- The page says of the simulated bench: no VS Code window opens; Playwright Chromium drives the
  preview page against a mock host.
- The name "Simulated bench" is also a section heading of the page and appears in `CONTRIBUTING.md`
  and `.agents/glossary/common.md`; the figure `images/how-we-test/test-levels.svg` draws the
  levels.
- `test/site/howWeTest.test.ts` requires the page to name every folder of `test/` and
  `sphinx/tests` in a code span: the level sections must still name those the column held.
