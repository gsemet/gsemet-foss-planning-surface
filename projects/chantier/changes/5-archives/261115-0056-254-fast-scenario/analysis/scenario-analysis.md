# `just scenario`: from about 40 minutes to under 5, an analysis from the code

Scope: this analysis comes from reading the code only. Nothing was run or timed. The files read are:

- `scenario/run_scenario.py` (7,130 lines)
- `scenario/README.md`, `scenario/fake_gh.py`, `scenario/fake_glab.py`, `scenario/fake_autosync.py`
- `justfile` (`scenario:` runs github, then gitlab)
- the CLI's legacy readers
- `skills/chantier/scripts/cli/tests/conftest.py`
- `.agents/changes/` and the planning surface, both read-only

Line numbers refer to `scenario/run_scenario.py` unless a file is named. Estimates marked **(guess)** come from no measurement.

The coordinator relayed two user decisions, and both are applied here:

- **No backward compatibility.** The legacy cases are DROP, and the CLI code they protect is listed for removal. Section F has the one-off migration.
- **Pure refusals move to pytest.** They run in-process, parametrized, few and fast. Refusals that need a live batch sequence stay in the scenario.

Each block below is marked **TESTS** (move to pytest) or **KEEP** (stays in the scenario). A pytest harness that calls the CLI in-process already exists: in `skills/chantier/scripts/cli/tests/conftest.py`, the `repo` fixture (l.35-72) builds a git repo and isolates HOME and the env, and the `chantier` fixture (l.75-84) calls `chantier.cli.main([...])` in-process. `tests/test_cli_runs.py` already opens batches with it. "In-process OK" below means that fixture is enough.

---

## A. Cases and main-batch sections

Abbreviations:

- **fx** = fixed-cost driver: a CLI subprocess at about 0.3-0.6 s on Windows **(guess)**.
- **G** = one `GATE` (`uv run --no-project python -m compileall`, l.48). Each costs a uv start plus a Python start, about 1-1.5 s **(guess)**. It is paid by `w.gate`, `w.ready` and `driver_round`.
- **S** = a real sleep.
- **dep** = hidden state dependency.
- **gh/gl** = forge-specific.

### A.1 Main batch `scenario(w)` (l.540-1009)

| Section | Lines | Proves | Hidden deps | Forge | Cost | Verdict |
|---|---|---|---|---|---|---|
| §1 setup, preflight, rules | 541-602 | Preflight P-checks with a redirected HOME. P10 `gh stack` extension detection (571-587). Rules. | none (fresh World) | P10 block is gh-only | about 9 preflight calls | Preflight refusal and warning lines: **TESTS** (in-process OK; `test_cli_runs.py` l.244-331 already covers P10 allow rules). Keep one preflight in the unit: **KEEP** (slim). |
| §2 open, Foreman | 604-679 | 5 `prepare_cr`; triage, abandon and file refusals; open; `opened_record` (2559); status; `foreman set` | none | no | about 20 fx | Triage, abandon and file refusals: **TESTS**. Open and record: **KEEP**. |
| §3 CR-101 round, ship, handback | 681-719 | The Driver's own push and PR, hand-back, gate line `pass {GATE} at` (l.692) | §2 | `open_pr` gh/gl (186-207) | 2 G, about 10 fx | **KEEP** (both forges) |
| §4 CR-102 two rounds | 721-728 | Two rounds | §2 | no | 2 G | **KEEP** |
| §5 steering | 730-772 | Drop CR-103 kills a sleeper (poll up to 5 s, 737-742); order add CR-105; order note | §2-4 | no | S up to 5, about 12 fx | **KEEP** |
| §6 Foreman restart, epoch 2 | 774-782 | The old Foreman is refused | §5 | no | few fx | **KEEP** |
| §7 lost Driver CR-104 | 784-808 | Lost then hand-back; `status_files` (2043); cancel twice | §6 | no | about 2 G | **KEEP** |
| §8 merges, fast-forward | 810-929 | `land` ×5, fast-forward of a clean main, untracked files intact; `fake_transcripts` (6429); `board_index` (2079) | §7 | `merge_pr` gh/gl | 5 scratch clones; `board_index` makes 60 padding folders (2099-2117) | Merges and fast-forward: **KEEP** (both forges). `board_index`'s "a folder without STATUS.json" and padding: **TESTS** (pure index rendering, in-process OK). |
| §9 cost | 931-993 | Exact $ ($1.608 over 94 calls); `cost_audit` (6330); `foreman_chief_lines` (1615) | `fake_transcripts` + §8 | no | about 10 fx | Exact pricing arithmetic: **TESTS** (`test_costs.py` domain). Keep one "cost line appears" check: **KEEP** (slim). |
| §10 Copilot cost | 995-998 | `copilot_cost` (6203), `copilot_uv` (6298, already in-process) | §9 | no | few fx | **TESTS** (in-process OK) |
| §11 event log, forge call log | 999-1009 | `events.jsonl` kinds; the forge call log has the merges | all above | gh/gl call shapes (1005-1009) | none | **KEEP** (both forges) |

