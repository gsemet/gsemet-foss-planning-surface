# Answers

## timing-Q1: in this batch

2026-11-17, the user chose the recommended answer: timing-settings joins the next batch, with the eleven retro points of batch-22, cost-receipt and board-visual-refresh.

## timing-Q2: the Configuration page's Timing tab

2026-11-17, after two screenshots (`prototypes/01-mockups/timing-table.html`, `prototypes/01-mockups/timing-cards.html`), the user chose option 2, not the recommended table: a card per host, a band per model family (or context: subagent, session) inside, each setting with its value; a value set in chantier.yaml stands out from a shipped default. The tab sits beside Models, in the style of board-visual-refresh.

## timing-Q3: granularity

2026-11-17, the user chose the recommended answer: host × model family (and, on Claude Code, subagent or session), with a general value each column may override.

## timing-Q4: which settings

2026-11-17, the user chose "the main ones only", not the recommended all: the prompt cache's TTL, the wakes (steering, Driver) and the CI retries' maximum. Every other wait or maximum stays where it is.

## timing-Q5: the tab after the design critique

2026-11-17, in the combined mock-up the tab keeps a card per host, but each setting shows once with one value column per model family (or context), instead of a band per family repeating every setting; the legend (shipped default, set in chantier.yaml) sits beside the tabs. The user approved it as the specification's reference, to compare at delivery: board-visual-refresh's `prototypes/01-mockups/final-config.html`.

Spec critic: yes, it adds configuration the CLI reads and changes the loops' waits and what the Configuration page shows and writes.

## Spec questions (2026-11-17)

- timing-Q6 (Driver wake): split off as its own CR; `driver_wake` is not a key in this CR. This CR keeps the steering wake, CI re-runs, the cache TTL and the Timing tab.
- timing-Q7 (Timing tab writes?): no, read-only.
- timing-Q8 (Copilot cache TTL default): `5m`, marked unproved.
- timing-Q9 (Copilot column for the steering wake): the family of the model the Chief of Staff started the Foreman with, else the general value.
- timing-Q10 (what the TTL does): shown, plus a warning in `playbook` when a wake is longer than its column's TTL.
- timing-Q11 (board's "late" mark): it follows the batch's steering wake.
- timing-Q12 (CI retries max): keep today's rule (re-run of a CI job failed on the infrastructure) and reword the caption to say so.
- timing-Q13 (general vs shipped column): the user's value wins: the strongest layer first, then within a layer the column beats the general value.
- timing-Q14 (idle stop): after 30 minutes or more with no Driver, whatever the wake; the wake that sees this ends it.
- timing-Q15 (durations): only what is proved: refuse a wake over 60 minutes on Claude Code and anything that is not whole minutes on Copilot, each with a trial named in the host reference.
- timing-Q16 (a setting a column never reads): the tab shows "not used" in that cell, and chantier.yaml refuses the key under that column with its line.
