# 254 — Release 1.3.0

Type: release · Owner: main session with the owner · No Foreman, no Driver.
Process: [release-process.guidelines.md](../../../.agents/guidelines/release-process.guidelines.md)
(written for this release, model 1.2.0). Version PR: https://github.com/gsemet/markdown-okf-schema-studio/pull/303

## Intent (owner, 2026-11-03, French)

> On va clôturer les P1 et P2 restant et faire une release.

> je ne vois pas la release notes de préparer en local pour revue (dans le CR) ni le tweet
> d'announce. regarde la release 1.2 pour le modele, encode le modele dans une guidelines
> 'release-process.guidelines.md'. Le tweet doit être plus organique, comporter 3 tweets, le
> premier peut être long, avec 1 images percutante, et the second tweet c'est la release notes
> github, la troisieme l'url vers le marketplace vscode.

## Scope

- CRs 236–253 (16 landed, plus 242 in #301 and 248 in #302, which must land first).
- Deliverables here: `release-notes.md`, `tweet.md`, `images/`.
- In the version PR #303: changelog backfill, the release instructions, the hero image scenario
  (`rendering-core/v27-release-1-3-showcase-cream-1200`), the version commit.

## Status

- 2026-11-03: #301 and #302 landed. The Grid form header/footer bug found while capturing the hero
  image is fixed in #304 (owner: fix before 1.3). Stack: #304 (bottom), #303 (one squashed version
  commit, top). Notes count 35 changes.
