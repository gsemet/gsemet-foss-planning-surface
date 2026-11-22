# Verify CR-437

Head: 20b7e694842421d08e5879b2e221887f923e7ce3

Verdict: VERIFIED

Claims, all judged at e21be68929ed9d6136d18167c300592a51c5c1a5 (pushed head, PR 409, worktree clean):

1. Shipped-text, byte-identity, moved-rule, startup-bytes, command_for and P10 tests pass.
   Command: `uv run --no-sync --project . pytest tests/test_launch_modes.py test_plugin_files.py test_startup_manifest.py test_allow_rules.py test_cli_runs.py -q` (cli/tests).
   Output: `106 passed in 28.17s`.
2. SKILL.md paragraph (4 skills): `grep -c "its mode checked once"` gives 1 in each of the four SKILL.md files. The chief-of-staff paragraph holds the check line `uv sync --locked --check --project "<plugin root>"`, "The environment is outdated", "Never stop or kill", `sync pending: held by`, "3 minutes", "but a reload", and the exception "except a sync held as above (`sync pending`)" after "follows `startup-core.md`".
3. session-start.md "6. Sync the checkout" holds the six steps, "No third line", "no second question", "is no longer own", "unless another session's watcher takes it", own-evidence `--seat <this session's id>` and `board already running` (read with `sed -n '/6. Sync the checkout/,$p'`).
4. Host rows: `grep -n "Name the holders"` finds the row in hosts/claude-code.md:39 and hosts/copilot.md:39; the check rule row is at claude-code.md:270.
5. chief-of-staff.md:1138 "one exception is your own board and watcher, on the user's yes"; status-layout.md:102 holds "but a sync pending more than 3 minutes", "until the user answers", "a later yes still counts", and still "It is not a **For you** item: nothing waits on the user". The moved-rule grep (`synced once by`, `run \`uv sync`) finds nothing in chief-of-staff.md and concepts.md.
6. The check's trial by hand, uv 0.13.6 (329bf9448 2026-10-26 x86_64-pc-windows-msvc), throwaway project in work/scratch (git-init'd, a hatchling package so the project itself is installed; removed afterwards):
   - `uv sync --locked`, then `uv sync --locked --check`: `Would make no changes`, exit 0.
   - Version bump in pyproject.toml and in uv.lock's own package: `error: The environment is outdated; run \`uv sync\` to update the environment`, exit 1.
   - Dependency added to pyproject.toml only: `--check` exit 1 with the same text; real `uv sync --locked` exit 1: `error: The lockfile at \`uv.lock\` needs to be updated, but \`--locked\` was provided.`
   - Note: with a project that has no build-system (virtual), a version bump gave exit 0; chantier is a package, so the bump case holds (it is the PR's case).
7. Gates: CI at the head green (`gh pr checks 409`): check macos, ubuntu, windows; eval-dry-run; scenario (ubuntu). Local gate log first line: `gate CR-437 ... head e21be68929ed9d6136d18167c300592a51c5c1a5`.
8. Review box: `$CHANTIER log CR-437` has the note "r1 approved at c5af034..., committed as e21be68929ed..."; the box "approved at e21be68 (carried from c5af034, same content)" matches it.
9. PR description (as posted): renders (sections, mermaid, fold); Summary, Deliverables and Changes match the 21-file commit; Known gaps lists the card-behaviour gap, the first-release proof, the prompt, macOS/Linux, untested listings, process tree; no images. The test plan's Evidence, Verified and CI boxes are still unticked and `<sha7>` placeholders remain: Driver fills them after this verdict (the Evidence box is now proved by claim 6). No role name outside the product terms.

Not run, by design: behaviour of the sync steps (card text, a Known gap, named in the PR).

## Description pass (closing), judged at e21be68929ed9d6136d18167c300592a51c5c1a5

Head: e21be68929ed9d6136d18167c300592a51c5c1a5

- Command: `gh pr view 409 --json body -q .body`, against `git diff --stat c5af034 HEAD` (21 files) and pr-template.md. Sections in order (Summary, Deliverables, Blast radius, Autonomous decisions, Known gaps, then one Details fold with blank lines, nothing after it); Human decisions present; CR name and batch only in Internal references; no role name as doer; Test plan boxes name e21be68; Review box matches `chantier log` note "approved at c5af034, committed as e21be68"; names (`launch.sync_check_line`, `plugin_files.sync_check_command`, `session-start.md` section 6, startup budget 12544 / 11383 / 12178 in work/r1b.md) match the diff; no image. Known gaps cover the unproved card behaviour. Description clean and consistent: VERIFIED.

## Move verification (rebase with conflict, e21be68..20b7e694), judged at 20b7e694842421d08e5879b2e221887f923e7ce3

Head: 20b7e694842421d08e5879b2e221887f923e7ce3

Verdict: VERIFIED

Move touched: hosts/claude-code.md (conflict, Every batch row), startup-core.md (11-byte tightening), status-layout.md (context), startup-manifest; base brought 80 files (`git diff --name-only c5af034b 0e36d1f8`), among them those cards. `git range-diff c5af034b..e21be68 0e36d1f8..20b7e694` shows the row resolved as main's force-push route kept whole plus CR-437's sync wording and the `--check` rule.

1. Claim 1 judged again at 20b7e694: `uv run --no-sync --project . pytest tests/test_launch_modes.py tests/test_plugin_files.py tests/test_startup_manifest.py tests/test_allow_rules.py tests/test_cli_runs.py -q` (cli/): `106 passed in 14.91s` (startup byte budget included).
2. Conflict resolution judged again at 20b7e694: `grep -c "<<<<<<<\|>>>>>>>"` on hosts/claude-code.md gives 0; `grep -c "uv sync --locked --check --project"` gives 4 (rule, rule table, row, trial); "Name the holders" is 1 in claude-code.md and 1 in copilot.md; `sync pending` in startup-core.md 1; "but a sync pending more than 3 minutes" in status-layout.md 1.
3. Claims 2-6, 8 (skill paragraphs, session-start, chief-of-staff, uv trial by hand): carried from e21be68: files the move did not change (range-diff shows only the three card files above differing); claim 6 is a uv behaviour, independent of the base.
4. Gates: `gh pr view 409 --json headRefOid` gives 20b7e694842421d08e5879b2e221887f923e7ce3 (pushed head = worktree head, clean). CI running in parallel, not waited for; `just check` and `just eval-dry-run` reported passed locally by the Driver (not rerun by me). Review box: the Inspector approved the move per the brief; the Driver fills the box and CI boxes at the new head (not re-judged here, description pass carried from e21be68 save that the SHA in its Test plan boxes must move to 20b7e69).
5. Known flaky: conflicts.md notes `test_w2_a_shell_inside_the_folder_refuses_then_lets_go` failing in a full local run only, passing alone; CR-437 touches nothing near it; reported, not mine.
