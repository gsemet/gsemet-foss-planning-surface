# CR-510: verification

Head: 4380df52776791c42253d49e971a6a38aaf9517e

**VERIFIED.** F1 to F4 of the judgment at `b85be4c` are fixed, the move broke nothing, and the
posted description matches the diff. One matrix cell of the specification is still not met (F5: the
generic-agent contract lines on Claude Code). It is not produced by the base either, the Driver
accepted it as a known gap, and the description discloses it. This verdict does not say that cell
is met. Not run on the owner's word: every quiz (evidence 6). Not captured: a `/compact` transcript
(evidence 11). Both are in Known gaps.

Conventions: `<wt>` the CR's worktree; `<CR>` the CR folder; `<v1>`, `<v2>` =
`<CR>/work/scratch/v1`, `v2` (raw logs and throwaway scripts of this pass and the last);
`BASE` = `ea11a9e05c3e682bf83ee2bb4e546de9b9db2dba`; `OLD` =
`b85be4cbeac5dac2208e26aeb440a9f6676e6ce3`; `HEAD` = `4380df52776791c42253d49e971a6a38aaf9517e`;
`REFS` = `skills/chantier/references`; `SRC` = `skills/chantier/scripts/cli/src/chantier`;
`TESTS` = `skills/chantier/scripts/cli/tests`. Commands run in `<wt>`. Outputs are excerpts. The
previous judgment is kept at `<CR>/work/verifier/verify-b85be4c.md`.

"Carried from b85be4c" always rests on M2 below: the one commit since `OLD` only appends a blank
line and a `[Trials]` link to 32 `REFS/topics/host-*.md` files.

## The move (judged at 4380df5)

| # | Claim | Command and output | Verdict |
| --- | --- | --- | --- |
| M1 | The head verified is the pushed head, clean; base unchanged (4380df5) | `git rev-parse HEAD` -> HEAD; `git status --porcelain` -> empty; `<v1>/pr_check.py` -> `head HEAD base BASE draft True OPEN`; `git rev-parse origin/main` and `git merge-base HEAD origin/main` -> BASE | VERIFIED |
| M2 | One commit since `OLD`, 32 host topics, only link lines (4380df5) | `git log --oneline BASE..HEAD` -> `4380df52 docs(cards): link the host topics to their trial history`, `b85be4cb feat(cards)!: ...`; `git diff --stat OLD HEAD` -> `32 files changed, 64 insertions(+)`; `<v2>/move.py` -> `changed files that are not exactly 'old text + blank line + one [Trials] link': []`; `git diff --stat OLD HEAD -- . ":(exclude)REFS/topics/host-*.md"` -> empty | VERIFIED |

## F1 to F5

