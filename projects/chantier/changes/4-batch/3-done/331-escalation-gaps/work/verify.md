# Verification of CR-331 escalation-gaps

Head: 2b95cfe265a5c8034bd4479d315f352dcd1f245d

Verdict: VERIFIED (round 6, see the end; earlier sections keep their own SHAs)

Method: all commands run in the CR worktree at the head above, `uv run --no-sync --project .`, over scratch
configurations (removed at the end). Browser: Google Chrome 157 (headless, driven through the DevTools
protocol from Node 24; the chrome MCP tools were not available to me). Raw probe log:
`verifier/copilot-take-probe.log`.

## 1. Defaults, no user file (14004edb)
`chantier playbook` (claude): coder, conflict-resolver and debugger lines carry
`escalation=opus (claude-opus-5-5, Claude Opus 5.5)`; last line
`escalate: coder opus (...); conflict-resolver opus (...); debugger opus (...)`. Roles without one
(inspector, cr-driver...) print no `escalation=`. PASS.
`playbook --host copilot`: `escalate: coder claude-opus-5.5 (claude-opus-5.5, Claude Opus 5.5) (generic); conflict-resolver ... (generic); debugger ... (generic)`. PASS.

## 2. User layer, refusals (14004edb)
- claude, `escalation: sonnet` on coder: `coder: ... escalation=sonnet (claude-sonnet-5-5, Claude Sonnet 5.5) [surface project]`; `escalate:` names it; plain `default` gives back `escalation=opus (...)`. PASS.
- `escalation` on inspector: `role "inspector": "escalation" is set only on a role whose shipped defaults carry one: coder, conflict-resolver, debugger`. PASS.
- quoted `"default"`: `"default" resets the value: write it plain, default; ...`. PASS.
- unknown model: `role "coder": model "nosuchmodel" is unknown on Claude Code; known: ...`. PASS.
- copilot, `coder escalation: gpt-6.1-sol`: `escalation=gpt-6.1-sol (gpt-6.1-sol, GPT-6.1 Sol) (generic) [surface project]`, accepted. PASS.
- copilot, debugger with the user's own `agent: myagent`, no user escalation: debugger line has no `escalation=` and `escalate:` omits debugger (no generic start in place of the user's agent). PASS.
- copilot, same role with a user `escalation: claude-opus-5.5`: refused, `role "debugger": Copilot cannot start a named agent with a model (hosts/copilot.md, "Models at an agent's start"): remove "escalation" for debugger under hosts.copilot.roles, or name the model in your agent's own file`, exit 2. PASS.

## 3. Tests (14004edb)
`python -m pytest tests/test_playbook_escalation.py tests/test_playbook_config.py tests/test_playbook_layers.py tests/test_playbook_edit.py -q` -> `45 passed`. CI at the head green (given; scenario ubuntu included). PASS.

