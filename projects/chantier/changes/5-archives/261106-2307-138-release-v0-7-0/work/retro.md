# Retro: Release v0.7.0

Out: tag v0.7.0 at main 337e467, <https://github.com/gsemet/chantier/releases/tag/v0.7.0>. Main's CI
on 337e467 is green (run 42306314179). The procedure names no deploy to watch, and the repository
has no Pages site.

What went wrong or slowly, and the long-term fix for each:

- `just tag` reads the version from its own checkout and tags `origin/main`, so from a stale main
  checkout (here 55d32c7, which reads 0.6.0) it asks for v0.6.0 on the release commit: that stops
  only because v0.6.0 already exists, and a checkout with an untagged version would tag wrongly. The
  last Driver avoided it by running it in the CR's worktree. Fix: `just tag` reads the version from
  `origin/main` after its fetch, not from the working tree.
- The eval `real` was in the spec but cannot run inside a batch (`open` refuses a second batch), so
  attempt 1 stopped for a question and the user waived it, against `CONTRIBUTING.md`. Fix: decide at
  the grill where `real` runs, before the batch that releases, and say so in the release spec.
- Five Drivers for one release in 55 minutes, a new one after each stop (question, merge, tag
  approval, release approval). Fix: ask for the tag and the release together once the PR is merged,
  as one approval of two named actions.
- `release go` matches the action's text: the first ask was worded "tag v0.7.0 on 337e467", the
  approval "just tag: ...". It held here because the Driver quoted the approval, but nothing says
  which wording counts. Fix: the card says an approval names the procedure's exact command.
- The host refused to start this Driver once, and the user had to allow it again in the Foreman's
  chat. Fix: name in the Claude Code reference what a refused Driver start needs from the user.
