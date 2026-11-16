# A CLI gate: no grill by the steering session while its direct batch runs

## The user's words (2026-11-10, batch-09)

"D'ailleurs tu es en train de griller alors que tu es en mode direct. C'est un problème, tu as des
règles et tu les oublies je pense qu'il faut une gate en CLI"

## The rule that was broken

`chief-of-staff.md`, "What you accept while you steer":

- "You hold no grill, no triage, no demo and no discussion until the batch completes."
- A new idea is filed in the inbox at once (`file`, no grill).
- A request to grill gets one line: fork this session, and the fork becomes a Griller.

## What happened

batch-09 runs in direct mode, steered by the Chief of Staff's own session. During the day, while
Drivers were running, that session:

- grilled `add-several-while-paused` with the user (four questions), wrote its `01-intent.md`
  and `02-answers.md`, and asked "grilled enough to triage it in P1?";
- wrote `status-command`'s `02-answers.md` and `03-change-spec.md` while CR-158 ran;
- offered to grill `options-by-environment`.

The rule is in the card, but after a compaction the session keeps only a summary of the card, and
the rule was lost. A card is not enough here: the CLI should refuse.

## The request

A gate in the CLI. While a direct batch runs, the CLI refuses the grill's steps when they come from
the steering session:

- the session is the batch's recorded steering session id;
- a Griller's session, any other id, is not refused.

The refusal message names the way out: fork this session, and the fork becomes a Griller; or wait
for the pause.

The specification decides which commands are gated. Candidates:

- `triage`;
- a new `grill` step that records a grill's start or its answers;
- the spec-writer's start.

`file` stays allowed.

## Also

- The same gate may cover "no demo".
- This is measured behaviour, not speculation: the rule was broken several times in one day by
  the same session (AGENTS.md: a new CLI tool comes from measured token-costly behaviour).
