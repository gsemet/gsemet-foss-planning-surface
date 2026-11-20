The owner shared requirement pages of the published site on X (2026-11-20): the index and the
MyST category show title and text but no image; a use case page (MYST-005) and a behaviour page
(CORE-022) show no card at all. The owner wants: a category page to say it is a feature category
of the extension; each requirement page its own text; one generic image per category (all MyST
pages share one).

Investigation (`work/investigation.md`): the live tags are correct; X most likely cached failed
crawls. Real defects: the `/requirements` stub has no tags; images are per level, not per
category; descriptions are not written for sharing.

Done when: every requirement page has its own title and text, one image per category (and one for
the index), the `/requirements` stub has a card, all checked by build tests; a reshare with a
`?v=` query shows the cards on X.
