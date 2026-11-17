# Answers

## 2026-11-12: picked for the next batch

Owner, 2026-11-12: « je suis d'accord. grille avec un advisor fable et fini par une CR de release. demande moi uniquement quand il y a un impact utilisateur », agreeing to add this item to the batch after the v1.7.1 retro items, and to put it back to P1 as their 2026-11-03 words said.
Priority P1. Open questions: a Fable advisor answers them; the owner is asked only on a user impact.

## 2026-11-12: delivery of the batch

Owner, 2026-11-12: « tu livreras une stack prete a mergée avec le PR de release en dernier ».
Open: this conflicts with the release-process guideline (the version commit is never stacked on
top of development; the stack lands first, then the heavy run on `main` HEAD, then the version PR).
The conflict was reported to the owner.

Owner, 2026-11-12, on the conflict: « Yes, and update the guide ». The release PR is the top of the
stack; before it turns ready, the heavy run is dispatched on the stack's top branch
(`gh workflow run ci.yml --ref <branch> -f heavy=true`); the owner merges the whole stack by
rebase in order; the version push on `main` stays the final gate and makes the tag.

## 2026-11-12: Fable advisor

A Fable advisor (read-only, at origin/main cb968299) answered the INTERNAL questions; its report is
`intake/advisor-grill.md` (the section of this CR). Its INTERNAL recommendations are adopted, per the
owner's instruction to be asked only on a user impact. USER-IMPACT questions go to the owner.

## 2026-11-12: left out of the batch

Owner, 2026-11-12: « exclu "Open VSX" pour l'instant. ok pour tout le reste. » This CR is left out of the batch; it stays P1 in the backlog for later.

## 2026-11-13: account set up, 1.8.0 published by hand, trusted publishing instead of a secret

Owner, 2026-11-13: « faisons ensemble open vsx ». Done with the Chief of Staff:

- Open VSX account (GitHub login), Eclipse account linked, Publisher Agreement signed.
- Namespace `GaetanSemet` created; ownership claim filed:
  https://github.com/EclipseFdn/open-vsx.org/issues/15660 (option 1, Marketplace publisher with repo).
- 1.8.0 published by hand from the GitHub release VSIX with a one-off access token
  (`Published GaetanSemet.markdown-okf-schema-studio v1.8.0`); the token is to be deleted right after.

Scope change, on the owner's word (« il y a moyen de ne pas faire de token »): the release job
publishes with Open VSX trusted publishing (GitHub OIDC), not an `OVSX_PAT` secret. The job gets
`permissions: id-token: write` and runs `npx ovsx publish --trusted-publishing` on the same VSIX.
Registration on Settings → Trusted Publishers: owner `gsemet`, repository
`markdown-okf-schema-studio`, workflow `release.yml`, environment `release`. It needs the namespace
ownership granted (issue above) and the extension to exist with one active version (now true), see
https://github.com/eclipse-openvsx/openvsx/wiki/Trusted-Publishing. No secret to add, so the
CONTRIBUTING "GitHub Configuration" change names the registration instead.

Follow-up idea from the owner (separate item): the VS Code Marketplace may also move away from
tokens; `vsce publish --azure-credential` with `azure/login` OIDC would remove `VSCE_PAT`.

## 2026-11-13: state, parked for later

Owner, 2026-11-13: « met a jour l'etat dans le CR que l'on traitera plus tard ».

Done:

- [x] Open VSX account, Eclipse account linked, Publisher Agreement signed.
- [x] Namespace `GaetanSemet` created (`verified: false` until the claim below is granted).
- [x] Ownership claim filed: https://github.com/EclipseFdn/open-vsx.org/issues/15660.
- [x] 1.8.0 published by hand (accepted by the registry at 14:36 local time).

Waiting, outside this repository:

- [ ] The one-off access token "first publish" (never expires) deleted by the owner. Owner,
  2026-11-13: « je garde le token pour l'instant ».
- [ ] 1.8.0 visible: right after the publish, `GET /api/GaetanSemet/markdown-okf-schema-studio`
  still answered "Extension not found" (probably the registry's checks before activation; not
  confirmed). If it stays hidden, look at Settings → Extensions on open-vsx.org.
- [ ] Namespace ownership granted (issue above).
- [ ] Trusted publisher registered (values in the entry above). Needed before the first release
  that runs the new step, not before this CR is developed or merged.

To do in this CR: the `release.yml` step with `id-token: write` and
`npx ovsx publish --trusted-publishing --skip-duplicate`, CONTRIBUTING, and the Cursor
compatibility report from the scope. If the registration is not done by the next release, the Open
VSX step fails alone; the Marketplace step runs before it.

## 2026-11-14: namespace granted

Owner, 2026-11-14: the claim was accepted
(https://github.com/EclipseFdn/open-vsx.org/issues/15660, closed as completed 2026-11-13T20:14Z).
Checked by the Chief of Staff: `GET /api/GaetanSemet` answers `verified: true`, and
`GET /api/GaetanSemet/markdown-okf-schema-studio` serves 1.8.0, verified.

- [x] Namespace ownership granted.
- [x] 1.8.0 visible.
- [x] Trusted publisher registered 2026-11-14 by the owner (form filled by the Chief of Staff,
  checked on the page: GitHub · gsemet/markdown-okf-schema-studio · workflow `release.yml` ·
  environment `release`; one trusted publisher per extension). Lesson from the Marketplace (CR-316): the
  policy matched the CALLED workflow `release.yml`, not the caller `ci.yml`; register
  `release.yml` here too, and check on the first release which one Open VSX matches.
- [ ] The one-off "first publish" token deleted by the owner (kept for now).

## 2026-11-14: scope added by the owner

Owner, 2026-11-14: « il faudra que le process de release watch les 2 marketplaces pendant 10-15
min, et il faudra mettre les liens vers les 2 marketplace dans la release notes et le README. Dans la
release note "[Install from the Marketplace](…)" => "[Install from VS Code Marketplace](…)" + meme
chose pour OpenVSX + met a jour les instructions d'install et les doc ».

Added to this CR:

- Release process (`.agents/guidelines/release-process.guidelines.md`, and CONTRIBUTING "How to
  Release" if it lists the checks): after the release job, watch both registries for 10 to 15
  minutes until each serves the new version (VS Code Marketplace gallery API, Open VSX API), and
  report each one's state.
- Release notes: the install link line becomes two links, "[Install from VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=GaetanSemet.markdown-okf-schema-studio)"
  and "[Install from Open VSX](https://open-vsx.org/extension/GaetanSemet/markdown-okf-schema-studio)",
  in the guideline's template and wherever the notes are generated or checked
  (`just release-notes-check`).
- README and the user docs: install instructions name both registries with their links (VS Code
  from the Marketplace; VSCodium, Cursor and other compatible editors from Open VSX).

## 2026-11-14: merge on the owner's word

Owner, 2026-11-14, before the night: « soit le plus autonome tu peux faire 2 releases tout seul ».
The release needs this CR merged first; the Chief of Staff merges its PR by rebase once it is ready,
its PR checks green and its branch heavy run green on the exact head.
