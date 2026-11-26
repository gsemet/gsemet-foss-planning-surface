# CR-510: verification

Head: 133640bc6b56f2c2d2c67b96054b08bcb6825b2f

**VERIFIED.** The one commit since the judgment at `4380df5` does what order O-175 asks: the
refusal paragraph of every agent file that asks for a path now accepts the `Read` line of the short
prompt `brief` prints, on both hosts. It broke nothing, and `work/pr-body.md` is true for this
head. One matrix cell of the specification is still not met (F5: the generic-agent contract lines
on Claude Code), accepted by the Driver and disclosed; this verdict does not say it is met. Not
run: every quiz. Not captured: a `/compact` transcript. Not tried: a real agent on the new
paragraph. Not seen: the new test failing.

**Not covered: the description posted on the forge.** It is still the one of `4380df5` (it holds
the Known gap this head fixes). This verdict judged the local file only; the repost needs its own
description pass. Edits owed before it are under "Pull request description".

**Slip of this pass:** two of my shell calls changed directory into the CR folder, against the
brief (one `cat`/`ls` under `work/`, one no-op `cd` into `work/scratch/v4`). Neither wrote
anything.

Conventions: `<wt>` the CR's worktree; `<CR>` the CR folder; `<v1>`, `<v2>`, `<v4>` =
`<CR>/work/scratch/v1`, `v2`, `v4` (raw logs and throwaway scripts); `BASE` =
`ea11a9e05c3e682bf83ee2bb4e546de9b9db2dba`; `OLD` = `4380df52776791c42253d49e971a6a38aaf9517e`;
`HEAD` = `133640bc6b56f2c2d2c67b96054b08bcb6825b2f`; `REFS` = `skills/chantier/references`; `SRC` =
`skills/chantier/scripts/cli/src/chantier`; `TESTS` = `skills/chantier/scripts/cli/tests`. Commands
run in `<wt>`. Outputs are excerpts. The previous judgment, with the full commands of every carried
row, is `<CR>/work/verifier/verify-4380df5.md`.

"Carried: M2" means: carried from the SHA named, because the move changed only the refusal paragraph
of 14 agent files and two test files (M2), which that proof does not exercise.

## The move (judged at 133640b)

| # | Claim | Command and output | Verdict |
| --- | --- | --- | --- |
| M1 | The head verified is the pushed head, clean; base unchanged | `git rev-parse HEAD` -> HEAD; `git status --porcelain` -> empty (before and after the runs); `gh pr view 488 --json headRefOid,baseRefOid,state,isDraft` -> HEAD, BASE, `OPEN`, draft; `git merge-base HEAD origin/main`, `git rev-parse origin/main` -> BASE | VERIFIED |
| M2 | One new commit, 16 files, all modified | `git log -1` -> `fix(agents): accept the brief's Read line in the worker agent files`; `git diff --name-status OLD HEAD` -> `M` x 16: 7 `agents/*.md`, 7 `com.github.copilot/agents/*.agent.md`, `TESTS/test_brief.py`, `TESTS/test_plugin_files.py`. `git diff --stat OLD HEAD -- hooks types SRC evals REFS skills/chantier/roles.yaml scripts docs scenario ...` and the two board-griller files -> empty. No added or removed line holds a markdown link | VERIFIED |

## O-175

