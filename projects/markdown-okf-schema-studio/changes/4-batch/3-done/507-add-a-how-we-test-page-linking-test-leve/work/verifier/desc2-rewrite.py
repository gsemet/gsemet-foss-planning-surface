# Rewrites work/verify.md for the description pass: keeps the first pass's proofs, replaces its
# description section and verdict. Usage: python -I desc2-rewrite.py <work folder>
import pathlib
import sys

work = pathlib.Path(sys.argv[1])
old = (work / "verifier" / "verify-first-pass-6c5106e.md").read_text(encoding="utf-8")


def sub(text, before, after):
    assert text.count(before) == 1, before
    return text.replace(before, after)


head = old.split("## The PR description", 1)[0]
head = sub(head, """Every claim is judged at `6c5106e` unless it says otherwise. Nothing is carried from an earlier judgment.

Result: the change does what the specification says (evidence items 1 to 5, and item 6's list of
differences). The posted PR description fails on three points (claims P1 to P3).
""", """Two passes at this one head. The first (verdict 2026-11-26T15:15:02Z, NOT VERIFIED on the description
only; copy in `<V>/verify-first-pass-6c5106e.md`) judged C0 to C4 and E1a to E6. Those claims keep the SHA
`6c5106e`: carried from 6c5106e: same head and same base, not run again (what the second pass read again is
named in D1 to D7). The second pass judged the description posted since (claims D1 to D7).

Result: the change does what the specification says (evidence items 1 to 6), and the posted PR
description holds.
""")
head = sub(head, "  The posted PR body does not hold them yet: see P1.\n",
           "  The body posted since holds them: see D2.\n")
head = sub(head, "  ship recorded at this head, see the `ship` refusal in P3).\n",
           "  ship recorded at this head: `$CHANTIER log CR-507`, 14:32:14Z, `ship` waits for the CR below).\n")

