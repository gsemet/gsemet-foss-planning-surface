# Answers

1. **Priority and place** (2026-11-14). The user: "Oui, P1 à la fin de la stack": P1, grilled and specified, then added at the end of batch-17's stack.
2. **The target** (2026-11-14). Back to the start-up time before CR-221, within about 10 %, keeping the PEP 723 dependencies and the pydantic records (chosen over "as fast as possible").
3. **The guard** (2026-11-14). A structure test that checks a simple command imports none of the heavy libraries at start (deterministic, not tied to the machine's speed), chosen over a time threshold in `just check`.
4. **Grilled enough** (2026-11-14). The user, after the full restatement: yes, to the specification.
5. **What the target means for commands that read a record** (2026-11-14). After the open question was re-explained, the user: "Oui il faut faire des imports lazy dans les commandes": the default. The target is met when `--version` and `--help` are back within about 10 % of `2d9a2aa`, and every other command comes as close as it can, at worst at the measured pydantic import floor, which the PR reports. Each command imports what it needs lazily, when it runs. No follow-up CR on pydantic's import cost.
6. **CR-237's launch cost** (2026-11-14). The same answer accepted the default: the PR measures uv's share of the launch agents use and reports it; this CR leaves the launch alone, with no follow-up CR.
