# Answers

## Grill of 2026-11-10 (batch-09 paused; the user: "Grillons tous les P1 et P2")

1. **The theme.**
   - The user: "Même chose que la doc de okf-schema je crois que c'est pydata."
   - The user wants what okf-schema's docs do.
   - Checked by the Chief of Staff in `gsemet/okf-schema`'s `docs/source/conf.py`: `html_theme = "furo"`. So the theme is **Furo**, as in okf-schema, not pydata.
   - The Chief of Staff tells the user.
2. **Making "no AI slop" checkable.**
   - The user chose "Guide + revue + exemples (Recommandé)".
   - A short style guide with good and bad examples.
   - An agent reviews each page against that guide.
   - The pages are laid out in Diátaxis sections.
3. **What becomes of `docs/` and the README.**
   - The Chief of Staff told the user that okf-schema uses Furo.
   - The user: "Sphin prend la place de docs en portant tout en diataxis mais le readme garde les présentation avec les images . Certains parti peuvent être déplacée dans la doc. Attention les images devront aussi apparaître dans la doc".
   - The Sphinx site replaces `docs/`, and everything is carried over into Diátaxis sections.
   - The README keeps its presentation with the images. Some of its parts may move into the docs.
   - The images also appear in the docs.
5. **Set aside.**
   - After the full restatement, the user: "Met de cote on traitera plus tard la doc".
   - The CR is not called grilled enough. It moves to P3, with its answers kept.
4. **The visual identity.** Not shared with the landing page (see `landing-page`): the docs keep Furo, in okf-schema's style.

## Settled by the spec-writer (2026-11-18)

Points with no user-visible behaviour, decided while writing `03-change-spec.md`:

- The Sphinx source folder is `docs/` itself (`docs/conf.py`); images keep their paths, so the
  README and `scripts/docs_screenshots.py` do not change their image paths. `docs/demo/`,
  `docs/release-notes/`, the SVGs' `*-texts.md` and `docs/STYLE.md` are excluded from the build.
- Pages are written in Markdown through MyST, with `sphinx-design` and `sphinx-copybutton`, as in
  the user's other projects.
- The docs' dependencies are a `docs` dependency group in the root `pyproject.toml`, locked in
  `uv.lock`; the CLI's own dependencies do not change.
- The build is `just docs` (`sphinx-build -W --keep-going`), run by `just check` on the three
  systems; `just tools` fetches the `docs` group; no new CI job.
- `conf.py` reads the version from `pyproject.toml`; `scripts/version.py` is unchanged.
- The cards are not copied into the site; pages link them on GitHub.
- The style guide is `docs/STYLE.md`, outside the site, linked from `AGENTS.md` and
  `CONTRIBUTING.md`.
- Tests read the shipped files: the link test covers the section folders, and a new test checks
  that every image of `docs/` is named by a site page.
## Settled by the Chief of Staff (spec-writer's questions, 2026-11-18)
- Q1 slug: `chantier` (A). If it is taken at import, the user picks the slug and the PR's links
  follow it before merge.
- Q2: the Inspector, through one `AGENTS.md` rule (A).
- Q3: no CLI reference page (A).
- Q4: the existing SVGs and screenshots plus sphinx-design cards and tabs, no new figures (A).
- Q5: no release notes in the site, a link to GitHub Releases (A).

## Settled by the Chief of Staff (spec-critic's findings, 2026-11-18)
- README: the long sections move to the site (A). The README keeps its presentation, its images
  and a short paragraph per section with a link to the site; the detailed prose lives only in the
  site (answer 3: "certaines parties peuvent être déplacées dans la doc").
- Release-note links to the docs are pinned to the version, `/en/vX.Y.Z/`, for the header and
  the highlights alike (A); the user turns on tag builds on Read the Docs (one more user step).
- Split (A): this CR moves the pages, builds the site, sets up Read the Docs and rewires the
  links. The style guide (`docs/STYLE.md`), the page-by-page anti-slop review and the Inspector's
  rule go to `1-inbox/docs-style-guide-and-anti-slop-review-of`, stacked on this one.
- `docs/STYLE.md` is named in `AGENTS.md` and `CONTRIBUTING.md` as a path in backticks, never a
  link, so `chantier rules` does not make every role read it (that CR's concern, recorded here).
- This CR starts once batch-28's docs CRs (370, 374, 376) have merged: it joins batch-28 stacked
  after them.
- Pinned release links (A): after the tag, the Release Driver checks that
  `https://chantier.readthedocs.io/en/vX.Y.Z/` serves before publishing the notes and the thread,
  and waits for it; `docs/how-to/release-process.md` adds the step.

- Back from the trash (2026-11-20): dropped from batch-28 on the user's word so v0.14.0 could ship; user, 2026-11-20: "En backlog P2". Its draft PR #346, worktree and branch are kept: the next Driver resumes them.

# Decision (2026-11-25, the owner, in chat)

"tu vas te concentrer sur livrer les CR 507 a 514 sur le rework. tu vas annuler les specs de tous les autres mais eviement pas perdre les reponses que j avais donnee en interview. Avec le rework en cours il faudra refaire la specification de tout, et on fera ca dans un batch 32."

The specification is cancelled: it is kept for reference in `work/spec-before-rework.md`, and is to be written again after the rework, from these answers, for batch-32.

Destination: none for now; to specify again for batch-32.
