# Investigation

## Entry points and current startup reads

The implementation worktree is `chantier/batch-20/cr-296`, based on
`origin/main` at `5eb0c1e`. The Claude and Copilot role wrappers are intended
to have identical bodies; `skills/chantier/scripts/cli/tests/test_plugin_files.py`
enforces this for all 14 roles (`DRIVERS`, `WORKERS`, and `CHIEF_ROLES`).
The wrappers only establish the prompt contract and point the worker at its
card; they do not load a common startup manifest.

Current direct skills:

* Chief of Staff: `skills/chief-of-staff/SKILL.md` (2,955 bytes), then
  `references/concepts.md` (52,952), `references/session-start.md` (15,558),
  `references/chief-of-staff.md` (133,201), and the selected host reference:
  `references/hosts/claude-code.md` (68,049) or `hosts/copilot.md` (8,279).
  The files/sections are explicitly named in the skill and the cards:
  concepts (whole file), session-start (whole file), chief-of-staff (whole
  file), and the host reference (whole file). Totals are **272,715 bytes
  Claude** and **212,945 bytes Copilot**, before project rules and command
  output.
* Griller: `skills/griller/SKILL.md` (2,156), concepts (whole), session-start
  (whole), `references/griller.md` (5,871), and the host reference (whole):
  **144,586 bytes Claude**, **84,816 bytes Copilot**.
* Router: `skills/chantier/SKILL.md` (2,719), concepts (whole), and
  session-start (whole), **71,229 bytes**; it then loads the selected role
  skill. Status is separate: `skills/status/SKILL.md` (2,452) and only
  `references/status-layout.md` (15,916), **18,368 bytes**.
* Drivers: `cr-driver`, `qa-driver`, `release-driver` use
  `references/driver.md` (85,140); `stack-driver` uses `foreman.md` (57,561).
  Each reads its own wrapper and then its card. Workers read their matching
  card: `investigator` 3,482; `coder` 4,232; `inspector` 5,290; `debugger`
  3,353; `verifier` 10,333; `conflict-resolver` 3,544; `demo-explorer`
  3,234. Chief-started cards are `spec-writer` 2,421, `spec-critic` 3,481,
  and `retro-critic` 2,901. The wrapper byte counts are measured with `wc -c`
  (Claude 937–1,341; Copilot 1,004–1,394), but are host metadata/prompt
  material rather than a declared core.

The Chief path has no host-specific selection inside the core: the host card is
read in full. On reload, `session-start.md`, section **5. Reload**, again
requires concepts, itself, the role card, the host card, and status-layout;
direct-batch Chief startup additionally reads foreman. This is the largest
repeat path. Hooks are Claude-only: `hooks/hooks.json` loads `./register.tsx`;
Copilot's manifest has no hooks. The two plugin manifests enumerate the four
skills and Copilot's agent directory, but do not declare startup reads.

## Consumers and breakage surface

Named consumers are primarily structural rather than semantic. Exact tests:

* `test_plugin_files.py::test_manifests_agree`,
  `test_the_board_mod_is_wired_on_claude_only`,
  `test_each_host_ships_one_agent_per_role_and_nothing_else`,
  `test_both_hosts_give_a_role_the_same_body_and_their_own_frontmatter`,
  `test_a_worker_agent_file_points_to_its_card_and_refuses_a_prompt_without_it`,
  `test_skill_and_references_links_resolve`, and
  `test_every_file_carries_the_same_version`.
* `test_playbook_config.py` asserts the Copilot model error text and host
  anchor `hosts/copilot.md, "Models"`.
* `scripts/version.py` counts version declarations in all four `SKILL.md`
  files, both plugin manifests, and all Copilot agents.

The CLI itself does not parse the cards. `skills/chantier/scripts/cli/src/chantier`
contains the rails and commands, while `scenario/run_scenario.py` exercises
the lifecycle and autosync/board records without reading card headings.
The relevant recipes are `just test` (pytest), `just check` (lint + test +
release-notes), `just scenario` (the no-model end-to-end scenario), and
`just mod` (Claude plugin validate/test). On this checkout all recipes using
`uv --locked` are currently blocked before useful work: `just test` was run
and failed in **0.27 s** because `uv.lock` needs updating. Therefore no
honest duration is available yet for check/scenario/mod; do not estimate one.
The project rule says `just test` must stay under 30 seconds and the historical
Windows measurement was 18.5 seconds (2026-11-14); `just check` is required
before hand-back and `just scenario` is the long gate.

## Contradictions with the accepted specification

