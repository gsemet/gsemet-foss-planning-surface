# The Drivers run Sonnet

The user: "Passe les driver en Sonnet, c'est possible ça ?"

Found:

- `agents/cr-driver.md`, `agents/stack-driver.md`, `agents/release-driver.md` set
  `model: claude-opus-5-5`; the QA driver already runs Sonnet.
- Their Copilot twins set `[Claude Opus 5.5, claude-opus-5.5]`.
- `tests/test_structure.py` holds `OPUS_ROLES` and asserts it on both hosts.
- batch-06: Opus costs twice Sonnet on every field; the cr-driver spent $20.48 and the stack driver
  $1.92. Sonnet's quality in these roles is not measured.
