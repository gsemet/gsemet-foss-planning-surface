# CR-133 investigation

Replay transcript: `work/replay.txt` (sections A to L, worktree CLI 0.6.0, throwaway repo with a bare origin, Windows).

## Findings replayed

| # | Finding | Still holds | Command, output, exit |
|---|---|---|---|
| 1 | `file` of an existing slug | yes | `file "Export the report as CSV"` twice: `error: CR folder already exists: <abs>\1-inbox\export-the-report-as-csv; choose another slug`, exit 3. Message names no `--slug`. |
| 2 | `triage` of a backlog item | yes | `triage .agents/changes/2-backlog/P2/dark-mode --priority P3`: `error: <abs> is not directly inside <abs>\1-inbox`, exit 1. Same for `triage dark` (cwd-resolved path), `triage .agents/changes/3-requests`, `triage README.md`. `triage <backlog/P2/x> --priority P2` same error. |
| 3a | second `order drop` | yes | `order drop CR-101` twice: both exit 0; O-1 and O-2, both `dropped CR-101: .agents/changes/5-trash/261106-1900-101-dark-mode`. |
| 3b | `101` | yes | `order drop 101`: `error: unknown CR 101 in batch batch-01`, exit 1. |
| 4 | `order note` on cancelled | yes | `order note CR-102 --note late` after the drop: exit 0, `noted on CR-102`. (`order merged` on it: exit 2 `cannot mark cancelled CR-102 merged`: fine.) Also `order rounds CR-101 --note 5` on a cancelled CR: exit 0 (not in the spec). |
| 5a | `order rounds` errors | yes | `order rounds --note 0`: `error: order rounds <cr>`, exit 1 (no `--note`, no reason). `order rounds CR-102 --note 0`, `--note abc`, no note: `error: order rounds <cr> --note <n>`, exit 1, no reason. |
| 5b | `order budget` errors | yes | `--note -5`, `0`, `abc`, none: `error: order budget --note <usd>`, exit 1, no reason. |
| 6 | applied orders stay "pending" | yes | after two drops: `status` => `orders pending: O-1 drop CR-101; O-2 drop CR-101; O-3 note CR-101 hello; ...` while CR-101 and CR-102 show `cancelled`; `land` => `error: cannot land batch-01: live -, queued ['CR-103'], not merged -, orders pending ['O-1', ..., 'O-7'], stack driver none`, exit 2. No word on how orders end. |
| 7 | dropped shows `cancelled` | yes | `status` row `CR-101 cancelled r0/3 - | -` (STATUS.md already says "dropped": `status.py:39,73`). docs/use-cases.md line 61 says `5-trash/` and never `cancelled`. |
| 8 | `order` errors / `--batch` | partly | rounds and budget: see 5. `--batch`: with several open batches `error: several open batches (...): pass --batch` is already clear (state.py:372); not replayed with two batches; the spec does not ask for it. |
| 9 | QA folder and `open` | yes | `order qa --note "try the export"` then `open .agents/changes/1-inbox/qa-261106-1859`: `error: missing Change Specification: <abs>\03-change-spec.md; grill the CR first`, exit 2. |
| 10a | `cost` on a fresh batch | yes | `cost`: `error: no Foreman transcript recorded: the Foreman runs chantier foreman transcript $CLAUDE_CODE_SESSION_ID`, exit 2. Same with `--batch batch-01` after `land`. |
| 10b | `close` | changed, wanted | 0.4.1 said `landed: none`. Now `close` on an unlanded batch: `error: cannot close batch-01, something still runs: CR-103 is queued, not merged or cancelled; order O-1 (drop) is open; ... Nothing was deleted.`, exit 2. On a landed batch with no transcript: `error: cannot close batch-01: its final cost cannot be priced (no Foreman transcript recorded). Nothing was deleted.`, exit 2 (CR-130, keep). |
| 10c | land path needs a Foreman | partly | `land` refusal still gives no way out. Replay K: `order done O-k` with no `--epoch` works with no Foreman (exit 0), then `land` succeeds, `status` and `cost` then say `no open batch: run chantier open first` (exit 2) until `--batch batch-01` is passed, and `close` refuses (cannot price). So the CLI alone can reach `land`, never `close`. |
| 11 | `open` output | yes | `open <3 folders>`: `opened batch-01 on claude: 3 CRs, 4 slots, stack`, `CR-101 Dark mode`, ..., `brief: <abs>`. No folder move, no next step. |

New, found on the way (not in findings.md):

- `order qa` twice in one minute: `error: CR folder already exists: ...\qa-261106-1902; choose another slug`, exit 3. `order qa` has no `--slug`. Same `_new_request`, so fixing finding 1's message must not name `--slug` there (or must stay true there).
- `cancel` then `order drop` on the same CR: the second prints `dropped CR-103: <trash path>` as new order O-11 (same bug as 3a, reached by another way).
- After `land`, `status` and `cost` without `--batch` say `no open batch` (the batch is landed, not open): probably worth the one docs sentence in use-cases.md.

