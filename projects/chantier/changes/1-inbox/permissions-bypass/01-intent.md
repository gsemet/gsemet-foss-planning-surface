# Allow rules cover gate and lease hold, which run any command

From the Fable audit (2026-11-21, high): P10's recommended allow rules let any agent with Bash run any command through `chantier gate` (shell) and `lease hold`, and `--from *` accepts any package. Intent: close that bypass without adding prompts to a night batch.
