# CR-520 retro: release v1.13.0

The publication itself cost nothing extra: every job of the version push and of the Release VSIX
run passed on the first attempt, and the release was public 21 minutes after the merge. The time
went into the steps before the merge and into the follow-up.

## 1. The change request showed as merged while its PR was open

- What happened: the Release Driver handed back `ready` without recording the PR with `ship`.
  chantier then showed CR-520 as merged (batch paused) while PR #552 was open and nothing was
  published. No supported command put it back.
- Cost: the later change of the notes was made outside a Driver, and no Driver was left for the
  steps after the merge. The release 1.12.0 report records the same early "merged" state.
- Root cause: chantier accepts a `ready` hand-back of a release CR with no recorded PR, and counts
  it as released.
- Fix (in chantier): refuse that hand-back until `ship` has recorded the PR, and give a supported
  command that puts such a CR back. Already told to the chantier maintainers' session.

## 2. The performance gain was missing from the highlights

- What happened: the first release notes did not put the faster comment rendering (PRs #549 and
  #550, answering issue #547) in the highlights: the plan listed it under "All fixes". The owner
  asked for it.
- Cost: the version commit amended (`3fefbd67` to `4222c324`), a new chart
  (`comment-render-speed.png`), a push with a lease, the PR body regenerated and a second PR CI
  run of 10 minutes.
- Root cause (inferred): the changes are `fix` commits and were sorted as fixes; the release
  guideline does not say that a measured gain or an answer to a user's report is a highlight
  candidate.
- Fix (in `release-process.guidelines.md`, "Structure"): pick highlights by what the user gains,
  whatever the commit type, and treat a measured performance gain or an answer to a user-reported
  issue as a candidate, to be proposed in the first draft.

## 3. The chantier CLI was served from a stale build

- What happened: the installed chantier CLI ran a stale build until it was rebuilt.
- Cost: time spent before the commands behaved as the current sources say.
- Root cause: not established here.
- Fix (in chantier): make the CLI report, or refuse to run, when its build is older than its
  sources.

## 4. Merged before the PR checks ended, batch closed before publication

- What happened: the owner merged PR #552 at 09:16:17, 4 minutes 32 seconds after the push of the
  amended commit, while some of its checks were still running; they passed at 09:22:00. The batch
  was closed before the publication.
- Cost: no failure came of it. The publication had to be handed to a separate session, and
  chantier holds no `release published` record.
- Root cause: the late amendment restarted the PR checks while a quick close of the batch was
  wanted, and nothing holds the close of a batch until its release is published.
- Fix: say that the version PR is ready only once its checks are green at its head (in the PR
  conversation, not only in its test plan), and have chantier keep the batch of a release open, or
  keep a follow-up step on record, until `release published` is recorded.

## 5. Smaller costs, from the CR's notes

- The first Release Driver started at 77,514 tokens of context after its startup research and
  stopped at 130,016 during the drafting of the notes; a second one resumed.
- The release could not join batch-09, which already had a release CR, so it waited for the next
  batch.
- The Driver's brief named reference files absent from the chantier skill checkout, and
  `help <topic>` refused the `--batch` option the brief asked to pass.
