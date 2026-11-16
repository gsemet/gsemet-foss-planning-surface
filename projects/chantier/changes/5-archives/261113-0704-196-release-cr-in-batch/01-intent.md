# A release CR asked in a batch is a normal CR of that batch

## Why

Today a release CR that shares a batch is an exception to it. It waits until every other CR is
merged (not ready), then for a separate confirmation; it sits outside a series and a stack, on
the default branch; its PR is never part of the stack. The user reviews and merges the work
first, and only then sees a version PR and release notes, in a second pass.
`docs/batch-pace.svg` draws it that way: a frame around "every CR in here", and the release
outside the frame, like a batch of one CR.

The user (2026-11-12) wants the other shape to be the normal, documented one: "Si une CR de
release est demandée dans un batch, elle est typiquement mise en dépendance de tous les autres
CR et donc ne pourra pas démarrer tant que le reste de la stack est prête."

## Outcome

- A release CR asked in a batch is a CR of that batch like the others: it waits for every other
  CR through intra-batch dependencies and starts once a single branch holds all the work it
  ships.
- In a stack or a series batch that is when every other CR is ready (not merged): the release
  stands on the top CR, and its PR is the top of the stack. Its version bump, changelog and
  release notes cover everything below it, plus what the default branch already holds since the
  previous tag. The user reviews the work and the release together and merges from the bottom
  up, the release PR last.
- Preparing the release PR is reversible. The irreversible actions (tag, forge release,
  publication, announcement) wait until the release PR is merged on the default branch, which
  means the whole stack is merged, and each still needs the user's go (an approval or a grant).
- The cards, the CLI where it refuses this, the project's release procedure
  (`CONTRIBUTING.md` "Release", `docs/release-process.md`), the use-case docs and
  `docs/batch-pace.svg` say so; the diagram draws the release inside the batch with its
  intra-batch dependencies.

## Not in this CR

- More than one release per batch; a release that ships only part of a batch.
- The fix grant, the "auto" grant and the `release go` vocabulary, other than the new wait for
  the merge.
- A new CLI command.
