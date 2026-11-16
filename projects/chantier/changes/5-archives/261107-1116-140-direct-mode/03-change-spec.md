# Change Specification: direct mode, a batch steered by the Chief of Staff

## Goal

A batch can be steered in one of two ways, chosen in the plan and approved by the user's go:

- **Foreman mode:** a separate Foreman session steers the batch.
- **Direct mode:** no Foreman session is started; the Chief of Staff steers the batch from its
  own session: it starts the Drivers (in the background, several slots in parallel), hears
  their hand-backs, and does everything the Foreman's card says until the batch completes.

The CR lifecycle, the batch frame (`open`, slots, rounds, budget, orders, `land`, `close`),
the folders, `STATUS.md`, the reports and the user's boundaries are the same in both modes.
The user decided the conditions (see `02-answers.md`); this specification settles the open
points of that grill, on the user's word "I leave direct mode to you".

## When the plan proposes direct mode

The Chief of Staff proposes direct mode when the host cannot start a Foreman session (a
terminal or IDE host, a Remote Control session with no Foreman to reuse) or when the batch has
few CRs, and says why in the plan; otherwise Foreman mode. The limits are the same in both modes
(slots, rounds, budget, the project's `chantier` section): there is no CR threshold of its own.

## What the Chief of Staff does while it steers

- It reads `foreman.md` and its host's reference and follows them, as the steering session,
  with the differences below. `chief-of-staff.md` gets a section, "Steering a batch yourself",
  that lists them; `foreman.md` gets one line pointing to it.
- It claims the batch's epoch for its own session, exactly as a Foreman does (`foreman set
  <its session id> --epoch <n>`, `foreman transcript <its transcript id> --epoch <n>`), carries
  `--epoch <n>` on every steering command, and arms the same heartbeat.
- What it would send itself is not sent: no `ready <batch>`, no `[foreman→chief-of-staff]`
  line. An ask is still recorded with `$CHANTIER asks "<text>"` (so a resume loses nothing) and
  told to the user at once, in the report's shape; a Driver's refused force push is run by the
  Chief of Staff as today, and the Driver hears the result as a note.
- The batch is strict: no CR joins it while it runs. `order add` and `order qa` are refused by
  the CLI on a direct batch (see below); a release fix that needs `order add --fix-for` is an
  ask to the user, who may switch the batch to Foreman mode.
- While it steers, it accepts only: "status?" and "what did it cost?"; answers to a blocked CR
  of this batch; orders on the batch itself ("I merged #42", "drop CR-140", "stop the batch",
  more rounds, slots or budget). Any other request is noted word for word and handed back when
  the batch completes; an idea may be filed in the inbox at once (`file`, no grill). It holds
  no grill, no triage, no demo and no discussion until the batch completes.
- It ends as the Foreman does: `land`, then, with nothing running, the `close` flow of today
  (the bilan, the final cost, `close --yes` on the user's yes).

## Switching to Foreman mode

On the user's word, a direct batch may switch to Foreman mode while it runs, only where a
Foreman can start: preflight in Foreman mode passes first (P1, P2), and on Remote Control the
switch needs a Foreman to reuse or is refused with the reason. The Chief of Staff starts no new
Driver, lets the running ones hand back (or stops them; a new Driver resumes with `handoff`),
then starts the Foreman with the next epoch, as in "Starting a batch". Its own epoch is then
stale, and the CLI refuses its steering commands (exit 3), as today. A Foreman batch does not
switch to direct mode.

## The CLI

- `open --direct`: the batch records `"steering": "direct"` (else `"foreman"`). `brief.md`,
  `status` (its first line) and `STATUS.md` show the steering. The `next:` line of `open` says
  "then steer it yourself" instead of "then start the Foreman".
- A later epoch claimed by a transcript other than the Chief of Staff's (`chief_transcript`)
  sets `"steering": "foreman"` and logs it.
- `order add` and `order qa` on a batch whose steering is direct exit 2 with "a direct batch
  is strict: switch to Foreman mode to add work".
- `preflight --direct`: P1 passes on any Claude Code entry point or a Copilot agent session;
  the line for the Chief of Staff's own checks leaves out P2 (no session to start). The other
  conditions are unchanged.
- Cost: each steering transcript is priced from its claim to the next claim (or now), not from
  the batch's opening; a direct batch's steering row is labelled "Chief of Staff (steering)"
  instead of "Foreman", in `cost`, `status --refresh`, `land` and `close`. The "Chief of Staff"
  line then prices only the Chief of Staff's session outside its steering windows, so nothing is
  counted twice, and the steering counts in `spent_usd` and the budget as a Foreman's does.
- No other command changes; `foreman set` and `foreman transcript` keep their names.

## The cards, the agents and the docs

- `SKILL.md`: the hard rule "You start no Driver…" becomes: in Foreman mode you start no
  Driver and never message one, orders go through the Foreman; in direct mode you steer the
  batch yourself (link to the new section). The Entry points table and the first-turn
  introduction say a batch is steered by a Foreman or, in direct mode, by the Chief of Staff.
- `chief-of-staff.md`: "Starting a batch" gains the choice of steering (preflight with or
  without `--direct`, the plan names it, `open --direct`, then step 4 is "start the Foreman" or
  "steer it yourself"); the new section above; "Never" and "Subagents" adapted.
- `foreman.md`, `driver.md`, `concepts.md`, `routing.md`, the hosts' references: where they name
  the Foreman as the one a Driver answers, say "the steering session (the Foreman, or the Chief
  of Staff in direct mode)". On Claude Code a Driver already sends to `main`, which is the
  Chief of Staff in direct mode; the Copilot reference says how a Driver reaches its steering
  session there, marked unproved where it is.
- The agent files change only where their bodies name the Foreman as the one to answer, on
  both hosts together, bodies identical.
- `docs/` and the README: where they describe the Foreman, a sentence on direct mode, as the
  final state (no "new").

## Out of scope

- A dedicated slash command, an automatic choice of mode without the user's go, a switch from
  Foreman to direct mode, a direct batch that accepts added CRs.

## Done when

- `just check` passes on the three platforms and `just scenario` passes (a CLI and card change).
- The structure tests cover `open --direct` (recorded, shown), the refusal of `order add` on a
  direct batch, and `preflight --direct`; the scenario covers a direct batch from `open` to `land`.
- A Verifier shows on the pushed head: a direct batch priced with one "Chief of Staff
  (steering)" row and a "Chief of Staff" line that excludes the steering window; a later epoch
  from another transcript switches the steering to Foreman and refuses the old epoch.
