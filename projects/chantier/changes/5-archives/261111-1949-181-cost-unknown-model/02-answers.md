# Answers: cost-unknown-model

## Decisions of 2026-11-11

Decided by a Fable advisor on the user's delegation: "Grille tout avec une session fable je ne sais pas te répondre…"

1. **The price table gains the models the host offers today that it lacks, `claude-fable-5-2`
   first,** each at the provider's published price, never guessed. Reason: the user runs Fable
   subagents; a figure from a wrong price is worse than none.
2. **A model the table does not know no longer makes a line unknown: the known calls are priced,
   the others are counted and named.** A line with such calls reads as its priced amount plus
   "N calls of `<model>` not priced"; the total says the same. Reason: one advisor on a new
   model must not hide a whole session's cost.
3. **Never a look-alike price** (no "priced as the nearest model", no family guess). Reason:
   AGENTS.md, "No fallback: no look-alike model".
4. **A figure with unpriced calls is a floor and says so; it is never shown as a plain total and
   never as `$0.00`.** Reason: the reports' rule that an unobserved cost is not a zero.
5. **The budget counts the priced part,** and `status` and the reports say the spend is a floor
   while unpriced calls exist. `take` and `round` are not refused for an unknown model.
   Reason: the batch must keep working; the user is told, and decides.
6. **`close` is no longer refused for an unknown model alone:** it prints the final cost with the
   not-priced remainder. It still refuses when nothing at all can be priced (no transcript, no
   priced call). Reason: today a batch that used a new model could not be closed until a release.
7. **A new model's price gets in without a release through `chantier.yaml`:** an optional entry
   gives a model's prices and ranks above the built-in table; the "not priced" line gives the
   exact model id to add. With no `chantier.yaml`, decision 2 applies. Reason: `chantier.yaml`
   is the only configuration the plugin has; nothing is fetched from the network.
8. **Copilot is untouched.** Reason: there the host's own records carry the price.
9. **One CR with `report-template` and point 3 of `cr-171-retro-fixes`.** Reason: the same
   `cost` code and the same card (`status-layout.md` "Cost").

## Merged items (2026-11-11)

This CR also carries `report-template` (all its answers) and point 3 of `cr-171-retro-fixes`
(its answers 3 to 5), on the Fable advisor's grouping: same `cost` code and same
`status-layout.md`. Their requests and answers are in `intake/`. Point 2 of
`cr-171-retro-fixes` went to `version-pr-rendered-notes`.

## The specification's open question (2026-11-11)

Settled by the Chief of Staff on the user's delegation ("Grille tout avec une session fable je
ne sais pas te répondre…").

- **The ratio's steering includes the steering session's own subagents** (an Explore, a
  critic): they serve the orchestration, not a CR's work. Reason: the same split as
  `cost --summary` already prints; one definition everywhere.
