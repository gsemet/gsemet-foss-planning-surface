# Answers

1. Q: The limit? User, 2026-11-18: "Je suis d'accord pour que la limite à 12K reste, il faut que
   ce noyau soit optimisé en taille et en efficacité."
2. Q: Run it? User, 2026-11-18: "optimise-the-startup-core-in-size-and-ef et tous les autres
   restant à spécifier et lancer".

## Settled by the Chief of Staff (2026-11-18, the user asks no questions)
- The limit stays 12544 in its three places; this CR lowers what each role reads, it does not
  lower the limit.
- Goal: the tightest role and host, at boot and at reload, ends at least 10% under the limit
  (at most 11,290 bytes), measured by the existing budget test; the PR gives the before and after
  table for every role and host.
- Size: remove repetition across the core files (a rule said in two cores is said once, where
  every role that needs it reads it), restatements of what a deferred card holds, and wording
  that adds no rule. Never drop a rule.
- Efficiency: the core holds only what a role needs before its first action or at every turn;
  any rule tied to one action moves to the card section that action reads (the manifest's
  action readings), with a one-line pointer only when the action could be missed. The rules
  that must never be missed (stop on a CLI failure, the watcher's start, the seat, the no-
  fallback rule) stay in the core, first in their file.
- Each moved or merged rule is listed in the PR's delivery with where it now lives; a structure
  test checks that the moved rules are still present in the cards.
- Both hosts' agent files stay identical in body (AGENTS.md rule).
- It stacks after `watcher-autostart` (which adds one core line); it must keep that line.

## Settled by the Chief of Staff (spec-writer's points, 2026-11-18)
- `portable-cli-invocation` is folded in: its rule and test ship here; that CR is abandoned once
  this one merges.
- The manifest moves to a version 2 with the same content (relative paths, `file#heading`,
  `startup_sections` only where a role has one): accepted.
- "No fallback" joins `startup-core.md`, second after the CLI stop: accepted.
- "The seat" in the core means the router's seat bullets and "no seat" in the CLI stop; the Chief
  of Staff's and the Griller's seat rule stays in `session-start.md` sections 2 and 5: accepted.

## Settled by the Chief of Staff (spec-critic's findings, 2026-11-18)
- Proof of a real boot: one real Claude Code session at the PR's head, quoted in the PR: a Chief of
  Staff boot, a Chief of Staff reload after a compaction with a running batch (the `watch: not
  running` line acted on) and one Driver start. Copilot the same when the host is at hand,
  otherwise the PR's Known gaps names it. The scenario claim is removed from the spec.
- The Chief of Staff's and the Griller's `SKILL.md` keep one short line: "At the session's start,
  read `session-start.md` (the manifest's `session-start` action)".
- The never-miss rules sit first under `## Startup core`, not first in the file: accepted; the
  spec's "Two readings" names it.
- The CR joins batch-28 (it stacks after CR-375 there).
