# CR-160 investigation (round 0)

Read in the worktree (base origin/main). Tree is `4-batch/` (singular), one batch at a time, `batch.json` at `4-batch/`.

## Map of the CLI (`skills/chantier/scripts/cli/src/chantier/`)

- `state.py` (454 lines). `CHANGES = .agents/changes` const; `Repo(root, git_dir, config)`; `Repo.find(cwd, convert)` takes `cwd` from arg, then `CHANTIER_ROOT`, then `os.getcwd()`, uses `git --git-common-dir`, and runs `convert_old_tree`. Properties: `changes` (= root/CHANGES), `batches` (= changes/4-batch), `worktrees` (= `<root>.worktrees`), `next_batch_number` (`changes/.batch-number`). `Batch.__enter__/__exit__` writes `batch.json`, `events.jsonl`, `.batch-number`, `.lock` in `4-batch/`, then `write_batch`/`write_dashboard`. `project_path(root, value)` checks "inside the repository" and is the one check to split (planning folder vs project root).
- `lifecycle.py`: `stage_layout` (base = `repo.changes`), `changes_lock` (`.lifecycle.lock`), `project_path(repo.root, ...)` at 67, 111, 120, 186, 308, 330; `cr["path"] = target.relative_to(repo.root)` at 126 and 368; `convert_old_tree` (258, `3-requests`).
- `commands.py` (2077 lines), with `Repo.find()` at ~25 sites (one per command). Sites to change:
  - `cli_command()` 73; `_shown` 93 (relative to root); `project_instructions` 104; settings read 156 (P10).
  - `preflight` 171-237: P6/P7 use `repo.root`/`repo.git_dir`; P8 `project_instructions`; add the default-branch line and clone check for external mode.
  - `init` 242; `file_cr` 286 (`repo.root / source` at 292); `abandon` 322 (325); fix 382; `add_cr` 390 (`origin` 402, `path` 409 relative to root, `worktree` 406 from `repo.worktrees`).
  - `open_batch` 523 (remote and default branch from `repo.root` at 528, 530; brief "Project instructions" 585).
  - `seat` 652, 666 (`changes/seat.json`); `_facts` 1203 (the `cli:` line is `cli_command() <command> --batch`); `handoff` 1249; `take` 1256; `order` 930 (merged -> `delivery.md`); `rules` 1406 (single file now, `repo.root`); `.long-gate.lock` 1425, 1439; `gate` 1487; `ship` 1523 (read-only git; the archive check); `close` 1696 (`.closing-<batch>` in `changes`; transcripts at 1805, 1849 call `costs.transcript_path(repo.root, ...)`).
- `status.py`: `repo.root / c["path"]` at 184, 242, 367, 430, 448; `_link(folder, repo.changes)`; `write_dashboard` 454 (STATUS files must be ignored).
- `costs.py`: `transcript_path(repo_root, uuid)` 42; used by `rails.py:45` `idle_seconds(repo.root, ...)`.
- `cli.py`: `_parser`'s `cmd(...)` helper adds `--batch`; no global option today. `main` runs `args.fn`; `FULL_OUTPUT` and `MAX_LINES` stay. A global `--project` goes on the top parser, before the sub-command (as the spec says), and must reach `Repo.find` (a module-level setting or an `args.project` read by `Repo.find` callers: the simplest is one `Repo.find()` that reads a module variable set in `main`; check that `commands.py`'s 25 `Repo.find()` calls need no edit).
- `CHANTIER_ROOT` exists in `Repo.find`; the scenario pops it. Concepts rule 9 forbids a leading assignment, so a `--project` in the `cli:` line is the way for the worktree calls.
- Python dependencies: none; keep a tiny `checkout.yml` parser (`key: value`, `#`).

### What to add (CLI)

