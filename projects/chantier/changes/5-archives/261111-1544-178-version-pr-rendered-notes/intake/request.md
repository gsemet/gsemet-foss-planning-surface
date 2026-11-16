# The version PR's body shows the rendered release notes and thread

Found by the `release-driver-diagram` specification (2026-11-11), comparing the target diagram
with the cards: the one step the cards do not do yet.

- What is wanted: the Release driver puts the release notes, then the thread, rendered (images
  included), in the version PR's body, separated by `---` rules, so the owner reviews them where
  they approve the release.
- Today: drafts go by `note --draft` and `status`'s `draft <path>`; nothing puts them in the PR.
- Touches: `driver.md` "Release driver" and `release-template.md` "Where they go" (the agent
  files on both hosts are unchanged: the contract is in the cards); for chantier itself,
  `docs/release-process.md`.