### A.2 The case sequence (l.1010-1044)

| Case | Lines | Proves | Hidden deps | Forge | Cost drivers | Verdict |
|---|---|---|---|---|---|---|
| `close_batch` → `close_refusals` + `unpriced_model` | 2430 / 2247 / 2178 | Close on the user's word; pause shows cost to date; the second pause is refused (2262); close refused while something runs (2301-2366); order add on a paused batch stays paused (2286-2297); unknown model priced as unpriced | **Strong.** Main-batch state: CR-103 dropped, CR-101 `merged_at`, `uuid-foreman.jsonl` (2252), Copilot `events.jsonl` from §10. Exact "$2.618 over 95 calls" (2284). Sets `w.paused_total`. | no | about 30 fx | Close flow: **KEEP** in U1. The second-pause refusal and the close-refused-while-X loop: **TESTS** (prepared paused `batch.json`, one call; in-process OK). `unpriced_model`: **TESTS**. "A call after the pause is spend": **TESTS** with a fixture transcript. |
| `retro_cases` | 2583 | 3 open/cancel/pause/close cycles; retro written into `batch-NN.md`; `merged_total` unchanged | `previous = w.name` closed by `close_batch` ("last closed: batch-01") | no | 3 × (open + close) about 25 fx | **KEEP** (U1, after `close_batch`). Could seed its own record if moved. |
| `copilot_missing_transcript` | 6287 | Cost with no Copilot transcript says so | leaves its batch open; the next case resets | no | 2 fx | **TESTS** (in-process OK) |
| `lifecycle_regressions` | 6189 | `open --remote nowhere` exits 4; "nothing written outside `.agents/changes`" (git porcelain) | clean porcelain of the shared repo | no | 2 fx | **Not legacy despite its name.** It guards `open`'s remote check and the AGENTS.md write-scope rule. Remote refusal: **TESTS**. The porcelain check duplicates `test_cli_runs.py:64` but is stronger after a full sequence, so keep it as a one-line end-of-unit assertion in every unit. The case function itself: **DROP**. |
| `stack_batch` | 4077 | Stack of 3, joiner via order add, order after, ship bases, pr-body stale-SHA (commit-tree loop up to 2000 tries, about 27 expected), bottom merged alone, take stack, pause, close | `w.reset()` only | no | about 3 G, about 60 fx, about 27 `git commit-tree` | **KEEP**. The second open refused (4089): **TESTS** (duplicates 6737). |
| `forge_stack_cli` | 4244 | Native stack on the forge: create, read, insert, retarget/unstack, refusals | none beyond reset | **gh (4420-4564, 4597-4679) / gl (4294-4419)**; common part 4279-4292, 4566-4596 | many `forge-stack` fx, fake forge only | **KEEP** (both forges, the per-forge part only on gitlab). The parallel-batch refusal (4680-4691): **TESTS**. |
| `ready_words` | 5741 | Ready locally / PR in draft / ready to merge icons; stack of 3; release on stack (§9); parallel dependency | `OPENED[a]` (5851) is global | no | about 4 G, about 50 fx | **KEEP** (merge §9 with `release_on_stack`). §8 "old record, no draft state" (5839-5843) and the hand-edited `pr` (5845-5849): **TESTS** (pure STATUS rendering of a prepared record). |
| `batch_modes` | 4694 | Parallel by default, series, a dependency before its CR refused, series→stack switch | reset | no | about 7 `driver_round` = 7 G | **KEEP**. The dependency-before-its-CR refusal: **TESTS**. |
| `release` | 4800 | Full release: approvals, fix, grant, merge refusal (`merge_refused`), budget, published | the final `calls.count(merged) >= 2` reads the cumulative log (works alone) | the call-log check (4973-4975) is forge-shaped | about 5 G, about 60 fx | **KEEP** (github) |
| `granted_fixes` | 4978 | Fix limit of 3; order drop refusals; usage messages; pause, close | reset | no | about 3 G | Fix flow: **KEEP**. Usage and drop refusals: **TESTS**. |
| `release_last` | 5041 | A release added later waits; confirm, void, fix-for; release alone | reset | no | about 4 G | **KEEP**. Queued-icon matrix (duplicates `dependencies`): **SHRINK**. "No approval covers the merge" (5162-5165): **SHRINK** (keep once, in `release`). |
| `release_on_stack` | 5203 | Release on the stack's top branch, restack, `open_pr` base `top`; §12 no release PR (5347); §13 series (5390); **§15 older CLI's `confirmed`** (5373-5388) | reset | no | long: about 6 G, about 80 fx | Main path: **KEEP**. §9 merge-approval (5321-5324): **SHRINK**. §13 series: **DROP** (duplicates `batch_modes`). **§15: DROP (legacy).** No CLI code to remove: `confirmed` no longer exists in `src/` (grep finds none), so the check only proves an unknown key is ignored. |
| `qa_on_head` | 5414 | order qa, budget (exit 5), QA folder, pause blocked by QA, QA folder not openable | reset | no | about 1 G | Live parts: **KEEP**. Budget refusal and "QA folder not opened" (5430, 5444): **TESTS**. |
| `old_words` | 5472 | `status: open` / `landed` read as running / paused | reset | no | about 6 fx | **DROP (legacy).** CLI code: `core/records.py:136-139` (docstring) and `:170-184` (`BatchRecord._old_words`). |
| `changes_tree` | 5526 | `triage --ready/--inbox`; open of a 3-ready item with no spec; folder follows status (take → 2-actives, merged → 3-done, drop → 6-trash); close refused for a stray folder | reset | no | about 1 G, about 25 fx | Triage moves and stray-folder refusal: **TESTS** (in-process OK). Folder-follows-status through take/handback/merge: **KEEP** (folded into U4). |
| `old_tree` | 5625 | Converts 3-requests / 4-archives / 5-trash in place; refuses a non-empty target | moves `w.state` aside; sets `.batch-number 80` to avoid the shared repo's branches | no | copytree/move, about 8 fx | **DROP (legacy).** CLI code: all of `lifecycle/convert.py` (301 lines) except `open_repo`; `commands/intake.py:23,52`; `lifecycle/stages.py:194-199` (3-requests cleanup in `_relocate`) and the "older tree" note in `start_cr` (l.203-204). |
| `next_number` | 2656 | Batch number from the records (batch-03.json + `.batch-number 1` → batch-04) | moves state aside | no | 2 fx | **TESTS** (prepared records, one `open`; in-process OK). Not legacy. |
| `backfill_cases` | 2684 | Backfill of `5-archives/batches` from older archives and old ids (`01-eval-real`) | moves state aside | no | copytree, about 6 fx | **DROP (legacy).** CLI code: all of `lifecycle/backfill.py` (219 lines); `convert.py:15,300`; `core/batch_records.py:78` (`"backfill": None` in a blank record); `history.py:29` ("(backfilled, no close date)") can stay as "no close date". |
| `dependencies` | 5924 | depends.json cycle / unknown slug / malformed; after-waits; `order after`; a QA order holds a slot; icon matrix | reset | no | about 3 G | Cycle, unknown and malformed refusals: **TESTS** (one `open` each, parametrized). Waits, slots and icons: **KEEP**. |
| `release_merge_on_approval` | 6076 | No approval covers the release PR's merge; Windows-only close on a folder in use (6113) | sets `w.number_after` | no | about 2 G | **KEEP**, but fold its approval check into `release` (4935-4940) and keep the Windows close check. |
| `lost_messages` | 6123 | The wake catches up; numbers keep rising after the folder is deleted (6130); a date in the trash is not a CR number (6136) | **`w.number_after`**; earlier trash entries; `git push origin X:main` | no | about 10 fx | **KEEP** in the same unit as `release_merge_on_approval`, or seed `.batch-number` and a trash entry. |
| `failed_opening` | 2741 | Latin-1 spec refused; second item fails, first restored | reset | no | 3 fx | **TESTS** (in-process OK) |
| `playbook_config` | 2761 | chantier.yaml S1-S6: S1 absent; S2 BOM; S3 a running batch keeps its playbook; S2b/S2c `ci:` lines; **S4: 19 refusals (2893-2943)**; S5 host cannot set a model; S6 absent again | reset | no | about 6 opens + 19 refusal opens | **TESTS** in full: S4 parametrized (19 cases, one call each); S1-S3 and S5 are open + read, in-process OK. The S2b `take`/`handoff` `ci:` line can stay in pytest (open + take in-process). |
| `cancel_during_gate` | 2978 | A cancel during a gate kills it; locks released (`lock_names` polls) | reset | no | slow gate `uv run … slow_gate.py` (60 s, killed) | **KEEP** (U9). Swap uv for `sys.executable` (D). |
| `stop_own_gate` | 3010 | A Driver stops its own gate; `cancel` needs the epoch | reset | no | about 6 background gates, several `sleep(0.5)`, polls | Live stop: **KEEP**. The epoch refusal: **TESTS**. "Stop per slot" duplicates `gate_parallel` E4: **SHRINK** one of them. |
| `rails` | 3152 | Second `round` refused (3171); round limit exit 5 (3180); slots 0 (3202); `land` invalid (3207); budget exit 5 (3215); take on ready needs `--note` (3228); held gates (2 s), queue (3 × 3 s), dead waiter (3 s), reused pid | reset | no | **S about 20-25 s (guess)**, about 3 G | Refusals 3171-3236: **TESTS** (prepared batch via in-process open+take, or a crafted `batch.json` as the scenario does at 3214). Gate lock, queue, dead waiter, reused pid (3238 onward): **KEEP** (real processes). |
| `gate_parallel` | 3365 | E6 `long_gate` yaml refusals (3416-3437); E5 move-up (3438); E2/E3 two at once (3468, a1 runs 16 s and is awaited at 3486); E4 stop per slot (3495) | reset | no | **S about 30 s+** | E6: **TESTS** (P12 overlap with `playbook_config`). E2-E5: **KEEP** with shorter, event-driven waits (D). |
| `handback_proofs` | 3682 | Two proofs (gate, verdict) at the head; `--no-gate`; reopen via `take --note`; merged under a Driver | reset | no | many G | **KEEP**. `take --note` reopen duplicates `rails` 3228-3236: **SHRINK**. |
| `gate_proof` | 3836 | 6 CRs; gate bound to the head; dirty tree; `core.abbrev 12`; short heads; budget versus rounds; round fingerprint | reset; sets and unsets repo git config | no | about 6 G | **KEEP**. The budget-vs-rounds refusal: **TESTS**. |
| `restore_cr` | 4010 | Restore from 6-trash; name clash; a former batch CR; numbering (4073) | reset | no | about 8 fx | **TESTS** (prepared trash folder, one `restore`; in-process OK). |
| `driver_liveness` | 3537 | Activity lines from an edited lock (`os.getpid()`, 3561); `note context:`; `cost --by cr` peak; restart rules; `handback blocked context:`; card text (foreman.md, driver.md) | reset | no | about 20 fx | Card text check: **TESTS** (structure, belongs in `test_plugin_files.py`). Liveness lines from a crafted lock or ticket: **TESTS**. Restart path through a live Driver: **KEEP** (slim). |
| `foreman_in_a_worktree` | 2020 | A Foreman in a linked worktree stops before claiming its epoch | worktree at `w.root/"foreman-session"` | no | 1 worktree, about 4 fx | **KEEP** (U10) |
| `direct_batch` | 1660 | Direct mode: preflight `--direct`, open `--direct` refusal, heartbeat, steering cost (`uuid-chief.jsonl` + subagents), spec-writer/critic cost lines, paused batch + order add, reopen, close, Foreman takeover | saves and restores `uuid-chief.jsonl` written by the main batch (`kept`) | no | about 6 G, about 60 fx | **KEEP**. Order add on paused (1929-1955) duplicates `close_refusals` 2286-2326: keep one. Spec-writer/critic pricing: **TESTS**. |
| `seat_handover` | 1553 | Seat: two Chief of Staff sessions, cost, pause, close | reset | no | about 15 fx | **KEEP** (U10). `test_cli_runs.py:28` already has the seat; keep only the batch-level part. |
| `remote_board` | 1252 | The board server: key, read-only files (404s, 1438), backlog moves (1174), POST refusals 400/409 (1211-1219), seat-watch exit (`exits()` up to 25 s), held port, `0.0.0.0` bind (1511), `board.port` from yaml (1526) | own BoardProcs | no | 6+ board starts, `sleep(1)` (1494), `line(1.5)` silence (1303), polls | **KEEP** (U12). The POST refusals and 404s are **TESTS** only if `test_board.py` has an in-process app harness **(not checked; guess)**. |
| `external_surface` + `surface_autosync` | 6695 / 6540 | Planning surface: two projects, init, open `--direct`, seat per project, board, autosync join/start/stop/approve, archive in the PR, close | own `SurfaceWorld`; `OPENED.clear()` | gl branch differs only by forge commands | board, autosync poll up to 40 s, 120 s sleeper | **KEEP** (github only; U1 on gitlab covers `open_pr`/`merge_pr`). `test_cli_runs.py:108` covers surface init in-process. |
| `cr_summary` | 7075 | The summary linter and commands; refusals (7000-7001); file moves with its folder | own World | no | about 25 fx, `copytree` (7048) | **TESTS** in full (in-process OK; no forge, no git beyond the repo fixture). |