## 4. Board Configuration page, real browser (14004edb)
Scratch planning surface (git repo, one project `demo`, its `.repo` clone), `chantier board --host 127.0.0.1 --port 8799` run from the worktree's code, its own key; not the live board.
Driven in Chrome (headless): opened `?p=demo&v=config`.
- Table headers: Role, Agent, Model, Escalation (Escalade, the browser's locale is French), Start.
- Rows with an escalation select: exactly coder, conflict-resolver, debugger on both hosts; every other row (cr-driver, inspector, verifier, ...) has an empty Escalation cell. The page names no role in its code.
- Seeded `escalation: sonnet` on claude coder: cell shows `sonnet`, `inherited: claude-opus-5-5 (defaults)`, `in effect: claude-sonnet-5-5 (surface project)`.
- Copilot coder cell: Copilot catalog in the select, `generic agent: the escalation model is given at the start`.
- Edit through the real select + Save: claude debugger -> claude-haiku-5-5 (answer `wrote projects/demo/chantier.yaml`, `applies at the next batch`); claude coder back to the inherited choice (key removed from the file); copilot coder -> gpt-6.1-sol. The surface file then held exactly `hosts.claude.roles.debugger.escalation: claude-haiku-5-5` and `hosts.copilot.roles.coder.escalation: gpt-6.1-sol`.
- Screenshots (opened and looked at; made-up paths only, no username or home folder visible): `verifier/evidence/config-escalation-claude.png`, `verifier/evidence/config-escalation-copilot.png`. PASS. Not covered: the Copilot cell of a role with the user's own agent in the browser (covered by the CLI refusal above and the test).

## 5. Copilot generic start of an escalated role (14004edb): FAIL
The spec (section 1, Copilot bullets; Decisions, escal-Q4) says the escalated role starts as a generic agent with the printed contract lines (`start: generic`, the caller's tools, "the printed contract lines"); `concepts.md` "Starting an agent" and `hosts/copilot.md` row "Start a generic agent" require the printed contract lines in the prompt.
Probe (real `open` then `take` of a Copilot batch, no user file, `verifier/copilot-take-probe.log`):
```
take lines with team:/contract/escalat:        (none)
record escalation coder: {'id': 'claude-opus-5.5', ..., 'mode': 'generic'}
coder: agent=chantier-coder model=(its file's) escalation=claude-opus-5.5 (...) (generic)
```
`plugin_files.contract_lines` prints a role's contract only when `resolved.roles[role].start == "generic"` (a configured model); the escalation's `mode: generic` is never read. In-process, `worker_prompt_lines("copilot", ..., resolved)` with a coder escalation mode generic returns 24 lines, none a contract. So when a Copilot Driver escalates the coder (debugger, conflict-resolver), no printed contract lines exist for the generic agent; the Driver would start a generic agent with no contract, or invent it. The CR did not change `plugin_files.contract_lines`/`worker_prompt_lines` for escalation. No test covers it. A real Copilot session was not run (no host call spent; the generic start itself is proved in CR-296, but this is the part the CR adds).

## 6. PR description (14004edb)
Sections render; Summary, Deliverables and Changes match the diff. Known gaps names the UNVERIFIED bullet; it must be updated once this is fixed (and name the Copilot contract gap if left). Review box `approved at 253fca6` matches the log note `r4 inspector approved at 253fca6ddb18...` and `committed as 14004edb`. Test plan `Local gates at 253fca6` predates the head (the later commit only touches `scenario/run_scenario.py`). No image attached. Not an independent failure.


# Round 5 (second verification), head 9c9e99d3ec161c79c3ee2aad19ea3951a0d82d09

Move 14004edb..9c9e99d3: rebase onto origin/main 75a748e8 plus one commit.
`git range-diff a111e182..14004ed 75a748e8..HEAD~1`: the CR's two commits are unchanged (one `!` only in
the context of driver.md's `writes:` line, which main changed; the other `=`). Sections 1-4 and 6 above
are carried from 14004edb: the move touched only `plugin_files.contract_lines`, its docstrings and one test;
the playbook/escalation/board-config code is the CR's patch, unchanged. Board Escalation column
carried from 14004edb (the CR's board files are unchanged by the range-diff; the base's board changes
are the batch-navigator/styling commits of main, not the Configuration page's escalation cell; no browser rerun).

## 5 again. Copilot generic start of an escalated role (9c9e99d3): FAIL
Probe: `verifier/probe_take.py.txt` (a pytest test run over the CLI's own fixtures, a real `open`, `foreman set`,
`take`, `round`, `handoff` of a Copilot batch; log `verifier/copilot-take-probe-9c9e99d.log`).
- No user file (the shipped default escalation, coder -> claude-opus-5.5, mode generic):
  `record escalation coder: {'id': 'claude-opus-5.5', ..., 'mode': 'generic'}`; take/round/handoff each:
  no `team:` coder line, no `escalate:`-bearing team line, `heading count: 0` (no contract lines).
- User file `hosts.copilot.roles.coder.escalation: gpt-6.1-sol`: `team: coder escalation=gpt-6.1-sol (...) (generic) [repository]`,
  `heading count: 2` at take, 1 at round and handoff. Works.
Cause: `contract_lines(role, text, d.playbook)` reads `resolved["roles"][role]["escalation"]`, which exists only when
a user layer configured the role; the batch's frozen escalation map (`record.escalation`, from the shipped
defaults) is not passed to `worker_prompt_lines`/`chief_prompt_lines`/driver_prompt. The new unit test feeds a
hand-built `{"roles": {"coder": {"escalation": {"mode": "generic"}}}}`, a shape the real flow does not produce for the default case.
Net: the default Copilot batch (no user file, the spec's main case) still prints no contract for the escalated role.

## Verdict: NOT VERIFIED (head 9c9e99d3ec161c79c3ee2aad19ea3951a0d82d09)


# Round 6 (third verification), head 2b95cfe265a5c8034bd4479d315f352dcd1f245d

Move 9c9e99d..2b95cfe: plugin_files.py, driver_prompt.py, commands/facts.py, commands/rules.py, two test files. Sections 1-4 and 6
carried from 14004edb/9c9e99d (the move only passes the frozen record.escalation into contract_lines; playbook/board code untouched).

## 5 again. Copilot generic start of an escalated role (2b95cfe): PASS
Probe `verifier/probe_take.py.txt`, real open/foreman set/take/round/handoff of a Copilot batch, logs
`verifier/copilot-take-probe-2b95cfe-nouser.log` and `-user.log`.
- No user file: record escalation coder `mode: generic`; take: heading count 6 (coder, conflict-resolver, debugger contracts, printed twice at take), round 3, handoff 3. (Was 0 at 9c9e99d.)
- User file `hosts.copilot.roles.coder.escalation: gpt-6.1-sol`: `team: coder escalation=gpt-6.1-sol (...) (generic) [repository]`, contracts printed (6 / 3 / 3).
Claude host: `chantier playbook` prints 0 generic contract headings (no regression).
Tests at the head: `python -m pytest tests -q` -> `460 passed`. CI all 5 green (given).
PR description, Known gaps: judged at 14004edb; carried (not re-read against the new head; the move changes no deliverable beyond the contract lines).
Known gap for the board's browser column stays UNVERIFIED per the brief; the browser run was at 14004edb and is carried.

## Verdict: VERIFIED (head 2b95cfe265a5c8034bd4479d315f352dcd1f245d)
