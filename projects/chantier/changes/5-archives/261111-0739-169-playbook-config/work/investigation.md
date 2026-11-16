# CR-169 investigation: the map for the `chantier.yaml` playbook

Read-only pass over the worktree `C:\Users\gaeta\Projets\chantier.worktrees\batch-09-CR-169`. Paths are
relative to it. CLI = `skills/chantier/scripts/cli/src/chantier/`.

## 1. CLI

### New module `playbook.py`
- Nothing to reuse for YAML: `state.read_keyed` (state.py:214) is a flat `key: value` reader for
  `checkout.yml` (comment strip with `(^|\s)#.*$`, `.strip("\"'")`); the new strict subset reader sits next
  to it or in `playbook.py`. Read with `utf-8-sig` (BOM), as the spec says.
- Plugin roles come from files, the way `_agent_problems` (commands.py:133) finds them: `plugin_root()`
  (59), `agents/*.md` (Claude) or `com.github.copilot/agents/*.agent.md` (Copilot). Role name = file stem,
  minus the `chantier-` prefix and `.agent` suffix on Copilot. `_agent_problems` returns strings only: add a
  small helper `plugin_roles(host) -> list[str]` (sorted, same folder logic) in playbook.py or commands.py
  and have `_agent_problems` reuse it. When `plugin_root()` is None (a skill alone) `playbook` must say so
  (exit 2), as P4 does.
- The file path: `Repo.find().root / "chantier.yaml"`. `Repo.root` is the project's repository, or the
  clone in external mode (state.py:274), and it is the main checkout even from a worktree (found through
  `git-common-dir`, state.py:297-307), so the spec's open question 1 is met by `repo.root` as is.
- Model table, per host: Claude has no display names in agent files (plain ids `claude-sonnet-5-5`,
  `claude-opus-5-5`); `costs.PRICE` (costs.py:28-32) keys the same three Claude ids plus a
  `claude-haiku-5-5>100k` pricing variant: do not seed the table from PRICE's keys blindly (the `>100k`
  key). Copilot frontmatter is `[Display Name, id]` (see 2).

### cli.py
- `_parser()` (cli.py:16): new `cmd("playbook", commands.playbook, ...)`. `cmd(batch=True)` (line 24) already
  adds `--batch`; `--host claude|copilot` is new (`choices=["claude","copilot"]`; `detect_host(explicit)`
  already takes `explicit`, commands.py:79). Note `preflight` and `init` use `batch=False`.
- `FULL_OUTPUT` (cli.py:13): add `"playbook"` (12 lines of roles exceed MAX_LINES = 10, cli.py:11).
- The help line of `preflight` (cli.py:34) says "check P1, P4–P8 and P10": update to name P12 (and P11 is
  already missing from it).
- Exit codes: `EXIT_PRECONDITION` = 2 (state.py), already used by `ChantierError(..., EXIT_PRECONDITION)`;
  `main` prints `error: <message>` to stderr and returns the code (cli.py:193-195). A multi-problem refusal
  is one `ChantierError` whose message holds one problem per line (each `chantier.yaml:<n>: ...`), since
  `main` prints a single stderr block; or `playbook` could return `(lines, 2)` like `preflight`/`gate`
  (tuple results go to stdout with the code, cli.py:196). The spec says "exit 2, every problem listed": the
  stdout tuple form fits `playbook`; `open` must raise (nothing moved).

### commands.py
- `open_batch` (560-637). Order today: `Repo.find`, `detect_host`, slots/budget check, remote and default
  branch, `settings`, `stage_layout(repo)` (574, creates stage folders), release grant, chief transcript,
  `prepared_cr` for each item (590: this is what moves nothing yet; folders move in `add_cr` inside the
  lock, 606). Read and resolve the playbook right after `detect_host` (line 562) or at 563, before
  `stage_layout`, so an invalid file stops everything: spec says "before it moves any folder".
  Record it in the `data` dict (593-601), a new key `"playbook"` next to `"settings"`, only when the file
  exists (spec: nothing recorded otherwise). `Batch.__enter__` (state.py:430-453) writes `create` as the
  data; any key is kept. Old batches have no key: `playbook --batch` and `team:` must treat a missing key as
  "no playbook".
