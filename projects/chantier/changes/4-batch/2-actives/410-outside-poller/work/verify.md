# Verify CR-410

Head: 2d07ac0c8658e50b07ece25b5b430b59eb75684a

All claims judged at 2d07ac0c8658e50b07ece25b5b430b59eb75684a, CLI run from the worktree (`uv run --no-sync --project <worktree> chantier`) in a scratch planning folder (work/scratch/p, git init, removed at the end).

1. `interests --kind issue --json` lists the CRs' `issue:` lines, `--kind pr` unchanged. Scratch: two CRs (1-inbox/a, 2-backlog/P2/b) naming one Jira link, one archived CR naming a GitHub link.
   - issue: `{"errors": [], "interests": [{"by": "1-inbox/a", ... "read_by": "outside", "ref": ".../PAY-12", "tracker": "jira"}, {"by": "2-backlog/P2/b", ...}], "project": "p", "schema": 1}` exit 0 (archived CR absent).
   - pr: `{"errors": [], "interests": [], ...}` exit 0. Text form: `interests of p: 2` + one `issue <link> (jira): events for <by>` line each.
2. `journal add issue@1`: stdin payload wrote `journal: seq 1 issue@1 commented on <ref> (1-inbox/a, 2-backlog/P2/b)` exit 0; same payload again `journal: already there (seq 1)` exit 0. Refused, exit and text per spec: unawaited ref (2), archived CR's ref (2), `merged@1` (2), extra key `cr` (1, `cr: Extra inputs are not permitted`), not JSON (1), `wakes: "yes"` (1). Journal afterwards holds exactly one line: `{"v":2,"seq":1,...,"source":"poller","audience":["project"],...,"wakes":false,"folders":["1-inbox/a","2-backlog/P2/b"]}`.
3. `wakes: false` rides along (watcher), 4. hub never collects issues, 5. wake rule/example/duplicate: `python -m pytest test_outside_poller.py test_watch_events.py test_forge_hub.py test_event_types.py test_event_audience.py test_scenario_coverage.py -q` -> `131 passed in 44.89s`.
6. Texts present at head: grep shows the AGENTS.md outside-poller clauses (lines 81, 84, 98), chief-of-staff.md `tracker saw` (lines 1347, 1383, 1390), concepts.md Interest, README, docs/hosts.md; diff stat lists docs/forge-connectors.md, planning-folder.md, web-board.md, scenario/README.md, CONTRIBUTING.md.
7. PR description (work/pr-body.md): renders, Summary/Deliverables/Changes match the diff; Known gaps names the unmeasured test budget and the missing gate/verification; no role names. Review box `approved at 2d07ac0` matches the Driver's note "move 69c30dc..2d07ac0 (rebase) inspector approved at 2d07ac0c...".

Not proved by me: the scenario case `outside_poller` and `just scenario` at this head (no gate pass at 2d07ac0; a scenario-surface-board log exists from the earlier head only), and the 2 s test budget (named in Known gaps).

VERIFIED
