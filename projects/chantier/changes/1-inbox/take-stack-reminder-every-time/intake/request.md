# Stack reminder: say take stack every time, not only the first

In a stack batch, the "take stack" reminder is given for the first stack only. Give it every time a stack is due.

Observed in code (chantier 0.15.1): `stack_due` in `scripts/cli/src/chantier/stacks.py` returns nothing when a stack driver is recorded or when any CR of the batch is already stacked, and `stack_line` calls it "the batch's first `take stack`". So `status` and `next` never say "take stack now" again after the first stack: not after a partial merge, nor when later CRs become ready with the stack driver gone.

Wanted:
- Whenever enough CRs are handed back ready, no stack driver holds the stack, and they are not stacked (or the stack is behind them), `status` and `next` say so again.
- The case after a partial merge of the stack is covered.

Related inbox item: `ready-crs-sit-in-draft-with-no-ask-parti` (ready CRs with no ask). Same owner expectation (a stack batch delivers the mergeable part as soon as it exists), a different gap: this one is about the reminder to take the stack.

From the markdown-okf-schema-studio batch-09 (stack batch, 2026-11), chantier 0.15.1, Claude Code desktop app on Windows. Filed on the owner's word (2026-11-26).
