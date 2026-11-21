# Conflicts

requirements/tiers/log.md, one hunk under "## 2026-11-21": main added CR-458, CR-447, CR-454 entries; this CR added "Mutation campaign on src/core (CR-450, round 3)". Kept all four, main entries first, blank line between, no markers, no BOM.

Fast gate: `just requirements-lint` passed (main paths 93 StRS, diagrams 94 StRS); `npx tsc --noEmit -p .` passed with no output. No other fast gate run.
