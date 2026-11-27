# CR-515: pass on the posted PR description

Head: 22ccbe0b1679de7e56bfb5795b2d2c3681c2acb6

Scope: the description of PR 491 as posted (`gh pr view 491 --repo gsemet/chantier --json body,headRefOid`),
copy in `evidence/desc-pass-posted/body.md` (28357 characters). The change itself is not proved
again: `../verify.md` holds that proof and is left as it was. Base: fbdb53d2a2860a95257235dc7f592ab0e75ce45e.

Scripts (run with `python -I`, read only) and their output, in `evidence/`:
`desc-pass-check.py` / `.txt`, `desc-pass-homes.py` / `.txt`, `desc-pass-gaps.py` / `.txt`;
command transcript `desc-pass-testplan.txt`. The first two arguments are the worktree and the body
copy; `check` and `gaps` also take the rendered HTML (`gh api repos/gsemet/chantier/pulls/491
-H "Accept: application/vnd.github.full+json" --jq .body_html`), `gaps` the CR's work folder.

## 1. Renders, and the layout of pr-template.md (at 22ccbe0)

- `desc-pass-check.txt`, "layout": Summary, Deliverables, Blast radius, Autonomous decisions, Known
  gaps visible, in order; one `<details>` block holding Changes, Human decisions, Impacts, Test plan,
  Internal references; blank line after `</summary>` and before `</details>`: both True.
- Rendered HTML: 1 details block, 1 table, 156 list items all closed, 6 checked boxes; no image;
  no STALE mark; backticks balanced (`desc-pass-gaps.txt`, "rendering").
- No Issues References: `grep -E "^\s*issue:"` over the CR folder's `*.md` finds nothing.
- One departure: the line "Generated with [Claude Code]" follows `</details>`, where the template says
  nothing follows. See the observations.

Holds, but for that line.

## 2. Counts (at 22ccbe0, base fbdb53d2)

`desc-pass-check.txt` and `desc-pass-homes.txt`:

- `docs/protective-rules.md`: 111 rows, 99 held, 0 restored here, 12 to add; each to-add row names
  plan step 15, 20, 16 or 7, or says "no step of plan section 6" (8 rows).
- The four removed files exist at the base (the inventory: 1474636 bytes) and not at the head.
- Open rows at the base: 329 (a 62, b 139, c 1, d 11, e 112, f 4). 112 per-row lines, all unique;
  each quoted span found in the file it names (0 misses).
- Homes: 210 in 18 keys at the base, 127 in 16 at the head, 83 dropped, none added; the 16 per-key
  counts and home names match `HOMES` (listed: 127 kept, 81 dropped; the other 2 are the two
  removed keys). The 101 list ids named after homes all exist in the list.
- "19 more protective": first judging 93, posted 112, 19 added, none dropped
  (`desc-pass-gaps.txt`).

Holds.

## 3. Test plan boxes and their SHAs (`desc-pass-testplan.txt`)

- Behaviour and changed tests, at 22ccbe0: `git diff --stat fbdb53d2..HEAD` lists 9 files, none under
  the CLI's `src/`; `test_card_homes.py` and `evals/kit/dry_run.py` changed, the two inventory test
  modules removed. Holds.
- Local gates at 22ccbe0: `work/scratch/driver-just-check-22ccbe0-bash.log` "2785 passed, 19
  skipped"; `work/scratch/driver-eval-dry-run-22ccbe0.log` "dry run: 26 of 26 cases as expected";
  record notes "before first push at 22ccbe0: just check: pass" and "just eval-dry-run: pass". The
  earlier red run (2 tests, `NO_COLOR=1` in one shell, shown by the debugger at base and head) is not
  this change's. Holds.
- Evidence, before fbdb53d, after 22ccbe0: `git grep` of the four removed names lists six files at
  the base and exits 1 with no output at the head. Holds.
- Review at 22ccbe0, carried from 5d7549e: note "r2 approved at 4d12a5be..., committed as
  5d7549ed..."; `git range-diff 5d7549e~1..5d7549e 22ccbe0~1..22ccbe0` shows `=`. Holds.
- Verified at 22ccbe0: record `verdict result=VERIFIED head=22ccbe0b...` (15:03:00Z). Holds.
- CI green at 22ccbe0: `gh pr checks 491`, five checks, all pass (`just check` on three systems,
  `just eval-dry-run` and `just scenario` on Linux). Holds.

## 4. Known gaps, six bullets (at 22ccbe0, `desc-pass-gaps.txt`)

- "Some `to add` lines name no step": 8 rows say so. Holds.
- N1, N7, C4 held only by topic pages planned for deletion: the rows cite only `topics/` pages
  (output above); that those pages are planned for deletion is carried from 22ccbe0: same head,
  `../verify.md` claim 8, judged against the specifications of the two later changes. Holds.
- No test guards `docs/protective-rules.md`: the only mention of the file under the tests at the head
  is the docstring of `test_card_homes.py` (`git grep`, end of `desc-pass-testplan.txt`); that module
  reads the files under `references/` and the host rows against its own `HOMES` and `FLOOR`, never
  the list, and the inventory's guard modules are removed. So the list can drift. Holds.
- P15/C8 (the bullet added after the VERIFIED): the row reads "recorded with the user's own words and
  a follow-up CR filed first"; `commands/orders_waive.py` line 45 raises "order waive stack: the
  top's gate validates, no --follow-up", and `waive_cr` (line 74) requires one. The bullet says what
  the row leaves out. Holds.
- The long scenario not run locally on Windows (CI ran it on Linux): no gate event for this CR, the
  record reads long gate waived (O-15), CI's ubuntu scenario passes. "A later change of the same
  stack validates it" matches the waiver and the record's assignment; the bullet claims no pass and
  no SHA. Holds; see the observations.
- B18: `topics/host-refused.md` line 10 ends "named by a", line 11 begins "wildcard"; the row's rule
  is whole. Holds.

No `**UNVERIFIED:**` claim in the body (the one occurrence of the word is inside a quoted card
span, row H-507). "None" is not claimed.

## 5. Other claims and internal references (at 22ccbe0)

- Human decisions match `../../02-answers.md` and the specification's decisions; Blast radius gives
  one grade that matches the diff; Impacts "No visual change" is true of the diff.
- Outside "Internal references": no CR, batch, round, order, planning path, question id, CR slug,
  PR number or machine path; the one capitalised role word, "Driver" (line 107), is inside the quoted
  card span of row H-357, not a doer. Title holds none. No user name or home path in the body.

Holds.

## Observations (no effect on the verdict)

- The attribution line after `</details>`: `pr-template.md` says "nothing after `</details>`". The
  host requires the line at the end of a PR description; it renders and claims no change. Earlier
  description passes of batch-31 recorded the same as an observation. Moving it inside the fold,
  last, would meet the template.
- The change the record names as this one's validator (CR-523, PR 492, head d8397a47, base `main`)
  does not contain 22ccbe0 (`git merge-base --is-ancestor` exit 1, `git cherry` "+"). Its recorded
  Windows pass therefore has not run this change; the run that does must be at a head that holds it.
  The batch's status text "validates CR-515..CR-520" for that pass is for the steering session to
  correct; it is not in this PR's description.
- Autonomous decisions mentions "the draft's remarks" and "the cleanup plan", which an outside reader
  has not seen. Neither is an internal reference by the template's list.

VERIFIED
