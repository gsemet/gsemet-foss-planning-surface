# CR-507 verification

Head: 03f973e4f0d0756c9b5fa77ed0f888f941745dbe

Base: `24111e6d9920a7ff3e8f210613186dd65d802ec8` (origin/main). Every claim below is judged at head `03f973e` (written "head") unless it says otherwise.

Result: **NOT VERIFIED**. The card, size, index, link, parser, brief, test and CI claims hold. Six claims fail: the PR Summary (F1), the split of "The user's boundaries" (F2), protecting rows' homes (F3), one Known gap statement (F4), the child-24 hand-over in the PR (F5) and acceptance records that are recorded nowhere (F6).

Paths: `<worktree>` the CR's worktree, `<planning>` the project's planning folder, `<CR folder>` this CR's folder, `<next>` = `skills/chantier/cards-next`. Scripts: `work/verifier/scripts/` (local paths replaced by placeholders); raw logs: `work/verifier/*.log`; before and after: `work/verifier/evidence/before-after.md`.

## Failed claims

### F1. The PR Summary matches the diff: NOT VERIFIED

PR body, lines 5-6: "Everything is under `skills/chantier/cards-next/`, which nothing loads until the later swap."

`git diff --name-status 24111e6d..HEAD -- . ':(exclude)skills/chantier/cards-next'`

```text
A  evals/quiz/chief-of-staff/a8-ask-delete.json
A  evals/quiz/chief-of-staff/a8-ask-release.json
A  evals/quiz/chief-of-staff/a8-ask-stop-process.json
A  evals/quiz/chief-of-staff/a8-chained-subcommand-refused.json
A  evals/quiz/chief-of-staff/a8-gh-pr-edit-base-refused.json
A  evals/quiz/chief-of-staff/a8-gh-pr-ready-refused.json
A  evals/quiz/chief-of-staff/a8-push-refused-cr-branch.json
A  evals/quiz/chief-of-staff/a8-push-refused-default-branch.json
A  evals/quiz/chief-of-staff/a8-rebase-refused-cr-branch.json
```

Nine added files are outside that folder. Deliverables (line 13) and Changes (line 172) name them, so the Summary contradicts both and the diff. Fix: narrow the sentence.

### F2. Part 1 acceptance 8, the split of "The user's boundaries", in the PR and the inventory: NOT VERIFIED

`grep -n -i -E 'boundar|B1a|B7f' <CR folder>/pr-body.md` prints nothing (0 matches). The posted body equals that file (C28), so the PR holds no split table.

Labels of the specification's section 4 table (`03-change-spec.md` lines 262-304) against the trigger column of the `FM-B` rows of `evidence/cards-inventory-foreman.md`, whose line 9 says "their `trigger` starts with the specification's label (B1a to B7f)":

```text
spec:      B1a B1b B1c B1d B1e B1f B1g B1h B1i B1j B1k B1l B1m B1n B1o B1p B2 B2b B3 B4 B5a B5b B5c B5d B6 B7a B7b B7c B7d B7e B7f
inventory: B1a B1d B1e B1f B1h B1i B1j B1k B1l B1m B1n B1o B2 B3 B4 B5a B5b B5c B5d B6 B7b B7c B7d B7e
missing:   B1b B1c B1g B1p B2b B7a B7f
```

Several present labels are shifted: `FM-B008` is labelled B1f but holds the evidence note, which is B1g in the specification (line 276); `FM-B025` is labelled B1m but holds the waiver sentence (spec B1n, line 283). The sentences have rows; the table "with the final homes" by label does not exist. No Known gap says it.

### F3. Every protecting row's home is the floor, the card or a refusal (Part 1 acceptance 8, Part 3 acceptance 10; PR line 21): NOT VERIFIED

Inventory claim (`cards-inventory-foreman.md` line 737): "None sits in a topic alone and none is inferable."