1. `Repo` gains `mode` ("project" | "external"), `surface` (root), `project_dir`, `clone`, `worktrees_dir`; `root` stays the code repo (the clone in external mode), `changes` becomes the planning folder. `find(project=None)` resolves per the spec: `--project` (absolute or bare name inside the surface), a surface auto-detected by `projects/*/checkout.yml|changes` with no `.agents/changes` (one project taken; several: exit 2 with the names), else in-project. `git_dir` for P7 is the surface's in external mode.
2. `cr["path"]`, `origin` relative to the planning folder; readers accept the old `.agents/changes/...` form (strip the prefix when present). Replace `repo.root / c["path"]` (status.py x5, lifecycle x4, commands 402/409/1751) with a `repo.changes`-based helper.
3. `.gitignore` in the planning folder, written before any local file (`init`, `file`, `open`, `take`, `gate`, `seat take`): `4-batch/batch.json`, `events.jsonl`, `brief.md`, `STATUS*`, `.lock`, `.lifecycle.lock`, `.long-gate.lock`, `.batch-number`, `seat.json`, `work/gates/`, `*.log`, `.closing-*`. Check exact filenames against what `write_batch`, `write_dashboard` and `status.py` write, because the dashboard files at `changes/` also need an entry.
4. `_facts`: absolute paths; external mode adds `clone:`, `archive:`; `cli:` line carries `--project <abs folder>`. `delivery.md` on `order merged`; `ship` flags a missing archive; archive stamp kept in the CR record at the first `take`.
5. `rules`: two headings `project:` and `surface:`; `preflight`: surface checkout on its default branch (warn), clone missing -> FAIL naming path and `project.md` remote; `init` in external mode refuses a linked worktree and never writes `project.md` or `checkout.yml`.
6. `costs.transcript_path` from the session's own folder (the surface root); `project.md` line `- Archive in the PR: yes|no` parser.

## Tests (`skills/chantier/scripts/cli/tests/test_structure.py`, conftest `repo`, `chantier` fixtures)

- Existing: `test_the_plugin_runs_with_no_setup_and_writes_only_in_agents_changes` (line 195): rename to "planning folder", add the external variant (temp surface with one project, bare clone, `preflight`, `open`, `take`, `git status --porcelain -uall` shows only `projects/<n>/changes/` documents and none of the local files; the clone stays clean).
- Keep few and fast; the links test (`test_skill_and_references_links_resolve`) must cover `docs/planning-modes.md` (check its glob; the new page needs the README link).
- Other tests that name `.agents/changes` or `repo.root` (seat 143, init 302) must still pass.

## Scenario (`scenario/run_scenario.py`, 2839 lines, `just scenario` = github then gitlab)

- `World` (build: one project `proj` with bare `origin.git`, `state = proj/.agents/changes`); `scenario(w)` runs the in-project run, then sub-runs (`seat_handover`, `direct_batch`, ...). Helpers `Foreman`, `start_driver`, `commit`, `push`, `ship`, `driver_round`, `prepare_cr`.
- Add a function `external_surface(w)` called from `main` after `scenario(w)`: a second World-like build (surface repo with a bare origin; `projects/demo` and `projects/other`; `checkout.yml` to a clone outside the surface with its own bare origin; `project.md` of `other` with `- Archive in the PR: no`). Reuse the fake forge and `driver_round`. The checks are the spec's "Evidence" list. The in-project run is unchanged and still passes first. Env: `CHANTIER_ROOT` is popped, so only `--project` carries the context.
- `World.state` and `w.work` are hard-wired: the external run needs a parametrised copy (a `Surface` helper) rather than edits to the 70 existing uses.
- `scenario/README.md`: the external run's checks; "outside `.agents/changes/`" -> "the planning folder".

## Board (`hooks/register.tsx`, `register.test.tsx`)

- `INDEX = '.agents/changes/STATUS.json'` (line 23); `findRoot` reads `git-common-dir` (124); `crUrl` builds `root + '/.agents/changes/' + dir` (384). In a surface: read `projects/*/changes/STATUS.json`, one section per project. Which round: the spec lists it in the CLI part; put it in round 1 (small, TS, tested in `register.test.tsx`; `just check` does not run it, so say so in the evidence).

## Cards, hosts, docs that name `.agents/changes` (the grep)

