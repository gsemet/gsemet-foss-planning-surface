# Change Specification: eval-campaign-cr220

Teach the eval kit's setup script the `ticket-summary` campaign that CR-220 wrote, so its first
real run is staged like every other sandbox campaign instead of by hand.

No `issue:` line: this CR comes from batch-16's retro (point 13), not from a tracker issue.

## Source of the decisions

- `intake/request.md`: batch-16's retro, point 13, reviewed by an advisor: `evals/kit/setup.py`
  lacks the campaign for CR-220 (a ticket's summary, plan and demo posted on the user's yes).
  "Eval kit only, no long gate."
- `02-answers.md` (the Chief of Staff with the user, 2026-11-13):
  1. The proposal as filed is the scope; points the request does not settle take this
     specification's defaults, listed as open points at the end.
  2. The CR joins the running batch-17.
- CR-220's archive (`.agents/changes/5-archives/261113-1646-220-ticket-summary-on-source/`): its
  specification, section 8, wrote `evals/ticket-summary/RUNBOOK.md` and the README row; its PR
  body says (Human decisions) "the eval runbook has the operator set the sandbox up by hand rather
  than extending the kit's setup script" and (Known gaps) "the eval kit's setup script does not
  know the new campaign ... extending it is a possible follow-up". This CR is that follow-up.

## Goal, in the user's terms

`uv run --no-project python evals/kit/setup.py ticket-summary <workspace>` stages the
`ticket-summary` campaign as it stages `full` or `real-direct`: it checks the sandbox is at its
base, takes the run's number and prefix, clones the sandbox, runs `chantier init` and
`uv sync --locked`, writes the run's record and the workspace's Claude settings, and prints what
the operator does next: the exact `gh issue create` line for the campaign's frozen issue, and the
frozen text of the ticket-less request. Two runs of the campaign then start from the same issue
and the same request, so they compare.

## What changes

Eval kit, its docs, and one structure test. No change to the CLI
(`skills/chantier/scripts/cli/src/`), the cards, the agent files, `hooks/`, `types/` or the
scenario.

### 1. The campaign's frozen texts: `evals/kit/ticket-summary/` (new folder)

- `evals/kit/ticket-summary/issue.md`: the body of the issue the operator creates. A visible
  change, so the Chief of Staff can judge a demo worth making (it imitates without the product).
  English. Content (wording may be polished, keep the shape and size):

  ```markdown
  The list page and the item pages are bright white. I read my list in the evening and the
  glare is hard on the eyes.

  Could shelf offer a dark theme? Following the system's light or dark setting would be enough
  for me; I do not need a switch on the page.

  Nothing else needs to change.
  ```

- `evals/kit/ticket-summary/chat-request.md`: the text the operator, playing the user, types in
  the chat to file the second CR, with no ticket. A change that is not visible, so it needs no
  demo either way. Content:

  ```markdown
  When shelf runs, it prints nothing for each request it serves. Add a `--verbose` option to
  `python -m shelf` that prints one line per request (method, path, status) to the terminal.
  Without the option, nothing changes.
  ```

