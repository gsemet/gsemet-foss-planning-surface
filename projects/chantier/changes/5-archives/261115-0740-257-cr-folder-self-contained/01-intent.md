# Intent

A CR's folder holds everything needed to resume it later or elsewhere, save for stated
exceptions. Today the cards contradict that, and agents leave grill work outside it.

## Origin

The Griller session "visualization-backend" (2026-11-12) built three prototype versions. The
prototype itself was in the CR folder, but its snapshot generators stayed in the host's
scratchpad and its screenshots in the session cache until the user asked for them to be moved.

## Causes found

1. `concepts.md:251` and `chief-of-staff.md:620` say "a prototype lives in a temporary folder and
   is thrown away" (meant for the Chief of Staff's exploration subagents, read as a general rule).
2. `griller.md` says prototypes go in the CR folder only under "In a planning surface" and "In a
   worktree"; the in-project default has no rule.
3. The CR folder tree (`concepts.md:22-30`) names no place for prototypes, scripts or experiments.
4. The host's system prompt sends scripts and intermediate results to its scratchpad; no chantier
   rule ranks above it for a CR's work.

## Other leaks to close or state as exceptions

- Scripts, tests and benchmarks written during a grill or a study (scratchpad).
- Built-in browser screenshots: not files unless saved on purpose.
- Images the user pastes in the chat: no file exists; ask the user for it, or describe it in
  `02-answers.md`.
- A Chief of Staff subagent's exploration or study: its result returns only in the conversation.
- Web research: sources and quotes stay in the transcript.
- claude.ai artifacts and inline visualizations: outside the repository.
- Plan-mode plans and the agent's memory (`~/.claude/`).
- How to run a prototype again (its server command): only in the session unless written down.
- A Griller in a worktree: its files are lost if the worktree is cleaned before the Chief of
  Staff places them.
- The cleaned archive in the PR (`concepts.md:51`, `driver.md:101`) keeps `intake/`, `evidence/`,
  `01`-`03`, `delivery.md`, `STATUS.md` only: a prototypes folder would be dropped.

## Out of the CR folder by design

Secrets, personal data, large binaries; the batch's own files and raw logs (already gitignored).
