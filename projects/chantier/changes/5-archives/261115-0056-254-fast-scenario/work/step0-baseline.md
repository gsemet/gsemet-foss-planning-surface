# Step 0 baseline

Today's scenario (main 4ecc7cd plus the timing instrumentation, d5a68c7), one run per forge on the user's Windows machine (Ryzen 7 7800X3D), the two runs started at the same time. A command is a process the scenario starts itself.

## GitHub: 895/895 checks, 1472.9 s, 2761 commands

| case or section | seconds | commands |
| --- | ---: | ---: |
| build | 1.1 | 8 |
| section 1. Setup and preflight | 6.7 | 9 |
| section 2. The Chief of Staff opens the batch and starts the Foreman | 17.6 | 42 |
| section 3. CR-101: one round, the Driver's own push and PR, hand-back | 11.4 | 23 |
| section 4. CR-102: two rounds | 13.4 | 27 |
| section 5. Steering: the user drops CR-103, adds an item, changes CR-101 | 8.2 | 18 |
| section 6. A Foreman restart: the old one is refused | 2.0 | 4 |
| section 7. CR-104 is lost, then hands back; CR-105 and CR-101 run | 20.8 | 39 |
| section 8. The user merges; the Foreman cleans up and pauses the batch | 21.6 | 113 |
| section 9. Cost | 6.5 | 13 |
| section 10. Copilot cost | 4.1 | 8 |
| section 11. Event log | 0.0 | 0 |
| close_batch | 27.3 | 56 |
| retro_cases | 15.9 | 31 |
| copilot_missing_transcript | 2.0 | 4 |
| lifecycle_regressions | 1.5 | 4 |
| stack_batch | 68.4 | 169 |
| forge_stack_cli | 43.9 | 65 |
| ready_words | 77.9 | 166 |
| batch_modes | 54.0 | 111 |
| release | 70.4 | 158 |
| granted_fixes | 19.5 | 33 |
| release_last | 44.4 | 88 |
| release_on_stack | 112.7 | 236 |
| qa_on_head | 11.8 | 24 |
| old_words | 7.9 | 16 |
| changes_tree | 24.0 | 57 |
| old_tree | 22.7 | 47 |
| next_number | 2.4 | 5 |
| backfill_cases | 2.1 | 4 |
| dependencies | 59.1 | 99 |
| release_merge_on_approval | 21.3 | 39 |
| lost_messages | 45.8 | 75 |
| failed_opening | 2.5 | 4 |
| playbook_config | 53.6 | 81 |
| cancel_during_gate | 6.3 | 11 |
| stop_own_gate | 28.7 | 45 |
| rails | 71.2 | 72 |
| gate_parallel | 61.3 | 63 |
| handback_proofs | 44.4 | 71 |
| gate_proof | 71.1 | 137 |
| restore_cr | 14.5 | 25 |
| driver_liveness | 23.5 | 48 |
| foreman_in_a_worktree | 4.2 | 11 |
| direct_batch | 75.5 | 150 |
| seat_handover | 10.3 | 18 |
| remote_board | 62.6 | 64 |
| external_surface | 64.6 | 106 |
| cr_summary | 29.7 | 63 |
| total of the rows | 1472.3 | 2760 |
| whole run | 1472.9 | 2761 |

## GitLab: 873/873 checks, 1456.3 s, 2738 commands

| case or section | seconds | commands |
| --- | ---: | ---: |
| build | 1.1 | 8 |
| section 1. Setup and preflight | 4.8 | 7 |
| section 2. The Chief of Staff opens the batch and starts the Foreman | 17.4 | 42 |
| section 3. CR-101: one round, the Driver's own push and PR, hand-back | 11.2 | 23 |
| section 4. CR-102: two rounds | 12.9 | 27 |
| section 5. Steering: the user drops CR-103, adds an item, changes CR-101 | 8.2 | 18 |
| section 6. A Foreman restart: the old one is refused | 2.2 | 4 |
| section 7. CR-104 is lost, then hands back; CR-105 and CR-101 run | 20.7 | 39 |
| section 8. The user merges; the Foreman cleans up and pauses the batch | 22.8 | 113 |
| section 9. Cost | 6.6 | 13 |
| section 10. Copilot cost | 4.4 | 8 |
| section 11. Event log | 0.0 | 0 |
| close_batch | 27.3 | 56 |
| retro_cases | 16.1 | 31 |
| copilot_missing_transcript | 2.0 | 4 |
| lifecycle_regressions | 1.6 | 4 |
| stack_batch | 69.0 | 167 |
| forge_stack_cli | 33.4 | 46 |
| ready_words | 77.1 | 166 |
| batch_modes | 53.9 | 111 |
| release | 68.2 | 158 |
| granted_fixes | 18.8 | 33 |
| release_last | 45.6 | 88 |
| release_on_stack | 112.1 | 236 |
| qa_on_head | 11.5 | 24 |
| old_words | 7.4 | 16 |
| changes_tree | 23.6 | 57 |
| old_tree | 22.3 | 47 |
| next_number | 2.1 | 5 |
| backfill_cases | 1.7 | 4 |
| dependencies | 56.9 | 99 |
| release_merge_on_approval | 21.1 | 39 |
| lost_messages | 44.8 | 75 |
| failed_opening | 2.7 | 4 |
| playbook_config | 54.1 | 81 |
| cancel_during_gate | 6.7 | 11 |
| stop_own_gate | 29.1 | 45 |
| rails | 72.7 | 72 |
| gate_parallel | 58.8 | 63 |
| handback_proofs | 45.9 | 71 |
| gate_proof | 72.5 | 137 |
| restore_cr | 14.9 | 25 |
| driver_liveness | 25.4 | 48 |
| foreman_in_a_worktree | 4.1 | 11 |
| direct_batch | 73.7 | 150 |
| seat_handover | 9.7 | 18 |
| remote_board | 62.7 | 64 |
| external_surface | 62.7 | 106 |
| cr_summary | 31.0 | 63 |
| total of the rows | 1455.5 | 2737 |
| whole run | 1456.3 | 2738 |

No firewall prompt was seen by the Driver (a background run; the user's screen was not watched).

