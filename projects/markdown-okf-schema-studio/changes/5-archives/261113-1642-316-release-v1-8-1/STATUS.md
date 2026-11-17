# CR-316 Change Specification: release v1.8.1

✅ merged · batch-03 · [PR](https://github.com/gsemet/markdown-okf-schema-studio/pull/388)

**Now:** Merged: https://github.com/gsemet/markdown-okf-schema-studio/pull/388.
**Next:** Nothing.

## Progress

- [x] Note: draft: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio.worktrees/batch-03-CR-316/docs/releases-notes/2026-11-13-v1.8.1/release-notes.md
- [x] Note: Attempt 1: stack already on main (b1907e9f); heavy run 43450028473 of main HEAD in progress; run 43416264245 of fd8adb9e had integration and stress red (to read); notes drafted.
- [x] Note: Heavy run 43450028473 green on main HEAD b1907e9f (integration success, stress success); version commit next.
- [x] Long gate fail: 46cef13e
- [x] Note: Gate 1 failed on the environment (tsc not found: the main checkout has no node_modules to symlink); just dev in the worktree, gate re-run.
- [x] Long gate fail: 46cef13e
- [x] Shipped: https://github.com/gsemet/markdown-okf-schema-studio/pull/388
- [x] Note: Version commit 08e3c0f8 (notes token sentences fixed per steering); preflight: static and visual passed, local real-window integration lost window focus; branch heavy run 43456982844 dispatched; PR 388 opened as draft until green.
- [x] Note: PR 388 green: PR CI pass; branch heavy run 43456982844 green at 08e3c0f8 (integration, stress success); marked ready; main still b1907e9f. Owner's merge approval O-3 noted; the steering session merges by rebase.
- [x] Blocked: merge: https://github.com/gsemet/markdown-okf-schema-studio/pull/388
- [x] Handed back

## Documents

- [request](intake/request.md)
- [intent](01-intent.md)
- [answers](02-answers.md)
- [specification](03-change-spec.md)
- [01-body-sections](work/01-body-sections.md)
- [02-pr-body](work/02-pr-body.md)
- [long gate log](work/gates/20261113-163528.log)
- [.agents/guidelines/release-process.guidelines.md](../../../guidelines/release-process.guidelines.md)
- [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## Where

- Branch: `chantier/batch-03/cr-316-change-specification-release-v1-8-1`
- Worktree: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio.worktrees/batch-03-CR-316`
- Driver: `abef22cc2491f88c0`

## Decisions and open questions

- confirmed: 1.8.1, set explicitly; short notes (publishing only, no stored token, no Open VSX); no hero image; no tweet.md (owner's exception); default grant; check of record: Marketplace 1.8.1, --oidc publish, which policy shows Last used
- Attempt 1: stack already on main (b1907e9f); heavy run 43450028473 of main HEAD in progress; run 43416264245 of fd8adb9e had integration and stress red (to read); notes drafted.
- Heavy run 43450028473 green on main HEAD b1907e9f (integration success, stress success); version commit next.
- Gate 1 failed on the environment (tsc not found: the main checkout has no node_modules to symlink); just dev in the worktree, gate re-run.
- Version commit 08e3c0f8 (notes token sentences fixed per steering); preflight: static and visual passed, local real-window integration lost window focus; branch heavy run 43456982844 dispatched; PR 388 opened as draft until green.
- approved: merge 388
- PR 388 green: PR CI pass; branch heavy run 43456982844 green at 08e3c0f8 (integration, stress success); marked ready; main still b1907e9f. Owner's merge approval O-3 noted; the steering session merges by rebase.
- back to a Driver: merged: PR 388 merged by the steering session by rebase at 2026-11-13T16:14:00Z, origin/main 0253426a (chore: version 1.8.1). Go on after the merge: the version push run on main makes the tag; then release published, the check of record (publish step with --oidc, gallery vspackage 1.8.1 HTTP 200, which Marketplace policy shows Last used), Pages, 04-report.md, retro.md. Stop the caffeinate you started when done.
- published: 1.8.1 https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v1.8.1

## Cost

$5.20.
