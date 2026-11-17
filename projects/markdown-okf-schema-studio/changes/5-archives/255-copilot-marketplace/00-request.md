# GitHub Copilot plugin marketplace catalog

Type: feat · Priority: P1 · Filed 2026-11-03 by the main session from the owner's request.

## Owner request (verbatim, French)

> je ne vois pas le fichier .github/plugins/marketplace.json qui déclare un marketplace pour
> copilot, je pense que ca a ete oublié. Cherche dans la doc copilot comment le faire tout en étant
> compatible avec AgentPlugins. verifie bien par un sous agent de revue, tu peux utiliser le CLI
> copilot pour tester mais pas lancer de prompt.

> tu veras faire le dev par dans une CR evidement

> arrange toi juste pour la placer avant l'eventuelle release 1.3.1, sinon tu en feras une pour
> release ca APRES que tout soit merger

## Research (main session, official sources)

| Source | Finding |
| --- | --- |
| [Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference) | Marketplace lookup order: `marketplace.json`, `.plugin/marketplace.json`, `.github/plugin/marketplace.json`, `.claude-plugin/marketplace.json`. Required: `name` (kebab-case, ≤64), `owner` (`name`, optional `email`), `plugins`. Optional `metadata` (`description`, `version`, `pluginRoot`). Entry: required `name`, `source` (relative path string, or `{source: github, repo, ref?, path?, sha?}`, or url); optional `description` (≤1024), `version`, `author`, `homepage`, `repository`, `license`, `keywords`, `category`, `tags`, `strict`… A root `plugin.json` with the Agent Plugins 1.0.0 `$schema` takes precedence over `.claude-plugin/plugin.json`. |
| [Creating a plugin marketplace](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-marketplace) | "Add a `marketplace.json` catalog file to `.github/plugin/`." |
| [github/awesome-copilot `.github/plugin/marketplace.json`](https://github.com/github/awesome-copilot/blob/main/.github/plugin/marketplace.json) | Reference catalog: `name`, `metadata {description, version}`, `owner {name, email}`, entries with `version`, `author`, `repository`, `homepage`, `license`, `keywords`, `source`. |
| [Agent Plugins specification](https://agent-plugins.org/specification) | Defines only `plugin.json` (and MCP); no marketplace or catalog format. Compatibility = the catalog points at the repository root, whose `plugin.json` is the Agent Plugins 1.0.0 manifest. |
| [VS Code agent plugins](https://code.visualstudio.com/docs/copilot/customization/agent-plugins) | Marketplace key must match the catalog `name`; format defers to the Claude Code marketplace format. |

Today Copilot falls back on `.claude-plugin/marketplace.json`, which has no `version` and Claude-only
semantics; there is no Copilot catalog of its own.

## Decisions (owner, 2026-11-03)

1. Path: `.github/plugin/marketplace.json` (singular `plugin`, the documented path), not
   `.github/plugins/`.
2. The plugin entry carries a `version`, kept equal to `package.json` by `scripts/version.py`
   (`just bump-version`) and checked by `test/build/test_plugin_manifests.py`.
3. Ship it in 1.3.1: it must merge before the 1.3.1 version PR (the release session waits for it).
   If it slips, it ships in a later release after everything is merged.
4. Same marketplace name and plugin name as the other catalogs (`markdown-okf-schema-studio`), so
   `copilot plugin install markdown-okf-schema-studio@markdown-okf-schema-studio` keeps working;
   source `./` (repository root, where the Agent Plugins `plugin.json` lives). No `$schema` key in
   the catalog (none is published).
5. Verification with the Copilot CLI is allowed for catalog and plugin commands only
   (`copilot plugin marketplace add/list/browse/remove`, `copilot plugin install/list/uninstall`),
   never a prompt (`copilot -p`, interactive session). A separate review sub-agent checks the work.
