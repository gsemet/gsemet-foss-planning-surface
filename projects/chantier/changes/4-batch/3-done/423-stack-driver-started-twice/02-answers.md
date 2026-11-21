# Answers

## 2026-11-20, settled without the user

The user asks no questions tonight ("tu es maintenant autonome. plus de question. tu grilles tout
seul"). Each point below is: Settled by the Chief of Staff (2026-11-20, the user asks no
questions), by the narrowest choice that meets the request, with its reason.

1. **The source of the fact.** The only evidence is the Studio project's batch-06 retro
   (`projects/markdown-okf-schema-studio/changes/5-archives/batches/batch-06.md`, its `[chantier]`
   point, 2026-11-20): a subagent Driver cannot `SendMessage` a Claude Desktop `local_` Foreman
   session, and its hand-back reaches the Foreman only as its final report. The host's exact text
   for the failed send was not recorded. The row cites that retro and its date, and names as a
   trial the recording of the host's exact text. Settled by the Chief of Staff (2026-11-20, the
   user asks no questions). Reason: the card's marks ask for where and when, and forbid stating
   more than was seen.
2. **Which Drivers.** The corrected row and the `Steering:` text hold for every Driver (CR, stack,
   release, QA), not the stack driver alone. Settled by the Chief of Staff (2026-11-20, the user
   asks no questions). Reason: the four prompts share one `Steering:` line and one host row, and
   the host fact is about a background subagent, whatever its role.
3. **Which steering sessions.** A Foreman is always a Claude Desktop `local_` session, so the
   corrected row is the Foreman-mode row. Direct mode from Claude Desktop (the Chief of Staff, a
   `local_` session too) gets the same means, marked unproved. Direct mode from a terminal or
   VS Code keeps `SendMessage` to `main`, marked unproved. Settled by the Chief of Staff
   (2026-11-20, the user asks no questions). Reason: the retro saw the Foreman case only; nothing
   seen supports "proved" anywhere else.
4. **What a Driver does with a line due before its end** (`anomaly`, `push`). It records an
   `anomaly` as a `$CHANTIER note` on the CR when it happens, and puts every such line in its
   final report, under the hand-back line, one per line. Settled by the Chief of Staff
   (2026-11-20, the user asks no questions). Reason: the note and the final report are the two
   means that exist; no new command.
5. **The `ping`.** A Driver cannot send a `pong` there. The Foreman still sends the `ping` to a
   suspect (a message to a Driver is proved, and it wakes a waiting one); at the next wake the
   proof of life is the Driver's `activity` age in `status --refresh`, younger than the ping. An
   age older than the ping, with no `gate running` and no `gate queued`, is the missing `pong`.
   Marked unproved, with its trial. Settled by the Chief of Staff (2026-11-20, the user asks no
   questions). Reason: it keeps the lost-Driver rule working with what `status` already prints
   (the age of the agent's own session record), and removes the false death that a `pong` that
   cannot come would give.
6. **Where the text goes.** Every host fact goes in `hosts/claude-code.md` only (the user's
   rule). The generic cards get two short pointers, with no host tool named: `foreman.md`'s proof
   of death and `driver.md`'s `ping` answer defer to the host's reference and the `Steering:`
   line. Settled by the Chief of Staff (2026-11-20, the user asks no questions). Reason: without
   them the generic cards contradict the host card.
7. **No CLI change.** The skeleton of `take`, `take stack` and `order qa` keeps its `Steering:`
   placeholder, which names the host row by its label; the row keeps that label. Settled by the
   Chief of Staff (2026-11-20, the user asks no questions). Reason: the request asks to fill the
   line with the host's truth, and the fill is the parent's, from the host card; the CLI knows no
   host tool.
8. **No agent file change.** `agents/*.md` and `com.github.copilot/agents/*.agent.md` stay as they
   are, the Drivers' `SendMessage` tool included. Settled by the Chief of Staff (2026-11-20, the
   user asks no questions). Reason: a role's contract lives in the cards; a terminal direct batch
   may still use the tool (unproved).
9. **Copilot.** `hosts/copilot.md` is not changed. Settled by the Chief of Staff (2026-11-20, the
   user asks no questions). Reason: its row already says a Driver's hand-back is its final answer.
10. **No new refusal of a second stack driver.** `take stack` already refuses while the stack's
    lease is live. Settled by the Chief of Staff (2026-11-20, the user asks no questions). Reason:
    the request asks for the row and the `Steering:` line; a new rail needs a measured cost.
