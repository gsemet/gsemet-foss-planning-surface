# CR-191 investigation: map for dry_run.py and sandbox_forge.py

Read in the worktree (base d6271d4). Paths are under `evals/kit/` unless noted.

## 1. gh and git calls the kit makes

sandbox.py (REPO `gsemet/chantier-eval-sandbox`, URL `https://github.com/<REPO>.git`, BRANCH main):
- `gh auth status` (stdout+stderr): needs a line with "scopes" containing the word `workflow` (quotes and commas replaced by spaces).
- `gh repo view REPO --json defaultBranchRef`: `defaultBranchRef.name == "main"`.
- `git config --get-regexp ^credential\..*helper$` (inherits os.environ; GIT_CONFIG_COUNT/KEY_0/VALUE_0 in the dry run's own env work).
- `git ls-remote URL` through `remote_refs()`: only refs/heads and refs/tags kept, `^{}` ignored. refs/pull is therefore ignored by reset verify.
- `gh pr list --repo REPO --state open --limit 1000 --json number,title,headRefName`.
- `gh release list --repo REPO --limit 1000 --json tagName`.
- reset plan: `gh pr close <n> --repo REPO`; `gh release delete <tag> --repo REPO --yes`; `git push URL --delete refs/tags/<t>`; `git push URL --delete refs/heads/<b>`; `git push --force URL base:refs/heads/main`. Without `--yes` it prints "plan only: nothing changed"; verified end state prints "sandbox reset: main at <base>".
- merge (`cmd_merge`): reads `<workspace>.run.json` (`prefix`, `repository == REPO`); `gh pr view <n> --repo REPO --json number,state,title,headRefOid,statusCheckRollup`; then `gh pr merge <n> --repo REPO --rebase --match-head-commit <sha>`. Refusals (stderr "sandbox.py: refused: ...; nothing merged", exit 2): not open; title not starting with the prefix; no check; checks not all green (`(conclusion or state) == "SUCCESS"` for every entry). Success prints "merged PR #n at sha7 into main by rebase".
- `build(dest)` makes the deterministic base commit; its SHA must equal `sandbox.json` base.

setup.py:
- `sandbox_main`: refuses a dest that exists or is inside ROOT; `subprocess.run(["gh","auth","status"])` (line ~250); `survey()` (refuses unless at base, exit 2); `run_number()` = `gh pr list --repo REPO --state all --limit 1000 --json title`, regex `^\[eval (\d+) `, max+1; prefix `[eval N date campaign]`; `git clone --quiet sandbox.URL dest`; `uv run --script CLI init`; `uv sync --locked`; `.claude/settings.local.json` (`permissions.allow`, including `Bash(<merge_command> *)`, `PowerShell(...)`, and for release CRs `git push origin <tag>`, `git -C * push origin <tag>`, `gh release create <tag> *`); copies frozen CRs into `.agents/changes/3-ready/<slug>` plus an "## Eval run" section; writes `<dest>.run.json` (`campaign, run, date, prefix, repository, base, chantier, host, crs`); prints `merge <cmd> <pr>` and the batch `open` lines (`$CHANTIER open <paths> --release N --mode parallel --slots S --budget B --default-branch main`).
- The claude-planted `main()` is the model for the launcher plus `FAKE_GH_STATE` / `LIVE_ORIGIN` env in settings.

audit.py:
- `forge_view`: `gh pr view <link> --json title,state,isDraft,baseRefName,autoMergeRequest,statusCheckRollup,headRefOid,mergedAt`, no `--repo`; the link is the recorded URL, so the fake must accept `https://github.com/gsemet/chantier-eval-sandbox/pull/N` and bare numbers.
- C12: `gh pr list --repo <run.repository> --state merged --limit 1000 --json number,title,mergedAt`.
- `git ls-remote --tags <origin>` of the workspace's origin for `refs/tags/vX.Y.Z` (version from the release CR title).
- `real_cost`: `uv run --script CLI cost --batch` in the workspace ("not measured" is not a failure).
- `main_checkout_check`: `git status --porcelain -uall` clean outside `.agents/changes/`.

judge.py:
- Clone of the origin, also fetching `+refs/pull/*/head:refs/remotes/origin/pull/*`; checkout tries `origin/<ref>` then `<ref>`.
- `pytest()`: `uv run --locked pytest -q -p no:cacheprovider`; `release()`: tag on origin, tag ancestor of origin/main, three version places, `uv run python scripts/release_check.py`, hidden tests, then `gh release view <tag> --repo REPO --json tagName,name,body` only if `is_sandbox(repository)` (a local path adds "GitHub release: not run: not the sandbox").

## 2. Where gh and PATH are resolved (change to shutil.which)

Bare `"gh"` call sites:
- sandbox.py: `run()` (cmd[0] bare; FileNotFoundError -> "`gh` is not installed or not on the PATH"), `gh()`, `check_preconditions` (`subprocess.run(["gh","auth","status"])`), reset plan `["gh","pr","close"...]` and `["gh","release","delete"...]`.
- setup.py ~250: `subprocess.run(["gh","auth","status"])`.
- audit.py: `run_cmd` and its callers at ~606 and ~677.
- judge.py ~224: `run(["gh","release","view"...])`.

Fix: `exe = shutil.which("gh")` (honours PATHEXT, so a `gh.cmd` launcher is found on Windows; a bare name finds only `.exe`). `which` searches the PATH of the process, so the dry run sets `os.environ["PATH"]` (fake first) before calling, or passes `path=env["PATH"]`. Keep the "not installed or not on the PATH" message when `which` returns None. No fallback to another tool.

BUG: `def remote_refs(url: str = URL)` binds URL at definition time; rebinding `sandbox.URL` later does not affect it. Change to `url=None` then `url or URL`. Other uses read the module attribute at call time and are fine.

## 3. Launcher pattern for the fake gh

- Windows: `gh.cmd` = `@"{sys.executable}" "{script}" %*\r\n`.
- POSIX: `#!/bin/sh\nexec "{sys.executable}" "{script}" "$@"`, chmod 755.
- State: JSON under an `os.O_EXCL` lock file (as forge.py), a `.calls` log, CI run once per SHA (`state["ci"][sha]`): clone the origin, check out the SHA, `uv run --locked pytest -q`. Merge: rebase in a fresh clone, then ff-only and push to the bare origin.
- Surface to cover: `auth status` (a "Token scopes: ... workflow" line), `repo view --json defaultBranchRef`, `pr create/view/list/checks/merge/close`, `release create/list/view/delete`, `refs/pull/<n>/head` written into the bare origin and never deleted, `statusCheckRollup` of `{name, conclusion|state}` with SUCCESS/FAILURE/pending, `mergedAt` (UTC ISO), `headRefOid`, `--match-head-commit`, `--state open|merged|all`, `--json` field selection. Refuse any `--repo` other than `sandbox.REPO`. forge.py (claude-planted) refuses `pr close` and has no refs/pull; the new fake must not.
- Dry-run process: `GIT_ALLOW_PROTOCOL=file`; rebind `sandbox.URL` to the bare repo path; reach the fake via `sandbox.main([...])` and `setup.sandbox_main(...)` in process; run `audit.py` and the CLI as subprocesses with the same env.

## 4. How audit --sandbox and judge read transcripts

- `data["foreman_transcripts"]` (set by `foreman transcript <uuid> --epoch n`): uuids at `<CHANTIER_CLAUDE_PROJECTS>/*/<uuid>.jsonl`. Agents at `<projects>/*/<uuid>/subagents/agent-*.jsonl` with `agent-*.meta.json` (`agentType`, `toolUseId`, `spawnDepth`). Parent found by matching the parent's assistant `tool_use` block ids to the child's `meta.toolUseId`. Agents whose first record `timestamp[:19]` is before the batch `created[:19]` are "earlier" and skipped. Timestamps must be UTC `%Y-%m-%dT%H:%M:%SZ` (the CLI's `now()`), as must the fake's `mergedAt`.
- First `type=="user"` record content = prompt. Regex `^chantier (?P<role>[a-z][a-z0-9-]*) for (?P<what>CR-\d+|the stack)\b`.
- Every agent: `$CHANTIER rules` in the prompt; drivers (cr-driver, stack-driver, qa-driver, release-driver) cite `references/driver.md`, workers (investigator, coder, inspector, debugger, verifier, conflict-resolver) cite `references/worker.md`.
- J1 `agentType` is `chantier:<role>` or not prefixed `chantier:`. J2 drivers' parent = steering session, workers' parent = a Driver; a cr-driver for each non-release CR and a release-driver if `data.release`. J12 workers' prompt has a `^writes:` line. J3 workers: no git commit/push/rebase/merge (conflict-resolver exempt), no worktree creation; read-only roles Write/Edit only under `/work/` or `/evidence/`; drivers write no code; release-driver writes nothing under src/ or tests/. J4 Driver push needs `--force-with-lease` or `-u`; no `git add -A|--all|.`; each merged CR's worktree created by a Driver `git worktree add`. C12 Drivers never `gh pr merge`. J6 Drivers run `gh pr checks`. J17 peak context <= 200000. J21 no Write to batch.json/events.jsonl.
- Steering session since `created`: C9 `$CHANTIER` calls `status --refresh|cancel|pause|take`, `agents set`, `order done|merged` carry `--epoch`; operator merges (`order merged` without epoch) must not be in the Foreman transcript. J22 no git commit/push/rebase/merge or `git worktree add`. J14 `git worktree remove` before the pause, and `$CHANTIER rules`. Tool names "Bash"/"PowerShell".
- Other rows: C5 gate events carry head and command; C7 each ready/merged non-release CR has a VERIFIED verdict and a passed gate at its head; C11 `release-go` ask then go; J5 per PR (title prefix + " ", no autoMergeRequest, green, merged base == default branch); C12 stray = PR with prefix, `mergedAt[:19] >= created[:19]`, not in the batch; "each merge of the release is recorded with order merged --epoch"; J23 `note <rel> --draft`; `ending_checks`: status paused, all CRs merged, `3-done/<num>-*` and STATUS.md present. `judge_rows` use `git remote get-url origin`, `judge.feature(origin, head, [slug])`, `judge.release(version, origin, merged_slugs)`, `judge.feature(origin,"main",slugs)`.
- PR links come from ship events' `pr`, notes `merged: <link>` (added by `release_merged`, which clears `pr`), and the current `pr`.

## 5. CLI sequence for the scripted Foreman (model: scenario/run_scenario.py World/Foreman/Driver)

env: `CLAUDE_CODE_SESSION_ID`, `CHANTIER_HOST=claude`, `CHANTIER_CLAUDE_PROJECTS=<staged>`, `CLAUDE_CODE_ENTRYPOINT`; invoke as `uv run --script CLI` (as setup prints it).
1. setup (in-process) -> `open` lines -> `foreman set <session> --epoch 1`, `foreman transcript <uuid> --epoch 1`.
2. Per CR: `agents set`, `take <cr> --epoch 1`; Driver `git worktree add`, edit, explicit `git add -- file`, commit, `push --force-with-lease -u`; `round`; `gate <cr> "<cmd>"` (clean worktree, binds to HEAD); `ship <cr> <url>` (needs "://"); `verdict <cr> VERIFIED`; `handback <cr> ready <url>` (needs pr recorded, head == shipped head, clean tree, origin/branch == head, gate passed, VERIFIED at head).
3. Merge: `sandbox.py merge <pr>` (operator path, via `sandbox.main`), then `order merged <cr>` without epoch (moves to 3-done). Foreman's own merge: `order merged --epoch n`.
4. Release CR (waits for the others): `order confirm <rel> --note ...` (no epoch), `take`; `release start <rel>`; `note <rel> --draft <file>`; `release go <rel> --note "<action>"` first logs `ask` (exit 2); then `order approve`/`order grant <rel> --note "releases=1 fixes=on budget=N"`; `release go` logs `go`; release PR merged; tag pushed; `release published <rel> --note ...`; `handback <rel> ready <url>`; `order merged <rel>` appends `merged: <pr>`.
5. `pause --epoch n` (all CRs merged/cancelled, no pending orders or live agents), then `audit.py --sandbox`.

Staged transcripts: write minimal jsonl records (user prompt line, assistant tool_use blocks with ids, Bash/PowerShell calls) and meta.json files satisfying section 4; timestamps >= batch `created`.

## 6. Frozen CRs and hidden tests

`CAMPAIGNS["full"]` (claude, parallel): batch 1 = QUICK (delete-item, edit-item, status-filter, json-api, stats-page) + csv-export, item-notes, title-search, release-v0-2-0, release 9, added `item-rating`, 4 slots, budget 40; batch 2 = sort-list, duplicate-url, release-v0-3-0, release 3, 4 slots, budget 15. 13 CRs total.

delete-item spec: `POST /items/<id>/delete` -> 303 to `/`; unknown id 404; GET 405; item page has `<form method="post" action="/items/<id>/delete">` with a Delete button; ids never reused. Files: store.py, app.py, item.html, README.md, tests/test_items.py. Hidden `sandbox-judge/delete-item/test_judge_delete_item.py` (5 tests): redirect and removal; unknown 404; GET 405; id never reused (add two, delete id 2, new one gets id 3 and `/items/2` is 404); form is POST to `/items/1/delete`.

Reference patch `evals/kit/dry-run/delete-item.patch`: store `remove` plus a persisted next-id (store is a list-JSON file with ids `max+1`, so a sidecar or dict keeping backward compatibility), app route regex (`ITEM_DELETE`), the form in item.html (string.Template, `$id` already there), README Routes rows (lines 23-34), tests using the `client` fixture. title-search is not clearly smaller; keep delete-item.

Release CRs (release-v0-2-0, v0-3-0): files pyproject.toml, `src/shelf/__init__.py`, CHANGELOG.md, uv.lock (already named in their Files list, with "run `uv lock`"); done = tag on origin, GitHub release with the changelog section, versions in both files, `release_check` ends "release check passed". The dry run can set uv.lock by text-substituting the shelf package version (`name = "shelf"` / `version = ...` near line 67) or by `uv lock`.

## 7. Stale uv.lock: what the judge does

Probed: with a stale lock, `uv run --locked pytest -q` exits 1 ("The lockfile at `uv.lock` needs to be updated, but `--locked` was provided"). `pytest()` raises NotRun when there is no pytest summary line, so the judge reports "not run" rather than a failure. `uv lock --check` exits 1. `uv run python scripts/release_check.py` (no `--locked`) silently re-locks and its inner `--locked` pytest passes, so the release judge does not catch a stale lock at all.

Fix: run `uv lock --check` in the judge's clone right after checkout, before any `uv run`. In `feature()` return ok False with "FAIL: uv.lock is not up to date at <sha7>" (not NotRun); in `release()` add `item(False, "uv.lock is not up to date at <tag>")` before the release_check item, so the audit row shows it (the audit prints `bad[0][6:90]` of the first FAIL line). The stale-lock case in the dry run asserts this text.

## 8. Windows pitfalls

- Bare `gh` finds only `.exe`: use `shutil.which` (section 2).
- Read-only git objects block temp-dir removal: use `sandbox.remove` (chmod then retry).
- UTF-8 everywhere; `.cmd` launcher uses CRLF and quoted paths; `merge_command()` quotes the script path only if it has spaces.
- Local clone paths with `GIT_ALLOW_PROTOCOL=file`; avoid backslash/URL mixups when binding `sandbox.URL`.
- Locks with `os.O_EXCL`; no `fcntl`.
- Credential-helper check: set `GIT_CONFIG_COUNT/KEY_0/VALUE_0` in the process only.
- Workspace must be outside the repo (`inside(dest, ROOT)` refused): use a temp folder.
- POSIX launcher needs chmod 755; PowerShell stderr from native tools yields NativeCommandError noise (use exit codes).

## 9. Tests, justfile, CI

- test_structure.py `test_the_sandbox_campaigns_name_only_frozen_crs_with_hidden_tests` (line 444) loads setup.py via importlib: keep it importable. Add: each `evals/kit/sandbox-crs/release-*/03-change-spec.md` names `uv.lock` in "## Files".
- justfile: add recipe `eval-dry-run`; keep it out of `check` and `scenario`.
- Timing: warm cache `uv sync --locked` ~0.7 s and pytest ~0.9 s here; the whole run (setup, fake CI per SHA, judge clones, four cases) will exceed 10 s, so keep a separate recipe and its own CI job.
- ci.yml: new job "just eval-dry-run (ubuntu-latest)" copying `scenario`'s steps (checkout, setup-uv@v6, setup-just@v3, git identity, `just eval-dry-run`); add Windows if the run is portable, since the Windows pitfalls are the point.
- Docs: evals/README.md "The kit" and CONTRIBUTING.md "Daily work" (rules files) get the new recipe.
- Planted faults (cases): stray-merge (C12), reset-leftover (refs/pull plus a leftover branch/tag/PR -> setup refusal / reset verify), merge-refused (sandbox.py merge refusals), stale-lock (uv.lock).

## 10. Evidence plan (in order)

1. `just eval-dry-run` full output on Windows saved under `work/verifier/evidence/` (the green run plus each planted case's expected failure text).
2. `just check` on Linux, macOS and Windows (CI) plus the new structure assertion.
3. CI job `eval-dry-run` green on the PR.
4. Mutation proof: run the new dry run against d72df44's kit in a temp worktree; it must fail on C12 (stray merge), on the reset verify (refs/pull / leftovers) and on the missing `sandbox.py merge`.
5. Measured duration of the dry run, recorded.
6. No-network proof: `GIT_ALLOW_PROTOCOL=file`, the fake `gh` first on PATH (`which gh` output), and the fake refusing any `--repo` other than `sandbox.REPO`; the `.calls` log shows no real gh invocation.
