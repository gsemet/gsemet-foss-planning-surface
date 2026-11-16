# Every worker reads its card before it works

Filed 2026-11-15 by the Chief of Staff, on the user's word ("oui fait") to a follow-up of batch-18's retro.

Problem: in batch-18, of the 44 Verifiers started after CR-256 merged (2026-11-14 23:34:59Z), 34 read no card at all and worked from their prompt alone (7 read worker.md in the main checkout, 3 the copy in their worktree; counted by the verdict-head spec-writer). Workers replied out of format: an Inspector "APPROVED" with no head, Verifiers that did not record their verdict, a conflict-resolver "Placeholder"; about 12 "restart: reply out of format" notes; it recurs from batch-17. CR-273 (verdict-head) refuses only a VERIFIED without the head: the symptom, for one role.

Today's chain is indirect: an agent file (agents/<role>.md, com.github.copilot/agents/) says only "your prompt names the files to read first"; the Driver must name the card in the prompt (driver.md, line ~143: "the first line ... and the card to read").

Step 1, measure: in batch-18's Driver transcripts, did the worker prompts name the card (worker.md and its section)? Count per role (Verifier, Inspector, Coder, Debugger, Conflict resolver, Investigator).

Step 2, fix by the cause:
- the Driver omits the card: the CLI gives the Driver the exact opening lines of a worker's prompt, card included (as `playbook` already prints the first line), and driver.md says to copy them unchanged;
- the worker ignores the card: each agent file names its own card to read first (the contract stays in the card, the agent file only points to it), on both hosts with identical bodies (AGENTS.md).

Scope: every worker role, not only the Verifier. Host- and forge-neutral: Claude Code and Copilot; a path not proved on Copilot carries "unproved".
