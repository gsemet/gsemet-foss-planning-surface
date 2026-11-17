# Answers

The reference picture: `intake/reference.jpg` (a card "Where the money went", by model).

- money-Q1 (where): the Costs page, for the latest batch by default. The user asked whether there is
  a new history page: there is none; CR-327 (merged) added the batch navigator (`‹ batch-n ›`,
  "Latest") on the Costs page, so the card follows the batch the navigator shows, the latest by
  default, a past one when chosen.
- money-Q2 (breakdown): by model by default, with a switch (top right, as in the picture) to show
  the same card by role.
- money-Q3 (the bar's span): from $0 to the batch's budget, the unspent rest hatched, and the line
  says "$X of the budget left unspent"; a batch with no budget: the bar spans the spend.
- money-Q4 (an older closed batch): from now on the close records the per-model and per-role
  figures in the batch's record; a batch closed before shows "not recorded for this batch", as the
  receipt does.
- money-Q5 (what it counts): everything. The batch's spend (Foreman, Drivers, workers) makes the
  bar's segments; the Chief of Staff (steering and grill, outside the budget) is one grey row of
  its own under the models, with no segment in the bar.
- money-Q6 (columns): as in the picture, colour swatch, provider logo, model name and version, the
  number of calls, and the cost; the calls column is labelled "turns" (not "runs").
- money-Q7 (logos): the providers' real logos (SVG icons), as in the picture.
- money-Q8 (logo source): vendor the marks of Lobe Icons (MIT, coloured, as in the picture) as
  inline SVG, with their licence file beside them and a docs line that the marks are their owners'
  trademarks.
- money-Q9 (providers): Anthropic (Claude, on both hosts; Copilot's Claude models show as Claude),
  OpenAI (GPT), Google (Gemini) and xAI (Grok) get a logo and a parsed name; any other model shows
  its exact id with no logo, never a guessed one.
- money-Q10 (colour): one colour per model, from a fixed palette in cost order (Opus and Sonnet stay
  apart in the bar).