---

## B. Duplicate checks

| Behaviour | Where | Keep |
|---|---|---|
| A release PR is the user's to merge; no approval covers it | `release` 4935-4940, `release_last` 5162-5165, `release_on_stack` §9 5321-5324, `release_merge_on_approval` 6100-6103 | once, in `release` |
| A release on the stack's top branch | `release_on_stack`, `ready_words` §9 | `release_on_stack` |
| Series mode | `batch_modes`, `release_on_stack` §13 (5390) | `batch_modes` |
| `take --note` reopens a ready CR | `rails` 3228-3236, `handback_proofs` 3786-3797, main §5/§7 | main batch plus one pytest refusal |
| Order add on a paused batch stays paused; the first take reopens | `close_refusals` 2286-2326, `direct_batch` 1929-1955 | one |
| Budget exit 5 (take, round, release go, qa) | `rails` 3215, `gate_proof`, `release`, `qa_on_head` 5430, `driver_liveness` 3655 | one parametrized pytest |
| `gate --stop` per slot | `stop_own_gate`, `gate_parallel` E4 | `gate_parallel` E4 |
| A gate waits for the lock | `rails` held gates, `gate_parallel` E5 | `gate_parallel` E5 (rails keeps queue and dead waiter) |
| No-chantier.yaml P12 preflight | `playbook_config` S1/S6, `gate_parallel` E6 3434 | pytest |
| Second open refused | `stack_batch` 4089, `external_surface` 6737 | pytest |
| Queued-icon matrix | `dependencies`, `release_last` | `dependencies` |
| Close/pause/price tail | about 10 cases end with `priced_foreman` + pause + close | keep in U1 and `retro_cases`; elsewhere `w.reset()` only, unless the case is about closing |
| Seat basics | `seat_handover`, `test_cli_runs.py:28` | pytest for basics |
| Write scope | `lifecycle_regressions`, `test_cli_runs.py:64` | a one-line end-of-unit porcelain assertion |

