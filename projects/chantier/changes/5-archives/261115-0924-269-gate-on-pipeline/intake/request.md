# A project's rule may name a pipeline job as its long gate

Filed 2026-11-15 by the Chief of Staff from batch-18's retro (kept by the retro critic, reshaped by a Fable review), on the user's word "lance le tout dans le batch actuel".

Problem: `just scenario` takes 9.5 min on the user's quiet Windows machine (573 s), 11 min loaded, against the 5 min target of CR-254; about 30 long gates ran one at a time and paced batch-18's night. The forge's pipeline runs the same scenario job in 1m43 on ubuntu. The local gate also missed `just eval-dry-run`, which CI runs (cost CR-253 a round), and unit budgets went red on a loaded PC.

Fix, generic (cards, no CLI change): one line in concepts.md, driver.md and foreman.md: a project's rule may name a pipeline job as its long gate; the Driver then hands back `--no-gate "<the rule>"` once that job is green at the PR's head, and the steering session reads that job's state on the forge (`gh pr checks` on GitHub, `glab ci status` on GitLab). Mark the GitLab and Copilot paths "unproved" until the user's trial.

Fix, this project (AGENTS.md): the long gate is the pipeline's scenario job, green at the PR's head. Windows coverage, which found the real defects (the gate race, os error 32), is kept by default by one local `just scenario` per batch on the stack's top before the user merges; a Windows leg in CI is the alternative, the spec says which and why.

Gap: a project with no CI, or a runner on the same slow machine, gains nothing.

Order in the batch: second (it removes most of the waiting).