- `FM-071`, kind a, "Never for another reason, nor at a Driver's request alone." (`gate --first`), home "card foreman.md:13 (use every free slot); `gate --first` stays the CLI's".
  `sed -n 13p <next>/foreman.md`: "- Starting Drivers: copy whole the prompt `take`, `take stack` or `order qa` prints, with the agent and model `playbook --batch` names, then `agents set`. Use every free slot."
  `git grep -n -e '--first' HEAD -- <next>` finds the rule only in `topics/long-gate.md:7` ("... Never for another reason, nor at a Driver's request alone."), plus the command in `topics/direct-mode-epoch-p1.md:3`. `floor.md` (10 rules) does not hold it. The rule is in a topic alone.
- `FM-B008`, home "card foreman.md:9 ... worded in the card". Line 9 is "- Read the rules and `status`, then send `[foreman→chief-of-staff] ready <batch>`." `git grep -n -i evidence HEAD -- <next>/foreman.md` prints nothing (exit 1). The card does not word it.
- `FM-B055`, kind a, "Never code, review, commit, ...", home and quote "card foreman.md:24". Line 24 is the chat rule ("5. Obey your chat but for \"stop\" and \"hold\" ..."). The rule is in the card, at line 22: the cited home is wrong.
- `FM-054` (kind e), home "card foreman.md:13": line 13 does not carry the `lease not confirmed` rule.
- `H-1057` (`cards-inventory-host-and-shared.md`), kind a, "A second Driver for a unit ... is started only by the restart path ... never on silence alone", home "card foreman.md:25". Line 25 is "6. `take --reclaim` a live lease without the user's word; remove the worktree of a trashed CR ..."; `git grep -n -i 'second Driver' HEAD -- <next>` finds only `topics/host-driver-silence.md:16`. The card does not state the restart-path-only rule.

These are the rows found by reading a sample; the PR says the homes were matched by script, not read row by row.

### F4. Known gap "rows with protecting wording that a topic carries are listed for the later review": NOT VERIFIED

`grep -n -i -E 'protecting-looking|protecting.*topic' evidence/cards-inventory-*.md` and `grep -n '^## ' evidence/cards-inventory-foreman.md`:

```text
cards-inventory-chief-of-staff.md:1746:## Protecting-looking rows a topic carries
cards-inventory-griller.md:96:## Protecting-looking rows a topic carries
cards-inventory-host-and-shared.md:2261:## Protecting-looking rows not classified a
foreman headings: How the sources were walked; foreman.md ...; "The user's boundaries"; foreman-stack/merge/hold/lost-driver/conflict/release/refused/pause.md; Protecting rows and their homes; Inferable rows; Counts; Check candidates for child 25; For child 24
```

The Foreman inventory (670 rows, 473 with a topic home) has no such list.

### F5. Part 1 handback: "The PR's Internal references name the hand-over items for child 24 (section 7)": NOT VERIFIED

`grep -n -i -E 'test_came_back|test_stack_shape|moved_rules|shape_line|help stack' <CR folder>/pr-body.md` prints nothing (0 matches). Internal references (lines 252-256) name the CR and `evidence/` only, and the "For the swap (child 24)" Known gap (lines 161-165) names none of the stack line, `shape_line()`, the eight tests or `moved_rules.tsv`. They are only in `cards-inventory-foreman.md` ("For child 24: the stack line", line 896 on).

### F6. Acceptance items recorded in the PR or under `<CR folder>/evidence/`: NOT VERIFIED

Missing from both, with no Known gap:

| Item | Search | Result |
| --- | --- | --- |
| `just test` seconds at base and head (P1.7, P2.8, P3.9) | `grep -rn -i 'just test' evidence/`; PR body for seconds | `part3-proofs.md` section 9: "Base and head times were not measured separately."; PR: none |
| `git diff --stat` quote (P1.1, P2.1) | `grep -rn -i 'diff --stat'` in PR body and `evidence/` | no match |
| `griller.md` diff quoted (P2.1) | `grep -rn -E 'git diff|^@@' evidence/`; PR body | no diff output quoted (`cards-inventory-griller.md:113` quotes the added sentence, the sibling table names line 7) |
| `just quiz ... --plan` output, "Before any spend" (P2.4) | `grep -rn -i -E 'quiz.*--plan|--plan'` | no match |
| old start readings beside the brief table: 144 KB measured (P1.3), 218 KB and 36 KB and the direct-mode total (P2.3) | `grep -rn -E '218 KB|144 KB|36 KB|direct.mode total'` | no match (only study-fable-v2 columns in `part3-proofs.md` section 4) |