- The issue's title is a constant of the campaign in `setup.py` (section 2): `Dark theme for the
  reading list`. The created issue's title is the run's prefix, a space, then that title.

The texts name no CR, batch, path or person (they are what a reporter and a user would write).

### 2. `evals/kit/setup.py`

- **The campaign.** Add to `CAMPAIGNS`:

  ```python
  "ticket-summary": {"host": "claude", "batches": [],
                     "issue": {"title": "Dark theme for the reading list",
                               "body": "ticket-summary/issue.md",
                               "chat": "ticket-summary/chat-request.md"}},
  ```

  It has `batches` (so `__main__` routes it to `sandbox_main`, the sandbox path) and none in it:
  no frozen CR is placed, no `open` line is printed. `sandbox_crs()` returns `[]` for it.
- **`sandbox_main`**, unchanged in its steps 1 to 5 (preconditions, run number and prefix, clone,
  `init`, `uv sync --locked`, settings, `place_crs` with no CR, the run record), with:
  - the run record (`<workspace>.run.json`) gains, for a campaign with `issue`, the key
    `"issue": {"title": "<prefix> Dark theme for the reading list", "body": "<absolute path of
    issue.md>"}`; `"crs"` is `[]`;
  - the summary prints, for a campaign with `issue`, in place of the CR list and the `open`
    lines:
    - `issue     gh issue create --repo gsemet/chantier-eval-sandbox --title "<prefix> Dark
      theme for the reading list" --body-file <kit>/ticket-summary/issue.md   (run it, then note
      its number)`, the body path quoted only when it holds a space (as `merge_command()` does);
      the repository from `sandbox.REPO`;
    - `chat      <the absolute path of chat-request.md>   (the ticket-less request, typed in the
      chat)`;
    - no `merge` line (no PR is merged in this campaign) and no `batch <n>:` line;
  - the CRs line reads `CRs placed in .agents/changes/3-ready/ (0):` as today's code prints it, or
    is left out when the list is empty: the Driver chooses one and the dry run checks it.
- **Setup creates no issue.** It stays read-only on the forge, as the README says ("never resets
  and never pushes"); the operator runs the printed line (the runbook's setup step 1).
- **`allow_rules(spec)`** for a campaign with `issue`: no merge rule (it merges nothing); in its
  place, in both the `Bash(...)` and `PowerShell(...)` forms, `gh issue comment *` and
  `gh issue artifact create *`: the two posting commands the Chief of Staff's "Ticket summary" step
  7 runs on GitHub, which would otherwise wait on a permission prompt the real user is not there to
  answer. Nothing else. The other campaigns' rules do not change.
- **The module docstring** names `ticket-summary` among the sandbox campaigns, and says it places
  no CR and prints the issue's `gh issue create` line and the chat request's path instead of `open`
  lines; it creates nothing on the forge.
- **The run's number** is unchanged: 1 plus the highest `[eval <n> ` among PR titles. A
  `ticket-summary` run opens no PR, so, as the README already says, it leaves its number free for
  the next run; the two prefixes still differ by their date or campaign name.

### 3. `evals/kit/dry_run.py`: a new case `ticket-summary-setup`

The README's rule: "A new campaign behaviour ... gets its case in the dry run in the same PR."
Add the case to `CASES` and to the docstring's list:

    ticket-summary-setup   setup of `ticket-summary` on the local sandbox: no CR placed, the issue line, no forge write

It builds a `World` at the base (no leftovers), runs `captured(setup.sandbox_main,
"ticket-summary", world.ws)`, and needs:

- exit 0;
- `.agents/changes/3-ready/` holds no CR folder;
- `<ws>.run.json` has `"campaign": "ticket-summary"`, `"crs": []`, and `"issue"` with the
  prefixed title;
- the output holds one `issue` line starting `gh issue create --repo gsemet/chantier-eval-sandbox
  --title "<the run's prefix> Dark theme for the reading list" --body-file`, whose body path is
  the kit's `ticket-summary/issue.md`, and a `chat` line naming `chat-request.md`; no `merge` line
  and no `batch ` line;
- `.claude/settings.local.json` allows exactly the four issue rules (two commands, two forms) and
  no merge rule;
- the fake forge (`sandbox_forge.py`) received no `issue` call and no write: setup created
  nothing on it (read from the forge's call log or state, whichever `sandbox_forge.Forge` keeps).

`sandbox_forge.py` needs no new command: setup does not call `gh issue`. If the case shows it does
need one, that is a finding to report, not a reason to add the command.

The `clean` case and the others do not change.

### 4. `skills/chantier/scripts/cli/tests/test_structure.py`

`test_the_sandbox_campaigns_name_only_frozen_crs_with_hidden_tests` (line 503) asserts the set of
campaigns with `batches` is exactly `{"full", "real-foreman", "real-direct", "copilot"}`. It
becomes those four plus `"ticket-summary"`, and the test also asserts that `ticket-summary` places
no CR (`setup.sandbox_crs(...) == []`) and that the files its `issue` names exist under
`evals/kit/`. Nothing else in the test changes.

### 5. `evals/ticket-summary/RUNBOOK.md`

"Setup, by the operator" becomes:

1. Prepare as the evals README's sandbox campaign text says, with
   `uv run --no-project python evals/kit/setup.py ticket-summary <workspace>`.
2. Run the `issue` line setup printed (the frozen issue, its title with the run's prefix); note
   its number `<n>`.
3. File a CR from it (`$CHANTIER file`, with the `issue: <link>` line under the title of
   `01-intent.md`), and a second CR from the chat with the text of the `chat` line's file, with
   no ticket.

The rest of the runbook (the user's turns, "Pass when", "At the end") does not change. The
sentence "with these differences: no batch is opened, and no PR is merged" stays, and adds "and
setup places no frozen CR".

### 6. `evals/README.md`

- Lines 6, 42 and 47: the sandbox campaigns are named as five, `ticket-summary` included ("The
  text common to the five sandbox campaigns").
- The preparation's step 2 (lines 57-64): one sentence: for `ticket-summary`, setup places no CR
  and prints, instead of `open` lines, the issue's `gh issue create` line and the chat request's
  file; it creates nothing on the forge.
- The kit table's `kit/setup.py` row (line 260): add "for `ticket-summary`, the issue's
  `gh issue create` line and the chat request, with the two posting commands allowed"; the
  `kit/dry_run.py` row (line 273) adds the new case to its planted list; a new row for
  `kit/ticket-summary/`: "The `ticket-summary` campaign's frozen issue and ticket-less request".
- The campaign table's `ticket-summary` row (line 25) is unchanged ("not run yet").

## Out of scope

- Running the campaign: its first real run comes after the merge, by the operator.
- The checklist for the next real eval named in the request (CR-216's early `context:` hand-back
  and shell guard, CR-218's `--plugin-dir` route, CR-220's posting routes): not part of this CR.
- Setup creating, commenting on or closing the issue: the operator does it, as the runbook says.
- `sandbox.py reset` closing issues, or `survey()` counting open issues: unchanged (the runbook's
  end step closes the issue).
- `audit.py` and `judge.py`: the campaign opens no batch and no PR; the runbook's "Pass when" is
  checked by the operator with `gh`. No `--sandbox` audit support for it.
- Any card, CLI, agent file, hook or scenario change; the GitLab and Jira routes.
- The run-number rule (PR titles only).

## Evidence

- `just check` passes (Linux, macOS, Windows in CI); the updated structure test passes.
- `just eval-dry-run` passes at the pushed head, the new case `ticket-summary-setup` included,
  every other case as before; its output is the Verifier's evidence (`work/verifier/evidence/`),
  quoted in the PR body (evals README, "Changing the kit").
- The output of `uv run --no-project python evals/kit/dry_run.py --case ticket-summary-setup
  --keep`, with the kept workspace's `run.json` and `.claude/settings.local.json` shown, kept as
  evidence.
- No `just scenario`: the CLI, the cards and the scenario do not change (AGENTS.md; the request
  says "no long gate"). No `just mod`: `hooks/` and `types/` do not change.
- An independent review of the whole campaign path (setup, the runbook's run, the absence of
  audit and judge for this campaign) by a reviewer that did not write it, before the merge (evals
  README, "Changing the kit").

## Open points, with the default taken

1. **Setup creates the issue, or the operator does?** Default: the operator, from the line setup
   prints; setup stays read-only on the forge as the README says of it.
2. **The frozen issue and request texts** (a dark theme; a `--verbose` request log): the
   specification's choice, a visible change for the ticket so a demo can be judged, a non-visible
   one for the ticket-less CR.
3. **Allow rules for posting** (`gh issue comment *`, `gh issue artifact create *`): default, yes,
   so the operator's run does not stall on a permission prompt; the "nothing before the yes"
   check (runbook, Pass (a)) still reads the issue itself.
4. **The run's number:** default, unchanged (PR titles only); a `ticket-summary` run leaves its
   number free, as the README already says of a run that opens no PR.
5. **Audit and reset:** default, untouched (no `audit.py --sandbox` for this campaign, no issue
   in `reset`'s survey).
