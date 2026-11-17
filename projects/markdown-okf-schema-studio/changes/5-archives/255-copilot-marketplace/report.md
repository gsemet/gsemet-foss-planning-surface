# Report: GitHub Copilot plugin marketplace catalog

PR: [#307](https://github.com/gsemet/markdown-okf-schema-studio/pull/307) · merged 2026-11-03 as `f7b1043d` (rebase) · CI run 41695805742 green · rounds: 1/3

## Delivered

- `.github/plugin/marketplace.json`: Copilot CLI catalog (documented path, read before
  `.claude-plugin/`), one entry `markdown-okf-schema-studio`, source `./` (the Agent Plugins
  `plugin.json` at the root), with `version`.
- `scripts/version.py` bumps the catalog entry version; tests in `test/build/test_plugin_manifests.py`
  and `test/build/test_release.py`; SwRS CORE-074/075 updated; README, CONTRIBUTING, CHANGELOG.

## Proof

- Separate reviewer: APPROVE. Fields checked against the official Copilot CLI plugin reference.
- Copilot CLI 1.0.105, catalog and plugin commands only: `browse` showed the new catalog's
  description, `install` installed 1 skill, `list` showed v1.3.0; owner setup restored byte for byte.

## Open items

- Non-blocking: VSIX exclusion test does not check `.github/**`; entry keys not restricted to the
  reference list in tests; early line break at `README.md:219`.
- Ships in 1.3.1 (version PR cut after this merge).
