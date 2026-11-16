# Answers

## Grill of 2026-11-10 (batch-09 paused; the user: "Grillons tous les P1 et P2")

1. **One CR or five.** The five P1s from the v0.8.0 release retro are:
   - `just-tag-checks-head`;
   - `release-create-full-command`;
   - `release-user-merge-no-go`;
   - `release-verify-merge-commit`;
   - `scan-uuid-after-underscore`.

   The user chose "Une seule CR (Recommandé)". They are merged into this CR. Their requests are in `intake/`, and their folders are in `6-trash/261110-2222-*`.
2. **`just tag`.** The user chose "Refuser si ça ne colle pas (Recommandé)".
   - `just tag` refuses unless the subject of origin/main's head is `release: v<the local version>`.
   - This covers the merge-commit check, so CONTRIBUTING needs no separate `gh pr view --json mergeCommit` step.
   - No expected-SHA argument.
3. **A merge the user already did.** The user chose "Vérifier et continuer (Recommandé)".
   - The Release driver sees the merge on the forge (`gh pr view`) and goes on to the next step without asking.
   - The user's merge is the go.

## Grilled enough (2026-11-10)

- **The full restatement:**
  1. `just tag` refuses unless origin/main's head subject is `release: v<the local version>`.
  2. CONTRIBUTING writes the full `gh release create` command, with `--title vX.Y.Z` and `--verify-tag`.
  3. The Release driver asks no release go for a merge the user already did: it sees it on the forge and goes on.
  4. `scripts/release_notes.py --scan` catches a UUID right after `_` (such as `local_<uuid>`), with a structure test.

  All in one PR.
- The user chose "Oui, grillé (Recommandé)".

## The specification's open question (2026-11-10)

- **The question:** does the user's merge also stand as the go for the tag push?
- **The answer taken: no.** The user had said "Oui lance les spec et le batch. Fait une stack", so the Chief of Staff took the specification's default, the safer reading:
  - the user's merge replaces only the go for the merge itself;
  - the tag push and every other irreversible action keep their own `release go`.
- The Chief of Staff tells the user, who may change it while reviewing the PR.
