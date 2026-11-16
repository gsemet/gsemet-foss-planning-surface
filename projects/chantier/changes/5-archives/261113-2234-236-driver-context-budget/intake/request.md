Measure the Driver's context before changing its rule

From batch-16's retro (point 1), reviewed by an advisor. Two Drivers ended at about 90k tokens: CR-216
handed back `context:`, CR-215 ended silently with no hand-back.

- The card's threshold is 150,000 (driver.md around 37-41), yet the Drivers ended near 90k: either the
  `context:` line under-reads, or the window is not the 200k assumed (hosts/claude-code.md around 346
  marks it unproved).
- Fix: compare the printed `context:` figures with the transcripts of CR-215 and CR-216, then set the
  threshold from the measure, so the Driver hands back `context:` well before its end, every time.
- Worker replies are already capped at ten lines (worker.md around 20); only the Inspector's JSON is
  unbounded: cap it.
- Lands: card; the CLI only if the measure is wrong.