| # | Claim | Command and output | Verdict |
| --- | --- | --- | --- |
| O1 | The old paragraph refused `brief`'s short prompt; the new one accepts it, both hosts | `<v4>/probe.py` (`<v4>/probe.log`): scratch project per host, `take CR-101`, `brief <role> CR-101`. Coder, both hosts: first line `chantier coder for CR-101 "One" of batch batch-01, in the project <project>.`, last `Read <project>/.git/chantier/briefs/proj/batch-01/CR-101-coder.md whole, first.`; against `git show OLD:` paragraph `asks ['coder.md']; prompt names one=False`; against HEAD `asks ['<unit>-coder.md', 'coder.md']; prompt names one=True`. The same for conflict-resolver, debugger, inspector, investigator, verifier and demo-explorer (`none-demo-explorer.md`). A reading of the words, not an agent's answer | VERIFIED |
| O2 | All 15 agent files checked: 7 asked for a path and are fixed; the others ask for none | `<v4>/probe.log`: `asks_a_path_at_head=True`, `changed claude=True copilot=True` for the 7; `False`, `False False`, `asked_before=False` for cr-, release-, stack-, qa-driver, spec-writer, spec-critic, retro-critic, board-griller. Their paragraph (`Grep`) reads `A prompt that does not start with ...` and names no file; `brief` first lines start with each one's `chantier <role>` on both hosts | VERIFIED |
| O3 | Both hosts' bodies identical for all 15 | `<v4>/probe.log`: `bodies identical=True` x 15 at HEAD (and at OLD) | VERIFIED |
| O4 | board-griller's unchanged; frontmatter and every other line unchanged | M2 stat of its two files empty; `front_changed=False` x 15; `git diff -U0 OLD HEAD -- agents com.github.copilot` -> 14 hunks, each `-N,3 +N,3` at the paragraph | VERIFIED |
| O5 | `just roles` | `just roles` -> `roles: 18 roles, 15 wrappers on 2 hosts agree`, exit 0 | VERIFIED |
| O6 | One test pins the paragraph against what `_short_prompt` prints, and passes | `uv run --locked --group dev pytest -v -p no:cacheprovider --basetemp <v4>/pt TESTS/test_brief.py -k refusal_paragraph` -> `14 passed, 27 deselected` (`<v4>/refusal-test.log`). Read: it runs `brief` on both hosts, checks the printed first line against the paragraph's `chantier <role>`, the count of `<unit>-<role>.md` and `<role>.md` (2 for the seven, 0 for the others) and the `Read` file's name against that suffix | VERIFIED as passing. Its failing on drift was NOT SEEN: not attempted by this pass; the host refused the Coder's edit (`$CHANTIER log CR-510` 10:53:42Z); in Known gaps |
| O7 | The removed pins of the old sentences are replaced | `git diff OLD HEAD -- TESTS/test_plugin_files.py`: the two literal asserts go, the test keeps its card checks under a new name; `git grep "names no path to my card"` over the agent files -> none | VERIFIED |

## Gates

| Claim (SHA) | Command and output | Verdict |
| --- | --- | --- |
| `just check` passes (133640b) | run in `<wt>` -> exit 0; `<v4>/just-check.log`: `All checks passed!`, `Success: no issues found in 533 source files`, `2762 passed, 19 skipped in 182.31s`, release notes `ok`. The Driver's `work/gates/r4-just-check.log` (first line HEAD): same counts, 141.24 s | VERIFIED |
| `just mod` passes (133640b) | run in `<wt>` -> exit 0; `<v4>/just-mod.log`: `Validation passed with warnings`, the 15 `chantier:` agents listed, `119 pass`, `0 fail`. The Driver's `r4-just-mod.log` (first line HEAD): same | VERIFIED |
| CI green, long gate `just scenario (ubuntu-latest)` included (133640b) | `gh pr view 488 --json statusCheckRollup`: `just check` ubuntu, macos, windows, `just scenario (ubuntu-latest)`, `just eval-dry-run (ubuntu-latest)`: all `SUCCESS`; job logs: `Merge 133640b... into ea11a9e...`, windows `2762 passed, 19 skipped` | VERIFIED |
| `just eval-dry-run`, 25 of 25 (133640b on CI; locally carried from b85be4c: no `SRC` or `evals/kit` change since) | `<v4>/ci-dry.log`: `dry run: 25 of 25 cases as expected`; `<v1>/dry-run.log` the same line | VERIFIED |

No local `gate` log exists and none is owed: this CR is not the top of its stack. `gate` was not
run. No quiz was run.

## Findings of the earlier judgments

| # | Claim | Proof | Verdict |
| --- | --- | --- | --- |
| F1 | Host topics link `docs/proofs/` | carried from 4380df5 (M2): 32 of 33 linked, each to an existing heading; the 33rd is for one host | VERIFIED |
| F2 | Known gaps holds the "do not merge" statement | judged at 133640b: first bullet of the local body | VERIFIED |
| F3 | Checklist ticked with its commits | judged at 133640b: lead names `b85be4c`, `4380df5`, `133640b`, all in `git log BASE..HEAD`; the table's rows are unchanged (`<v4>/body.log` diff) | VERIFIED |
| F4 | Deleted-tests table names real files | carried from 4380df5 (M2 deletes and adds no test file) | VERIFIED |
| F5 | Matrix cell "Claude Code, configured generic agent: brief carries the contract lines" | carried from b85be4c: no `SRC` change since. Accepted: log 2026-11-26T08:02:09Z; Known gaps bullet and Autonomous decision in the body | NOT MET, accepted, disclosed |

