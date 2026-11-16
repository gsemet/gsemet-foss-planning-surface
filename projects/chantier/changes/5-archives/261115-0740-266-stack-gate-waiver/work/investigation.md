# CR-266 investigation: the stack's one long gate, the waiver per CR

Read in the worktree `C:\Users\gaeta\Projets\chantier.worktrees\batch-18-CR-266` (at CR-265's head
cd51c8b: `gate_from`, next-merge queue order and early push are in). CLI root `S` =
`skills/chantier/scripts/cli/src/chantier/`.

Facts that shape the work:

- `scenario/run_scenario.py` is one 6600-line file; a "unit" is a key of `UNITS` (line 73) naming
  cases (functions further down). Units `stack` = `stack_batch`, `ready_words`, `forge_stack_cli`
  (budget 320); `gates` = `rails ... gate_carry` (budget 400). Coverage bullets in
  `scenario/README.md` carry `(unit: ...)` / `(test: file::func)`, checked by
  `tests/test_scenario_coverage.py`. The README says edit the unit's budget literal with a case.
- Two row builders, not one: `status/views.py::_row` (STATUS.json, pane, dashboard) and
  `board/crs.py::_row` (the web board's own data, takes `events`). The web reads `board/crs.py`
  rows, not STATUS.json. Both need the `gate` object, from one shared function.
- `status/views.py::_row` and `batch_view` have no events today; `status/write.py::write_batch`
  already holds `_events_by_cr(folder)` and passes it to `cr_view`. `dashboard_view` calls `_row`
  with no events and no folder events read. `commands/batch_status.py::_cr_row` (the text) has no
  events either (it reads `Batch` record only; `cr_events(repo, batch, cr)` in `commands/crs.py`
  exists).
- `gate_lock.gate_state(repo, cr)` returns `"gate running"`, `"gate queued ..."` or None (reads slot
  files, live data). STATUS files are rewritten only when the record changes, so queued/running in
  STATUS.md/JSON is as of the last render: accept and say so in `status-layout.md`; `chantier
  status` text reads it live.
- The top of a waived stack: `stacks.top_cr` already takes the last open non-release, non-fix CR of
  a stack or series batch; `stacks.chain` gives the stack. A CR in `chain` whose `gate_waiver.scope
  == "stack"` is covered unless it is that top.

## Round 1: CLI core + pytest

Files (all under `S`):

- `core/records.py`: add `class GateWaiver(Record)` (`order: str`, `scope: str`, `note: str = ""`,
  `follow_up: str | None = None`) next to `OrderRecord`; `CrEntry.gate_waiver: GateWaiver | None =
  None` (after `stacked`). Withdrawal: `c.unset("gate_waiver")` (pattern: `_set_after`'s `unset`).
- `stacks.py`: add pure functions beside `top_cr`: `stack_top(d)` (top_cr restricted to chain, same
  rule, release excluded), `gate_cover(d, c) -> ("covered"|"validates"|None, ...)`: covered when
  `c.gate_waiver` and (scope `cr`, or scope `stack` and `c.id != stack_top(d).id`); validates when
  scope `stack`, c is the top: list `[x.id for x in chain(d) if x.gate_waiver and x is not c and
  scope stack]`. Both display and handback call these (one source).
- `declare/orders.py`: add `--follow-up` argument (pattern: `--fix-for`); extend `kind` help with
  `waive stack|<cr> [--follow-up]`.
- `commands/orders_apply.py`: `_waive(w)` and `"waive": _waive` in `HANDLERS`. Pattern: `_mode`
  (stack-mode check, refusal text) and `_approve`/`_note` (`_need_note`, `b.touch(c)`). `waive`
  must NOT be in `CR_ORDERS` (its cr is `stack` or a CR): resolve in `orders.py::_word`. Stack
  scope: refuse unless `b.record.mode == "stack"`; for each x in `chain(b.record)` with `x.kind not
  in {"release","fix"}` set `x.gate_waiver = GateWaiver(order=<O-k>, scope="stack", note=...)`.
  The order id: `_record_order` computes `oid = f"O-{len(orders)+1}"` AFTER `apply_order`; compute
  it once in `order()` (it is the same expression) and put it on `Word` (new field `order_id`) so
  the handler can write it. CR scope: `follow_up` required and must exist: reuse
  `lifecycle/backlog.py::backlog_folder(repo, slug)` (looks in inbox, `P1-P4`, `3-ready`; check what
  it raises) with `w.b.repo`; spec says `--follow-up <folder>` names the backlog folder: accept the
  slug or the path's last name. Withdrawal: `note.strip() == "-"` clears `gate_waiver` on the CR or
  on every chain CR with scope stack. CR already `ready`/`merged`: record stays (handback event
  carries it); refuse a waiver on a release/fix/ended CR. `--note` required (`_need_note`).
- `_add` in the same file: after `added = add_cr(...)`, if any open chain CR has
  `gate_waiver.scope == "stack"`, give `added` a copy of the waiver (same order id, scope, note).
  Stack mode only; placement on top is by `add_cr` order (verify in `commands/opening.py::add_cr`).
- `commands/orders.py::_check_args`: `waive` needs `args.cr` (`stack` or a CR id);
  `args.kind == "waive"` with `args.cr != "stack"` -> `args.cr = _cr_arg(args.cr)` (currently only
  `CR_ORDERS` or `note` are normalized, in `order()`); add `--follow-up` only valid with `waive`
  (pattern: the `--release` refusal). `_word`: `has_cr = kind in CR_ORDERS or (kind=="note" and cr
  != "-") or (kind=="waive" and cr != "stack")`. `_record_order`: `applied` stays True for waive
  (CLI applied; the Foreman ends it with `order done`); add `follow_up` to `OrderRecord`
  (optional field, like `fix_for`) and to the written order so `status`' order lines can show it.
  The output line `[chief-of-staff->foreman] order O-k: waive ...` already formats kind/cr/note.
- `commands/driver_checks.py::handback_refusals` and `driver.py::handback`: when the CR is covered
  (`gate_cover`), skip `_gate_missing`/`gate_passed` (like `no_gate is not None`), keep head, clean,
  pushed, VERIFIED. Return a waiver description so `handback` logs
  `gate_waiver=<order id>`, `gate_waiver_scope`, `validated_by`/`follow_up` on the `handback`
  event (pattern: `**({"gate_from": carried} ...)`) and prints `long gate waived (O-k): validated
  by CR-<top>'s gate` / `follow-up <folder>` in the `gate` string of `handback` (pattern: the
  `carried` branch). `handback_refusals` currently returns `carried or None` (a str): change it to
  return a small result (a dataclass or tuple) rather than overloading the string. The top of a
  waived stack is NOT covered: unchanged path (gate or carried pass). Check the `--no-gate` +
  waiver combination: no_gate wins (exempt), nothing to refuse.
- `commands/facts.py::cr_facts`/`_gate_lines`: print one `gate:` line, only for `c.kind not in
  {"release"}`: covered -> `gate: waived (O-k, scope): run no long gate; validated by CR-<top>` or
  `follow-up <folder>`; the top -> `gate: this CR's long gate validates the stack (CR-a, CR-b, ...)`.
  Keep today's checklist but for a covered CR drop the "[ ] long gate passed" line or mark it
  waived. `take` and `handoff` and `round_` all go through `cr_facts`, so one edit.
- Not to forget: `status/views.py::_steps` is Round 2. `rails.py` needs no change (`rails.py` says
  what it refuses; the refusal lives in `orders_apply.py`/`driver_checks.py` as today).

Existing tests to extend: `tests/test_rail_refusals.py` (order refusals style), `test_gate_refusals.py`,
`test_gate_carry.py` (monkeypatched git; pattern for `handback_refusals`), `batch_helpers.open_batch`
(`args=("--mode", "stack")`) and `write_record`/`record` to prepare states. New files (spec: 400
lines/file, 50/function): `tests/test_gate_waiver_orders.py` (waive stack refused outside stack mode
parametrized over modes; `waive <cr>` refused without `--follow-up`, with a missing folder, with an
empty note, on a release CR) and `tests/test_gate_object.py` (Round 2, the `gate` state per source:
pure function over a prepared `BatchRecord` plus a list of `EventRecord`s; the queued/running case
monkeypatches `gate_lock.gate_state`).

## Round 2: display, CLI and STATUS

- New module `status/gate_view.py` (or in `status/words.py`, 144 lines): `gate_object(repo, d, c,
  events) -> dict` returning the spec's shape; sources in the spec's order: `waived`/`validated_by`
  from `stacks.gate_cover`; `carried` from the last `handback` event's `gate_from`; `exempt` from
  `no_gate`; `passed`/`failed` from the last `gate` events at `c.head` (reuse `commands/crs.py`
  `gate_passed`/`last_gate_pass`; check they take `EventRecord` lists, they do in `driver_checks`);
  `queued`/`running` from `gate_lock.gate_state` (import it lazily: `status/` sits below
  `commands/`; maybe pass the live state in or import in `commands/batch_status.py` and inject). A
  layering check exists (test_code_targets.py): run it before choosing where `gate_state` is
  called.
  `validated_by.pr` = the top CR's `pr`. `validates` = ids covered by the top.
- `status/views.py`: `_row(repo, d, c, start)` gains `events` (default `[]`) and `"gate"`;
  `cr_view` adds `"gate"`; `batch_view(repo, d, folder)` needs the events:
  pass `events_by_cr` from `write_batch` (already computed) and from `dashboard_view` (read
  `folder/events.jsonl` per batch with `read_events`). `_step_entries`: handback event with
  `gate_waiver` -> `("Long gate", f"waived (O-k): validated by CR-k (#n)", "")` or `follow-up
  <folder>`; `gate_from` -> `("Long gate", "carried from <sha7>", "")`; the existing
  `waived: <reason>` becomes `exempt: <reason>` (`views.py` line 97). Check the scenario/pytest
  strings that match `waived: ` (grep `waived:` in `scenario/run_scenario.py`, `evals/`).
  `SCHEMA = 3`: adding a field is additive; keep 3 (the pane's schema check is on the number).
- `status/markdown.py::_rows_markdown`: add the "Long gate" column (words in the spec) from
  `r["gate"]`; one helper `gate_word(gate) -> str` shared with `batch_status.py` (put it in
  `status/words.py`). `cr_markdown`: steps already print `name verdict: note`, so the step text
  change in `_step_entries` is enough.
- `commands/batch_status.py::_cr_row`: append ` | gate <word>` for a non-merged CR (text, same
  words); needs events: `cr_events(repo, batch, c.id)` is one read per CR (the file is read each
  time: read `read_events(folder)` once in `status()` and group, as `status/write.py` does).
  `_order_lines`: show `--follow-up` for a waive order (the `o.note[:40]` cut would hide it).
- The paused report ("What the batch did not prove"): `commands/summary.py`/`summaries/`? The text
  lives in `references/status-layout.md` (line 112) and is produced by the Chief of Staff, not the
  CLI (verify with `grep -rn "did not prove" S`); if CLI-produced, add each waived CR with validator
  or follow-up there, else cards only (Round 5).
- Tests: `tests/test_gate_object.py` as above; a `_rows_markdown` string test for each of the nine
  words (small, parametrized).

## Round 3: the pane (`just mod`)

- `types/index.d.ts`: `ChantierGate` type (state union, head, waiver, validated_by, validates);
  `ChantierRow.gate?: ChantierGate` and `ChantierSheet.gate?: ChantierGate`. Optional keeps old
  STATUS.json files readable.
- `hooks/register.tsx`: `COLUMNS` (line 837) gets `'Long gate'`; `Crs` row map (line 843) adds a
  cell from a new pure `gateWord(g)` (same nine words as `status/words.py`); `Pasts` rows keep 5
  columns (no gate for merged), so `Table` must tolerate different widths (look at `Table` at ~760
  and the `COLUMNS` users). CR page: line 917 area, add a "Long gate: <word>" `Text` under the
  label, and the steps table already shows the changed step text. Keep `register.tsx` under its
  size limits (1040 lines today: check lint size rule; split `gateWord` into a new `hooks/` module
  only if the build allows extra files, otherwise inline).
- `hooks/register.test.tsx` (1063 lines, patterns around `readiness`): extend with one table test
  per word and a CR page test. `just mod` must pass.
- Screenshot from a real session: cannot be taken by an agent; Known gaps line "no screenshot of
  the pane from a real session" (AGENTS.md rule).

## Round 4: web board

- `board/crs.py::_row`: add `"gate": gate_object(...)` (events already passed in); `board/state.py`
  needs nothing else. Check `board/web/js/model/events.js` `EVENT_KINDS` (events.py `EVENT_KINDS`
  in `board/state.py` ~line 70) does not need `handback` waiver keys: add `gate_waiver`,
  `gate_from`, `no_gate` to `EVENT_KEYS` if the journal should show them (optional).
- `board/web/js/model/semantics.js`: a `gateWord(c)` and `isCovered(c)` helper next to `vstate`.
- `views/batch-pr-card.js` (`prCard`, `body`): a line `t('gate.<state>')` in the card's second
  row for a CR with a gate state other than `none`, and for `waived` an `<a href=validated_by.pr>`
  link (use `safeUrl` as `earlierCard` does; `prNumber` helper exists). `views/batch.js` /
  CR panel (`panel/head.js`): same word. `kanban-cards.js` is the other CR card: decide in Round 4
  whether it shows it (spec names PR card, batch view, CR panel only).
- `i18n/en.js` and `fr.js` (and write variants not needed): keys `gate.passed`, `gate.carried`,
  `gate.queued`, `gate.running`, `gate.failed`, `gate.waived`, `gate.validates`, `gate.exempt`;
  there is a parity test in `tests/test_board.py`? (check: `fr.js` has fewer lines; keep keys equal).
- CSS: one small class in `css/views/batch-prs.css` (the PR cards).
- Docs screenshots: `just docs-screenshots` (needs the board running with a waived stack record:
  the scenario or a fixture). One capture in the PR body: the Chief of Staff or the user takes it;
  an agent can run `docs-screenshots` only if its tooling is installed here: check `justfile`.

## Round 5: cards, eval kit, scenario

Cards (agent files unchanged; they are in `skills/chantier/references/`):

- `chief-of-staff.md`: the go of a stack batch offers the choice and records `order waive stack
  --note ...` (find the go section; grep "go" near the batch plan); the one-CR waiver rule with
  `file` first and `--follow-up`; batch plan gate count (line 808-811: "The gates") excludes
  covered CRs and counts the top; the stack's merge offer names the validating CR and its gate
  state (grep "merge offer").
- `foreman.md` (lines 55-68: the hand-back check): add the waived branch checked against the
  recorded order (`status` shows it, the ask carries `long gate waived: validated by CR-k` or
  `follow-up <folder>`); nothing in a Driver's brief beyond `take` output.
- `driver.md` (lines 171-184, 356-368): a `gate: waived` line in `take`/`handoff` means no gate
  and no `--no-gate`; the top runs it; a fix found by the top's gate goes on the top PR or above.
- `concepts.md` (lines 281-308 long gate; "Order, ask, hand-back"): what a waiver is, who records it.
- `status-layout.md` (lines 89, 112-113): column, step, report line. `routing.md`: only if the ask
  or hand-back line text changes (it does: `long gate waived ...`): grep `no long gate` there.
- `evals/kit/audit.py` line 391: `waived = ... (e.get("no_gate") or e.get("gate_from") or
  e.get("gate_waiver"))`; the message at 398; `evals/SCORECARD.md` C7 row (line 33, one long
  line) and `evals/claude-planted/RUNBOOK.md` line 98 say the same.

Scenario (`scenario/run_scenario.py`, `scenario/README.md`):

- `stack` unit: extend `stack_batch` (line ~3861) or `ready_words` (~5307, it already reads the
  STATUS files in a stack): `order waive stack --note ...` -> lower CR hands back ready with no
  gate (`handback_proofs`-style helper `gate_passed(evs, head)` at ~2669 reads events), top refused
  without gate, `take` prints the two `gate:` lines, `status`/STATUS.md/STATUS.json show `waived ->
  CR-k` and `validates ...`, `order add` moves the validation, `--note -` restores the need. Needs
  a 3-CR stack in a case that already has one: confirm in `stack_batch`; else the new case joins
  the `stack` list (UNITS line 75), whose budget (320 s, measured 259-314 s) must be raised by
  the case's measured time (edit the literal; README lines 43-45 hold the timing table).
- `gates` unit: after `gate_carry` (~3726), assert `STATUS.md` of the carried CR shows `carried
  from <sha7>` (one `check`).
- README coverage: extend the bullet at lines 129-136 (stack/ready words) and 189-194 (gates)
  with the new cases, `(unit: stack)` / `(unit: gates)` and `(test: test_gate_waiver_orders.py::...)`
  markers; the structure test fails if a named function does not exist.
- Replace any existing scenario check matching `waived: <reason>` (now `exempt:`): grep first.

## Evidence plan

1. `just check` on this machine (Windows); Linux/macOS by CI.
2. `just mod` after Round 3 and at the head.
3. `just scenario` full (both forges) at the PR head: the CR's long gate (the CLI, cards and
   scenario change); Round 1-4 may run `uv run --locked python scenario/run_scenario.py --unit
   stack --unit gates` for a quicker loop.
4. `evals/kit/audit.py` C7 run once on the scenario's record of the waived stack (need the
   scenario's `--keep` workspace; capture its output for the PR body).
5. Pane screenshot (user, real session, captioned with the 7-character head); until then Known gap.
6. Web board: a capture of a waived stack in the PR body and `just docs-screenshots` retake;
   Chief of Staff or user runs them (needs a real browser).
7. Write `evidence/` notes: command, exit code, head SHA per item.

## Risks and open points for the grill-free Coder

- `handback_refusals` signature change touches `driver.py` only (one caller): safe.
- `OrderRecord` gains `follow_up` (extra field): `Record` accepts extras? Check `Record` config in
  `core/records.py` top (lines 1-58) before relying on it.
- `status/` importing `gate_lock` may trip the layering test (`test_code_targets.py`): inject the
  live queue state instead (pass a dict `cr -> state` from the command layer).
- `dashboard_view` reading every batch's events adds IO per render: read only for `active` CRs.
