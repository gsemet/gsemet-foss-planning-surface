## Summary

Every session and agent reads the startup core whole at each boot and reload, and the 12,544-byte limit was nearly reached (the tightest role was at 12,502). The limit stays; the core is now smaller and sharper: each boot rule is said once, the key rules come first in each file, and what one action needs is read at that action. The tightest role and host now reads 8,664 bytes at reload (goal: at most 11,290).

## Deliverables

Startup bytes, tightest role and host, boot and reload (the test's own LF count, `pytest -s -k measures`), before at the base and after at the head:

| | before | after |
| --- | --- | --- |
| tightest reload (router, Copilot, before; Chief of Staff, Copilot, after) | 12,502 | 8,664 |
| Chief of Staff, Copilot, boot | 11,742 | 7,870 |
| Foreman, Claude Code, boot | 10,282 | 5,807 |

Every role and host: a drop of roughly 3,800 to 4,500 bytes at boot and reload; the full table is in Changes. No rule is dropped; the moved and merged rules are listed under Changes. Judged at dd6f84d (verdict carried from a1d165d).

Choices: the manifest is compact (version 2, paths relative to its folder, `file#heading` readings, one startup section per role that has one); the key rules (stop on a CLI failure, no fallback, the seat, the watcher's start) come first in their file; `$CHANTIER` is written in full in each shell call, never in a shell variable.

**UNVERIFIED:** a boot and a reload from a real Claude Code session at this head; see Known gaps.

## Blast radius

Grade: 2

Every role reads these files at boot, so a wrong reading would be noticed at the first start of a session; the limit test and the structure tests guard the sizes and the moved rules. Rollback: revert the PR.

## Autonomous decisions

- A full stop added in the Foreman card's startup sentence so "and the project's rules" does not dangle after the rewording.
- Constants added in the manifest test for the new manifest form; the limit constants are untouched.

## Known gaps

- No screenshot or session proof yet: a real Claude Code boot, reload and Driver start at this head are not captured (UNVERIFIED).
- No real Copilot session at the head.
- zsh and sh/dash were not run for the shell-variable rule (zsh not at hand).
- The router's reload sentence still says "nothing else of this file" although a reload now reads its startup section; left as specified; a follow-up change would close it.

<details>
<summary>Details</summary>

## Changes

- `startup-core.md` rewritten (CLI stop, no fallback, shell-variable rule, report sentence); `role-core.md` holds the deferral rule once; the host cores lose a sentence the common core says.
- `startup-manifest.json` version 2; `startup_sections` replaces `mandatory_sections`.
- The twelve cards lose their boilerplate startup line (emptied sections go); the four `SKILL.md` files put the key rule first under `## Startup core`; both hosts' agent files get one shorter reading sentence, bodies identical.
- Tests: manifest test adapted to version 2, a moved-rules test, the one-launch test extended with the shell-variable rule.

### Startup bytes at dd6f84d, every role and host (LF bytes, `pytest -s -k measures`)

| role | host | boot before | boot after | reload before | reload after |
| --- | --- | --- | --- | --- | --- |
| chief-of-staff | claude | 11736 | 7864 | 12479 | 8658 |
| chief-of-staff | copilot | 11742 | 7870 | 12485 | 8664 |
| coder | claude | 10424 | 6598 | 11167 | 7392 |
| coder | copilot | 10458 | 6632 | 11201 | 7426 |
| conflict-resolver | claude | 10529 | 6703 | 11272 | 7497 |
| conflict-resolver | copilot | 10590 | 6764 | 11333 | 7558 |
| cr-driver | claude | 10359 | 6550 | 11102 | 7344 |
| cr-driver | copilot | 10425 | 6616 | 11168 | 7410 |
| debugger | claude | 10457 | 6631 | 11200 | 7425 |
| debugger | copilot | 10524 | 6698 | 11267 | 7492 |
| demo-explorer | claude | 10523 | 6697 | 11266 | 7491 |
| demo-explorer | copilot | 10588 | 6762 | 11331 | 7556 |
| foreman | claude | 10282 | 5807 | 11025 | 6601 |
| foreman | copilot | 10428 | 5988 | 11171 | 6782 |
| griller | claude | 11476 | 7401 | 12219 | 8195 |
| griller | copilot | 11482 | 7407 | 12225 | 8201 |
| inspector | claude | 10445 | 6619 | 11188 | 7413 |
| inspector | copilot | 10507 | 6681 | 11250 | 7475 |
| investigator | claude | 10473 | 6647 | 11216 | 7441 |
| investigator | copilot | 10538 | 6712 | 11281 | 7506 |
| qa-driver | claude | 10344 | 6535 | 11087 | 7329 |
| qa-driver | copilot | 10414 | 6605 | 11157 | 7399 |
| release-driver | claude | 10417 | 6608 | 11160 | 7402 |
| release-driver | copilot | 10477 | 6668 | 11220 | 7462 |
| retro-critic | claude | 10211 | 6385 | 10954 | 7179 |
| retro-critic | copilot | 10283 | 6457 | 11026 | 7251 |
| router | claude | 11753 | 7429 | 12496 | 8223 |
| router | copilot | 11759 | 7435 | 12502 | 8229 |
| spec-critic | claude | 10146 | 6320 | 10889 | 7114 |
| spec-critic | copilot | 10218 | 6392 | 10961 | 7186 |
| spec-writer | claude | 10125 | 6299 | 10868 | 7093 |
| spec-writer | copilot | 10198 | 6372 | 10941 | 7166 |
| stack-driver | claude | 10403 | 6594 | 11146 | 7388 |
| stack-driver | copilot | 10465 | 6656 | 11208 | 7450 |
| status | claude | 11571 | 7607 | 12314 | 8401 |
| status | copilot | 11577 | 7613 | 12320 | 8407 |
| verifier | claude | 10449 | 6623 | 11192 | 7417 |
| verifier | copilot | 10516 | 6690 | 11259 | 7484 |

### Moved and merged rules

| Rule | Now |
| --- | --- |
| Deferral (read the core at boot, the rest at the action) | `role-core.md`, once; removed from `startup-core.md` opening, agent files, card boilerplates (12 cards), `SKILL.md` boilerplates, `concepts.md` and host cards |
| What a worker reads at startup | coder, inspector, verifier, demo-explorer: "At startup read the startup core; defer ..." |
| What the Foreman reads at startup / after compaction | `foreman.md` lines 3 and 10-15, Foreman start prompt in `chief-of-staff.md`: startup sections of `concepts.md` and `hosts/<host>.md`; `foreman.md` is the `batch` action reading, its own section gone |
| Reload repeats no grant, starts no service twice | `session-start.md` "5. Reload", Does |
| A host path not exercised is labelled untested | `startup-core.md` (both host cores lose "Availability is not proof...") |
| failed/unavailable/not performed; available/documented/... lists | `startup-core.md`, the report sentence |
| `$CHANTIER` prepared only as skill/prompt gives it | `startup-core.md`, first paragraph |
| No fallback | `startup-core.md`, second paragraph (cards keep theirs) |
| `$CHANTIER` in full, never in a shell variable | `startup-core.md`, first paragraph; test in `test_plugin_files.py::test_one_launch_two_modes_one_text` |
| Zero configuration + CR archive in its PR when the project asks | `session-start.md` "4. First turn", Zero configuration; router's, Griller's, status's "Nothing to install" sentences cut (Griller keeps writes sentence) |
| Read `session-start.md` at the session's start | Chief of Staff's and Griller's `SKILL.md`, under `## Startup core` |
| A prompt names the card and section the role reads | `concepts.md`, beside the prompt template |
| concepts intro; host cards' "What is proper to this host" | above their `## Startup core`, unchanged |
| Router seat bullets; CoS watcher line; status "You change nothing" | first under each `SKILL.md`'s `## Startup core` |

## Human decisions

- The 12K limit stays; the core is optimised in size and efficiency.
- Target: every role and host at most 10% under the limit.

## Impacts

No visual change; every session reads about 4,000 fewer bytes at boot and reload.

## Test plan

- [x] New or changed tests (the manifest test now reads version 2, the moved-rules test and the shell-variable rule fail on the previous files), at `dd6f84d` (carried from a1d165d)
- [x] Local gates at `dd6f84d` (carried from a1d165d): `just check` passed (ruff, mypy, uv lock, biome, 688 tests, release notes); `pytest -s -k measures` tightest 8,664 bytes
- [x] Shells, the literal command `<cli> --version` at `dd6f84d` (carried from a1d165d): PowerShell 5.1 runs (`chantier 0.13.0`); bash runs; a quoted path kept in a bash variable fails ("Project directory ... does not exist", the quotes stay characters); sh/dash at hand, not run; zsh not at hand
- [ ] Evidence: real Claude Code boot, reload and Driver start at the head (not captured)
- [x] Review: approved, carried from a1d165d by a clean rebase to `dd6f84d`
- [x] Verified, carried from a1d165d by a clean rebase to `dd6f84d`
- [x] CI green at `dd6f84d` (5 jobs)

## Internal references

- CR-379 startup-core-optimise; folds in portable-cli-invocation.

</details>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
