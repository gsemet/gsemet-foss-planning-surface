Head: a49d89ba030f20210a318e5001cecfad2f162c13

Quiet window: no local run of check, test, scenario, gate, eval-dry-run. Proof by code reading and CI.
All claims judged at a49d89ba.

- Journal-only set (sec.1): `hub/journal.py::seen_merged` is pure, filters `_listed`, type merged@1, batch, cr, pr == link_of(c.pr). Command: git diff origin/main...HEAD -- hub/journal.py. VERIFIED by reading.
- landed threaded through stacks.py (below_with_pr, nearest_open, open_after, live_start, top_cr, series predecessor, start_on_for, stack_start, start_base), default empty frozenset; stack_base/off_place/etc. untouched. stacks.py does not import hub.journal (imports: core, rails). VERIFIED by reading the diff.
- take reads journal once, passes to start_on_for and cr_facts; rails untouched (diff of commands/driver.py). `_base_of` uses start_base with landed; `_landed_line` prints the spec's `base:` line only when the set changed the base. VERIFIED by reading.
- No forge call: `git diff origin/main...HEAD -- skills/chantier/scripts/cli/src | grep -E '^\+' | grep -nE 'gh|glab|connectors|pr_state|read_state'` -> empty output. VERIFIED.
- Word rules (sec.2): stack_words.py implements placed/release/no-base = chain rule; default -> ready to merge; open CR -> recursive word with loop guard; merged -> chain; other -> PR in draft; draft_waited split as specified. Moved from stacks.py with same signatures (stated in PR). VERIFIED by reading.
- Cards (sec.3): concepts.md (Words, Stack, Dependencies), foreman.md, driver.md diffs match the spec; chief-of-staff/status-layout/routing/agents untouched (diff --stat). VERIFIED.
- Scenario (sec.4): run_scenario.py has checks 1-10 and README updated (grep of added check labels). Execution proof: PENDING, see below.
- Tests (sec.5): test_stack_base.py +153 lines, test_stack_hold.py adjusted; execution proof is CI `just check`.
- PR description: renders, Summary/Deliverables/Changes match the diff, no images, Known gaps names the freshness limit and the scenario budget overrun. No Review box. VERIFIED.
- CI at head (gh pr checks 391): just check ubuntu pass, just eval-dry-run ubuntu pass; just check macos/windows and just scenario ubuntu still in_progress at time of writing.

Not proven (needs CI result): scenario checks 1-10 and just check macOS/Windows. Known gap in PR: scenario stack unit exceeded its 640 s budget locally (1196.8 s beside just check); if CI scenario fails on the budget, the claim fails.

NOT VERIFIED (pending: scenario and cross-platform CI not yet green at the head)
