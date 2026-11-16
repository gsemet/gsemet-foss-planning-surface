## Summary

The version PR of chantier 0.8.0, prepared with `just release minor` as CONTRIBUTING.md "Release"
says: the version moves from 0.7.0 to 0.8.0 everywhere, and the release folder
`docs/release-notes/2026-11-07-v0.8.0/` holds the notes, the announcement thread and their images.
This is the first release under docs/release-process.md.

## What to review

- `release-notes.md`: the GitHub release notes, published as written after the merge.
- `tweet.md`: the three-post thread. Only you post it.
- Every image: `conversation.png`, `report.png`, `board.png`, `status.png`. Each comes from
  the real batch that shipped this work. Each was anonymised, its HTML source scanned with
  `release_notes.py --scan` (exit 0), rendered with headless Chrome, then read before the commit.

## Checks

- `just check` passes at this head (32 tests, `release-notes: docs/release-notes/2026-11-07-v0.8.0/release-notes.md ok`).
- `just scenario` passed at this head (the long gate).

## After the merge

On your word at each step: tag `v0.8.0` (`just tag`), then publish the GitHub release with
`release_notes.py --prepare v0.8.0` and `gh release create --notes-file`, with the images attached.
