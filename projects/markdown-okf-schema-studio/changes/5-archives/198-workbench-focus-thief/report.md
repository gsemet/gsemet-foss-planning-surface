# 198 — Workbench focus dump on real-window failures (merged)

- PR: https://github.com/gsemet/markdown-okf-schema-studio/pull/220 (replaces #218, rebuilt on main after stack 217 without force push), merged
  2026-10-29T06:47Z.
- Delivered: real-window integration failures dump the workbench focus (active group, editors,
  focused element); the test profile is quieter.
- CI: normal CI green on head 2428cf7a; heavy proof via the stacked #221 run
  https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40828891957 (all green, stress about 21 min).
