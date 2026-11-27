# CR-522 verification

Head: 3412cd90a3e33c3b8953e03a23b26b44bfb23227
Base: 4d12a5be711e7af8b9bd59b4ec9432e18a0421de

First verification. Every claim below was judged at 3412cd9, on Windows, from the worktree
(`git rev-parse HEAD` = the head above, `git status --short` empty before and after). `work/scratch`
paths below were mine and are removed; the scripts are in `work/verifier/`, the outputs in
`work/verifier/evidence/` (`E/` below). Long gate: waived (O-15, stack); not run.

## 1. Default widths, order of giving way, thresholds (spec 1 and 2) - 3412cd9, PASS

Command: `uv run --no-sync python work/verifier/probe_widths.py` (reads the drawn text of
`screen.plain`, widths 40..230, one project, several projects, two and four boards, against an
oracle written from section 2). Exit 0. Output `E/widths-drawn.txt`:

```
one       left column first drawn at 122 (spec 122); all defaults from 141 (spec 141)
projects  left column first drawn at 133 (spec 133); all defaults from 162 (spec 162)
boards    left column first drawn at 135 (spec 135); all defaults from 164 (spec 164)
boards4   left column first drawn at 135 (spec 135); all defaults from 164 (spec 164)
case      width mode       left project who event
one         121 Time          0    None  15    42
one         122 Time         28    None  10    20
one         127 Time         28    None  15    20
one         128 Time         29    None  15    20
one         141 Time         42    None  15    20
projects    132 Time          0      20  15    32
projects    133 Time         28      10  10    20
projects    143 Time         28      20  10    20
projects    144 Time         28      20  11    20
projects    148 Time         28      20  15    20
projects    162 Time         42      20  15    20
boards      134 Time          0      22  15    32
boards      135 Time         28      12  10    20
boards      145 Time         28      22  10    20
boards      164 Time         42      22  15    20
projects    117 Time          0      20  12    20
projects     90 Time          0      10  10     5
screens checked against the oracle: 3995; failures: 0
```

So: the left column goes 42 to 28 first, then Who 15 to 10, then Project 20 to 10 (22 to 12);
Event is at least 20 whenever the left column is drawn; without it Project, then Who, widen back;
Event is under 20 only with Project and Who at 10 and no left column.

## 2. `t`, maximized Flow, panel list and Tab (spec 2) - 3412cd9, PASS

Same command and file:

```
case      width mode       left project who event
one         122 t (Ago)      28    None  10    28
one         121 t (Ago)       0    None  15    50
projects    133 t (Ago)      28      10  10    28
projects    132 t (Ago)       0      20  15    40
one          90 maximized     0    None  15    55
projects     90 maximized     0      20  15    34
boards       90 maximized     0      22  15    32
projects     70 maximized     0      19  10    20
one       width 121: panels ['flow', 'ready', 'tasks']; Tab x5 from flow: ['ready', 'tasks', 'flow', 'ready', 'tasks']
one       width 122: panels ['projects', 'agents', 'flow', 'ready', 'tasks']; Tab x5 from flow: ['ready', 'tasks', 'projects', 'agents', 'flow']
active panel at 140: agents; after redraw at 121: flow, drawn ['flow', 'ready', 'tasks']
```

`t` never changes whether the left column shows, its width, Project or Who; Event gains what Ago
frees. The panel list changes at 133 and 135 too (same file).

## 3. Narrow terminals are drawn as before - 3412cd9, PASS

Command: `uv run --no-sync python work/verifier/narrow_same.py`, at the head, then with
`PYTHONPATH` on a `git archive` of 4d12a5be (widths 40..94 one project, 40..99 several projects
and two boards). `E/narrow-same.txt`:

```
screens: 175 head, 175 base
ff2b9e03a3f0c4123d5c6a691ecdec6c2566c96826ef8c16add6efd98a67cd8d
ff2b9e03a3f0c4123d5c6a691ecdec6c2566c96826ef8c16add6efd98a67cd8d
IDENTICAL base 4d12a5be vs head 3412cd9
```