---

## C. The split design

### C.1 Units (13 GitHub + 2 GitLab = 15 processes)

| Unit | Content | Forge | World | Weight **(guess, after D)** |
|---|---|---|---|---|
| U1 main | §1-§11 + `close_batch` + `retro_cases` | **gh + gl** | `World.build` | heaviest: about 150 fx + about 12 G + 5 clones, about 90-150 s |
| U2 stack | `stack_batch` + `ready_words` (with §9) | gh | fresh | about 110 fx + 7 G, about 60-90 s |
| U3 forge-stack | `forge_stack_cli` | **gh + gl** (per-forge branch) | fresh | about 60 fx, about 30-40 s |
| U4 modes | `batch_modes` + `dependencies` (live) + `changes_tree` (live) | gh | fresh | about 10 G + 60 fx, about 60-80 s |
| U5 release | `release` + `granted_fixes` | gh | fresh | about 8 G + 80 fx, about 60-80 s |
| U6 late release | `release_last` + `release_on_stack` (slim) + `release_merge_on_approval` + `lost_messages` | gh | fresh; the `number_after` chain stays in-unit | about 12 G + 120 fx, about 90-120 s |
| U7 rails | `rails` live gate parts | gh | fresh | S 20 → 8 s + about 30 fx, about 30 s |
| U8 gate-parallel | `gate_parallel` E2-E5 | gh | fresh | S 30 → 10 s + about 30 fx, about 30-40 s |
| U9 gates | `cancel_during_gate` + `stop_own_gate` + `handback_proofs` + `gate_proof` | gh | fresh | about 15 G + 80 fx, about 70-100 s |
| U10 direct | `direct_batch` + `seat_handover` + `foreman_in_a_worktree` | gh | fresh; the `uuid-chief.jsonl` fixture written locally instead of restored | about 6 G + 90 fx, about 60-80 s |
| U11 driver | `driver_liveness` (live part) + `qa_on_head` (live part) | gh | fresh | about 30 fx, about 20 s |
| U12 board | `remote_board` | gh | fresh | board starts plus the `exits()` wait, about 40-60 s |
| U13 surface | `external_surface` + `surface_autosync` | gh | `SurfaceWorld` (already isolated) | board plus autosync polls, about 40-60 s |
| pytest | every TESTS block above (`cr_summary`, `playbook_config`, refusals, cost arithmetic, legacy gone) | none | `repo` + `chantier` fixtures | in-process, about 10-20 s total |

