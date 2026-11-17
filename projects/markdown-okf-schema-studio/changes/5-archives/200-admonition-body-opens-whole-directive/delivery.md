# 200 — Admonition body click opens the whole directive (merged early)

- Owner decision 2026-10-29: option A. Also records the BLOCK-047 decision (whole-window blur
  commits and closes the editor, by design) in the requirement rationale; no code change for it.
- PR: https://github.com/gsemet/markdown-okf-schema-studio/pull/222 (stacked on #221), merged 2026-10-29T06:46Z by the user, head a17b394f.
- Delivered: `editingElementFor` (`src/page/features/mappedBlocks.ts`) opens the nearest
  admonition (`aside.admonition`, `details.admonition`) on a body click, as for GitHub alerts;
  context-tag panels (`myst-context-admonition`, MYST-013) keep paragraph-level editing.
  BLOCK-014 updated and its Known issue line removed; unit tests in
  `test/session/alertBlockEditOpen.test.ts`; new visual fixture
  `test/visual/fixtures/72-myst-admonition-editing.md`.
- Review: Inspector rounds 1 and 2 in `reviews/` (round-1 findings fixed in round 2).
- **Not done at merge time:** the heavy CI run and the headless real-click visual proof had not
  completed when the PR merged. The Driver was stopped after the merge; no further push.
  Runs started on the merged head: normal https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40830547091, heavy
  https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40830553206 (both completed after the merge).

## Post-merge results (2026-10-29)

- Normal CI https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40830547091 on
  a17b394f: success.
- Heavy https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40830553206 on a17b394f:
  success (static, visual, integration, stress, report, checks).
- Main https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40831352287 on 9b53edbe:
  success; no version change, so no tag.
- The headless real-click visual proof was never run as a dedicated step; the heavy visual job passed
  (not checked whether it covers the new fixture 72).
