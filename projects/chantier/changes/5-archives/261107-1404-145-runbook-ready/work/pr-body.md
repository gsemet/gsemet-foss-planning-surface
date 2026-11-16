The real-eval runbook (`evals/real/RUNBOOK.md`) said a CR's PR stays a draft and that nobody marks it ready. Since CR-131 a CR Driver opens the PR as a draft and turns it ready once it can merge; on another base it stays a draft. The runbook now says so in its two places ("Nothing merges", "Check"). Nobody merges it or enables auto-merge still holds.

Docs only: `just check` passes; no `just scenario` needed. `grep -i draft evals/real/` shows no other line.
