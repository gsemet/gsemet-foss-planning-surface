# CR-111 investigation: a batch is numbered, single and a stack by default

Read in the worktree `C:\Users\gaeta\Projets\chantier.worktrees\batch-folder-CR-111`. Paths are
relative to it. CLI sources are in `skills/chantier/scripts/cli/src/chantier/`.

## Files and entry points

- `state.py`: `Repo.batch_folders`, `batch_dir`, `next_batch_number`, `open_batches`;
  `Batch.__init__`/`__exit__` (number, folder, `.batch-number`); `resolve_batch`, `find_cr_batch`,
  `read_batch`, `check_epoch`.
- `commands.py`: `add_cr` (branch, worktree, CR folder), `open_batch`, `foreman`, `_apply_order`
  (`order add/merged/slots`), `_stack_base`/`_base_of`, `take` (stack branch), `stack`,
  `land`, `close`, `_landed_batch`.
- `cli.py`: `open` parser (positional name, `--slots default=2`, `--stack`), `--batch` help.
- `status.py`: `batch_view` (`batch: d["id"]`, `folder: folder.name`), `cr_view` (`batch: d["folder"]`),
  `dashboard_view`, `batch_markdown`.
- `rails.py`: refusals keyed on a `Batch` (budget, slot, round, archive on merge).
- Not touched: `lifecycle.py` (only uses `batch_folders` / `batch.dir`), `costs.py`, `procs.py`.

## Smallest change (summary)

1. `Repo`: drop the `\d+-name` match. `batch_dir(batch)` normalises `4`/`04`/`batch-04` to
   `batches/batch-04`. A helper `normalize_batch(str)`; call it in `resolve_batch` (it covers `--batch`
   and `$CHANTIER_BATCH`) and in `_landed_batch`/`close`, which read `args.batch` directly.
2. `next_batch_number`: parse the folder number with `re.search(r"\d+", d.name)`, not
   `d.name.split("-")[0]` (that gives `batch` and `int()` raises).
3. `Batch.__init__` create path: id and dir are `batch-{n:02d}`; `open_batch` no longer takes a name
   (`args.batch` goes, the items become the first positional) and sets `data["id"]` from the
   number. Remove the id regex check. `brief.md` title `# Batch batch-05` becomes `# batch-05`.
4. `open_batch`: refuse when any folder with a `batch.json` exists (see 2). Default `--slots` 4 in
   `cli.py:46`. Drop `--stack`, add `--parallel` (`mode = "parallel" if args.parallel else "stack"`).
5. State and cards for the stack (see 3), scenario, tests, docs (see 4).

## (1) Where the batch id, folder, branch and worktree names are read or built

- Built: `commands.py:316` branch `chantier/{b.id}/{cr_id.lower()}-{slug}`; `:317` worktree
  `repo.worktrees / f"{b.id}-{cr_id}"`; `:312` CR folder `b.dir / f"{number:03d}-{slug}"`;
  `state.py:259` batch dir `f"{n:02d}-{batch_id}"`; `commands.py:357` `"id": args.batch`.
  With id `batch-05` these come out as spec'd with no further change (`chantier/batch-05/...`,
  `<repo>.worktrees/batch-05-CR-111`).
- Read by name: `state.py:233-236` (`batch_dir`, the `\d+-name` regex), used in
  `commands.py:275` (`_cr_events`), `:1217` (cost events), `state.py:375` (`read_batch`);
  `resolve_batch` (`state.py:352`) returns the bare string from `--batch`/`$CHANTIER_BATCH`/the
  only open batch's `id`; `find_cr_batch` returns `b["id"]`; `_facts` prints `--batch {batch}`
  (so a Driver is handed `--batch batch-05`: fine).
- Display: `status.py:148` `cr_view["batch"] = d["folder"]`, `:217/:305` `batch`+`folder`; the
  hook shows `b.batch` as the title and keys folds on `b.folder`.
- How an old record stays readable:
  - A merged CR is moved to `4-archives/<stamp>-<NNN>-<slug>` (`lifecycle._retire`): no batch name
    in the folder name. Its `STATUS.json` holds `batch: "03-foo"` (the old folder name), shown as an
    opaque string by `status._past` (`s.get("batch")`): readable, untouched. No code parses it.
  - A CR's `branch` and `worktree` are stored in `batch.json` and used verbatim (`_worktree`,
    `ship`, `close`): an old-form record keeps working.
  - A live batch folder `NN-name/` with `batch.json` stays found by `batch_folders` (it globs any
    dir with `batch.json`), but `batch_dir("name")` would no longer match it once the regex goes.
    The spec says run only when no batch is open, so this is not a concern; if wanted,
    keep a fallback: none (no-fallback rule), just document.
  - `next_batch_number` still reads `max(.batch-number, folder numbers)`: old `04-x` folder gives 5.
