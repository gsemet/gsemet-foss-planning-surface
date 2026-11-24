# Demo videos, one feature each

## Owner direction (2026-11-24): feature clips for the release notes

The owner's words: "On a déjà une demo video de présentation mais la l'idée c'est de faire des vidéo démo direct d'une feature, que l'on pourra mettre dans la release notes. Cette CR est la préparation de ce qu'il faut faire et mise en place puis on fait 1 vidéo de la nouvelle feature copier collé intelligent avec les delimiteur. Une vidéo dure quelque seconde, doit être focus sur l'avion et le résultat attendu. Et on la converti par exemple en gif ou webm pour la mettre dans la doc et la publier sur tweeter par exemple."

Intent now: a repeatable way to make a feature clip, a few seconds long, focused on the action and its expected result, converted (GIF, WebM or similar) for the docs, the release notes and X. This CR sets up the process and tooling, then makes the first clip: the smart copy-paste with delimiters (copy-raw-edge-balancing, batch-09). The short-demo-01 process and kit (docs/demo-video/) are the base; the older ideas below (horizontal and vertical series, presentation, chapter showcase) are kept as history, not this CR's scope unless the grill says so.


Moved to P3 on 2026-11-04 by the owner, from the backlog item `demo-video` (P2), after the first
video landed. That video, its 15, 40 and 59-second rounds and the guide are done: see archive
`257-demo-process`.

What is left here is the other video ideas: the short horizontal and vertical videos
(`10-short-videos-*`), the longer presentation (`11-demo-presentation`) and the chapter showcase
(`12-chapter-showcase`). A new video follows
`docs/demo-video/guidelines/short-demo-process.guidelines.md`, in its own folder
`docs/demo-video/short-demo-NN/`.

The history below comes from the original item; its "Owner direction" round is the one now done.

## History

Back in the backlog (P2) on 2026-11-03, by the owner, from CR 170 (status blocked, owner-paced).
The full request is [00-request.md](intake/request.md). The three tracks were delivered and wait for the
owner's review: see `STATE-a.md`, `STATE-b.md`, `STATE-c.md` and the branches
`change-requests/170-demo-video-{a,b,c}-assets`, kept as they are.

## Owner direction (2026-11-03, later)

Resume after release 1.3.0 lands. The next round is a framework for every future video, not a
one-off cut:

- A 15-second scenario.
- A visual identity: palette, typography, framing, pacing, transitions, title and end cards.
- The Markdown shown in the renderer is representative of real use, and beautiful.
- The use cases shown are attractive and pleasant to watch.
- A short list of key messages that the video must get across clearly (to agree with the owner
  first).
- Deliverable: the 15-second video plus a reusable guide (identity, scenario template, content
  rules, message checklist) that the next videos follow.

## Key messages (agreed with the owner, 2026-11-03)

The 15-second video gets these three across, in this order:

1. What your agent writes becomes a beautiful page: diagrams and cards, no configuration.
2. You read, comment and edit in the same place.
3. You answer your agent from the page.
