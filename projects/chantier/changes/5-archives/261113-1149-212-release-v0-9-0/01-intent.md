# Intent

Release chantier v0.9.0 (minor, from v0.8.0) at the top of this batch's stack, so the user finds
in the morning a complete stack ready to merge: every P1 and P2 CR of the batch, then the version
PR with its release notes on top. The user's merge of the whole stack, bottom-up, is the go for the
rest of the project's release procedure (CONTRIBUTING.md "Release", steps 4 to 6).

This batch runs the shape the CR `release-cr-in-batch` makes normal, before that CR's code is on
`main`: today's CLI still refuses a kind-`release` CR before the others merge, so the version PR is
an ordinary CR of the batch that waits for every other CR, and the steps after the merge are run by
the steering session from the project's procedure.