| # | Claim | Command and output | Verdict |
| --- | --- | --- | --- |
| F1 | Hand-over row 4: the host topics link `docs/proofs/` (4380df5) | `<v2>/move.py` -> `host topics at head: 33`; `linked: 32; claude-code.md: 27; copilot.md: 5; unlinked: ['host-claude-only.md']`; every link prints an existing heading with a body (no `MISSING`, no `HOST MISMATCH`); `host-claude-only.md` printed whole: it only says the subject is a Claude Code feature with nothing recorded for Copilot. At BASE: `git grep -c "docs/proofs/" BASE -- REFS skills/chantier/cards-next` -> exit 1 | FIXED, VERIFIED |
| F2 | Known gaps holds the "do not merge" statement (4380df5) | `<v1>/pr_check.py` -> `"do not merge" in body: True`, `Known gaps lines on merge: ['- Do not merge alone: it merges in order with the changes st...']`; the wording drops "after child 28's campaign", as `02-answers.md` 5 says | FIXED, VERIFIED |
| F3 | The checklist is ticked with its commits (4380df5) | `<CR>/work/pr-body.md`, Internal references lead: "Rows marked done are in commit `b85be4c`; the links of row 4 are in commit `4380df5` (rows 11 to 14: not done ... D9 under order O-159)"; both commits are in `git log BASE..HEAD` (M2); row 2 reads "owner answered otherwise: no evaluation run in this batch, 2026-11-26" (`02-answers.md` 4); 25 rows | FIXED, VERIFIED |
| F4 | The deleted-tests table names real files (4380df5) | `git diff --name-status BASE HEAD -- TESTS` -> `D` `moved_rules.tsv`, `test_role_cards_split.py`, `test_session_start_split.py`, `test_stack_chain_cards.py`, `test_start_reading.py`, `test_startup_manifest.py`, `test_watcher_step.py`; `M` `test_release_template_card.py` and the other files the table names; `A` `test_brief_bytes.py`, `test_card_homes.py`, `test_card_names.py`; `<v1>/pr_check.py` -> `lines naming test_release_template.py: []`; the pin-list comment names `test_release_template_card.py` only | FIXED, VERIFIED |
| F5 | Matrix cell "Claude Code, configured generic agent: brief carries the contract lines" | carried from b85be4c: M2 touches no CLI source, test or configuration. `<v1>/probe.py` at `OLD`: `coder` with `agent: general-purpose` records `start: named`, brief 5055 bytes, one `=== floor`, 0 contract lines; BASE the same; no such case in `TESTS/test_brief.py` (`git grep -n -i -E 'generic\|contract'` -> exit 1). Accepted: `$CHANTIER log CR-510` 2026-11-26T08:02:09Z. Its Known gaps bullet and Autonomous decision are in the posted body | NOT MET, accepted, disclosed |

## Gates

| Claim (SHA) | Command and output | Verdict |
| --- | --- | --- |
| `just check` passes (4380df5) | run in `<wt>` -> exit 0; `<v2>/just-check.log`: `All checks passed!`, `Success: no issues found in 533 source files`, `2748 passed, 19 skipped in 218.68s`, release notes `ok` | VERIFIED |
| `just mod` passes (4380df5) | run in `<wt>` -> exit 0; `<v2>/mod.log`: `Validation passed with warnings`, `119 pass`, `0 fail`, `(pass) the reload message names the floor and no removed file` | VERIFIED |
| `just eval-dry-run`, 25 of 25 (4380df5 on CI; locally at `OLD`) | `gh run view --job 139828767099 --log` (`<v2>/ci-dry-run.log`): `HEAD is now at 229ed95 Merge 4380df5... into ea11a9e...`, `dry run: 25 of 25 cases as expected`. Local, carried from b85be4c (M2 touches no `SRC` or `evals/kit`): `<v1>/dry-run.log` the same line | VERIFIED |
| CI green, long gate `just scenario (ubuntu-latest)` included (4380df5) | `<v1>/pr_check.py` -> `just check` ubuntu, macos, windows, `just scenario (ubuntu-latest)`, `just eval-dry-run (ubuntu-latest)`: all `SUCCESS` | VERIFIED |

No local `gate` log exists and none is owed: this CR is not the top of its stack. `gate` was not
run. No quiz was run.

## Acceptance evidence