Forge matrix: GitLab runs **U1 and U3 only**. That is everything that touches `open_pr`/`merge_pr` (186-207), P10's gh block (571-587, github only), the forge call-log checks (1005-1009) and `forge_stack_cli`'s gl branch. Today's second 1,200 s run becomes about 2 units in parallel.

### C.2 Mechanics

- **One process per unit.** This keeps `LOG`, `CHECKS`, `ARGS` and `OPENED` (l.59) separate with no refactor. `OPENED` must not be shared: CR numbers restart at CR-101 per World.
- **CLI.**
  - Add `--unit NAME` (repeatable) to `run_scenario.py`. Add a `UNITS = {name: [case, ...]}` table that replaces the call list at l.1010-1044.
  - `main()` (7091) builds the World for the unit (`World.build` or `SurfaceWorld`) in its own `mkdtemp`.
  - It writes `<run-dir>/<unit>-<forge>.md` (transcript) and `<unit>-<forge>.json` (`{"checks": n, "failed": [...], "seconds": t}`).
- **Parent.**
  - `--all [--jobs N]` (default `os.cpu_count()`) spawns children with `subprocess.Popen([sys.executable, __file__, "--unit", u, "--forge", f, "--out", run_dir])`.
  - Children use `sys.executable`, not `uv run --locked`, which saves one uv start per child. The parent already runs inside uv's env.
  - It waits with a per-unit timeout, then concatenates transcripts **in the fixed table order** into `scenario/results/scenario-<YYYYmmdd-HHMMSS>-<pid>.md`. This fixes the second-only name at l.7115.
  - It prints a per-unit table (checks, failures, seconds) and exits nonzero if any unit failed or timed out.
  - On timeout it kills the child's process tree: `taskkill /T /F` on Windows, `os.killpg` on POSIX. That needs `start_new_session=True` or `CREATE_NEW_PROCESS_GROUP`.
