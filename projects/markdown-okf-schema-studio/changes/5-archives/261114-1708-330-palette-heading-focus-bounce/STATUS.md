# CR-330 Change Specification: find why a click on a palette list option is lost and closes the block editor

✅ merged · batch-04 · [PR](https://github.com/gsemet/markdown-okf-schema-studio/pull/403)

**Now:** Merged: https://github.com/gsemet/markdown-okf-schema-studio/pull/403.
**Next:** Nothing.

## Progress

- [x] Shipped: https://github.com/gsemet/markdown-okf-schema-studio/pull/403
- [x] Handed back
- [x] Merged: https://github.com/gsemet/markdown-okf-schema-studio/pull/403

## Documents

- [request](intake/request.md)
- [intent](01-intent.md)
- [answers](02-answers.md)
- [specification](03-change-spec.md)
- [.agents/guidelines/ci.guidelines.md](../../../guidelines/ci.guidelines.md)
- [.agents/guidelines/git-commit-allowed-scopes.md](../../../guidelines/git-commit-allowed-scopes.md)

## Where

- Branch: `chantier/batch-04/cr-330-change-specification-find-why-a-click-on`
- Worktree: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio.worktrees/batch-04-CR-330`
- Driver: `-`

## Decisions and open questions

- Owner, 2026-11-14, on the conditional question: « option a si c'est le cas ». If the proof reaches a product cause (H2), the fix is option a: a focus loss that returns straight to the same webview does not commit or close the block editor; SwRS-MDOKFSTUDIO-BLOCK-047 changes accordingly (approved by the owner for this CR), with a log entry. A real leave (focus to another editor, panel or app, no return) still commits. If the cause is CI only (H3), no product change and BLOCK-047 stays as is. No further ask on this point.
- Owner, verbatim: « option a si c'est le cas ». On a proven product cause (H2) the fix is option a: a focus loss that returns straight to the same webview keeps the block editor open; SwRS-MDOKFSTUDIO-BLOCK-047 changes accordingly (approved for this CR); a real leave still commits. On H3 (CI only): no product change.

## Cost

$2.02.
