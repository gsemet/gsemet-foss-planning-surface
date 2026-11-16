# Answers

- 2026-11-07, the user: a release of chantier ships release notes with the most visual evidence
  possible, usage and call examples, and links to the relevant docs; and an announcement thread
  of three posts (the first may be long) with one image. The model is Markdown OKF-Schema Studio
  ("c'est topissime"): `.agents/guidelines/release-process.guidelines.md` and
  `docs/releases-notes/` in `gsemet/markdown-okf-schema-studio`.
- 2026-11-07, the user, on the scope: both. A guideline specialised for chantier's own releases,
  and a generic model for the users' projects (the release Driver's), which also tries to put
  screenshots and visible evidence of what is delivered in the release notes, to explain what
  ships.
- 2026-11-07, the user, on chantier's visuals: captures of the board and of the reports (a real
  batch or the scenario), excerpts of a conversation with the Chief of Staff, and CLI output.
  Not the docs SVG diagrams by default. Everything shown is anonymised with care (no personal
  path, user name, email, private repository or session id).
- 2026-11-07, the user, on the mechanics: as Studio. The notes, the thread and their images in
  `docs/release-notes/YYYY-MM-DD-vX.Y.Z/`, reviewed by the user in the version PR, checked by
  `just check` (invalid notes fail it), published as they are with
  `gh release create --notes-file` (not `--generate-notes`), images attached to the release.
- 2026-11-07, the user, on post 3: one sentence (install or update, free, the licence) and the
  link to the README's Install section.
- 2026-11-07, the user, on the generic model: a default shipped in the skill (as
  `pr-template.md`): visual release notes and a three-post thread, applied by the release Driver
  when the project has no release procedure of its own; the project's own ranks above it.
- 2026-11-07, the user, on chantier's captures: from the release's real batch, anonymised. The
  release Driver renders to PNG (headless Chrome) the batch's `STATUS.md` and report, with paths,
  names and ids replaced.
- 2026-11-07, the user: P1, beside docs-lifecycle; release 0.8.0 is the first to use the new
  procedure.
- 2026-11-07, the user (spec-writer's open question 1): when the user confirms the release
  (`order confirm`), the Chief of Staff writes its latest Progress report and the conversation
  excerpts it chooses into the release CR's folder, as `report.md` and `conversation.md`; the
  release Driver renders them from there, anonymised.
- 2026-11-07, the user (open question 2): for chantier, the release CR joins the batch whose work
  it ships (`order add --release`), so the board and `STATUS.md` show that work.
- 2026-11-07, the user (open question 3): a docs SVG diagram is shown in the notes only on the
  user's word in the release CR's grill.
