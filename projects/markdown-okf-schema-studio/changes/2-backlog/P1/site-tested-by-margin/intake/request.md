# Requirement pages: the Tested by list has no side margin

Filed on the owner's word of 2026-11-27, one of a series of small bugs to put in P1 for the next batch, in French:

> « manque de marge dans les vue dans https://gsemet.github.io/markdown-okf-schema-studio/requirements/rendering-core/SwRS-MDOKFSTUDIO-CORE-081/ »

Screenshot given with the words: `evidence/tested-by-no-margin.png`.

What the screenshot shows: on a requirement page of the published site, in a scenario card (S1 to
S4), the **Tested by** heading and the test file paths touch the card's left border (a red arrow
points there), and the `UNIT` tags touch its right border. The GIVEN / WHEN / THEN columns above
them do have an inner margin.

Facts read in the code at `origin/main` `b9b29c5a`, not decisions:

- The block is `<div class="scn-tests">` in `test/site/requirementsViewer/pages.ts`.
- `test/site/requirementsViewer/viewer.css` styles `.scn-tests` with a top margin only, and
  `.files li` with vertical padding only.
