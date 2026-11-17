# Change Specification: `ci-report` names each failed visual check

Triage: automatable (short specification, not reviewed by the owner). Priority P1. Code read at
`origin/main` `cb968299` (`chore: version 1.7.1`); the local `main` is behind, so cut the branch from
`origin/main`.

## Goal

When the visual stage fails, the `report` job of CI prints `FAILED visual: [object Object]; [object
Object]` (seen in run 40804420093, attempt 2, 2026-10-29), so the log does not say which page or
check failed. After this change the line names each failure: `FAILED visual: <page>: <detail>; ...`.

## Cause

`scripts/e2e-campaign.mjs`, `stageFrom`: the `error` of a failed stage is
`manifest.failures.join("; ")`. The visual manifest (`out/reports/e2e/screenshots/run-manifest.json`,
written by `test/visual/capture.py`) holds `Failure(page, detail)` objects, serialized as
`{ "page": ..., "detail": ... }`. `join` stringifies them as `[object Object]`. The check name and
message are already inside `detail` (`<check_name>: <error>`), so `page` and `detail` are all that
needs printing.

## What changes

Redo the three edits of the closed eval PR 321 on a fresh branch from `origin/main` (decision 1). Do
not reopen or rebase the eval branch.

1. `scripts/e2e-campaign.mjs`
   - Add a helper above `stageFrom`, marked `// @implements_req SwRS-MDOKFSTUDIO-CORE-076`:
     ```js
     function failureText(failure) {
       if (typeof failure === "string") return failure;
       if (failure && typeof failure === "object" && "page" in failure) return `${failure.page}: ${failure.detail}`;
       return JSON.stringify(failure);
     }
     ```
   - In `stageFrom`, replace `manifest.failures.join("; ")` with
     `manifest.failures.map(failureText).join("; ")`. `manifest.error` keeps its priority over
     `failures`, and the `<name> manifest status is <status>` fallback is unchanged.
   - Format (decision 2): one failure is `<page>: <detail>`; failures are joined with `; `; a string
     failure prints as it is; any other value prints as `JSON.stringify`.
   - JUnit (decision 3): no change. `writeJUnit` (imported from `scripts/run-e2e.mjs`) writes
     `stage.error`, which now carries the new text.

2. `test/site/e2eCampaign.test.ts`: add one test after "the visual-only report fails when the
   visual stage failed or did not run", marked `// @tests_req SwRS-MDOKFSTUDIO-CORE-076`, named
   "the report names each failed check of a visual manifest". It uses the file's helpers
   (`workspace`, `writeCampaign`, `run`, `hoursAgo`):
   - write a visual campaign, a passed `review.json`, and a visual manifest
     `{ status: "failed", failures: [{ page: "home", detail: "blank" }, { page: "toc", detail: "overflow" }] }`;
   - `run(root, "report", "--visual-only")` exits 1, its stdout matches
     `FAILED visual: home: blank; toc: overflow` and does not match `[object Object]`;
   - rewrite the manifest with `failures: ["first", "second"]`: stdout matches
     `FAILED visual: first; second`.

3. `requirements/tiers/swrs/rendering-core/SwRS-MDOKFSTUDIO-CORE-076.md` (decision 4): in the table
   of "Scenario (boundary): Artifact names and attempts", add this row before the row "the visual and
   integration stages started two hours apart or more":

   `| a failed visual manifest lists `{page, detail}` failures | `report` prints each as `<page>: <detail>`, joined with `; `, never `[object Object]`; string failures print as they are; `error` of the manifest keeps its priority |`

4. `requirements/tiers/log.md`: a dated entry (`## 2026-11-12` or the day of the change) saying that
   SwRS-MDOKFSTUDIO-CORE-076 gains a boundary row on the failure text of the `report` stage, with
   `scripts/e2e-campaign.mjs` (`failureText`) and `test/site/e2eCampaign.test.ts` as its code and
   test. Then run `just requirements-update` and commit the regenerated files.

5. Changelog and commit (decision 5): no user-facing change, so no `CHANGELOG.md` line; if the
   batch's changelog rule (CR changelog-line-in-each-pr) asks the PR for a line, write "No
   user-facing change". Commit type `ci:` with no scope (for example
   `ci: name each failed visual check in the e2e report`); `fix(ci)` is forbidden by
   `.agents/guidelines/git-commit-allowed-scopes.md`.

## Decisions carried from `02-answers.md` and the advisor (section 9, adopted)

1. Reuse PR 321: redo its three edits on a fresh branch from `origin/main`.
2. Format: `<page>: <detail>`, joined with `; `; strings unchanged; anything else `JSON.stringify`.
3. JUnit: nothing more, it reads `stage.error`.
4. Requirement: the PR 321 boundary row in CORE-076.
5. Changelog: none ("No user-facing change"); commit type `ci:`.

No USER-IMPACT question for this CR (owner, 2026-11-12).

## Out of scope

- `test/visual/capture.py` and the manifest format (unchanged).
- The integration stage, the console layout of the report, and `scripts/run-e2e.mjs`.
- Any new SwRS, any change to the CI workflow files.
- PR 321 and its eval branch (left as they are).

## Evidence

- The new test in `test/site/e2eCampaign.test.ts` fails on `origin/main` (stdout carries
  `[object Object]`) and passes after the change.
- `just check` (unit tests, formatting, unused exports, file size) passes.
- `just requirements-lint` passes; `just requirements-update` leaves no diff after the commit.
- `just preflight` passes (completion gate).

## Stack position

Second in the batch stack, after changelog-line-in-each-pr. It shares `requirements/tiers/log.md`
and the generated `rendering-core` index with publish-to-open-vsx, which the owner has excluded for
now, so the only expected conflicts are on `log.md` and the generated indexes.

## Open questions

None.

Note for the Chief of Staff: the advisor allowed `fix(ci)` as a commit type; the commit scopes
guideline forbids it, so this specification uses `ci:`.
