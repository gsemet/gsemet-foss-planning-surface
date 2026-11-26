# Verify CR-492

Head: 0a293d2037379db99ea10c4aed0ee8ef787819aa

All claims judged at 0a293d2037379db99ea10c4aed0ee8ef787819aa (worktree clean, `git status --short` empty after the runs).

1. `just eval-dry-run` green, five quiz cases ok. Command: `just eval-dry-run`. Output: `ok quiz-cases: the 50 shipped cases load ...`, `ok quiz-staged ...`, `ok quiz-cap ...`, `ok quiz-ref ... SHA 0a293d20`, `ok quiz-folder ...`, `dry run: 25 of 25 cases as expected` (took 244 s whole). Per case, `dry_run.py --case quiz-*`: took 0 s, 1 s, 0 s, 2 s, 0 s, each `1 of 1 cases as expected`. The "about 3 s" in the PR holds; the before figure was not re-measured by me (see Not proved).
2. 50 seed cases, 29 floor pairs. Command: a Python check over `evals/quiz/*/*.json` (id equals stem, role equals folder, exact five keys, `rules` non-empty, floor pairs against the spec's table). Output: `50 29 set() set()` (50 files, 29 required floor pairs, none missing, none extra); the rails used: J3, J4, J6 to J12, J15, J16, J18 to J29.
3. `quiz --plan` and refusals (run as `uv run --locked python evals/kit/quiz.py ...`, the recipe's body):
   - `cr-driver --max-usd 0.01 --plan` prints `plan: cr-driver 18 cases x 3 runs on claude-sonnet-5-5 + 54 judge calls on claude-fable-5-2: ~$20.25` and `plan total: 54 runs, ~$20.25 (cap $0.01)`, no model call.
   - `foreman --plan`: exit 2, `foreman has no shipped model: pass --model <id>`.
   - `cr-driver --model x --plan`: exit 2, `--model is refused for cr-driver: it has a shipped model, claude-sonnet-5-5`.
   - `nope --plan`: exit 2, lists the 18 roles. `cr-driver --case zzz --plan`: exit 2, `no case zzz among the roles named (cr-driver)`.
   - `CHANTIER_HOST=copilot ... cr-driver --plan`: exit 2, `the quiz runs on Claude Code only`.
   - `cr-driver --cards evals --plan`: the CLI's own usage error (`invalid choice: 'brief'`), then `quiz.py: --cards <folder> needs chantier brief, which this head does not have`. (Exit code of the pipeline was masked by `tail`; the dry run's `quiz-folder` case asserts exit 2.)
4. Cap, price, judge-model, ref, staged runs, F4, save: proved by the dry-run cases of claim 1 (they read the shipped files at this head), not by a model run.
5. Scope: `git diff --name-only HEAD~1 HEAD` lists only `evals/README.md`, `evals/kit/dry_run.py`, `evals/kit/quiz.py`, `evals/kit/quiz_judge.py`, `evals/quiz/**` and `justfile`: no `src/`, card, hook or test change. `quiz` is not in `check`.
6. PR description (`gh pr view 476`): renders, sections and the mermaid block are well formed, Summary, Deliverables and Changes match the diff, no image. Known gaps names the baseline not run, each unproved host-flag point and `HOST_PROMPT_TOKENS`. The Test plan's `<sha7>` placeholders are still unfilled (the Driver fills them at closing); the posted Known gaps is a little shorter than `work/pr-body.md` (it lacks the UNVERIFIED mark on the cost estimates and the run defaults): the Driver should post the pr-body.md text.
7. Review box: `$CHANTIER log CR-492` holds `inspector approved at 5374657... (rounds 1+2 uncommitted)` and `approved at 537465754469... committed as 0a293d20`, so the box `approved at 0a293d2` is backed.

## Not proved (all marked UNVERIFIED in Known gaps)

`claude` is not on PATH, so no model run: the host flags, `total_cost_usd`/`num_turns` in the JSON, `HOST_PROMPT_TOKENS`, the baseline results files (spec Evidence asks for them; the PR names them as a Known gap and the Risk section allows that hand-back), and case command spellings. The `just test` delta of 0 s (no pytest file touched) is proved by claim 5; the dry-run's pre-change duration was not measured by me.

CI: macOS failure on `tests/test_serve_webui.py` is outside this CR's files (claim 5), per the Driver.

VERIFIED
