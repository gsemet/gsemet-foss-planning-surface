# CR-510: verification

Head: b85be4cbeac5dac2208e26aeb440a9f6676e6ce3

**NOT VERIFIED.** The code at this head does what the specification says in every point checked but
two (F1: the host topics link nothing in `docs/proofs/`; F5: one matrix cell, accepted and
disclosed). The pull request misses two things the specification requires of it (F2, F3) and names
one test file that does not exist (F4). F2, F3 and F4 are fixes of the description alone; F1 needs a
Known gaps bullet or the links.

Conventions: `<wt>` the CR's worktree; `<CR>` the CR folder; `<v1>` = `<CR>/work/scratch/v1` (raw
logs and the throwaway scripts); `BASE` = `ea11a9e05c3e682bf83ee2bb4e546de9b9db2dba`; `HEAD` =
`b85be4cbeac5dac2208e26aeb440a9f6676e6ce3`; `REFS` = `skills/chantier/references`; `SRC` =
`skills/chantier/scripts/cli/src/chantier`; `TESTS` = `skills/chantier/scripts/cli/tests`. Commands
run in `<wt>` at HEAD unless said otherwise. Every claim is judged at HEAD (`b85be4c`) unless a
"carried from" line says otherwise. Outputs are excerpts.

## Failed claims

### F1. The host topics do not link `docs/proofs/` (hand-over row 4): NOT VERIFIED (b85be4c)

Specification, row 4: "The host cards' history leaves the cards: what child 23 did not carry goes to
`docs/proofs/` (already) or `docs/incidents.md`; the host topics link `docs/proofs/`".

- `git grep -n proofs/ HEAD -- skills/chantier/references` -> no output, exit 1.
- Same at BASE: `git grep -n -i docs/proofs BASE -- skills/chantier/cards-next REFS` -> exit 1.
- The rest of the row holds: `git ls-tree --name-only HEAD docs/proofs/` -> `docs/proofs/claude-code.md`,
  `docs/proofs/copilot.md`; `git grep -n proofs/ HEAD -- docs/incidents.md` -> 11 lines linking
  `proofs/claude-code.md`.
- The pull request marks row 4 "done" with the clause dropped from its text, and no Known gaps bullet
  names it (`<v1>/pr_check.py`: `Known gaps lines naming proofs: []`).

Fix: a Known gaps bullet and row 4 corrected, or the links.

### F2. Known gaps holds no "do not merge" statement (specification, Handback): NOT VERIFIED (b85be4c)

