# Answers

test-ceiling-Q1 (2026-11-21, the user): **Measure on an idle machine first.** ("Mesurer au repos d'abord".) A CR measures `just test` on an idle machine (main's head, the slowest tests named), and the user then decides between raising AGENTS.md's ceiling and moving or cutting the real-git tests; the ceiling stays as it is until then.
test-ceiling-Q2 (2026-11-21, Fable advisor): **The PR's diff: no PR, a study of the Chief of Staff.** The measure changes nothing in the repository and its numbers feed one decision written into AGENTS.md itself; inside a batch a CR with no PR cannot hand back ready, so the measure runs as a Chief of Staff study subagent whose result is a file in the CR's `experiments/`.
test-ceiling-Q3 (2026-11-21, Fable advisor): **Idle threshold: at most 10 % average load over 30 s before each run, wait up to 30 minutes, then stop with no numbers.** Loaded numbers already exist (CR-417's); runs labelled "not idle" would be a look-alike of the measure asked for; the study then returns the load samples and the process list naming what loads the machine.
test-ceiling-Q4 (2026-11-21, Fable advisor): **When it measures: after batch-30 closes, outside any batch.** Batch-30 has no reliable "every other CR handed back" moment, and it still merges about 20 CRs that add tests, so numbers taken before its close would be stale.
Destination (2026-11-21, Fable advisor): does not join batch-30. Right after batch-30's close and the main checkout's fast-forward, with no batch running, the Chief of Staff starts one study subagent that measures and writes the report in the CR's `experiments/`; the Chief of Staff then puts the ceiling decision to the user as test-ceiling-Q5, and that answer makes the real change, which this CR then carries into a batch.
test-ceiling-idle-processes (2026-11-21, the Chief of Staff): **The surface server's and the watchers' own uv and Python processes do not count in the idle check; the report names them.** Any `git`, `just` or `pytest` process they start counts, so the study waits and checks again.
test-ceiling-clean-check (2026-11-21, the Chief of Staff): **The clean check is on tracked files only.** `git status --porcelain --untracked-files=no` prints nothing, before the first run and after the last; the main checkout's untracked files (`.agents/`, stray root files) stay as they are, and the study never removes or moves an untracked file.
test-ceiling-study-runs (2026-11-21, the Chief of Staff): **Accepted: all five idle runs carry `--durations=30` and a junit file, the figures come from the median run; runs done before a 30-minute stop stay in the report, marked not counted.**

Spec final (2026-11-21, the Chief of Staff): v2 with the study decisions; destination 2-backlog/P2, not batch-30: the Chief of Staff starts the study right after batch-30's close and main's fast-forward, then asks the user test-ceiling-Q5.

# Decision (2026-11-25, the owner, in chat)

"tu vas te concentrer sur livrer les CR 507 a 514 sur le rework. tu vas annuler les specs de tous les autres mais eviement pas perdre les reponses que j avais donnee en interview. Avec le rework en cours il faudra refaire la specification de tout, et on fera ca dans un batch 32."

The specification is cancelled: it is kept for reference in `work/spec-before-rework.md`, and is to be written again after the rework, from these answers, for batch-32.

Destination: none for now; to specify again for batch-32. Replaces the earlier destination.

# Decision (2026-11-25, the owner, in chat): to 3-ready

Asked (Chief of Staff): "Je passe en ready les 10 CR à respécifier, pour batch-32 ?" Answer: "Oui, les 10".

Not automatable: the request is not its specification. The Chief of Staff told the owner that the specification stays to be written before the launch: write it from these answers before any batch takes this CR.

Destination: next batch (3-ready), batch-32. Replaces the earlier destination.
