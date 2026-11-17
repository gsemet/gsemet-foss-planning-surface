# Stress flake: the review-threads comment popover's Resolve button does not appear

Type: fix (test or product) · Priority: P1 · Filed 2026-10-28 by the Foreman from the 1.0.0 heavy
gate · No CR now (user decision via the Chief of Staff): the post-CR-168 heavy gate on main
decides; if `review-threads` fails again, the user chooses between a fix before 1.0.0 and a release
with a known flake.

## Evidence

- Failing run: heavy on main `b71fac7c`,
  https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40732349085, `stress` job,
  round 9 of 20, scenario `review-threads`:
  `locator.textContent: Timeout 30000ms exceeded` waiting for
  `[data-okf-comment-popover] [data-okf-comment-resolve]`
  (`out/test/integration/realInput/run.js:93`, `runStress`). Rounds 1–8 of the scenario passed.
  Log: `stress-b71fac7c.log` (this folder).
- Earlier heavy runs, `stress` green:
  - https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40728621051 (`2577039e`)
  - https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40723757734 (`620c640a`, Edit figure fix)
  - https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40716533723 (`ff9f9c1e`, five-row toolbar)
  - https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40700884217 (`59f0c329`)
- Suspect range `2577039e..b71fac7c`: PR #175 (toolbar and tooltip motion, incl. the shared
  tooltip slide-in) and PR #178 (table menu: clear the toolbar before revealing). Lead (unproven):
  a motion transition delays the popover or its Resolve button becoming visible.

## Expected

- Reproduce in the stress job (CI only; no local real-window runs), find the cause, fix product or
  test wait per `.agents/guidelines/ci.guidelines.md` rule 12 (record host/page state on failure;
  never a blind retry or a longer timeout alone), and prove it with a green stress run.