- `brief.md` (612-627) has a line `- Team (who runs which role):` left empty for the Chief of Staff; the
  spec does not ask to fill it from the playbook (no change needed; mention only).
- `_facts` (1245-1292), the single producer for `take` (1350), `round_` (1368) and `handoff` (1299): append
  the `team:` lines at its end (or before `notes:`; spec says "after their other lines", i.e. at the end,
  after the gate log tail at 1290-1291). `d` (batch data) is already a parameter, so
  `d.get("playbook")` is read there; nothing else to thread. These three commands are all in `FULL_OUTPUT`.
  `take stack` (1318-1338) returns early without `_facts`: it prints no `team:` lines; the Foreman starts the
  stack driver from `playbook --batch` (consistent with the spec's "who reads what"). Say so in the card.
- `playbook(args)` is new, near `rules` (1467) or after `preflight`. With `--batch`: `resolve_batch(repo,
  args.batch)` then `read_batch(...)`/`read_batch_json` (state.py:75) and print `d.get("playbook")`; no file
  read. Without: read the file for `detect_host(args.host)`.
- `preflight` (188-272). Check numbering: tags in order of appearance P1, P6 (error case only, 223), P4, P5,
  P6, P7, P8, P11 (external only), P10 (Claude only), then a literal line "P3, P9 and 'not unattended' are
  the Chief of Staff's own checks" (269-270, `P2, P3, P9` outside `--direct`). P2, P3 and P9 are the Chief of
  Staff's; P12 is free. Add P12 inside `if repo:` after P8 (it needs `repo.root`), via the local
  `check(tag, passed, good, bad, warn=False)` helper (191); a failing P12 sets `ok` False so the closing
  line is "preflight FAILED: start nothing" and exit 2. Host None: P12 cannot resolve a host-specific model,
  so skip or check structure only; decide in the spec (the spec does not).
- **Line budget risk.** `preflight` is not in `FULL_OUTPUT`, so `MAX_LINES = 10` truncates it
  (cli.py:197-198). Today an in-project Claude run prints exactly 9 lines (P1, P4, P5, P6, P7, P8, P10,
  the "P3, P9" line, "preflight passed"); external mode adds P11 and prints 10. P12 makes them 10 and 11:
  an external run would lose its last lines (cut to 9 plus "… 2 more lines"), hiding "preflight passed"/
  "FAILED". The test `test_preflight_warns_on_missing_allow_rules...` asserts `len(out) <= 10` (test_structure.py:320).
  Fix choices for the Driver: add `"preflight"` to `FULL_OUTPUT`, or fold P12 into an existing line. Flag
  to the Chief of Staff; adding to `FULL_OUTPUT` is the smallest.
- Existing P-check tests: test_structure.py:196-230 (no-setup run), 292-303 (direct preflight leaves out
  P2), 306-337 (P10). No per-P unit tests otherwise; scenario checks P1 and P10 at run_scenario.py:448-468.
- `_apply_order`/`order` do not touch the playbook: a running batch keeps its own. `apply_batch_settings`
  (state.py:258) is the precedent: it reads `data["settings"]`; the playbook needs no equivalent because it
  is only read from `data`.

## 2. Agent-file frontmatter model formats

Claude Code (`agents/<role>.md`): `model: claude-sonnet-5-5` or `model: claude-opus-5-5`, plain id, line 4.
Opus: stack-driver, release-driver, spec-writer; the other 9 Sonnet. No haiku anywhere.

Copilot (`com.github.copilot/agents/chantier-<role>.agent.md`): a flow list of `[Display, id]`, line 4, then
`model-policy: required`:
- `[GPT-5.6 Luna, gpt-5.6-luna]`: coder, conflict-resolver, debugger, demo-explorer, investigator;
- `[GPT-6.1 Sol, gpt-6.1-sol]`: inspector, verifier;
- `[Claude Sonnet 5.5, claude-sonnet-5.5]`: cr-driver, qa-driver;
- `[Claude Opus 5.5, claude-opus-5.5]`: release-driver, spec-writer, stack-driver.
The ids use a dot on Copilot (`claude-opus-5.5`), a dash on Claude: the spec's normalisation turns both
into `claude-opus-5-5`, but the two hosts need their own table rows (their start values and exact ids
differ). The Foreman is started with `model: "claude-opus-5-5"` (claude-code.md:18) and
`"claude-opus-5.5"` (copilot.md:15): sessions, not in the table.

## 3. tests/test_structure.py conventions

Path: `skills/chantier/scripts/cli/tests/test_structure.py` (355 lines), with `conftest.py` (`repo`
fixture: a git repo with AGENTS.md; `chantier(*args)` runs `main` in-process and returns `(code, stdout
lines, stderr)`; `PLUGIN_ROOT`, `SKILL`, `sh`). Conventions: module constants `CLAUDE_MODELS = {"claude-sonnet-5-5",
"claude-opus-5-5"}`, `ROLES`, `agent_file(role, host)`, `_front(path)` (splits the frontmatter on `": "`, so
Copilot's model arrives as the string `"[GPT-5.6 Luna, gpt-5.6-luna]"`: strip the brackets and split on
`", "`), `@pytest.mark.parametrize("host", ...)`, `monkeypatch.setenv("CHANTIER_HOST", ...)`. Tests are
plain functions with `assert`. Related: `test_both_hosts_give_a_role_the_same_body_and_their_own_frontmatter`
(108-123) already reads every role's model on both hosts and asserts `claude["model"] in CLAUDE_MODELS`
(116): the spec's drift test belongs next to it (loop `ROLES` x `("claude","copilot")`, take the id, call the
resolver with it, assert it returns that entry). A haiku entry in the table makes `CLAUDE_MODELS` narrower
than the table: keep that constant as is. The second test (no duplicate identifier or display name per host)
imports the table from `chantier.playbook`. Existing check that `RECOMMENDED_ALLOW` is imported from commands
(line 14) is the precedent for importing table constants into tests.
The "no setup" test (198-230) already proves the plugin runs with no `chantier.yaml`; S1 can reuse it.
Docs links are tested (126-131): every `](...)` link in SKILL.md, references, README, docs must resolve,
so a new link in the amended docs must be valid. HOST_TOOLS test (178-191): the cards must hold no host
tool name outside lines with `hosts/` (`SendMessage`, `TaskStop`, ...): the new "Starting an agent" text in
concepts.md/chief-of-staff.md/foreman.md/driver.md must not name host tools such as `Agent`'s parameters
(`SendMessage`, `write_agent`...); `Agent`/`task` are not in that list, but keep model-passing mechanics in
`hosts/*.md`.

