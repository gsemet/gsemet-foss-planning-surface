# Answers: version-pr-rendered-notes

## Decisions of 2026-11-11

Decided by a Fable advisor on the user's delegation: "Grille tout avec une session fable je ne sais pas te répondre…"

1. **When the release has a version PR, its body shows the release notes, then the announcement
   thread, as rendered Markdown, each after a `---` rule, under the PR's own description.**
   Reason: the owner reviews them where they approve the release, on a phone too.
2. **It is the default, under the project's own procedure.** A project that says where its notes
   are reviewed is followed as written; a release with no PR (a tag only) keeps today's drafts
   and nothing more. Reason: the mechanics of a release are always the project's.
3. **The draft files stay the source; the body is a copy.** `note --draft` and `status`'s
   `draft <path>` stay as today. The Driver refreshes the body from the files each time they
   change and before it asks for the merge, and never rewrites the drafts from the body. A
   change the user wants is told to the Chief of Staff or made in the file. Reason: one source,
   so an edit is never lost between two copies.
4. **The thread's section is headed as a draft the user posts themselves.** Reason: no agent
   posts it, and a reader of the PR must not take it for published.
5. **Images show in the body only once uploaded, and the upload keeps its `release go`,** as
   `release-template.md` says today; they are anonymised first. Until then, and where the forge
   cannot upload, the body names the image in prose. Reason: an image on the forge leaves the
   machine and others see it; the existing rule already covers it.
6. **What the forge's size limit does not let in is named by its path in the body, not cut
   silently.** Reason: the reviewer must know the body is not the whole text.
7. **Cards only:** `driver.md` "Release driver" and `release-template.md` "Where they go"; for
   chantier itself, `docs/release-process.md`. No CLI change, no agent-file change. Reason: the
   contract is in the cards; the Driver already edits its PR.
8. **Point 2 of `cr-171-retro-fixes` (a Driver reads its team with `handoff`) rides in this
   CR.** Reason: both are small `driver.md` changes; one long gate.

## Merged item (2026-11-11)

This CR also carries point 2 of `cr-171-retro-fixes` (its answers 1 and 2: `driver.md` says a
Driver reads its `team:` lines with `handoff`; `round` only starts a round; no CLI change), on
the Fable advisor's grouping. Its request and answers are in `intake/`.

## The specification's open question (2026-11-11)

Settled by the Chief of Staff on the user's delegation ("Grille tout avec une session fable je
ne sais pas te répondre…").

- **An image already committed and pushed with the version PR's branch is on the forge:** the
  body links it at the PR's head, with no new `release go`. Only a new upload (a release asset,
  a PR attachment) waits for one. Reason: the push is already part of the reviewed PR; nothing
  new leaves the machine.
