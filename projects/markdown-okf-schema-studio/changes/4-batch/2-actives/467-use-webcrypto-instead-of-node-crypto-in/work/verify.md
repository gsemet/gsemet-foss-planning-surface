# Verify CR-467

Head: faba0c4b4d5016f5d7e4323ed8be46485d20a68a

All claims judged at faba0c4b (pushed head), in the CR worktree, after `npm run compile` (tsc, clean).

1. No node:crypto import in csp.ts / commentStore.ts. `grep -n crypto src/core/security/csp.ts src/core/comments/commentStore.ts` gives only `globalThis.crypto.getRandomValues` (csp.ts:3, commentStore.ts:42). `grep -rn "node:crypto\|from 'crypto'" src/core` gives only a comment line in sha256.ts:4. PROVED.
2. Out of NODE_DEBT: `grep -c "csp.ts\|commentStore.ts" .dependency-cruiser.cjs` = 0 (NODE_DEBT lists no crypto entry). `npm run check:boundaries` (the justfile target): "no dependency violations found (445 modules, 1234 dependencies cruised)", "check-boundaries: passed (385 modules)". PROVED.
3. sha256 test: `node --test out/test/core/comments/sha256.test.js`: "the synchronous sha256 equals node:crypto on empty, ASCII, multibyte, long and block-boundary inputs" pass 1 fail 0. `node --test "out/test/core/comments/*.test.js" out/test/host-vscode/fileRename.test.js`: tests 76, pass 76, fail 0. `node --test out/test/security/trustReq.requirements.test.js`: 16 pass incl. "each nonce is 18 random bytes as 24 base64url characters, fresh for every page"; 1 fail, "a read-only preview reads includes from the folder of its document", RenderError "Cannot find module .../node_modules/markdown-it/lib/common/utils.js imported from markdown-it-dollarmath": a dependency resolution failure in the render pipeline, not in crypto code, outside the CR's diff (6 files); not attributed to the CR (not re-run on base). PROVED for the crypto-touching tests.
4. Format probe: createNonce() twice gave `E6Pcii6h0egTGeUFEluWXaoc`, `4O0zjT1waxDq-9MCdrp3qLEe`: both match /^[A-Za-z0-9_-]{24}$/ and differ. newId gave `t_6f0aa98f`, `c_007db5bb`, `t_ea89ba35`: all match /^[tc]_[0-9a-f]{8}$/. PROVED.

Not run by me: `just check` / preflight (PR body's Local gates box), CI, Review box. The PR body text matches the diff (`git diff --stat origin/main...HEAD`: .dependency-cruiser.cjs, SwRS REVIEW-054, commentStore.ts, sha256.ts, csp.ts, sha256.test.ts); the description as posted on the forge was not fetched.

VERIFIED

## Description pass at faba0c4b4d5016f5d7e4323ed8be46485d20a68a

Fetched with gh pr view 481 --json body,title; checked against git diff origin/main...HEAD --stat. Sections, order, fold, SHAs on Test plan, Changes vs diff, CI (gh pr view statusCheckRollup: static, static-windows, visual, viewer-graph success) and Review note (driver note approved at 116f39d, committed as faba0c4) all hold. FAILED: Deliverables says "None" for a refactor that adds a module (sha256.ts) and changes the NODE_DEBT boundaries; pr-template allows None only for a one-line fix and requires a visual or targets (for instance a before/after of the NODE_DEBT table or imports) for a structural change.

NOT VERIFIED

## Description pass 2 at faba0c4b4d5016f5d7e4323ed8be46485d20a68a

Fetched with `gh pr view 481 --json body,title`; checked against pr-template and `git diff origin/main...HEAD`. The previous Deliverables failure is fixed (before/after table of the targets set, no screenshot, matches the diff: csp.ts, commentStore.ts, sha256.ts, NODE_DEBT entries removed). Sections order, fold, Test plan SHAs, Changes vs diff hold.
FAILED: the CR's specification `01-intent.md` has `issue: https://github.com/gsemet/markdown-okf-schema-studio/issues/413` (grep "issue:" output), so the body needs a `## Issues References` section (after Summary) with one line for the ticket (`Closes #413`, or the project's form). It is missing, and the Summary names the ticket ("Part of #413"), which the template allows only in Issues References.

NOT VERIFIED

## Description pass 3 at faba0c4b4d5016f5d7e4323ed8be46485d20a68a

Fetched with `gh pr view 481 --json body,title`; checked against pr-template, `.agents/guidelines/pull-request.guidelines.md` and `git diff origin/main...HEAD --stat` (6 files). The pass 2 failure is fixed: `## Issues References` is present after Summary with `Part of #413`; the Summary no longer names the ticket. `Part of` instead of `Fixes` is a decision, listed under Autonomous decisions; the guideline asks for `Fixes #N` only when the change closes the issue, so it does not forbid it. Section order, fold with blank lines, no text after `</details>`, Deliverables table matching the diff, Known gaps "None" (no UNVERIFIED claim, no accepted failure), Review box (`approved at 116f39d`, committed as faba0c4, matches the driver notes in `chantier log`), no role name or `.agents/changes/` path outside Internal references, no images: all hold.
Note, not a failure: the project's `.github/PULL_REQUEST_TEMPLATE.md` has a Changelog test-plan item that the body leaves out; the chantier template does not carry it and the change has no user-facing line.

VERIFIED
