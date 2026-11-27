# How we ship page: show the release steps instead of the 1.6.1 timings

Filed on the owner's word of 2026-11-27, one of a series of small bugs to put in P1 for the next batch, in French:

> « cette section dans how we ship n'est pas bien fait. enleve les temps c'est nul. Mais met les etapes:
>
> * travail avec le chief of staff, a la fin il y a un CR de release qui fait la release notes et presente a l'humain
> * l'human approve, la CI fait la release, l'agent monitor et observe l'impact sur le marketplace »

Screenshot given with the words: `evidence/how-we-ship-release-section.png`.

Request: on the **How we ship** page, rewrite the section "Release 1.6.1, hour by hour": remove
the times, and show the steps instead:

1. The work is done with the Chief of Staff; at its end a release change request writes the release
   notes and presents them to the human.
2. The human approves; the CI makes the release; the agent monitors it and watches its effect on
   the Marketplace.

Facts read at `origin/main` `b9b29c5a`, not decisions:

- The section is in `docs/how-we-ship.md` ("## Release 1.6.1, hour by hour"): a swimlane figure,
  `images/how-we-ship/release-1-6-1.svg`, and a table of times and events.
- The page's introduction announces "one real release, 1.6.1", and the next section is "What the
  release taught us".

Open points for a grill: whether the figure is replaced by a new one of the steps or dropped, and
what becomes of the introduction's mention of 1.6.1 and of "What the release taught us".

Related: `site-how-we-ship-columns` (the tables of the same page).
