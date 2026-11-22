# Remote CLI commands through the surface server; the TUI one of them

The user (2026-11-22): turn the terminal client into a family of CLI commands, like Vercel Board's
idea, so that other agents can act from the command line, remotely, through the surface server
(take, ...). One of these subcommands is today's TUI (for instance a board TUI subcommand), another
the web UI (`chantier webui`). The web UI will later move to its own project. Place it in batch-30
right before CR-447 docs-gardening.

Conflicts to grill: `chantier board` starts the surface server today; AGENTS.md says the server
"never edits a batch and never messages an agent", so remote batch actions change that rule.