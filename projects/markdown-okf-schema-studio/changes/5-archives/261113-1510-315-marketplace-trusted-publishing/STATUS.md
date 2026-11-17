# CR-315 Change Specification: publish to the VS Code Marketplace with trusted publishing

✅ merged · batch-03 · [PR](https://github.com/gsemet/markdown-okf-schema-studio/pull/387)

**Now:** Merged: https://github.com/gsemet/markdown-okf-schema-studio/pull/387.
**Next:** Nothing.

## Progress

- [x] Round 1: Implement the change specification 03-change-spec.md sections 1-6 fully; edits only, no commit; run the evidence checks 1-4
- [x] Round 2: Fix CONTRIBUTING.md: restore the sentence 'Manual pushes of valid vX.Y.Z tags also run this workflow.' at the end of its original paragraph; OIDC paragraph separate and last; rewrap step 6
- [x] Note: Round 2 approved; committed; running just preflight
- [x] Long gate fail: 1a881c48
- [x] Note: preflight run 1: ci-static passed; visual and real-window integration failed (Shottr took window focus; visual 'text not found'), report/gallery follow; re-running once as infrastructure
- [x] Long gate fail: 1a881c48
- [x] Blocked: infra: just preflight at 1a881c48 fails only in ci-integration (real-input step times out: real VS Code window; Shottr, the user's running app, is frontmost) twice; ci-static passed both runs, ci-visual flaked once then passed; change is CI/docs only. Committed locally, not pushed, no PR. Needs the owner to quit Shottr or allow a push for CI; log work/gates/20261113-152216.log
- [x] Shipped: https://github.com/gsemet/markdown-okf-schema-studio/pull/387
- [x] Note: PR 387 opened as draft; heavy run 43445113627 dispatched on the branch head 1a881c4; waiting for integration and stress
- [x] Handed back
- [x] Merged: https://github.com/gsemet/markdown-okf-schema-studio/pull/387

## Documents

- [request](intake/request.md)
- [intent](01-intent.md)
- [answers](02-answers.md)
- [specification](03-change-spec.md)
- [pr-body](work/pr-body.md)
- [long gate log](work/gates/20261113-152216.log)
- [.agents/guidelines/release-process.guidelines.md](../../../guidelines/release-process.guidelines.md)
- [CHANGELOG.md](../../../../CHANGELOG.md)
- [CONTRIBUTING.md](../../../../CONTRIBUTING.md)

## Where

- Branch: `chantier/batch-03/cr-315-change-specification-publish-to-the-vs-c`
- Worktree: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio.worktrees/batch-03-CR-315`
- Driver: `-`

## Decisions and open questions

- Round 2 approved; committed; running just preflight
- preflight run 1: ci-static passed; visual and real-window integration failed (Shottr took window focus; visual 'text not found'), report/gallery follow; re-running once as infrastructure
- back to a Driver: resume: the owner accepts the branch heavy CI run as the gate instead of the local real-window integration (Shottr frontmost). Rebase, push, open the draft PR, dispatch the heavy run on the branch, wait for integration and stress green on the exact head, then the verifier. Record the local failure in the PR body.
- PR 387 opened as draft; heavy run 43445113627 dispatched on the branch head 1a881c4; waiting for integration and stress

## Cost

$1.51.
