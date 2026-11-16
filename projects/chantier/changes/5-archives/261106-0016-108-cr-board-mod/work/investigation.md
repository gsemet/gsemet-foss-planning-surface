# Investigation, CR-108 CR board (before round 1)

Binary used: Claude Code 2.1.309 (path from CLAUDE_PID). Contract source: the engine's embedded `claude-code` API d.ts (about 14,000 lines), its long-form guide and the plugin-authoring skill, extracted from the binary. Mods are early access: "this surface may change between releases without notice" (changelog).

## Q1. Copilot and `hooks/`  (verdict: ignored, with one caveat)
Verified (GitHub docs "Copilot CLI plugin reference", agent-plugins.org spec, both fetched):
- `.github/plugin/plugin.json` carries `$schema` = `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`. Copilot docs: that exact value opts a plugin into Agent Plugins semantics.
- Under Agent Plugins 1.0, Copilot reads hooks only from `com.github.copilot/hooks/hooks.json`; "These locations apply only to Agent Plugins 1.0 plugins." Root `hooks/hooks.json` is the LEGACY location (`hooks.json` or `hooks/hooks.json`). So with the `$schema` present, a root `hooks/` is not read.
- The manifest names only `agents` and `skills`, no hooks. (`agents` is not in the closed 1.0 schema; unknown fields are reported and ignored; agents come from `com.github.copilot/agents`.)
Not verified: no Copilot binary here, so I did not run Copilot. The guarantee rests on the docs and on the `$schema` line staying in the manifest. If that line is ever removed, Copilot becomes legacy and WOULD pick up `hooks/hooks.json` and try to run `register.tsx`. Not a stop, but a fragile dependency: add a structure test (Copilot manifest keeps the 1.0.0 `$schema`, names no hooks).

## Q2. Claude Code mod contract: what `$` can and cannot do
| Spec asks | Verdict | Source / note |
| --- | --- | --- |
| `hooks/hooks.json` naming `./register.tsx` | Yes | skill: `{ "modules": ["./register.tsx"] }`, one path, relative to that file. Suffixes .ts .tsx .jsx .js .mjs ... |
| `types/index.d.ts`, named in plugin.json | Yes | skill: `"types": "./types/index.d.ts"` in `.claude-plugin/plugin.json`; declares `interface PluginState { 'cr-board': {...} }` under `declare module 'claude-code'`; `validate` checks every `$.state` key against it. |
| `$`, `$.state` | Yes, but idiomatic form is `atom({plugin,key} as const, init, {shape})`, `read($, atom)` in render, `update($, atom, fn)` in handlers. `plugin`/`key` must be literals. Set refused while a ui.render draws. |
| `$.fs.stat` | Yes | `stat(path,{resolve?})` -> `{kind,size,mtimeMs,isLink[,realPath]}`, rejects ENOENT. `$.fs.read` text is UTF-8, over 4 MiB rejects. The 200 KB cap and "not UTF-8" check are the mod's job (size from stat; behaviour of read on non-UTF-8 bytes not verified). `list`, `exists` also exist. |
| `skill.prompt` | Yes | `on('skill.prompt',{skill:'chantier'},hook)`; input skill,text,frontmatter,source,pluginName?,path?; returns `{text}`; `next(e)` leaves the prompt unchanged. Fires on `/name`, the Skill tool and preloads, so a subagent loading the skill fires it too (session-wide). |
| pane open/close | Yes | `$.ui.open({id,title,focus?,closeOnEscape?})` -> `{isPlaced}` or `{isPlaced:false,reason}`; id `[A-Za-z0-9_-]{1,64}`, "cr-board" ok. Drawn by `on('ui.render',{component:'Pane',requestId:'cr-board'})`. `$.ui.close({id})`; `$.ui.panes()` lists the plugin's own open panes (use for the toggle). `$.ui.invalidate('ui.render')` redraws. |
| slash command | Yes | `$.command.register({name,description,argumentHint?})` in `session.start`, served by `on('command.run',{command:'chantier-board'},async $=>({text}))`. Built-in names refused. |
| timers | Yes | `$.clock.every(ms,fn)` (has `cancel()`), `after`, `sleep`, `now`. Reload drops old timers; start from `session.start`. |
| `git rev-parse ...` | Yes on the CLI; Desktop unproven | `$.process.run(argv,{cwd,env,stdin,timeoutMs})` -> `{exitCode,stdout,stderr,...}`, no shell, 30 s default, documented "CLI only". Whether the Desktop local session counts is NOT verified: needs a real test in Desktop. |
| shared by desktop, mobile, terminal, vscode | Only Box, Text, Button, Link, Code, Markdown | terminal lacks Svg; mobile lacks Input, Select, Client; vscode lacks Client. No fold/disclosure element: folding = state + Buttons. `Markdown` has `onLinkPress`. |

