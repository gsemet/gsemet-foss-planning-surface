Edit for the CR and stack Drivers

From batch-16's retro (point 2), reviewed by an advisor; the user agreed to give the Drivers editing
tools. The CR-215 Driver rewrote the PR body with Write, since the cr-driver agent has no Edit.

- agents/cr-driver.md and agents/stack-driver.md (and their com.github.copilot/agents/ twins) lack Edit;
  the release driver has it. driver.md (around 101) says "always written with the Write tool".
- Fix: add Edit on both hosts and reword that line. First confirm the write guard in `hooks/` holds a
  Driver's Edit to its `writes:` folders; if `hooks/` changes, `just mod` applies.
- Lands: agent files on both hosts, the card.