new = """## The PR description (second pass, at `6c5106e`)

The body judged: `gh pr view 543 --json body -q .body`, sha256 `4e803065ca96c95d...d57fee664e`, saved as
`<V>/desc2-posted-body.md`; PR updated 2026-11-26T15:18:28Z, head `6c5106e4589592002f828b6feb3d545a442591aa`,
draft, OPEN, MERGEABLE (read again at 15:21Z, same hash). It equals `<F>/work/pr-body.md` but for one final
empty line. Its changes from the first body: `<V>/desc2-diff-from-first-body.txt`.

### D1. It renders

- `gh api repos/gsemet/markdown-okf-schema-studio/pulls/543` (HTML media type, `<V>/desc2-posted-body.html`):
  headings Summary, Deliverables, Changes, Impacts, Blast radius, Autonomous decisions, Known gaps, Test
  plan, Internal references; 1 table; 7 task boxes, all checked; 5 `img` tags, each with its alt text; one
  Mermaid block.
- The Mermaid block, put in a one-file bundle in the scratchpad, `node scripts/check-use-case-diagrams.mjs
  <bundle>`: `use case diagrams: 1 StRS checked, all parse (Mermaid 12.2.0)`, exit 0.

### D2. Impacts holds the before and after (former P1: fixed)

- `curl` of the five raw URLs at assets commit `398427751f944842a06fede7b6d18dc51560fc67`
  (`<V>/desc2-images.log`): each `200 image/png`, byte identical (`cmp`) to the file of the same name in
  `<V>/evidence/`. `git ls-remote`: that commit is the head of the CR branch's `-assets` side branch.
- The five downloaded images opened: header with five links (before), six with "How we test" between "How
  we ship" and "Gallery" (after), page top with introduction, two levels and diagram, the table, the
  section with four points. Captions and alt texts say that. No user name and no home folder in any.
- Captions: before at `4e4eeb4` (the base), after at `6c5106e`, as `<V>/evidence/before-after.md` says.
- "light theme only": `git grep` at the head: `test/site/siteTheme.ts:54` `color-scheme:light`, and
  `siteTheme.test.ts:45` forbids `prefers-color-scheme: dark`.

### D3. Each proof names its SHA and is proven (former P2: fixed)

`grep` of the body: each Test plan result, screenshot caption, "Built site" and "Drift probes" names
`6c5106e` or the base `4e4eeb4`, except the Changelog line (a statement about the diff, C0). No `STALE`, no
`UNVERIFIED`; `9d7e788` is gone.

- "13 of the 49 tests ... fail on the base `4e4eeb4`; all 49 pass": E1b and E1a. The list under it matches
  `<V>/base-five-files.log`: 9 failing drift checks (`ENOENT` on `docs/how-we-test.md`, the diagram one on
  `test-levels.svg`), then the four named tests with the messages quoted (`index.html holds <a ...>`, `the
  six links, in order`, actual `Home, Contributing, How we ship, Gallery, Requirements`, missing
  `docs/how-we-test.md`).
- Requirements line: E2 (`just requirements-lint`, 0 errors, `0 files would change`); `git diff
  4e4eeb4..HEAD -- test/site/siteLinks.test.ts`: the added `#S1` marker on the header test.
- Local gates line: `<F>/work/gates/preflight-6c5106e.log` read again: unit 5443/5435/0/8, security 116/116,
  `296 passed`, `1228 requirements, 0 errors`, Sphinx `4 passed`, `found 0 vulnerabilities`, `preflight exit
  0 at 6c5106e...`.
- "Verified at `6c5106e`: the tests against the base, requirements-lint, the site build and the drift
  probes": E1b, E2, E3, E4.
- CI line: `gh pr checks 543` run again: `static`, `static-windows`, `visual`, `visual-2`, `viewer-graph`,
  `report`, `checks` pass; the others `skipping`.
- "Built site" paragraph: `<V>/head-site-scan.log` and `<V>/site-scan.mjs`: 20 headings, one table of 10
  rows, 11 relative `href` and `src` of the page all resolved (`problems: 0`), 643 pages with a header and 0
  without the six links, manifest page and card. `gh run view 45830014522`: `success`, static, visual,
  integration, acceptance and stress jobs included; `git rev-parse cd3b8e6a^{tree} 223a8c49^{tree}`: both
  `e6f6894d...`; `223a8c49` is an ancestor of the head.
- "Drift probes" paragraph: `<V>/probe.sh` (probe 1 removes every `stress` code span) and
  `probe-{1,2,3}-unit.log`: each `tests 5443, pass 5435, fail 1, skipped 7`, with the messages quoted.

### D4. The Review box (former P3: fixed)

- Body: "Review: approved at `6c5106e` (carried from `166532f`: a clean rebase after the last review left
  the files unchanged)".
- `$CHANTIER log CR-507`, 14:30:52Z: `r3 approved at bde4bd58..., committed as
  166532f46b824ebad9659f696835f9254f1f961d`.
- `git rev-parse HEAD^{tree} 166532f4^{tree}`: both `e9e12e6af08cd9ca108c9cbb7f369b67e2220d27`.

### D5. It is consistent with the diff

- Outside Impacts and Test plan the text changed in one place (`desc2-diff-from-first-body.txt`): the e2e
  groups are "described as the first part of the visual scenario ids, which are the folders of their
  captures": `docs/how-we-test.md` lines 202-205; `test/shared/e2eGroups.ts` (ids "used in scenario ids
  (`<group>/vNN-...`) and folder names"), `test/visual/scenarios.ts:329`. This also lists the refinement E6
  noted as unlisted.
- The rest is the text the first pass compared with `git diff 4e4eeb4..HEAD` (same head; `git ls-remote`: the
  base branch is still `4e4eeb4`). Also read now: CORE-086 `implemented_in_files` is
  `test/site/siteTheme.ts` (not in the diff), `tested_in_files` the three test files Changes names.

### D6. Known gaps

- Visible, five bullets, unchanged text, each true (C2, E6 with `<V>/head-capture.log`: 1240 shown 880, C4).
  No `UNVERIFIED` claim. `before-after.md` names no capture that failed: its "none" entries are views of a
  page the base does not have (`base-capture.log`: `not in this site`).

### D7. No internal reference or role outside the last section

- `grep -nE 'STALE|UNVERIFIED|CR-?[0-9]|[Bb]atch|[Rr]ound|Driver|Coder|Inspector|Verifier|Foreman|\\.agents/changes|O-[0-9]'`
  on the body: one line, `- CR-507 how-we-test.`, under "Internal references". "the last review" and "a
  maintainer decision" name no agent role.

## Verdict

Code, page, tests, requirements, site and probes: verified at `6c5106e` (first pass). PR description:
verified at `6c5106e` (D1 to D7; P1 to P3 of the first pass are fixed).

VERIFIED
"""
(work / "verify.md").write_text(head + new, encoding="utf-8", newline="\n")
