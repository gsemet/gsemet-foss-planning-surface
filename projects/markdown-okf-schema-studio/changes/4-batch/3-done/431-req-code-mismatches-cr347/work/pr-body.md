## Summary

Five software requirements described behaviour the code does not have; each carried a "Known
issue" line saying so. This PR settles each one: for one of them the code was wrong and is fixed,
for the other four the requirement was wrong and now states the current, intended behaviour. No
requirement keeps that known issue.

The one visible change: when a render fails without a message, the preview now shows "The render
failed." (first render) or "The latest render failed." (a later render, the old page kept as
stale), instead of the text "undefined" or an empty message.

## Deliverables

| Requirement | Verdict | What the reader now gets |
| --- | --- | --- |
| SwRS-MDOKFSTUDIO-CORE-010 (wikilinks) | requirement fixed | "Raw HTML" means an HTML block or a tag itself; a `[[wikilink]]` written between two inline tags (`<span>[[Note]]</span>`) is converted like any text, as CommonMark treats Markdown there and as bare URLs already behave. |
| SwRS-MDOKFSTUDIO-CORE-025 (failed render message) | code fixed | A failure with no message shows the fallback text again; the fallback strings had become unreachable because the render pipeline turned every thrown value into an error message such as "undefined". |
| SwRS-MDOKFSTUDIO-DIAG-005 (Mermaid theme colours) | requirement narrowed | The drawn-picture claim covers what the picture check reads (node fill, background); the border, secondary and tertiary colours are checked as the values given to Mermaid. The sample diagram draws no part that uses the secondary or tertiary colours. |
| SwRS-MDOKFSTUDIO-DIAG-009 (late Mermaid results) | requirement fixed | Mermaid drawing passes run one at a time, so a later theme is drawn only after the running pass ends; the "result for a replaced key is dropped" rule holds for PlantUML and charts. The two Mermaid guards stay as defence, with a comment. |
| SwRS-MDOKFSTUDIO-TRUST-042 (SVG links) | requirement fixed | An SVG link (`xlink:href`) in raw HTML is treated like an HTML link: a blocked address is removed and only the navigation request remains; an allowed one keeps its address; in both cases a click is routed through the host's link check. |

```ts
// src/session/features/rendering.ts
export function failureMessage(error: unknown, fallback: string): string {
  // the error's own message when it has one, else the fallback text
  ...
}
```

## Changes

- Render failure message: the render pipeline gives a failure with no message (`undefined`,
  `null`, an `Error` with an empty message) an empty message instead of the text "undefined"; a
  thrown string keeps its text. The first-render and later-render failure paths use the fallback
  when the message is empty, through one shared helper.
- Requirements: CORE-010, CORE-025, DIAG-005, DIAG-009 and TRUST-042 reworded where the
  requirement was wrong, each "Known issue" line on these points removed (the other known issues
  of DIAG-005 and DIAG-009 stay); a dated entry in `requirements/tiers/log.md`; generated
  coverage files regenerated.
- Comments only, no behaviour change: the two Mermaid late-result guards
  (`src/page/modules/mermaidPreview.ts`) and the `xlink:href` branch of the HTML sanitizer
  (`src/core/security/html-sanitizer.ts`).
- Tests: the comments that called these behaviours known issues now say what the tests check.

Sources and tests per requirement:

- CORE-010: `src/core/render/mystInlineTransforms.ts`;
  `test/core/render/renderReq.coreRows.requirements.test.ts`.
- CORE-025: `src/core/render/renderPipeline.ts`, `src/session/features/rendering.ts`,
  `src/session/previewManager.ts`; `test/host/coreReq.requirements.test.ts`.
- DIAG-005: `src/page/modules/mermaidPreview.ts`;
  `test/page/modules/diagReq.pageDiagrams.requirements.test.ts`,
  `test/visual/capture_final_checks.py`.
- DIAG-009: `src/page/modules/mermaidPreview.ts`;
  `test/page/modules/mermaidPreviewEntry.test.ts`,
  `test/page/modules/diagReq.pageDiagrams.requirements.test.ts`.
- TRUST-042: `src/core/security/html-sanitizer.ts`;
  `test/security/trustReq.pageBuild.requirements.test.ts`.

## Impacts

No visual change in normal use. The only change a user can see is the text of the error page when
a render fails without a message ("The render failed." / "The latest render failed." instead of
"undefined"); no screenshot, as this state is reached only by a failing render.

## Blast radius

Grade: 1. The code change is limited to the message of a failed render; a plain `git revert`
restores the previous text. The other changes are requirement text and comments.

## Autonomous decisions

- SVG links in raw HTML stay routed through the host like HTML links (TRUST-042): nothing in the
  docs, tests or history asked for them to be left out, and routing every clickable link through
  the same host check is the safer behaviour. The opposite choice (treat `xlink:href` apart, so
  SVG links get no navigation request) is a small sanitizer change, if wanted.
- Wikilinks between inline HTML tags are converted (CORE-010), matching CommonMark and the bare
  URL transform; keeping them literal would need tag pairing in the inline transform.
- The DIAG-005 picture check is not extended to the border colour; the requirement is narrowed
  instead.

## Known gaps

- SwRS-MDOKFSTUDIO-GFM-003 uses the same "raw HTML" wording for bare URLs as CORE-010 did; it has
  the same behaviour and no known issue, and is left unchanged here.
- **UNVERIFIED:** the four new failure-fallback tests failing on the previous code. One local run
  of the new tests against the old source showed 4 failed, 3 passed; an independent re-run on a
  checkout of the base could not be made (the checkout failed on Windows with "Filename too long").
  The tests pass at the head.

## Test plan

- [x] New or changed tests: four new host tests for the failure fallback (`undefined`, `null`, an
      empty-message `Error` on the first render, and a later render failing without a message), and
      one that a thrown string keeps its text; all pass at 61893a8 (carried from the same patch at
      the earlier head, a clean rebase onto #437). **UNVERIFIED:** that the four
      fail on the previous code (4 failed, 3 passed) rests on one local run of the new test file
      against the old source; it was not reproduced independently (see Known gaps)
- [x] Requirements: SwRS updated, markers in code and tests, `just requirements-update`
- [x] Changelog: one user-facing line under `## Unreleased` in `CHANGELOG.md`
- [x] Local gates: `just check` (exit 0), `just requirements-lint` (92 StRS, 578 SwRS citations
      valid), `okfreq validate --check-links` (pass), `just requirements-update` (0 indexes to
      update); `just preflight` pass at 61893a8 (on Windows, its static stage; carried from the same
      patch, a clean rebase onto #437)
- [x] Review: approved at 61893a8; verified at 61893a8 (carried from the same patch, a clean
      rebase onto #437)
- [x] CI green at 61893a8: checks, static, static-windows, visual and report on the PR; the real
      VS Code jobs (integration, stress) green in the manual heavy run 44738309448 at 61893a8

## Internal references

- Settles the code/requirement mismatches listed as known issues in #418.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
