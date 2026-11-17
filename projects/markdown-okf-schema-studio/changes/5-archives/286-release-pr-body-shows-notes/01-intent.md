---
title: Show the release notes and the announcement thread in the version PR body
description: The owner reviews the rendered notes and thread in the version PR description, and comments on the files.
status: inbox
date: 2026-11-10
---

# Show the release notes and the announcement thread in the version PR body

Owner's request, 2026-11-10, during release 1.6.0 (PR #342).

## The request

The body of the version pull request (`chore: version X.Y.Z`) shows, rendered:

1. the release notes (`docs/releases-notes/<date>-vX.Y.Z/release-notes.md`);
2. a `---` rule;
3. the announcement thread (`tweet.md`).

So the owner reads the result in the PR page. To make a remark, the owner comments on the files
in the PR diff (`release-notes.md`, `tweet.md`), line by line; the release driver applies the
comments and refreshes the body.

## Points to settle

- Images: the notes link images by file name; in the PR body they need a URL that renders before
  the tag exists (for example `raw.githubusercontent.com/<owner>/<repo>/<head sha>/docs/releases-notes/...`),
  while the committed file keeps relative links (the release check requires them).
- Where it is written: `release-process.guidelines.md` (step 5, version PR) and the release driver's
  role in the lifecycle; maybe `.github/PULL_REQUEST_TEMPLATE.md` for the version PR.
- The body is refreshed when the notes change during the review.

## Asked again (2026-11-11, release 1.6.1, PR #354)

Owner: "Rajoute en CR post merge: la prochaine release je veux voir le contenu de la release notes
et le tweet dans la description de la PR. Séparation avec triple - ou autre moyen visuel clair. Quand
j'aurai des remarques je mets dans le fichier md livré dans la PR."

- Moved to P1. To run as a CR right after release 1.6.1 is published, so release 1.6.2 or 1.7.0
  uses it.
- Separation: a `---` rule, or another clear visual break (for example a heading per part).
- Remarks: the owner comments on the delivered `release-notes.md` and `tweet.md` in the PR diff.
