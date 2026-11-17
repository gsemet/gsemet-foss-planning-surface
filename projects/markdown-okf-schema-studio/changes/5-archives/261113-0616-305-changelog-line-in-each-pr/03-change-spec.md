# Change specification: release process fixes from the v1.7.1 retro

Triage: automatable (short specification; the owner does not review it). Read the files at
`origin/main` (the local `main` is behind). Documents only: no behaviour change, no SwRS, no
`CHANGELOG.md` line for this CR. Commit type `docs:` (no scope).

## Goal

From the v1.7.1 retro, four fixes to the release documents:

1. Each PR adds its own `## Unreleased` line to `CHANGELOG.md` in the same PR. In 1.7.1 the lines
   were written late, in the version commit.
2. Release step 6 names the Marketplace check that counts and says how long the listing page can
   lag behind it.
3. Release step 8: when the release closed no issues, one line in `report.md` ends the step, and the
   owner is not asked to approve anything.
4. A release may also ship as a stack that is ready to merge, with the version PR on top (owner,
   2026-11-12: « Yes, and update the guide »).

## Changes, file by file

### `.github/PULL_REQUEST_TEMPLATE.md`

Add one checkbox to "Test plan", after the "Requirements" checkbox. Add no new section: CI rule 10
lists the template sections by name.

```markdown
- [ ] Changelog: one user-facing line under `## Unreleased` in `CHANGELOG.md`
      <!-- or "No user-facing change" -->
```

### `.agents/guidelines/release-process.guidelines.md`

This is a project guideline, so `test/build/test_guideline_isolation.py` applies: no role names
("driver", "Foreman", "Chief of Staff", "Inspector", "coder"), no link to the process guideline and
no mention of its name. Say "the agent that runs the release" instead.

- **Intro paragraph** ("The goal: ..."): replace "The real VS Code jobs stay on `main`, so the
  version commit is never stacked on top of development: the development lands first, then the
  release runs on its own." with this meaning: the version commit lands only after a green heavy
  run of the exact code it releases. That happens in one of two ways:
  - the default: the stack lands on `main` first, then the heavy run of `main` HEAD;
  - the version PR on top of a ready stack, with the heavy run dispatched on the top branch (new
    section below).

  Keep the 1.3.0/1.3.1 reason: the version push is never the first real VS Code run of its code.
- **Rules of a release, "Merge rights"**: the owner merges the version PR and, when it tops a
  stack, the whole stack with it.
- **Step 2, changelog lines**: every PR with a `feat` or `fix` commit adds one user-facing line to
  `CHANGELOG.md` `## Unreleased`, in that PR. It appends the line at the end of the list. A rebase
  conflict on that block keeps both lines. PRs that are only `test`, `ci`, `build`, `docs` or
  `chore` add no line and tick the template checkbox with "No user-facing change". A `feat` or
  `fix` PR that landed without its line is a gap of that PR: a fix PR adds the line before the
  version commit. The version commit only moves the lines under the version heading.
- **Steps 2, 4 and 5**: each one points to the new section for the stacked way. Step 2's "Once
  the stack is merged, every other merge is held" also applies from the dispatch of the branch
  heavy run in the stacked way.
- **New section "The version PR on top of a stack"**, after "The steps of a release". The version
  PR may be the top PR of a stack that is ready to merge:
  1. The stack's bottom is based on the current `origin/main` HEAD. Every PR below the version PR
     is ready (CI green, review done). The version commit (`just bump-version`, changelog heading,
     notes folder) is made on the top branch, so Commitizen sees the commits of the stack.
  2. From here until the release is published, every other merge is held.
  3. Dispatch the heavy run on the top branch:
     `gh workflow run ci.yml --ref <top-branch> -f heavy=true`. Find it with
     `gh run list --workflow ci.yml --branch <top-branch> --event workflow_dispatch --limit 3`. Then
     use the `gh run watch` and `gh run view ... --jq` commands of step 4, reading the result of
     each of `integration` and `stress`. The run's `headSha` must be the top branch's head; a push
     to any PR of the stack starts this step again. Red jobs and flakes are handled as in step 4.
  4. Only then the version PR is marked ready. The owner merges the whole stack by rebase, bottom
     up, in order (`gh stack merge <version PR> --rebase`, see `stacked-prs.guidelines.md`).
  5. The version push on `main` runs the heavy jobs again (CI rule 14). It stays the final gate and
     makes the tag. Steps 6 to 8 follow as usual.
- **Step 6, Marketplace check**: what counts is an HTTP 200 on
  `https://marketplace.visualstudio.com/_apis/public/gallery/publishers/GaetanSemet/vsextensions/markdown-okf-schema-studio/X.Y.Z/vspackage`
  (for example `curl -sS -o /dev/null -w '%{http_code}' -L <url>`). The listing page is not
  checked. Write: "The listing page can lag by several minutes (more than 3 seen in 1.7.1); it is
  not a gate." Give no fixed number.
- **Step 8, empty list**: "No issue closed by this release: write that line in `report.md`; the
  step ends, no approval is asked."
- Leave the Open VSX parts of the guideline as they are (Open VSX is out of this batch).

### `CONTRIBUTING.md`, "How to Release"

CONTRIBUTING.md is a project rule too, so the same rule applies: no role names.