## 4. scenario/run_scenario.py structure

- Globals: `CHECKS`, `check(label, ok, detail)` (59), `note()` (53), `World` (66) with `w.chantier(*args,
  env=None, expect=0, cwd=None)` (130; returns `(code, out_lines)`; stderr in `w.last_stderr`; `expect=None`
  to not auto-fail), `w.start(...)` (opens a batch, sets `w.name`), `w.reset()` (158, sweeps `4-batch` so a
  case can open again), `w.batch()`, `w.folder()`, `w.state`, `w.work`. `World.env` sets `CHANTIER_HOST=claude`
  and pops `CHANTIER_PLUGIN_ROOT`, so the plugin root is the repo (agent files are found: preflight P4 passes
  in section 1).
- `scenario(w)` (446-777) runs numbered sections then calls helper functions in a fixed order (758-777):
  `close_batch`, ..., `lost_messages`, `failed_opening`, `cancel_during_gate`, `rails`, ... `seat_handover`.
  Each helper starts `note("\n## <n>. ...")`, uses `w.reset()` when it needs a fresh open, and `check(...)`.
- Add one helper `playbook(w)` (S1-S6) and call it from `scenario` right after `failed_opening(w)`
  (line 772), the section that already does clean `open` failures. Its shape:
  `failed_opening` (1415-1432) is the model for S4: prepare an item with `prepare_cr`, make `open` fail
  (`expect=None`), then check `code == 2`, the message, and that the item folder is back/unmoved and
  `list((w.state/"4-batch").glob("batch.json"))` is empty. Each refusal in S4 reuses that pattern after
  `(w.work/"chantier.yaml").write_text(...)`.
- Write `chantier.yaml` into `w.work` (the repo root); remove it at the end (S6) and between cases. It is
  untracked in the main checkout, harmless to worktrees, but the check "nothing was written in the working
  tree" (469) runs earlier, so it is not hit.
