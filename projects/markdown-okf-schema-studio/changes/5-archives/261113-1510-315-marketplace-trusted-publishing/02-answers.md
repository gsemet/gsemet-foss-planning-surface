# Answers

## 2026-11-13: Marketplace policy created

Owner, 2026-11-13, with the Chief of Staff in the browser: Trusted Publishing policy created on the
`GaetanSemet` publisher (marketplace.visualstudio.com/manage/publishers/gaetansemet/trustedpublishing):
name "Release workflow", provider GitHub Actions, repository owner `gsemet` (#133498), repository
`markdown-okf-schema-studio` (#1418546863), workflow `release.yml`, environment `release`. State:
Active, last used Never.

`VSCE_PAT` stays in the `release` environment until the first release published with `--oidc`
succeeds; then the owner deletes it (Microsoft's migration advice).

Installed `@vscode/vsce` is 4.0.0, which has no `--oidc` (`vsce publish --help`); npm has 4.1.0 and
4.1.1 (published 2026-11-12).

## 2026-11-13: run it now

Owner, 2026-11-13, asked whether to run this CR now: « Oui, lance-la ». Then, mid-turn: « je garde
le token pour l'instant » (read as: the tokens stay for now; `VSCE_PAT` stays in any case until
an OIDC release succeeds).

## 2026-11-13: grill

1. vsce version. Owner: « 4.1.0 ». `@vscode/vsce` pinned to 4.1.0 (4.1.1 is a day old).
2. On an OIDC failure at release time. Owner: « je ne sais pas que me recommende tu ? normalement
   la publicaiton devrait marcher ». Chief of Staff's recommendation, adopted unless the owner
   corrects it: no automatic fallback to `VSCE_PAT`. The Marketplace step runs before the GitHub
   release step, so a failed exchange fails the job before the GitHub release is written; the
   recovery is a fix then `workflow_dispatch` of `release.yml` with the tag (the existing path),
   or, in an emergency, a local `vsce publish` with the PAT the owner keeps.
3. Proof before the next feature release. Owner: « on peut faire un 1.8.1 fake si tu veux ».
   Proposed: a 1.8.1 maintenance release right after this CR merges, as a release CR in the same
   batch; its release notes say the release changes only how the extension is published.

## 2026-11-13: go

Owner, 2026-11-13, on the restatement (recommendation 2 adopted, 1.8.1 release CR after this one,
batch-03 as a stack in direct mode, this CR automatable with a specification the owner does not
review): « Oui, lance ».

## 2026-11-13: open question 1 of the specification (second policy)

Owner, 2026-11-13, on the recommendation to add a second Marketplace policy for `ci.yml`:
« Oui, remplis-la ». The Chief of Staff filled it on the `GaetanSemet` publisher (name "CI
workflow (calls release.yml)", owner `gsemet`, repository `markdown-okf-schema-studio`, workflow
`ci.yml`, environment `release`); the owner clicks Create. No change to this CR's scope.

## 2026-11-13: the local gate

Owner, 2026-11-13, on the blocked local `just preflight` (only `ci-integration` fails: real VS Code
window steps time out while Shottr is frontmost): « Heavy run en CI ». The proof is the heavy run
on the branch (`gh workflow run ci.yml --ref <branch> -f heavy=true`), `integration` and `stress`
green on the PR's exact head; the local real-window failure is recorded in the PR, not a blocker.
