# Land the three docs SVGs

## Problem

Three diagrams approved by the user exist only outside the repository's history: the two lifecycle
diagrams redrawn on two rows, and a new diagram of how batches set the pace.

## Change

Copy the three files of this CR's `svgs/` folder, byte for byte, into `docs/` of the CR's worktree:

- `svgs/cr-lifecycle-simple.svg` replaces `docs/cr-lifecycle-simple.svg`.
- `svgs/cr-folder-lifecycle.svg` replaces `docs/cr-folder-lifecycle.svg`.
- `svgs/batch-pace.svg` is the new `docs/batch-pace.svg`.

Nothing else changes. `README.md` stays as it is: it keeps its two links and does not name
`batch-pace.svg`, which the user has not finished with.

This is a docs-only change: `just check` is its gate, `just scenario` is not needed.

## Acceptance

- The three files in `docs/` are identical to those in `svgs/`.
- The PR's diff holds those three files and nothing else.
- `just check` passes.