## 4. Real flow: `live --once` against a running board - 3412cd9, PASS

My own board: the head's code, `serve --host 127.0.0.1 --port 0 --ui none`, in a made-up
in-project repository `demo-shop` under `work/scratch` (its own git repository and config folder,
batch-01 with CR-101 working, CR-102 blocked, CR-103 queued). Stopped afterwards by its PID.
No call touched the user's board, planning surface or profiles.

Command: `bash work/verifier/demo.sh live --once` (a pipe), and again with `--transport http`;
both exit 0, widest line 120, no Projects or Agents box, Who 15 (served path in the header
rewritten). `E/once-piped-ws-3412cd9.txt`, `E/once-piped-http-3412cd9.txt`:

```text
$ chantier live --once | (a pipe; the head 3412cd9, my own demo board, made-up data)
chantier live  /work/demo-shop (real path rewritten)…
working 1  ready 0  held 1  done 0
╭─ ▸ Flow ─────────────────────────────────────────────────────────────────╮╭─ Ready ──────────────────────────────────╮
│ Time           Who             Event                                     ││ PR CR State Age Title                    │
│ 11-27 13:45:26 driver          handback CR-102 blocked waits for the us… ││ no PR ready                              │
│ 11-27 13:45:25 foreman         take CR-102                               │╰──────────────────────────────────────────╯
│ 11-27 13:45:17 foreman         take CR-101                               │╭─ Tasks ──────────────────────────────────╮
│ 11-27 13:45:11 chief-of-staff  open                                      ││ State   Task                             │
│ 11-27 13:45:11 chief-of-staff  add CR-103                                ││ working CR-101  export-the-report-as-csv │
│ 11-27 13:45:11 chief-of-staff  add CR-102                                ││         lease 02:25  round 0/3  coder r1 │
│ 11-27 13:45:11 chief-of-staff  add CR-101                                ││ blocked CR-102  fix-the-login-redirect   │
╰──────────────────────────────────────────────────────────────────────────╯╰──────────────────────────────────────────╯
Ctrl-C to quit
```

Before (same command, base source on `PYTHONPATH`, same board, `E/once-piped-base-4d12a5b.txt`):
Projects and Agents drawn at 28, `Who` cut.

```text
$ chantier live --once | (a pipe; base 4d12a5be's source on PYTHONPATH, the same demo board)
chantier live  /work/demo-shop (real path rewritten)…
working 1  ready 0  held 1  done 0
╭─ Projects ───────────────╮╭─ ▸ Flow ─────────────────────────────────────╮╭─ Ready ──────────────────────────────────╮
│ demo-shop  batch-01 run… ││ Time           Who        Event              ││ PR CR State Age Title                    │
│   inbox 0 backlog 0 rea… ││ 11-27 13:45:26 driver     handback CR-102 b… ││ no PR ready                              │
╰──────────────────────────╯│ 11-27 13:45:25 foreman    take CR-102        │╰──────────────────────────────────────────╯
╭─ Agents ─────────────────╮│ 11-27 13:45:17 foreman    take CR-101        │╭─ Tasks ──────────────────────────────────╮
│ Foreman                  ││ 11-27 13:45:11 chief-of-… open               ││ State   Task                             │
│ Driver CR-101 coder r1   ││ 11-27 13:45:11 chief-of-… add CR-103         ││ working CR-101  export-the-report-as-csv │
│                          ││ 11-27 13:45:11 chief-of-… add CR-102         ││         lease 01:16  round 0/3  coder r1 │
│                          ││ 11-27 13:45:11 chief-of-… add CR-101         ││ blocked CR-102  fix-the-login-redirect   │
╰──────────────────────────╯╰──────────────────────────────────────────────╯╰──────────────────────────────────────────╯
Ctrl-C to quit
```

