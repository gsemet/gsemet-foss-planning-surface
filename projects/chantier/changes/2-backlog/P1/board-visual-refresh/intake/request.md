# Web board: a lighter, more elegant visual style

Filed 2026-11-15 by the Chief of Staff, the user's words (French, translated): "Analyse the attached
image to see the style of the menu, the typography... which I find very elegant, and compare it with
the current web board, because I find it very beautiful. The current board is very beautiful but it
deserves to be a little lighter and even more elegant."

The reference is a mock-up of an automation app ("Optima"), saved with this request as
`reference.png`. Its traits, read by the Chief of Staff:

- One modern sans-serif (Inter-like), two weights (regular, medium); medium-size titles; section
  captions in small grey capitals with letter spacing (MENU, PROJECTS, OTHERS).
- A white sidebar separated by a hairline; thin monochrome outline icons; tall, airy rows; the
  active item a light grey pill with no border; almost no counters, one pastel "New" badge;
  projects marked by a small coloured square.
- Almost monochrome, with one deep teal accent for the primary buttons; state colours only in tiny
  icons.
- Two-tone cards: a white body and a grey band at the bottom for metadata; large radius, faint
  border, diffuse shadow; grey chips with no border.
- A breadcrumb header (grey parents, dark current page) with a status chip; text-only tabs told
  apart by weight; a discreet dotted grid under the canvas.

The current board, compared (tokens.css, the Triage and Batch views):

- Segoe UI at 14px, a 30px bold title; a grey sidebar whose active item is white with a border;
  a counter on every nav row.
- Many colours: eight states each with a tinted border and fill, coloured tags, three mode colours,
  an eight-dot legend row in the Batch view.
- Cards hold their metadata in the same block as their title; the Triage "modified" tags are
  clipped at the top edge of the post-its (a visual bug).
- A line of counters and pills in the header, no breadcrumb.

Suggested directions, by effect (to grill, not decided):

1. One accent colour; states as a small dot or icon instead of tinted borders and fills; the
   legend in a tooltip.
2. The sidebar: white with a hairline, the active item a grey pill, thin icons, counters lighter or
   only where they serve, section captions in small capitals.
3. Two-tone cards: title on white, metadata (files, raw, labels) in a grey bottom band; larger
   radius, softer shadow.
4. Type: titles 24-26px semi-bold, two weights; Inter only if the board ships the font itself (the
   CLI needs no network).
5. Neutral grey chips with no border; colour kept on the CR id.
6. A "Project / View" breadcrumb; the counters as quieter text.
7. A dotted grid under the Batch view's graph.
8. Fix the clipped "modified" tags.

Related: the inbox item `board-triage-polish`.
