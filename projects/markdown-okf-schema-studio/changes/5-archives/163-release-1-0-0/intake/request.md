# 163 — Release 1.0.0 notes

Type: release · Owner: main session (Chief of Staff), with the user · No Foreman, no Driver.

## Intent (user, 2026-10-28, verbatim French)

> en attendant tu vas m'aider a préparer la release 1.0.0. la derniere release etait
> https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v0.3.1 et je vais publier main
> avec beaucoup de changement d'un coup. Le skill sera un peu dépasser, surtout qu'il n'y a pas de
> documentation reellement prete aujourd'hui.
>
> Donc il faut que l'on construise ensemble un Release notes elegante, en markdown dans un CR qui ne
> sera pas traduit par une PR (ou juste le bump). pas de foreman, fait le directement. ta release
> notes sera directement dans le dossier de CR. pose moi des questions, et propose moi des epreuves
> markdown format GFM

## Scope

- Deliverable: `release-notes.md` in this folder (GFM, for the GitHub release page of v1.0.0).
- Proofs to choose from: `proof-a-showcase.md`, `proof-b-compact.md`, `proof-c-tour.md`.
- Source: `CHANGELOG.md` "Unreleased" (127 entries), `git log v0.3.1..origin/main` (297 commits:
  70 feat, 102 fix, 13 perf, 45 docs), plus CRs 160-162 if they land before the release.
- Only code change, if any: the version bump through `scripts/version.py` (1.0.0).

## Decisions

Grill 2026-10-28 (user):

- Style: proof A "Showcase" (hero, six highlights with one picture each, full list folded).
- Documentation: "Guide" links point to the README; no mention of missing docs.
- Scope: release once CR 161 (heavy integration hotfix) has main green and CR 160 (agent plugin,
  PR #173) is merged; the notes present the plugin ("Usage with coding agent", before "Fast and
  safe"). Also the Ctrl+/ plain-comment fix (backlog P1 ctrl-slash-plain-comment), added 2026-10-28.
  CR 162 (toolbar motion) was merged by the user (#175), so it is in 1.0.0 too. (Updated 2026-10-28: the user wants
  the plugin install in the notes, not "copy the folder".)
- Full list: the CHANGELOG entries rewritten one line each, grouped by theme, folded.

- Screenshots: copied into `images/` (relative links). 9 of 15 showed the old toolbar; the README
  screenshot refresh (backlog P1 refresh-readme-screenshots) is part of 1.0.0; re-copy `images/`
  from main after it merges.

Draft: `release-notes.md` (first full draft 2026-10-28).
