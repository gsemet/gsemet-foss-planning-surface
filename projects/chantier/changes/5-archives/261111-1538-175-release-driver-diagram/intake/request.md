# A docs diagram: what a release driver does, from a real release

Sent on 2026-11-11 by the Markdown OKF-Schema Studio Chief of Staff, at the user's request (the
user announced it here: "tu vas recevoir une demande d'une autre session"). It is a request to
bring to the user, not a go.

## The request

A swimlane timeline SVG for `docs/`, in the style of the existing diagrams (own background
rectangle, mid-tone strokes, readable in light and dark, text 14 px or more, a `<title>` and a
`<desc>` that tells the whole story in prose, a companion `*-texts.md`). It shows what a release
driver does, from the owner's "release" to the archive, with Markdown OKF-Schema Studio 1.6.1 as
the example (times in UTC).

- Lanes, top to bottom: Owner, Chief of Staff, Release driver, CR drivers (fix CRs), CI, GitHub
  and Marketplace. Time axis 07:30 to 12:00 UTC, with a compressed break before it for the night
  when the stack PRs were opened (22:55 the day before).
- Show:
  1. The owner's four touchpoints only, as diamonds: merges the stack; "is a release worth it?"
     → "yes, now"; reviews the notes and the thread in the version PR and says "publish"; posts
     the thread. A bracket "owner asked nothing" between the notes review and the publication.
  2. The gates as bars in the CI lane: the heavy run on `main` HEAD (green on that exact commit
     before the version commit exists), then the version push run, its jobs fanning out
     (static, static-windows, visual, integration, stress), then tag, package and publish,
     Pages.
  3. The outputs: tag, GitHub release with its images, Marketplace version, Pages.
  4. The release driver's own work: release CR folder, notes and thread from the changelog,
     version commit, version PR (draft until mergeable), monitoring, `report.md`, `retro.md`.
  5. The fix-CR path, dashed, in the CR drivers lane: "a red heavy job → the Foreman runs a fix
     CR (at most 3 rounds) → the release driver merges it → heavy run again", labelled "not
     needed in 1.6.1".
  6. Two steps added after 1.6.1, each tagged "new": the version PR body shows the rendered
     notes and thread, separated by `---` rules; the archive gets a `retro.md` whose fixes the
     owner picks at the end.
  7. A loop arrow from the archive back to the intake: "retro and owner remarks become process
     CRs" (in 1.6.1: two process PRs landed the same day).
- Footnote: "In 1.6.1 the Chief of Staff held the release driver role in direct mode; with a
  Foreman, the Foreman starts a release driver once the stack is merged."
- Generic labels (the project's release procedure, its heavy CI, its marketplace); the 1.6.1
  values as small annotations.

## Timeline of release 1.6.1 (UTC, 2026-11-10 → 2026-11-11)

| Time | Lane | Event |
| --- | --- | --- |
| 22:55–23:31 (day before) | CR drivers | Stack of six table fixes opened as draft PRs (#346, #347, #348, #350, #351, #352) |
| 07:36 | Owner | Merges #346, #347, #348 |
| 08:24 | Owner | Merges #350 |
| 08:59 | Chief of Staff | Process CR "Verifier step" opened (#353), after the owner noticed missing screenshots |
| 09:02 | Owner | Merges #351 |
| 10:15 | Owner | Merges #353 |
| 10:37 | Owner | Merges #352, the last of the stack; asked before: "once merged, check the heavy pipeline and tell me if a release is worth it" |
| 10:37–10:59 | CI | Heavy run on `main` HEAD `2e9cf0b9` (run 43005192087): integration and stress green |
| ~11:00 | Chief of Staff | 7 user-visible fixes since 1.6.0 → patch 1.6.1; owner: "yes, do it now" |
| 11:00–11:16 | Release driver role | Notes (13 changes, three highlights, a before/after picture) and a three-post thread from `CHANGELOG.md`; `just version 1.6.1`; one `chore: version 1.6.1` commit with the notes folder and two missing changelog lines |
| 11:16 | Release driver role | Version PR #354 opened as a draft; `just release-notes-check` and CI green; marked ready; autonomous decisions listed in the body |
| 11:16–11:30 | Owner | Reviews the notes and the thread in #354: "OK to publish, you can merge the PR" |
| 11:30 | Release driver role | Merges #354 by rebase (`96a86e46`) |
| 11:30–11:43 | CI | Version push run 43012439055: static (3 min), static-windows (4 min), visual (13 min), integration (12 min) |
| 11:52 | CI | Stress done (22 min), the last heavy job |
| 11:52–11:53 | GitHub | Tag `v1.6.1`, GitHub release with the VSIX and two images (11:53:53) |
| 11:53 | Marketplace | `vsce publish` of v1.6.1; the page shows it a few minutes later |
| 11:53–11:55 | GitHub | Pages built and deployed |
| ~12:05 | Release driver role | Checks tag, release, Marketplace and Pages; archives the release CR with `report.md` |
| afternoon | Chief of Staff | Owner's remark → process CRs: rendered notes in the version PR body (#355), the retro step (#356); stale branches cleaned |

Times marked "~" are reconstructed.

## Numbers for annotations

- Stack merged to published: 07:36 → 11:53, about 4 h 20; heavy run on `main` to published:
  1 h 16.
- Version PR open to merge: 14 min; version push to Marketplace: 23 min.
- Owner interventions: 4 messages. Fix CRs: 0. Red jobs: 0. Retries: 0.
- The owner's words: "une fois mergé tu vérifies si la pipeline lourde passe et tu me dis si ça
  vaut le coup de préparer une release" · "Oui fais-la maintenant" · "Ok pour publication tu
  peux merger la PR."

Repository: gsemet/markdown-okf-schema-studio (public): PRs #346–#356, runs 43005192087 and
43012439055, release v1.6.1.

## Open for the grill

- Whether chantier's own release driver does what this diagram says (the version PR with the
  rendered notes, the `retro.md` in the archive, the Foreman starting it once the stack is
  merged), or whether the diagram shows a target, as the other docs SVGs do.
- Where it sits in `docs/` and the README.