Specification: "The typed merge wait ... is recorded once child 28's PR exists. Until then the PR's
Known gaps say "do not merge: merges with children 19 to 28 as one unit, after child 28's
campaign"". `02-answers.md` 5 drops only "after child 28's campaign" ("the CRs still merge in order,
in one sitting, by the owner").

- `<v1>/pr_check.py` -> `"do not merge" in body: False`, `Known gaps lines on merge: []` (24
  bullets).
- `$CHANTIER log CR-510` -> no wait recorded; order O-174: "one merge ask once CR-510..513 are all
  handed back, never CR-510 without CR-511's verdict".
- The merge order is told only in "Blast radius" and "Human decisions".

Fix: a Known gaps bullet, in the description's own words (no internal reference there), for example
"Do not merge alone: it merges in order with the changes stacked with it, in one sitting, by the
owner."

### F3. The hand-over checklist is not ticked with its commit (acceptance evidence 2): NOT VERIFIED (b85be4c)

Specification: "The PR's Internal references hold the hand-over checklist, every row ticked with its
commit, or marked "owner answered otherwise: <answer>"".

- `<CR>/work/pr-body.md` lines 137 to 163: columns `# | What | State`, 25 rows, states "done" or
  "not done: ...", no commit column and no SHA in the table or its lead line.
- `git log --oneline BASE..HEAD` -> one commit, `b85be4cb feat(cards)!: swap in the new role cards
  and remove the old set`.

Fix: name `b85be4c` on the done rows (or in the table's lead line, for all of them).

### F4. The deleted-tests table names a file that does not exist: NOT VERIFIED (b85be4c)

The body, "Changes": "the manifest test and "Visible evidence" check of `test_release_template.py`".

- `git ls-tree -r --name-only BASE -- TESTS/test_release_template.py TESTS/test_release_template_card.py`
  -> `TESTS/test_release_template_card.py` only; the same command at HEAD -> the same one line.
- `git diff --name-status BASE HEAD -- "TESTS/test_release_template*"` ->
  `M TESTS/test_release_template_card.py`.
- `git diff BASE HEAD -- TESTS/test_release_template_card.py` removes
  `test_release_template_is_an_action_reading_only` (the manifest test) and the
  `## Visible evidence` heading check, and reads `topics/release-evidence.md`: the row means this file.

Fix: write `test_release_template_card.py`.

### F5. Matrix cell 2, a configured generic agent on Claude Code gets the contract lines: NOT VERIFIED (b85be4c); accepted and disclosed

Specification matrix: "Claude Code | a configured generic agent for a worker | Its brief carries the
contract lines (child 10's case in `test_brief.py`)".

- `<v1>/probe.py` (scratch `git init` project, `hosts.claude.roles.coder.agent: general-purpose`,
  `take`, then `chantier brief coder CR-101`) -> exit 0, the record holds
  `"coder": {"agent": "general-purpose", "start": "named"}`, brief 5055 bytes, starts `# Coder`,
  one `=== floor`, `lines holding 'contract (a generic agent': 0` (`<v1>/probe-head3.log`). A take
  at BASE with the same configuration gives no contract lines either (`<v1>/probe-base.log`).
- `git grep -n -i -E 'generic|contract' HEAD -- TESTS/test_brief.py` -> exit 1: no such case.
- `git grep -n NAMED_AGENT_MODEL_AT_START HEAD -- SRC` -> `playbook/models.py:57:
  NAMED_AGENT_MODEL_AT_START = {"claude": True, "copilot": False}`; `git diff --stat BASE HEAD --
  SRC/playbook/layers.py SRC/playbook/escalation.py` -> empty. The branch did not introduce this.

State: the Driver accepted it (log 2026-11-26T08:02:09Z, not blocking under O-166); its Known gaps
bullet and Autonomous decision are in the body and are true. On its own this does not keep the
description NOT VERIFIED.

## Head, move and gates

| Claim (SHA) | Command and output | Verdict |
| --- | --- | --- |
| The head verified is the pushed head, clean (b85be4c) | `git rev-parse HEAD` -> HEAD; `git status --porcelain` -> empty; `<v1>/pr_check.py` -> `head HEAD base BASE draft True OPEN` | VERIFIED |
| One commit on BASE, which is origin/main (b85be4c) | `git log --oneline BASE..HEAD` -> one line; `git rev-parse origin/main` -> BASE; `git diff --shortstat BASE HEAD` -> `515 files changed, 4550 insertions(+), 16579 deletions(-)` | VERIFIED |
| The move 7d2c4dc on 88d9ab40 -> b85be4c on ea11a9e is a clean rebase (b85be4c) | `git rev-parse 88d9ab40^{tree} BASE^{tree} 7d2c4dc^{tree} HEAD^{tree}` -> `b6c77cd5...` twice, `f48002c3...` twice; `git show <c> \| git patch-id --stable` -> `38539a12654f92c6b714fa9c37d9d066770101c8` for both; `git diff --stat 7d2c4dc HEAD` -> empty | VERIFIED |
| `just check` passes (b85be4c) | the pre-push log `<CR>/work/scratch/pre-push-*.log`, copied reading `<v1>/just-check.log`: `All checks passed!`, `2748 passed, 19 skipped in 183.78s`; log note 08:10:26Z "just check: pass" | VERIFIED |
| `just eval-dry-run` passes (b85be4c) | `<v1>/dry-run.log` line 28: `dry run: 25 of 25 cases as expected` | VERIFIED |
| `just mod` passes (b85be4c) | `<v1>/mod.log`: `Validation passed with warnings`, `119 pass`, `0 fail`, `(pass) the reload message names the floor and no removed file`; base `<v1>/mod-base.log`: 118 pass, the same 14 TypeScript warnings | VERIFIED |
| Long gate: CI `just scenario (ubuntu-latest)` green at the head (b85be4c) | `gh pr view 488 --json statusCheckRollup` (`<v1>/pr-check.log`): `just check` ubuntu, macos, windows, `just scenario (ubuntu-latest)`, `just eval-dry-run (ubuntu-latest)`: all `SUCCESS` | VERIFIED |

No local `gate` log exists and none is owed: this CR is not the top of its stack. `gate` was not run.
No quiz was run but the free `--plan` form.

## Acceptance evidence

| # | Claim (SHA b85be4c) | Command and output | Verdict |
| --- | --- | --- | --- |
| 1 | `cards-next/` is empty; `REFS` equals its list minus `skills/` | `<v1>/verify-run.log` "e1 lists": `cards-next: 0 files`; `HEAD references: 330; base cards-next: 334; minus skills/: 330`; only-in lists `[]` both ways; contents differ for 6 files, all named in the body | VERIFIED |
| 1 | `cards-next` named nowhere | `git grep -n cards-next HEAD` -> exit 1 | VERIFIED |
| 1 | Every removed path listed with its completeness row | 45 removed paths, none missing from `evidence/removed-files.md`; `<wt>/.venv/Scripts/python.exe -I <v1>/rows.py` -> `removed paths: 45`, `without a completeness row: []`, no row fate outside "not carried" / "folded" | VERIFIED |
| 2 | Checklist ticked with its commits | see F3; row 4 see F1 | NOT VERIFIED |
| 2 | Rows 2 and 11 to 14 not done, truthfully | row 2: `02-answers.md` 4; rows 11 to 14: order O-159 (D9) and CR-502's pull request body line 47 (the launcher leaves the CLI running after its stop on Windows) | VERIFIED |
| 3 | Driver table: four rows, cards equal `roles.yaml` | `driver_prompt.driver_table()` -> `cr-driver.md`, `release-driver.md`, `stack-driver.md`, `qa-driver.md`; `load_roles()` the same four | VERIFIED |
| 3 | `"Change Request"` found | `git grep -n "Change Request" HEAD -- REFS/concepts.md` -> `concepts.md:20:## Change Request (CR)` | VERIFIED |
| 3 | `host` prints the JSON rows on both hosts | `<v1>/host_check.py`: claude and copilot exit 0, `json rows 50; printed ids in order equal True`, `row texts not found in the output: 0` | VERIFIED |
| 3 | `floor.md` and the two JSON files unchanged | `git ls-tree -r BASE` (staged paths) and `HEAD` (`REFS`): blobs `61da01e8` floor, `3f2daf79` claude-code.json, `b4dec473` copilot.json on both sides | VERIFIED |
| 4 | `help` lists the topics; each name the CLI prints resolves; `help --for` for 18 roles | `<v1>/help_only.py`: `help: exit 0`, `topics in topics.json: 240 missing from the listing: []`, `board`, `host-allow-not-add`, `lease`, `merge`, `refused-push`, `stack`, `stack-merge`, `watcher` exit 0 (the other grep words are not topic names), `every topic, exit non-zero: []`, 18 `help --for` exit 0 | VERIFIED |
| 5 | `just roles` | `roles: 18 roles, 15 wrappers on 2 hosts agree`, exit 0 | VERIFIED |
| 6 | Quiz against the baseline | not run, owner's word (`02-answers.md` 4, O-168). `just quiz ... --plan` (the four commands, new and `--cards ea11a9e0`) exit 0: 90 runs ~$32.19, 87 ~$32.29, ~$33.52, ~$41.80. Known gaps name both skipped sets with their commands | NOT RUN, disclosed; does not block |
| 7 | Bytes per role; over-target cards listed | `uv run --locked --group dev pytest -q -s -p no:cacheprovider TESTS/test_brief_bytes.py` -> `18 passed`, `cr-driver 9773`, `coder 3939`, `chief-of-staff 24351`, `foreman 22125` and 14 more, equal to `evidence/e7-bytes.md` (`<v1>/bytes.log`); `git ls-tree -l HEAD REFS/`: release-driver 3809, spec-writer 1667, coder 1603, verifier 3112, demo-explorer 1612, spec-critic 1572, retro-critic 1565, as in Known gaps | VERIFIED |
| 8 | `test_card_names.py` passes; its prepared case; CLI lines before and after | `pytest TESTS/test_brief.py test_brief_bytes.py test_card_names.py test_card_homes.py` -> `66 passed in 26.93s`; failure line and CLI lines in `evidence/e8-card-names.md` (carried from the committed tree: e8 was made on the tree committed as 7d2c4dc, same tree as HEAD) | VERIFIED |
| 9 | Test seconds at base and head, expected at most +3 s | `evidence/e9-test-seconds.md` (carried from 7d2c4dc: same tree): base 157.82 s / 165.0 wall; head 265.01 / 267.6, then 162.47 / 167.2, 138.63 inside `just check`. Figures quoted; the bound is neither proved nor disproved | figures VERIFIED; bound NOT PROVED, marked `**UNVERIFIED:**` in Known gaps |
| 10 | No broken relative link, none into `cards-next/` | `<v1>/links.py <wt> HEAD blob` -> `sources 617, relative links 311, broken 0, bad anchors 0`; at BASE 12 broken; the 2 `blob/v0.13.0` card links exist at that tag; `evidence/e10-links.md`: no D5 rewrite | VERIFIED |
| 11 | `just mod` and the new hook case | `<v1>/mod.log` as above; `hooks/register.test.tsx:1103` | VERIFIED |
| 11 | Transcript of a real session after `/compact` | not captured; disclosed in Known gaps | NOT CAPTURED, disclosed; no project rule requires it |
| 12 | Gates | "Head, move and gates" above | VERIFIED |

## Specification sections (b85be4c)

| Claim | Command and output | Verdict |
| --- | --- | --- |
| The review step's reply block is unchanged | `git grep -n -A2 -F '```json' BASE HEAD -- REFS/review-step.md` -> the same JSON line at BASE:40 and HEAD:12 | VERIFIED |
| `roles.yaml` cards and replies | `git diff -U0 BASE HEAD -- skills/chantier/roles.yaml`: 4 Driver cards, chief-of-staff and griller cards, 14 `reply:` lines; `git diff --stat BASE HEAD -- agents com.github.copilot/agents` -> 30 files, 44+, 58-; `Read the brief your prompt` once in 14 + 14 wrappers; `git grep -i 'startup core'` in them exit 1; board Griller wrappers keep `## Started from the board` | VERIFIED |
| CLI lines of section 3 | `git grep` at HEAD: `commands/opening.py:269` "its first step is `brief foreman ...`"; `commands/seat.py:58` `next: $CHANTIER brief foreman`; `stack_shape.py:58` "shape: stack: read `$CHANTIER help stack`"; `commands/preflight.py:220` names `hosts/claude-code.md`; `status/ready_line.py:135` "run your brief again"; `topics.json:136` `refused-push`; `foreman-refused` exit 1; `startup-core\|startup-manifest\|cards-next/` in `SRC` and `hooks/register.tsx` exit 1 | VERIFIED |
| `take`, `take stack`, `order qa`, `round`, `handoff` print `brief` | before and after captures, `<CR>/work/verifier/evidence/before-after.md` | VERIFIED |
| SKILL.md texts | `git diff --numstat BASE:cards-next/skills/<s>-SKILL.md HEAD:skills/<s>/SKILL.md` -> 2/12 (three), 1/11 (status): today's `$CHANTIER` paragraph kept | VERIFIED |
| Hook reload message | `git diff -U0 BASE HEAD -- hooks/register.tsx`: only `reloadLine`; the new text names `brief`, `--epoch <n>` and "the floor, in that brief, holds" | VERIFIED |
| Tests converted or deleted | `<v1>/removed_tests.py` (each removed test and its file); `<v1>/homes.py`: 271 pin lines, `comment homes missing from test_card_homes: 0`; `test_driver_prompt.py:24,36` checks the card cells; no test reads the planning folder: `git grep -n -E "planning-surface\|4-batch\|cards-inventory\|gsemet-foss" HEAD -- TESTS/test_card_homes.py TESTS/test_card_names.py TESTS/test_brief_bytes.py` -> exit 1 | VERIFIED |
| Eval kit, dry run, scenario, CONTRIBUTING | `evals/kit/audit.py:570,573`; dry run 25 of 25; `scenario/README.md:158`; CI scenario green; `CONTRIBUTING.md:106` | VERIFIED |
| Incident stories of home `incidents file` in `docs/incidents.md` | 11 dated entries cover the 19 rows of that home; the phrase `incidents file` is in only one card inventory (host and shared), no other | VERIFIED |
| D9: launcher not switched | O-159; Known gaps line "Launcher not switched" | VERIFIED |
| No version bump | `git diff --stat BASE HEAD -- pyproject.toml plugin.json .claude-plugin .github/plugin` -> empty | VERIFIED |

## Host and default matrix

| Cell | Judged at | Proof | Verdict |
| --- | --- | --- | --- |
| 1 Claude Code, shipped: briefs for 18 roles; reload message | b85be4c | 66 tests pass (`test_brief.py`, `test_brief_bytes.py` among them); `mod.log` 119 pass with the reload case. The quiz and the `/compact` transcript of this column: not run, not captured, disclosed | VERIFIED for what ran |
| 2 Claude Code, configured generic agent | b85be4c | F5 | NOT VERIFIED |
| 3 Copilot, shipped: briefs for 18 roles, rows untested, no hook | carried from 7d2c4dc: clean rebase, same tree and patch-id, empty diff | `<CR>/work/verifier/matrix-r2.md` claim 3. Inertness is inferred from `.github/plugin/plugin.json` (no `hooks`) and `hooks/hooks.json` (a Claude mod); unproved in a real Copilot session | VERIFIED with that limit |
| 4 Copilot, configured | carried from 7d2c4dc: same reason | `matrix-r2.md` claim 4 (`gpt-6.1-terra`) | VERIFIED with that limit |

## Pull request description (b85be4c)

| Claim | Command and output | Verdict |
| --- | --- | --- |
| The posted body is `<CR>/work/pr-body.md`; it renders | `<v1>/pr_check.py` -> `posted == pr-body.md: True`; rendered HTML: the ten `h2` in order, 3 tables, 1 `details` opened and closed, 1 mermaid fence, 0 images | VERIFIED |
| No username or home folder published | same script: 13 files read (body, `evidence/`, `work/verifier/`) `with a hit: []`; body and the pin-list comment: no hit | VERIFIED |
| No internal reference outside "Internal references" | search of `CR-n`, `O-n`, `Dn`, `batch-n`, `child n`, `scNN` in the body: only lines 134 to 161 | VERIFIED |
| Summary, Deliverables, Changes match the diff | the rows of the sections above; card text beyond the move: `git diff --numstat BASE:cards-next/<f> HEAD:REFS/<f>` gives exactly the 6 files named, and `git diff -U0` of `sync-checkout.md`, `foreman-start-p2.md` and the two allow-rule topics says what the body says (the two sync steps that left are in `topics/sync-offer-p1.md`, `-p2.md`) | VERIFIED but F4 |
| Brief sizes in "Deliverables" | `<v1>/bytes.log` at HEAD for the new figures; old figures `evidence/e7-bytes.md` (base tree) | VERIFIED |
| Autonomous decisions | `<v1>/claims-run.log`: `facts split`, `griller board`, `griller brief`, `refusals`, `roles reply`, `runbooks`, `read key test`, `generic *`; `02-answers.md` 2 and 3 for the two defaults; `before-after.md` for `take`'s lines and `Team:` / `Note:` | VERIFIED |
| "The quiz builds a new-card boot with the batch variable removed ... because an inherited batch variable made the boot fail" | `git grep -n CHANTIER_BATCH HEAD -- evals/kit/quiz.py` -> line 394 drops it and sets the host to claude. `<v1>/brief_env.py` on a scratch project: `brief coder` without the variable exit 0; with `CHANTIER_BATCH=batch-99` exit 2, `error: unknown batch batch-99` (`<v1>/env-run.log`). Shows the cause for a batch the project does not hold | VERIFIED |
| Known gaps facts | `<v1>/claims-run.log`: `copilot marks` (50 untested), `copilot plugin`, `worker refusal` (`agents/coder.md:18`), `agents md reads` (`AGENTS.md:262-263`), `docs team` (two pages), `contract heading` (`plugin_files.py:263`), `generic test` (exit 1), `hosts json names`, `old wording base/head`, `stale names`, `team entries` (exit 1: no filter of these names), `budget` (`9_900`), `hook test`; `mod-base.log` for the old warnings; `e7` for sizes | VERIFIED |
| Each unrun or unproved item has its bullet | quiz, baseline, transcript, Copilot, generic case, real run, launcher, over-target cards, `**UNVERIFIED:**` seconds: present. Missing: F1 and F2 | NOT VERIFIED (F1, F2) |
| Human decisions | `02-answers.md` 4 and 5, orders O-168, O-171, O-174 | VERIFIED |
| Test plan: local gates and CI boxes | "Head, move and gates" | VERIFIED |
| Test plan: Review box | `$CHANTIER log CR-510`: 07:51:19Z "r2 inspector approved at 88d9ab40...", 07:51:31Z "committed as 7d2c4dc..."; carried to b85be4c by the clean rebase above | VERIFIED |
| "its branch started on CR-507's (PR 487, merged)" | `gh pr view 487` -> `MERGED`, head `88d9ab40...`, the base of 7d2c4dc | VERIFIED |

## Before and after

`<CR>/work/verifier/evidence/before-after.md`: eight pairs, BASE against HEAD. Not captured: a
`/compact` transcript, a real batch run, a Copilot session, the quizzes.

## Observations (no effect on the verdict)

- `REFS/topics/wakes-p1.md:5` still names the `prompt` blocks `take` and `order qa` no longer print;
  it is not in the Known gaps list of such files.
- Checklist row 5 reads "done" for `AGENTS.md`'s role sentences (the specification asks no
  `AGENTS.md` edit); Known gaps names two sentences of `AGENTS.md` that are now stale.
- "Changes" says links and sentences naming removed files are fixed; Known gaps names those left.
- `evidence/e3` to `e10` were made on the uncommitted tree (base 88d9ab40), the content later
  committed; the facts above were judged again at HEAD where a row says so.
- The brief-sizes sentence of "Deliverables" names no SHA.
- The `just test` time is far above the `AGENTS.md` budget already at the base (157.8 s).