This verification measured the times (C25), the diff and `griller.md` diff (`before-after.md`) and the plan (C18); they can be cited from there.

## Verified claims

### C1. State of the PR: VERIFIED

`gh pr view 487 --repo gsemet/chantier --json headRefOid,baseRefName,isDraft,state` and `git rev-parse HEAD`; `git status --porcelain` prints nothing.

```text
headRefOid 03f973e4f0d0756c9b5fa77ed0f888f941745dbe, base main, draft true, OPEN
```

### C2. Diff size and place: VERIFIED

`git diff --stat 24111e6d..HEAD` ends `263 files changed, 6080 insertions(+), 27 deletions(-)`; 244 added, 19 modified; everything is under `<next>/` but the nine files of F1 (Part 2 acceptance 1: "cards-next/ and evals/quiz/ only"). A word diff of the 19 modified files finds each change covered by the PR's sibling-edit table.

### C3. No test added or changed: VERIFIED

`git diff --name-only 24111e6d..HEAD | grep -E '(^|/)tests/'` prints nothing (exit 1).

### C4. Unloaded: VERIFIED

`git grep -n cards-next HEAD -- . ':(exclude)skills/chantier/cards-next'` prints nothing (exit 1).
`git grep -n "Read this short role contract at boot\|# chantier-agent:\|chantier board" HEAD -- <next>` prints nothing (exit 1).

### C5. Encoding: VERIFIED

`scripts/proofs.py`: `files: 263 BOM or CRLF: []`.

### C6. Card sizes against budgets, PR bytes tables: VERIFIED

`scripts/proofs.py` (`git show <rev>:<path>`, LF bytes):

```text
foreman 3998/4000 within; chief-of-staff 5994/6000 within; griller-skill 3497/4000 within; griller.md 1925/2000 (base 1758; section 1914)
cr-driver 3749/4096; stack-driver 3783/4096; qa-driver 1567/2048; floor 554/1200; review-step 1385/1500; inspector 2000/2000; conflict-resolver 1494, debugger 1281, investigator 1486 /1500
OVER: coder +33, demo-explorer +112, retro-critic +65, spec-critic +72, spec-writer +167, verifier +112, release-driver +739
shared: concepts 73286->18565; pr-template 16801->11849; release-template 12155->6758; status-layout 17475->10992; titles 2684->1428; ticket-summary-example 1422->1308; routing 5016->4790; init 10041->6171; review-step 3950->1385; sync-checkout 4801->1115; forges 739->587, 744->590; hosts md claude 109857->23319; skills 3537->2650, 3664->2730, 3223->2292, 3644->2729
```

Every number equals the PR's, and the over-budget list equals the Known gaps'.

### C7. Topic sizes: VERIFIED as stated with its gap

