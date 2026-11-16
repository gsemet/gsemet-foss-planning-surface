# Change Specification: the runbook says a PR is turned ready

## Goal

`evals/real/RUNBOOK.md` (lines 18 and 32) still says a CR's PR stays a draft. Since PR 69
(CR-131) a CR Driver opens it as a draft and turns it ready once it can merge (its base is the
default branch, green, evidence in); on another base it stays a draft and says what it waits for
(`skills/chantier/references/driver.md`, "Your end").

## What changes

Those two places, and any other line of `evals/real/` that says the same, state the current rule
in the runbook's own words. Nothing else.

## Evidence

`grep -n -i draft evals/real/` shows no line that contradicts `driver.md`. A docs-only change:
`just check` passes; no `just scenario` needed.