- **Template repo (optional speedup).** The parent builds one World template once (origin bare, AGENTS.md, CONTRIBUTING.md, first push). Each child copies it with `shutil.copytree` and fixes the remote URL with `git remote set-url`. This saves about 6 git calls per unit **(guess: small)**.
- **justfile.** Python does the parallelism, so the recipe is the same on Windows (`powershell` shell, l.3) and on Linux CI:

  ```
  scenario *args:
      {{run-cli}} scenario/run_scenario.py --all {{args}}
  ```

  `just scenario --unit U7` reruns one unit, and `--forge gitlab` restricts the forge.
- **README.** Update the coverage list (lines 25-160) to the unit table, and fix the stale "about two minutes per forge".

### C.3 Is under 5 minutes reachable?

The wall time is about the longest unit plus process overhead, **if cores ≥ units**. With the GATE fix and the sleep cuts (D), U1 and U6 look like 90-150 s **(guess)**. **Under 5 minutes looks reachable on an 8+ core dev machine.**

Caveats:

- **CPU contention.** 15 units each spawn Python, git and uv subprocesses. On Windows, process creation and Defender scanning dominate, so 15 parallel units on 8 cores may stretch each unit by 1.5-2× **(guess)**.
- **CI.** GitHub's standard Linux runner has 4 vCPUs **(guess, check)**. There the wall time is about sum/4. The sum after cuts is about 900-1,100 s **(guess)**, so about 4-5 min on CI. It is tight; the GATE fix and pytest moves are what make it possible.
- **The biggest lever is per-call cost**, not the split. Every fx and G is a Python or uv start.

---

## D. Cheap speedups inside cases

1. **GATE without uv** (l.48). Use `f'"{sys.executable}" -c pass'`, or `-m compileall -q .` if compile matters. Checks quote the constant (l.692 `pass {GATE} at`), so they still match. This saves a uv start on every `w.gate`, `w.ready` and `driver_round`: about 80-100 G across the run, roughly 1 s each **(guess)**. The largest single win.
2. **`cancel_during_gate`'s slow gate** (`uv run --no-project python slow_gate.py`): use `sys.executable` the same way.
3. **Event-driven waits instead of fixed sleeps.**
   - `gate_parallel`: a1 16 s awaited (3486), a2 8 s, q1 8 s, 1.1 s sleeps.
   - `rails`: 2 s held gates, 3 × 3 s queue, 1.1 s sleeps.
   - Make the gate script block on a release file that the test touches (a `Path.exists` poll), not on `time.sleep(N)`. The checks then assert order, not duration. Keep the `waited >= 1` checks by touching the release file after at least 1 s.
   - Saves about 40 s of real sleep and removes load sensitivity. Shrinking the sleeps proportionally would also work but adds flakiness under load (E).
4. **`remote_board`.**
   - `line(1.5)` silence (1303) → 0.5 s.
   - `sleep(1)` (1494) → poll.
   - `exits()` (up to 25 s) depends on the board's seat-watch interval **(not checked in the CLI; guess)**. If the interval is configurable by env, set it short for the scenario. Otherwise leave it, since the CLI must not grow a test-only knob without the user's word.
5. **Drop the close/pause/price tail** in cases that are not about closing. `w.reset()` already clears `4-batch` (l.173).
6. **`prepare_cr` costs 2 CLI calls** (file + triage). Cases that do not test filing could write the backlog folder directly. This is less real, so flag it to the user; saves about 2 fx per CR, about 100+ calls overall **(guess)**.
7. **`stack_batch`'s `commit-tree` loop** (about 27 expected tries for an all-decimal 7-hex SHA). Pin `GIT_COMMITTER_DATE`/`GIT_AUTHOR_DATE` and a known message so the first try hits, or keep the loop: about 27 git calls, about 3-5 s on Windows **(guess)**.
8. **Gone with the DROPs.** The state-move-aside and copytree work in `old_tree`, `next_number` and `backfill_cases` disappears with the DROP or TESTS verdicts.
9. **`open_repo`** (`lifecycle/convert.py:293-301`) runs `convert_old_tree` and `backfill_history` on every CLI command. Each is a few `stat` calls; dropping them is a tiny saving per call.

---

## E. Flakiness risks in parallel runs

- **Results file name to the second** (l.7115): parallel runs collide. Fixed by the parent naming in C.2.
- **`free_port()` races** (l.1079, 1526, 1537): bind 0, close, reuse. Another unit can take the port in between. Only U12 and U13 start boards. Prefer `--port 0` and reading the start line, which most boards already do. Keep `free_port()` only for the `board.port` yaml check, and retry once on "port held".
- **`0.0.0.0` bind** (1511): the Windows firewall may prompt once per `python.exe` path. It is not parallel-specific, but a prompt blocks an unattended run.
- **Timing upper bounds under load.**
  - `lock_names` 10 s deadlines, `wait_tickets` 15 s, `exits()` 25 s, the autosync join poll 40 s, `communicate` timeouts of 30/60/90 s, `< 10` checks.
  - 15 parallel units slow each call. Lower bounds (`waited >= 1`) are safe; upper bounds are the flake source.
  - Event-driven gates (D3) remove most of this.