## Acceptance evidence

| # | Claim (SHA) | Command and output | Verdict |
| --- | --- | --- | --- |
| 1 | `cards-next/` named nowhere (133640b) | `git grep -n cards-next HEAD` -> exit 1 | VERIFIED |
| 1 | `cards-next/` empty; `REFS` equals BASE's staged set but for the named edits (4380df5, carried: M2 touches no `REFS`) | `<v2>/move.py`: 330 and 330 files; 36 files differ, and those beyond the link lines are named in the body | VERIFIED |
| 1 | Every removed path listed with its completeness row (b85be4c, carried: M2 removes no file) | `<v1>/rows.py` -> 45 paths, none without a row | VERIFIED |
| 2 | Checklist truthful (133640b) | F3; rows 11 to 14 not done, order O-159 | VERIFIED |
| 3 | Driver table, `"Change Request"`, `host` rows; `floor.md` and the two JSON files unchanged (b85be4c, 4380df5; carried: M2 touches none) | `verify-4380df5.md`, acceptance 3 | VERIFIED |
| 4 | `help` lists and prints every topic; `help --for` 18 roles (4380df5, carried: `help` reads `REFS`, `roles.yaml` and `SRC`, none touched) | `<v1>/help_only.py`: 240 topics, none missing, no non-zero exit | VERIFIED |
| 5 | `just roles` (133640b) | O5 | VERIFIED |
| 6 | Quiz against the baseline | not run: `02-answers.md` 4, O-168; in Known gaps with the commands | NOT RUN, disclosed; does not block |
| 7 | Brief bytes per role (133640b) | `pytest -q -s ... TESTS/test_brief_bytes.py` -> `18 passed`: cr-driver 9773, release-driver 9531, stack-driver 9179, qa-driver 6032, coder 3939, griller 6441, chief-of-staff 24351, foreman 22125 (`<v4>/bytes.log`): equal to the body | VERIFIED |
| 7 | Over-target files listed with sizes (4380df5, carried: M2 touches no `REFS`) | `verify-4380df5.md`, acceptance 7 | VERIFIED |
| 8 | `test_card_names.py` passes (133640b); its prepared case and CLI lines (b85be4c, carried: no `SRC` change) | in `just check`; `evidence/e8-card-names.md` | VERIFIED |
| 9 | Added test time at most +3 s | figures carried from b85be4c (`evidence/e9-test-seconds.md`); the two runs at this head (141.24, 182.31 s) are inside the body's "139 to 265" | bound NOT PROVED, marked `**UNVERIFIED:**` in Known gaps |
| 10 | No broken relative link (4380df5, carried: M2 changes no link) | `<v1>/links.py` -> 343 links, 0 broken, 0 bad anchors | VERIFIED |
| 11 | `just mod` and the hook case (133640b) | Gates | VERIFIED |
| 11 | Transcript of a real session after `/compact` | not captured; in Known gaps | NOT CAPTURED, disclosed; no project rule requires it |
| 12 | Gates (133640b) | "Gates" | VERIFIED |

## Specification sections

| Claim (SHA) | Command and output | Verdict |
| --- | --- | --- |
| Section 2, wrappers (133640b) | "Kept: the refusal paragraph" (spec lines 237 to 238) is overridden by order O-175 as a specification defect (log 10:44:22Z): O1 to O4. The rest: `git grep -c "Read the brief your prompt" HEAD` over both agent folders -> 28 files; `git grep -i "startup core"` there -> exit 1; `just roles` | VERIFIED |
| Review step's reply block; `roles.yaml` cards and replies; CLI lines of section 3; `take`, `take stack`, `order qa`, `round`, `handoff` print `brief`; SKILL.md texts; hook reload message; eval kit, scenario, CONTRIBUTING; incident stories; D9 launcher not switched; no version bump (b85be4c, carried: M2 touches none of these files) | `verify-4380df5.md`, "Specification sections" | VERIFIED |
| Tests converted or deleted (b85be4c); the two tests changed since (133640b) | carried rows as `verify-4380df5.md`; O6, O7; `just check` runs `test_card_homes.py` green; the new test works on the `repo` fixture, no planning folder | VERIFIED |

## Host and default matrix

