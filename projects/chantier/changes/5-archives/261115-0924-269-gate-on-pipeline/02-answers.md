# Grill answers

## 2026-11-15

- Source: batch-18's retro, kept by the retro critic and by a Fable review; the request's fix is the user's choice ("oui les 6", then "lance le tout dans le batch actuel"). It joins batch-18, switched to a stack.
- Generality (the user's word): the change works the same on both hosts (Claude Code, GitHub Copilot) and both forges (GitHub, GitLab); a path not proved on Copilot or a real GitLab carries the mark "unproved" in its card line.
- Place in the stack: second.
- Windows coverage default (A, recommended): one local `just scenario` per batch on the stack's top before the user merges; a Windows leg in CI is the alternative, named in the spec's open points with its cost.
- The CLI does not change; the cards carry the generic rule, this project's AGENTS.md the job's name.

- Spec open points 1-3 (2026-11-15): the spec's defaults stand, decided by the Chief of Staff to start it at once in batch-18 (the user's word "lance le tout"): 1. the local run on the stack's top (A), no windows-latest leg for now; 2. with no stack, the last CR the user will merge carries the local Windows run; 3. this CR's own long gate is the local `just scenario` of today's AGENTS.md.
