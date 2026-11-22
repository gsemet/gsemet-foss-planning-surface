# Verify CR-443

Head: 1353bbdbb9d4bc59c9a4ee31c654c4a39807b106

All claims judged at 1353bbd, the pushed head, with the CLI of the worktree (`uv run --no-sync --project <worktree> chantier`)
on a scratch project (own git repo, one CR taken, a worktree on a scratch branch), removed at the end.

## Gate cells of the matrix (scratch project, 1353bbd)

- No entry, `gate CR-101 tests` and `gate CR-101 "just scenario"`: exit 2, `error: gate CR-101: chantier.yaml names no long gate; add to the code repository's root chantier.yaml:` then `long_gate:` / `  commands:` / `    <name>: <the long gate's command>` / `(the Chief of Staff offers it to the user)`. `playbook`: `long gate: none named in chantier.yaml (long_gate.commands)`. PASS.
- `gate CR-101 --stop` with no entry: `no long gate running for CR-101: nothing to stop`, exit 0. `--stop tests`: `gate CR-101 --stop takes no name`, exit 1. `gate CR-101`: `gate <cr> <name> [<name>...]: the long gate's names ...`, exit 1. PASS.
- Entry set (a, bad, c) in the main checkout's root: `playbook` prints `long gate: a (...), bad (...), c (...) (chantier.yaml: long_gate.commands)`. `gate CR-101 "just scenario"` and `gate CR-101 nope`: exit 1, `"<word>" is not a long gate named in chantier.yaml (long_gate.commands); named: a, bad, c`; `log` then holds no `gate` event for them (only the two runs below). PASS.
- `gate CR-101 a`: `pass python -c ... at e6d01a1`, exit 0, event carries `command=... name=a`. `gate CR-101 bad c`: `FAIL ... (exit 3)`, c never ran, exit 4, event `name=bad`. `gate CR-101 a c`: pass a then pass c, exit 0. PASS.
- Bad key, `long_gate:\n  slots: 2`: `chantier.yaml:2: long_gate: unknown key "slots": one of parallel, commands`, exit 2, before the name check. PASS.
- A worktree's own committed `chantier.yaml` naming `a` as `WORKTREE a`: `gate CR-101 a` still ran `ran a` (root file read). PASS.
- Surface-only `long_gate.commands` ignored and `parallel` merged: proved by `test_a_surface_layers_commands_are_ignored_but_its_parallel_merges` (below), not by a hand probe.

## Lease hold cells (scratch project, 1353bbd)

- `lease CR-101 hold --lease 1`: `live until 03:09:32 (renewed 02:24:32)`: 45 minutes. `--minutes 90`: `live until 03:54:33 (renewed 02:24:33)`. PASS.
- `--minutes 0` and `--minutes 91`: exit 1, `is a whole number from 1 to 90`. `-- echo hi`: exit 1, `hold runs no command: start your wait yourself, then run lease CR-101 hold --lease <n>`. PASS.
- `lease CR-101 renew --lease 1` after the 90-minute hold: `live until 03:54:33 (renewed 02:24:35)`: not shortened. `find .agents -name '.lease-hold*'`: none. PASS.
- Hold lapse, "not confirmed", and the stack's `lease-late`: not probed by hand (no sleep allowed); carried from the pushed gate log `work/gates/20261122-030047.log` (first line `gate CR-443 ... head 1353bbdbb9d4bc59c9a4ee31c654c4a39807b106`, last line `result: pass at 1353bbdbb9d4bc59c9a4ee31c654c4a39807b106`), whose transcript shows `after the hold lapses, lease says not confirmed`, `after a lease stack hold lapses, lease stack says not confirmed`, and `a command with the same --lease on stack is accepted, and the log says lease-late`, plus `"just scenario" is not a long gate named in chantier.yaml`. PASS.

## Tests and shipped state (1353bbd)

- `pytest test_gate_refusals.py test_lease_hold.py test_leases.py test_playbook_layers.py test_carry_ship.py`: `76 passed in 96.94s`. PASS.
- `pytest -k "shipped or root_chantier or sandbox or fixture"`: `51 passed`. Root `chantier.yaml` holds `long_gate.commands.scenario: just scenario`; `AGENTS.md` line 10 names `chantier gate <cr> scenario`; `.lease-hold.*.run` stays only in `core/files.py` `IGNORED` (grep of the tree). PASS.
- `validate` on the live planning folder: gaps only for `6-trash` items, no failure.

## PR description (as posted, `gh pr view 416`, head 1353bbd)

- Body equals `work/pr-body.md` (the only diff is a trailing line). Renders: Summary, Deliverables, fold with a blank line after `</summary>` and before `</details>`, nothing after it. No images.
- Matches the diff (`git diff --stat <base>..HEAD`, 53 files): new `long_gate.commands` key and `playbook`/`validate` lines, `gate` by name, `lease hold` without a command, `holds` gone from the board, TUI and `docs/server-api.md`, root `chantier.yaml`, `AGENTS.md`, cards, docs, eval kit files and `sandbox.json`, tests, scenario. Before-you-update paragraph, API change, `sandbox.py reset --yes` and the known limit are present. Role names (Coder, read-only roles) are product terms of chantier's own repository; CR name only under Internal references.
- Known gaps names the free-form local gate; no `UNVERIFIED`/`STALE` mark left. Test plan names `1353bbd`; `Verified at <sha7>` and `CI green at <sha7>` are open boxes for the Driver.
- Review box `Review: approved at 1353bbd`: the log's note `r3 approved at ce00b809..., committed as 1353bbdb...` covers it (the round's committed-as SHA).

## Evidence

No visual change: no screenshots; no before/after pair (the proofs are the command outputs above). Scratch removed.

VERIFIED