## Code map

- `skills/chantier/scripts/cli/src/chantier/commands.py`
  - `_new_request` 183-198 (message, exit 3 = `EXIT_CONFLICT`; used by `file_cr` 201 and `order qa` 683). Spec asks exit 2 = `EXIT_PRECONDITION`.
  - `triage` 228 -> `lifecycle.move_backlog_item` 119-127 (only `source.parent == inbox`). Help strings in `cli.py` 35-37 ("move an inbox CR"). `abandon` 236 already knows the backlog test (`in_backlog`): same predicate to reuse.
  - `order` 645-695 and `_apply_order` 524-642: `CR_ORDERS` 513, `drop` 579-587, `note` 588-595, `rounds` 605-609, `budget` 615-619, generic usage line 658-659. The order is appended and logged only after `_apply_order` returns; a raised `ChantierError` leaves `batch.json` untouched (`Batch.__exit__`, state.py 299-328), so a refusal "records no order" for free.
  - `open_batch` 407-471 (output 467-470); `prepared_cr` in `lifecycle.py` 45-76 (QA folder refusal goes before 64).
  - `status` ~740-794 (pending line 786-790), `_facts` 920-923 (per-CR pending), `land` 1319-1349 (refusal 1334-1337), `_close_target` 1352-1369, `close` 1371-1405, `cost` error at ~1632.
- `rails.py`: `running()` 31-49 lists `order O-k (kind) is open` for close; `check_idle` 52. Not to be changed beyond the spec.
- `state.py`: `Batch.cr` 333 (unknown CR, exit 1), `find_cr_batch` 394 (other commands, not `order`), `check_epoch` 375.
- `status.py`: `orders_pending` counted at 241, shown 258, in the JSON view 329 (STATUS.md, dashboard, `index`); `dropped` wording 39, 73.
- `cli.py`: `MAX_LINES = 10`, `FULL_OUTPUT` (status, cost, close, ... not truncated; `open`, `order`, `land`, `file`, `triage` are).
- Docs and cards: `docs/use-cases.md` lines 61, 67 and "Know what it costs" 133-146; `skills/chantier/references/concepts.md` 84 (exit codes), `foreman.md` 34 (orders listed until `order done`), `chief-of-staff.md` 41 (`file ... [--slug]`). `README.md` 207-208 already says close refuses when it cannot price.
- `scenario/run_scenario.py` asserts, and must be kept true or updated with the code:
  - 553: `[chief-of-staff→foreman] order O-1: drop CR-103` (first line of `order`, keep).
  - 585, 1522, 1726: `status` lines that start with `orders pending: O-`, `orders pending: O-2 qa <folder>`, `orders pending: <order> note <cr> first`. Changing that prefix or splitting applied from untouched orders breaks these three unless the `note` and `qa` forms keep the prefix. Note that 585 and 1726 are `note` orders on live or ready CRs, which would be "applied".
  - 1477: loops `order drop` over every CR of the batch after earlier drops: a CR already cancelled there now fails, so the loop must skip cancelled CRs (check which CRs are cancelled at that point).
  - 1609: `"{dropped} cancelled"` in a stderr; 983 `no Foreman transcript recorded`; 919-972 close refusals (CR-130): keep.
  - 641 `order merged ... expect=3` (stale epoch, unrelated).
  - 434-435 `triage` output parsing `triaged <path> (<P>)`: keep that line format.
  - `fm.do_order` 274-298: the scenario's Foreman marks orders done itself with `order done --epoch`; unchanged.
- `tests/test_structure.py`: structure only; check it for docs/agents identity rules if docs are touched (`agents/` untouched).

## Smallest change

1. `_new_request`: exit `EXIT_PRECONDITION`; message `CR folder already exists: <rel path>; file it again with --slug <other>`. For `order qa` pass a different hint (the folder is stamped to the minute; the order can simply be repeated) or make the QA name unique (seconds), the smallest being a message that does not name `--slug` for qa.
2. `move_backlog_item`: accept `inbox/<x>` and `backlog/P?/<x>`; a source elsewhere says `triage expects a CR folder in 1-inbox/ or 2-backlog/P1..P4/`; show the path as `_shown` does (relative). Update `cli.py` help text.
3. `order()`: normalise a bare number to `CR-<n>` for the CR argument (`args.cr` when it is digits, kinds in `CR_ORDERS` and `note`), and the ids in `order after --note`. In `_apply_order` `drop`: `cancelled` -> `ValueError`-like `ChantierError("CR-101 is already dropped: <path>")`; `note` on `cancelled` -> refused.
4. `rounds`/`budget`: full usage (`order rounds <cr> --note <n>`, `order budget --note <usd>`) and the reason (`<n> is not a whole number of at least 1`, `<usd> must be a number above 0`); the generic line 658-659 must stop shadowing rounds' usage.
5. Orders applied: add an `applied` timestamp (`"applied": now()` or `None`) on each order when `_apply_order` has done its whole part; `status` prints two groups; `land` refusal says `the Foreman marks each order done with order done <O-k>`.
6. `open`: one line per CR with its new folder, one line for the next step (`status`, then the Foreman). `prepared_cr`: a folder named `qa-*` (or whose request starts with `# QA`) is refused with "a QA folder holds findings: triage it and split it into CRs, it is not opened".
7. `docs/use-cases.md`: three sentences (cost/close on a batch with no Foreman, `cancelled` for a drop, the land/close path needs a Foreman).