## 5. Real terminal: `chantier live` on that board - 3412cd9, PASS

Command: `uv run --no-sync python work/verifier/terminal.py <out> <png>`: the head's
`chantier live` in a classic console window of its own (8x16 px cells), resized by the window
size and driven by console key events (synthetic input, not a person's drag), the drawn text read
from the console's buffer. Exit 0. `E/terminal-drawn-3412cd9.txt`:

| Step | Terminal | Drawn |
|---|---|---|
| start | 150x28 | left 42, Who 15, Flow active |
| resize | 141 | left 42, Who 15, Event 20 |
| resize | 140 | left 41, Who 15 |
| resize | 122 | left 28, Who 10 (`chief-of-...`), Event 20 |
| resize | 121 | no left column, Who 15 |
| `t` at 122, then 121 | 122, 121 | Ago: left column at 122, none at 121 |
| Tab x4 | 122 (widened from 121, column back) | `> Agents` active |
| resize | 121 | left column gone, `> Flow` active |
| `m`, resize 90 | 121, 90 | Flow over the whole body, Who 15 |
| `m` | 90 | normal layout, no left column |
| `q` | | `q: chantier live exit 0` |

Widening was judged by one column only (121 to 122).

## 6. Screenshot the specification owes - 3412cd9, CAPTURED (not yet in the PR)

`evidence/live-terminal-3412cd9-150.png` (also in `E/`, with a second one at 122 columns,
`E/live-terminal-3412cd9-122.png`): the real console window of claim 5, that window only
(`PrintWindow`), 150 columns, left column shown, running board, made-up data. Command: the one of
claim 5; output:

```
captured live-terminal-150.png: window 1216x487 px, client 1200x448, 150x28 cells (8.00x16.00 px, font 8x16); painted over x 126..1208, y 31..48 (header row from column 15)
```

Edit to disclose in its caption: the header row after `chantier live` is painted grey, because the
served path it prints lies under the home folder (the version, transport and time of that row are
hidden with it). I opened both images: window title `chantier live (demo)`, no username, no home
folder, no other project's data.

## 7. The new tests fail on the base and pass at the head - 3412cd9, PASS

Base: `git archive 4d12a5be` into `work/scratch/base` with the head's `live_world.py`,
`test_live_link.py`, `test_live_panels.py` (compared identical), no `widths.py`. Command:
`PYTHONPATH=<base>/.../cli/src uv run --no-sync --project <worktree> python -m pytest
-c <base>/pyproject.toml --rootdir <base> -p no:cacheprovider -q <files>`; at the head
`uv run --no-sync python -m pytest -p no:cacheprovider -q <files>`.
`-k "closes_the_columns_up or never_shows_or_hides"` with `-n 0` for the new cases.
`E/tests-summary.txt` (details: `E/base-tests.txt`, `E/base-new-cases.log`, `E/head-tests.txt`):

```
base, new cases:                      20 failed, 4 passed, 7 deselected in 2.03s
base, test_live_panels + test_live_link: 20 failed, 28 passed in 7.59s
head, new cases:                      24 passed, 7 deselected in 0.31s
head, panels + link + model:          103 passed in 7.58s
```

Example base failure: `assert (28, None, 10, 62) == (42, None, 15, 43)`. The 4 new cases that
pass on the base (one-122, projects-133, boards-135, Ago 122) are threshold widths where the base
already draws 28/10/10.

## 8. Docs (spec 3) - 3412cd9, PASS

Command: `uv run --no-sync python evidence/live-once-capture.py E/docs-capture-3412cd9.txt <copy
of docs/boards.md>`, exit 0, then `cmp`:

```
cmp: boards.md copy unchanged by the rewrite
cmp: same as evidence/live-once-140.txt
capture block in docs/boards.md, verbatim: True | widest line 140
```

`grep -c -i -E "<user name>|Users|C:\\|C:/|/home/"` on the capture: 0 (served `/work/demo`).
`git diff 4d12a5be 3412cd9 -- docs/boards.md`: "(from 100 columns)" replaced by the rule; the
Flow paragraph names Who 15, Project 20 (22) and how they close up; the Tab row says "without the
left column"; the sentence above the capture says 140 columns.

## 9. Scope and code points of the specification - 3412cd9, PASS

`git diff --stat 4d12a5be 3412cd9`: 8 files: `docs/boards.md`, `scenario/README.md`,
`tui/parts.py`, `tui/screen.py`, `tui/widths.py` (new), `live_world.py`, `test_live_link.py`,
`test_live_panels.py`. No `pyproject.toml`, `uv.lock`, `AGENTS.md`, `hooks/` or web file.
`git diff ... parts.py screen.py`: `LEFT_W` 28 to 42, `RIGHT_W` 44 unchanged; `NARROW`, its
comment and the old width constants gone; `_plan`, `render` and `_maximized` call
`column_widths`; `flow()` takes the widths; both docstrings state widths and order.
`widths.py` only computes and imports no Rich. `wc -l`: `screen.py` 400, `widths.py` 48
(`test_code_targets.py`: `MAX_FILE_LINES = 400`).

## 10. Gates and CI at 3412cd9 - PASS

- `work/gates/just-check-3412cd9.log`, first line `uvx ruff@0.17.5 format --check skills
  scripts`; `2813 passed, 19 skipped in 242.60s (0:04:02)`. Not rerun.
- `work/gates/eval-dry-run-3412cd9.log`, first line `uv run --locked python evals/kit/dry_run.py`;
  `dry run: 26 of 26 cases as expected`. Not rerun.
- `handoff CR-522`: `before first push at 3412cd9: just check: pass`, `before first push at
  3412cd9: just eval-dry-run: pass`, `gate: waived (O-15, stack): run no long gate; validated by
  CR-523`.
- `gh pr checks 490`: `just check` macos, ubuntu, windows `pass`; `just eval-dry-run` `pass`;
  `just scenario (ubuntu-latest)` `pass` 7m15s (run 45998818704).

## 11. PR description - 3412cd9, PASS

`gh pr view 490`: head 3412cd90a3e33c3b8953e03a23b26b44bfb23227, draft, open, MERGEABLE, base
main; the posted body equals `work/pr-body.md` but for one trailing blank line (`diff`).

- Widths and thresholds tables, giving-way chart, `column_widths` signature: claims 1, 2, 9.
- "at 141 columns [Event] goes from 39 to 20": `python work/verifier/event_at_141.py` on base and
  head (`E/event-base-vs-head.txt`): base `width 141: left 28, Who 10, Event 39`, head `width 141:
  left 42, Who 15, Event 20`.
- "between 100 and 121 columns the left column is no longer drawn" and the piped 120-column gap:
  claims 1 and 4.
- "a blocked item's reason can be cut [...] predates this change": the base piped view of claim 4
  and the head's both end the Tasks box at `blocked CR-102` with no reason line; the docs capture
  shows the same for CR-104; the full-height terminal shows the reason.
- 400-line limit, `scenario/README.md` bullet, 140-column test cases and capture: claims 8, 9.
- "CI runs [the scenario] on Linux", local gate figures: claim 10.
- No image in the body; no username or home folder; Known gaps present.
- Now out of date once the screenshot of claim 6 is posted: the Known gaps bullet "No screenshot
  ... yet" and the unchecked "Evidence" and "Verified" boxes. The specification wants that
  screenshot in the PR's Deliverables: it is not there yet.

Verdict of the first pass: VERIFIED (cancelled by the description pass below).

## Second pass: the posted description alone - 3412cd9

Head unchanged (`gh pr view 490 --json headRefOid,isDraft`: 3412cd90a3e33c3b8953e03a23b26b44bfb23227,
draft). Only the description changed since the first pass; claims 1 to 10 were judged at 3412cd9
and were not rerun.

## 12. The posted body renders, and its image resolves - 3412cd9, PASS

- `gh pr view 490 --json body -q .body` against `work/pr-body.md` (`diff`, CR stripped): one
  trailing blank line only.
- `gh api repos/gsemet/chantier/pulls/490 -H "Accept: application/vnd.github.full+json" -q
  .body_html`: headings, the three tables, the Mermaid block, the code block, one `<img
  alt="chantier live at 150 columns">` in Deliverables, one `<details>` holding Changes to
  Internal references with nothing after it, six checked task boxes.
- `curl -sSL` on the attachment URL into an empty scratch folder: `http 200 image/png 22256`.
  `sha256sum` of it, `evidence/live-terminal-3412cd9-150.png` and the copy in `E/`: all
  `9772607331e9e3ca7e9cce2e2ddb84e09a45c175105ccc76a629a99d3713561a`.

## 13. The attached image shows no username or home folder - 3412cd9, PASS

I opened the downloaded attachment: window title `chantier live (demo)`, header row grey after
`chantier live`, made-up `demo-shop` data; no username, no home folder, no path.

## 14. Screenshot, caption, Known gaps and Test plan - 3412cd9, PASS

- The screenshot is in Deliverables with a caption naming `3412cd9`: real console window, running
  board, made-up data, painted header (claims 5, 6). The "No screenshot" Known gap is gone; the
  three gaps left match claims 4 and 10. No `UNVERIFIED` or `STALE` in the body.
- Tests box (20 of 24 fail on the base, 24 pass): claim 7. Local gates box: `head -n1` and the
  result line of `work/gates/just-check-3412cd9.log` (`2813 passed, 19 skipped in 242.60s`) and
  `eval-dry-run-3412cd9.log` (`dry run: 26 of 26 cases as expected`).
- Evidence box: base drawn widths in `E/event-base-vs-head.txt` and `E/base-new-cases.log`, base
  `--once` text in `E/once-piped-base-4d12a5b.txt`; head in claims 1, 4, 6.
- Review box: `log CR-522`: `r1 approved at 4d12a5be711e7af8b9bd59b4ec9432e18a0421de, committed as
  3412cd90a3e33c3b8953e03a23b26b44bfb23227`.
- Verified box: `log CR-522`: `verdict result=VERIFIED head=3412cd90...` (the first pass).
- CI box: `gh pr checks 490`: `just check` macos, ubuntu, windows, `just eval-dry-run`, `just
  scenario (ubuntu-latest)` all `pass`; `gh api .../actions/runs/45998818704`: head_sha
  3412cd90a3e33c3b8953e03a23b26b44bfb23227, `success`.

## 15. Impacts: "The screenshot shows the three columns at their new default widths" - 3412cd9, FAIL

The posted sentence: "The screenshot shows the three columns at their new default widths on a
150-column terminal." The body's three widened columns are the left column and the Flow's
`Project` and `Who` (Summary, first table). The screenshot has no `Project` column: one project is
watched, so the Flow's header is `Time`, `Who`, `Event`. Seen by opening the attachment (claim 13),
and in the console text it was captured from:

Command: `grep -n -E "Time +(Project +)?Who|^=+|150" E/terminal-drawn-3412cd9.txt`

```text
3:== start: terminal 150x28
7:| demo-shop  batch-01 running parallel   || Time           Who             Event                         || PR CR State Age Title
32:captured live-terminal-150.png: window 1216x487 px, client 1200x448, 150x28 cells ...
```

(box characters rewritten as `|`). `E/widths-drawn.txt`, same head: `one 141 Time 42 None 15 20`
(project `None` with one project, at every width from there up). So the screenshot shows two of
the three: the left column at 42 and `Who` at 15. `Project` at 20 is proven only by the drawn
text of claim 1, in no image. Fix: narrow the sentence to the left column and `Who`, saying no
`Project` column is drawn with one project watched.

NOT VERIFIED
