# Answers

Short name: `visual-job`

1. visual-job-Q1 (2026-11-26, Chief of Staff, on the Foreman's ask A-33): **The CI `visual` job at its
   15-minute limit.** The owner: "A. CR dans batch-09 (reco.)", offered as: a new CR, placed low in
   the stack, splits or shortens the job; the end of the batch is delayed. The other option was a
   backlog item only, with the same risk on every run. The question said that the CI rules forbid
   raising the limit to make a slow run pass.

2. Placement (2026-11-26, Chief of Staff's decision under visual-job-Q1's "placed low in the stack"):
   directly above CR-505 (https://github.com/gsemet/markdown-okf-schema-studio/pull/532, head 9d7e788)
   and below CR-512. CR-509 and CR-505 are ready to merge and stay so; every CR that still waits for CI
   (CR-512, CR-511, CR-513, CR-514, CR-507) sits above and gets the fix. The specification is written
   against CR-505's head as its base, not against main.

3. Placement, replaces item 2 (2026-11-26, Chief of Staff, after the user's word "Il faut que tu
   prioritize la finition du stack"): directly above CR-512
   (https://github.com/gsemet/markdown-okf-schema-studio/pull/536) and below CR-511, so that CR-512,
   already verified, does not wait for this change. The CI files of that base are CR-505's. If
   CR-512's own CI cannot pass because of the `visual` limit, this change moves below CR-512.

Destination: running batch batch-09.
Spec critic: no, a CI change with no product behaviour (Chief of Staff; the owner may ask for it).
