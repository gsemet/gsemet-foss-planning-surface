# Verify: CR-349 (second Verifier, description pass)

Head: abeb761a9ea8815888f2bb59d3e114ef83979598

PR #426 (draft), base `chantier/batch-06/cr-348-change-specification-garden-the-requirem` at
`e5b4b27`. `gh pr view 426 --json headRefOid` gives `abeb761a9ea8815888f2bb59d3e114ef83979598`,
the worktree's `git rev-parse HEAD`.

## Claims

1. **Clean rebase, patch unchanged (52c0488 -> abeb761).** At abeb761.
   `git show 52c0488 | git patch-id --stable` and `git show abeb761 | git patch-id --stable` both
   give `ba861ea1c9aa879010ebeca70b25448a3162cc5e`. `$CHANTIER log CR-349` has the `carry` event
   `head=abeb761… base=e5b4b27… gate_from=52c0488…`. Pass.

2. **`just check` passes (spec Evidence 1).** At abeb761, re-run by me on Windows:
   `just check > work/verifier/check-abeb761.log 2>&1` exit 0. Its tail includes
   `0 requirement OKF projections would change`, `0 files would change` (requirements-lint, part of
   `just check`) and `main paths: 92 StRS checked, 578 SwRS citations, all valid`. No new export
   (the diff adds only module-local `const`, `interface` and `function`). Pass.

3. **`just preflight` passes (spec Evidence 2).** Carried from 52c0488: clean rebase, patch-id
   equal (claim 1). Gate log `work/gates/20261120-003012.log`, first line
   `gate CR-349 branch chantier/batch-06/cr-349-name-the-stuck-tooltip-when-the-capture- head 52c04880204fb117da2f2045e80c11d9fc8abf4b`,
   last lines `ci-static: passed`, `preflight: visual, integration, report and gallery stages
   skipped on Windows; CI runs them`, `result: pass at 52c0488…`. Its requirements-lint shows
   nothing moved (same output as claim 2). Pass (static stage only on Windows; real-window tests
   did not run locally).

4. **Heavy CI at the head (spec Evidence 3).** At abeb761.
   `gh run view 44639811161 -R gsemet/markdown-okf-schema-studio --json headSha,status,conclusion,jobs`:
   `headSha abeb761a9ea8815888f2bb59d3e114ef83979598`, `completed`, `success`; jobs
   static-windows, visual, static, integration, stress, report, checks: success; toc-loop,
   release-check, gallery, pages, tag-release, release: skipped. `gh pr checks 426`: checks, report,
   static, static-windows, visual pass; integration, stress and others skipping on the PR run.
   The unchanged condition lets every capture through within 10 s. Pass.

5. **Spec points 1-4, by reading the diff** (`git diff e5b4b27..HEAD`, one file,
   `test/integration/realInput/harness.ts`, +74/-7, 806 lines). At abeb761.
   - Point 1, one probe: module-level `shownToolbarTooltips()` lists
     `[data-sphinx-preview-toolbar] button[data-tooltip]` whose `::after` is not hidden by
     `content === "none" || content === "normal" || visibility === "hidden" || Number(opacity) === 0`,
     the negation of the old `.every(...)` predicate token for token, so the condition is unchanged.
     It returns `data-tooltip`, `:hover`, `:focus-visible`, `content`, `visibility`, `opacity`. The
     wait is `` `(${shownToolbarTooltips.toString()})().length === 0` `` and the report is
     `frame.evaluate(shownToolbarTooltips)`: one definition. Pass.
   - Point 2: `const TOOLTIP_HIDE_TIMEOUT_MS = 10_000;` passed as `{ timeout: TOOLTIP_HIDE_TIMEOUT_MS }`.
     No `setDefaultTimeout` under `test/` (`grep -rn setDefaultTimeout test` prints nothing), so
     the old wait had Playwright's 30 s default. Pass.
   - Point 3: non-`Error` or `name !== "TimeoutError"` rethrown unchanged; second probe throwing
     rethrows the original `error`; empty second probe throws
     `capture ${id}: toolbar tooltips hid only after the ${TOOLTIP_HIDE_TIMEOUT_MS} ms wait timed out`;
     otherwise `capture ${id}: toolbar tooltip still shown after ${TOOLTIP_HIDE_TIMEOUT_MS} ms: `
     + `"<tooltip>" (hover: yes|no, focus-visible: yes|no, ::after content "<…>", visibility <v>, opacity <o>)`
     joined by `; `; both with `{ cause: error }`. Matches the settled form (content is
     JSON-quoted, so a computed `"Bold"` shows as `"\"Bold\""`; the Inspector noted it; the spec's
     `"..."` placeholder allows it). Pass.
   - Not matching `detachedFrameError`: `node -e` probe building both messages with every toolbar
     tooltip text from `src/core/preview/previewToolbar.ts` and the capture id
     `review-annotations/r03-incoming-change-bars`, tested with
     `/frame.*detach|execution context was destroyed|cannot find context with specified id/iu`
     on `String(error)` (as `harness.ts` lines 62, 143, 248 do): output `false false false`
     (both messages unmatched; no newline). No capture id in `test/shared/captureRegistry.ts`
     contains `detach` (grep of `detach` outside `test/integration` lists no registry file). Pass.
   - Point 4: the doc comment of `capture` gains "It then waits up to 10 s for the toolbar tooltips
     to hide and, if one stays shown, fails with the button's tooltip text and its hover and focus
     state." Pass.
   - The timeout path did not run (cannot be forced; spec Evidence 4); judged by reading only.

