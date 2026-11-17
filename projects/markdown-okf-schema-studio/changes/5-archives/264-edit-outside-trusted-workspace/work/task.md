# Task 264

Worktree: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-264. Branch: change-requests/264-edit-outside-trusted-workspace. One PR from `main`. Decisions: `00-request.md`.

## Change

Today `preview.readOnly` means two things: writes are refused, and reads are narrowed. Separate them.

1. Replace it with what each use means, for example a "restricted reads" flag (no workspace folder, or
   Restricted Mode) that drives everything about reads: `resource-policy.ts`, `plantUmlIncludes.ts`,
   `renderPipeline.ts`, `links.ts`, schema resolution in `frontmatter.ts`. Those reads do not change.
2. Every write path stops refusing on trust: the dispatcher's five edit requests, `hostRequests.ts`,
   `comments.ts`, `blockEdits.ts`, `rendering.ts`, the boot context, `page/runtime.ts`,
   `page/features/checkboxes.ts`, the Edit button in `previewToolbar.ts`. Go through every use of
   `readOnly` in `src/`, `baselineDiff.ts` included, and decide it by the two meanings.
3. Remove the reasons that no longer apply (`readOnlyReasons.ts`); keep `READ_ONLY_FILE`.
4. A feature that needs trust stays disabled with its reason. List every such feature in the report.
5. `package.json` `capabilities.untrustedWorkspaces.description`, the README and any user doc that say
   Restricted Mode is read-only.

## Requirements

Update TRUST-001, 002, 005 and 006 (SwRS) and StRS TRUST-001, and every other requirement that states a
read-only preview. Their ids stay when the contract is refined; use the lifecycle operations when one
is replaced. Markers move with the code. `just requirements-update`, an entry in `tiers/log.md`.
Requirements guideline first. The owner agreed to change the approved StRS BLOCK-025, REVIEW-003, REVIEW-015 and TABLE-001 (see
`00-request.md`): set `approved_by` and the approval date as the requirements guideline says, list them in
the PR body under "Approved requirements changed", and request the owner's review. Any other `approved`
requirement: stop and report it.

## Tests first

Failing tests before the change: edit, frontmatter, checkbox, image paste and comment in Restricted Mode
and on a standalone file; includes, non-image resources and dot-directories still refused in both.
Existing tests that assert read-only change intent here by the owner's decision: list each one with why.
Unit and contract tests, and the e2e scenarios of Restricted Mode.

## Gates

`just check`, `just e2e` for the groups touched as far as the machine allows. The PR needs a heavy
run on the branch: `gh workflow run ci.yml --ref change-requests/264-edit-outside-trusted-workspace -f heavy=true` (real Restricted Mode windows run
there only). Before and after screenshots of the Edit button in Restricted Mode, in the PR.
