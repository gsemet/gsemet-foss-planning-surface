# Stack state (2026-10-27)

Base `main`. Stack #139 (gh stack). Bottom to top:

| CR | PR | Branch | Static | Visual |
| --- | --- | --- | --- | --- |
| 125 | [#132](https://github.com/gsemet/markdown-okf-schema-studio/pull/132) | `change-requests/125-unclosed-fence-swallows-document` | red (requirements indexes) | see PR |
| 126 | [#133](https://github.com/gsemet/markdown-okf-schema-studio/pull/133) | `change-requests/126-edit-button-greyed-untrusted` | red (same) | see PR |
| 127 | [#134](https://github.com/gsemet/markdown-okf-schema-studio/pull/134) | `change-requests/127-paste-raw-no-fence` | red (same) | see PR |
| 128 | [#135](https://github.com/gsemet/markdown-okf-schema-studio/pull/135) | `change-requests/128-table-handle-drop-zone` | red (same) | see PR |
| 129 | [#136](https://github.com/gsemet/markdown-okf-schema-studio/pull/136) | `change-requests/129-keyboard-nav-after-window-switch` | red (same) | see PR |
| 130 | [#137](https://github.com/gsemet/markdown-okf-schema-studio/pull/137) | `change-requests/130-block-actions-follow-keyboard-selection` | red (same) | see PR |
| 131 | [#138](https://github.com/gsemet/markdown-okf-schema-studio/pull/138) | `change-requests/131-code-block-reading-comfort` | red (same) | see PR |

Heavy CI on the top branch: [run 40499257994](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40499257994).

## Done

- Rebased in order onto origin/main; conflicts only in `CHANGELOG.md`, `requirements/tiers/log.md`
  (kept both entries) and `test/site/e2eGroups.test.ts` (131: scenario count 387 = 382 + 5).
- `just check` in each worktree: green except `requirements-lint` (installed okfreq lacks `--check-links`).
- Screenshots pushed to `change-requests/<NNN>-<slug>-assets` (125, 126, 128, 129, 130, 131); PR-BODY.md
  placeholders replaced; missing template sections (Changes, Impacts, Blast radius, Test plan) added to 126, 127, 128, 131.

## Resume run (2026-10-27, after PR #128 / CR 123 merged)

- `git fetch --prune`; whole stack 125 -> 131 rebased onto origin/main a7bf21b2 (manual `git rebase --onto`
  per branch; conflicts kept both sides: `test/site/e2eGroups.test.ts` counts 384 (125) and 389 (131),
  `requirements/tiers/log.md` (129), `test/integration/trusted-suite.ts` (130)). Force-pushed with lease.
- `just requirements-update` (authorized) run per CR with STUDIO_OKFREQ=okf-schema/.venv/bin/okfreq. That newer
  okfreq reorders `implemented_in_files`/`tested_in_files` in ~268 requirement files (noise; CI's okfreq 0.13.0
  `update-coverage --check` would then disagree), so only the generated `index.md` changes were amended into the
  commits (125: myst/index.md, 126: trust-security/index.md, 129: block-editing/index.md, 131: code-blocks/index.md).
- Local `just check`: green up to `requirements-lint`; its last step `update-coverage --check` fails locally only
  because of that newer okfreq's ordering (not reproducible with CI's 0.13.0, local .venv is broken).
- CI after first push: 125 static pass; 126+ static fail on `update-coverage --check` "1 files would change".
  Suspect: 126's hand-edited TRUST-001 description wrap; re-wrapped as the generator does, amended into 126, 127-131
  restacked and pushed. Confirmed for 126; 129, 130 and 131 needed the same normalisation (description wrap and
  sorted `implemented_in_files`/`tested_in_files` of the requirement files they edit; 131 also `derived_by` of
  StRS-MDOKFSTUDIO-CODE-001), amended into their commits.
- Result: normal CI (static + visual) green on all 7 PRs (#132-#138). Heavy CI on top branch 131:
  [run 40507920933](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40507920933):
  integration success, visual success, static success, stress (advisory) still running at hand-off.
  The earlier CR 130 integration failure no longer occurs (test-only fix 86beaff6 in the rebased commit).
- The "Red items" and "Heavy CI result" sections below are historical (pre-resume).

## Red items

- **All 7 PRs, job `static`, step `requirements-lint`**: CI's okfreq (locked okf-schema 0.13.0) supports
  `--check-links`; `validate` passes (0 errors) but `okfreq lint requirements --check` says
  "N indexes would change" (125: 1, 126-128: 2, 129-130: 3, 131: 4). The generated requirements indexes
  are stale in each CR: `just requirements-update` with a current okfreq must be run and its output
  amended into each CR's commit, bottom to top. This includes 126's hand-edited TRUST-001
  `implemented_in_files` (not separately checked by CI; the index drift is the failure).
- Not done by the stack driver: **permission denied** when running `just requirements-update` with
  `STUDIO_OKFREQ` pointing to `../okf-schema/.venv/bin/okfreq` (auto-mode classifier, "Modify Shared Resources").
  Not worked around. Read-only `requirements-lint` with that binary reproduces CI exactly ("1 indexes would change" on 125).
- Because every CR is red for the same cause, no CR was moved to the top.

## Heavy CI result ([run 40499257994](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40499257994), top branch 131)

- visual: success. static: failure (same requirements-lint index drift). stress (advisory): still running at hand-off.
- **integration: failure, CR 130** (`test/integration/blockActionsFollowSelection.test.ts`, trusted suite):
  after the pointer moved last, expected a hovered action bar but got `{"selectedBar":0,"hoveredBar":0,"ring":false}`
  in cream and dark (after-keys state was correct). The mouse half of the fix (actions follow the pointer) does not
  hold in the real window on CI. Needs a new coder round on CR 130; then it should move to the top of the stack.
  Not moved by the stack driver (restack + CI rerun is deferred to that round).
- PR-level visual: success on all 7 PRs; static red on all 7 (index drift only).
