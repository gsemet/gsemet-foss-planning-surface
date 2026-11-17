---
type: cr-answers
description: The user's answers to the grill of prompt-writes-bare-path.
---

# Answers

## Round 1 (2026-11-17)

### batch-Q8: in which batch

The user: the six retro points of batch-23 join the next batch, with the four board CRs of
2026-11-17.

### carry-Q7: as filed

The user: as filed. The Driver's prompt skeleton prints `writes:` as a bare path (no
parenthetical) and names a scratch folder inside `work/` for Verifiers.

## Spec questions (2026-11-17, settled by the Chief of Staff)

- The planning folder's `.gitignore` ignores `work/scratch/`.
- The "neutral location" scratch option goes: Verifiers use `work/scratch` and rewrite the
  user's paths in a capture, or do not keep it.
- A path too long on Windows is a stop the Verifier reports.
## Spec questions, round 2 (2026-11-17, settled by the Chief of Staff after the spec critic)

- A scratch project under `work/scratch` must be its own git repository (`git init` first),
  and every `\` or `board` call there names it explicitly, so a probe never reaches the
  live planning folder; a test or scenario check proves it.
- Only throwaways the Verifier makes itself go under `work/scratch`; the project's own tests
  keep their fixtures and tmp folders.