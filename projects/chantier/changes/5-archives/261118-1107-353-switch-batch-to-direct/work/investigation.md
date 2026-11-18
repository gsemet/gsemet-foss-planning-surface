# CR-353 investigation: switch a Foreman batch to direct mode

Paths are under `skills/chantier/scripts/cli/src/chantier/` (CLI) unless noted. Read only; nothing run
beyond `rules`.

## Project rules that touch the work

`AGENTS.md`: `just check` before handback, `just eval-dry-run` (change under CLI `src/`), long gate
`just scenario (ubuntu-latest)` green before the PR leaves draft, Windows `chantier gate` for the CR on
top; tests few, parametrized, fast (`just test` budget); agent files untouched (cards hold the
contract); no `epoch` word in user-facing text; repository text in English. `CONTRIBUTING.md` and
`scenario/README.md` were not read in full: the Driver reads them for the scenario step's style.

## 1. The flip: `commands/seat.py`, `_transcript` (lines 55-79)

Today:
- l.58-65: `foreman_transcript` conflict check (reset to `None` by `_claim`, l.50, so a new number is free).
- l.66-70: `foreman_transcript` set; `foreman_transcripts` and `foreman_claims` appended **only if
  the transcript was never seen** (`not in foreman_transcripts`).
- l.71-77: the one flip, `steering == "direct"` and `chief_transcript` set and `args.value !=
  chief_transcript` -> `steering = "foreman"`, `b.log("steering", ...)`.
- l.78-79: `foreman-transcript` event; output `["transcript <uuid>"]`.

Change: an `elif` after l.71-77: `steering == "foreman"` and `chief_transcript` and `args.value ==
chief_transcript` -> `steering = "direct"`, `b.log("steering", None, steering="direct",
transcript=args.value)` before the `foreman-transcript` log; append the extra output line (no word
"epoch"). Use `elif`/else-exclusive: after the flip the first condition would be false anyway
(`value == chief`), but keep them exclusive for readability. Both conditions read `steering` at call
time, nothing else to touch for the words (spec section 1 list holds; I did not re-verify each reader).
`own_transcript` (l.82) and `_record_transcript`/`_set_chief` (l.113-130) are unchanged.
`opening.py` l.288 `chief = own_transcript(host)` records `chief_transcript` at `open` (it is
required for `--direct`, l.291; for a Foreman batch it may be `None` on an unknown id, which is the
"no transcript" cell: no flip, no line, no event).

Edge to note in the PR: a batch whose Foreman is legitimately the same transcript as the recorded
Chief of Staff (Remote Control reuse) would now flip on its own claim. The card pre-check (Q11) is
the only guard; the spec accepts it.

## 2. Single-window-per-transcript assumptions to change

The root fact: the `if args.value not in foreman_transcripts` guard (seat.py l.67) gates **both** the
transcript list and the claims. After direct -> Foreman -> direct with the same Chief transcript:
`foreman_transcripts == [chief, foreman]`, `foreman_claims == [chief, foreman]`, so the third claim
records nothing.

Recommended smallest shape: keep `foreman_transcripts` **unique** (it is a set-like list read by many
callers, see risks) and make `foreman_claims` the log of stints:
- `seat.py` l.67-70: split the guard. `foreman_transcripts` append stays `not in`; the claim is
  appended when `foreman_claims` is empty or `foreman_claims[-1].transcript != args.value`. An old
  record with transcripts but no claims (the `[]` default, `opening_record.py` l.75) then gets a first
  claim on its next claim: harmless (cost already falls back, `steering_window` returns
  `(created, "")` when the uuid is not in `names`).
