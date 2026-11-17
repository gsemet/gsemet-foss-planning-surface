# 051 — perf-zero-reloads

From backlog `P3/deep-analysis-review` (copied here: 04–07 findings, 08-remediation-plan.md),
"Increment 3 — Zero reloads per keystroke". Parts are already done on main (incremental updates
setting, include budget, PlantUML JS engine, bounded state): verify each finding against current
code first and skip what is already fixed (say so in the PR).

## Decisions (user grill, 2026-10-23)

1. Measure first: add a reproducible probe (script or test harness, committed) that reports, on a
   large fixture (e.g. a long chapter with Mermaid, tables, frontmatter): number of
   `webview.html` assignments while typing ten characters, number of full page reloads, scroll
   frame script time, and whether an open inline editor survives save / theme change / diagram
   completion. Record the baseline on current main.
2. Then implement increment 3 except PERF-10: status updates by `postMessage` (PERF-05 step 1);
   runtime script and CSS as bundled cacheable files instead of inlined (PERF-11); content and
   properties table by `postMessage` with keyed DOM morph (PERF-05 step 2); no reload during edits,
   range tracking and explicit stale-edit errors (STAB-03, STAB-06); Mermaid loaded once and cached,
   geometry-free scroll frames, throttled state (PERF-07, PERF-08). NOT in scope: dropping
   `retainContextWhenHidden` (PERF-10) and STAB-05.
3. Exit criteria (plan): typing ten characters performs zero `webview.html` assignments after the
   first render; an open inline editor survives save, theme change and diagram completion; a
   scroll frame on the large fixture stays under 4 ms of script time. The PR shows before/after
   numbers from the probe.
4. CSP stays strict (nonce scripts, no `unsafe-inline`); no behaviour change visible to users other
   than speed and kept editor state; existing visual screenshots unchanged.
5. Split allowed: if it is too big for one PR, the driver ships it as stacked PRs (guideline
   "Stacked PRs"), probe + PERF-05 step 1 + PERF-11 first.
6. Branch `changes-requests/051-perf-zero-reloads`, assets `changes-requests/051-perf-zero-reloads-assets`.
7. Speed: Opus everywhere, reviewer on the round diff, ready when `checks` is green; also one manual
   heavy run (real VS Code) since it touches the preview lifecycle. Rounds: 3. PR for an external reader.