`topic files: 268 over 1500: 24` (each present at the base head of the round; names and sizes equal the PR's Known gaps); `host topics: 33 total 36066 largest 1490`; `topic files new in this diff: 214 largest 1500`.

### C8. Byte-identical copies: VERIFIED

`git rev-parse HEAD:<next>/<p> HEAD:skills/chantier/references/<p>`:

```text
floor.md                61da01e8b67f8b8eec1845172a29d2466d1cc380 (both)
hosts/claude-code.json  3f2daf7915192a790e2dc17b36d74d3cfd9a1fd0 (both)
hosts/copilot.json      b4dec473e0dab53cbacd334fa29286ce3ccc2ff9 (both)
```

### C9. Topic index: VERIFIED

`load_topics(<next>/topics.json)` from the worktree's `commands/help.py` (`scripts/proofs.py`):

```text
topics: 234 readings entries: 388 forms: 415; missing references names: []; missing cards-next base names: []
roles.yaml roles: 18 unknown topic roles: []; review_by topics: 37 ['0.16.0']; references foreman rows: none lost the foreman role
topic files no topic reads: []; PR list: 234 missing: [] extra: []; PR review_by 37 named 37 missing [] extra []
```

### C10. `help` readings of the new set: VERIFIED

`scripts/helpread.py` (`help._print_topic` on every topic with base `<next>`; the `help` command itself reads `references/` and has no `--cards`):

```text
host claude: printed 234, errors [], empty [], total bytes 482363, largest steering 21783
host copilot: printed 234, errors [], empty [], total bytes 457919, largest steering 21783
```

### C11. `help <name>` names: VERIFIED

`cited names: 175 not in topics.json: {}`; names the CLI source prints: none missing.

### C12. Links: VERIFIED

`links: 22 broken: [] into references: []`; outside `<next>`: `forges/github.md` and `gitlab.md` to `docs/forge-connectors.md`, `init.md:17` to `../assets/tour.html` (named in Known gaps).

### C13. Driver table: VERIFIED

`driver_prompt.driver_table()` on `references/concepts.md` and `<next>/concepts.md`: `rows old: 4 new: 4 equal: True`. `git grep -c "Change Request" HEAD -- <next>/concepts.md`: 1.

### C14. Review step's reply block: VERIFIED

`fenced blocks old: 1 new: 1 equal: True`.

### C15. Foreman reply lines unchanged: VERIFIED

`scripts/replies.py`: `base reply spans: 16 | missing byte for byte at head: []`; `pong <first line of status>` is in `foreman.md:36`, the form the specification gives (line 195; the base card wrote "the first line").

### C16. `griller.md`: VERIFIED

`git diff 24111e6d..HEAD -- <next>/griller.md` changes two lines: line 7 gains "never a secret or personal data" (Part 3 sibling edit, in the PR's table) and the one "How you grill..." sentence is added to line 11.

### C17. `brief` with `--cards`: VERIFIED as stated with its gap (11 of 18)

`scripts/briefs.py`, batch-31, host claude from the record; byte table in `before-after.md`, pair 2. 11 roles exit 0 with the specified units (spec roles on an inbox item; on this running CR folder they are refused, old and new alike). The four Drivers exit 2 (`cannot read <next>/driver.md`); staged copies give 8010, 8072, 8044, 5828 (PR's figures; today's role-only 59216). `brief foreman --epoch 1`, old and new: exit 0, `epoch: 1`. `CHANTIER_HOST=copilot` still builds host `claude`: Copilot cannot be selected here, so it stays untested.
PR table: foreman, chief-of-staff, griller, retro-critic, demo-explorer and the staged Drivers reproduce exactly. The six workers reproduce the same old-new differences with absolute values 742 lower here than the PR's (`part3-proofs.md` section 4 names the units and measured them in an earlier round; the cause of the constant offset was not traced); the spec roles were measured on another inbox item. The PR's table names neither unit nor SHA: worth adding.
These runs wrote brief files in the surface's git folder; every file left with new-card content was rebuilt with today's cards (`scripts/restore.py`, 14 calls, exit 0).

### C18. Quiz not run (Known gap): VERIFIED as a gap

No model run was made. `just quiz chief-of-staff griller --plan --cards <next> --model claude-opus-5-5`, exit 0:

```text
plan: chief-of-staff 17 cases x 3 runs ... ~$24.02
plan: griller 1 cases x 3 runs ... ~$1.32
plan total: 54 runs, ~$25.34 (cap $10)
```

`just quiz foreman --plan ...`: `plan total: 33 runs, ~$15.40 (cap $10)`. `just quiz cr-driver --plan --cards <next>` fails: `error: brief: cannot read <worktree>/skills/chantier/cards-next/driver.md` / `chantier brief cr-driver exited 2` (same for release-driver and stack-driver). The PR says the quiz was not run; it does not say the Driver quizzes cannot run on this set until `roles.yaml` changes, nor that the plans exceed the $10 cap: worth adding.

### C19. Inventories, completeness: VERIFIED (homes: see F2, F3)

`scripts/inv.py`: Foreman 670 rows (a 111, b 21, c 13, d 9, e 506, f 10), Chief of Staff 1619, Griller 52, host and shared 1880: `empty new home: 0`; `kind-a rows marked inferable: []`; card homes name existing files. `scripts/srcrange.py` over each row's full source range at the base: Foreman, Chief of Staff, Griller `0` rows fail. Completeness table: `references files: 74 SKILL.md: 4 table rows: 78; without a row: [] []`. The refusal lines cited by the protecting tables were checked against the source. The Chief of Staff and Griller inventory is two files, not the one the specification names.

### C25. `just test`, 0 s added: VERIFIED (not recorded by the Driver, see F6)

Same machine, sequential:

```text
base 24111e6d: 2932 passed, 20 skipped in 192.40s (wall 197.9 s)
head 03f973e:  2932 passed, 20 skipped in 171.16s (wall 172.6 s)
```

### C26. Local gates: VERIFIED

`$CHANTIER log CR-507`: "before first push at 03f973e: just check: pass (2932 passed, 20 skipped); just eval-dry-run not owed". Run here at head: `just lint` exit 0 (923 files formatted, ruff "All checks passed!", mypy "no issues found in 536 source files", `uv lock --check`, biome 188 files), `just release-notes` ok, `just test` as C25.

### C27. CI at head, the long gate included: VERIFIED

`gh pr checks 487`, run 45685459142:

```text
just check (macos-latest) pass; just check (ubuntu-latest) pass; just check (windows-latest) pass
just eval-dry-run (ubuntu-latest) pass; just scenario (ubuntu-latest) pass 7m17s
```

No local scenario gate is owed (no stack top); no `gate` was run here.

### C28. PR description, the rest: VERIFIED

- Posted body equals `<CR folder>/pr-body.md` (`diff` of `gh pr view 487 --json body` and the file: only one trailing empty line). It renders as sections, tables and one fold; no image. No username or home path in it or in `evidence/` (`grep` for the username: 0).
- Changes: topic names (234) and the 37 `review_by` names equal `topics.json` (C9). Sibling-edit table lines of `chief-of-staff.md`, `griller-skill.md` and `foreman.md` carry the changes named.
- Autonomous decisions: at base `startup-core.md` holds "retry once only on a transient network error" (line 8), the report fields (line 22) and "read every reading the manifest lists" (line 27), and `review-step.md:15` "`cd` there first"; `git grep -n -E "Report role, project|every reading the manifest|transient network" HEAD -- <next>` and `git grep -n -F '`cd` there' HEAD -- <next>/review-step.md` print nothing (exit 1); "unproved behaviour" rows are filed as kind d (`H-937`, `H-1460`). "Settle alone" lists four refused-forge routes in `chief-of-staff.md`, then "Asks first".
- Test plan: byte copies (C8), unloaded (C4), links (C12), index (C9), Driver table (C13), `just check` (C26) name `03f973e`.
- Review box: `Review: approved at 03f973e (carried from bb6a563)`. Log: "r6 approved at bf4e4c42..., committed as bb6a5639..." and "rebased onto origin/main 24111e6d: bb6a563 -> 03f973e, clean, tree identical (git diff empty); r6 approval carried". `Verified` and `CI green` are unchecked: no claim.
- Known gaps other than F4: `concepts.md:121` wording; English rule under `worker-shell`; no real run; quiz not run; 11 of 18 briefs; cards and topics over budget; Never list of 14 items; allow table's `uv` rules and the unproved launcher rule; host JSON names; `topics/reload.md`; unlinked names; "Stop no sync holder"; inspector-only red-check rule; each matches the files at head.
- Role names: product terms of a change to the roles (pr-template, "The rules").

## Not judged

- No model run and no real run (stated gaps). Copilot untested.
- Judgment of whether the new cards lose no behaviour rests on the later review; only the rows named in F3 and a source check were read here.

## Refusal met during this verification

Early in the run two throwaway files were written to the host's scratch folder, outside this agent's `writes:` folders; the later removal was refused: "refused: a shell write to <host scratch folder>/pr.json is outside the folders this agent may write in (<worktree>; <CR folder>); the shell follows the same rule as Write and Edit". Not worked around; `pr.json` and `cmpbody.py` remain there. Exact text: `work/verifier/refusal.log`. Every later throwaway went to `<CR folder>/work/scratch/ver`.
