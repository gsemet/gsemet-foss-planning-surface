# Report — agent-plugin-packaging

Status: **done** (2026-10-28, branch `change-requests/160-agent-plugin-packaging`,
PR [#173](https://github.com/gsemet/markdown-okf-schema-studio/pull/173), head `e2ed1eec`, merged as 2017e39d, 6f976acf, f3be77ef (rebase-merged)).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 r1 | Repo root is the plugin `markdown-okf-schema-studio`: `plugin.json` (Agent Plugins 1.0.0), `.claude-plugin/plugin.json` + `marketplace.json`, `.agents/plugins/marketplace.json` (Codex); one skill tree; `scripts/version.py` syncs manifest versions; `test/build/test_plugin_manifests.py` (drift, schema, single tree, `.vscodeignore`); SwRS CORE-074/-075 proposed | `2017e39d` |
| T1 r2 | README "Usage with coding agent": plugin install first (Claude Code, Copilot CLI, VS Code local harness and CLI/SDK harness, Codex, Agent Plugins), copy-the-folder last; SKILL.md VS Code extension install; CHANGELOG | `6f976acf`, `f3be77ef` |

## Proof of completion

- `claude plugin validate . --strict`: passed (warning: no plugin icon). `just check` green; `okfreq validate --check-links` 0 errors.
- CI: normal [40725552382](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40725552382) pass on the rebased head; heavy not needed (VSIX unchanged, 58 files).
- Research table: `reports/research.md`; official sources cited in the PR body.

## Open items

- `just version` can leave the tree half-updated if it fails between package.json and the manifests (non-blocking).
- Codex install beyond `codex plugin marketplace add` is not documented by OpenAI.
- Process: the driver made two small edits itself (CHANGELOG re-wrap, CORE-075 file).
- Not removed yet: worktree `../markdown-okf-schema-studio-wt-160` and its branch.