These are direct file/section conflicts, not implementation claims:

* `skills/chantier/references/session-start.md`, **2. The seat and the role**
  and **The board**: a Chief automatically takes a free seat and immediately
  launches the board, while the specification requires asking before board
  launch and asking before takeover of another/unknown session.
* The same file, **The surface's autosync**: role startup automatically joins
  autosync, and the board joins it on fresh start; the specification makes
  persistent autosync explicit opt-in and board-independent.
* `skills/chantier/references/concepts.md`, **Planning surface**, says the
  board joins the autosync group; `AGENTS.md` lines 36–38 names the same board
  exception and says it runs autosync start/stop/approve.
* `skills/chantier/references/chief-of-staff.md`, **The project / The allow
  rules (P10)**, describes a first-message permission question and writes
  `~/.claude/settings.json`; this is not the accepted blanket activation
  behavior (CLI preparation is the explicit automatic exception).
* `skills/chantier/references/chief-of-staff.md`, **What the user hears** and
  **The trials before the go**, requires a long startup report and preflight
  trials; the specification calls for a short factual report with measured,
  announced, available, untested, and blocked states.
* `skills/chantier/references/session-start.md`, **1. Start checks, first**,
  permits preflight/configuration behavior whose actual effects must be
  classified, whereas the specification makes ordinary checks read-only and
  permits only official CLI preparation and the defined seat exception.
* `docs/use-cases.md`, startup/install text, repeats the automatic allow-rule
  and setup story and must be aligned if it states the old behavior.

## Measurement and smallest coherent design

There is no existing CLI command or test that measures mandatory startup bytes;
the existing structure tests only check existence, links, versions, manifests,
and host parity. Add a small parametrized fast test in
`skills/chantier/scripts/cli/tests/test_plugin_files.py` (or a focused
`test_startup_manifest.py` beside it) that loads one manifest, resolves paths,
uses `Path.read_bytes()`/`len`, and asserts every role/host total is `<= 12_288`.
It should also reject undeclared mandatory files and missing action references.
Do not make the CLI track comprehension.

Smallest coherent design:

1. Declare one `skills/chantier/references/startup-manifest.yaml` (or JSON if
   the existing parser cannot safely read YAML) with `version`, common core,
   host entries, role entries, and an `actions` map. Each role/host names
   exact paths and optional heading anchors; the test is the authority for
   byte accounting.
2. Replace the large common startup reads with short `core.md` and short
   `host-core-{claude-code,copilot}.md`; retain the manifest as the sole
   declaration. Put the action-to-required-readings table in the manifest
   (or a directly linked short `startup-actions.md`) and make each action
   refuse/stop when an indispensable declared reading is unavailable.
3. Keep the large cards as deferred action references: relocate detailed
   Chief/session material into action sections, trim duplicated rules, and
   retain `driver.md`, `foreman.md`, and role cards for the actions that need
   them. `concepts.md`, `chief-of-staff.md`, `session-start.md`, and host
   references should become deferred references rather than mandatory boot
   reads; do not duplicate them in a second “short” card.
4. Update both skill entry points and both host paths together. Update
   `AGENTS.md` and the planning-surface contradiction only where they conflict
   with the accepted startup contract. Preserve plugin manifests and hooks,
   adding only a manifest link if needed; no hook should inject a second
   mandatory core.

Risks are exact-name/heading links in the skill files, tests, docs, and
Copilot model-error assertion; moving headings without compatibility anchors
will break `test_skill_and_references_links_resolve` and prompt contracts.
Changing card sizes changes the measured values and requires searching every
old path, heading, version declaration, and manifest list. No question remains
for the user: the answers and Batch go authorize this scope.

## Evidence plan

At the implementation head, record `git rev-parse HEAD`, then run
`wc -c` through the manifest resolver (and save its plain output under the CR
evidence/work log) for every role × Claude/Copilot host. The Verifier should
run the new parametrized structure test, which proves each resolved mandatory
file total is at most 12,288 bytes, and inspect the manifest for the complete
role/host matrix and action table. Run `just test`, `just check`, `just scenario`
and, because skills/manifests/hooks change, `just mod`; capture exit status and
elapsed time. The long-gate evidence is the pipeline's
`just scenario (ubuntu-latest)` at the PR head. Also run targeted tests for
seat takeover, board refusal/independence, autosync opt-in, CLI failure,
reload idempotence, and short report evidence; these behaviors currently have
no single existing startup-byte mechanism. The current head's only measured
gate evidence is the `just test` lockfile failure above; no successful behavior
or <=12,288 result is claimed.