- **Leaked sleepers.** The 60 s gates, the 120 s surface sleeper and the 300 s sleepers survive a crashed unit. The parent should kill each unit's process group on exit or timeout (C.2).
- **Shared user environment.**
  - HOME is overridden only for preflight. `CHANTIER_CLAUDE_PROJECTS` and `COPILOT_HOME` are redirected per World.
  - Global git config is inherited: a global hook, template, `core.autocrlf` or credential helper is a risk for every unit equally. `core.abbrev` is set at repo level (`gate_proof`), so that is fine.
  - Suggest `GIT_CONFIG_GLOBAL` set to an empty file in `World.env` (git ≥ 2.32).
- **uv cache**: shared, and concurrent reads are fine. With D1 the scenario barely calls uv.
- **Process lookup by command line** (sleepers named by their worktree, 735-738; `cancel` kills by worktree path): paths are unique per `mkdtemp`, so this is safe in parallel.
- **Gate locks**: per planning folder (`gate_slots.py:26-28`, `repo.changes / ".long-gate{mid}.lock"`; `gate_queue.py:16`), not machine-wide. Safe in parallel.
- **Board key** in each repo's `.git/chantier/board.json`, autosync state under each surface's `.git/ai-autosync`, fake forge state per `root/gh-state.json`: all per World. Safe.
- **Windows file locks**: parallel `rmtree` of temp dirs while Defender scans. Use `shutil.rmtree(onerror=...)` with a retry at teardown and do not fail the run on cleanup.

---

## F. Dropping backward compatibility: formats, what is still on disk, a one-off migration

### F.1 Legacy readers to remove, and the format each reads

| Reader | Code | On-disk format it reads | Scenario case |
|---|---|---|---|
| Old batch status words | `core/records.py:136-139, 170-184` (`BatchRecord._old_words`) | `batch.json` with `status: "open"`, or `status: "landed"` plus a `landed` time | `old_words` (5472) |
| Old tree conversion | `lifecycle/convert.py` (`old_tree` l.23, `convert_old_tree` l.38, helpers l.57-291); call sites `convert.py:299`, `commands/intake.py:23,52`; `lifecycle/stages.py:194-199` (`_relocate` removes emptied `3-requests` folders); docstring note in `start_cr` (l.203-204) | `.agents/changes/3-requests/` (batch folder with `batch.json`, STATUS.md/json), `4-archives/`, `5-trash/`, paths in records prefixed with those names | `old_tree` (5625) |
| Records backfill | `lifecycle/backfill.py` (219 lines); `convert.py:15,300`; `core/batch_records.py:78` (`"backfill": None`); `history.py:29` wording | archived and trashed CRs' `STATUS.json` whose `batch` is an old id (`01-eval-real`, `02-eval-heavy`, ...), `.batch-number`, old retro folders `<stamp>-batch-<n>` (`OLD_RETRO_FOLDER`, backfill.py:33) | `backfill_cases` (2684) |
| `.agents/changes/`-prefixed record paths | `core/repo.py:213-218` (`planning_path`), `history.py:39` (`archive_of`); scenario `World.at` l.182 | `crs[].path` in `batch.json` or records written as `.agents/changes/...` instead of relative to the planning folder | none named; covered implicitly |
| Older CLI's `confirmed` field | none left in `src/` (grep finds no `confirmed` in the release code) | `crs[].confirmed` in `batch.json` | `release_on_stack` §15 (5373-5388): drop the check only |
| Record with no `pr_draft` | `core/records.py:72` (`pr_draft: bool \| None`), `stacks.py:75,87` (None reads as draft) | `crs[]` without `pr_draft` | `ready_words` §8 (5839-5843). **Keep the code**: None-as-draft is also the safe reading of a hand-edited record. Move the check to pytest. |

Once all of these are gone, `open_repo` (`convert.py:293-301`) becomes `Repo.find(cwd, project=project)`. It moves to `core/repo.py` or a small `lifecycle/open.py`, and its 16 importers (`commands/*.py`: batch_status, closing, driver, delivery, facts, forge_stack, cost/command, gate, opening, intake, orders, release, preflight, summary, seat, rules) change their import line.

### F.2 What is still on disk (read-only inventory, 2026-11-14)

**`C:\Users\gaeta\Projets\chantier\.agents\changes`:**

