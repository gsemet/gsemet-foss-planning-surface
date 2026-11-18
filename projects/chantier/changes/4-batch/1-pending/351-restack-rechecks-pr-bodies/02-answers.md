# Answers

## Settled by the Chief of Staff

The user's word, 2026-11-18: "file all six and run them in batch-24" (the six kept points of
batch-24's retro). This CR is run as `intake/request.md` writes it, with no grill.

Working choices made by the Spec-writer, within that word:

- The re-check is `ship`'s own: every restack and every rebase already ends with `ship` for each
  moved CR (driver.md, Stack driver and CR driver), and `ship` already names the stale lines of
  `work/pr-body.md`. No new CLI command and no forge read is added; the gap is closed where `ship`
  missed it.
- The two misses seen in batch-24 (CR-345's body): a line holding `carried from` was skipped
  whole, so the SHA the line claims the proof stands at (`at 15359cc (carried from 7f07565)`) went
  unchecked after the next restack; and an image linked into a commit's blob
  (`/blob/<sha>/…?raw=true`) on that same line was skipped too.
- `carried from` exempts only the SHA that follows it, not the whole line. A `STALE` line stays
  exempt for its text (it already says it is stale and the PR is not ready).
- An image whose link names a commit outside the head's history is named by `ship` on every line,
  `carried from` and `STALE` lines included, with its own off line: such a link can break when the
  forge drops the unreachable commit, whatever the caption says.
- Images are attached with the forge's CLI (the cards' rule already); the cards now say that a
  link into a commit of the CR's branch is not an upload, and that one found after a move is
  attached, or captured again at the moved head, before the PR turns ready.
- The proof is extended in the scenario's existing step for `ship`'s stale body lines (where this
  behaviour is covered today); no new unit test fixture.

## Settled by the Chief of Staff (after the spec critic)

- After a clean rebase, an image linked into the old commit: the Driver attaches the same image
  file with the forge's CLI (from `work/`, or from `git show <old>:<path>` while the commit is
  still local); it is captured again only when a Verifier is due anyway (a conflict, a refused
  carry). A clean rebase still starts no Verifier and no long gate. (Critic's recommended option.)
- `carried from` exempts the SHA right after it by position, not by value: the same SHA elsewhere
  on the line is still checked.
- No depends.json entry with ship-refuses-foreign-commits (same batch, same `ship` function and
  card paragraph): a rebase is expected.
