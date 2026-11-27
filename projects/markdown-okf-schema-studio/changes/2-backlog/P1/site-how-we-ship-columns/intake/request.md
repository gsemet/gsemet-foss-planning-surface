# How we ship page: the table columns are too narrow

Filed on the owner's word of 2026-11-27, one of a series of small bugs to put in P1 for the next batch, in French:

> « les colonnes ici doivent etre elargie »

Screenshot given with the words: `evidence/how-we-ship-narrow-columns.png`.

What the screenshot shows: the **How we ship** page of the published site. In the "Who does what"
table a red arrow points at the first column (**Role**), which is so narrow that "Chief of Staff"
and "Release driver" wrap onto two lines. The first column (**Step**) of the next table wraps too
("1. Pick and grill"). Both tables stop at their content and their headers are centred, unlike the
text around them.

Facts read in the code at `origin/main` `b9b29c5a`, not decisions:

- The page is built from `docs/how-we-ship.md` (`test/site/buildSite.ts`).
- The site's table style is in `test/site/siteTheme.ts` (`table{display:block;max-width:100%;overflow-x:auto}`).

Open point for a grill: which columns to widen (the first one only, or the table as a whole), and
whether other pages of the site are concerned.
