# Grill answers

## 2026-11-15

- Source: batch-18's retro, kept by the retro critic and by a Fable review; the request's fix is the user's choice ("oui les 6", then "lance le tout dans le batch actuel"). It joins batch-18, switched to a stack.
- Generality (the user's word): the change works the same on both hosts (Claude Code, GitHub Copilot) and both forges (GitHub, GitLab); a path not proved on Copilot or a real GitLab carries the mark "unproved" in its card line.
- Place in the stack: third, before early-conflicts.
- A forge read that fails keeps the existing `base ? (not read...)` line; no retry, no fallback.

- Spec open points 1-3 (2026-11-15), decided by the Chief of Staff (the user's word "lance le tout"): 1. `ship --draft` goes (the spec's default); 2. yes: `ship` records the forge's base on the CR and `ready_word` and `draft_waits` read it, since the stale "waits on cr-265" text is the drift the retro named; 3. `draft not read` stays.
