
## batch-12 (2026-11-12, real-foreman eval, the batch-11 Foreman reused)

- The eval audit reads every agent transcript of the session's folder, not the batch's: 114 agents and 110 FAILs, almost all from batch-09 to batch-11 Drivers and workers, so the scorecard cannot be read as batch-12's: the audit filters its agents by the batch's creation date.
- `cost` prices no `claude-fable-5-2` call (58 calls of the Chief of Staff unpriced): the price table knows the current model ids.
- CR-186's spec assumed `take` keeps a CR's recorded agent, but `check_take` refuses it: a spec is checked against the CLI before it is marked ready (the Driver changed the Foreman card instead; the eval has to show the resume).
- CR-186's final PR description was edited after the Verifier's pass and no Verifier read it: a Driver re-runs the short description pass after its last edit of the body.
