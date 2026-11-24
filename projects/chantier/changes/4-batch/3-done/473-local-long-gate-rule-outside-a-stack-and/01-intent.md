# Local long gate outside a stack, and ask the batch shape at open

Short name: `own-gate`. The user's words of 2026-11-23, after batch-31: "I should have told you to run in stack mode."

Batch-31 ran parallel. CR-467, 468, 469 and 470 were handed back `--no-gate` under the AGENTS.md rule that the local Windows long gate is owed by the stack's top only. A parallel batch has no stack: each PR lands alone on main, so that exemption did not apply, and the Chief of Staff passed the hand-backs on anyway. The fix has two parts. First, AGENTS.md and the cards say who owes the local gate in each batch shape: in a parallel batch, each PR passes it before it is called ready to merge; in a stack batch, the stack's top only. Second, at the opening of a batch the Chief of Staff asks the user for the shape, with a recommendation drawn from how much the CRs' files overlap, instead of taking parallel by default. `status` shows the shape.
