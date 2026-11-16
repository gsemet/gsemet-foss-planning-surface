# Answers

## Grill of 2026-11-10 (batch-09 paused; the user: "Grillons tous les P1 et P2")

1. **What "auto" covers.**
   - While a release runs, the Chief of Staff offers to say "auto". The question was what the Release driver then does alone.
   - The user chose "Merge, tag, publication (Recommandé)".
   - In auto, the Release driver merges the version PR, tags, and publishes the GitHub release without asking.
   - Announcements (posts) stay drafts for the user.
2. **How often a tip comes.**
   - The key moments: first use, after a `status`, at the end of a batch, during a release.
   - The user chose "Un par moment, par session (Recommandé)".
   - A tip is one short line, at most once per key moment and per session.
   - "plus de conseils" (no more tips) turns them off.

## Grilled enough (2026-11-10)

- **The full restatement:**
  1. During a release, the Chief of Staff offers "auto". The Release driver then merges the version PR, tags and publishes the GitHub release without asking. Announcements stay drafts for the user.
  2. One-line tips come at the key moments: first use, after a `status`, at the end of a batch, during a release. At most one per moment and per session. "plus de conseils" turns them off for the session.
- The user chose "Oui, grillé (Recommandé)".

## The specification's open questions (2026-11-10)

The user had said "Oui lance les spec et le batch. Fait une stack", so the Chief of Staff took the specification's recommended answer on each question. The user may change them while reviewing the PR.

1. **"auto" in an approval question.** "auto" is one of the answers to the approval question, not a tip line. It stays even after "plus de conseils".
2. **A batch with no budget.** The CLI refuses a release grant then. The Chief of Staff asks for a budget, with a proposed figure, before it sends the grant.
3. **The other tips.** Tips come only at the four key moments. The other tips (at the end of a piece of work, in a quiet turn) go.
4. **A project that also publishes a package** (npm, PyPI). "auto" covers every publication step of the procedure, never an announcement post.
