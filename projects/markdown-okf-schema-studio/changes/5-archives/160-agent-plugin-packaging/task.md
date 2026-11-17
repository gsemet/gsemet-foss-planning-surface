# Task T1 — Writing skill as an installable agent plugin

Implement `00-request.md` (goal, research, constraints and addendum) in
`../markdown-okf-schema-studio-wt-160` on branch `change-requests/160-agent-plugin-packaging`
(from `origin/main` d48739d7, own `npm ci`).

## Definition of done

- Research table (host, format, file path, install command, official source URL) from raw official
  pages; no invented manifest; hosts without an official format say so.
- Claude Code plugin + marketplace, Agent Plugins manifest, Copilot and Codex as officially
  supported, all pointing at the single `skills/writing-for-markdown-okf-schema-studio/` tree.
- Every manifest `version` = `package.json` `version`; `scripts/version.py` updates them; a test
  fails on drift (new test fails before the version code change).
- README install one-liners per host; SKILL.md says how to install the VS Code extension
  (marketplace link + `code --install-extension GaetanSemet.markdown-okf-schema-studio`);
  CHANGELOG; requirements `--lifecycle proposed`.
- VSIX contents unchanged except as intended (`.vscodeignore`).

## Gates

- `just check`; `just requirements-update`; `uv run --group requirements okfreq validate
  --check-links --project-root .`; `claude plugin validate . --strict` (or the plugin dir) if the
  CLI is available; Agent Plugins manifest validated against its published JSON Schema.
- Normal CI green on the PR (no UI change: heavy CI not required unless the VSIX packaging test
  is heavy-only).
