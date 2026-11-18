# Answers

- The user (2026-11-18): "Oui, spécifie les P1", after the standing word of the day "plus de question" (no more questions): no grill; the behaviour choices below are the Chief of Staff's.

## Settled by the Chief of Staff

- **The top with no stack.** In a batch with no stack (parallel shape, or one CR), the "top" that owes the local run of the long gate (AGENTS.md: "the CR on top of the stack also passes `just scenario` locally") is the batch's last CR still open: the one CR not merged or cancelled when every other one is. A one-CR batch's CR is its top from the start.
- **Who runs it and when.** That CR's Driver, before its first hand-back as the top (no `--no-gate`); a CR that becomes the top later (another CR merged or dropped, or it was already handed back) gets the run from its Driver, or from a new one the Foreman starts, before the ready ask goes to the user. A CR joining by `order add` becomes the top when it is the last open one, and the run moves to it.
- **What the ask says.** As in partial-stack-ask-windows-gate: the ready line states the local gate at that head (passed, failed, not run); the Foreman sends the last CR's ready ask only with a pass, except at a `deliver by` time.
- **Shared cards.** It touches the same cards as partial-stack-ask-windows-gate (driver.md, foreman.md, chief-of-staff.md): the two CRs run one after the other (`order after`), never side by side.
- Spec critic: yes, it changes the Driver's and the Foreman's contracts.
