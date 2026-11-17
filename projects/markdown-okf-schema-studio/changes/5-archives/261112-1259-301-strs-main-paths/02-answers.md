# Answers

## 2026-11-12

- Owner: "il faudra faire créer intelligemment les main path la ou c'est possible idéalement sur
  tous les StRS".
- Owner: "Ok pour 2 CR": the Main paths are their own change, before the viewer.
- Priority P1. Same batch as `gallery-page-social-card` and `requirements-viewer`.
- The check that every cited SwRS exists, is active and derives from its StRS is a project script
  run by `just requirements-lint` and CI; okfreq is not changed (owner chose "Project script").
- Owner, 2026-11-12: "Oui tu peux tout lancer" (go for the specifications and the batch).
- Spec questions, owner's choices on 2026-11-12:
  - The 16 approved StRS: "Yes, all 16". The owner explicitly agrees that this CR adds Main paths
    to them; `approved_by` and `approved_at` are stamped again and the owner reviews the PR.
  - A path may cite a `draft` SwRS: "Yes, draft allowed" (active = draft, proposed or approved).
  - The check script gets no SwRS of its own: "No SwRS".
- Owner, 2026-11-12: "No more question. Finish the work autonomously" (go for the batch).

## 2026-11-12: review of PR #372 (owner)

- Owner's words: "Il faut rebase 372. Et pour moi c'est mergeable oui"
- Decision: rebase PR #372 on `main` (it is BEHIND since #371 merged); after the rebase the owner considers it mergeable, accepting the unconfirmed local `ci-integration` real-input failure (no `src/` change) and the 16 restamped approved StRS.