- **Intro paragraph** ("Make the version commit (step 3) only after a green heavy run of `main`
  HEAD (step 1)"): add "or of the top branch of the stack when the version PR tops it", and point
  to "The version PR on top of a stack" in the release guideline.
- **Step 1**: add one sentence for the stacked way: dispatch
  `gh workflow run ci.yml --ref <top-branch> -f heavy=true` and wait for green on that head,
  instead of merging first.
- **Step 2**: keep the `git log ... | grep -E '^\S+ (feat|fix)'` check as the release's safety
  net. Replace "and add the missing ones in the release branch" with: a missing line is a gap of
  its PR, and a fix PR adds it before the version commit. Each PR adds its own line, appended at
  the end of `## Unreleased`.
- Leave the Open VSX and "GitHub Configuration" text alone.

### `.agents/guidelines/ci.guidelines.md`, rule 14

The last sentence says "The version commit itself is made only after a green heavy run of `main`
HEAD". Change it to "... of `main` HEAD, or of the top branch when the version PR tops a stack
(see release-process.guidelines.md)". The rest of the sentence stays: "the heavy run of the version
push stays the final gate". This keeps it consistent with the owner's decision.

### `.agents/guidelines/change-requests-lifecycle.guidelines.md` (process guideline)

- **Lifecycle table**:
  - Step 5 Code: the coder writes the `## Unreleased` line in the same round as a `feat` or `fix`
    change.
  - Step 6 Review: the Inspector checks that the line is there, or that the change is not
    user-facing.
  - Step 8 PR: the body's Changelog checkbox is ticked, or says "No user-facing change".
- **"Planning a release"** and **"Release driver"**: allow the stacked way. When the version PR
  tops the stack, the Foreman starts the release driver once the PRs of the stack are ready, not
  merged. The heavy run is the top branch's, and the owner merges the whole stack.
- **Release driver prompt**: "a green heavy run on `main` HEAD" becomes "a green heavy run on
  `main` HEAD, or on the stack's top branch when the version PR tops the stack".
- **"Release driver", "Lists" bullet**: add the empty-list case, in the same wording as release
  step 8: with no issue closed, the line goes in `report.md`, and nothing is drafted or approved.

## Decisions carried from `02-answers.md` and the advisor's report (this CR's section)

- One CR for the three retro fixes. release-marketplace-check-of-record and
  release-step8-empty-issue-list are folded in.
- The documents require the changelog line (lifecycle guideline and the template checkbox). No
  CI check enforces it.
- Advisor answers 1 to 10, adopted as INTERNAL decisions: which PRs owe a line, a checkbox rather
  than a section, lifecycle steps 5, 6 and 8, CONTRIBUTING step 2 kept as the safety net, lines
  appended at the end, the `vspackage` check of record, no fixed delay, the step 8 wording mirrored
  in both documents, no role names in project rules, and this CR first in the stack, so the other
  CRs of the batch add their own lines.
- Delivery: the version PR may top a ready stack once the heavy run on the branch is green. The
  version push on `main` stays the final gate. The 1.3.0/1.3.1 reason is kept, and the branch heavy
  run meets it.
- Open VSX is out: none of its text is touched.
- My own reading, beyond the decisions: `ci.guidelines.md` rule 14 and the lifecycle guideline's
  release sections say the same thing as the release guideline. They are updated so that no
  document contradicts the new way (advisor answer 8 uses the same reasoning). The "hold other
  merges from the branch heavy run" rule follows from "the version push stays the final gate on
  the tested code".

## Out of scope

- A CI or `just check` rule that enforces the changelog line.
- Open VSX (publication, `ovsx`, its guideline text).
- Any change to `src/`, the requirements bundle or `CHANGELOG.md` content.
- Changing `stacked-prs.guidelines.md` (merging bottom up already covers a version PR on top).

## Evidence

- `just check`. It covers the Markdown format of the guidelines and
  `test/build/test_guideline_isolation.py` (no role names or process link in the release
  guideline, CONTRIBUTING.md or ci.guidelines.md).
- `just preflight` before the PR is ready (constitution, section 4).
- Each of these greps returns at least one match at the head:
  - `grep -n 'Changelog' .github/PULL_REQUEST_TEMPLATE.md` (inside "Test plan");
  - `grep -n 'vspackage' .agents/guidelines/release-process.guidelines.md`;
  - `grep -n 'No issue closed' .agents/guidelines/release-process.guidelines.md .agents/guidelines/change-requests-lifecycle.guidelines.md`
    (both files);
  - `grep -n 'top branch' .agents/guidelines/release-process.guidelines.md CONTRIBUTING.md .agents/guidelines/ci.guidelines.md`;
  - `grep -n 'Unreleased' .agents/guidelines/change-requests-lifecycle.guidelines.md` (steps 5, 6
    and 8).
- `grep -n 'add the missing ones in the release branch' CONTRIBUTING.md` returns nothing.
- The template still has exactly the sections Summary, Deliverables, Changes, Impacts, Blast
  radius and Test plan.
- Scenario: read the release guideline from step 1 to step 8. It must describe both ways without
  contradiction: the stack lands first, or the version PR tops it. In each way, nothing is tagged
  before a green heavy run of the released code and the green heavy run of the version push.
- Evidence of the change: "no visible change" (process text only).
- The PR's own body ticks the new checkbox with "No user-facing change".

## Open questions

None.
