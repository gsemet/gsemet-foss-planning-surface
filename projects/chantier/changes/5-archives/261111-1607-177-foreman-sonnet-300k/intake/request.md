# The Foreman runs Sonnet 5.5, with an auto-compact window of 300K

The user's words (2026-11-11): "En mode foreman, quelle est la configuration recommandée ? Je
voudrais recommander l'utilisation de sonnet 5.5 avec un autocompact à 300K".

## What main says today (7ad33cb)

- `README.md` "Models": Foreman on Opus 5.5, effort medium (Copilot: Claude Opus 5.5).
- `hosts/claude-code.md`: the Foreman's session is started with `model: "claude-opus-5-5"`,
  `effort: "medium"`; the "Models" row says the Foreman runs Opus 5.5 (proved).
- `hosts/copilot.md`: `create_session` with `model: "claude-opus-5.5"`.
- `CONTRIBUTING.md`: the roles that judge (the Foreman among them) run Opus.
- `hosts/claude-code.md`, compaction: the recommendation is `autoCompactWindow: 400000` in
  `~/.claude/settings.json` for the Chief of Staff's and the Foreman's sessions, unproved; a
  note records sessions set to 300000 compacting around 165 to 170k tokens, unexplained.

## What the user wants

Recommend Sonnet 5.5 for the Foreman's session, and an auto-compact window of 300K.

## Open points for the grill

- The Chief of Staff's session: does its recommendation change too (Opus 5.5 today, 400K)?
- The rule "the roles that judge run Opus" no longer holds for the Foreman: reword it.
- The effort: keep "medium" with Sonnet 5.5?
- Copilot: the same model for its Foreman?
- Overlap with CR-169 playbook-config (running): it leaves the Foreman's model out of scope.

## Addition (2026-11-11): Sonnet everywhere, escalation on trouble

The user's words: "Les drivers et foreman peuvent être en sonnet tu penses ? J'aimerais que on
l'utilise un maximum et quand il y a un soucis il y a une escalade vers un modèle plus
puissant."

- Sonnet 5.5 by default for the Foreman and every Driver (stack and release drivers too, Opus
  today); the CR and QA drivers and the workers already run Sonnet.
- An escalation rule: on a defined trouble, the work moves to a stronger model (Opus 5.5).
- Context, batch-09 cost at $93.53: steering 46 %, Drivers 17 %, workers 36 %.

Facts for the grill:
- An agent's model is set when it starts. Escalation means a new agent on Opus (the `Agent`
  tool takes a model alias, proved by CR-169's trial with `haiku`), or, for a session, a model
  change of the session (`set_session_model` on Claude Desktop, unproved for this use).
- AGENTS.md "No fallback": an escalation must be a written rule with named triggers, never a
  silent swap.
- Candidate triggers: a CR blocked twice; rounds used up with the Inspector still FIX-REQUIRED;
  a red check the Debugger could not explain; a conflict the resolver could not settle; a
  restack that failed; the steering session judging a hand-back it cannot read.
- Overlap: CR-169's `chantier.yaml` playbook sets the model per role; the escalation model
  could live there too.

Batch-09 observation for the trial: the CR drivers on Sonnet delivered all six CRs, but two
skipped the Investigator although told to run every step, one skipped a second Inspector, and
one asked for a refused force push the right way.

## Trial (2026-11-11): batch-11's Foreman switched to Sonnet 5.5

On the user's word ("Oui, en Sonnet"), batch-11's Foreman (epoch 2, started on Opus 5.5 as the
cards say) was switched to Sonnet 5.5 from its next turn, after its `ready`. Its batch holds one
CR (CR-174). Read its transcript's model and its steering at the batch's end for the trial.
