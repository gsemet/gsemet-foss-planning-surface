# "The user's boundaries": label to final home

The labels of the specification's section 4. Rows are `FM-` rows of `cards-inventory-foreman.md`. `card:N` is `cards-next/foreman.md:N`; `floor N` is `cards-next/floor.md:N+4`; a file with no folder named here is under the CLI's `src/chantier/`.

| label | protects | rows | final home | topic |
| --- | --- | --- | --- | --- |
| B1a | yes | B001, B003 | floor 1; card:20, card:15 (`judge` words the ask) | - |
| B1b | no | B002 | `judge` carries no icon: the rule disappears (card:15) | - |
| B1c | yes | B063 | refusals `check_shape`, `shape_refusal` (`rails_release.py:192`, `:178`); `judge` prints `no ask:` (`commands/judge.py:58`); card:15 | `stack` |
| B1d | yes | B004, B005 | card:15, card:21; `judge` appends the gaps (`status/judge_words.py:99`) | - |
| B1e | yes | B006 | floor 8; card:15. Known gap: `judge` does not carry an image note | - |
| B1f | yes | B007 | card:21 | `take-back` |
| B1g | no | B008 | topic only | `orders` |
| B1h | yes | B009, B010, B013 | card:21 (B013: topic) | `long-gate`, `local-gate` |
| B1i | yes | B011, B012, B014 | card:21 (B012: Copilot host row) | `local-gate` |
| B1j | yes | B015-B017, B019, B022 | card:21, card:15; `judge --local-gate` (`status/judge_words.py:33`); B017: Copilot host row, B022: topic | `local-gate` |
| B1k | no | B020, B021 | topic; card:21 points to it | `local-gate` |
| B1l | yes | B023 | card:21 | `long-gate` |
| B1m | yes | B024 | card:21 ("An absent gate never means success.") | `long-gate` |
| B1n | yes | B025-B032 | card:21, card:15; `judge --local-gate` (`status/judge_words.py:33`); B032: topic | `long-gate-waiver`, `local-gate` |
| B1o | yes | B033, B034 | floor 1, 6; card:20; refusal `release go`: "no grant for: …; the user merges it" (`commands/release.py:81`), "no approval for: …" (`:84`) | `merge-under-grant` |
| B1p | yes | B018, B035 | floor 1, 6; card:20, card:21; refusal `check_granted_fix` (`rails_release.py:108`) | `merge-under-grant`, `main-checkout` |
| B2 | yes | B036, B037 | refusals `check_slot`, `check_budget`, `check_round` (`rails.py:57`, `:222`, `:305`); floor 9 | - |
| B2b | no | B038 | topic only | `escalation` |
| B3 | no | B039 | none (inferable: the refusals name the next command) | - |
| B4 | no | B040-B042 | topic only | `orders` |
| B5a | yes | B043, B044 | card:14; floor 7; refusal "cannot pause <batch>: …" (`commands/closing.py:95`) | `orders` |
| B5b | yes | B045 | refusal "cancel <cr>: no destination recorded; …" (`commands/release.py:137`) | `orders` |
| B5c | yes | B046-B051 | card:29; refusal "<cr> is <status>: a Driver takes it back only with `--note` …" (`rails.py:249`); B047-B051: inferable or topic | `take-back` |
| B5d | no | B052 | topic only | `take-back` |
| B6 | yes | B053, B054 | card:24, with "stop" and "hold" only (the third case is dropped, answer 8) | - |
| B7a | yes | B055 | card:22 | - |
| B7b | yes (the named exception) | B056, B065 | card:22 | `drop` |
| B7c | yes | B057-B059 | card:22, card:25; floor 5; B057: topic | `cleanup` |
| B7d | yes | B060, B062 | card:22; floor 5 | `main-checkout` |
| B7e | yes | B061 | `chantier conflicts` runs the check (`commands/conflicts.py`); card:22 bounds the Foreman's git; floor 5 | `conflict-check` |
| B7f | yes | B064 | card:22 | `refused-push`, `refused-rebase` |