| # | Claim (SHA) | Command and output | Verdict |
| --- | --- | --- | --- |
| 1 | `cards-next/` empty and named nowhere (4380df5) | `git ls-tree -r --name-only HEAD skills/chantier/cards-next \| wc -l` -> 0; `git grep -n cards-next HEAD` -> exit 1 | VERIFIED |
| 1 | `REFS` equals BASE's `cards-next/` minus `skills/` (4380df5) | `<v2>/move.py` -> `330` and `330`, only in base `[]`, only in head `[]`; 36 files differ, of which beyond the link lines: `concepts.md`, `sync-checkout.md`, `topics.json`, `topics/foreman-start-p2.md`, `topics/host-allow-rules-copilot.md`, `topics/host-allow-rules.md`, all named in the body | VERIFIED |
| 1 | Every removed path listed with its completeness row (b85be4c) | carried from b85be4c: M2 removes no file. `<v1>/rows.py` -> `removed paths: 45`, `without a completeness row: []` | VERIFIED |
| 2 | Checklist ticked with commits; rows 2 and 11 to 14 truthful (4380df5) | F1, F3; rows 11 to 14: O-159 (D9) | VERIFIED |
| 3 | Driver table equals `roles.yaml`; `"Change Request"`; `host` rows (b85be4c) | carried from b85be4c: M2 touches neither `concepts.md`, `roles.yaml`, `SRC` nor `hosts/*.json`. `driver_table()` four rows equal; `concepts.md:20:## Change Request (CR)`; `<v1>/host_check.py` both hosts, 50 rows, none missing | VERIFIED |
| 3 | `floor.md` and the two JSON files unchanged (4380df5) | `<v2>/move.py` -> `floor.md` `61da01e8`, `claude-code.json` `3f2daf79`, `copilot.json` `b4dec473`, head equal to base | VERIFIED |
| 4 | `help` lists the topics; every printed name resolves; `help --for` 18 roles (4380df5) | `<v1>/help_only.py` on a scratch project (`<v2>/help.log`): `help: exit 0`, `topics in topics.json: 240 missing from the listing: []`, the 8 topic names printed by `SRC` exit 0, `every topic, exit non-zero: []`, 18 `help --for` exit 0; `help host-turn-end` exit 0, ends with its `[Trials]` line | VERIFIED |
| 5 | `just roles` (4380df5) | `roles: 18 roles, 15 wrappers on 2 hosts agree`, exit 0 | VERIFIED |
| 6 | Quiz against the baseline | not run: `02-answers.md` 4, O-168; both skipped sets in Known gaps with their commands | NOT RUN, disclosed; does not block |
| 7 | Brief bytes per role (4380df5) | `uv run --locked --group dev pytest -q -s -p no:cacheprovider TESTS/test_brief_bytes.py` -> `18 passed`: `cr-driver 9773`, `release-driver 9531`, `stack-driver 9179`, `qa-driver 6032`, `coder 3939`, `griller 6441`, `chief-of-staff 24351`, `foreman 22125` (`<v2>/bytes.log`) | VERIFIED |
| 7 | Over-target files listed with sizes (4380df5) | role cards, carried from b85be4c (M2 touches none): `git ls-tree -l` sizes equal Known gaps. Host topics: `<v2>/move.py` lists exactly nine over 1,500 (1578, 1571, 1561, 1558, 1540, 1524, 1522, 1520, 1509), each 1,500 or less before the link; names and sizes equal the new bullet | VERIFIED |
| 8 | `test_card_names.py` passes, prepared case, CLI lines (4380df5) | in `just check` above (2748 passed); failure line and CLI lines carried from b85be4c (`evidence/e8-card-names.md`; M2 touches no `SRC` or test) | VERIFIED |
| 9 | `just test` seconds, expected at most +3 s | carried from b85be4c: `evidence/e9-test-seconds.md`, same CLI and tests. This pass's run (218.68 s) and round 3's (153.74 s, `r3-check.log`) are inside the body's "139 to 265" | figures VERIFIED; bound NOT PROVED, marked `**UNVERIFIED:**` in Known gaps |
| 10 | No broken relative link, none into `cards-next/` (4380df5) | `<v1>/links.py . HEAD show-blob` -> `sources 617, relative links 343, broken 0, bad anchors 0`; the 2 `blob/v0.13.0` card links exist at the tag; equals `evidence/e10-links.md` (343, 0) | VERIFIED |
| 11 | `just mod` and the new hook case (4380df5) | `<v2>/mod.log` as above | VERIFIED |
| 11 | Transcript of a real session after `/compact` | not captured; in Known gaps | NOT CAPTURED, disclosed; no project rule requires it |
| 12 | Gates (4380df5) | "Gates" above | VERIFIED |

