# Intent: stop ci-integration at once on a locked screen

From the v1.7.1 retro. The local `just preflight` of the version commit failed at
`ci-integration` because the macOS screen was locked: the VS Code window never became active, and
`ci-report` and `ci-gallery` failed from it. The cause was only found by reading the logs, and the
proof then needed an on-demand heavy run on the branch (about 20 minutes more).

Wanted: `ci-integration` checks for a locked screen before the run and stops with that cause and
what to do instead (unlock, or dispatch the branch heavy run). The release procedure tells the
release to dispatch the branch heavy run at once when the screen is locked.
