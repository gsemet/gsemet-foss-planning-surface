# Verify CR-405

Head: 40363bd70a131c7255050c3fa84dcf65a7af780e

Verdict: VERIFIED (second pass: code carried from 40363bd, description re-checked at 40363bd)

Claims, each judged at 40363bd (the pushed head, `git rev-parse HEAD` in the worktree).

1. Spec section 8 tests exist and pass. Command (cwd skills/chantier/scripts/cli, PYTHONPATH=src of the worktree, because the shared venv's editable install points at the main checkout):
   `python -m pytest tests/test_connectors.py tests/test_hub_connectors.py tests/test_forge_hub.py tests/test_board_prs_unclaimed.py tests/test_board_prs.py tests/test_watch_events.py -q`
   Output: `130 passed in 37.34s`. Collected: 67 tests in the three new files.
   Forge matrix cells map to tests: GitHub/GitLab hub, one query, today's text: `test_the_query_with_no_optional_fact_is_the_one_read_before_the_connectors`, `test_a_gitlab_batch_is_read_in_one_query_and_told_as_before`; review asked: `test_an_interest_asking_review_makes_the_one_query_carry_it...[github|gitlab]`, `test_review_is_asked_of_github_and_its_four_answers_map_to_words[x4]`, `test_review_is_unproved_on_gitlab_with_the_same_query`; Enterprise host: `test_the_argv_is_a_graphql_query_and_names_a_host_other_than_the_forges_own[x2]`; unclaimed link: `test_a_link_no_connector_claims_is_named_and_the_other_prs_are_read_and_judged`, `test_a_link_no_connector_claims_is_not_read`, `test_board_prs_unclaimed`; two repositories: `test_a_batch_in_two_repositories_is_not_read_and_the_entry_says_so`; two providers one call, other-kind provider not called: the two matching tests in `test_hub_connectors.py`.
   Note: the spec put the page's unclaimed case in `test_board_prs.py`; it is in `test_board_prs_unclaimed.py` (disclosed in the PR's Autonomous decisions). Accepted.
2. The guard refuses a mutation and a non-graphql argv. Command: `run.guard(argv)` on prepared argvs. Output:
   mutation only -> `refused a connector sends a query`; query plus mutation -> `refused a connector never sends a mutation`; `['pr','list']` -> `refused a connector runs only api [--hostname <host>] graphql`; `api repos/x` -> refused; `api --hostname h graphql -f query=query { a }` -> accepted.
3. No reference to `board.forge_read`. Command: `git grep -n "forge_read"`. Output: only `tests/test_watch_events.py:149,154`, a local test function named `forge_read_called` that monkeypatches `connectors.read`; no module reference. `board/forge_read.py` and `test_board_forge_read.py` are deleted in the diff.
4. AGENTS.md, docs and cards match spec 6. Command: `git diff origin/main...HEAD -- AGENTS.md docs/hosts.md skills/chantier/references`; diff stat also shows `docs/forge-connectors.md` (new, 57 lines), `README.md` (+1), `docs/web-board.md`. AGENTS.md edits 1 and 2 are word for word spec 6.1; hosts.md has the Connector column and sentence; concepts.md has Connector and Interest; session-start.md has the "only the PRs a running batch waits for" addition. Passes.
5. GitHub reviewDecision proof: `evidence/review-decision-proof.md` holds two real reads (gsemet/okf-schema PR 55, required_approving_review_count=1: REVIEW_REQUIRED; gsemet/chantier PR 374, count 0: null). Matches the expected answers of spec 3.2 and the mapping in `connectors/github.py` tested above. Judged, not rerun. Minor: the recorded command text omits `state` while the output shows it (abbreviated command); not blocking.
6. Unclaimed-link text and hub behaviour: `connectors.UNCLAIMED = "no connector reads {link}: chantier reads GitHub and GitLab"` (exact spec 5 text); asserted in `test_connectors.py:193`, hub and page tests pass (claim 1).
7. PR description vs diff, re-checked at 40363bd (second pass). Command: `gh pr view 375 --json body,headRefOid`; headRefOid = 40363bd70a131c7255050c3fa84dcf65a7af780e.
   - Summary, Deliverables, Changes match the diff (carried claim 4 and the diff stat): connectors package, hub interests, docs, cards, AGENTS.md. No change unmentioned.
   - Known gaps no longer holds the stale UNVERIFIED bullet (the reviewDecision proof is in evidence, claim 5); it names one real residual (second hub error replaces the first). No UNVERIFIED claim remains, none needed.
   - Test plan has no placeholders; SHAs are 40363bd. Review box: `chantier log` has `inspector approved at 40363bd70a13...` (move f5e1365b..40363bd7), matches. Gates box: gate pass at 40363bd (claim 8). CI box: log note "CI green 5/5 at 40363bd7". Renders: sections, fold with blank line after summary, mermaid block, no images, no STALE mark.
   - Two boxes stay unchecked: tests (proved by claim 1, carried from 40363bd; the Driver may tick it) and Verified (this pass). Not a failure.
8. Gate: `chantier log` shows `gate result=pass head=40363bd70a131c7255050c3fa84dcf65a7af780e command=just scenario`.

No before/after evidence captured: no UI change (the PR says "No visual change").

VERIFIED.

9. Description-only pass (third), at 40363bd70a131c7255050c3fa84dcf65a7af780e: `gh pr view 375 --json body,headRefOid` gives headRefOid 40363bd; body has all boxes ticked, SHAs 40363bd, no placeholder or STALE, Known gaps matches claim 7, Summary/Changes match the diff stat; Review note present in `chantier log`. VERIFIED.
