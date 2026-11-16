One way to run the CLI: a root pyproject.toml, uvx at a pinned ref, the local code in chantier's own checkout

Today the CLI runs as `uv run --script <skill>/scripts/cli/chantier.py` (PEP 723, kept by CR-221
python-inline-deps), with a second pyproject.toml in `skills/chantier/scripts/cli/`. A launch without
any agent (the web board and its sync started from a planning surface) needs the CLI on a machine with
no plugin: `uvx --from git+https://github.com/gsemet/chantier@<ref> chantier …` works today only with
`#subdirectory=skills/chantier/scripts/cli` (tested 2026-11-13 with uv 0.13.6).