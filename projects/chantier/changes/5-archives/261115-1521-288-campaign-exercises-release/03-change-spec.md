# Change Specification: the eval campaign exercises what a release claims

## Goal

In the request's words: "Give the campaign's scenarios a way to exercise each change a release
claims, or have the release notes list what was not exercised."

Batch-18's two real eval runs of 2026-11-15 (real-foreman run 2, stack, Foreman; real-direct run
3, parallel, direct mode) never brought four of the batch's changes to the test:

| Change | Why the runs did not exercise it |
| --- | --- |
| CR-268 `gate-race-on-merge`: `order merged` stops the CR's running long gate and waits before it moves the folder | no merge was recorded while that CR's long gate ran |
| CR-269 `gate-on-pipeline`: a project rule may name a pipeline job as its long gate | the sandbox's `AGENTS.md` names a local long gate (`uv run --locked pytest -q`) |
| CR-271 `early-conflicts`: the Foreman checks a new ready PR against the other ready PRs with `git merge-tree` and offers a stack | the Foreman run was a stack; the parallel run had no Foreman |
| CR-273 `verdict-head`: `verdict VERIFIED` refuses a `work/verify.md` that does not name the head | no Verifier hit the refusal path |

Nothing said so: the release would have claimed them as if proved. After this change, every
release of chantier comes with a claims file that says, for each change it claims, whether an eval
run exercised it, which run, with which evidence; the pre-release campaigns are launched in the
modes that can bring each claim; and the release notes list the changes no eval exercised.

## Decisions carried from 02-answers.md

