# Answers: board-batch-view-tabs

## tabs-Q1: the Gantt's time scale
**Answer (A):** real time, from the batch's start to now, with a "now" line; a CR not started is a
cross stuck to the right edge.

## tabs-Q2: how long a card keeps its "just changed state" burst
**Answer (B):** for 10 minutes after the change, whatever the user does.

## tabs-Q3: the Gantt's vertical dependencies
**Answer (A):** exactly the graph's arrows (declared dependencies and stack base), so both tabs
say the same thing.

## tabs-Q4: the time card's rework stamp
**Answer (A):** an orange "REWORKED ×N" stamp (French "RETOUCHÉ ×N", N the CR's rounds) on a CR
at round 3 or more, distinct from the red MERGED stamp; both may show together.

## Settled by the Chief of Staff
- The open tab is kept in the URL; the graph is the default tab.
- Each non-default tab's module is imported on its first opening (dynamic `import()`).
- Start, end and per-round times come from the batch's `events.jsonl` as the board already
  reads it; no new CLI command.
- Every label goes through the i18n keys, in every language.
- The time card follows the prototype (`intake/prototypes.html`, view 1): one card per CR, a
  stamped line per round (coder, inspector), the verifier line, the PR and the cost, the MERGED
  stamp in red.
## The user, after the grill (2026-11-17)
"Keep the Gantt uniform with the redesign in this CR": the Gantt (like every new view of this CR)
uses `board-design-system`'s rules and shared pieces: the tokens only, the one card and chip
components (the priority chip as in Triage), no side border, no new one-off style.
## tabs-Q5: how a Gantt bar shows a CR that is not finished
**Answer (user's words):** "put several coloured sections (respect the state colours)". A CR's bar
is split into segments, one per period the CR spent in a state (working, blocked, ready,
merged...), each in that state's colour from the tokens; the current, open segment runs to the
"now" line and stays hatched.

## Settled by the Chief of Staff
- tabs-Q3 is read as the user meant it: the Gantt draws exactly the graph's arrows, which today are
  the declared dependencies only.
- Batch CRs' priority chip, with no CLI change: the board derives it from the CR's `add` event's
  `origin` (`commands/opening.py:52`, `:75`): `1-inbox/…` gives the Inbox chip,
  `2-backlog/P<n>/…` the P<n> chip, `3-ready/…` the 3-ready chip. Closed records show no chip.
  No change to the CLI, `summary.json`, `CrEntry`, the closed record or the events.
- Closed batches keep no events: their Gantt and time-card tabs show a "no times kept" note.
- This CR depends on board-design-system (it uses its card, chip and tokens): `depends.json`.

## Settled by the Chief of Staff (after the spec critic, 2026-11-18)
- The Costs receipt's `costs-stamp.css` stays untouched (a protected feature). The time card's
  stamps are a variant inside `card.css`'s `paper` variant, built on the same tokens.
- The graph's levels keep today's look, on tokens only; they do not become `column()`.
- Both tabs draw the declared dependencies only, as today's graph does. The tabs-Q3 option text
  the user picked wrongly named the stack base; its point, "the same arrows as the graph", holds.
- It stays one CR: with the chip from `origin` and the stamp in `card.css`, its extra load is gone,
  and the time cards build on the Gantt's `times.py`.
