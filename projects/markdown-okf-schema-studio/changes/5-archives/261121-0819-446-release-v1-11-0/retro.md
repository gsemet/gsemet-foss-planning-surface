# CR-446 retro: what cost time

Details of root causes below come from the Foreman's brief; the process fixes are proposals.

- **The stack was not a git chain, so CR-440..445 were restacked twice.** Root cause: the changes
  were ordered in the batch but their branches were not each based on the previous one. Fix: create
  each branch of an ordered batch from the previous CR's branch, and check the chain with
  `git merge-base` before the first push.
- **CR-444 screenshot push refused by the safety check.** Root cause: the push of the capture files
  tripped the push safety check. Fix: state in the driver brief how screenshot files are committed
  and pushed, so the check is met up front.
- **CR-441 visual timeout (15 min job limit).** Root cause: the visual job outgrew the limit.
  Fixed by splitting out the `viewer-graph` job, without raising the timeout. Fix: watch the visual
  job duration and split before it nears the limit.
- **CR-445 took 6 rounds.** Root cause: not analysed here. Fix: review the CR-445 rounds for a
  pattern (spec gaps or late findings) before the next batch.
- **CR-446 notes review fixes (picture order, crops).** Root cause: the release notes pictures were
  ordered and cropped wrongly in the draft. Fix: check picture order and crops against the
  release-notes guideline before sending the notes to the owner.