## Specification sections

All carried from b85be4c: M2 touches none of the files these commands read (`SRC`, `TESTS`,
`roles.yaml`, agent files, `SKILL.md`, `hooks/`, `evals/kit/`, `scenario/`, `CONTRIBUTING.md`,
`docs/incidents.md`, `review-step.md`).

| Claim (b85be4c) | Command and output | Verdict |
| --- | --- | --- |
| The review step's reply block is unchanged | `git grep -n -A2 -F '```json' BASE OLD -- REFS/review-step.md` -> the same JSON line at both | VERIFIED |
| `roles.yaml` cards and replies; wrappers | `git diff -U0 BASE OLD -- skills/chantier/roles.yaml`: 4 Driver cards, chief-of-staff and griller cards, 14 `reply:` lines; 30 agent files, `Read the brief your prompt` once in 14 + 14; no `startup core` | VERIFIED |
| CLI lines of section 3 | `git grep`: `commands/opening.py:269`, `commands/seat.py:58`, `stack_shape.py:58`, `commands/preflight.py:220`, `status/ready_line.py:135`; no `startup-core\|startup-manifest\|cards-next/` in `SRC` or the hook | VERIFIED |
| `take`, `take stack`, `order qa`, `round`, `handoff` print `brief` | `<CR>/work/verifier/evidence/before-after.md`, pairs 1 to 4 | VERIFIED |
| SKILL.md texts | `git diff --numstat BASE:cards-next/skills/<s>-SKILL.md OLD:skills/<s>/SKILL.md` -> only today's `$CHANTIER` paragraph kept | VERIFIED |
| Hook reload message | `git diff -U0 BASE OLD -- hooks/register.tsx`: only `reloadLine` | VERIFIED |
| Tests converted or deleted | `<v1>/removed_tests.py`; `<v1>/homes.py`: 271 pin lines, none missing from `test_card_homes`; no test reads the planning folder | VERIFIED |
| Eval kit, dry run, scenario, CONTRIBUTING | `evals/kit/audit.py:570,573`; `scenario/README.md:158`; `CONTRIBUTING.md:106`; gates above | VERIFIED |
| Incident stories in `docs/incidents.md` | 19 inventory rows of that home; 11 dated entries tell them or link them | VERIFIED |
| D9: launcher not switched | O-159; Known gaps "Launcher not switched" | VERIFIED |
| No version bump | `git diff --stat BASE OLD -- pyproject.toml plugin.json .claude-plugin .github/plugin` -> empty | VERIFIED |

## Host and default matrix

| Cell | Judged at | Proof | Verdict |
| --- | --- | --- | --- |
| 1 Claude Code, shipped | 4380df5 | `just check` (`test_brief.py`, `test_brief_bytes.py` among the 2748), the reload case in `mod.log`, CI scenario. Quiz and transcript: not run, not captured, disclosed | VERIFIED for what ran |
| 2 Claude Code, configured generic agent | carried from b85be4c: no CLI change | F5 | NOT MET, accepted, disclosed |
| 3 Copilot, shipped | carried from b85be4c (from 7d2c4dc, same tree): M2 adds link lines only; the 5 Copilot topic links resolve (F1) | `<CR>/work/verifier/matrix-r2.md` claim 3. Hook inertness is read from the manifests; unproved in a real Copilot session (Known gaps) | VERIFIED with that limit |
| 4 Copilot, configured | carried from b85be4c, same reason | `matrix-r2.md` claim 4 | VERIFIED with that limit |

## Pull request description

