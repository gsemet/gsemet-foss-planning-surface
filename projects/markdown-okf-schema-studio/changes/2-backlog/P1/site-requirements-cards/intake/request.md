# Requirements page: drop one figure card to get two tidy rows

Filed on the owner's word of 2026-11-27, one of a series of small bugs to put in P1 for the next batch, in French:

> « j'ai quelques bugs placer en P1 encore
>
> page requirements il faut virer un des cartes pour faire 2 jolies lignes. »

Screenshot given with the words: `evidence/requirements-cards.png`.

Request: on the **Requirements** home of the published site, remove one of the cards of "The figures"
so that the cards make two tidy rows.

Facts read in the code at `origin/main` `6b1dd90d`, not decisions:

- `test/site/requirementsViewer/home.ts` draws 11 cards: StRS use cases, SwRS behaviours,
  implemented, tested, fully traceable, SwRS with a marker exemption, known issues, StRS paths
  tested, StRS paths accepted, StRS covered, SwRS scenarios tested. The screenshot shows them five
  per row, the eleventh alone on a third row.
- SwRS-MDOKFSTUDIO-CORE-069 (`req_lifecycle: proposed`) names four of them, in its statement and in
  scenario S5: StRS paths tested, StRS paths accepted, StRS covered, SwRS scenarios tested.
  `test/site/requirementsViewer/home.test.ts` checks them.

Open points for a grill: which card is removed, and whether two rows are wanted at every window
width or at the width of the screenshot.
