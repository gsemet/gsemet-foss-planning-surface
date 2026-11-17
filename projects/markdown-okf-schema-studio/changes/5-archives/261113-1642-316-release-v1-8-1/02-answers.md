# Answers

## 2026-11-13: filed with the batch

Owner, 2026-11-13: « on peut faire un 1.8.1 fake si tu veux » (proof of the OIDC publish before the
next feature release), then « Oui, lance » on the plan: batch-03 as a stack in direct mode,
`marketplace-trusted-publishing` then this release CR. Release notes say the release changes only
how the extension is published. Still to settle at the confirmation: hero image, announcement
thread, grant.

## 2026-11-13: second Marketplace policy

Owner, 2026-11-13: « Oui, remplis-la » (a second Trusted Publishing policy for `ci.yml`, the
workflow that calls `release.yml`). At the check of record, note which policy shows a "Last used"
date: it settles which workflow the Marketplace matches.

## 2026-11-13: CR-315 merged; version consistency

Owner, 2026-11-13: « Mergé » (PR 387, merged 15:09:59Z as b1907e9f), then « il faudra faire une
release donc, verifie bien que la version soit coherente ». Checked on origin/main by the Chief of
Staff: every versioned file of `scripts/version.py` says 1.8.0 (`package.json`, `package-lock.json`
root and `packages[""]`, `plugin.json`, `.claude-plugin/plugin.json`,
`.github/plugin/marketplace.json`); the only tag is v1.8.0; the Marketplace serves 1.8.0. Since
v1.8.0: b1907e9f (ci) and fd8adb9e (docs), so 1.8.1, set explicitly (`just version 1.8.1`): the
commitizen guess may not bump on ci and docs commits alone. `## Unreleased` of CHANGELOG.md is
empty (CI commits get no line).

## 2026-11-13: confirmation

Owner, 2026-11-13: « Oui, confirme », on the Chief of Staff's recommendations: version 1.8.1 set
explicitly; very short release notes (the extension does not change, only how it is published, with
no stored token; no mention of Open VSX); CHANGELOG per the guideline (the 1.8.1 section empty, or
one maintenance line if the procedure requires one); no hero image (patch); no announcement thread
(nothing to tell users; an exception to the guideline's three posts, noted here); default grant;
check of record: the Marketplace serves 1.8.1, the publish step ran with `--oidc`, and which of the
two policies shows "Last used".

## 2026-11-13: merge of the version PR

Owner, 2026-11-13: « tu as mon autorisation de merger ce ticket automatiquement » (version PR 388).
The steering session merges PR 388 by rebase once it is mergeable and its heavy run is green on the
exact head, without asking again. GitHub's auto-merge stays untouched (agents never set it).

## 2026-11-13: which policy matched

Checked by the Chief of Staff on the publisher's Trusted Publishing page after the 1.8.1 publish:
"Release workflow" (`release.yml`) shows "Last used 6 minutes ago"; "CI workflow (calls
release.yml)" (`ci.yml`) shows "Never". The Marketplace matches the called workflow
(`job_workflow_ref`), not the caller: the `ci.yml` policy is unused and can be deleted, and
`VSCE_PAT` can be deleted (first `--oidc` publish succeeded).