- S2: Claude capability is the trial's outcome; the table's flag is what the scenario sees, so write S2
  conditionally on `chantier.playbook`'s capability for claude (import path is set up at line 461:
  `sys.path.insert(0, SKILL/scripts/cli/src)`).
- Ordering trap: batch numbering. `w.reset()` removes `4-batch`; `next_batch_number` uses
  `.batch-number`, so successive opens in the helper are batch-N, N+1 ... (a name taken from the `open`
  output via `w.start`). S3 needs a running batch with two CRs (open both), edit `chantier.yaml`, `take` the
  second CR, `playbook --batch`. `take` needs an epoch: `--epoch` is needed only after a Foreman set one; in
  a fresh batch epoch is 0 (check how `rails`/`failed_opening` neighbours take) so the helper may need
  `w.chantier("foreman","set",...,"--epoch",1)` as in line 506.
- `--host copilot` S5 and the S4 `gpt` case are CLI-flag cases, independent of the environment: `playbook
  --host copilot` reads the Copilot agent folder under `SKILL.parents[1]`.
- `scenario/README.md` lists what the scenario covers (25-86): add one bullet.
- Gate: `just scenario` runs both forges (justfile `scenario`), so S1-S6 run twice; keep them fast.

## 5. Lines to amend

### The "only configuration" sentence (exact locations, all in the worktree)
| File:line | Text there |
| --- | --- |
| `AGENTS.md:7` (continues on 8) | "The plugin must work with no setup: the user's `AGENTS.md` is the only configuration, and" |
| `README.md:14` | "- **Zero configuration.** Your `AGENTS.md` is the only configuration. Everything chantier writes" |
| `skills/chantier/SKILL.md:18` | "agents, the project's `AGENTS.md` is the only configuration, and everything chantier writes goes" |
| `skills/chief-of-staff/SKILL.md:23` | "project's `AGENTS.md` is the only configuration, and everything chantier writes goes to the" |
| `skills/griller/SKILL.md:18` | "project's `AGENTS.md` is the only configuration, and everything chantier writes goes to the" |
| `skills/status/SKILL.md:18` | "project's `AGENTS.md` is the only configuration." |
| `skills/chantier/references/session-start.md:124` | "- **Zero configuration:** the project's `AGENTS.md` is the only configuration (I learn how it" |
| `skills/chantier/references/chief-of-staff.md:60-61` | "Nothing is configured / anywhere else." (the spec's "The project" line) |
Related lines the spec did not list but say the same thing (decide whether to amend):
`README.md:346` "Nothing is configured in chantier." (about the forge CLI login, probably fine as is);
`docs/tutorial-claude-code.md:74` "It records nothing anywhere else" (about the Chief of Staff's own offers; read it first);
`scenario/README.md:25` and `scenario/run_scenario.py:455` "no setup" (a test label, true with no `chantier.yaml`).

### Cards and references (spec "Cards and references touched")
- `skills/chantier/references/concepts.md`: "Starting an agent" section 159-193 (line 162 "it passes no model
  and no effort"); prompt template 165-175 with `Team:` at 173 (add `Needs:` after it); rule 2 "No fallback"
  at 203-206 (add the one sentence); also the output-lines sentence at 155-157 lists the commands exempt from
  the ten-line cut: add `playbook` there.
- `skills/chantier/references/chief-of-staff.md`: entry row at 32 ("use my agent for <role>", ..., "which
  models?" -> `chantier` section of `AGENTS.md`); "The project" 56-85 (60-61, 68-85: the `chantier` section
  example 71-77, the sentence at 84-85 "The host's reference says which model each role runs"); "Starting a
  batch" 162-: step 1 preflight list at 166-176 (add P12; mention the needs check), step 2 plan at 177-189
  ("the team"), the Foreman's prompt block 207-215 with `Team:` at 214; the Spec-writer start at 190-193 of
  concepts.md and its start in chief-of-staff.md (find it with "spec-writer", around the "Backlog and grill"
  section 106-); Demo explorer start in "Subagents and the demo". Hard-rules "No fallback" bullet at 40-42.
- `skills/chantier/references/foreman.md`: "Your means" 51-64, the `take` bullet at 55-58 (add that a Driver
  start reads `playbook --batch`).
- `skills/chantier/references/driver.md`: "Your means" 13-: bullet 18-21 ("with the agent your prompt's
  `Team:` names"), and line 106 ("each review step your `Team:` lists").
- `skills/chantier/references/hosts/claude-code.md`: rows at 26 ("Start a Driver or a worker": "no model, no
  effort"), 27 ("Start the Spec-writer": same), 33 ("Models"); no row exists yet for how a session sees its
  skills (add after 22 "Load another skill", which is related).
- `skills/chantier/references/hosts/copilot.md`: rows 18 and 19 ("no model, no effort"); there is no "Models"
  row at all (copilot.md:11-31): add one, plus the skills row.
- `skills/chantier/references/init.md:75` and `session-start.md:31`, `chief-of-staff.md:62`: mention
  "P5, P9, P10" as what the Chief of Staff tells the user from preflight; add P12 only if its FAIL is
  reported there (a P12 FAIL fails preflight: "start nothing" already covers it).
- Agent files: unchanged (open question 6 settled as no change).

### Docs
- `docs/tutorial-claude-code.md`: section 8 at 177-213 (the `chantier` section at 188-195, the default models
  paragraph 201-203, which stays).
- `docs/use-cases.md`: "Use your own agents" 148-165 (the `chantier` section mention at 152 and 164).
- `README.md`: line 14; table at 195-197 ("use my `rust-coder` agent...", "which agents and models?");
  "Your own agents" 210-225 (the `chantier` section example at 212-220); "Models" 227-243. One line naming
  `chantier.yaml` goes in the zero-configuration bullet.
- `README.md` and `docs` also hold a CLI-command list? Only `chantier rules`-style mentions were found
  (CONTRIBUTING.md has 2); no single command table to extend. `CONTRIBUTING.md:56` is the "no fallback"
  design rule (a line to read when adding the needs sentence, not a required edit).

## 6. Open points the Driver must settle or flag
1. Preflight line budget (see section 1): P12 pushes an external run to 11 lines; truncation hides the
   verdict. Needs `FULL_OUTPUT` or a merged line.
2. Resolution rule "contains it as whole dash-separated parts" does not say contiguous: `gpt-5` on Copilot
   (parts `gpt, 5, 6, luna`) must match Luna by contiguous prefix; `5-5` would be rejected earlier (no
   letter). Pick contiguous.
3. `take stack` prints no `team:` lines (it returns before `_facts`): the stack driver's own workers' team
   reaches it through the Foreman's prompt `Team:` line.
4. `playbook --batch` on a batch opened before this CR (no `playbook` key) and on a batch opened with no
   file: print the same "no chantier.yaml" line; `--host` with `--batch`: ignore or refuse (spec says
   nothing).
5. P12 with an unknown host (host None): skip.
6. A Claude start value cannot be settled until the trial; the structure of the code must not hard-code it:
   one table field per host (`start_value`/capability).

## 7. Evidence plan

Checks (each a command run at the pushed head, output kept in `evidence/`):
1. `just check` on Linux, macOS and Windows (CI) and locally on Windows: structure tests including the two
   new ones (every agent-file model resolves to itself on both hosts; no duplicate id or display name per
   host).
2. `just scenario` (both forges): sections S1-S6 as in the spec, each a `check` in `playbook(w)` after
   `failed_opening(w)`; S2 conditional on the recorded Claude capability. Keep the transcript
   (`scenario/results/*.md`, not committed) and quote the S1-S6 lines.
3. Unit-level proof of the parser from structure tests or the scenario: each S4 refusal with its line number
   (`chantier.yaml:<n>:`), exit 2, `open` moving nothing (the `failed_opening` pattern); BOM accepted;
   a duplicate key, anchor, tab, flow mapping, `---` refused.
4. By hand, once, on the user's Claude Code, recorded in `hosts/claude-code.md` with date and mark: the trial
   of a model passed at an `Agent` start (read the transcript's model), and the needs trial (one installed
   skill and one missing: only the missing one is warned). Copilot stays "none, unproved" with its trial
   written.
5. `preflight` output on an in-project and an external run with a `chantier.yaml` present, showing P12 and the
   closing line intact.
6. `git status --porcelain` after `open`: chantier wrote nothing outside `.agents/changes/`, and never
   `chantier.yaml`.
7. Doc grep: no remaining "is the only configuration" without the amendment
   (`rg "only configuration"` returns the amended sentence in all eight places above).
