# Retro — 288-export-single-html

| What happened | Root cause | Process fix |
| --- | --- | --- |
| Round 1 red: visual `rendering-core/v16-inline-code-narrow-full-dark-460` and `myst/v32-conf-warning-banner-narrow-dark-460` (run 43063467860) | The Export button widened toolbar row 1 from 102 to 134 px; the banner reserve in `pageChromeStyles.ts` and a fixture line were sized for the old width, and the spec did not list chrome-width consumers | Fixed in rounds 2 and 3; add to `task.md` template: when a change alters a floating chrome's size, grep for every value derived from its width |
| Round 2 still red in CI only on v16 (run 43073231025) | The fixture line fitted locally with about 13 px to spare, and CI fonts are wider | Round 3 left an 87 px margin; rule candidate: a fit-on-one-line fixture must be measured with a margin, not an exact fit |
| Integration failures at two heads: `Timed out waiting for Heading 2 to prefix the line`, then a 20-minute hang in the reload campaign, then a `checkbox-toggle` timeout | CI flakes in real VS Code runs, not from this CR (the watchdog did not fire on the hang) | Filed as backlog items (reload-campaign-watchdog-misses-hang, integration-checkbox-toggle-render-timeout) |
| A GitHub rerun of a heavy run failed with "workflow file issue" and a heavy run ended in `startup_failure` | Workflow dispatch on a force-pushed head right after a push | None: a fresh `workflow_dispatch` worked |
| The stack driver wrote a stale head into `STATUS.md` (4ba858d6 after the restack to ffca17bf) | Two writers on one header after the restack | Foreman reset the header via `hdr.sh`; rule: one writer per header (already in the lifecycle) |
| Whole stack went BEHIND `origin/main` when #357 landed; owner asked for one rebase of all PRs | A docs-only merge on main during a long stack run | None: the Rebase rule worked as intended |