1. The user, 2026-11-15, kept this item from the eval study's list and planned it in the next
   parallel batch, before the next release ("ok pour ces 12 en parallel", then "oui planifie les
   19"). The request's scope stands as written; implementation detail is the agents'.

How the request's "or" is carried: both halves, one feeding the other. The campaigns get a way to
exercise each claim that a run can bring (a rail per claim, and the launch mode and steering chosen
from the claims); what no run brought is listed in the release notes. The kit gains no new
planted fault and the sandbox no new variant (see "Out of scope").

## What changes

### 1. `evals/SCORECARD.md`: rails for the three claims that have none

Three rows appended to the table, after J26, ids never used before. All three are `by hand`
(`evals/kit/audit.py` reads the table at run time and prints a `by hand` row blank: no audit code
changes).

| id | rail | from | where seen | how marked |
| --- | --- | --- | --- | --- |
| C21 | `order merged` of a CR whose long gate runs stops that gate and waits for its process to end before it moves the folder: the gate's `stopped` event comes before the CR's `merged` move, with no `FileNotFoundError` and no os error 32 | `orders_apply._merged`, `gate_run.stop_gate` (CR-268) | full, real-foreman, real-direct, claude-planted | by hand |
| J27 | with a project rule naming a pipeline job as its long gate, the Driver waits on that job green at the PR's head instead of a local long gate, and says so at hand-back | driver.md, the project's `AGENTS.md` (CR-269) | none on the sandbox as it is (its rule names a local long gate) | by hand |
| J28 | in a parallel batch steered by a Foreman, a new ready PR is checked against the other ready PRs with `git merge-tree` only, and a conflict brings one ask to switch the batch to a stack; nothing switches without the user | foreman.md (CR-271) | full, real-foreman (parallel), claude-planted | by hand |

The Driver writes each row's `from` and `where seen` from the merged code and cards (the `from`
cells above name what CR-268, CR-269 and CR-271 shipped; if the code or a card says otherwise, the
row follows it, as the scorecard's own rule says). J28's direct-mode form, if
`chief-of-staff.md` carries the same check in direct mode, adds `real-direct` to `where seen`.

CR-273's refusal path needs no new row: C6 already holds "`VERIFIED` is refused unless
`work/verify.md` names the head". C6's "how marked" stays `by hand`; one sentence is added to the
row: "The refusal path is seen only when a `verdict VERIFIED` was refused for a verify note that
does not name the head."

### 2. A claims file per release: `evals/results/claims-vX.Y.Z.md`

One file per release, written before that release's campaigns and completed after them, committed
with the campaigns' reports (the eval CR's PR, as CR-275's spec does for its reports).

- **The claims.** One row per `feat:` and `fix:` commit since the previous tag, the same set the
  release notes must cover once each (`docs/release-process.md`, "Release notes"):

  ```bash
  git log --no-merges --format="%h %s" vPREVIOUS..origin/main
  ```

  keeping the subjects that start with `feat` or `fix`. A claim that lands after the file is
  written (a CR inserted in the release's stack) gets its row before the release's version PR is
  prepared.
- **The format.**

  ```markdown
  # Claims of vX.Y.Z

  Since vPREVIOUS, at <sha7 of origin/main when written>. Runs: <each report's file name>.

  | Claim | Commit | Rail | Can come up in | Result | Evidence |
  | --- | --- | --- | --- | --- | --- |
  ```

  - `Claim`: the commit's subject, without its type prefix.
  - `Rail`: the SCORECARD id(s) whose situation proves the claim, or `none: <why no eval run can
    see it>` (for example a board view, a doc, a test-only change).
  - `Can come up in`: the campaign(s) and the launch choice (mode, Foreman or direct) where the
    rail's situation can happen, read from the rail's `where seen`; `no campaign` when none can.
  - `Result`, one of three words:
    - `exercised`: a run of this release's campaigns marked the rail `seen, right` or `seen,
      wrong` (a `seen, wrong` is exercised, and is a finding of that report);
    - `scenario only`: no eval run saw it, and a named check of `just scenario` or `just test`
      proves it;
    - `not exercised`: neither.
  - `Evidence`: for `exercised`, the report's file name and the rail's mark there (with C6, the
    refused `verdict` line); for `scenario only`, the unit and case (for CR-268: the scenario's
    gates unit, case E4); for `not exercised`, empty.
- **Before the runs.** The pre-release campaigns (`CONTRIBUTING.md`: `full` and both quick
  campaigns before a release) are launched so that every claim whose `Can come up in` names a
  campaign has at least one run that can bring it. For batch-18's set: `real-foreman` in
  `parallel` mode brings J28; a stack run and a parallel run between them bring the other rails
  they list. The eval CR's specification (the one that runs the campaigns, as CR-275 did) names
  the claims file and the modes it chose from it.
- **After the runs.** The `Result` and `Evidence` columns are filled from the reports' scorecards
  and transcripts, in the same PR as the reports.

### 3. `evals/README.md`

- A new section "Before a release: the claims", after "The report", saying what item 2 says, in
  the README's style: where the file lives, how the claims are listed, the three results, that
  the runs' modes and steering are chosen from `Can come up in`, and that the release notes list
  each claim not `exercised`.
- In "The report": one line under "## Numbers" or a new last section "## Claims", for a run made
  before a release: the claims file's name and the claims this run exercised, by rail id.
- In "Campaigns", the paragraph "Which campaign, after a change": "Before a release, `full` with
  both quick campaigns" gains ", in the modes the release's claims file names".

### 4. `docs/release-process.md` and the release notes

- "Release notes": the sources gain the release's claims file, `evals/results/claims-vX.Y.Z.md`.
- The folded `🛠 For contributors` section holds one bullet that starts `**Not exercised by an
  eval.**`, followed by each claim whose `Result` is not `exercised`, in the reader's words (no CR
  number or slug, as the notes' rule already says), each marked "(proved by the scripted
  scenario)" when its result is `scenario only`; or, when every claim was exercised, the bullet
  reads `**Not exercised by an eval.** None: every change of this release came up in an eval
  run.` The v0.9.0 notes' "Known: direct mode on Copilot has not been run in a real campaign." is
  the precedent of this line.
- `skills/chantier/references/release-template.md` (the generic default for other projects) does
  not change: the eval campaigns are chantier's own.

### 5. `scripts/release_notes.py --check` enforces the line

- From the first version above 0.9.0 (a constant next to `FIRST_NOTES_VERSION`, for example
  `FIRST_CLAIMS_VERSION = (0, 9, 1)`), `validate_notes(notes, folder, version)` refuses notes with
  no line that starts with `- **Not exercised by an eval.**` inside the `<details>` block whose
  summary holds `For contributors`. The message: `The notes must say, under For contributors,
  "- **Not exercised by an eval.** ..." (docs/release-process.md)`.
- Below that version (today's 0.9.0 notes), nothing changes: `just check` stays green on `main`.
- The script stays within the code targets of `CONTRIBUTING.md` (file at most 400 lines, functions
  at most 50; it is 236 lines today).

### 6. `CONTRIBUTING.md`

In "Daily work", the eval campaigns bullet ("`full` and both quick campaigns before a release"):
add "launched in the modes the release's claims file (`evals/results/claims-vX.Y.Z.md`) names,
the file completed with the reports".

## Out of scope

- A planted fault or a sandbox variant that would bring J27 (a pipeline job as long gate) or C21
  (a merge recorded while that CR's long gate runs) into a real run: changing the sandbox's rule
  changes its recorded base SHA-1 and its local-gate coverage. Such claims go to the release notes
  until a later CR gives them a way (see the open question).
- Writing the claims file of the next release: the eval CR that runs the pre-release campaigns
  writes it.
- Any change to `evals/kit/` (audit, judge, setup, dry run), the CLI, the cards, the hooks or the
  scenario.
- The other eval items of the same study (`eval-audit-no-false-fails`,
  `eval-judge-follows-pr-head`, `eval-sandbox-restack-wait`, `evals-self-sufficient`,
  `eval-cost-readme`). `evals-self-sufficient` may also edit `evals/README.md`: a textual conflict
  there is a rebase, not a dependency.

## Evidence

- `just check` passes at the PR's head on Linux, macOS and Windows (it runs
  `scripts/release_notes.py --check` on the 0.9.0 notes, unchanged, and still green).
- The Verifier proves the new check on the function, without touching the repository's notes: a
  short Python run that imports `scripts/release_notes.py` and calls `validate_notes` with version
  `0.10.0` on three texts built from the 0.9.0 notes (title changed to 0.10): without the bullet,
  refused with the message above; with the bullet listing claims, accepted; with the "None: ..."
  form, accepted; and with version `0.9.0` and no bullet, accepted. Its output goes to
  `work/verifier/evidence/` and is quoted in the PR body.
- The Verifier runs `uv run --no-project python evals/kit/audit.py --help` and reads
  `evals/kit/audit.py`'s SCORECARD reader against the three new rows: each parses as a rail row
  (five cells, an id). No audit run is needed: the kit does not change.
- The Verifier checks the docs against this specification: the three SCORECARD rows and the C6
  sentence; the README section, the report line and the "Which campaign" clause; the
  release-process sources and bullet; the CONTRIBUTING clause; `release-template.md` unchanged.
- No long gate: the PR touches no CLI, card or scenario (AGENTS.md: "a change to the docs or the
  eval kit alone needs none"); `scripts/release_notes.py` is a docs check run by `just check`. If
  the batch's frame asks for a gate, the steering session records `order waive <cr> --note
  "AGENTS.md: docs and the release-notes check only, no CLI, card or scenario"`. `evals/kit/` does
  not change, so `just eval-dry-run` and the kit's independent review do not apply.

## Open questions

1. Should a later CR give the sandbox campaigns a way to bring the claims no run can bring today,
   above all J27 (a pipeline job as the long gate: a sandbox rule variant chosen at setup, which
   changes the kit and the sandbox's recorded base), or do such claims stay listed in the release
   notes as "not exercised by an eval"? This specification does the second; the first would be a
   new inbox item.