- Mixed sort: `batch_folders()` sorts by name; `04-x` < `batch-05` < anything. Irrelevant at one open
  batch, but the dashboard lists landed ones too; order stays chronological since digits < letters.

## (2) `open`, `.batch-number`, the one-open-batch refusal

- Today: `open_batch` takes `args.batch` (name), holds `changes_lock(repo)`, builds `Batch(create=...)`.
  `Batch.__init__` calls `repo.next_batch_number()` = `max(.batch-number content, folder numbers) + 1`,
  sets `dir = 3-requests/<NN>-<name>`. `.batch-number` is written in `__exit__` only if events
  were logged (state written), so a failed `open` burns no number. A failed `open` removes the empty
  folder.
- Number is stable under concurrent `open`: the number is chosen inside `changes_lock`.
- The refusal: `Repo.open_batches()` excludes `landed`, but the spec says "whatever its state until
  `close`", so the test is `repo.batch_folders()` non-empty (landed ones are included; `close`
  deletes the folder). The check goes in `open_batch` right after the lock is taken (before
  `prepared_cr`). Exit 2 = `EXIT_PRECONDITION` (`concepts.md:51`: 2 precondition), not `EXIT_USAGE`
  (1). Naming which batch: `batch-NN (landed)`, plus "order add joins it".
- rails.py fit: rails.py holds refusals on a `Batch` (`check_take`, `check_budget`...); a check with no
  `Batch` yet (a repo-level refusal) is a new shape, but fits "the CLI says what it refuses". Put
  `check_no_open_batch(repo)` there and call it from `open_batch`; or keep it inline in
  `commands.py` if you want no new function. Either is consistent with AGENTS.md (the rail
  knows no role).
- Side effects to handle: `resolve_batch` with exactly one folder still works; `find_cr_batch`
  keeps working. `land` leaves a landed batch that blocks `open` until `close`. The scenario
  opens ~10 batches in sequence (`night`, `latin`, `stuck`, `halt`, `rails`, `ship`, `fixes`, ...);
  most never `close`: each needs a `close --yes` first or a fresh workspace (see 4).
- `ensure_unclaimed` (lifecycle.py:79) already skips landed batches; no change.

## (3) A stack merged in part: what the state and rails say today

State holds `mode` ("stack"|"parallel"), per-CR `order`, `status` (merged/cancelled/...),
`stack_agent`. Facts:

- `_stack_base` (`commands.py:696`): in stack mode, the chain is the CRs sorted by `order` and
  not `cancelled`/`merged`; a CR's base is the previous one's branch, the first one's the
  default branch. So after `order merged` of the bottom CR, the remaining CRs already re-chain on
  the default branch, in the state: `take`'s facts (`base`) and `ship` (`base=`) recompute it.
  This is what the spec wants, and no state change is needed for the base.
- `archive_merged` (rails) moves the merged CR to `4-archives/` at once and alone: matches the spec.
- `take stack` (`commands.py:776`): lists the live chain, refused if `stack_agent` is still
  recorded (`agents set stack -` first; foreman.md:52 already says "again after a merge"). So the
  "second stack, same batch" loop exists: merge -> `agents set stack -` -> `take stack`. `land`
  refuses while `stack_agent` is set.
- `stack <cr>…` only sets `order` on the CRs named (others keep theirs).
- `driver.md:61-67` and `agents/stack-driver.md` (identity block only; the role is the card):
  "rebase and push each PR on the one under it". Nothing says what to do after a partial merge:
  the first remaining PR has to be retargeted to the default branch (`gh pr edit --base`) and
  rebased on `origin/<default>`. Card change needed in driver.md only; `stack-driver.md` keeps
  its body identical on both hosts (`com.github.copilot/agents/` unchanged since the card carries the role).

What state and rails cannot say (gaps):