## Constraints

- Ten lines: `open`, `order`, `land`, `file`, `triage` are truncated at 10 (`MAX_LINES`); `status`, `cost`, `close` are not. An `open` of 8 or more CRs already hits 10 lines (header + CRs + brief); one more line per folder move truncates the next step first. Put the next step before the long CR list, or print the move on the CR's own line.
- No new command: every item above is a message, an argument form or a field.
- `close` keeps its refusal (CR-130): scenario 948-1000 asserts it.
- `rails.py` refuses nothing more: the two new refusals (second drop, note on cancelled) are in `_apply_order`, the spec's own addition; `land`/`close` still refuse on applied orders (only the message changes).
- Zero dependency, UTF-8, Windows paths: messages already show absolute Windows paths; prefer `_shown` (relative, posix).
- Agents/cards: a role contract does not change; the docs/`foreman.md` line 34 ("`status` lists them until you mark each `order done`") stays true.

## Decisions the specification leaves open (they change what the user gets)

1. Which orders are "applied by the CLI". Candidates: drop of a non-live CR, note, rounds, slots, budget, after, approve, grant, merged, add. "Untouched": qa and the drop of a live CR. A `note` is recorded but the Foreman still has to relay it to the Driver: is it "applied"? Needs a per-order marker in `batch.json` (no field exists today; orders from older batches have none and must count as untouched).
2. The wording and place of that split in `status`. Keeping the `orders pending:` prefix for the untouched ones keeps scenario 1522 green; 585 and 1726 assert it for notes on ready/live CRs, so they would need updating.
3. `status.py`'s `orders_pending` (STATUS.md, dashboard, JSON): does it count both groups? Today it feeds `land` and `close`, which keep refusing on both.
4. Exit code of "already dropped" and "note on a cancelled CR": unspecified (existing sister refusals use 2).
5. `order drop` twice while the CR is live (first order says `is live: the Foreman stops its Driver`): refuse or record? The spec says "already dropped", so only a cancelled CR; a live one is a pending order, not a drop.
6. `101` in `order`: only the CR argument, or also the ids of `order after --note`; and the other commands (`take`, `cancel`, `handoff`, `log`, `note`) still need `CR-101`. The spec says only `order`.
7. `order rounds` (and approve/grant) on a cancelled CR is also accepted today: the spec refuses `note` only.
8. `triage` of a backlog item to the same priority: refuse, say "already P2", or do nothing; and a target collision (`move_directory` refuses, exit 3).
9. How a QA folder is recognised: name prefix `qa-` (the CLI's own naming) versus the request text. A user-filed `qa-...` folder would be taken as one.
10. Whether `order qa` twice in a minute (exit 3, no `--slug`) is in scope.
11. `status` and `cost` after `land` say `no open batch` instead of "landed: pass --batch": in scope only as a docs sentence.

## Questions only the user can answer

None blocking: items 1, 4, 5 and 9 have an obvious smallest answer (above); they are stated so the Coder takes them knowingly.

## Evidence plan

Kind of change: CLI behaviour (messages, exit codes, one status line), plus three docs sentences. Nothing visual.

- Before and after: re-run `work/replay.txt`'s commands (a small script of the same `C(...)` calls, kept as `evidence/replay.py`) against base 42a1cbd and against the worktree, in a throwaway repo with a bare origin, and keep both transcripts in `evidence/before.txt` and `evidence/after.txt` (command, stdout/stderr, exit code per step). Diff them in the PR body: one line per finding, "fixed: <command> now exit N, <message>" or "no longer holds: <command>".
- The ones that must show a change: `file` twice (exit 3 -> 2, `--slug`), `triage` of a backlog item and of `README.md`, `order drop` twice (`already dropped`, `batch.json` `orders` length unchanged: show `len(orders)` before and after), `order drop 101`, `order note` on a cancelled CR, `order rounds --note 0` and `order budget --note -5`, `status` and `land` with an applied order, `open` of two CRs, `open` of a QA folder.
- Unchanged, to show: `close` and `close --yes` on a batch it cannot price (still exit 2, nothing deleted), `order qa` then `status` (still `orders pending: O-n qa`), `cost` on a fresh batch (exit 2).
- Ten lines: count the lines of `open` with 8 CRs and show the next step survives.
- Gates: `just check` on the worktree; `just scenario` for the CLI change (lines 585, 1477, 1522, 1726 above are the likely failures); report both outputs in `evidence/`.
- Cannot be shown: Linux/macOS behaviour from here (the CI does it); Copilot host output (same code path, `detect_host` only).
