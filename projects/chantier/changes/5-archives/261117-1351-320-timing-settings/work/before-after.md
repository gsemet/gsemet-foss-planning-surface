# Before and after

Before: 9bb941f374df58ab4b5412125f14d61ee452debc (the PR base, CR-319's branch). After: 17b1c6b16d65785004aac790ccfbbef89f938893.

| Pair | Before | After | Reproduce |
| --- | --- | --- | --- |
| Timing tab at 1680 px beside the reference | no Timing tab and no timing key: `git grep -c "steering_wake\|timing_lines" 9bb941f -- skills config` prints nothing (no match) | `evidence/timing-tab-1680.png` (scratch demo board, made-up paths, no username), beside `evidence/final-config-1680.png` (board-visual-refresh's `final-config.html`, same width) | `scripts/docs_screenshots.py`'s helpers on a demo copy with a `chantier.yaml` setting `session: steering_wake: 20m, cache_ttl: 1h` and `copilot gpt ci_reruns: 2`; Playwright at 1680 px, click Timing |

Not captured: a CLI before run on a base checkout (the base worktree was not synced for `uv run --no-sync`); the base has no timing code, shown by the git grep above.
The look: both images opened; the Timing tab shows two host cards, "not used" cells (Subagent steering wake, Session CI re-runs), teal dotted set values (20 min, 60 min, 2), grey defaults, the legend on the tabs' line. No username or home folder shows. The reference's illustrative values differ and its Driver wake row is not drawn, as the specification says.
