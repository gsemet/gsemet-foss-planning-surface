## Summary

The requirements of code blocks, GitHub Flavored Markdown and MyST were hard to review: one
approved use case (StRS) grouped callouts, layout blocks, figures and inline text, some use cases
promised more than the code does, some behaviours (SwRS) repeated a shared rule or held several
behaviours, and several `@implements_req` and `@tests_req` markers sat away from the code or the
test they name. This PR gardens those three groups so a reviewer can read each use case and follow
it down to the code and to a test. It changes no product behaviour.

## Deliverables

Each use case of the three groups now reads as one story with a use-case diagram, and is traced
down to the code and to a validation test on a real scenario.

| | Before | After |
| --- | --- | --- |
| Use cases | MyST blocks in one use case; radio choices inside the checkbox use case | MYST-001 split into four use cases; radio choices in their own use case; a use-case diagram each |
| Shared rules | derived by several use cases | cited with `depends_on` |
| Behaviours | merged behaviours and internal steps as scenarios | merges superseded (never deleted), internal steps as verification notes |
| Markers | some on generic helpers or unrelated tests | on the code that does the behaviour and the test that checks it |

Requirements added:

- `StRS-MDOKFSTUDIO-GFM-005` (choose an option of a plan with one click), with
  `SwRS-MDOKFSTUDIO-GFM-040` (a radio choice list renders as a radio group) and
  `SwRS-MDOKFSTUDIO-GFM-041` (choosing an option moves the `(x)`).
- `StRS-MDOKFSTUDIO-MYST-015` (admonitions and context tags), `MYST-016` (grids, cards, tabs),
  `MYST-017` (figures and tables), `MYST-018` (definition lists and roles).
- `SwRS-MDOKFSTUDIO-MYST-102` (dollar amounts and prices stay text).

Requirements superseded (old into new):

- SwRS CODE-005 into CODE-001 and CODE-039; CODE-026 into CODE-019; GFM-027 into GFM-021; GFM-039
  into GFM-040 and GFM-041; MYST-051 into MYST-045; MYST-101 into MYST-096.
- StRS MYST-001 into StRS MYST-015, MYST-016, MYST-017 and MYST-018.

Approved requirements changed (the maintainer agreed in advance to the corrections the change
specification planned; please review them):

- `StRS-MDOKFSTUDIO-GFM-002`: its rationale now lists the colours the code keeps (named, hex,
  rgb/rgba, hsl/hsla), with a new approval date; commit: 22c97db8.
- `StRS-MDOKFSTUDIO-MYST-001`: superseded by the four use cases above; commit: 436226d9.

New tests: code block box and font (CODE-007), a second copy click (CODE-019), a footnote with no
definition (GFM-008), host refusals of a checkbox toggle (GFM-021), a heading reference text
(MYST-019), a missing KaTeX bundle (MYST-024), grid nesting depth (MYST-053), and a new visual
capture of a page with display maths, dollar prices and an invalid formula (MYST-006).

## Impacts

No visual change: the `src/` changes are marker comments, and the new visual scenario adds a
capture without changing an existing one.

## Human decisions

- Published requirements are never deleted: merges and splits supersede them.
- The corrections the change specification planned to approved use cases (GFM-002, MYST-001) were
  agreed in advance, one commit each, for review on this PR.
- A use-case diagram added to an approved use case needs no re-approval.
- Shared rules are cited with `depends_on`, never derived, Main paths included.
- The open placement questions follow the change specification's recommendations.

## Blast radius

Grade: 1

Requirement text, markers and tests only; the `src/` changes are marker comment lines. A plain
`git revert` restores the previous bundle.

## Autonomous decisions

- MYST-097 (fences and front matter read the same way everywhere) now derives from StRS CORE-001.
- The alert-body click scenario of GFM-009 is held by BLOCK-014, which already specified it.
- The "offer the table palette action" scenario stays in MYST-063: no palette behaviour fits it.
- MYST-031 cites the allowed-roots rule TRUST-025 with `depends_on`.
- The `previewShowProblems` tests are traced to MYST-081 (the banner and its message), not MYST-078
  (the Problems publication).