- **Old tree**: `3-requests/`, `4-archives/` and `5-trash/` are absent. Nothing to convert.
- **Old status words**: `4-batch/` holds only the empty `1-pending/`, `2-actives/`, `3-done/`, with no `batch.json`. No `batch.json` exists anywhere under the folder, so there is nothing in the old words.
- **Records**: `5-archives/batches/` holds `batch-01` … `batch-17` (`.json` + `.md`). **16 of them (batch-01 to batch-16) carry a non-null `backfill` object.** Example from `batch-01.json`: `"closed": null`, `"backfill": {"written": "2026-11-13T19:36:26Z", "former_id": "01-eval-real", ...}`. batch-17 has the key too, null. These are current-schema records (schema 1); the `backfill` key is provenance data, not a legacy format. Records are read as dicts (`Rec`), so the key is harmless once the writer is gone.
- **Old batch ids in archived STATUS.json**: 14 of 151 STATUS.json files name an old id.
  - 10 in `5-archives`, for example `261105-1059-101-forge-auth-status` → `01-eval-real`, `261105-2126-106-qa-budget-rail` → `03-eval-real-050`, `261106-0016-108-cr-board-mod` → `04-cr-board`, `261106-0812-111-batch-folder` → `05-batch-folder`.
  - 4 in `6-trash` (`261105-1314-102…105` → `02-eval-heavy`).
  - One more, `5-archives/work/captures`, has an empty `batch` (a stray folder in `5-archives`, worth a look).
  - Only backfill reads these ids specifically. The board index shows them as-is.
- **`.agents/changes/` prefix**: 0 records in `5-archives/batches/*.json` use it. 8 archived STATUS.json contain the string, but in document-link `name` labels (for example `"name": ".agents/changes/STATUS.md"` in `261110-1449-158-changes-tree-v2`), not as CR paths. These are display text, unaffected by removing `planning_path`'s prefix strip **(checked on samples; a full key-level scan is part of the migration's verify step)**.
- **Old retro folders `<stamp>-batch-<n>`**: none.

**`C:\Users\gaeta\Projets\gsemet-foss-planning-surface`:**

- No `batch.json`, no `5-archives/batches`, no STATUS.json with old ids. There are no chantier-written records to migrate.
- **`projects/agentic-planning-surface/changes/` has `1-inbox, 2-backlog, 3-batches, 4-archive, 5-trash`**, and `5-trash/` holds only `.gitkeep`. Today `old_tree()` (`convert.py:28`) returns True on `5-trash/`, so **the first chantier command on that project would try to convert it** (rename `5-trash` → `6-trash`). This is a live hazard that removing the reader also ends.
- `projects/{chantier, markdown-okf-schema-studio, okf-schema}/changes/` use `3-stash/` and `4-batches/{1-pending,2-actives,3-done}`, `.gitkeep` only. **The CLI knows neither name** (no match in `src/`); its layout is `3-ready/` and `4-batch/`. This looks like the surface's own scaffold, not a chantier legacy format **(guess)**. It is outside the legacy readers, but chantier would create its own `3-ready/` and `4-batch/` beside them. Flag it to the user.

### F.3 One-off migration (a script run once from the scratchpad, never kept in the CLI)

The order is: migrate, verify, remove.

1. **Preconditions.** No running batch in either folder (true today: no `batch.json`). Autosync stopped on the surface. A clean `git status` in both repos, so the migration is one reviewable commit each.
2. **Migrate (mostly a no-op here). The script:**
   - (a) refuses if `3-requests/`, `4-archives/` or a `5-trash/` with files exists in a chantier planning folder, and if any `batch.json` has `status` `open` or `landed` (none today);
   - (b) rewrites the 14 archived `STATUS.json` `batch` values from old ids to `batch-NN`, using the map in the records' `backfill.former_id` (01-eval-real → batch-01, 02-eval-heavy → batch-02, 03-eval-real-050 → batch-03, 04-cr-board → batch-04, 05-batch-folder → batch-05). This is optional; it only makes the index uniform;
   - (c) strips a leading `.agents/changes/` from any `crs[].path` or `archive` value in `batch.json` and records (0 found today; the scan proves it);
   - (d) leaves the `backfill` provenance in records as data;
   - (e) on the surface, `agentic-planning-surface/changes/5-trash/` (only `.gitkeep`) can be renamed `6-trash`, or left alone once the reader is gone. It is the user's call, together with the `3-stash`/`4-batches` scaffold question.
3. **Verify with the current CLI, before removal.** On a copy of each planning folder in a temp git repo:
   - run `chantier status` ("last closed: batch-17"), `chantier cost --batch batch-17`, and the board's index (`board_index`-style `tree`/`file` reads);
   - confirm no stderr line `converted .agents/changes…` or `backfilled 5-archives/batches…` appears, which proves the readers are already no-ops;
   - save the outputs.
4. **Remove the readers** (F.1) on a branch: `convert.py` except `open_repo` (moved), `backfill.py`, `_old_words`, the prefix strips, the `3-requests` cleanup, intake's call. Drop the scenario cases `old_words`, `old_tree`, `backfill_cases`, `release_on_stack` §15, and `World.at`'s prefix (l.182). Then:
   - rerun step 3's commands with the new CLI and diff the outputs; they should be identical;
   - run `just check`, then `just scenario` (a CLI change, per AGENTS.md).
5. **Docs.** Remove the `scenario/README.md` lines for 14d (old words), 14f (old tree) and 14g (backfill), and any card or doc line that promises conversion of an older tree **(not searched; check)**.
