# `just scenario` under 5 minutes

Filed 2026-11-14 by the Chief of Staff, on the user's word: "Objectif: just scenario < 5 minutes".

## Why

CR-228's long gate (2026-11-14) took 1,197.9 s on GitHub (895 checks) and 1,195.5 s on GitLab
(873 checks), run one after the other: about 40 minutes per gate, and a CR that needs two rounds
pays it twice. On 2026-11-04 the scenario had 106 checks per forge and took about 1 min 47 s per
forge: the cost per check barely moved (about 1 s then, 1.3 s now); the scenario grew about 8.5
times in ten days, every CR adding its cases. `scenario/run_scenario.py` builds one temporary
repository, plays a main batch, then about 44 case functions one after the other on that same
repository, and the GitLab pass replays all of it although only `forge_stack_cli` and a few
shipping paths depend on the forge.

## Decided with the user (2026-11-14)

1. The normal cases: one world and one whole batch per configuration (parallel, series, stack,
   direct, release, external planning surface), run in parallel.
2. The dynamic cases: a few representative CRs added during a batch (order add, a dependency, a
   release added, a QA, a dropped CR, a restarted Foreman, a lost Driver), grouped by
   configuration instead of a dozen case functions that each reopen batches.
3. GitLab runs only the forge-specific cases, not the whole scenario a second time.
4. The scenario is split into independent units run in parallel, each its own temporary world,
   so the wall time is about the longest unit.
5. No backward compatibility: chantier is still a proof of concept. The legacy readers (old
   `batch.json` words, the old tree, the batch-record backfill and the like) and their scenario
   cases go. Before they go, this project's own records (`.agents/changes/`, its `5-archives`
   and `5-archives/batches`) and the planning surface `gsemet-foss-planning-surface` are migrated
   once to the current format by a script run once and not kept in the CLI; then the CLI is
   checked to read everything (`status`, the board, the cost of old batches); then the readers
   are removed.
6. The pure refusals that need only a prepared state and one CLI call (the `chantier.yaml`
   validation, the rails' refusals, the close refusals, the cost and STATUS reading, the CR
   summaries) move to pytest in `tests/`, calling the CLI in-process, parametrized so the tests
   stay few and fast. Refusals that exist only in the middle of a real run stay in the scenario.
   `AGENTS.md` says so: "tests check the structure and the CLI's refusals on a prepared state;
   the batch workflow belongs to `just scenario`".
7. The cases with real waits (gate stop, gates in parallel, gate proof, cancel during a gate,
   Driver liveness) stay, run in parallel.

Done when `just scenario` passes in under 5 minutes on the user's Windows machine, both forges,
and on Linux CI.

An analysis by a read-only subagent (what to prune safely, the split, the risks of running in
parallel) is in progress; its report feeds the specification.
