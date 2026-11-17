# Prompt for Chantier: a visual of what a release driver does

Paste the section "Prompt" into a Chantier session. The section "Timeline of release 1.6.1" is the
real data the visual is built from; keep it with the prompt.

## Prompt

> Make a swimlane timeline SVG for the Chantier docs, in the style of the existing diagrams in
> `docs/` (own background rectangle, mid-tone strokes, readable in light and dark, text 14 px or
> more, a `<title>` and a `<desc>` that tells the whole story in prose, and a companion
> `*-texts.md` like the other diagrams). It shows what a release driver does, from the owner's
> "release" to the archive, using a real release as the example: Markdown OKF-Schema Studio 1.6.1
> (timeline below, times in UTC).
>
> Lanes, top to bottom: **Owner**, **Chief of Staff**, **Release driver**, **CR drivers (fix
> CRs)**, **CI**, **GitHub and Marketplace**. A horizontal time axis from 07:30 to 12:00 UTC,
> with a compressed break before it for the night when the stack PRs were opened (22:55 the day
> before).
>
> Show:
> 1. The owner's four touchpoints only, as diamonds in the Owner lane: merges the stack; "is a
>    release worth it?" → "yes, now"; reviews the notes and the thread in the version PR and says
>    "publish"; posts the thread. Nothing is asked of the owner between the notes review and the
>    publication: draw that span as a bracket labelled "owner asked nothing".
> 2. The gates as bars in the CI lane: heavy run on `main` HEAD (must be green on that exact
>    commit before the version commit exists), then the version push run, whose jobs fan out
>    (static, static-windows, visual, integration, stress) and then tag, package and publish,
>    Pages.
> 3. The outputs in the GitHub and Marketplace lane: tag, GitHub release with its images,
>    Marketplace version, Pages.
> 4. The release driver's own work: release CR folder, notes and thread drafted from the
>    changelog, version commit and version PR (draft until mergeable), monitoring, `report.md`,
>    `retro.md`.
> 5. The fix-CR path as a dashed branch in the CR drivers lane: "a red heavy job → the Foreman
>    runs a fix CR (at most 3 rounds) → the release driver merges it → heavy run again". It did
>    not happen in 1.6.1: label it "not needed in 1.6.1".
> 6. Two steps added after 1.6.1, each with a small "new" tag: the version PR body shows the
>    rendered release notes and thread, separated by `---` rules (the owner comments on the
>    delivered files); and the archive gets a `retro.md` whose fixes the owner picks at the end
>    of the run.
> 7. A closing loop arrow from the archive back to the intake: "retro and owner remarks become
>    process CRs" (in 1.6.1: two process PRs landed the same day).
>
> Footnote, small: "In 1.6.1 the Chief of Staff held the release driver role in direct mode;
> with a Foreman, the Foreman starts a release driver once the stack is merged."
>
> Keep the labels generic (the project's release procedure, its heavy CI, its marketplace), and
> put the 1.6.1 values (times, PR numbers, counts) as small annotations, so the diagram explains
> Chantier and the example proves it.

## Timeline of release 1.6.1 (UTC, 2026-11-10 → 2026-11-11)

| Time | Lane | Event |
| --- | --- | --- |
| 22:55–23:31 (day before) | CR drivers | Stack of six table fixes opened as draft PRs (#346, #347, #348, #350, #351, #352) |
| 07:36 | Owner | Merges the bottom of the stack (#346, #347, #348) |
| 08:24 | Owner | Merges #350 |
| 08:59 | Chief of Staff | Process CR "Verifier step" opened (#353), after the owner noticed missing screenshots |
| 09:02 | Owner | Merges #351 |
| 10:15 | Owner | Merges #353 (Verifier step) |
| 10:37 | Owner | Merges #352, the last of the stack. Asked before: "once merged, check the heavy pipeline and tell me if a release is worth it" |
| 10:37–10:59 | CI | Heavy run on `main` HEAD `2e9cf0b9` (run 43005192087): integration and stress green on that commit |
| ~11:00 | Chief of Staff | Assessment: 7 user-visible fixes since 1.6.0 → patch 1.6.1. Owner: "yes, do it now" |
| 11:00–11:16 | Release driver role | Notes (13 changes since 1.6.0, three highlights, before/after picture of the cell editor in a narrow pane) and a three-post thread, from `CHANGELOG.md`; `just version 1.6.1`; one `chore: version 1.6.1` commit with the notes folder; two changelog lines that were missing added in that commit |
| 11:16 | Release driver role | Version PR #354 opened as a draft; `just release-notes-check` and CI green; marked ready. Autonomous decisions listed in the body: patch version, the added changelog lines, no hero image |
| 11:16–11:30 | Owner | Reviews the notes and the thread in #354: "OK to publish, you can merge the PR" |
| 11:30 | Release driver role | Merges #354 by rebase (`96a86e46`) |
| 11:30–11:43 | CI | Version push run 43012439055: static (3 min), static-windows (4 min), visual (13 min), integration (12 min) |
| 11:52 | CI | Stress done (22 min), the last heavy job |
| 11:52–11:53 | GitHub | Tag `v1.6.1`, GitHub release with the VSIX and the two images (published 11:53:53) |
| 11:53 | Marketplace | `vsce publish`: "Published GaetanSemet.markdown-okf-schema-studio v1.6.1"; the Marketplace page shows 1.6.1 a few minutes later |
| 11:53–11:55 | GitHub | Pages built and deployed |
| ~12:05 | Release driver role | Checks tag, release, Marketplace and Pages; archives the release CR with `report.md` (tag, release URL, both CI runs, no issue closed) |
| afternoon | Chief of Staff | Owner's remark → process CR: the version PR body shows the rendered notes and thread (#355, merged); then the retro step (#356, merged); stale branches cleaned, branches now deleted on merge |

## Numbers for annotations

- Stack merged to published: 07:36 → 11:53, about 4 h 20; heavy run on `main` to published: 1 h 16.
- Version PR open to merge: 14 min; version push to Marketplace: 23 min.
- Owner interventions during the release: 4 messages. Fix CRs: 0. Red jobs: 0. Retries: 0.
- Owner's own words for the touchpoints: "une fois mergé tu vérifies si la pipeline lourde passe et
  tu me dis si ça vaut le coup de préparer une release" · "Oui fais-la maintenant" · "Ok pour
  publication tu peux merger la PR."
