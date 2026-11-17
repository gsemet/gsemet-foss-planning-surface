# Answers

## timing-Q1: in this batch

2026-11-17, the user chose the recommended answer: timing-settings joins the next batch, with the eleven retro points of batch-22, cost-receipt and board-visual-refresh.

## timing-Q2: the Configuration page's Timing tab

2026-11-17, after two screenshots (`mockups/timing-table.html`, `mockups/timing-cards.html`), the user chose option 2, not the recommended table: a card per host, a band per model family (or context: subagent, session) inside, each setting with its value; a value set in chantier.yaml stands out from a shipped default. The tab sits beside Models, in the style of board-visual-refresh.

## timing-Q3: granularity

2026-11-17, the user chose the recommended answer: host × model family (and, on Claude Code, subagent or session), with a general value each column may override.

## timing-Q4: which settings

2026-11-17, the user chose "the main ones only", not the recommended all: the prompt cache's TTL, the wakes (steering, Driver) and the CI retries' maximum. Every other wait or maximum stays where it is.

## timing-Q5: the tab after the design critique

2026-11-17, in the combined mock-up the tab keeps a card per host, but each setting shows once with one value column per model family (or context), instead of a band per family repeating every setting; the legend (shipped default, set in chantier.yaml) sits beside the tabs. The user approved it as the specification's reference, to compare at delivery: board-visual-refresh's `mockups/final-config.html`.

Spec critic: yes, it adds configuration the CLI reads and changes the loops' waits and what the Configuration page shows and writes.
