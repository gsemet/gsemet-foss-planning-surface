# retro batch-28: ship calls a clean rebase a changed patch

From batch-28's retro (2026-11-19), kept by the retro critic.

After clean restacks, `ship` (and the stack driver's report) called the patch changed for CR-375
and CR-383 (restack A-19) and CR-379 (order O-24), refused to carry the verdict and the long gate,
and a fresh inspector or verifier run was ordered each time. CR-379's Driver then found the rebase
clean and carried both (ask A-28); CR-376's Driver showed by hand that patch-ids were unchanged.

Long-term fix: before calling a patch changed, compare patch-ids (`git patch-id`, or `git
range-diff`) of the CR's commits before and after the rebase; equal patch-ids carry the verdict
and the gate.