What `$` cannot do / the spec must live with:
- Pane placement: "beside the chat" holds only docked. Asked (command, press) it is placed at any width; unasked it is placed only from 144 columns (110 once asked); terminal docks fullscreen only from 110 columns; below that it waits undrawn. A `skill.prompt`-triggered open may count as unasked on a narrow terminal. Changelog: `$.ui.open` reported placed in sessions with no surface (VS Code, `claude -p`) before a fix; mobile reports isFullscreen false.
- No DOM, no Node, no `import()` in the module; no shell; no network outside `$.http`.
- `claude plugin test` environment has NO fs, network or process: the spec's tests on the worktree path and "unchanged file is not re-read" must stand in for the engine with hooks like `on('ui.open',...)`; the hook names for fs.stat/fs.read/process.run I did not verify (the guide only shows ui.open, command.register, session.start, state.get, tool.call). Test files: `*.test.ts(x)`, kit from `claude-code/testing` (`test`, `expect`, `mount`, `find`, `press`, mocked clock `advance`). Exact-tree asserts must include `part:{plugin}` on each root.
- Type-check: `tsc -p <mod>` only works when the engine laid `<mod>/.claude-plugin/types/` (hot-reloaded folders only; an installed plugin is never written in). In `just check` on three OSes (no claude binary in CI) a type-check is not available without more machinery; the d.ts is only obtainable from the binary.
- `claude plugin validate [--json] [--profile directory] [--strict] <path>` reads manifest and module source, lists hooks and calls, checks `$.state` keys against the contract. `claude plugin test [dir]` runs the tests. Both exist in 2.1.309. I did not run them on the repo (no mod yet).
- Name: plugin names starting with "claude"/"anthropic" are refused; "chantier" ok. A command name Claude Code ships is refused.

## Q3. What the spec touches
`skills/chantier/scripts/cli/src/chantier/status.py` (SCHEMA = 2):
- `_row(repo,d,c,start)`: add `blocked` (as `cr_view`: `blocked_reason` if status blocked), `silent_minutes` (as `cr_view`: `round(age_minutes(c["updated"]))` when `c["status"] in LIVE`; `LIVE = {"working"}` in state.py), `folder` (via `_link`, relative to `3-requests/`). `_row` is shared with `batch_view`, which passes `start=` the batch folder, so STATUS.json of each batch gains these fields with links relative to the batch (additive; the batch folder differs from `3-requests/` for `folder`). Decide the base explicitly.
- `dashboard_view` (about line 277 returns `backlog`): batch entries need `heartbeat` and `orders_pending` (already in `batch_view`'s dict); add `landed`, `trashed`, `landed_total`, `trashed_total` from `paths["archives"]` / `paths["trash"]` (`lifecycle.py` lines 18-20), newest first by `YYMMDD-HHMM` prefix, 50 each, STATUS.json else `_title`. Keep the 100-file read cap in mind.
- `dashboard_markdown`, `_backlog`, `write_dashboard`: unchanged. `_title` used as fallback.
- SCHEMA bump: spec decides; the Foreman should say whether a field addition bumps 2 -> 3 (the mod must then read 2 and 3).

Tests and scenario:
- `scenario/run_scenario.py`: dashboard checks near lines 460-465 (STATUS.md), 632-634, 697-714 (`status_files`), 739-741 (abandoned batch absent). Nothing checks STATUS.json board fields yet. New checks belong in `status_files` and after the land/abandon steps (landed/trashed listing, totals, `blocked`, `silent_minutes`, `folder`, `heartbeat`, `orders_pending`). The 50-item limit needs a fixture with more than 50 archive folders (cheap to fabricate directly on disk). Required gate: `just scenario` (CLI changed).
- `tests/test_structure.py`: nothing objects to new root `hooks/` and `types/`: `test_manifests_agree` checks names and Copilot's skills/agents folders only; the agent-folder test lists only `agents/` dirs; link checks scan SKILL.md and references only; the smoke test requires git status to show only `.agents/changes/`. Candidate checks to add (few, fast): hooks.json names an existing module; Claude plugin.json `types` file exists; Copilot manifest keeps the 1.0.0 `$schema` and names no hooks; the mod's `PluginState` key equals the plugin name. `scripts/version.py` TARGETS: not read; if `.claude-plugin/plugin.json` is the only mod manifest no change (the mod is the same plugin, so no new version file).
- `.github/workflows/ci.yml` runs `just check` on ubuntu/macos/windows: `claude plugin test` cannot be part of it (no binary), so the mod's tests are a documented local step (CONTRIBUTING.md), not a CI gate. Spec's Done-when must say so.

## Smallest change
1. status.py: three fields on `_row`, two on batch entries in `dashboard_view`, four new top-level lists/totals; scenario checks.
2. `hooks/hooks.json`, `hooks/register.tsx`, `types/index.d.ts`, `"types"` key in `.claude-plugin/plugin.json`, mod test file `hooks/*.test.tsx`.
3. README line for `/chantier-board`; CONTRIBUTING: mod and how to run `claude plugin validate/test`.
4. A few structure tests as listed above.

## Risks
- Early-access API, may change between releases without notice.
- `$.process.run` documented "CLI only": git root lookup may fail in Desktop (the spec's main target). Test in Desktop before trusting it.
- Pane placement rules (not always "beside the chat").
- No CI for mod tests or type-check.
- Copilot isolation depends on the `$schema` line.
- `_row` reuse changes batch STATUS.json (additive).
- `skill.prompt` fires for subagents too, so Drivers/Workers loading the skill may open the pane.

## Questions only the user can answer
1. Accept that mod tests and type-check are local only (no binary in CI)?
2. Desktop: confirm `$.process.run` works in a Desktop local session, or accept a degraded board (no worktree resolution) there.
3. On narrow terminals the pane may not be placed unless the person asks: acceptable?
4. Bump `SCHEMA` 2 -> 3 for the added fields, or stay at 2 (additive)?
5. Should the pane open on a subagent's `skill.prompt` or only for the main session?