| Cell | Judged at | Proof | Verdict |
| --- | --- | --- | --- |
| 1 Claude Code, shipped | 133640b | `just check` (`test_brief.py`, `test_brief_bytes.py`), reload case in `just mod`, CI scenario, `<v4>/probe.log` claude. Quiz and transcript: not run, not captured, disclosed | VERIFIED for what ran |
| 2 Claude Code, configured generic agent | carried from b85be4c: no CLI change | F5 | NOT MET, accepted, disclosed |
| 3 Copilot, shipped | 133640b | `<v4>/probe.log` copilot: 14 roles with an agent file brief, record host `copilot`; `just check` copilot cases. Rows untested and hook inert: carried from 7d2c4dc (`verifier/matrix-r2.md` claim 3: no row or hook manifest change) | VERIFIED with that limit, unproved in a real Copilot session |
| 4 Copilot, configured | 133640b (re-judged: the contract lines are the agent file's body, which moved) | `<v4>/probe_generic.py` (`<v4>/generic.log`), `roles.coder.model: gpt-6.1-terra`: the short prompt names `CR-101-coder.md`; the brief holds `coder contract (a generic agent: ...` with the new paragraph accepting `<unit>-coder.md` | VERIFIED with the same limit |

## Pull request description (`work/pr-body.md`, local, not reposted)

| Claim (133640b) | Command and output | Verdict |
| --- | --- | --- |
| Posted body | `<v4>/body_check.py` (`<v4>/body.log`) -> `posted == local: False 17215 18234`; posted holds the removed gap: `True` | NOT JUDGED for this head: repost and description pass owed |
| Structure | same script: ten `h2` in the template's order, 3 even tables, 1 `details` opened and closed, 6 fence lines none open, 0 images, `STALE` 0, `UNVERIFIED` 1. Read, not rendered by the forge | VERIFIED |
| No username or home folder | same script -> local `False`, posted `False` | VERIFIED |
| What changed since the posted body | its diff: one Autonomous decision, one Known gap replaced by three, one Changes bullet added and one extended, the Test plan, the checklist lead. Nothing else | VERIFIED |
| Autonomous decision on the refusal paragraph | spec lines 237 to 238 say keep; O1 (the old one asked for a file the short prompt does not name); O-175 says "to confirm by the owner" | VERIFIED |
| Changes: "seven agent files ... on both hosts with identical bodies ... The other agent files check the first line only, and the board Griller's is unchanged" | O2, O3, O4 | VERIFIED |
| Changes: the `test_brief.py` case; "the pins of the old refusal sentences are removed" | O6, O7 | VERIFIED |
| Known gaps: not tried with a real agent | no record of such a start in `work/coder/r4.md` or the log; the agent files this pass was started from hold the old paragraph | VERIFIED |
| Known gaps: a card-only prompt is accepted, two sentences do not read true | HEAD paragraph accepts `<role>.md`; `agents/coder.md` line 11 "Read the brief your prompt's last line names" and line 13 "it opens that brief", both outside the move's hunk | VERIFIED |
| Known gaps: the test was only seen passing; new tests not run on the previous code | O6; log 10:53:42Z; no run on BASE or OLD is recorded or was made | VERIFIED |
| The old gap "A worker's agent file refuses ..." is gone, rightly | O1; `<v4>/body.log` -> local holds it: `False` | VERIFIED |
| Each unrun, unproved or accepted-failed item has its bullet | merge, both quizzes, transcript, Copilot, F5, real run, launcher, over-target cards and topics, the new paragraph, the test, `**UNVERIFIED:**` seconds | VERIFIED |
| Test plan: local gates | "Gates": 2762 passed, 19 skipped; 119 pass; dry run at `b85be4c`, two commits back | VERIFIED |
| Test plan: new tests pass at `133640b` | O6; `just check` | VERIFIED |
| Test plan: Review box `approved at 133640b` | log 10:56:00Z "r4 inspector approved at 4380df5 (round 4 diff and pr-body.md)", 10:56:20Z "r4 approved at 4380df5..., committed as 133640bc6b56f2c2d2c67b96054b08bcb6825b2f" | VERIFIED |
| Internal references: the paragraph is in commit `133640b` | M2 | VERIFIED |
| Deliverables excerpts and brief sizes | excerpts carried from b85be4c (before-after pairs 1 and 4; M2 changes no `SRC`); sizes: acceptance 7 | VERIFIED |
| Summary, Blast radius, the other Autonomous decisions, Human decisions, Impacts, the other Changes and Known gaps | text unchanged (the diff above); carried from 4380df5 and b85be4c: M2 touches none of their subjects | VERIFIED |

### What carries to 133640b, and the edits owed before the repost

- Carries: the "Before, at `ea11a9e`" excerpt; the "After" excerpt (from `b85be4c`); the brief
  sizes (measured again here); the local dry run at `b85be4c`; the unproved seconds figures; every
  pair of `before-after.md` 1 to 7 (from `b85be4c`) and 9 (from `4380df5`); pair 8 printed again;
  pair 10 new at `133640b`.
- Deliverables caption "After, at `4380df5` (carried from `b85be4c`)": name `133640b`.
- Test plan "Evidence": after at `133640b`, command captures carried from `b85be4c`; it can be
  ticked (`verifier/evidence/before-after.md`).
- Test plan "Verified: pending": verified at `133640b`; the added-test-time bound is not proved.
- Test plan "CI: pending": all five checks green at `133640b`.

## Before and after

`<CR>/work/verifier/evidence/before-after.md`: ten pairs. Pair 10: the paragraph at `4380df5` and
at `133640b` against what `brief` prints. Not captured: a `/compact` transcript, a real agent on
the new paragraph, the new test failing, a real batch run, a Copilot session, the quizzes; each is
in Known gaps.

## Observations (no effect on the verdict)

- The body's "runs of the new head span 139 to 265 seconds" does not count the Coder's 136.00 s run
  on the uncommitted round 4 tree (`work/coder/r4.md`); the bullet is marked unverified either way.
- For a role with no unit the brief file is `none-<role>.md`: the demo explorer's, which the new
  paragraph accepts.
- `just check` and `just mod` ran as the project defines them, so their tests used the default
  system temporary folder, and `uv` and `gh` their own caches; my own targeted test runs used a
  base folder under `<v4>`.
- Carried from before: `AGENTS.md`'s two stale sentences (disclosed); `docs/proofs/claude-code.md`
  holds a local home path, as at BASE; the `just test` time is far above the `AGENTS.md` budget
  already at the base.

## Description pass on the posted body (133640b)

**NOT VERIFIED.** The posted description of PR 488 holds two sentences that are false against the
PR's diff at this head. Everything else judged here holds. The sections above are unchanged and
keep their `VERIFIED` on the code. All rows judged at 133640b. `BASE`, `HEAD`, `OLD`, `<wt>`,
`<CR>` as above; `<v5>` = `<CR>/work/scratch/v5` (throwaway scripts, removed at the end of the
pass). Nothing was edited in the PR or the code; no gate, test, quiz or eval was run.

### Failed

| # | Sentence (posted body) | Command and output | Verdict |
| --- | --- | --- | --- |
| P1 | Known gaps: "A worker started with a prompt that names its card and no brief is accepted, but two sentences of its agent file, about the brief that the prompt names, do not read true for it; **they are unchanged.**" | `git grep -c -e "Read the brief your prompt" -e "it opens that brief" BASE -- agents com.github.copilot/agents` -> exit 1, no hit; the same on HEAD -> 2 in each of the 14 worker agent files. `git diff BASE HEAD -- agents/coder.md com.github.copilot/agents/chantier-coder.agent.md`: both sentences are `+` lines (they replace "Read the startup core first..." and "read it first, before any other step, at the path your prompt's `Read` line gives"). This PR wrote them. Only the last commit left them as they were (`git diff OLD HEAD`). The rest of the sentence is true | FALSE |
| P2 | Changes: "The other agent files check the first line only, and **the board Griller's is unchanged.**" | `git diff BASE HEAD -- agents/board-griller.md com.github.copilot/agents/chantier-board-griller.agent.md` -> one line changed on each host: "Read the startup core first, then your card's ..." becomes "Read your card's ...". The sentence's subject is agent files, so it says the file is unchanged. Only its refusal paragraph is (same diff: both paragraph lines are context). The first half is true (`<v5>/agents_check.py`) | FALSE as written |

Wording that would be true: P1 drop "they are unchanged" (or say the refusal fix did not reword
them); P2 "and the board Griller's refusal paragraph is unchanged".

### Holds

| # | Claim | Command and output | Verdict |
| --- | --- | --- | --- |
| D1 | Head, base, posted body | `gh pr view 488 --json headRefOid,baseRefOid,isDraft,state,body` -> HEAD, BASE, draft, `OPEN`; `<v5>/body_check.py`: posted == `work/pr-body.md`, 19226 characters; unchanged at the end of the pass | VERIFIED |
| D2 | Changed places since the body judged at 4380df5 | `<v5>/body_check.py`, diff of surface commit `7fa81e5a` against posted: Deliverables caption and refusal excerpt, one Autonomous decision, one Known gap replaced by three, one Changes bullet added and one extended, six Test plan lines, the checklist lead. Nothing else | VERIFIED |
| D3 | Refusal excerpt: prompt's last line, "Before, at `4380df5`", "After, at `133640b`" | `git diff OLD HEAD -- agents/coder.md`: both quoted pairs of lines match; `commands/brief.py` `_short_prompt` appends `Read <path> whole, first.` last; `<CR>/work/scratch/v4/probe.log` and pair 10: `.../CR-101-coder.md` | VERIFIED |
| D4 | "After, at `133640b` (carried from `b85be4c`)" | `git diff --stat b85be4c HEAD -- <SRC> evals hooks types scenario` -> empty | VERIFIED |
| D5 | Autonomous decision on the refusal paragraph | spec section 2 "Kept: ... the refusal paragraph"; log 10:44:22Z (O-175, to confirm by the owner); the old paragraph asks for `<role>.md`, the short prompt names `<unit>-<role>.md` (D3) | VERIFIED |
| D6 | Changes: seven worker agent files on both hosts, identical bodies; the others check the first line only | `<v5>/agents_check.py`: 15 and 15 files, `identical=True` x 15; the 14 changed files are the seven named; the other eight conditions are the first line only | VERIFIED |
| D7 | Changes: the `test_brief.py` case; old pins removed | `git diff OLD HEAD -- <TESTS>`: 14 roles, both hosts, board-griller excluded; `git grep -e "names no path to my card" -e "must name my card" HEAD -- skills/chantier/scripts scripts hooks evals scenario` -> exit 1 | VERIFIED |
| D8 | Three new Known gaps otherwise: not tried with a real agent; two sentences do not read true for a card-only prompt; test only seen passing | `work/coder/r4.md` ("no real agent was started here", "seen passing only"); log 10:53:42Z; `agents/coder.md` lines 11 and 13 | VERIFIED but for P1 |
| D9 | Each unrun, uncaptured or accepted item has its bullet | `before-after.md` "Not captured" and F5, acceptance 9 above against Known gaps: all present | VERIFIED |
| D10 | Test plan: local gates | `work/gates/r4-just-check.log` (line 1 HEAD): `2762 passed, 19 skipped`; `just mod` `119 pass`, `0 fail` (`r4-just-mod.log`, and "Gates" above); `work/scratch/pre-push-eval-dry-run.log` and log 08:12:07Z: 25 of 25 at `b85be4c`, two commits back (`git log BASE..HEAD`); CI job 139862625478 on `Merge 133640b... into ea11a9e...`: `dry run: 25 of 25 cases as expected` | VERIFIED |
| D11 | Test plan: new tests, evidence, Verified, CI | "Gates" and O6 above; `before-after.md` head (base BASE, pair 10 `4380df5` -> HEAD); log 11:22:35Z verdict at HEAD; `statusCheckRollup`: five checks `SUCCESS` | VERIFIED |
| D12 | Review box `approved at 133640b` | log 10:56:00Z, 10:56:20Z "r4 approved at 4380df5..., committed as 133640bc..." | VERIFIED |
| D13 | Checklist lead: paragraph in commit `133640b` | `git log BASE..HEAD`, `git diff --stat OLD HEAD` | VERIFIED |
| D14 | Rendering, fold, marks, images, private paths, internal references | `gh api .../pulls/488` full media type: 10 `h2`, 3 tables, 5 `pre`, 1 `details`; `<v5>/body_check.py`: 0 images, 0 `STALE`, 1 `UNVERIFIED` (its bullet in Known gaps), no username or home folder, no internal reference outside Internal references | VERIFIED |
| D15 | The rest of the body | unchanged text (D2); the last commit touches only 14 agent files and 2 test files; carried from 4380df5 and b85be4c, save P1 and P2 | VERIFIED |

### Observations (no effect on the verdict)

- The Test plan "Evidence" line does not say that pair 9 is carried from `4380df5`.
- "runs of the new head span 139 to 265 seconds" leaves out two runs on uncommitted trees, 132.95 s
  (`r2-check.log`) and 136.00 s (`r4-check.log`); the bullet is marked unverified.
- The "Gates" section above says `r4-just-mod.log` starts with HEAD; its first line is the command.
- One shell call of this pass changed directory into the CR folder and back, against the brief
  (nothing was read or written by that change).