- "Current steering session" (last claim) replaces "last of `foreman_transcripts`":
  1. `rails.py` `running`, l.79 `sessions = d.foreman_transcripts or ...` and l.90-92 passes it to
     `transcript_endings`; `costs/endings.py` `transcript_endings`, l.51-55: `mine if i ==
     len(sessions) - 1 else others` marks the current Foreman by list position. Needs a `current`
     (the last claim's transcript, falling back to `sessions[-1]` when there are no claims) and
     `ending ... (mine if session == current else others)`. Subagent loop (l.56-63) already runs
     under every session, replaced ones included, and `_missing` (l.64) too: Q10 holds without change.
     Also `own` (chief sessions) already skips a Chief's main file (l.53); the live trap is only the
     direct -> Foreman -> direct case where `sessions[-1]` is the stale Foreman.
  2. The docstrings: `rails.running` (l.56-69) and `rails.check_idle` (l.145-155), `endings.py` l.38.
  3. `rails.py` l.81 (Copilot `idle_seconds`) takes every session: unchanged.
- Windows: `commands/cost/pricing.py` `steering_window` (l.68-79) uses `names.index(uuid)`, so only the
  first claim of a transcript; it returns one `(since, until)`; `since` is the claim's `since` for a
  Chief transcript (`uuid in chief_sessions(d)`) else `d.created`. Change to return a **list** of
  windows (successor `steering_windows`): for each index `i` with `names[i] == uuid`, since =
  claim `since` (Chief) or, for a Foreman, `created` for its first stint and the claim's `since` for
  later stints (else overlapping windows double count); until = next claim's `since` or `""`. No claim
  for the uuid: `[(created, "")]` as today. One claim per transcript gives one window equal to
  today's. Callers:
  - `cost/sessions.py` `_chief_session` l.105-117: `window = steering_window(...)`, then
    `session_costs(path, *window, scope=Scope(..., window))` summed as `steered`.
  - `cost/sessions.py` `cost_rows` l.252-271: `since, until = steering_window(d, uuid)` then one
    `session_costs(transcript_path, since, until, scope=Scope(..., steering=(since, until)))`.
  - `cost/sessions.py` l.34 `claimed_transcripts` (a name list, duplicates fine with `in`).
- Where `usage` takes the window: `costs/sessions.py` `session_costs` (l.36-67) takes one `since`,
  `until` and `Scope.steering` (l.33); `costs/transcripts.py` `usage` (l.333-375): `start, end =
  _when(since/until)` (l.354), `inside` (l.373) is a single range test, `_place(scan, split, (start,
  end))` (l.302-316, uses `any(window)` only to skip untimed calls), `Reading.steering` (l.330) is one
  tuple feeding `in_steering` (l.359-365). Two ways, pick the smaller:
  a. **Teach `usage` and `Scope`/`Reading` a list of windows** (`inside` = any range contains `when`;
     `in_steering` = any steering range; `_place`'s `any(window)` becomes "any window bounded").
     One scan per transcript, no row merging, exact. Touches `costs/transcripts.py`,
     `costs/sessions.py`, `cost/sessions.py`, `cost/pricing.py`.
  b. Call `session_costs` per window and merge rows by agent. Smaller in `usage` but the row shape
     (usage fields, nested `grill`, `last_context`, `compactions`, `untimed`) must be summed field by
     field, and `allow_empty` is needed per window. Not recommended.
  I recommend (a). `_absorb` (`cost/sessions.py` l.120-146) sums `since` rows and `steered` rows
  already, so it needs no change once `steered` covers all windows; `main = since[0]` is the
  whole-since-opening read, one per transcript.
- `evals/kit/audit.py` l.455-470: `since = {c["transcript"]: c["since"] ...}` keeps only the **last**
  claim per transcript; the `a.since` window opens at one claim. This is the audit of an eval's
  real batches, under `evals/kit/`, so a change to it triggers `just eval-dry-run` anyway. Not
  required by the spec; note it in the PR as the one other single-window reader (a batch with a
  repeated claim would audit from the last stint). `evals/kit/dry_run.py` l.1008 builds a single claim.
- Not changed by design (Q8): `chief_outside` (l.219-233), `_chief_lines`.
- `commands/cost/command.py` l.139 and `foreman_uuid` (sessions.py l.38-43) use the unique list:
  unchanged if `foreman_transcripts` stays unique. If it were allowed to repeat, `cost_rows` (loop over
  `uuids`, l.252), `activity.py` l.55/119, `driver.py` l.196, `batch_status.py` l.98/177,
  `closing.py` l.39, `close_archive.py` l.98, `board/costs.py` l.30 would all double count or
  double list; that is why uniqueness is the smaller change.

## 3. Other code and files

- Cards, docs, host reference: as in the spec (sections 3-7); text only, no code. `chief-of-staff.md`
  has lines to move after edits (the spec cites approximate lines: 776, 1377, 1410, 1555-1565).
- `agents/` and `com.github.copilot/agents/`: not touched.
- No `hooks/` or `types/` change, so no `just mod`. No `STATUS.json` field changes, so no
  screenshot is owed.

## 4. Existing tests and scenario steps to extend

- `tests/test_cli_runs.py` `test_a_direct_batch_is_recorded_shown_and_queues_added_work` (l.191-222)
  is the model for env (`CHANTIER_HOST`, `CLAUDE_CODE_SESSION_ID`), `open --direct`, `status` first
  line (` steering direct `) and `take` skeleton (`Steering: the Chief of Staff`, l.222). The new test
  is a Foreman-batch sibling next to `test_a_foreman_batch_takes_added_work...` (l.225): open with
  `CLAUDE_CODE_SESSION_ID=uuid-chief` on a Foreman batch, `foreman set`/`transcript` n°1 as another
  transcript, then n°2 with `uuid-chief`. Parametrize over the cells (Claude Code, Copilot via
  `CHANTIER_HOST=copilot` + `COPILOT_AGENT_SESSION_ID`, no transcript recorded). Mind
  `MAX_OUTPUT_LINES = 10` (l.24) for the added output line.
- `tests/test_costs.py` (`test_in_the_steering_window_only_a_write_or_a_spec_writer_is_grill`, l.190)
  and `tests/test_cost_receipt.py` (helpers `row`, `chief`, `record`, imports `_Chief`) exist for
  steering reading; the cost unit test goes next to the first (it already builds transcripts), plus a
  pure test of `steering_windows` on a `BatchRecord` (cheap, no files): repeated claims -> each
  window; one claim per transcript -> as before.
- `tests/test_transcript_end.py` (`test_transcript_state`, l.76) covers `transcript_state` only; the
  `close` current-Foreman logic is covered in the scenario (below), so a unit test of
  `transcript_endings(current=...)` is optional.
- `scenario/run_scenario.py`, unit `direct_batch`: the "a Foreman takes the batch over" step is at
  l.2411-2456 (`chief`, `t0`, `t1`, `edit(...)`, `foreman_file` seeded at l.2426-2428). After l.2435's
  checks, claim n°3: `w.chantier("foreman", "set", "local_chief_next", "--epoch", 3)` then
  `foreman transcript uuid-chief --epoch 3`; assert `foreman_claims` transcripts `["uuid-chief",
  "uuid-foreman", "uuid-chief"]`, `steering == "direct"`, a second `steering` event, `status --refresh
  --epoch 2` exit 3, `status`/`STATUS.md` direct; `cost` seeding one call in each Chief window and one
  in the Foreman window (there is `msg`/`at(n)` helpers at l.2428; windows are `t1` and a new stamp);
  the "outside the budget" line holds no second-stint call. The scenario already asserts the labels
  at l.2440-2445 and `by cr` at l.2446-2450: they must still pass (the Chief now being direct again,
  `_transcripts` wording at cost/sessions.py l.236-239 changes to the steering wording).
  `close` replaced-Foreman check: reuse the `closes`/`refused`/`age_sessions` helpers in the close
  unit around l.2966-3040 (case 5, l.3010-3037: `two = {"foreman_transcripts": [...]}`): add the
  round-trip case there (`foreman_transcripts: [uuid-chief, uuid-foreman]`, `foreman_claims` three
  entries, seeded `uuid-foreman.jsonl` ending on a tool call -> listed apart, not a cause).
  The "Foreman-opened batch switched to direct with a CR working" part is a new small block: the
  `Foreman(w, epoch=1)` helper (used at l.2467) opens/claims; seed the Driver file under
  `uuid-foreman`'s `subagents/` as at l.2396-2404 (`driver`, `runs`, `clear_agents`) to show
  `close` (no `--yes`) listing the Driver as running then ended; then `agents set <cr> - --epoch 2`,
  `handoff`, `take --note "resume: switch to direct mode" --epoch 2`; assert branch/worktree/PR kept
  and board state `steering == direct` (`board/state.py`).
- `evals/kit/dry_run.py` must stay green (`just eval-dry-run`); l.1008 is its single claim record.

## 5. Risks

- `foreman_transcripts` must stay unique (listed above); every list consumer was grepped.
- A Foreman's second stint window must not overlap its first (since = claim, not `created`).
- `close` current: records with claims absent (old batches, scenario `edit(...)`) must fall back to
  `foreman_transcripts[-1]`; keep that fallback in one helper (e.g. `current_steering(d)` in
  `core/records.py` next to `chief_sessions`, l.304) used by `rails.running`.
- The new flip depends on `chief_transcript`; `seat take` refreshes it on all non-closed batches
  (seat.py l.113-121), so a stale value is the Q11 pre-check's job.
- Exit-code and output length: the added line must keep `foreman transcript`'s output within the
  10-line cap (it prints two lines).
- "Never edit a version by hand" and no changelog: nothing to bump.
- Old-value search for the values the change alters: none is renumbered; the removed phrases are in
  the cards and docs (spec Evidence 4 greps: `never becomes direct`, `never switches to direct mode`,
  `never switches back to direct mode`, `A Foreman batch does not switch to direct`). Run them with
  `rg -U` over `skills/`, `docs/`, `README.md`, `scenario/`, `evals/` before the final check.

## 6. Questions only the user can answer

None for the CLI. One observation for the Driver's PR note: whether to also fix `evals/kit/audit.py`
l.458 (last claim wins) in this CR; I suggest a one-line note, not a change.

## 7. Evidence plan

Kind: CLI behaviour change + card/doc text. No UI pixel (no board pane field changes), so no
screenshot owed.

| What shows | Before | After | Technique |
| --- | --- | --- | --- |
| `foreman transcript` flips Foreman -> direct | claim by `uuid-chief` leaves `steering: foreman`, no event | `batch.json` `steering: direct`, `steering` event with `direct`, extra output line, `status` first line ` steering direct `, old number exit 3, `take` skeleton "Steering: the Chief of Staff" | the parametrized in-process test (`just test`); capture `pytest -k <name> -v` output to `evidence/` |
| Round trip prices right | third claim records nothing; second Chief stint lands on the "outside the budget" line | claims `[chief, foreman, chief]`, each window priced, none outside | scenario `direct_batch` output of `cost` (log lines), cost unit test run |
| `close` not blocked by a replaced Foreman; old Driver state shown | replaced Foreman blocks when it reads running | listed apart; Driver running then ended | scenario `close` check output |
| Restart path accepted after the switch | n/a | `take ... resume: switch to direct mode` accepted, branch/worktree/PR kept, queued CR queued, board `steering` direct | scenario block; scenario log |
| Cards/docs | phrases present | phrases gone, new bullets present | `rg -U` lines in `evidence/` (spec Evidence 4), head SHA noted |
| Gates | | `just check`, `just eval-dry-run` green; `just scenario` (ubuntu CI) green at the head; Windows `chantier gate` for the CR on top | gate logs under `work/gates/` |

Capture scenario output with `just scenario` (or the scenario unit alone if `scenario/README.md` names
a per-unit run) into a `*.log` in `work/gates/`, and quote the matching `check(...)` lines into
`evidence/`. Cannot be shown: the live Claude Desktop stop of a silent Foreman
(`mcp__ccd_session_mgmt__stop_session`), the Remote Control cell, and a real Foreman answering
`switch to direct mode`; the cards are text only and marked unproved, as the spec says. The Copilot
`cost` stays "not measured on this host".
