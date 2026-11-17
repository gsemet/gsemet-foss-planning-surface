# Package the writing skill as an installable agent plugin (Claude Code, Copilot, Codex)

Type: feat · Priority: P1 · Filed 2026-10-28 by the main session from the user's request ·
Runs in PARALLEL with CR 153 (#167): its own branch from `origin/main`, NOT stacked.

## User request (verbatim, French)

> tu vas lancer une deuxieme CR en parallele sans stack, sur faire un plugin claude (cherche sur
> internet) pour packager le skill writing-for-markdown-okf-schema-studio dans un plugin installable
> facilement dans claude. essaye d'etre le plus ouvert possible, et fournir également un
> "AgentPlugin" https://agent-plugins.org/ pour copilot, et codex.
>
> il faudra que tu alignes les versions (scripts/version.py)

## Goal

Anyone can install the skill `skills/writing-for-markdown-okf-schema-studio/` in one or two
commands, in as many agents as possible:

1. **Claude Code** plugin + marketplace in this repo (`/plugin marketplace add gsemet/markdown-okf-schema-studio`
   then `/plugin install ...`).
2. **Agent Plugins** (open spec 1.0.0, https://agent-plugins.org/ ; spec
   https://agent-plugins.org/specification , schemas https://agent-plugins.org/schemas , repo
   https://github.com/agentplugins/agent-plugins-spec): a portable `plugin.json` + `skills/`.
3. **GitHub Copilot** (CLI and/or VS Code agent plugins) and **OpenAI Codex** (`.codex-plugin/plugin.json`,
   marketplace `.agents/plugins/marketplace.json`): whatever each host officially reads.
4. "As open as possible": one skill source, no copies; every host points at the same `skills/` tree.

## Research first (step 1 of the CR)

Read the OFFICIAL docs (raw pages, not search summaries) and cite them in the PR body:

- Claude Code: https://code.claude.com/docs/en/plugins-reference , marketplace reference, `claude plugin validate`.
  Starting notes from the main session: manifest `.claude-plugin/plugin.json` (only `name` required;
  `version` pins users until bumped), default `skills/<name>/SKILL.md` scan, marketplace file
  `.claude-plugin/marketplace.json`. Plugin names must not start with `claude-`.
- Agent Plugins spec: required fields of its `plugin.json`, layout, which clients support it today.
- Copilot (GitHub docs) and Codex (OpenAI developer docs) plugin formats and install commands.
  Third-party blogs disagree on Codex details (e.g. `agents/openai.yaml`): verify against OpenAI.

Record the per-host findings (format, file path, install command, verified source URL) in a table
in the PR body. If a host has no official plugin format, say so and give the closest official
install path (e.g. copy into `.agents/skills/` / `.github/skills/`), do not invent a manifest.

## Constraints

- **Versions aligned**: every plugin manifest `version` equals `package.json` `version`;
  `scripts/version.py` updates them in the same version commit, and a test (or check in
  `just`/CI) fails when they drift.
- Plugin name kebab-case, e.g. `markdown-okf-schema-studio` (reserved prefixes forbidden).
- Manifests must not end up in the VSIX (`.vscodeignore`) unless intended; do not break the
  extension build or packaging.
- Validate: `claude plugin validate . --strict` (or the plugin dir) passes; the Agent Plugins
  manifest validates against its published JSON Schema; add these to tests/preflight where cheap.
- Docs: README "Install the writing skill" section with the one-liners per host; CHANGELOG;
  requirements (okfreq, `--lifecycle proposed`, unique IDs) for the new deliverable.
- Do NOT modify okf-schema. PR body for an external reader; autonomous decisions listed under
  "Autonomous decisions". No UI change, so no screenshots; show the install commands and the
  validate output instead.

## Addendum (user, 2026-10-28)

> aussi le readme doit fournir cette information, et le skill doit lui meme également décrire
> comment installer le plugin dans vscode depuis
> https://marketplace.visualstudio.com/items?itemName=GaetanSemet.markdown-okf-schema-studio

- README: a section with the install one-liners for every host (Claude Code, Copilot, Codex,
  Agent Plugins), with links.
- SKILL.md itself: a short section telling the reader how to install the VS Code extension
  (Marketplace link above, `code --install-extension GaetanSemet.markdown-okf-schema-studio`,
  or Extensions view search), since the skill is useless without the extension. Keep the skill
  lean (it loads into agent context); the SKILL.md example tests must still pass.

## User feedback on the PR (2026-10-28, via Chief of Staff) — new round

- Rename the README section "Install the writing skill" to "Usage with coding agent".
- Lead with the plugin install, not with copying. Claude Code and GitHub Copilot first, as numbered
  commands: add the Git repository as a marketplace, then install the plugin
  `markdown-okf-schema-studio` from it.
  - Claude Code: `/plugin marketplace add gsemet/markdown-okf-schema-studio`, then
    `/plugin install markdown-okf-schema-studio@markdown-okf-schema-studio`.
  - Copilot CLI and VS Code: marketplace add + install the plugin by name; verify the exact
    install-by-name command against the official GitHub doc or `copilot plugin --help` (do not
    guess).
- Codex and Agent Plugins after that; "copy the skill folder" only as the last-resort fallback for
  hosts without plugins.
- Same wording in SKILL.md / CHANGELOG wherever they say "copy the folder".
- Update the PR body, push, report.
- Copilot CLI syntax (verified by the Chief of Staff from the local `copilot plugin install --help`;
  the docs page gives none). Source forms: `plugin@marketplace` (after `copilot plugin marketplace
  add`), `owner/repo`, `owner/repo:path`, git URL. README: `copilot plugin marketplace add
  gsemet/markdown-okf-schema-studio`, then `copilot plugin install
  markdown-okf-schema-studio@markdown-okf-schema-studio`; a direct `copilot plugin install
  gsemet/markdown-okf-schema-studio` also works. Cite "copilot plugin install --help" as the source.
- VS Code, local Copilot harness: add `gsemet/markdown-okf-schema-studio` to the setting
  `chat.plugins.marketplaces`, linked as `vscode://settings/chat.plugins.marketplaces` (user-given
  URL), then in the Extensions view search `@agentPlugins` > Install. Official source:
  https://code.visualstudio.com/docs/copilot/customization/agent-plugins . A vscode:// link renders
  on GitHub but may not be clickable there: keep the setting name in plain text too.
- VS Code, Copilot CLI / Copilot SDK harness: the Copilot CLI commands as slash commands in the
  session: `/plugin marketplace add gsemet/markdown-okf-schema-studio`, then
  `/plugin install markdown-okf-schema-studio@markdown-okf-schema-studio`. Official source:
  https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-finding-installing
  (terminal form `copilot plugin install PLUGIN@MARKETPLACE`). VS Code also discovers plugins
  installed by Copilot CLI (`~/.copilot/installed-plugins/`).
