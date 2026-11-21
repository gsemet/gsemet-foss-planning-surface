# Answers

Short name: `viewer-ids`

## Owner's answers, 2026-11-21 (asked by the Chief of Staff; the Griller session was blocked on its question)

- viewer-ids-Q1 (search). Owner: "Plus sans les zéros": the full ID and the short ID, any case, find the page; an exact ID match comes first and Enter opens it; a number without leading zeros (`block-14`) also finds BLOCK-014.
- viewer-ids-Q2 (title: eyebrow, browser tab, X share card). Owner: "ID complet partout": "Use case StRS-MDOKFSTUDIO-BLOCK-003: …" in the eyebrow, the tab and the share card; same for an SwRS. With the owner's 2026-11-20 words "utilise StRS-MDOKFSTUDIO-BLOCK-014 a la place pour les liens partout": every link to a requirement on the site shows the full ID (captions, graph steps, lists, breadcrumb, titles).
- viewer-ids-Q3 (breadcrumb). Owner: "Tous les requirements": every requirement in the breadcrumb in full ID.
- viewer-ids-Q4 (graph overlaps): dropped, it is its own item `requirements-path-graph-design` (separate design session).
- viewer-ids-Q5 (split): moot: requirements-share-cards already shipped as CR-443 in v1.11.0.
- Owner, 2026-11-21: "Et tout ça partira dans le batch en cours": once final and ready, added to batch-07.

## Owner's answers to the spec's open questions, 2026-11-21 (asked by the Chief of Staff)

- viewer-ids-Q6 (short ID shared by a use case and a behaviour, e.g. BLOCK-014). Owner: "Le cas d'usage": the use case first, Enter opens it; the behaviour right under it.
- viewer-ids-Q7 (headings of the results when ID matches come first). Owner: "Titres habituels": keep the usual kind headings (Use cases, Behaviours), even if one appears twice; no extra "exact match" heading.
- viewer-ids-Q8 (eyebrow). Owner: "Type + ID seulement": `Use case StRS-MDOKFSTUDIO-BLOCK-003` above the h1; the title is not repeated.
- viewer-ids-Q9 (a bare number such as `14`). Owner: "Oui, le nombre seul suffit": a bare number counts as an ID match and lists every requirement ending in that number first (it may push text hits down or out).

## Settled by the Chief of Staff

- Share card title: viewer-ids-Q2 already named the X share card with the format `Use case <full ID>: <title>`; the spec's change of the share title stands (supersedes share-cards-Q9's order for the title).
- Pager links: covered by viewer-ids-Q2 "every link to a requirement shows the full ID"; the previous/next link text carries the full ID.
