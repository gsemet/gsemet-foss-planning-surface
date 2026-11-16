# The eval campaigns, redesigned

The user (2026-11-11): "il faut un eval real en direct et un en foreman. donc renomme ce real en
real-foreman et un real-direct ou ce sera une autre session propre a declancher, tu me donnes
par exemple le prompt ou tu lance la commande claude equivalent", then "on peut revoir ensemble
pour la prochaine campagne ce que tu me conseilles pour redesign les eval. laisse copillot dans
son coin pour l instant", then "on redesign les evals et on merge tout pour avoir un design
propre".

## Today (`evals/README.md`)

- `real`: this repository, the real forge and CI, draft PRs nobody merges, Foreman mode only;
  last run 2026-11-05 (v0.5.0). No fixed scorecard; `evals/kit/audit.py` does not apply.
- `claude-smoke` and `claude-full`: the fictional `tasks-cli` project, planted failures; last run
  2026-11-04, before `verdict`, the two-gate `handback ready`, multi-command `gate`, the worker
  write guard, the force-push route and direct mode.
- `copilot`: never run; left as it is.
- Batch-10 (a `real` run) stopped on the worker write guard bug.

## The Chief of Staff's proposal, to grill

- Three campaigns: `real-foreman` (today's `real`), `real-direct` (the same, steered by the Chief
  of Staff in its own new session), and `claude-planted` (`claude-smoke` and `claude-full`
  merged: what a real run cannot produce, a red CI, the round limit, a question, a release).
- The same scorecard in every report: each rail seen and right, seen and wrong, or not seen; the
  cost and the steering share.
- An audit for the real campaigns, reading `log` and `cost --by cr` before `close`.
- Real campaigns take real small items from the inbox, not invented defects.
- How to start `real-direct`: a prompt for a new desktop session on this repository.