`README.md`, `CONTRIBUTING.md`, `docs/{cr-folder-lifecycle-texts,cr-lifecycle-simple-texts,how-chantier-works-texts,release-process,tutorial-claude-code,use-cases}.md`, `skills/chantier/references/{chief-of-staff,concepts,foreman,griller,init,pr-template,session-start}.md`, `skills/{chantier,chief-of-staff,griller,status}/SKILL.md`. No `agents/*.md` nor `com.github.copilot/agents/*` body matches the grep: no host change expected (still check `routing.md` and `spec-writer.md`, which the spec names, for wording only; `driver.md` and `worker.md` have no match, but get new text). `docs/release-process.md` and `skills/status/SKILL.md` are not in the spec: leave them unless they describe the planning folder as the place for the plan.
New: `docs/planning-modes.md`, `docs/planning-modes.svg`, `docs/planning-modes-texts.md`. SVGs to edit: `how-chantier-works.svg`, `-simple-direct.svg`, `-simple-foreman.svg`, `cr-folder-lifecycle.svg` (and `cr-lifecycle-simple.svg`), each with its `*-texts.md`.
Also `AGENTS.md` (project rule line: say it in the PR) and `references/hosts/{claude-code,copilot}.md`.

## Proposed split

**Round 1: CLI, tests, scenario, board.** Everything under "What to add", in this order: state.py `Repo` + parser, relative paths, `.gitignore`, `cli.py --project`, `commands.py` (preflight, init, rules, _facts, take, order merged, ship, close, seat, gate), `costs`, board. Then the structure test and the external scenario run (both forges), `scenario/README.md`. Gate: `just check` and `just scenario`. This is the heavy round and the only one with the long gate.

**Round 2: cards, hosts, docs, diagrams.** concepts, session-start, chief-of-staff, griller, foreman, driver, worker, init, pr-template, routing, spec-writer, the three SKILL.md, hosts (the user's finding for remote, the unproved folder-access rows with the "For you" block), `AGENTS.md`, `CONTRIBUTING.md`, README (Planning modes section, positioning, tree), `docs/planning-modes.md`, use-cases and tutorial lines, the SVGs with texts, and PNG renders. The round also writes the card lines that the CLI now prints (`clone:`, `archive:`, the `.gitignore` rule). Gate: `just check` only (docs and cards alone need no scenario; but the PR passes it from round 1).

Dependency: round 2 reads round 1's final CLI names (`--project`, `clone:`, `archive:`, `delivery.md`, the `.gitignore` list): the round 1 report must list them.

## Risks to watch

- `Repo.root` is used as both the code repo and the planning base in ~40 places: a missed site silently writes in the clone. Grep `repo.root` after the change; only git calls and the project's instruction files should keep it.
- Windows: `checkout.yml` paths with `\`, `Path.resolve()`; `msvcrt` lock stays on `.lifecycle.lock` in the planning folder.
- The scenario's in-project run must stay green: it hard-wires `w.state`.
- `convert_old_tree` runs in `Repo.find`; in external mode it must run on the planning folder, not touch the surface root.
- The 10-line output limit: `preflight` and `rules` gain lines; check `MAX_LINES` and `FULL_OUTPUT`.
- PNG renders: need a renderer on the box (check for `rsvg-convert`, `inkscape` or a headless browser before round 2; if none, say it at once). Upload goes through the forge CLI per driver.md.
- Wording: "the `3-ready` folder" vs "a PR ready to merge"; "no epoch" word (the CLI has `--epoch` already: do not touch it, do not write the word in new text).

## Evidence plan

- `evidence/check.log` (summary, not raw): `just check` result on the host; Linux and macOS come from CI.
- `evidence/scenario-github.md` and `scenario-gitlab.md`: the results transcripts from `scenario/results/` (pass counts, the external checks listed).
- `evidence/external-status.txt`: the `git status --porcelain -uall` of the surface after each scenario step (the spec's list of ignored files, absent).
- `evidence/structure-test.txt`: the external variant test passes.
- `evidence/board.txt`: the register test run (`hooks/register.test.tsx`) result, or the statement that it has no runner.
- `evidence/diagrams/*.png`: one render per new or changed SVG, uploaded in the PR description; the PNGs stay out of the diff unless the repo already tracks them.
- `evidence/rules-grep.txt`: `grep -n ".agents/changes"` before and after on the cards, showing each remaining mention is an in-project one.
- The host trials stay marked unproved; no evidence claims otherwise.
- The PR description names the `AGENTS.md` rule change.
