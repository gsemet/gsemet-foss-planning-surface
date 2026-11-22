# AGENTS.md: name the forge reads ship, take and forge-stack make

Priority P3. Split out of `take-base-from-forge` (its answer Q11), 2026-11-20, by the Chief of Staff.

AGENTS.md says the CLI needs no network once uv's cache holds its packages, except the server's read of a batch's PRs, the forge hub and the surface server's writer. The CLI makes other forge reads today, with the user's own `gh` or `glab`, that this sentence does not name: `ship` reads a PR's base and draft state (`commands/forge_base.py`, `read_state`), `take` and `handoff` read the base of a stacked CR that has a PR (`stacked_read`), and `forge-stack` reads and writes the stack on the forge (`commands/forge_stack_gh.py`, `forge_stack_gitlab.py`).

Make the rule and the code agree: either name these reads in AGENTS.md (and in README or CONTRIBUTING where the same sentence is repeated), or move them out of the CLI. A wording decision on a project rule, for the user. No code change is asked for here.