1. Queued CRs sit in the chain. `_stack_base` filters only cancelled/merged, so a queued CR (no
   branch yet) is the base of the next one; and a CR joined by `order add` (`order` = max+1) lands on
   top of the chain, based on a branch maybe not created. With `--parallel` gone as default this
   matters: `take` of the third CR prints `base chantier/...cr-2` before CR-2 has a worktree.
   Likely fix: the chain is the non-queued, non-ended CRs? Questions for the user: does a stack
   build bottom-up in order (a CR starts only when the one below has a branch), or all at once?
2. Kinds in the chain: `release` and `fix` CRs are not stackable (release starts once the others
   are merged; a fix is on the default branch). `_stack_base` ignores `kind`; with stack as the
   default, a release CR is chained on the CR below it. The chain should skip `kind` in
   {release, fix} (base = default).
3. No record of "restacked": nothing marks that the remaining chain was rebased after a merge;
   the stack driver's ship events carry `base`, which is enough proof (`ship` logs `base`). A
   minimal addition is a `restack` hint in `take stack`'s output: for each live CR, its base now vs
   its recorded PR base. The `ship` event's last `base` per CR is in `events.jsonl`; no new field is
   required unless the user wants one.
4. `stack_agent` is a single slot: a batch with several stacks "in turn" is exactly this slot used
   repeatedly (never two at once). No change; just say so in the card.
5. `stack` refuses a batch of mode `parallel` (`:1066`); `take stack` too. With `--parallel` nothing
   changes.
6. A batch with 1 CR is a "stack" of one: base default; `take stack` pointless but harmless; the
   Foreman card says when it takes the stack ("open CRs all ready or blocked").

## (4) Where the names appear (to change or check)

- `<NN>-<batch>`, `<NN>-<name>`: `README.md:177,181,188-189`; `CONTRIBUTING.md:26`;
  `skills/chantier/references/concepts.md:26,29-31`; `chief-of-staff.md:74,88,92-93`;
  `docs/cr-folder-lifecycle.svg` (line 41 text `&lt;NN&gt;-&lt;batch&gt;`, and the long line 3) and
  `docs/cr-folder-lifecycle-texts.md:3,54`; `evals/kit/audit.py:248-255` (`\d+-name` regex,
  `folder.name.split("-", 1)[1]`); `state.py:4` docstring. The grep in the spec ("<NN>-<batch>")
  also hits those SVG/texts lines. `cr-lifecycle-texts.md`/`how-chantier-works-texts.md`
  mention stacks/slots generically: check for a diagram that says "parallel by default".
- A batch name in a command: `chief-of-staff.md:70` (`open <batch> …`), `:77-97` (prompt
  `Foreman of batch <batch>`, `--batch <batch>`, titles `Foreman [batch <NN>]` (now simply the
  batch id)); `evals/real/RUNBOOK.md:10`, `evals/claude-smoke/RUNBOOK.md:19` (`open smoke`),
  `evals/claude-full/RUNBOOK.md:35` (`open full`), `evals/copilot/RUNBOOK.md:22`
  (`open copilot`); `docs/tutorial-claude-code.md:109`; `foreman.md:30,45,65,66,81` and
  `routing.md:11` (`ready <batch>`: still fine with the id, since `<batch>` becomes `batch-NN`);
  `concepts.md:63` (prompt shape).
- `--stack`: `cli.py:48`, `commands.py:358`, `chief-of-staff.md:71`; the cards say "in parallel or as
  a stack" at `concepts.md:29`, `SKILL.md:38`. README:51,53 (the stack driver), `docs/use-cases.md:39-45`
  ("build them as a stack" becomes the default: rewrite the section as "independent CRs").
- A default of 2 slots: only `cli.py:46` (`default=2`). No card or README gives "2 slots" (README/
  cards say "slots" without a number; `docs/use-cases.md:31` says three slots as an example).
  `scenario/run_scenario.py:430,958` pass `--slots 2` explicitly (unaffected).
- Scenario (`scenario/run_scenario.py`): every `w.chantier("open", "<name>", ...)` (lines 427-430, 804,
  809, 837, 861, 958, 1104, 1142, 1191, 1230, 1293, 1372), `--batch night`/`halt`/... (643, 648, 777,
  783, 1136, 1182, 1218, 1222, 1339, 1345, 1374), `w.name`, `CHANTIER_BATCH` (838, 863, 960, 1105...),
  paths asserting `/3-requests/01-night/` (444), `[Batch 01-night](01-night/STATUS.md)` (464,
  706), `"01-night" not in board` (795), `w.folder()`. No scenario case runs a stack (grep: only line
  209 `target != "stack"`); a new one is needed for the stack merged in part, a second `open` refused and
  an `order add` joining. It also needs a `close --yes` between its batches.
