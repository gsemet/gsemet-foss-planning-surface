# Task: GitHub Copilot plugin marketplace catalog

Worktree: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-255
Branch: change-requests/255-copilot-marketplace

## Files (start here)

- New `.github/plugin/marketplace.json`.
- `scripts/version.py` (`PLUGIN_MANIFESTS`, line 19): also bump the catalog entry `version`.
- `test/build/test_plugin_manifests.py` (`VERSIONED`, marketplace checks, "hosts share one name").
- Tests of `scripts/version.py` if any (`grep -rn PLUGIN_MANIFESTS test/`).
- README "Usage with coding agent" (Copilot CLI part, around line 208) and CONTRIBUTING "How to
  Release" step 2 (list of files the version commit changes): name the new catalog.
- The SwRS behind `@tests_req SwRS-MDOKFSTUDIO-CORE-074` / `CORE-075` (plugin packaging).

## Change

What `00-request.md` decides, and nothing more. Catalog content, modelled on
github/awesome-copilot and on `.claude-plugin/marketplace.json`:

- top level: `name` `markdown-okf-schema-studio`, `owner` (`name` Gaetan Semet; `email` only if
  already public in the repo, else omit), `metadata.description`;
- one entry: `name`, `source` `"./"`, `description`, `version` (= package.json), `author`,
  `homepage`, `repository`, `license`, `keywords`, `category` (copied from `plugin.json`).

## Tests first

- `test_plugin_manifests.py`: the catalog entry version equals `package.json` (fails before the
  file exists); the catalog names the same plugin and source `./` as the other catalogs; its
  shape follows the Copilot reference (required `name`, `owner.name`, `plugins[].name/source`,
  name kebab-case ≤64, description ≤1024).
- `scripts/version.py` bumps the catalog version (a test that fails on the unchanged script, if
  the script has tests; otherwise extend the manifest test).

## Requirements

Update the plugin packaging SwRS (CORE-074/075 or the one that lists the manifests) to name the
Copilot catalog; markers per `rules.md`; `just requirements-update`; entry in
`requirements/tiers/log.md`.

## Changelog

One user-facing line under `## Unreleased` in `CHANGELOG.md`, e.g. GitHub Copilot now finds the
plugin through its own marketplace catalog.

## Verification with the Copilot CLI (no prompt)

From the worktree, with a throwaway marketplace name if needed, and removing everything added:

- `copilot plugin marketplace add <worktree path>` (or the local form the CLI accepts; check
  `copilot plugin marketplace add --help`), `copilot plugin marketplace list`,
  `copilot plugin marketplace browse markdown-okf-schema-studio`: the plugin shows with its
  version and description, read from `.github/plugin/marketplace.json` (prove which file was
  read, e.g. by a temporary different description, reverted).
- `copilot plugin install markdown-okf-schema-studio@markdown-okf-schema-studio`,
  `copilot plugin list`: installed with the skill; then uninstall and remove the marketplace.
- Never `copilot -p` nor an interactive session. If the owner already has this marketplace
  registered, record its state first and restore it.

## Gates (foreground)

- `uv run --group docs --group release --group requirements pytest test/build/test_plugin_manifests.py`
- `just check`
- `just requirements-update`
