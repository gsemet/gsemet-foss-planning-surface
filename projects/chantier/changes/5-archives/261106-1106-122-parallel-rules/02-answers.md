# Answers

Given by the user on 2026-11-06, in the Chief of Staff's session.

- **Default:** chantier favours parallel development, "quitte à ce que le stack driver les rebase".
- **A queue:** the Chief of Staff explains why it queues CRs rather than running them in parallel.
  One valid reason: the work is small and rebasing it in the stack would cost too much.
- **Base of a CR with no dependency, in a stack:** the default branch; the stack driver stacks the
  CRs once they are ready.
- **Changing a dependency in an open batch:** yes, with a new order, without a drop or a new number.
- **When it runs:** in batch-06, once the user has approved this specification and a slot is free.
- **Specification:** approved by the user on 2026-11-06, with `order after` as written; it joins batch-06 on top of the stack.