- Tests: `skills/chantier/scripts/cli/tests/test_structure.py` and `test_costs.py` do not name a
  batch (grepped: only the role lists); `register.test.tsx` (hook) uses fake `batch: 'demo'`,
  `folder: BATCH`: unaffected.

## (5) Reusing a Foreman session

- The epoch claim: `batch.json["foreman_epoch"]`, set by `foreman set <session> --epoch n`
  (`commands.py:399-410`), accepted only if `n == current + 1`; it also clears `foreman_transcript`.
  Every Foreman command carries `--epoch`; `check_epoch` refuses a different one (exit 3). A
  second `foreman transcript` with another uuid is refused (`:414-418`).
- Consequence for reuse: a new batch has `foreman_epoch` 0 and a new folder, so the "next epoch"
  of a reused session is `1` again (the Chief of Staff's rule `1, else foreman get + 1`
  yields 1). The old Foreman's stale commands carry `--batch batch-04` (closed folder, so
  "unknown batch") so no cross-batch confusion by epoch: the guard is the batch id, not the epoch.
  Spec text "with the next epoch" is then true only for a Foreman of the same batch (a restart);
  say in the card that a reused session is told the epoch of the new batch (1).
- The transcript: `foreman transcript <uuid>` is stored; `cost` reads that transcript from the batch's
  `created` timestamp (`costs.session_costs(path, d["created"])`), so a reused (or compacted)
  session's cost for batch N+1 excludes rows before its `created`. `/clear` may change the
  uuid: `chantier cost` would then miss the old part, as the spec says.
- Not in the CLI: whether a message reaches a stopped session is a host fact (SendMessage / a `send_message`
  tool of `ccd_session`). Nothing in the repo proves it.
- What a host test would need: Claude Desktop (or a Remote Control session) with the `ccd_session`
  tools (`start_session`, `get_session("self")`, send), the plugin loaded, a throwaway repo with a
  remote, two batches. Steps: start Foreman 1, let it `land`; `close`; `open` batch 2; (a) with the
  session alive and idle, send the new prompt; (b) after stopping the session (process ended), send
  it and look for a wake; (c) the user pastes it into the stopped session. For each: assert
  `foreman get` shows the reused session id with epoch 1 and the transcript uuid stored, a second
  session refused with exit 3. It runs on a host, by hand, in `evals/` (a runbook line next to
  `evals/real/RUNBOOK.md`), never in `just scenario` (no host). The card says only what was proved.
- Heartbeat: the first Foreman ended its `/loop` after `land` (foreman.md:67-68); the reused
  Foreman must arm a new one: say so in foreman.md.

## The mod (hooks/)

`hooks/register.tsx` reads `.agents/changes/3-requests/STATUS.json` (`INDEX`) and each CR's
`STATUS.json`. It uses `b.batch` (displayed on the fold title, line 426) and `b.folder` (the fold
key, `batch-<folder>`, line 422; also relative CR paths). It does not parse the name or number
and works with `batch-05` for both. `STATUS.json` keeps its fields (spec). One cosmetic point:
the title shows `batch-05` twice if you also show the folder. No change is needed.

## Risks

- `int(d.name.split("-")[0])` crash on `batch-05` (state.py:242): must change with the folder name, or
  the second `open` raises `ValueError`.
- Scenario heavy rewrite: ~12 `open` calls and the one-open rule: the long gate is the cost.
- `release`/`fix` CRs in a default stack (gap 2) and queued CRs in the chain (gap 1): behaviours the
  spec does not mention and that break once stack is default.
- `--parallel` flips the default: every runbook that opens a one-CR batch gets a (harmless) stack of one.
- `just check` includes the card/agent structure test: a card edit must keep `agents/` and
  `com.github.copilot/agents/` bodies identical (no role body changes needed here).
- Version: do not edit by hand.

## Questions for the user

1. Stack chain: does a queued CR with nothing below it yet start at once (all in parallel up to the
   slots, each PR based on the previous branch), or only once the CR below has a branch? And should
   `release` and `fix` CRs sit outside the stack (base = default)? My recommendation: yes, outside.
2. After an `order add` to a batch that has a stack merged in part: does the new CR go on top
   (current behaviour, `order` = max+1)?
3. For the reuse of a Foreman, the new batch's epoch is 1, not "the next" of the old one: confirm the
   wording, since there is no stale-epoch protection between batches (the batch id protects).