- GFM-029 (inline HTML subset) is left to the rendering-core gardening; TRUST-006 is superseded, so
  the code-copy behaviours cite TRUST-005.
- The GFM-016 marker stays on the sanitizer's `rewriteNode`: the sanitizer has no branch of its own
  for checkbox inputs.

Questions for the maintainer:

- MYST-019 says a `{numref}` to a captionless figure shows its number, while the code keeps a
  numref as an inert placeholder. Should the scenario or the code change? No test was added for it.
- StRS CODE-001's intent still says "in the language and colours of their editor", while its
  rationale now says Dark+ or Light+ whatever the theme. Should the intent change too?

## Known gaps

- The MYST-019 `{numref}` scenario contradicts the code and has no test.
- CODE-007's exact-fit and long-line geometry is checked by the CSS rule and the visual suite only.
- The gallery job did not run: the workflow skips it on this branch even when asked (it runs
  through its own dispatch), so the gallery pages were not rebuilt for this change.
- The local long gate ran on Windows, static stage only; the visual, integration and Linux checks
  are covered by CI alone.
- The verification notes of GFM-021 and GFM-041 say the no-editor path makes "one or two edits",
  while `test/host-vscode/documents.test.ts` checks less than that; the wording was not narrowed.
- StRS CODE-001's intent still says "colours of their editor"; it waits for the maintainer's answer
  above.

<details><summary>Details</summary>

## Changes

- `requirements/tiers/strs/` and `requirements/tiers/swrs/`: the use cases and behaviours above,
  reparented, split, superseded and reworded; a use-case diagram per use case; generated links
  updated; a dated entry in `requirements/tiers/log.md`.
- `src/`: marker comments moved onto the code they name.
- `test/`: markers fixed and added, the new tests above, the new visual module
  `test/visual/mathScenarios.ts` and fixture `test/visual/fixtures/89-maths-offline.md`.
- `scripts/marker-baseline.json`: entries of files that are now clean removed; `scripts/unused-exports-allowlist.json`:
  `clearMathCache` is now used by a test.

## Test plan

- [x] New or changed tests: the tests listed above, run by `just check` at e5b4b27e (carried over a clean rebase). They check
      behaviour the code already has, so they pass on the previous code too.
- [x] Requirements: SwRS updated or added, markers in code and tests, `just requirements-update`;
      `just requirements-lint` (okfreq validate and lint with links, coverage up to date) passes
      at e5b4b27e (carried over a clean rebase)
- [x] Changelog: no user-facing change
- [x] Local gates: `just preflight` at e5b4b27e (carried over a clean rebase: same patches), the static stage on Windows (`just check`: unit
      4070 tests, 0 failed; security 101 tests, 0 failed; build tests 175 passed;
      Sphinx contract 4 passed; `just audit`, `just sphinx-check`, `just requirements-report`)
- [x] Review: approved at e5b4b27e (carried over a clean rebase: same patches)
- [x] CI green at e5b4b27e: pull request checks (static, static-windows, visual, report, checks)
      and the real VS Code run (`heavy=true`): static (Linux and Windows), visual, integration,
      stress, report and checks pass; the gallery job was skipped by the workflow
- [x] Verified at e5b4b27e (carried over a clean rebase: same patches): requirement checks, markers, supersessions, new tests and this
      description judged against the diff

## Internal references

- Change request: CR-348, batch batch-06 (planning surface), from the requirements gardening
  audit of code blocks, GFM and MyST.
- New visual scenario: `myst/v47-maths-offline-light-900`; the lock texts of the dollar-price
  scenarios v35 and v36 now say the prices stay text, as they render.

</details>

Assisted-by: Claude:Opus-5.5
