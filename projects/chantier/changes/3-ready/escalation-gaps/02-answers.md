---
type: cr-answers
description: The user's answers to the grill of escalation-gaps.
---

# Answers

## Round 1 (2026-11-17)

### batch-Q8: in which batch

The user: this item and the other five retro points of batch-23 join the next batch, with the
four board CRs of 2026-11-17; so they are grilled now.

### escal-Q1: when a CR escalates

The user chose the recommended answer: the second `blocked rounds:` of the same CR, whatever its
cause (a red CI job, a gate broken after a rebase, a Verifier NOT VERIFIED, an Inspector
FIX-REQUIRED), makes the next round's Coder start on the escalation model (`escalate: rounds`),
said in the note as today. `rounds:` and `fix:` hand-backs count for the blocked-twice trigger.

### escal-Q2: which agents escalate

The user: the agents that write code (Coder, Debugger, Conflict resolver); the judging agents
(Inspector, Verifier, Investigator, spec agents) keep their model. The escalation must match a
role that is configurable in the configuration (the project's `chantier.yaml`, the board's
Configuration page), per host: on Copilot it may be different. So the escalation model is a
configured setting per host, not a fixed name in the cards.

### escal-Q3: a CR already escalated fails again

The user chose the recommended answer: the CR stops, blocked, and goes up to the Chief of Staff
as a question for the user (one more round, drop it, another approach). No further round without
the user.

## Spec questions (2026-11-17, settled by the Chief of Staff)

- The Drivers do not escalate: blocked twice escalates the next rounds' Coder, a failed restack
  its conflict-resolver (as the spec reads escal-Q2).
- On Copilot, a configured `escalation` is refused at validation until a start there can take a
  model (no fallback).
## Spec questions, round 2 (2026-11-17, after the spec critic)

- escal-Q4: the Chief of Staff's earlier settlement on Copilot rested on a wrong premise (a
  Copilot start can take a model: a generic agent, proved in CR-296). The user chose the
  recommended answer: a configured `escalation` on Copilot is accepted; the escalated role starts
  as a generic agent with that model, as a configured `model` does today. This replaces the
  earlier settlement.
- escal-Q5: the user chose the recommended answer: the first `blocked rounds:`, whatever its
  cause, escalates the next rounds' Coder once the user grants rounds; blocked twice covers the
  other reasons.
- escal-Q6: the user chose the recommended answer: only escalations made for that CR (its rounds'
  Coder, its own Debugger or conflict-resolver) count for "once per CR, then the user"; a
  stack-wide escalation note does not.
- Settled by the Chief of Staff: the CLI knows no role names; `escalation` is accepted only on a
  role whose shipped defaults carry one, and the cards say who escalates.- Settled by the Chief of Staff: the shipped escalation model on Copilot is `claude-opus-5.5`, the Opus identifier the Copilot defaults already use for the planning roles; on Claude Code it is `claude-opus-5-5`.
- Settled by the Chief of Staff (second critique), by the no-fallback rule as `model` follows it today: on Copilot, an `escalation` the user wrote on a role that carries the user's own `agent` is refused at validation, as a `model` there is; a shipped `escalation` on such a role does not apply (that role does not escalate on that host, and the escalation note says so). The user's agent is never replaced by a generic one.
