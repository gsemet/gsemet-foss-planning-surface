# SC20 evidence: the quiz

Command shape: `just quiz <role> --cards <staging> [--case <id>] --plan` (staging: the role's folder with `driver.md`, `floor.md`, `topics/`, `topics.json`; the staging step holds until child 24 makes `--cards` read `cards-next/` itself). The spend plan was printed first, for each run.

| run | plan (estimate) | result |
| --- | --- | --- |
| cr-driver, all 18 cases | about $19.35 | over the $10 cap: not run, unproved |
| cr-driver, one case (floor-1-cr-driver-merge, floor-2-cr-driver-push, floor-5-cr-driver-dirty-rebase, floor-9-cr-driver-refused-send) | about $1.07 each, about $4.3 for the four | refused: see below, unproved |
| stack-driver, floor-2-stack-driver-restack | about $1.08 | refused, unproved |
| release-driver, 3 cases | about $3.22 | refused, unproved |
| qa-driver | no case exists under `evals/quiz/qa-driver/` | no case |

The real run is refused on this machine: `quiz.py: claude: not found on this machine` (`work/coder3/quiz-cr-floor1.out`). No workaround was used (no other host, no estimate). So every row is "unproved", and the real run is not done (child 28). No baseline file `evals/results/quiz-*-baseline-old-cards-*.json` exists, so there is nothing to compare with either.