6. **Commit.** At abeb761: one commit on the base, `test: name the stuck toolbar tooltip when a
   capture's wait times out` (`git log --oneline -3`). Pass.

7. **Review box** `Review: approved at abeb761 (carried from 52c0488)`. `$CHANTIER log CR-349`:
   `r1 approved at 2a6f4f1…, committed as 52c04880204fb117da2f2045e80c11d9fc8abf4b`, then the
   `carry` to abeb761. Pass.

Claims 1-7: carried from abeb761: same head, no move (`gh pr view 426 --json headRefOid` and
`git rev-parse HEAD` both give `abeb761a9ea8815888f2bb59d3e114ef83979598`). Claim 4 rechecked:
`gh run view 44639811161 --json headSha,status,conclusion` gives
`abeb761a9ea8815888f2bb59d3e114ef83979598 completed success`.

8. **PR description as posted (second Verifier).** At abeb761. Pass.
   `diff <(gh pr view 426 -R gsemet/markdown-okf-schema-studio --json body --jq .body | tr -d '') <(tr -d '' < work/pr-body.md)`
   prints only `106d105 <` (one trailing empty line in the posted body), exit 1: the posted body is
   `work/pr-body.md`, word for word. Its Test plan now has `- [x] CI green at abeb761: ... heavy
   dispatch run 44639811161 passes its integration and stress jobs ...`, which spec Evidence 3
   requires and claim 4 proves. Every other sentence was judged against the diff, spec and CI in
   the first pass (same text, same head): Summary, Deliverables, Changes match the one-file diff;
   Known gaps names the unforced timeout path; gates line (claims 2-3); Review box (claim 7); no
   images; no internal reference outside Internal references; sections and code fences render
   (standard GitHub Markdown, no fold).

## Evidence

`work/verifier/evidence/before-after.md`: no pair; no visual change, timeout path not forceable.

## Verdict

VERIFIED at abeb761a9ea8815888f2bb59d3e114ef83979598: the code meets spec points 1-4 and every
evidence point; the posted PR description now names the heavy CI run 44639811161 (claim 8).

## Description pass 3 (third Verifier, description only)

Head: abeb761a9ea8815888f2bb59d3e114ef83979598

9. **PR description as posted, after the edit (Changes line, Test plan boxes, attribution line).** At abeb761. Pass.
   `gh pr view 426 -R gsemet/markdown-okf-schema-studio --json body -q .body` against `work/pr-body.md`
   (CR stripped): differs only by one trailing empty line in the posted body.
   - Changes "Not changed" names `test/integration/checkboxToggle.test.ts` and
     `test/integration/previewEditingHelpers.ts` (used by `previewEditing.test.ts`): `grep` shows both
     hold the inline tooltip wait (`checkboxToggle.test.ts:82`, `previewEditingHelpers.ts:122`) and
     `previewEditing.test.ts:29` imports `./previewEditingHelpers`. `git diff --stat e5b4b27..abeb761`:
     only `test/integration/realInput/harness.ts` (74+, 7-); `src/` and CHANGELOG unchanged.
   - Summary, Deliverables and the table match the diff (constant 10_000, probe, helper, messages,
     TimeoutError-only catch, second-probe fallback, doc comment).
   - Test plan: Requirements and Changelog boxes carry their "no behaviour change / no user-facing
     change" reason; Verified box matches work/verify.md claims 1-8; CI box: `gh pr checks 426` shows
     checks, report, static, static-windows, visual pass (rest skipping);
     `gh run view 44639811161 --json headSha,conclusion` gives the abeb761 SHA and `success`.
   - No internal reference outside Internal references (`PR #402` is a public PR); the Claude Code line
     follows Internal references as the guideline asks; template sections all present; Known gap is the
     expected one; no images.

VERIFIED at abeb761a9ea8815888f2bb59d3e114ef83979598 (description pass).
