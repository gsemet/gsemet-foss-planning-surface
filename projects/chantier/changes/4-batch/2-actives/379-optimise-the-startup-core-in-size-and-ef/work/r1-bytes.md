# CR-379 r1: startup bytes, base (CR-375 landed) vs after

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

Tightest after: 8664 ([('chief-of-staff', 'copilot')]); goal 11,290: held. Tightest before: 12502.

## Moved and merged rules, as landed

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