| Claim (SHA) | Command and output | Verdict |
| --- | --- | --- |
| The posted body is `<CR>/work/pr-body.md`; it renders (4380df5) | `<v1>/pr_check.py` -> `posted == pr-body.md: True 15876 15876`; rendered: the ten `h2` in order, 3 tables, 1 `details` opened and closed, one mermaid fence pair, 0 images | VERIFIED |
| No username or home folder published (4380df5) | same script -> `files read for private paths: 14 with a hit: []`, `body hit: False comment hit: [False]` | VERIFIED |
| What changed in the body since the last judgment (4380df5) | `git diff --no-index <v1>/posted-body.md <CR>/work/pr-body.md`: the merge bullet (F2), the host-topic size bullet (acceptance 7), the "32 of the 33" bullet (F1, M2), the table's file name (F4), the Test plan SHAs, the checklist lead and rows 2 and 4 (F3). Nothing else | VERIFIED |
| "32 of the 33 ... one added line each, `[Trials](...)`" | M2 and F1 (the added line is preceded by a blank separator line) | VERIFIED |
| Summary, Deliverables, Changes match the diff (4380df5) | acceptance 1 (the card text beyond the move is the 6 files plus the link lines, all named); `git diff --shortstat BASE HEAD` -> 515 files; rest carried from b85be4c (M2 changes nothing else) | VERIFIED |
| Brief sizes in "Deliverables" (4380df5) | acceptance 7; old figures from the base tree (`evidence/e7-bytes.md`) | VERIFIED |
| Autonomous decisions (b85be4c) | carried from b85be4c: text unchanged, M2 touches none of their subjects. `<v1>/claims-run.log`, `<v1>/brief_env.py`, `02-answers.md` 2 and 3 | VERIFIED |
| Known gaps facts that did not change (b85be4c) | carried from b85be4c: text unchanged, M2 touches none of the files they describe (`<v1>/claims-run.log`) | VERIFIED |
| Each unrun, unproved or accepted-failed item has its bullet (4380df5) | merge, both quizzes, transcript, Copilot, F5, real run, launcher, over-target cards and topics, `**UNVERIFIED:**` seconds; no `STALE` mark (one `UNVERIFIED`, the seconds bullet) | VERIFIED |
| Human decisions (b85be4c) | carried from b85be4c: text unchanged; `02-answers.md` 4 and 5 | VERIFIED |
| Test plan: local gates and CI at the named SHAs (4380df5) | "Gates" above: 2748 passed, 19 skipped; 119 pass; 25 of 25; five checks green | VERIFIED |
| Test plan: Review box `approved at 4380df5` | `$CHANTIER log CR-510`: 09:55:59Z "r3 inspector approved at b85be4c (round 3 diff, 32 host topics, and pr-body.md)", 09:56:13Z "r3 approved at b85be4c..., committed as 4380df52776791c42253d49e971a6a38aaf9517e" | VERIFIED |
| "its branch started on CR-507's (PR 487, merged)" (b85be4c) | carried from b85be4c: `gh pr view 487` -> `MERGED`, head `88d9ab40...` | VERIFIED |

The unticked boxes "Evidence: before at `ea11a9e`, after at `4380df5`" and "Verified" are now
backed by `<CR>/work/verifier/evidence/before-after.md` and this file.

## Before and after

`<CR>/work/verifier/evidence/before-after.md`: nine pairs, before at BASE. Pairs 1 to 7 carried
from b85be4c (M2 reaches none of their outputs), pair 8 printed again at HEAD, pair 9 (the topic
link) new at HEAD. Not captured: a `/compact` transcript, a real batch run, a Copilot session, the
quizzes; each is in Known gaps.

## Observations (no effect on the verdict)

- `REFS/topics/wakes-p1.md:5` still names the `prompt` blocks `take` and `order qa` no longer
  print; the Known gaps list of such files says "Some" and does not name it.
- Known gaps names two sentences of `AGENTS.md` that are now stale, while checklist row 5 reads
  "done" (the specification asks no `AGENTS.md` edit).
- `docs/proofs/claude-code.md:885` holds a local home path, as at BASE; this change does not touch
  `docs/proofs/` but 27 topics now link that file: a follow-up.
- The `just test` time is far above the `AGENTS.md` budget already at the base.
